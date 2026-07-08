"""Add ISO 3166-1 `code` to each 'Live jurisdictions' row of jurisdiction_matrix.json.

The KYC.com coverage matrix uses its own jurisdiction names (e.g. "UK", "South Korea",
"UAE", "HK CR", "Viet Nam - NBR") which differ from the app's reference jurisdiction
names. This resolves each matrix row to the app's ISO code so /api/jurisdiction?code=XX
works. US states / Canadian provinces are sub-national -> code = null (name lookup only).

Run AFTER build_jurisdiction_matrix.py, with the app running (reads /api/reference):
    python build_jurisdiction_matrix.py
    python enrich_matrix_codes.py

Matching is EXACT normalized-name + a curated ALIAS table only (no substring matching —
that produced false hits, e.g. mis-assigning Afghanistan). AF/BD/GH have no matrix row:
KYC.com's matrix genuinely omits them (verified) -> they stay code-less.
"""
import os, json, urllib.request

MATRIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jurisdiction_matrix.json")
REFERENCE_URL = os.getenv("APP_URL", "http://localhost:8770") + "/api/reference"

# normalized matrix-name -> ISO code, for names that differ from the reference
ALIAS = {
    "uk": "GB", "southkorea": "KR", "russia": "RU", "vietnamnbr": "VN", "vietnamgdt": "VN",
    "uae": "AE", "bosniaherzegovina": "BA", "britishvirginislandbvi": "VG",
    "usvirginislands": "VI", "hkcr": "HK", "hkird": "HK", "usa": "US", "unitedstates": "US",
    "brunei": "BN", "iran": "IR", "laos": "LA", "macedonia": "MK", "moldova": "MD",
    "palestine": "PS", "taiwan": "TW", "philippinessec": "PH", "philippinesdti": "PH",
    "seychellesbusinessregister": "SC", "seychellesfsa": "SC",
}


def norm(s):
    return "".join(c for c in (s or "").lower() if c.isalnum())


def main():
    m = json.load(open(MATRIX, encoding="utf-8"))
    ref = json.load(urllib.request.urlopen(REFERENCE_URL))["jurisdictions"]
    refmap = {norm(r["name"]): r["code"] for r in ref}

    matched = unmatched = 0
    for j in m["jurisdictions"]:
        if j.get("group") == "Live jurisdictions":
            j["code"] = refmap.get(norm(j["name"])) or ALIAS.get(norm(j["name"]))
            matched += 1 if j["code"] else 0
            unmatched += 0 if j["code"] else 1
        else:
            j["code"] = None
    json.dump(m, open(MATRIX, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    covered = {j["code"] for j in m["jurisdictions"] if j.get("code")}
    missing = [(r["code"], r["name"]) for r in ref if r["code"] not in covered]
    print(f"Live rows coded: {matched} | uncoded: {unmatched}")
    print(f"App jurisdictions with no matrix row (expected AF/BD/GH — not in KYC.com matrix): {missing}")


if __name__ == "__main__":
    main()
