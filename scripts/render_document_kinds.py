"""Render curation/document_kinds_evidence.json into a publishable, cited document.

One source of truth, two outputs: this makes the customer-facing markdown; the same JSON
is what an API would serve. Every claim carries its legal basis, a verbatim quote where
we have one, and a URL — so a customer can check us rather than trust us.

Run (no app or network needed):
    python scripts/render_document_kinds.py

Writes docs/DOCUMENT_KINDS_EVIDENCE.md and prints a coverage/quality summary.

The summary is the point of this script as much as the document is: it counts how many
assertions carry a verbatim quote and how many are flagged UNVERIFIED, so the gaps stay
visible instead of being smoothed over by the prose.
"""
import os, json
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "curation", "document_kinds_evidence.json")
OUT = os.path.join(ROOT, "docs", "DOCUMENT_KINDS_EVIDENCE.md")

# Deliberately blunt wording: a customer must never read "not researched" as "does not
# exist", and must never read "provable" as "we already send it to you".
STATUS = {
    "proved_by_base_document": (
        "✅ Provable", "Evidenced by a document you already receive with the case."),
    "proved_by_additional_document": (
        "💶 Provable on request", "Evidenced, but only by a document that must be "
        "ordered separately (additional tier)."),
    "not_provable_from_registry": (
        "❌ Not provable", "The registry does not evidence this fact. No supplier can "
        "change this — it is a matter of local law."),
    "not_researched": (
        "❔ Not yet researched", "We have not established the position. This is NOT a "
        "statement that the document does not exist."),
}
KIND_LABEL = {
    "REGISTERAUSZUG": "Registerauszug",
    "GESELLSCHAFTERLISTE": "Gesellschafterliste",
    "GESELLSCHAFTSVERTRAG": "Gesellschaftsvertrag",
}


def main():
    rows = json.load(open(SRC, encoding="utf-8"))
    by_juris = defaultdict(list)
    for r in rows:
        by_juris[r["jurisdiction"]].append(r)

    L = ["# Document kinds — what each registry actually evidences", "",
         "For every jurisdiction and legal form: which document proves the "
         "Registerauszug, the Gesellschafterliste and the Gesellschaftsvertrag.",
         "",
         "**A document is the proof.** Structured data parsed out of a registry is not a "
         "substitute for the document that evidences it, so this table only credits a "
         "fact as provable when a retrievable document carries it.",
         "",
         "Germany is out of scope: we source German entities directly, not through this "
         "supply chain.",
         "", "## Legend", ""]
    for _k, (label, desc) in STATUS.items():
        L.append("- **%s** — %s" % (label, desc))
    L += ["", "---", ""]

    for code in sorted(by_juris):
        L.append("## %s" % code)
        L.append("")
        for r in sorted(by_juris[code], key=lambda r: (r["kind"], r["legalForm"])):
            label, _ = STATUS[r["status"]]
            L.append("### %s — %s" % (r["legalForm"], KIND_LABEL.get(r["kind"], r["kind"])))
            L.append("")
            L.append("**%s**" % label)
            L.append("")
            L.append(r["summary"])
            L.append("")
            if r.get("documentLocal"):
                doc = "**Document:** %s" % r["documentLocal"]
                if r.get("documentLabel"):
                    doc += " — delivered as `%s`" % r["documentLabel"]
                L += [doc, ""]
            if r.get("bestAvailable"):
                L += ["**Best available alternative:** %s" % r["bestAvailable"], ""]
            for e in r.get("evidence", []):
                L.append("> **%s**" % e["basis"])
                if e.get("quote"):
                    L.append("> ")
                    L.append("> „%s\"" % e["quote"])
                if e.get("note"):
                    L.append("> ")
                    L.append("> %s" % e["note"])
                if e.get("url"):
                    L.append("> ")
                    L.append("> Source: <%s> (retrieved %s)" % (e["url"], e.get("retrieved", "—")))
                L.append("")
            if r.get("caveats"):
                L += ["**Caveats:**", ""]
                L += ["- %s" % c for c in r["caveats"]]
                L.append("")
            L.append("")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write("\n".join(L))

    ev = [e for r in rows for e in r.get("evidence", [])]
    quoted = [e for e in ev if e.get("quote")]
    unver = [c for r in rows for c in r.get("caveats", [])
             if "UNVERIFIED" in c or "INFERENCE" in c or "CONFLICT" in c]
    print("Rows: %d across %d jurisdictions -> %s"
          % (len(rows), len(by_juris), os.path.relpath(OUT, ROOT)))
    print("Evidence items: %d | with a verbatim quote: %d (%.0f%%) | URL-backed: %d"
          % (len(ev), len(quoted), 100.0 * len(quoted) / len(ev),
             len([e for e in ev if e.get("url")])))
    print("Confidence: " + ", ".join(
        "%s=%d" % (c, len([r for r in rows if r.get("confidence") == c]))
        for c in ("high", "medium", "low")))
    print("Flagged UNVERIFIED / INFERENCE / CONFLICT caveats: %d" % len(unver))
    print()
    for s in STATUS:
        n = len([r for r in rows if r["status"] == s])
        if n:
            print("  %-32s %d" % (s, n))
    kinds = {r["kind"] for r in rows}
    missing = set(KIND_LABEL) - kinds
    if missing:
        print("\nNOT YET COVERED FOR ANY JURISDICTION: %s" % ", ".join(sorted(missing)))
        print("  -> these must be researched before the table is customer-ready.")


if __name__ == "__main__":
    main()
