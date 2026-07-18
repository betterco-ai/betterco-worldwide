"""Classify a delivered document as one of the three German document kinds.

STP reasons in German cases. This answers, for a foreign company: which delivered
document plays the role of the Registerauszug / Gesellschafterliste /
Gesellschaftsvertrag? The mapping is functional, not textual — GB's "CS01" is the
shareholder list, and in AT/NL that role is filled by data fields on the extract rather
than by any document — so it is read from curation/document_kinds_curation.json, which
is hand-authored. See scripts/curate_document_kinds.py.

    kinds_of("CS01 <14/02/2026>", "GB")   -> ["GESELLSCHAFTERLISTE", "REGISTERAUSZUG"]
    coverage("AT")["GESELLSCHAFTERLISTE"] -> {"via": "data", "tier": "base", ...}

One document can serve SEVERAL roles — GB's CS01 restates the registered particulars
AND lists the shareholders — so this returns a list, never a single kind. Most delivered
documents serve none of the three and return [].

`tier` separates what the customer gets from what exists: 'base' documents come with the
case, 'additional' ones are orderable on request and billed extra. Today STP receives
base only, so an 'additional' mapping describes what COULD be delivered, not what will.

Germany is out of scope by construction (we serve DE ourselves, not via KYC.com).

The jurisdiction must be supplied by the caller: the case endpoints do not return it —
GET /cases/{id} yields only {caseCommonId, caseReadyDatetime, complete, ready,
statusName}. Until the gateway carries a jurisdiction, this cannot be driven off a case
id alone.
"""
import os, json, re

_CURATION = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "curation", "document_kinds_curation.json")

# The live API returns the label with the date inlined — 'CS01 <14/02/2026>',
# 'New Incorporation <05/02/2007>'. The matrix holds the bare label.
_DATE_SUFFIX = re.compile(r"\s*<\d{2}/\d{2}/\d{4}>\s*$")

_table = None


def _norm(s):
    """Match the matrix's spelling to the API's: they differ in case, &/and and stray
    punctuation (API 'Registration certificate' vs matrix 'Registration Certificate';
    the matrix holds '- Incorporation' with a leading dash)."""
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower().replace("&", "and")).strip()


def strip_date(label):
    """'CS01 <14/02/2026>' -> 'CS01'. Also drops the '.pdf' that `name` carries."""
    label = re.sub(r"\.pdf$", "", (label or "").strip(), flags=re.I)
    return _DATE_SUFFIX.sub("", label).strip()


def _load():
    global _table
    if _table is None:
        rows = json.load(open(_CURATION, encoding="utf-8"))
        _table = {"by_label": {}, "by_juris": {}}
        for r in rows:
            j = r["jurisdiction"]
            _table["by_juris"].setdefault(j, {}).setdefault(r["kind"], []).append(r)
            if r.get("label"):
                _table["by_label"].setdefault((j, _norm(r["label"])), []).append(r)
    return _table


def _rows_for(label, jurisdiction):
    if not label or not jurisdiction:
        return []
    return _load()["by_label"].get((jurisdiction.upper(), _norm(strip_date(label))), [])


def kinds_of(label, jurisdiction):
    """Every German kind this delivered document serves, sorted. [] if it serves none —
    which is also what an uncurated jurisdiction returns. Use coverage() to tell those
    two apart; they are NOT the same and must not be shown to a customer as if they were."""
    return sorted({r["kind"] for r in _rows_for(label, jurisdiction)})


def tier_of(label, jurisdiction):
    """'base' | 'additional' | None. 'base' wins if the document is base for any kind."""
    tiers = {r["tier"] for r in _rows_for(label, jurisdiction)}
    return "base" if "base" in tiers else ("additional" if tiers else None)


def coverage(jurisdiction):
    """{kind: {"via": "document"|"data", "labels": [...], "tier": "base"|"additional"}}
    for the kinds this jurisdiction can serve. A kind ABSENT from the result is
    UNRESOLVED — nobody has confirmed the local equivalent. That is NOT the same as
    "does not exist"; never present it to a customer as such."""
    out = {}
    for kind, rs in _load()["by_juris"].get((jurisdiction or "").upper(), {}).items():
        out[kind] = {
            "via": "data" if all(r["via"] == "data" for r in rs) else "document",
            "labels": [r["label"] for r in rs if r.get("label")],
            "tier": "base" if any(r["tier"] == "base" for r in rs) else "additional",
        }
    return out


def annotate(documents, jurisdiction):
    """Add `kinds` (list) and `tier` to each document dict from case_documents_flat().
    Non-destructive: returns new dicts."""
    out = []
    for d in (documents or []):
        label = d.get("category") or d.get("name")
        out.append(dict(d, kinds=kinds_of(label, jurisdiction),
                        tier=tier_of(label, jurisdiction)))
    return out
