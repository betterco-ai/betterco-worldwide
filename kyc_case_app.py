
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
import requests
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


def _doc_type(label: str) -> str:
    """Canonical machine type derived from a document label:
    'Registered financial statements' -> 'REGISTERED_FINANCIAL_STATEMENTS'."""
    s = "".join(c if c.isalnum() else "_" for c in (label or "").upper())
    while "__" in s:
        s = s.replace("__", "_")
    return s.strip("_")


def jurisdiction_detail(code=None, name=None):
    """Structured coverage for ONE jurisdiction. Returns None if not found.

    Live from the gateway when an ISO code is supplied and the gateway has a
    coverage row for it; otherwise from the static matrix. `source` records which
    answered ("gateway" | "matrix") so the UI can say whether it is showing live
    data or the snapshot.

    The fallback is not just belt-and-braces: 89 of the matrix's 217 rows have no
    ISO code (the 50 US states, 14 Canadian provinces, and code-less entries like
    Anguilla), so the gateway cannot address them at all — they are name-only
    lookups. The 128 coded rows map 1:1 onto the gateway's 128 coverage rows.
    """
    if code:
        try:
            live = gw.jurisdiction_coverage(code.strip().upper())
            if live:
                live["source"] = "gateway"
                return live
        except requests.HTTPError as e:
            # 404 = priced but uncovered (AF/BD/GH) — expected; fall through to the
            # matrix, which has no row for them either, so the caller gets a 404.
            sc = e.response.status_code if e.response is not None else None
            if sc != 404:
                print(f"WARNING: coverage lookup failed for {code} (HTTP {sc}) — using snapshot.")
        except (requests.Timeout, requests.ConnectionError, ValueError) as e:
            # Unreachable or unconfigured gateway: serve the snapshot rather than
            # fail, but `source` will say "matrix" so it is never passed off as live.
            print(f"WARNING: coverage unavailable for {code} ({type(e).__name__}) — using snapshot.")

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
        "source": "matrix",
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
    """All workspace cases that currently have >=1 document, via the gateway
    (scope=workspace — the only scope that carries `ready`/`statusName`). The
    gateway does the search-by-properties + parallel doc-count + caching
    server-side; returns [{caseCommonId, name, docCount, ready, statusName}]."""
    return gw.list_cases(scope="workspace", with_documents=True, refresh=refresh)

def case_documents_flat(case_common_id, include_pending=True):
    """A case's documents via the gateway, flattened to the shape the UI expects:
    {name, documents:[{type, name, category, docId, availability}]}. 'type' is the
    per-document category code (AD/DK/...); 'category' is the human grouping.

    include_pending=True (default) also surfaces documents while the case is still
    building. 'availability' is available | pending | missing; a missing row is a
    placeholder for a gap and carries no docId, so it can't be downloaded."""
    d = gw.case_documents(case_common_id, include_pending=include_pending)
    flat = [{"type": doc.get("type") or "",
             "name": doc.get("name") or "document",
             "category": doc.get("category") or "",
             "docId": doc.get("documentId"),
             "availability": doc.get("availability") or ""}
            for doc in (d.get("documents") or [])]
    return {"name": d.get("name"), "documents": flat}

def fetch_document_bytes(case_common_id, doc_id, include_pending=True):
    """Download a document via the backend document-search API. include_pending
    mirrors how the document was listed (see case_documents_flat)."""
    return gw.download_document(case_common_id, doc_id, include_pending=include_pending)

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

def _upstream_error(exc):
    """Pull a clean, user-facing message out of a gateway HTTPError. The gateway
    wraps registry errors as {"message": 'KYC.com upstream error: "<real msg>"'};
    unwrap that so the user sees e.g. 'More than 200 records found in France,
    please refine your search criteria.' rather than '400 Client Error'."""
    resp = getattr(exc, "response", None)
    msg = None
    if resp is not None:
        try:
            msg = (resp.json() or {}).get("message") or (resp.json() or {}).get("error")
        except Exception:
            msg = (getattr(resp, "text", "") or "")[:300]
    msg = msg or str(exc)
    m = re.search(r'upstream error:\s*"?(.+?)"?\s*$', msg)
    return m.group(1) if m else msg


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
                # The page is read from disk on every request, so it is never stale
                # server-side — but without this the browser caches it and keeps
                # showing an old UI after the HTML changes.
                self.send_header("Cache-Control", "no-store, must-revalidate")
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
                self.send_header("Cache-Control", "no-store, must-revalidate")
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
                try:
                    results = gw.search(jurisdiction=jur, query=query, datasource=ds)
                except requests.HTTPError as e:
                    # The registry often returns a helpful message (e.g. "More than 200
                    # records found … please refine your search criteria") as a 4xx —
                    # surface it instead of a generic 500.
                    msg = _upstream_error(e)
                    refine = any(k in msg.lower() for k in
                                 ("refine", "more than", "adjust your search", "too many", "200 record"))
                    return _json(self, {"error": msg, "refine": refine,
                                        "jurisdiction": jur, "query": query}, 400)
                except (requests.Timeout, requests.ConnectionError):
                    # Some registries (e.g. Cayman) are very slow and can hang for minutes.
                    # Fail fast with clear guidance rather than a long wait + cryptic error.
                    return _json(self, {"error": "This registry is taking too long to respond "
                                        "(some jurisdictions, e.g. Cayman, are slow). Please refine "
                                        "your search or try again in a moment.",
                                        "slow": True, "jurisdiction": jur, "query": query}, 504)
                # Each hit carries the gateway's own `enrichment` object (one schema for
                # every jurisdiction) surfacing location/type the raw address may hide —
                # e.g. India's address is truncated to the state, but the CIN yields the
                # city. Passed straight through; the app decoded this itself until the
                # gateway adopted the same decoders (verified field-identical).
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
                cases = gw.list_cases(scope="workspace", with_documents=True,
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
                # Manual (no-registry-search) jurisdictions can't anchor on an externalCode,
                # so the address block + province + registry number are what let the upstream
                # locate the right entity; unregisteredEntity flags an entity with no register
                # entry at all. All optional; forwarded straight through to the gateway.
                for key in ("externalCode", "legalType", "entityType", "companyType",
                            "addressLine1", "addressLine2", "postcode", "city", "province",
                            "unregisteredEntity"):
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
