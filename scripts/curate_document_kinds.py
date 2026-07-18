"""Map each jurisdiction's registry documents onto the three German document kinds.

STP works in German cases. For a foreign company they need to know which of the
delivered documents plays the role that the Registerauszug, the Gesellschafterliste and
the Gesellschaftsvertrag play in a German case. That is a question about FUNCTION, not
about names: the shareholder list is "CS01" in the UK, "List of Shareholders" in
Thailand, part of the "Certidao" in Portugal, and in Austria and the Netherlands it is
not a document at all — it is the shareholder fields carried inside the registry extract.
No string matching gets you from one to the other, so the equivalence table below is
hand-authored and this script only validates it and reports what is still open.

Germany is deliberately absent: we serve DE from our own stack (Northdata /
handelsregister / Transparenzregister) and never order it from KYC.com, so the matrix's
DE row is out of scope here.

Run (no app or network needed — reads the committed matrix):
    python scripts/curate_document_kinds.py

Writes curation/document_kinds_curation.json and prints a coverage summary naming every
unresolved jurisdiction. Unresolved is the honest default: a jurisdiction is only mapped
when someone knew what the local document actually is. Do not fill gaps by guessing from
the label text — that is exactly the failure this table exists to prevent.
"""
import os, json, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATRIX = os.path.join(ROOT, "jurisdiction_matrix.json")
OUT = os.path.join(ROOT, "curation", "document_kinds_curation.json")

# The three roles, named as STP names them.
REGISTERAUSZUG = "REGISTERAUSZUG"
GESELLSCHAFTERLISTE = "GESELLSCHAFTERLISTE"
GESELLSCHAFTSVERTRAG = "GESELLSCHAFTSVERTRAG"
KINDS = (REGISTERAUSZUG, GESELLSCHAFTERLISTE, GESELLSCHAFTSVERTRAG)

# Labels that carry the same role in every jurisdiction that lists them. Kept
# deliberately short: only labels whose meaning does not shift across registries.
# "Certificate of Incorporation" is NOT here — it evidences incorporation, it is not an
# extract of the current register entry, and treating it as one silently answers the
# wrong question.
GLOBAL = {
    "Registry Extract": REGISTERAUSZUG,
    "Registry Extract_English": REGISTERAUSZUG,
    "Registration Extract": REGISTERAUSZUG,
    "Company Registration Extract": REGISTERAUSZUG,
    "Registry Report": REGISTERAUSZUG,
    "Register Report": REGISTERAUSZUG,
    "Historical Registry Extract": REGISTERAUSZUG,
    "Articles of Association": GESELLSCHAFTSVERTRAG,
    "Articles of association": GESELLSCHAFTSVERTRAG,
    "Articles Of Association": GESELLSCHAFTSVERTRAG,
    "Memorandum & Articles of Association": GESELLSCHAFTSVERTRAG,
    "Memorandum and Articles of Association": GESELLSCHAFTSVERTRAG,
    "Memorandum And Articles Of Association": GESELLSCHAFTSVERTRAG,
    "Memorandum and Articles": GESELLSCHAFTSVERTRAG,
    "List of Shareholders": GESELLSCHAFTERLISTE,
}

# Per-jurisdiction equivalences that GLOBAL cannot express, because the local document
# is named nothing like the German one. {code: {kind: [labels]}}. Each entry is a
# judgment call and is listed in curation/README.md for sign-off.
OVERRIDE = {
    # CS01 is DELIBERATELY NOT mapped to REGISTERAUSZUG or GESELLSCHAFTERLISTE. Research
    # (see curation/document_kinds_evidence.json, GB rows) established: GB has no register
    # extract at all, and the CS01 reports only CHANGES since the last statement
    # (CA 2006 s.853F(4)) — it is not a standing shareholder list and is not
    # self-describing. Only the articles are a genuine document.
    "GB": {GESELLSCHAFTSVERTRAG: ["Memorandum and Articles of Association"]},
    # "Aktuelle Fassung" is the consolidated current text of the Gesellschaftsvertrag.
    "AT": {GESELLSCHAFTSVERTRAG: ["Gesellschaftsvertrag (social contract)",
                                  "Aktuelle Fassung (Current version)"]},
    "CH": {GESELLSCHAFTSVERTRAG: ["Statutes - certified"],
           REGISTERAUSZUG: ["Commercial register extrait - certified"]},
    "NL": {GESELLSCHAFTSVERTRAG: [
        "Documenten zoals statuten, fusie- ofsplitsingsvoorstellen "
        "(Documents such as articles of association, merger or division proposals)"]},
    "PT": {GESELLSCHAFTSVERTRAG: [
        "Certidão do Último Pacto Social/Estatutos Actualizados "
        "(Certificate of the Last Articles of Association/Updated Statutes)"]},
    "TH": {REGISTERAUSZUG: ["Company Information Report"]},
}


def norm(s):
    """Normalized label key: the API's spelling and the matrix's differ in case,
    &/and, and stray punctuation (API 'Registration certificate' vs matrix
    'Registration Certificate'; matrix holds '- Incorporation' with a leading dash)."""
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower().replace("&", "and")).strip()


def merged_by_code(m):
    """One entry per jurisdiction, not per matrix row. Several registries can share a
    code — 'HK CR'/'HK IRD', 'Viet Nam - NBR'/'- GDT', 'Philippines SEC'/'DTI', two
    Seychelles rows — and each lists only its own documents. Counting rows would report
    HK twice and hide half its documents behind whichever row was seen first."""
    out = {}
    for j in m["jurisdictions"]:
        code = j.get("code")
        if not code or code == "DE":
            continue
        e = out.setdefault(code, {"code": code, "documentsMandatory": [],
                                  "documentsNonMandatory": [], "shareholders": [],
                                  "rows": []})
        e["rows"].append(j.get("name"))
        for k in ("documentsMandatory", "documentsNonMandatory"):
            e[k].extend(l for l in (j.get(k) or []) if l not in e[k])
        e["shareholders"].extend(s for s in (j.get("shareholders") or [])
                                 if s not in e["shareholders"])
    return out


def main():
    m = json.load(open(MATRIX, encoding="utf-8"))
    merged = merged_by_code(m)
    rows = [merged[c] for c in sorted(merged)]
    global_norm = {norm(k): v for k, v in GLOBAL.items()}

    out, unresolved = [], {k: [] for k in KINDS}
    for j in rows:
        code = j["code"]
        base = list(j.get("documentsMandatory") or [])
        extra = list(j.get("documentsNonMandatory") or [])
        ov = OVERRIDE.get(code, {})
        # every label this jurisdiction can deliver, with its billing tier
        tier = {norm(l): ("base", l) for l in base}
        tier.update({norm(l): ("additional", l) for l in extra if norm(l) not in tier})

        for kind in KINDS:
            # OVERRIDE ADDS TO the global matches, it does not replace them. Replacing
            # them let a hand-written entry demote a base document to 'additional' —
            # e.g. CH's base 'Registry Extract' was being shadowed by the curated
            # 'Commercial register extrait - certified', which is an extra-cost order.
            hits = []
            for lbl in ov.get(kind, []):
                if norm(lbl) not in tier:
                    raise SystemExit(
                        f"OVERRIDE[{code}][{kind}] names {lbl!r}, which {code} does not "
                        f"list. Fix the table — a typo here silently drops the mapping.")
                hits.append((tier[norm(lbl)][1], tier[norm(lbl)][0]))
            for n, (t, lbl) in tier.items():
                if global_norm.get(n) == kind and not any(h[0] == lbl for h in hits):
                    hits.append((lbl, t))
            # Base documents first: they are what the customer actually receives today.
            hits.sort(key=lambda h: (h[1] != "base", h[0]))
            for lbl, t in hits:
                out.append({"jurisdiction": code, "kind": kind, "label": lbl,
                            "via": "document", "tier": t})
            if not hits:
                # A Gesellschafterliste with no document of its own is still answerable
                # if the registry returns shareholder data fields on the extract.
                if kind == GESELLSCHAFTERLISTE and (j.get("shareholders") or []):
                    out.append({"jurisdiction": code, "kind": kind, "label": None,
                                "via": "data", "tier": "base"})
                else:
                    unresolved[kind].append(code)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    n = len(rows)
    multi = {j["code"]: j["rows"] for j in rows if len(j["rows"]) > 1}
    print(f"Jurisdictions in scope (distinct codes, excl. DE): {n}")
    print(f"  merged multi-registry codes: {multi}")
    print(f"Rows written: {len(out)} -> {os.path.relpath(OUT, ROOT)}\n")
    # STP receives BASE documents only. The 'additional' tier is orderable-on-request and
    # is not delivered today, so base-only is the coverage they actually experience —
    # report it first and keep the fuller number beside it, not instead of it.
    print(f"{'kind':22} {'base only':>10} {'incl. add.':>11}  (of {n} jurisdictions)")
    for kind in KINDS:
        rs = [r for r in out if r["kind"] == kind]
        base_j = {r["jurisdiction"] for r in rs if r["tier"] == "base"}
        all_j = {r["jurisdiction"] for r in rs}
        data_j = {r["jurisdiction"] for r in rs if r["via"] == "data"}
        print(f"{kind:22} {len(base_j):>10} {len(all_j):>11}"
              f"   ({len(data_j)} of the base ones via extract data, not a document)")
    print()
    for kind in KINDS:
        u = sorted(unresolved[kind])
        print(f"{kind:22} unresolved in {len(u):>3}: {u[:14]}{'...' if len(u) > 14 else ''}")
    print("\nUnresolved means nobody has confirmed what the local equivalent is — not "
          "that none exists. Curate from registry knowledge, never from the label text.")


if __name__ == "__main__":
    main()
