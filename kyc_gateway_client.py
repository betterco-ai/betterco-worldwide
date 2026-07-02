"""Client for the BetterCo backend document-search REST API.

This is what the local app talks to instead of calling KnowYourCustomer.com
directly: upstream OAuth, reads, and billable creates all happen server-side in
the BetterCo backend. The app never sees upstream credentials or endpoints.

Auth: BetterCo REST API key+secret -> Partner JWT (POST /restapi/v1/auth/login),
1h TTL, auto-refreshed. Same scheme as betterco_client.py.

Endpoints (all under /restapi/v1/workspaces/{workspaceId}/document-search):
    GET  /jurisdictions?includeUncovered=          reference (with price bands)
    GET  /company-types                            reference
    GET  /legal-forms?jurisdiction=                reference (gateway-owned mapping)
    GET  /cases/search?jurisdiction=&query=        registry search (automated only)
    GET  /cases?scope=&withDocuments=&q=&refresh=  case list (scope=account|workspace)
    GET  /cases/{caseCommonId}                     status by caseCommonId
    GET  /cases/{caseCommonId}/documents           documents by caseCommonId
    GET  /cases/{caseCommonId}/documents/{id}/content   download (binary)
    POST /cases                                      create (BILLABLE, workspace-scoped)

Required .env:
    DOCUMENT_SEARCH_BASE_URL                  backend base URL (default http://localhost:8080; falls back to BETTERCO_BASE_URL)
    BETTERCO_API_KEY / BETTERCO_API_SECRET   REST key+secret for the JWT login
    BETTERCO_WORKSPACE_ID                    workspace the requests are scoped to
"""
from __future__ import annotations

import os
import time
import logging
import requests
from dotenv import load_dotenv

load_dotenv()
log = logging.getLogger("document_search")

class KycGatewayClient:
    """Thin HTTP client for BetterCo document search (no KYC.com access here)."""

    def __init__(self):
        self.base_url = None
        self.api_key = None
        self.api_secret = None
        self.workspace_id = None
        self.session = requests.Session()
        self._token: str | None = None
        self._token_expiry: float = 0.0
        # Seed from environment; missing values just leave the app unconfigured
        # (the setup page collects them at runtime — no hard failure on startup).
        self.configure(
            base_url=os.getenv("DOCUMENT_SEARCH_BASE_URL") or os.getenv("BETTERCO_BASE_URL") or "http://localhost:8080",
            api_key=os.getenv("BETTERCO_API_KEY"),
            api_secret=os.getenv("BETTERCO_API_SECRET"),
            workspace_id=os.getenv("BETTERCO_WORKSPACE_ID"),
        )

    def configure(self, base_url=None, api_key=None, api_secret=None, workspace_id=None):
        """Set/override connection settings and reset the cached token."""
        if base_url is not None:
            self.base_url = base_url.rstrip("/")
        if api_key is not None:
            self.api_key = api_key
        if api_secret is not None:
            self.api_secret = api_secret
        if workspace_id is not None:
            self.workspace_id = workspace_id
        self._token = None
        self._token_expiry = 0.0
        self.session.headers.pop("Authorization", None)

    def is_configured(self) -> bool:
        return bool(self.base_url and self.api_key and self.api_secret and self.workspace_id)

    def config_summary(self) -> dict:
        """Non-secret view of the current config for the setup UI."""
        return {"baseUrl": self.base_url, "workspaceId": self.workspace_id,
                "hasKey": bool(self.api_key), "hasSecret": bool(self.api_secret),
                "configured": self.is_configured()}

    def connect(self):
        """Force a fresh login to validate the current settings (raises on failure)."""
        self._token = None
        self._ensure_auth()

    def _ensure_auth(self):
        if not self.is_configured():
            raise ValueError("Not configured — set base URL, workspace, key and secret first.")
        if self._token and time.time() < self._token_expiry - 60:
            return
        url = f"{self.base_url}/restapi/v1/auth/login"
        r = self.session.post(url, json={"key": self.api_key, "secret": self.api_secret}, timeout=30)
        r.raise_for_status()
        self._token = r.json()["token"]
        self._token_expiry = time.time() + 3600 - 300
        self.session.headers["Authorization"] = f"Bearer {self._token}"
        log.info("Authenticated to BetterCo document search (token ~55min)")

    def _ws(self, path: str) -> str:
        return f"{self.base_url}/restapi/v1/workspaces/{self.workspace_id}{path}"

    def _get(self, path: str, params: dict | None = None):
        self._ensure_auth()
        r = self.session.get(self._ws(path), params=params, timeout=60)
        r.raise_for_status()
        return r.json()

    def _get_bytes(self, path: str) -> tuple[bytes, str]:
        self._ensure_auth()
        r = self.session.get(self._ws(path), timeout=120)
        r.raise_for_status()
        return r.content, r.headers.get("content-type", "application/octet-stream")

    def jurisdictions(self, include_uncovered: bool = False) -> list[dict]:
        return self._get("/document-search/jurisdictions", {"includeUncovered": str(include_uncovered).lower()})

    def company_types(self) -> list[str]:
        return self._get("/document-search/company-types")

    def legal_forms(self, jurisdiction: str | None = None) -> list[dict]:
        return self._get("/document-search/legal-forms", {"jurisdiction": jurisdiction} if jurisdiction else None)

    def search(self, jurisdiction: str, query: str, datasource: str | None = None) -> list[dict]:
        params = {"jurisdiction": jurisdiction, "query": query}
        if datasource:
            params["datasource"] = datasource
        return self._get("/document-search/cases/search", params)

    def list_cases(self, scope: str = "account", with_documents: bool = True,
                   q: str | None = None, refresh: bool = False) -> list[dict]:
        params = {"scope": scope, "withDocuments": str(with_documents).lower(),
                  "refresh": str(refresh).lower()}
        if q:
            params["q"] = q
        return self._get("/document-search/cases", params)

    def case_status(self, case_common_id) -> dict:
        return self._get(f"/document-search/cases/{case_common_id}")

    def case_documents(self, case_common_id) -> dict:
        return self._get(f"/document-search/cases/{case_common_id}/documents")

    def download_document(self, case_common_id, document_id) -> tuple[bytes, str]:
        return self._get_bytes(f"/document-search/cases/{case_common_id}/documents/{document_id}/content")

    CREATE_WAIT_SECONDS = 25

    def create_case(self, body: dict) -> tuple[int, dict]:
        """Workspace-scoped (proxy) create — no betterco customer required.
        POST /document-search/cases. Returns (status_code, json).

        A real create can take a long time upstream (the case is built over several
        minutes). We wait up to CREATE_WAIT_SECONDS for a quick answer — a validation
        error, a dry-run, or a fast create — and otherwise return a 202 "processing"
        acknowledgment. The backend keeps building and persists the case regardless, so
        it shows up in the cases list shortly after.
        """
        self._ensure_auth()
        payload = {**body, "confirm": True}
        try:
            r = self.session.post(self._ws("/document-search/cases"), json=payload,
                                  timeout=self.CREATE_WAIT_SECONDS)
            return r.status_code, self._json(r)
        except requests.exceptions.Timeout:
            return 202, {"processing": True,
                         "message": "Case creation started — it is being built and will "
                                    "appear in your cases shortly."}

    @staticmethod
    def _json(r):
        try:
            return r.json()
        except ValueError:
            return {"error": r.text}
