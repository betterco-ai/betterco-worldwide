
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
import os, sys, json, argparse, threading, webbrowser
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
ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")


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
            elif u.path == "/api/search":
                jur = (q.get("jurisdiction", [""])[0] or "").strip().upper()
                query = (q.get("query", [""])[0] or "").strip()
                ds = (q.get("datasource", [""])[0] or "").strip() or None
                if not jur or not query:
                    return _json(self, {"error": "jurisdiction and query required"}, 400)
                results = gw.search(jurisdiction=jur, query=query, datasource=ds)
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
