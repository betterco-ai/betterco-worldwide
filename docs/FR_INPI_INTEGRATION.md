# France — direct registry integration via INPI RNE (build spec)

**Verdict: build it for statuts / actes / comptes annuels.** Free, JWT-secured REST API, simple
three-call flow, covers exactly those three document kinds. No aggregation vendor needed for them.
**Two carve-outs** (below): the legally-recognised **Kbis** extract is NOT on INPI (paid Infogreffe),
and **PDF redistribution rights** must be confirmed against the licence before shipping.

Feeds the vendor-neutral routing ([[vendor-neutral-aggregator-architecture]]): FR becomes the first
**split-vendor** jurisdiction — `inpi.rne` (free) for articles/deeds/accounts, `infogreffe` (paid)
for the certified register extract.

## Don't confuse the two "INPI APIs"
- **RNE Open Data API** — host `registre-national-entreprises.inpi.fr` — free, self-service, and the
  one that serves **document PDFs**. ← this is the one we build against.
- **API Entreprise** (`entreprise.api.gouv.fr`) — habilitation-gated (public administrations); returns
  a JSON + PDF *attestation d'immatriculation*, NOT the filing documents. Not our channel.

## 1. Onboarding
Register a free account at **data.inpi.fr** ("Espace Open Data"), then self-activate the packages
under "Mes accès API/SFTP": Base RNE, Comptes annuels, Actes. Free, open to anyone, effectively
immediate (no habilitation gate). Ref: `https://data.inpi.fr/content/editorial/Acces_API_Entreprises`.

## 2. Auth
```
POST https://registre-national-entreprises.inpi.fr/api/sso/login
Content-Type: application/json
{ "username": "<email>", "password": "<password>" }
→ 200 { "token": "<JWT>", "user": {...} }
```
Pass `Authorization: Bearer <JWT>` on all subsequent calls. Token is a short-lived session JWT —
**re-login on 401** (exact lifetime not documented). Pre-prod host:
`registre-national-entreprises-pprod.inpi.fr` for integration testing.

## 3. Document flow (list → id → download)
```
GET /api/companies/{siren}/attachments        (Bearer)   → JSON: { actes:[...], bilans:[...] }
GET /api/actes/{id}/download                  (Bearer)   → application/pdf (binary)
GET /api/bilans/{id}/download                 (Bearer)   → application/pdf (binary)
```
Structured company data: `GET /api/companies/{siren}` (and `?siren[]=` batch, `/companies/diff`
changes feed).

| Kind (ours) | INPI document | Endpoint | Cost |
|---|---|---|---|
| Gesellschaftsvertrag | **statuts** (filed within *actes*) | `/api/actes/{id}/download` | free |
| — (amendments/deeds) | **actes** | `/api/actes/{id}/download` | free |
| — (accounts) | **comptes annuels / bilans** | `/api/bilans/{id}/download` | free (non-confidential) |
| **Registerauszug** | **Kbis** — NOT on INPI | Infogreffe (§5) | **paid** |

Note: France's *Gesellschafterliste* answer is unchanged — it's `not_provable_from_registry` for
SAS/SA (private titres register); the statuts prove members only for SARL/SNC. INPI serving the
statuts PDF doesn't change that; it just makes the SARL route free.

## 4. Coverage & limits
- **Historical:** actes/statuts from **1993**; comptes from **1 Jan 2017** (confirmed, primary).
- **Confidential accounts excluded:** comptes a company lawfully declared confidential
  (micro-entreprise L.232-25; petite entreprise compte de résultat) are **not distributed** —
  they appear as listed-but-no-downloadable-file (same as our existing `missing`-doc pattern).
- **Rate limits (secondary — operator report, not spec):** ~10,000 req/day and ~10 GB/day; a wall
  near ~4,168 files/day; **parallel requests get blocked → run single-threaded with backoff.**
- **Bulk:** SFTP delivery of the whole corpus (XML/JSON/CSV/PDF), daily updates —
  `https://data.inpi.fr/content/editorial/Serveur_ftp_entreprises`. Use SFTP for large pulls
  rather than hammering REST.

## 5. Kbis carve-out (the Registerauszug)
INPI does not issue the Kbis. Options:
- **MonIdenum** — free for the company's own legal representative.
- **Infogreffe** third-party extrait K/Kbis — **3,06 € electronic**, 4,00 € post (2,44 € at counter).
- INPI's free *extrait RNE / attestation d'immatriculation* (via API Entreprise) is an *informational*
  proof, **not** a legally-recognised Kbis.

So if a customer needs a genuine Kbis, that's a separate paid Infogreffe integration; budget it.

## 6. Gotchas / open items
- **⚠️ PDF redistribution licence — VERIFY BEFORE SHIPPING.** RNE data is Open Data (Licence Ouverte),
  which cleanly covers the structured JSON. Whether the same terms permit **re-serving the document
  PDFs** (actes/comptes) to our customers is **NOT confirmed** — read
  `https://data.inpi.fr/content/editorial/licences_reutilisation_donnees_inpi` + the CGU and confirm
  explicitly. Do not assume the JSON open-data licence authorises PDF redistribution.
- Handle "listed in metadata but no downloadable file" (confidential / not-yet-digitised) as
  unavailable, not an error.
- **API versioning:** Actes tech doc is **v3.0**; pin to the current versioned PDF per package and
  watch for updates. The v3.0 Actes PDF is image-based — download and read it to lock the exact
  confidential-flag JSON field and pagination before coding.

## Implementation roadmap — mirror the Germany (hr.de) pattern

Germany is the precedent (our first free direct vendor). The free German document route is
**handelsregister.de (hr.de)** — `handelsregister_client.py` in the betterco-skills plugin.
**NorthData is a PAID enrichment source, not the free document route** — do not conflate them.

**What hr.de is:** free since Aug 2022, but **no public API** — the client is a **Playwright
browser scraper** over the portal's JSF/PrimeFaces UI (`HandelsregisterClient.search()` +
`.download(result, doc_type, dest)`), ToS-limited (~60/hr filed ceiling), with occasional
reCAPTCHA and session-scoped stalls it recovers via `rebuild()`. It serves the real documents free:
`shareholders` (Gesellschafterliste), `articles` (Gesellschaftsvertrag/Satzung), `extract` (AD),
`history` (CD), `financial` (Jahresabschluss).

**France mirrors the provider SHAPE but is a cleaner integration.** INPI RNE is a proper REST API
(JWT auth, clean endpoints, ~10k/day, no captcha, no scraping) — strictly better than the hr.de
scraper. The France provider client should expose the same conceptual surface —
`search(siren)` + `download(doc_type)` — so it drops into the same doc-kind router, but implemented
as a thin REST client rather than a browser automation.

| | Germany — hr.de (free, precedent) | France — INPI RNE (free, this spec) |
|---|---|---|
| access | browser scraper (no API) | REST API (JWT) |
| rate | ~60/hr ToS, captcha risk | ~10k/day, no captcha |
| free docs | Gesellschafterliste, Satzung, extract | statuts, actes, comptes |
| paid gap | — (register extract is free) | Kbis extract → paid Infogreffe |
| client | `handelsregister_client.py` (Playwright) | new thin REST client |

**Phase 1 — INPI provider client** (mirrors the hr.de client's `search`/`download` surface, but as
a REST client not a scraper). Methods:
`login() → JWT` · `search(siren)` · `list_documents(siren)` (→ actes[], bilans[]) ·
`download_document(kind, id)` returning PDF bytes. Single-threaded + backoff + re-login on 401.
Effort: small — it's a thin REST client (3 endpoints).

**Phase 2 — vendor routing.** Add to `document_kinds_routing.json` vendor map:
`FR` → split vendor — `inpi.rne` for statuts/actes/comptes (free), `infogreffe` for the Kbis
(paid). This is the first split-vendor jurisdiction; the routing layer already models per-document
vendor selection.

**Phase 3 — doc-kind mapping into BetterCo.** Reuse the existing router:
INPI **statuts** → `kind='satzung'` → `ARTICLES_OF_ASSOCIATION`;
INPI **comptes** → a process 'Sonstige' doc (`OTHERKYCDOCS_*`);
the **Kbis** (Infogreffe) → `kind='hr_auszug'`-equivalent register extract slot.
(FR has no Gesellschafterliste for SAS/SA — see the evidence table; nothing to file there.)

**Phase 4 — Infogreffe (the paid Kbis path).** Separate small client; only needed if a customer
requires a genuine Kbis. See payment below.

**Phase 5 — licence check (OFFLINE, user-owned).** Confirm PDF redistribution rights before shipping.

## How to pay

- **INPI RNE (statuts / actes / comptes): FREE.** No payment rail at all — a free data.inpi.fr
  account, activate the packages, done. Same "free direct vendor" tier as hr.de for Germany — but
  via a real API instead of a scraper.
- **Infogreffe (the certified Kbis, only if needed): PAID, ~3,06 € / electronic doc.** Requires an
  **Infogreffe professional account**; billing is per-document (prepaid balance or monthly invoice —
  confirm the account terms at signup). **MonIdenum** is free but only for the company's *own* legal
  representative, so it doesn't help a third-party KYC provider.
- **Net:** for the three document kinds we actually serve, France costs **€0 marginal**. The only
  paid line is the optional Kbis, at registry cost with no vendor markup — cheaper than KYC.com.

## Confidence
Auth host/path, base URLs, `/companies` endpoints, 1993/2017 coverage, free access, SFTP, and the
Infogreffe/MonIdenum tariffs are **primary-sourced**. The `/attachments`, `/actes/{id}/download`,
`/bilans/{id}/download` paths and the 10k/10GB quota are **secondary-confirmed** (a working
third-party implementation, consistent with INPI's confirmed base host) — validate against the
official Actes/Comptes technical PDFs before committing code.

Key sources: data.inpi.fr Acces_API_Entreprises · inpi.fr/ressources acces-lapi-formalite-rne ·
Actes tech doc v3.0 (inpi.fr) · formalité JSON doc (inpi.fr download-document id=162) ·
service-public F21000 (Kbis tariff) · data.inpi.fr licences_reutilisation.
