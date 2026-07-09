"""Sweep every AUTOMATED jurisdiction with a free search and record what the
KYC.com search actually returns — so we know the STANDARD fields that come back
and what we can ENRICH per jurisdiction (like India's CIN).

Free (search is not billable). Re-runnable and EXTENSIBLE: results are merged into
docs/search-catalog.json keyed by ISO code, so re-running fills in jurisdictions
that timed out last time without losing the ones already captured.

    python scripts/search_response_sweep.py            # sweep all automated jurisdictions
    python scripts/search_response_sweep.py DE FR IT   # only these

Needs the app running (reads /api/reference and /api/search on localhost:8770).
"""
import os, sys, json, urllib.request, urllib.parse

APP = os.getenv("APP_URL", "http://localhost:8770")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "search-catalog.json")
QUERIES = ["holding", "bank", "invest", "trading", "group"]  # fallbacks until a hit
TIMEOUT = 18


def _get(url):
    return json.load(urllib.request.urlopen(url, timeout=TIMEOUT))


def automated_codes():
    ref = _get(APP + "/api/reference")["jurisdictions"]
    return sorted(j["code"] for j in ref if j.get("auto"))


def granularity(addr, country_name):
    """Rough granularity of the returned address string."""
    if not addr:
        return "none"
    a = addr.strip()
    if "," in a:
        return "city+region"
    if country_name and a.lower() == country_name.lower():
        return "country"
    return "single-token"  # a state OR a city — inspect the sample to tell


def main():
    codes = [c.upper() for c in sys.argv[1:]] or automated_codes()
    catalog = {}
    if os.path.exists(OUT):
        catalog = json.load(open(OUT, encoding="utf-8"))
    names = {j["code"]: j["name"] for j in _get(APP + "/api/reference")["jurisdictions"]}

    for code in codes:
        rec = {"code": code, "name": names.get(code)}
        hit = None
        for q in QUERIES:
            url = "%s/api/search?jurisdiction=%s&query=%s" % (APP, code, urllib.parse.quote(q))
            try:
                r = _get(url)
                rs = r.get("results", [])
                if rs:
                    hit = (q, rs[0], len(rs))
                    break
                rec["note"] = "no results for common queries"
            except Exception as e:
                rec["error"] = str(e)[:60]
                if "timed out" not in str(e):
                    break
        if hit:
            q, first, n = hit
            rec.update(
                observed=True, query=q, resultCount=n,
                externalCode=first.get("externalCode"),
                rawAddress=first.get("rawAddress"),
                addressGranularity=granularity(first.get("rawAddress"), names.get(code)),
                parsedCity=first.get("city"), parsedZip=first.get("zip"),
                dataSource=first.get("dataSource"),
                companyStatus=first.get("companyStatus"),
            )
            rec.pop("error", None)
        else:
            rec.setdefault("observed", False)
        catalog[code] = rec
        print("%-4s %s" % (code, rec.get("externalCode") or rec.get("error") or rec.get("note") or "-"), flush=True)
        json.dump(catalog, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    obs = sum(1 for v in catalog.values() if v.get("observed"))
    print("catalog: %d jurisdictions, %d observed -> %s" % (len(catalog), obs, OUT))


if __name__ == "__main__":
    main()
