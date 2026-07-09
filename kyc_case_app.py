
"""Local document-search app: search a company, resolve its legal form,
create a case, and retrieve documents from a browser UI.

This app makes no direct calls to KnowYourCustomer.com. Every operation goes
through the BetterCo backend document-search API, which owns the upstream OAuth,
free reads, and billable create server-side. The app never sees upstream
credentials or endpoints.

Cost model is enforced by the gateway: reads are free; create is BILLABLE and gated
by the backend flag `kyc-com.create-enabled` (dry-run by default → returns the exact
payload that WOULD be posted, never calls the billable endpoint).

Config: see kyc_gateway_client.py (DOCUMENT_SEARCH_BASE_URL + BetterCo REST
key/secret + workspace). The backend must be running and reachable.

Usage:
    python3 kyc_case_app.py                 # → http://localhost:8770
    python3 kyc_case_app.py --enable-create # UI hint only; the real gate is backend-side
    python3 kyc_case_app.py --port 8770

Zero extra deps — built on http.server + kyc_gateway_client.
"""
import os, sys, re, json, argparse, threading, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

ap = argparse.ArgumentParser()
ap.add_argument("--port", type=int, default=8770)
ap.add_argument("--enable-create", action="store_true",
                help="UI hint only: shows the 'live create' label. The real billable "
                     "gate lives in the backend.")
ap.add_argument("--no-browser", action="store_true")
args = ap.parse_args()

from kyc_gateway_client import KycGatewayClient
gw = KycGatewayClient()

INDEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kyc_case.html")
TOKENS_CSS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "betterco-tokens.css")
ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
MATRIX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jurisdiction_matrix.json")

_matrix = {}
def jurisdiction_matrix():
    """Static KYC.com jurisdiction coverage (data fields + documents + SLA per
    jurisdiction), pre-parsed from the Excel workbook by build_jurisdiction_matrix.py.
    Info-only, no backend call — cached after first read."""
    if not _matrix:
        with open(MATRIX_PATH, encoding="utf-8") as f:
            _matrix.update(json.load(f))
    return _matrix


# ── India CIN decoder ────────────────────────────────────────────────────────
# CIN = [L|U][5-digit industry][2-letter STATE][4-digit year][3-letter class][6-digit reg#].
# The STATE segment is the Registrar-of-Companies jurisdiction = the registering city.
# This lets us reconstruct the CITY from a search hit whose address is truncated to the
# state — a FREE pre-purchase check (customer gives name+city → confirm before billing).
_CIN_STATE = {
    "TG": ("Telangana", "Hyderabad"), "AP": ("Andhra Pradesh", "Vijayawada"),
    "MH": ("Maharashtra", "Mumbai / Pune"), "DL": ("Delhi", "Delhi"), "HR": ("Haryana", "Delhi"),
    "KA": ("Karnataka", "Bengaluru"), "TN": ("Tamil Nadu", "Chennai"), "GJ": ("Gujarat", "Ahmedabad"),
    "WB": ("West Bengal", "Kolkata"), "UP": ("Uttar Pradesh", "Kanpur"), "RJ": ("Rajasthan", "Jaipur"),
    "KL": ("Kerala", "Ernakulam (Kochi)"), "MP": ("Madhya Pradesh", "Gwalior"), "PB": ("Punjab", "Chandigarh"),
    "CH": ("Chandigarh", "Chandigarh"), "BR": ("Bihar", "Patna"), "OR": ("Odisha", "Cuttack"),
    "GA": ("Goa", "Goa"), "AS": ("Assam", "Guwahati/Shillong"), "JH": ("Jharkhand", "Ranchi"),
    "CT": ("Chhattisgarh", "Bilaspur"), "UT": ("Uttarakhand", "Dehradun"), "UK": ("Uttarakhand", "Dehradun"),
    "HP": ("Himachal Pradesh", "Shimla"), "JK": ("Jammu & Kashmir", "Jammu"), "PY": ("Puducherry", "Puducherry"),
}
_CIN_CLASS = {"PLC": "Public Limited Company", "PTC": "Private Limited Company", "OPC": "One Person Company",
              "NPL": "Not-for-Profit (Sec 8)", "GOI": "Government of India company", "SGC": "State Government company",
              "ULL": "Unlimited (public)", "ULT": "Unlimited (private)", "FLC": "Foreign public", "FTC": "Foreign private"}


def decode_cin(cin):
    """Decode an Indian CIN → {listed, state, rocCity, class, year, regNo, label}.
    Returns None if the string is not a valid CIN."""
    m = re.match(r"^([LU])(\d{5})([A-Z]{2})(\d{4})([A-Z]{3})(\d{6})$", (cin or "").strip().upper())
    if not m:
        return None
    listed, _ind, st, year, cls, reg = m.groups()
    state, roc = _CIN_STATE.get(st, (None, None))
    return {
        "cin": m.group(0), "listed": listed == "L",
        "stateCode": st, "state": state, "rocCity": roc,
        "classCode": cls, "class": _CIN_CLASS.get(cls, cls),
        "year": int(year), "regNo": reg,
        "label": "%s %s · RoC %s%s · est. %d" % (
            "Listed" if listed == "L" else "Unlisted",
            _CIN_CLASS.get(cls, cls), roc or "?",
            (" (%s)" % state) if state else "", int(year)),
    }


def enrich_search_result(jur, r):
    """ONE generic enrichment shape for a search hit — SAME schema for every
    jurisdiction. Jurisdiction-specific decoders (e.g. India CIN) fill what they
    can; unknown fields stay null. Consumers get an identical object everywhere.

    Schema:
        registryId, idScheme, entityType, listed, incorporationYear, status,
        location:{city, region, countryCode, raw}, summary, source
    """
    reg_id = r.get("externalCode")
    enr = {
        "registryId": reg_id,
        "idScheme": None,
        "entityType": None,
        "listed": None,
        "incorporationYear": None,
        "status": r.get("companyStatus"),
        "location": {
            "city": r.get("city") or None,
            "region": None,
            "countryCode": (jur or "").upper() or None,
            "raw": r.get("rawAddress") or None,
        },
        "summary": None,
        "source": "registry",
    }

    # ── jurisdiction-specific decoders write INTO the shape above ──
    if (jur or "").upper() == "IN":
        d = decode_cin(reg_id)
        if d:
            enr["idScheme"] = "CIN"
            enr["entityType"] = d["class"]
            enr["listed"] = d["listed"]
            enr["incorporationYear"] = d["year"]
            enr["location"]["city"] = d["rocCity"]
            enr["location"]["region"] = d["state"]
            enr["source"] = "cin-decode"
    # (future jurisdictions — DE registry court, CN USCC, RU OGRN, ... — all just
    #  fill the same `enr` fields; the returned JSON shape never changes.)

    # human one-liner assembled from whatever is populated (segments joined by " · ")
    head = " ".join(x for x in [
        ("Listed" if enr["listed"] else "Unlisted") if enr["listed"] is not None else None,
        enr["entityType"],
    ] if x)
    city, region = enr["location"]["city"], enr["location"]["region"]
    loc = city or region
    segs = []
    if head:
        segs.append(head)
    if loc:
        segs.append(loc + (" (%s)" % region if city and region and region != city else ""))
    if enr["incorporationYear"]:
        segs.append("est. %d" % enr["incorporationYear"])
    enr["summary"] = " · ".join(segs) or None
    return enr


def _doc_type(label: str) -> str:
    """Canonical machine type derived from a document label:
    'Registered financial statements' -> 'REGISTERED_FINANCIAL_STATEMENTS'."""
    s = "".join(c if c.isalnum() else "_" for c in (label or "").upper())
    while "__" in s:
        s = s.replace("__", "_")
    return s.strip("_")


def jurisdiction_detail(code=None, name=None):
    """Structured coverage for ONE jurisdiction, looked up by ISO code (baked into
    the matrix) or by exact matrix name. Returns None if not found. Documents are
    shaped as {type, description}. No backend call — pure static matrix."""
    juris = jurisdiction_matrix().get("jurisdictions", [])
    entry = None
    if code:
        cu = code.strip().upper()
        entry = next((j for j in juris if (j.get("code") or "").upper() == cu), None)
    if entry is None and name:
        nl = name.strip().lower()
        entry = next((j for j in juris if (j.get("name") or "").strip().lower() == nl), None)
    if entry is None:
        return None

    def docs(arr):
        return [{"type": _doc_type(x), "description": x} for x in (arr or [])]

    access = entry.get("registryAccess") or ""
    registries = [r.strip() for r in access.replace("/", ",").split(",") if r.strip()] or ([access] if access else [])
    return {
        "code": entry.get("code"),
        "name": entry.get("name"),
        "group": entry.get("group"),
        "sla": entry.get("sla"),
        "registries": registries,
        "dataFields": {
            "companyIdentity": entry.get("companyIdentity") or [],
            "controllingEntitiesAndIndividuals": entry.get("controlling") or [],
            "shareholdersPartnersAndUBOs": entry.get("shareholders") or [],
        },
        "baseDocuments": docs(entry.get("documentsMandatory")),
        "additionalDocuments": docs(entry.get("documentsNonMandatory")),
    }


def persist_env(updates: dict):
    """Upsert KEY=VALUE lines into the local .env, preserving other lines/comments."""
    lines = []
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH) as f:
            lines = f.read().splitlines()
    seen = set()
    out = []
    for ln in lines:
        parts = ln.split("=", 1)
        key = parts[0].strip() if len(parts) == 2 else None
        if key in updates:
            out.append(f"{key}={updates[key]}")
            seen.add(key)
        else:
            out.append(ln)
    for key, value in updates.items():
        if key not in seen:
            out.append(f"{key}={value}")
    with open(ENV_PATH, "w") as f:
        f.write("\n".join(out) + "\n")

def list_cases_with_documents(refresh=False):
    """All account cases that currently have >=1 document, via the gateway
    (scope=account). The gateway does the search-by-properties + parallel
    doc-count + caching server-side; returns [{caseCommonId, name, docCount}]."""
    return gw.list_cases(scope="account", with_documents=True, refresh=refresh)

def case_documents_flat(case_common_id):
    """A case's documents via the gateway, flattened to the shape the UI expects:
    {name, documents:[{type, name, category, docId}]}. 'type' is the per-document
    category code (AD/DK/...); 'category' is the human grouping."""
    d = gw.case_documents(case_common_id)
    flat = [{"type": doc.get("type") or "",
             "name": doc.get("name") or "document",
             "category": doc.get("category") or "",
             "docId": doc.get("documentId")}
            for doc in (d.get("documents") or [])]
    return {"name": d.get("name"), "documents": flat}

def fetch_document_bytes(case_common_id, doc_id):
    """Download a document via the backend document-search API."""
    return gw.download_document(case_common_id, doc_id)

def _send_bytes(handler, data, content_type, filename):
    handler.send_response(200)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Disposition", f'attachment; filename="{filename}"')
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)

_ref = {}
def reference():
    if not _ref:

        jrows = gw.jurisdictions(include_uncovered=False)
        out = [{"code": r.get("code"), "name": r.get("name"), "area": r.get("area"),
                "auto": bool(r.get("automated")),
                "priceBand": r.get("priceBand"),
                "priceUsd": r.get("priceUsd")}
               for r in jrows]
        _ref["jurisdictions"] = out
        _ref["automated"] = {r["code"] for r in out if r["auto"]}
        _ref["companyTypes"] = gw.company_types()

        mappings = {}
        for f in gw.legal_forms():
            code = f.get("jurisdiction")
            if not code:
                continue
            mappings.setdefault(code, []).append({
                "local": f.get("local"), "abbr": f.get("abbr"),
                "et": f.get("entityType"), "ct": f.get("companyType")})
        _ref["mappings"] = mappings
    return _ref

def _json(handler, obj, code=200):
    body = json.dumps(obj, default=str).encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)

class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        try:
            if u.path in ("/", "/index.html"):
                with open(INDEX, "rb") as f:
                    body = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            elif u.path == "/api/config":
                _json(self, gw.config_summary())
            elif u.path == "/api/reference":
                ref = reference()
                _json(self, {
                    "jurisdictions": ref["jurisdictions"],
                    "companyTypes": ref["companyTypes"],
                    "mappings": ref["mappings"],
                    "createEnabled": bool(args.enable_create),
                })
            elif u.path == "/betterco-tokens.css":
                # BetterCo design-system tokens (styling only). Linked, not inlined,
                # so the app reads the current token snapshot on every load.
                with open(TOKENS_CSS, "rb") as f:
                    body = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/css; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            elif u.path == "/api/jurisdiction-matrix":
                _json(self, jurisdiction_matrix())
            elif u.path == "/api/jurisdiction":
                code = (q.get("code", [None])[0] or "").strip() or None
                name = (q.get("name", [None])[0] or q.get("q", [None])[0] or "").strip() or None
                if not code and not name:
                    return _json(self, {"error": "code or name required"}, 400)
                detail = jurisdiction_detail(code=code, name=name)
                if detail is None:
                    return _json(self, {"error": "jurisdiction not found",
                                        "hint": "use an ISO code (e.g. DE) or exact matrix name (e.g. Germany, Alberta, Alabama)"}, 404)
                _json(self, detail)
            elif u.path == "/api/search":
                jur = (q.get("jurisdiction", [""])[0] or "").strip().upper()
                query = (q.get("query", [""])[0] or "").strip()
                ds = (q.get("datasource", [""])[0] or "").strip() or None
                if not jur or not query:
                    return _json(self, {"error": "jurisdiction and query required"}, 400)
                results = gw.search(jurisdiction=jur, query=query, datasource=ds)
                # Attach ONE generic `enrichment` object to every hit (same schema for
                # all jurisdictions) so the free search surfaces location/type/etc. that
                # the raw address may hide (e.g. India's address is truncated to state).
                if isinstance(results, list):
                    for r in results:
                        if isinstance(r, dict):
                            r["enrichment"] = enrich_search_result(jur, r)
                _json(self, {"jurisdiction": jur, "query": query, "results": results})
            elif u.path == "/api/case":
                cid = q.get("id", [None])[0]
                st = gw.case_status(cid)
                _json(self, {
                    "caseCommonId": st.get("caseCommonId", cid),
                    "statusName": st.get("statusName"),
                    "complete": st.get("complete"),
                    "caseReadyDatetime": st.get("caseReadyDatetime"),
                    "ready": bool(st.get("ready")),
                })
            elif u.path == "/api/cases":
                qq = (q.get("q", [""])[0] or "").strip()
                cases = gw.list_cases(scope="account", with_documents=True,
                                      q=(qq or None),
                                      refresh=q.get("refresh", [""])[0] == "1")
                _json(self, {"cases": cases[:300], "total": len(cases)})
            elif u.path == "/api/case-docs":
                cid = q.get("id", [None])[0]
                if not cid:
                    return _json(self, {"error": "case id required"}, 400)
                _json(self, case_documents_flat(cid))
            elif u.path == "/api/case-doc":
                cid = q.get("id", [None])[0]
                did = q.get("doc", [None])[0]
                if not cid or not did:
                    return _json(self, {"error": "case id and document id required"}, 400)
                data, ctype = fetch_document_bytes(cid, did)
                ext = "pdf" if "pdf" in (ctype or "").lower() else "bin"
                _send_bytes(self, data, ctype or "application/octet-stream",
                            f"case{cid}_doc{did}.{ext}")
            else:
                _json(self, {"error": "not found"}, 404)
        except Exception as e:
            _json(self, {"error": str(e)}, 500)

    def do_POST(self):
        u = urlparse(self.path)
        n = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(n) or b"{}")
        try:
            if u.path == "/api/config":
                # base_url + workspace update when provided; key/secret only when non-empty
                # (blank secret field = keep the existing one).
                gw.configure(
                    base_url=(payload.get("baseUrl") or "").strip() or None,
                    workspace_id=(payload.get("workspaceId") or "").strip() or None,
                    api_key=(payload.get("apiKey") or "").strip() or None,
                    api_secret=(payload.get("apiSecret") or "").strip() or None,
                )
                if not gw.is_configured():
                    return _json(self, {"ok": False,
                                        "error": "Base URL, workspace, key and secret are all required."}, 400)
                try:
                    gw.company_types()  # end-to-end check: auth + workspace membership + gateway
                except Exception as e:
                    return _json(self, {"ok": False, "error": f"Could not connect: {str(e)[:200]}"}, 400)
                persist_env({
                    "BETTERCO_BASE_URL": gw.base_url,
                    "BETTERCO_WORKSPACE_ID": gw.workspace_id,
                    "BETTERCO_API_KEY": gw.api_key,
                    "BETTERCO_API_SECRET": gw.api_secret,
                })
                _ref.clear()  # drop reference cached under the previous workspace
                return _json(self, {"ok": True, "config": gw.config_summary()})
            if u.path == "/api/create-case":
                jur = (payload.get("jurisdiction") or "").strip().upper()
                name = (payload.get("name") or "").strip()
                if not jur or not name:
                    return _json(self, {"error": "jurisdiction and name required"}, 400)

                body = {"jurisdiction": jur, "name": name,
                        "journeyName": payload.get("journeyName") or "All"}
                for key in ("externalCode", "legalType", "entityType", "companyType",
                            "addressLine1", "postcode", "city"):
                    if payload.get(key):
                        body[key] = payload[key]

                status, data = gw.create_case(body)
                if status >= 400:
                    return _json(self, {"error": data.get("message") or data.get("error")
                                        or f"create failed ({status})"}, status)
                data.setdefault("posted", body)
                _json(self, data)
            else:
                _json(self, {"error": "not found"}, 404)
        except Exception as e:
            _json(self, {"error": str(e)}, 500)

def main():
    try:
        reference()
        print("Reference data loaded (jurisdictions + company types).")
    except Exception as e:
        print(f"WARNING: could not preload reference data ({str(e)[:80]}) — "
              f"will retry lazily on first request.")

    def _warm_cases():
        try:
            n = len(list_cases_with_documents())
            print(f"Document case list pre-warmed ({n} cases with documents).")
        except Exception as e:
            print(f"WARNING: case list pre-warm failed ({str(e)[:80]}).")
    threading.Thread(target=_warm_cases, daemon=True).start()

    srv = ThreadingHTTPServer(("127.0.0.1", args.port), H)
    url = f"http://localhost:{args.port}/"
    mode = "LIVE (billable creates ENABLED)" if args.enable_create else "DRY-RUN (safe)"
    print(f"Document search app running at {url}")
    print(f"Mode: {mode}")
    print("Ctrl+C to stop.")
    if not args.no_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()

if __name__ == "__main__":
    main()
