"""Validate + merge staged registry-intelligence rows, and derive a build-vs-buy verdict.

Staged per-batch files in curation/staging_registry/*.json are validated, deduped by
jurisdiction, and merged into curation/registry_intelligence.json. Each row also gets a
computed `goDirect` verdict from the three decision drivers (open API? documents via API?
cost?), so the internal reader gets a ranked build-vs-buy scorecard, not just prose.

Run:
    python scripts/merge_registry.py            # merge + score
    python scripts/merge_registry.py --check    # validate only
"""
import os, sys, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "curation", "registry_intelligence.json")
STAGE = os.path.join(ROOT, "curation", "staging_registry")

REQUIRED = {"jurisdiction", "registryName", "openApi", "apiDelivers", "documentsViaApi",
            "cost", "notes", "confidence", "sources"}
OPENAPI = {"yes", "partial", "no"}


def validate(r, where):
    errs = []
    if not isinstance(r, dict):
        return [where + ": not an object"]
    for k in REQUIRED - set(r):
        errs.append("%s: missing %s" % (where, k))
    if r.get("openApi") not in OPENAPI:
        errs.append("%s: bad openApi %r" % (where, r.get("openApi")))
    if not isinstance(r.get("cost"), dict) or not r["cost"].get("model"):
        errs.append("%s: cost.model missing" % where)
    if not r.get("sources"):
        errs.append("%s: no sources" % where)
    return errs


def go_direct(r):
    """Verdict for build-vs-buy. The prize is a registry we can hit directly AND that
    serves the documents (not just data), cheaply. Data-only or no-API => keep the vendor
    for documents."""
    api, docs = r.get("openApi"), r.get("documentsViaApi")
    model = (r.get("cost") or {}).get("model")
    free = model == "free"
    if api == "no":
        return {"verdict": "vendor_only", "reason": "no registry API — portal/per-document only"}
    if not docs:
        return {"verdict": "direct_data_only",
                "reason": "API delivers data but NOT documents — vendor still needed for filings"}
    # documents ARE available via a usable API:
    if api == "yes" and free:
        return {"verdict": "direct_strong", "reason": "open API delivers documents, free/low cost"}
    if api == "yes":
        return {"verdict": "direct_good",
                "reason": "open API delivers documents; per-document/subscription cost"}
    return {"verdict": "direct_contract",
            "reason": "documents via API but access is contract/gated (negotiation needed)"}


def main():
    check = "--check" in sys.argv
    existing = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else []
    seen = {r["jurisdiction"] for r in existing}
    accepted, rejected = [], []
    for f in sorted(glob.glob(os.path.join(STAGE, "*.json"))):
        name = os.path.basename(f)
        try:
            rows = json.load(open(f, encoding="utf-8"))
        except Exception as e:
            rejected.append("%s: bad JSON — %s" % (name, e)); continue
        for i, r in enumerate(rows):
            errs = validate(r, "%s[%d]" % (name, i))
            if errs:
                rejected.extend(errs); continue
            if r["jurisdiction"] in seen:
                continue
            seen.add(r["jurisdiction"])
            r["goDirect"] = go_direct(r)
            accepted.append(r)

    print("Accepted: %d | problems: %d" % (len(accepted), len(rejected)))
    for p in rejected:
        print("  REJECT", p)
    if check:
        print("--check: nothing written."); return
    merged = sorted(existing + accepted, key=lambda r: r["jurisdiction"])
    json.dump(merged, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Merged -> %s (%d jurisdictions)" % (os.path.relpath(OUT, ROOT), len(merged)))

    from collections import Counter
    print("\nBuild-vs-buy scorecard:")
    order = ["direct_strong", "direct_good", "direct_contract", "direct_data_only", "vendor_only"]
    by = {}
    for r in merged:
        by.setdefault(r["goDirect"]["verdict"], []).append(r["jurisdiction"])
    for v in order:
        if by.get(v):
            print("  %-16s %s" % (v, ", ".join(sorted(by[v]))))


if __name__ == "__main__":
    main()
