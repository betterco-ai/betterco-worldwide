"""Round D helper: export medium/low target rows per batch, apply verified updates in place.

Usage:
  python round_d_tools.py export <BATCH_NAME> <JURIS,JURIS,...>   -> writes targets_<BATCH_NAME>.json here
  python round_d_tools.py apply <updates_file.json>               -> merges into evidence JSON in place
  python round_d_tools.py stats                                   -> confidence counts

Guardrails enforced on apply:
  - match by (jurisdiction, legalForm, kind); unmatched updates are REJECTED loudly
  - status/kind/documentLabel/summary/legalForm fields are NEVER touched
  - only evidence / caveats / confidence are replaced
  - confidence may only be 'high' or 'medium' (never invent other values)
  - every evidence entry must have basis+url; quote may be absent (then note required)
"""
import json, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO = r"C:\Users\unzer\Dropbox\02_4Ventures\04_4V_Projects\2104_Founders1\07_Projects\2601_Claude\betterco-worldwide\betterco-worldwide"
EVID = os.path.join(REPO, "curation", "document_kinds_evidence.json")
HERE = os.environ.get("ROUND_D_WORKDIR", os.path.dirname(os.path.abspath(__file__)))

def load():
    with open(EVID, encoding="utf-8") as f:
        return json.load(f)

def key(r):
    return (r["jurisdiction"], r["legalForm"], r["kind"])

def export(batch, juris_list):
    rows = load()
    targets = [r for r in rows if r.get("confidence") in ("medium", "low")
               and r["jurisdiction"] in juris_list]
    out = os.path.join(HERE, f"targets_{batch}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(targets, f, ensure_ascii=False, indent=1)
    print(f"exported {len(targets)} rows -> {out}")
    for r in targets:
        print(" ", r["jurisdiction"], "|", r["legalForm"], "|", r["kind"], "|", r["status"])

def apply(updates_file):
    rows = load()
    index = {key(r): r for r in rows}
    with open(updates_file, encoding="utf-8") as f:
        updates = json.load(f)
    applied, rejected = 0, []
    for u in updates:
        k = (u["jurisdiction"], u["legalForm"], u["kind"])
        r = index.get(k)
        if r is None:
            rejected.append((k, "no matching row"))
            continue
        if u.get("confidence") not in ("high", "medium"):
            rejected.append((k, f"bad confidence {u.get('confidence')!r}"))
            continue
        ev = u.get("evidence")
        if not isinstance(ev, list) or not ev:
            rejected.append((k, "missing evidence array"))
            continue
        bad = [e for e in ev if not e.get("basis") or not e.get("url")
               or (not e.get("quote") and not e.get("note"))]
        if bad:
            rejected.append((k, f"{len(bad)} evidence entries missing basis/url/quote-or-note"))
            continue
        if u.get("status") and u["status"] != r["status"]:
            rejected.append((k, f"attempted status change {r['status']} -> {u['status']}"))
            continue
        r["evidence"] = ev
        if isinstance(u.get("caveats"), list):
            r["caveats"] = u["caveats"]
        r["confidence"] = u["confidence"]
        applied += 1
    with open(EVID, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"applied {applied} updates, rejected {len(rejected)}")
    for k, why in rejected:
        print("  REJECTED", k, "--", why)
    stats()

def stats():
    rows = load()
    from collections import Counter
    c = Counter(r.get("confidence") for r in rows)
    print("total", len(rows), dict(c))

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "export":
        export(sys.argv[2], sys.argv[3].split(","))
    elif cmd == "apply":
        apply(sys.argv[2])
    else:
        stats()
