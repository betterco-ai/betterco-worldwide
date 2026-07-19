"""INPI RNE client — FREE direct access to French company documents.

France's free direct-vendor route (the counterpart to hr.de for Germany), but via a real
REST API instead of a browser scraper. Serves the actual filing PDFs — **statuts** (articles /
Gesellschaftsvertrag), **actes** (deeds/amendments), **comptes annuels** (annual accounts) —
from the Registre National des Entreprises, free of charge.

Provider shape mirrors `HandelsregisterClient` so it drops into the same doc-kind router:

    from inpi_client import InpiClient
    with InpiClient() as inpi:               # creds from INPI_USERNAME / INPI_PASSWORD (.env)
        hits = inpi.search("552081317")      # by SIREN (9 digits) — or a name (best-effort)
        inpi.download("552081317", "articles", "outputs/inpi/statuts.pdf")   # statuts PDF
        inpi.download("552081317", "financial", "outputs/inpi/comptes.pdf")  # latest accounts

Auth: POST /api/sso/login {username,password} -> JWT; sent as Authorization: Bearer; re-login
on 401. Free account at data.inpi.fr; activate the RNE / Actes / Comptes packages.

Coverage: actes/statuts from 1993, comptes from 2017. Comptes a company declared confidential
are not distributed (surfaced here as DocumentUnavailable). Fair use: single-threaded, throttle
between calls (INPI blocks parallel requests; ~10k req/day soft cap).

The **Kbis** register extract (the Registerauszug equivalent) is NOT on INPI — it comes from
Infogreffe (paid, ~3.06 EUR). Asking this client for it raises KbisViaInfogreffe by design.

CONFIDENCE: the /sso/login, /companies/{siren} paths and 1993/2017 coverage are primary-sourced
(INPI docs). The /companies/{siren}/attachments and /{actes,bilans}/{id}/download paths and the
attachment JSON field names are SECONDARY-confirmed (a working third-party implementation,
consistent with INPI's confirmed base host). The response parsing here is deliberately defensive;
validate the exact field names against a live account + the official Actes/Comptes technical PDFs
before relying on it in production. Spots to check are marked `# SECONDARY`.
"""
from __future__ import annotations

import logging
import os
import re
import time
from pathlib import Path

import requests

log = logging.getLogger("inpi")

BASE = "https://registre-national-entreprises.inpi.fr/api"

# doc_type -> INPI attachment channel. Vocabulary chosen to line up with hr.de's doc_types
# (articles / financial) so both providers present the same surface to the router.
DOC_TYPE_CHANNEL = {
    "articles": "acte",     # statuts (Gesellschaftsvertrag/Satzung), filed within `actes`
    "statuts": "acte",
    "satzung": "acte",
    "actes": "acte",        # any deed / amendment
    "financial": "bilan",   # comptes annuels (annual accounts)
    "comptes": "bilan",
}
# For 'articles'/'statuts' we additionally filter actes down to the statuts by label.
STATUTS_NEEDLES = ("statut", "articles of association")
# doc_types that mean "the register extract" — NOT on INPI; Infogreffe (paid) only.
KBIS_TYPES = {"extract", "kbis", "registerauszug", "register_extract"}


class InpiError(RuntimeError):
    pass


class InpiAuthError(InpiError):
    pass


class DocumentUnavailable(InpiError):
    """Listed in metadata but not downloadable — confidential comptes, or not yet digitised
    (mirrors the registry `missing`-doc pattern: present but no downloadable file)."""


class KbisViaInfogreffe(InpiError):
    """The Kbis / register extract is not served by INPI — order it from Infogreffe (paid,
    ~3.06 EUR electronic). Raised on purpose so a caller routes it to the paid vendor."""


class InpiClient:
    def __init__(self, username: str | None = None, password: str | None = None,
                 download_dir: str = "outputs/inpi", base: str = BASE,
                 throttle_s: float = 0.5, timeout_s: int = 60, max_retries: int = 3):
        self.username = username or os.getenv("INPI_USERNAME")
        self.password = password or os.getenv("INPI_PASSWORD")
        self.base = base.rstrip("/")
        self.download_dir = Path(download_dir)
        self.throttle_s = throttle_s
        self.timeout_s = timeout_s
        self.max_retries = max_retries
        self.session = requests.Session()
        self._token: str | None = None
        self._last_call = 0.0

    # ── lifecycle ───────────────────────────────────────────────────────────
    def __enter__(self) -> "InpiClient":
        return self

    def __exit__(self, *exc):
        self.session.close()

    # ── auth ────────────────────────────────────────────────────────────────
    def _login(self):
        if not self.username or not self.password:
            raise InpiAuthError("Missing INPI credentials (set INPI_USERNAME / INPI_PASSWORD "
                                "or pass username=/password=).")
        r = self.session.post(f"{self.base}/sso/login",
                              json={"username": self.username, "password": self.password},
                              timeout=self.timeout_s)
        if r.status_code in (401, 403):
            raise InpiAuthError(f"INPI login rejected ({r.status_code}) — check credentials.")
        r.raise_for_status()
        tok = (r.json() or {}).get("token")
        if not tok:
            raise InpiAuthError("INPI login returned no token.")
        self._token = tok
        log.info("authenticated to INPI RNE")

    def _throttle(self):
        # single-threaded politeness — INPI blocks parallel requests
        wait = self.throttle_s - (time.monotonic() - self._last_call)
        if wait > 0:
            time.sleep(wait)
        self._last_call = time.monotonic()

    def _request(self, method: str, path: str, *, stream: bool = False, **kw):
        """Authenticated request with lazy login, one 401 re-login, and backoff on 429/5xx."""
        if self._token is None:
            self._login()
        url = f"{self.base}{path}"
        for attempt in range(self.max_retries):
            self._throttle()
            headers = {**kw.pop("headers", {}), "Authorization": f"Bearer {self._token}"}
            r = self.session.request(method, url, headers=headers, stream=stream,
                                     timeout=self.timeout_s, **kw)
            if r.status_code == 401 and attempt == 0:
                log.info("token expired — re-authenticating")
                self._login()
                continue
            if r.status_code == 429 or r.status_code >= 500:
                back = 2 ** attempt
                log.warning("INPI %s on %s — backoff %ss", r.status_code, path, back)
                time.sleep(back)
                continue
            return r
        raise InpiError(f"INPI request failed after {self.max_retries} attempts: {method} {path}")

    # ── SIREN helpers ───────────────────────────────────────────────────────
    @staticmethod
    def _norm_siren(value: str) -> str:
        digits = re.sub(r"\D", "", value or "")
        if len(digits) == 14:      # a SIRET — the SIREN is its first 9 digits
            digits = digits[:9]
        if len(digits) != 9:
            raise ValueError(f"not a SIREN (need 9 digits): {value!r}")
        return digits

    @staticmethod
    def _looks_like_siren(value: str) -> bool:
        return len(re.sub(r"\D", "", value or "")) in (9, 14)

    # ── company + documents ─────────────────────────────────────────────────
    def get_company(self, siren: str) -> dict:
        siren = self._norm_siren(siren)
        r = self._request("GET", f"/companies/{siren}")
        if r.status_code == 404:
            raise InpiError(f"no INPI company for SIREN {siren}")
        r.raise_for_status()
        return r.json()

    def search(self, query: str) -> list[dict]:
        """Provider-parity search. A 9/14-digit query is resolved directly by SIREN (the clean,
        reliable path). A name query is best-effort against the companyName filter and is marked
        unverified — in the BetterCo flow the SIREN normally comes from the case / registry search,
        so prefer passing a SIREN."""
        if self._looks_like_siren(query):
            siren = self._norm_siren(query)
            try:
                c = self.get_company(siren)
            except InpiError:
                return []
            return [{"siren": siren, "name": _company_name(c), "raw": c}]
        # SECONDARY: name search endpoint/param not primary-confirmed; best-effort.
        r = self._request("GET", "/companies", params={"companyName": query})
        if not r.ok:
            log.warning("INPI name search unsupported/failed (%s) — pass a SIREN instead",
                        r.status_code)
            return []
        data = r.json()
        items = data if isinstance(data, list) else (data.get("content") or data.get("items") or [])
        out = []
        for c in items:
            s = _dig(c, "siren") or _dig(c, "formality", "siren")
            if s:
                out.append({"siren": s, "name": _company_name(c), "raw": c})
        return out

    def list_documents(self, siren: str) -> dict:
        """{'actes': [...], 'bilans': [...]} — each item normalized to
        {id, kind, date, label, downloadable}. SECONDARY: attachment field names."""
        siren = self._norm_siren(siren)
        r = self._request("GET", f"/companies/{siren}/attachments")
        if r.status_code == 404:
            return {"actes": [], "bilans": []}
        r.raise_for_status()
        data = r.json() or {}
        actes_raw = data.get("actes") or []
        bilans_raw = data.get("bilans") or data.get("comptesAnnuels") or []
        return {
            "actes": [_norm_attachment(a, "acte") for a in actes_raw],
            "bilans": [_norm_attachment(b, "bilan") for b in bilans_raw],
        }

    # ── downloads ───────────────────────────────────────────────────────────
    def download(self, siren: str, doc_type: str, dest_path: str, which: str = "latest") -> str:
        """Resolve a doc_type to a specific document and save its PDF. Returns the saved path.

        doc_type ∈ articles/statuts, actes, financial/comptes. `which`='latest' (default) picks
        the most recent matching document; 'all' is not implemented here (call the id-level
        methods for that). Asking for the Kbis raises KbisViaInfogreffe."""
        dt = doc_type.lower()
        if dt in KBIS_TYPES:
            raise KbisViaInfogreffe(
                "The Kbis register extract is not available from INPI — order it from Infogreffe "
                "(paid, ~3.06 EUR electronic). Route doc_type='extract' to the infogreffe vendor.")
        channel = DOC_TYPE_CHANNEL.get(dt)
        if channel is None:
            raise ValueError(f"unknown doc_type {doc_type!r}; choose from "
                             f"{sorted(set(DOC_TYPE_CHANNEL))} (or 'extract' -> Infogreffe)")
        docs = self.list_documents(siren)
        pool = docs["actes"] if channel == "acte" else docs["bilans"]
        if channel == "acte" and dt in ("articles", "statuts", "satzung"):
            statuts = [d for d in pool if _matches(d["label"], STATUTS_NEEDLES)]
            pool = statuts or pool  # fall back to all actes if none is labelled 'statuts'
        pool = [d for d in pool if d["downloadable"]]
        if not pool:
            raise DocumentUnavailable(
                f"no downloadable '{doc_type}' for SIREN {siren} "
                f"(none filed, or confidential/not digitised).")
        pool.sort(key=lambda d: d["date"] or "", reverse=(which == "latest"))
        doc = pool[0]
        if doc["kind"] == "acte":
            return self.download_acte(doc["id"], dest_path)
        return self.download_bilan(doc["id"], dest_path)

    def download_acte(self, acte_id: str, dest_path: str) -> str:
        return self._download(f"/actes/{acte_id}/download", dest_path, f"acte {acte_id}")

    def download_bilan(self, bilan_id: str, dest_path: str) -> str:
        return self._download(f"/bilans/{bilan_id}/download", dest_path, f"bilan {bilan_id}")

    def _download(self, path: str, dest_path: str, what: str) -> str:
        r = self._request("GET", path, stream=True)
        if r.status_code in (404, 403):
            raise DocumentUnavailable(f"{what}: not downloadable ({r.status_code}) — "
                                      "likely confidential or not digitised.")
        r.raise_for_status()
        dest = Path(dest_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        first = next(r.iter_content(chunk_size=8192), b"")
        # INPI serves application/pdf; guard against an HTML/JSON error body sneaking through.
        if first[:4] != b"%PDF" and b"pdf" not in (r.headers.get("content-type", "").lower()).encode():
            raise DocumentUnavailable(f"{what}: response was not a PDF "
                                      f"(content-type {r.headers.get('content-type')!r}).")
        with open(dest, "wb") as fh:
            fh.write(first)
            for chunk in r.iter_content(chunk_size=8192):
                fh.write(chunk)
        log.info("saved %s (%d bytes) <- %s", dest, dest.stat().st_size, what)
        return str(dest)


# ── module helpers ──────────────────────────────────────────────────────────
def _dig(d: dict, *keys):
    cur = d
    for k in keys:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
    return cur


def _company_name(c: dict) -> str | None:
    # SECONDARY: the RNE company payload nests naming under formality/content — try a few paths.
    for path in (("formality", "content", "personneMorale", "identite", "entreprise", "denomination"),
                 ("formality", "content", "personneMorale", "denomination"),
                 ("denomination",), ("companyName",), ("name",)):
        v = _dig(c, *path)
        if v:
            return v
    return None


def _norm_attachment(item: dict, kind: str) -> dict:
    """Normalize an acte/bilan entry. SECONDARY: field names — parse defensively."""
    doc_id = item.get("id") or _dig(item, "acte", "id") or _dig(item, "bilan", "id")
    date = (item.get("dateDepot") or item.get("dateCloture") or item.get("date")
            or _dig(item, "acte", "dateDepot") or "")
    # label: acte type name(s) or filename — used to pick statuts out of the actes pile
    label_parts = []
    for k in ("nomDocument", "typeRdd", "libelle", "typeActe"):
        v = item.get(k)
        if isinstance(v, str):
            label_parts.append(v)
        elif isinstance(v, list):
            label_parts += [str(x.get("typeActe") if isinstance(x, dict) else x) for x in v]
    types = item.get("typeRdd") or []
    if isinstance(types, list):
        for t in types:
            if isinstance(t, dict):
                label_parts.append(str(t.get("typeActe") or t.get("libelle") or ""))
    label = " ".join(p for p in label_parts if p)
    confidential = bool(item.get("confidentiality") or item.get("confidentialite")
                        or item.get("confidentialCompteResultat"))
    downloadable = bool(doc_id) and not confidential
    return {"id": doc_id, "kind": kind, "date": date, "label": label,
            "downloadable": downloadable, "confidential": confidential, "raw": item}


def _matches(label: str, needles) -> bool:
    low = (label or "").lower()
    return any(n in low for n in needles)


# ── CLI ──────────────────────────────────────────────────────────────────────
def _main(argv):
    import argparse
    ap = argparse.ArgumentParser(description="INPI RNE free document client (France)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("search"); sp.add_argument("query")
    dl = sub.add_parser("download")
    dl.add_argument("siren")
    dl.add_argument("docs", nargs="+", help="doc types: " + ", ".join(sorted(set(DOC_TYPE_CHANNEL))))
    dl.add_argument("--outdir", default="outputs/inpi")
    st = sub.add_parser("selftest", help="offline checks (no network/creds)")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    if args.cmd == "selftest":
        return _selftest()
    if args.cmd == "search":
        with InpiClient() as c:
            for h in c.search(args.query):
                print(f"{h['siren']}  {h['name']}")
        return 0
    if args.cmd == "download":
        out = Path(args.outdir)
        with InpiClient() as c:
            for doc in args.docs:
                dest = out / f"{args.siren}_{doc}.pdf"
                try:
                    print(f"  [ok]   {doc}: {c.download(args.siren, doc, str(dest))}")
                except KbisViaInfogreffe as e:
                    print(f"  [kbis] {doc}: {e}")
                except InpiError as e:
                    print(f"  [FAIL] {doc}: {e}")
        return 0
    return 1


def _selftest() -> int:
    """No-network sanity checks: SIREN normalization, doc_type routing, attachment parsing."""
    ok = True

    def check(name, cond):
        nonlocal ok
        print(("PASS " if cond else "FAIL ") + name)
        ok = ok and cond

    check("SIREN from spaced string", InpiClient._norm_siren("552 081 317") == "552081317")
    check("SIREN from SIRET (14->9)", InpiClient._norm_siren("55208131700024") == "552081317")
    try:
        InpiClient._norm_siren("123"); check("reject short SIREN", False)
    except ValueError:
        check("reject short SIREN", True)
    check("looks_like_siren name", InpiClient._looks_like_siren("Founders1") is False)
    check("articles routes to acte", DOC_TYPE_CHANNEL["articles"] == "acte")
    check("financial routes to bilan", DOC_TYPE_CHANNEL["financial"] == "bilan")
    check("kbis is Infogreffe-only", "extract" in KBIS_TYPES)
    a = _norm_attachment({"id": "X1", "dateDepot": "2001-05-03",
                          "typeRdd": [{"typeActe": "Statuts mis à jour"}]}, "acte")
    check("acte parsed + labelled", a["id"] == "X1" and _matches(a["label"], STATUTS_NEEDLES)
          and a["downloadable"])
    b = _norm_attachment({"id": "B1", "dateCloture": "2022-12-31", "confidentialite": True}, "bilan")
    check("confidential bilan not downloadable", b["confidential"] and not b["downloadable"])
    print("\nSELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    raise SystemExit(_main(sys.argv[1:]))
