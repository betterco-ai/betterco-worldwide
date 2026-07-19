"""Build the vendor-neutral routing table from the registry-truth evidence file.

Two layers, deliberately separate (see the aggregator-architecture memo):
  LAYER 1  curation/document_kinds_evidence.json — what the REGISTRY evidences, per
           (jurisdiction x legalForm x kind), with citations. Vendor-independent.
  LAYER 2  this script — turns each row into an ACTIONABLE decision and resolves which
           VENDOR serves that jurisdiction, and HOW that vendor is ordered from.

Output: curation/document_kinds_routing.json — the API's backing data.

Vendor ordering granularity differs, and that is the point:
  - KYC.com is CASE-LEVEL. You order a case for a company; base documents come with it,
    "additional" documents are requestable within the case (extra charge). There is NO
    per-document SKU — the jurisdiction_matrix.json base/additional lists ARE the catalog.
  - handelsregister.de is DOCUMENT-LEVEL — you order a specific German document.
  Our aggregation layer presents a uniform document-level request and maps down to whatever
  the vendor supports (a case order for KYC.com, a document order for handelsregister.de).

Run:
    python scripts/build_routing.py
"""
import os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "curation", "document_kinds_evidence.json")
OUT = os.path.join(ROOT, "curation", "document_kinds_routing.json")
MATRIX = os.path.join(ROOT, "jurisdiction_matrix.json")


def shareholder_data_by_code():
    """Per jurisdiction, the shareholder DATA fields KYC.com parses (from the coverage
    matrix). This is DATA, not a proof document — but where the proof document cannot be
    sourced, delivering this data (as a data sheet / generated document) is a real backup.
    Merged across a jurisdiction's registry rows (HK CR/IRD etc.)."""
    out = {}
    if not os.path.exists(MATRIX):
        return out
    for j in json.load(open(MATRIX, encoding="utf-8")).get("jurisdictions", []):
        c = j.get("code")
        if not c:
            continue
        out.setdefault(c, [])
        for s in (j.get("shareholders") or []):
            if s not in out[c]:
                out[c].append(s)
    return out


_SHDATA = shareholder_data_by_code()

# ---- LAYER 2a: vendor routing + ordering model (per vendor) ---------------------------
VENDOR_BY_JURISDICTION = {
    "DE": "handelsregister.de",   # served directly (free), NOT via KYC.com
    "FR": "inpi.rne",             # free direct REST API for statuts/actes/comptes
    "*": "kyc.com",
}
# Per-(jurisdiction, kind) vendor override — takes precedence over the jurisdiction default.
# This is where SPLIT-vendor jurisdictions live: FR serves statuts free via INPI, but the Kbis
# register extract only via paid Infogreffe. First real per-document vendor split.
VENDOR_BY_JURISDICTION_KIND = {
    ("FR", "REGISTERAUSZUG"): "infogreffe",       # Kbis — paid, ~3.06 EUR (INPI does not issue it)
    ("FR", "GESELLSCHAFTSVERTRAG"): "inpi.rne",   # statuts — free
    # FR GESELLSCHAFTERLISTE is not_provable (SAS/SA private) — vendor is informational only.
    ("GB", "GESELLSCHAFTSVERTRAG"): "companies-house.uk",  # Articles — free via Companies House API
    # GB REGISTERAUSZUG + GESELLSCHAFTERLISTE are not_provable — vendor informational only.
}
# How each vendor is ordered from. case_level => document identified WITHIN a case, no SKU.
VENDOR_ORDER_MODEL = {
    "kyc.com": {"model": "case_level", "catalog": "jurisdiction_matrix.json",
                "note": "Order the case; base docs included, additional docs requestable "
                        "within the case. No per-document SKU."},
    "handelsregister.de": {"model": "document_level", "catalog": "handelsregister.de (scraper)",
                           "note": "Free. Browser-scraper provider client; order the document directly."},
    "inpi.rne": {"model": "document_level", "catalog": "INPI RNE API",
                 "note": "Free REST API (JWT): login -> /companies/{siren}/attachments -> "
                         "/{actes,bilans}/{id}/download. See inpi_client.py."},
    "infogreffe": {"model": "document_level", "catalog": "Infogreffe",
                   "note": "Paid ~3.06 EUR/electronic doc (professional account). Certified Kbis."},
    "companies-house.uk": {"model": "document_level", "catalog": "Companies House API",
                           "note": "Free REST API (Public Data + Document API), free API key. "
                                   "Serves filed document images incl. articles."},
}


def vendor_for(j, kind=None):
    if kind is not None and (j, kind) in VENDOR_BY_JURISDICTION_KIND:
        return VENDOR_BY_JURISDICTION_KIND[(j, kind)]
    return VENDOR_BY_JURISDICTION.get(j, VENDOR_BY_JURISDICTION["*"])


# ---- LAYER 2b: completeness / fallback (registry-truth consequences, vendor-neutral) --
# completeness: full | delta | threshold | snapshot | sole_only | founders_only | conditional
# fallback:     company_register | ubo_register | none
# Keyed (jurisdiction, kind); an optional middle element pins a specific legalForm.
OVERRIDES = {
    ("GB", "GESELLSCHAFTERLISTE"): {"completeness": "delta", "fallback": "company_register"},
    ("DK", "GESELLSCHAFTERLISTE"): {"completeness": "threshold", "fallback": "company_register"},
    ("SE", "GESELLSCHAFTERLISTE"): {"fallback": "company_register"},
    ("FI", "GESELLSCHAFTERLISTE"): {"fallback": "company_register"},
    ("NO", "GESELLSCHAFTERLISTE"): {"fallback": "company_register"},
    ("ES", "GESELLSCHAFTERLISTE"): {"fallback": "company_register"},
    ("NL", "GESELLSCHAFTERLISTE"): {"completeness": "sole_only", "fallback": "company_register"},
    ("BE", "GESELLSCHAFTERLISTE"): {"completeness": "founders_only", "fallback": "company_register"},
    ("GG", "GESELLSCHAFTERLISTE"): {"fallback": "company_register"},
    ("IE", "GESELLSCHAFTERLISTE"): {"completeness": "snapshot"},
    ("MT", "GESELLSCHAFTERLISTE"): {"completeness": "snapshot"},
    ("JE", "GESELLSCHAFTERLISTE"): {"completeness": "threshold"},
    ("IT", "SpA", "GESELLSCHAFTERLISTE"): {"completeness": "snapshot"},
    ("IM", "2006 Act company", "GESELLSCHAFTERLISTE"): {"completeness": "conditional"},
    # --- adjudicated 2026-07-18 (the 9 auto-flagged rows) ---
    ("CY", "GESELLSCHAFTERLISTE"): {"completeness": "snapshot"},   # HE32 annual + nominee flag
    ("CY", "REGISTERAUSZUG"): {"completeness": "full"},            # generic issue-date staleness only
    ("MT", "REGISTERAUSZUG"): {"completeness": "full"},            # free vs certified, content full
    ("FR", "SAS", "GESELLSCHAFTSVERTRAG"): {"completeness": "full"},   # statuts complete (caveat is re shares)
    ("NO", "ANS", "GESELLSCHAFTERLISTE"): {"completeness": "full"},    # all partners named; % in unfiled agmt
    ("PL", "sp. z o.o.", "GESELLSCHAFTERLISTE"): {"completeness": "full"},  # lista wspolnikow is full
    ("PL", "partnerships (sp. j./sp. k./sp. p./S.K.A.)", "GESELLSCHAFTERLISTE"): {"completeness": "full"},
}

# not_provable where nothing public exists at all (no company-register route worth offering).
FALLBACK_NONE = {
    ("PL", "GESELLSCHAFTERLISTE"), ("CZ", "GESELLSCHAFTERLISTE"),
    ("PT", "GESELLSCHAFTERLISTE"), ("FR", "GESELLSCHAFTERLISTE"),
    ("LI", "GESELLSCHAFTERLISTE"), ("AT", "GESELLSCHAFTERLISTE"),
    ("CH", "GESELLSCHAFTERLISTE"), ("LU", "GESELLSCHAFTERLISTE"),
}

# Markers that mean a genuine completeness limit (NOT cross-cutting concerns like nominee
# holdings or the issue-date staleness inherent to every extract).
INCOMPLETE_MARKERS = ("only changes", "delta", ">=5", ">=10", "founders at incorporation",
                      "sole shareholder", "sole-shareholder", "periodic snapshot",
                      "less than one per cent", "500 shares", "conditional exception")


def override(j, form, kind):
    return OVERRIDES.get((j, form, kind)) or OVERRIDES.get((j, kind)) or {}


def decide(r):
    j, form, kind, status = r["jurisdiction"], r["legalForm"], r["kind"], r["status"]
    ov = override(j, form, kind)
    caveat_text = " ".join(r.get("caveats", [])).lower()

    if status == "proved_by_base_document":
        availability = "base"
        completeness = ov.get("completeness", "full")
        fallback = None
    elif status == "proved_by_additional_document":
        availability = "additional"
        completeness = ov.get("completeness", "full")
        fallback = None
    else:
        completeness = None
        # A company-held fallback (register of members) only exists for the SHAREHOLDER LIST.
        # For a register extract or the articles, not_provable means genuinely no route.
        default_fb = "company_register" if kind == "GESELLSCHAFTERLISTE" else "none"
        fb = ov.get("fallback", default_fb)
        if (j, kind) in FALLBACK_NONE:
            fb = "none"
        availability = "none" if fb == "none" else "off_registry"
        fallback = fb

    # Action depends on HOW the resolved vendor is ordered. For a case_level vendor (KYC.com) a
    # base document arrives with the case → "use_delivered"; for a document_level vendor (hr.de,
    # inpi.rne, infogreffe) you always fetch the specific document → "order".
    vendor = vendor_for(j, kind)
    order_model = VENDOR_ORDER_MODEL.get(vendor, {}).get("model")
    warn = "_with_warning" if (completeness and completeness != "full") else ""
    if availability == "off_registry":
        action = "manual"
    elif availability == "none":
        action = "unavailable"
    elif order_model == "case_level" and availability == "base":
        action = "use_delivered" + warn
    else:
        action = "order" + warn

    needs_review = bool(availability in ("base", "additional") and completeness == "full"
                        and any(m in caveat_text for m in INCOMPLETE_MARKERS)
                        and not ov.get("completeness"))

    # Cross-cutting badges surfaced separately from completeness (they don't make the list
    # incomplete, but the operator must see them).
    flags = []
    if "nominee" in caveat_text:
        flags.append("nominee")           # registered holder may be a nominee, not beneficial
    if completeness and completeness != "full":
        flags.append(completeness)

    # Data backup: KYC.com's parsed shareholder data, relevant to the shareholder-list kind.
    # Especially valuable where the proof document is off_registry/none — we can still deliver
    # the data (clearly as data, not proof). Only meaningful for the KYC.com-routed path.
    # KYC.com data backup is a property of KYC.com's coverage (the matrix), independent of which
    # vendor we primarily route to — so it stays available even where we go direct for documents.
    data_backup = None
    if kind == "GESELLSCHAFTERLISTE":
        fields = _SHDATA.get(j, [])
        data_backup = {
            "available": bool(fields),
            "fields": fields,
            "source": "kyc.com structured data (parsed)",
            "isProof": False,
            "note": "Data, not a proof document. Deliverable as a data sheet / generated "
                    "document where the proof document is unavailable.",
        }

    order = None
    if availability in ("base", "additional"):
        model = VENDOR_ORDER_MODEL.get(vendor, {})
        order = {
            "vendor": vendor,
            "model": model.get("model"),
            # For a case-level vendor the document is identified within the case by its
            # registry/matrix name; there is no SKU. For a document-level vendor it maps to
            # that vendor's document type. `registryName` is our normalized handle either way.
            "registryName": r.get("documentLocal") or r.get("documentLabel"),
            "howToObtain": ("included_in_case" if availability == "base"
                            else "additional_within_case") if model.get("model") == "case_level"
                            else "order_document",
            "vendorCatalog": model.get("catalog"),
            "aggregationNote": "Document-level request provided by our aggregation layer; "
                               "for a case-level vendor no per-document SKU exists.",
        }
    return {
        "jurisdiction": j, "legalForm": form, "kind": kind,
        "availability": availability, "action": action,
        "orderable": availability in ("base", "additional"),
        "completeness": completeness, "flags": flags,
        "order": order, "vendor": vendor, "fallback": fallback,
        "dataBackup": data_backup,
        "confidence": r.get("confidence"), "needsReview": needs_review,
        "sources": [{"basis": e.get("basis"), "url": e.get("url")}
                    for e in r.get("evidence", []) if e.get("url")],
    }


def main():
    rows = json.load(open(SRC, encoding="utf-8"))
    routes = [decide(r) for r in rows]
    out = {
        "generatedFrom": "curation/document_kinds_evidence.json",
        "note": "Vendor-neutral routing. Consumer asks (jurisdiction, kind, legalForm) and "
                "gets an actionable decision; it never names a vendor. Registry truth lives "
                "in the evidence file; vendor selection and ordering model live here.",
        "vendorRouting": VENDOR_BY_JURISDICTION,
        "vendorRoutingByKind": {"%s/%s" % k: v for k, v in VENDOR_BY_JURISDICTION_KIND.items()},
        "vendorOrderModel": VENDOR_ORDER_MODEL,
        "actionVocabulary": {
            "use_delivered": "Document arrives with the case bundle; classify the delivered file.",
            "use_delivered_with_warning": "As above, but flag the completeness limitation.",
            "order": "Place an additional request via the resolved vendor.",
            "order_with_warning": "As above, but surface the completeness badge.",
            "manual": "No registry document; use the fallback (e.g. company's own register).",
            "unavailable": "No route to this document in this jurisdiction.",
        },
        "routes": routes,
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    from collections import Counter
    print("Routes: %d -> %s" % (len(routes), os.path.relpath(OUT, ROOT)))
    print("By action:", dict(Counter(r["action"] for r in routes)))
    print("By availability:", dict(Counter(r["availability"] for r in routes)))
    print("Completeness (orderable):", dict(Counter(r["completeness"] for r in routes if r["orderable"])))
    print("Flagged 'nominee':", len([r for r in routes if "nominee" in r["flags"]]))
    gl = [r for r in routes if r["kind"] == "GESELLSCHAFTERLISTE" and r.get("dataBackup")]
    db = [r for r in gl if r["dataBackup"]["available"]]
    rescue = [r for r in db if not r["orderable"]]
    print("Gesellschafterliste rows with KYC.com data backup: %d/%d (of which %d have NO "
          "proof document — data is the only route)" % (len(db), len(gl), len(rescue)))
    nr = [r for r in routes if r["needsReview"]]
    print("needsReview after adjudication: %d%s" % (len(nr), (" -> " + ", ".join(
        "%s/%s/%s" % (r["jurisdiction"], r["legalForm"], r["kind"]) for r in nr)) if nr else ""))


if __name__ == "__main__":
    main()
