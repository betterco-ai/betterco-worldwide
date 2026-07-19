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

## Confidence
Auth host/path, base URLs, `/companies` endpoints, 1993/2017 coverage, free access, SFTP, and the
Infogreffe/MonIdenum tariffs are **primary-sourced**. The `/attachments`, `/actes/{id}/download`,
`/bilans/{id}/download` paths and the 10k/10GB quota are **secondary-confirmed** (a working
third-party implementation, consistent with INPI's confirmed base host) — validate against the
official Actes/Comptes technical PDFs before committing code.

Key sources: data.inpi.fr Acces_API_Entreprises · inpi.fr/ressources acces-lapi-formalite-rne ·
Actes tech doc v3.0 (inpi.fr) · formalité JSON doc (inpi.fr download-document id=162) ·
service-public F21000 (Kbis tariff) · data.inpi.fr licences_reutilisation.
