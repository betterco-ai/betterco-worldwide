"""Validate and merge staged research rows into curation/document_kinds_evidence.json.

Overnight, one research agent per jurisdiction returns a JSON array of evidence rows.
Each array is saved verbatim to curation/staging/<CODE>.json. This script validates every
row against the schema, REJECTS anything malformed (loudly, never silently), de-duplicates
against what is already merged, and writes the combined set back.

Run:
    python scripts/merge_evidence.py            # validate + merge all staged files
    python scripts/merge_evidence.py --check    # validate only, write nothing

The point is that a bad or hallucinated row is caught here, not discovered in the
customer-facing document. A row missing its source URL, or citing no statute, is not
evidence — it is rejected and named.
"""
import os, sys, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVID = os.path.join(ROOT, "curation", "document_kinds_evidence.json")
STAGE = os.path.join(ROOT, "curation", "staging")

KINDS = {"REGISTERAUSZUG", "GESELLSCHAFTERLISTE", "GESELLSCHAFTSVERTRAG"}
STATUS = {"proved_by_base_document", "proved_by_additional_document",
          "not_provable_from_registry", "not_researched"}
REQUIRED = {"jurisdiction", "legalForm", "kind", "status", "summary", "evidence",
            "caveats", "confidence"}
CONF = {"high", "medium", "low"}


def validate_row(r, where):
    """Return a list of problems; empty means the row is acceptable."""
    errs = []
    if not isinstance(r, dict):
        return ["%s: not an object" % where]
    missing = REQUIRED - set(r)
    if missing:
        errs.append("%s: missing keys %s" % (where, sorted(missing)))
    if r.get("kind") not in KINDS:
        errs.append("%s: bad kind %r" % (where, r.get("kind")))
    if r.get("status") not in STATUS:
        errs.append("%s: bad status %r" % (where, r.get("status")))
    if r.get("confidence") not in CONF:
        errs.append("%s: bad confidence %r" % (where, r.get("confidence")))
    if not isinstance(r.get("jurisdiction"), str) or len(r.get("jurisdiction", "")) != 2:
        errs.append("%s: jurisdiction should be a 2-letter code, got %r"
                    % (where, r.get("jurisdiction")))
    ev = r.get("evidence")
    # A provable claim MUST carry at least one sourced evidence item. A
    # "not_provable_from_registry" may cite the absence, but still needs a basis+url.
    if not isinstance(ev, list) or not ev:
        errs.append("%s: no evidence items" % where)
    else:
        for i, e in enumerate(ev):
            if not isinstance(e, dict):
                errs.append("%s evidence[%d]: not an object" % (where, i)); continue
            if not e.get("basis"):
                errs.append("%s evidence[%d]: no 'basis' (statute/source)" % (where, i))
            if not e.get("url"):
                errs.append("%s evidence[%d]: no 'url'" % (where, i))
    if r.get("status", "").startswith("proved") and not r.get("documentLocal") \
            and not r.get("documentLabel"):
        errs.append("%s: status is 'proved_*' but names no document" % where)
    return errs


def sanitize(r):
    """Clean up two things agents sometimes emit: a literal 'omit' where the quote
    should be absent, and empty-string quotes. Both become no-quote (a valid state —
    quote is optional; basis+url carry the citation)."""
    if not isinstance(r, dict):
        return
    for e in r.get("evidence", []) or []:
        if isinstance(e, dict):
            q = e.get("quote")
            if q is not None and (not str(q).strip() or str(q).strip().lower() == "omit"):
                e.pop("quote", None)


def key(r):
    return (r.get("jurisdiction"), r.get("legalForm"), r.get("kind"))


def main():
    check_only = "--check" in sys.argv
    existing = json.load(open(EVID, encoding="utf-8")) if os.path.exists(EVID) else []
    seen = {key(r) for r in existing}

    staged_files = sorted(glob.glob(os.path.join(STAGE, "*.json")))
    accepted, rejected, dup = [], [], 0
    for f in staged_files:
        name = os.path.basename(f)
        try:
            rows = json.load(open(f, encoding="utf-8"))
        except Exception as e:
            rejected.append("%s: not valid JSON — %s" % (name, e)); continue
        if not isinstance(rows, list):
            rejected.append("%s: top level is not an array" % name); continue
        for i, r in enumerate(rows):
            sanitize(r)
            errs = validate_row(r, "%s[%d]" % (name, i))
            if errs:
                rejected.extend(errs); continue
            if key(r) in seen:
                dup += 1; continue
            seen.add(key(r)); accepted.append(r)

    print("Staged files: %d" % len(staged_files))
    print("Rows accepted (new): %d | duplicates skipped: %d | problems: %d"
          % (len(accepted), dup, len(rejected)))
    for p in rejected:
        print("  REJECT %s" % p)

    if check_only:
        print("\n--check: nothing written.")
        return
    if not accepted:
        print("\nNothing new to merge.")
        return
    merged = existing + accepted
    merged.sort(key=lambda r: (r["jurisdiction"], r["kind"], r["legalForm"]))
    json.dump(merged, open(EVID, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    juris = sorted({r["jurisdiction"] for r in merged})
    print("\nMerged -> %s" % os.path.relpath(EVID, ROOT))
    print("Total rows: %d across %d jurisdictions: %s"
          % (len(merged), len(juris), ", ".join(juris)))


if __name__ == "__main__":
    main()
