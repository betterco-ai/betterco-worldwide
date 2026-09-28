# -*- coding: utf-8 -*-
"""Checklist for the match score (PR #2343) against a deployed environment.

    python scripts/match_checklist.py <workspace .env> [--unsearchable CODE]

The .env needs BETTERCO_BASE_URL, BETTERCO_WORKSPACE_ID, BETTERCO_API_KEY, BETTERCO_API_SECRET
(the workspaces/*.env format of betterco_claude_api). Credentials never enter this repo.

Reads only. The one create is confirm:false - a free dry run that must answer 428.
Row 9 needs a jurisdiction that environment cannot search: dev's test system and prod differ
(Spain is searchable on dev, not on prod), so it is picked from the environment's own
/jurisdictions unless --unsearchable is given. Row 5-7 use a GB example company that exists
on dev's test system; on prod pass a real GB company via --gb-name/--gb-number.
"""
import argparse, json, sys, requests
from dotenv import dotenv_values

ap = argparse.ArgumentParser()
ap.add_argument("env_file")
ap.add_argument("--unsearchable")
ap.add_argument("--gb-name", default="CROPWELL BISHOP CREAMERY LIMITED")
ap.add_argument("--gb-number", default="00364890")
args = ap.parse_args()

v = dotenv_values(args.env_file)
BASE = v["BETTERCO_BASE_URL"].rstrip("/")
WS = v["BETTERCO_WORKSPACE_ID"]
tok = requests.post(f"{BASE}/restapi/v1/auth/login", timeout=60,
                    json={"key": v["BETTERCO_API_KEY"], "secret": v["BETTERCO_API_SECRET"]}).json()["token"]
H = {"Authorization": f"Bearer {tok}"}
DS = f"{BASE}/restapi/v1/workspaces/{WS}/document-search"
print("environment:", BASE)
results = []

def check(name, ok, detail=""):
    results.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name + ("  | " + detail if detail else ""))

def get(path, **params):
    return requests.get(DS + path, headers=H, params=params, timeout=180)

def post(path, body):
    return requests.post(DS + path, headers=H, json=body, timeout=180)

# --- existing calls, unchanged -------------------------------------------------
r = get("/jurisdictions")
check("1 GET jurisdictions -> 200", r.status_code == 200, f"{r.status_code}, {len(r.json()) if r.ok else r.text[:120]} rows")
r = get("/cases", scope="workspace")
check("2 GET cases?scope=workspace -> 200", r.status_code == 200, f"{r.status_code}")
r = get("/cases/search", jurisdiction="GB", query=args.gb_name)
hits = r.json() if r.ok else []
if isinstance(hits, dict):
    hits = hits.get("results") or hits.get("items") or hits.get("companies") or []
print("   search GB:", len(hits), "hits")
check("2b GET cases/search GB -> 200", r.status_code == 200, f"{r.status_code}")
r = post("/cases", {"jurisdiction": "GB", "name": args.gb_name,
                    "externalCode": args.gb_number, "confirm": False})
check("3 POST cases confirm:false (dry run, no match called) -> 428 not_confirmed",
      r.status_code == 428, f"{r.status_code} {r.text[:160]}")

# --- new calls -----------------------------------------------------------------
r = get("/match/rules")
rules = r.json() if r.ok else {}
check("4 GET match/rules -> 200 with rulesVersion", r.status_code == 200 and bool(rules.get("rulesVersion")),
      f"{r.status_code} rulesVersion={rules.get('rulesVersion')} comparable={rules.get('numberComparableJurisdictions')}")

def match(body):
    r = post("/match", body)
    try:
        j = r.json()
    except Exception:
        j = {}
    return r.status_code, j

s, j = match({"jurisdiction": "GB", "name": args.gb_name, "registerNumber": args.gb_number})
top = (j.get("candidates") or [{}])[0]
check("5 match GB name+number -> 200, NUMBER lookup ran", s == 200 and "NUMBER" in (j.get("signals") or {}).get("lookups", []),
      f"{s} score={j.get('score')} band={j.get('bandId')} top={top.get('rawname')}/{top.get('foundBy')} signals={j.get('signals')}")
s, j = match({"jurisdiction": "GB", "name": args.gb_name})
sig = j.get("signals") or {}
check("6 match GB name only -> numberSupplied false, lookups [NAME]",
      s == 200 and sig.get("numberSupplied") is False and sig.get("lookups") == ["NAME"],
      f"{s} score={j.get('score')} band={j.get('bandId')} signals={sig}")
s, j = match({"jurisdiction": "GB", "name": args.gb_name, "registerNumber": "99999999"})
check("7 match GB right name, wrong number -> not 100", s == 200 and j.get("score") != 100,
      f"{s} score={j.get('score')} band={j.get('bandId')} candidates={len(j.get('candidates') or [])}")
s, j = match({"jurisdiction": "DE", "name": "Beispiel GmbH"})
check("8 match DE -> 200, orderable false, JURISDICTION_NOT_AVAILABLE",
      s == 200 and j.get("orderable") is False and j.get("reason") == "JURISDICTION_NOT_AVAILABLE", f"{s} {json.dumps(j)[:160]}")
unsearchable = args.unsearchable or next(
    (x["code"] for x in get("/jurisdictions").json() if x.get("automated") is False and x["code"] != "DE"), None)
s, j = match({"jurisdiction": unsearchable, "name": "Test Company"})
check(f"9 match {unsearchable} (not searchable here) -> 200, checkable false, NO_SEARCHABLE_REGISTRY",
      s == 200 and j.get("checkable") is False and j.get("reason") == "NO_SEARCHABLE_REGISTRY", f"{s} {json.dumps(j)[:160]}")
s, j = match({"name": "x"})
check("10 match without jurisdiction -> 400", s == 400, f"{s}")
s, j = match({"jurisdiction": "AT", "name": "Modern Hero Academy", "registerNumber": "1545796600"})
check("11 match AT association number (row 16, today's fix) -> 0 NO_COMPANY_REGISTER",
      s == 200 and j.get("score") == 0 and j.get("bandId") == "NO_COMPANY_REGISTER", f"{s} score={j.get('score')} band={j.get('bandId')}")

print()
print(f"{sum(ok for _, ok in results)}/{len(results)} passed")
sys.exit(0 if all(ok for _, ok in results) else 1)
