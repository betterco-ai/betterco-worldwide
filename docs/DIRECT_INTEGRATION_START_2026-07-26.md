# Direct registry integrations — start plan, 2026-07-26

*Internal. Which of the 15 STP priority jurisdictions we can integrate directly (bypassing the aggregation
vendor), ranked by effort, plus step-by-step instructions for the first three.*
*Sources: `curation/registry_intelligence.json` (69 jurisdictions), `curation/all_countries_view.json`,
`curation/stp15_document_name_map.json`, `docs/FR_INPI_INTEGRATION.md`.*

---

## 1. Ranking — the 15 STP jurisdictions by direct-integration readiness

| Tier | Jurisdictions | API | Documents via API | Cost | Commercial reuse licensed | Verdict |
|---|---|---|---|---|---|---|
| **A — build now** | **FR, GB, DK** | open, self-service | **yes** | free | **yes** | Full direct replacement incl. documents |
| **B — buildable, paid/contract** | IT, ES | IT yes / ES partial | yes | per document | not clarified | Only worth it at volume; onboarding is the blocker |
| **C — data only** | NL, LU, CH, IL, BE, SG | yes/partial | **no** | mixed | mostly no | Direct for *data* (incl. shareholders), vendor stays for documents |
| **D — vendor only** | US, JP, HK, KW | none | no | – | – | No direct path; KW has no registry intelligence record at all |

**Outside the STP 15**, three further jurisdictions are Tier A on identical criteria: **EE, PL, SK** (open API,
documents, free — licence not yet clarified). Cheap additions once the Tier-A pattern exists, but not priority.

**Why Tier A is the whole business case.** In FR, GB and DK the documents that the vendor either does not
deliver at all or bills as *additional* are free at the registry:

| | Registry extract | Constitutional doc | Shareholder list |
|---|---|---|---|
| **FR** | vendor base — *Kbis stays paid at Infogreffe, NOT on INPI* | vendor: none → **INPI: free (statuts)** | data only |
| **GB** | vendor: no equivalent | vendor: additional → **Companies House: free (filing image)** | not evidenceable (CS01 = delta) |
| **DK** | vendor base | vendor: additional → **CVR: verify** | data only |

So the three Tier-A integrations remove exactly the cost line we currently cannot even price with the vendor.

---

## 2. Sequence and why

1. **GB first** — instant free API key, HTTP Basic, no contract, no email round-trip. Fastest path to a
   working end-to-end direct document fetch, and it establishes the pattern the others follow.
2. **DK second, but start the paperwork today** — the system-to-system credentials must be requested by
   email (`cvrselvbetjening@erst.dk`) and involve signing a terms declaration. Unknown lead time, so send it
   before writing any code; it must not sit on the critical path.
3. **FR third** — furthest along conceptually (`inpi_client.py` + `docs/FR_INPI_INTEGRATION.md` exist), but
   it is the only split-vendor case (INPI free for statuts/actes/comptes, Infogreffe paid for the Kbis) and
   its licence carries real restrictions. Do it once the routing layer has proven itself on GB and DK.

---

## 3. Prerequisites — do these first, in this order

| Step | Action | Lead time |
|---|---|---|
| P1 | **DK:** email `cvrselvbetjening@erst.dk`, request system-to-system access to the CVR distribution API, sign the terms declaration | unknown — **do today** |
| P2 | **GB:** register an application at `developer.company-information.service.gov.uk`, create a Public Data API key (same key works for the Document API) | minutes |
| P3 | **FR:** register at `data.inpi.fr` ("Espace Open Data"), self-activate the packages *Base RNE*, *Comptes annuels*, *Actes* | minutes, no habilitation gate |
| P4 | Add the three credential sets to `.env` following the existing pattern; never commit them | – |
| P5 | **Legal sign-off on redistribution** — see §6. Blocks *shipping*, not building | before go-live |

Suggested `.env` keys, consistent with the existing `BETTERCO_*` convention:

```
GB_COMPANIES_HOUSE_API_KEY=
DK_CVR_S2S_USER=
DK_CVR_S2S_PASSWORD=
INPI_USERNAME=
INPI_PASSWORD=
```

The INPI names are **not** prefixed `FR_` — `inpi_client.py` already reads `INPI_USERNAME` /
`INPI_PASSWORD`, and the doc follows the code.

---

## 4. Per-jurisdiction build instructions

### GB — Companies House

- **Host:** `https://api.company-information.service.gov.uk` (data), `https://document-api.company-information.service.gov.uk` (documents)
- **Auth:** HTTP Basic, API key as username, **empty password**
- **Docs:** `https://developer.company-information.service.gov.uk`
- **Rate limit:** ~600 requests / 5 minutes → the client needs backoff from day one, not later
- **Flow:**
  1. `GET /search/companies?q=<name>` or `GET /company/{number}` → structured data
  2. `GET /company/{number}/filing-history` → find the filing, read its `links.document_metadata`
  3. `GET /document/{id}/content` with `Accept: application/pdf` → the PDF bytes
- **Maps to our kinds:** articles → the `MEMORANDUM_ARTICLES` / incorporation filings; `CS01` → shareholder
  data only, **do not** classify it as a shareholder list; accounts → `AA`
- **Watch out:** filing history is a *chronology*, not a current-state view. Picking "the articles" means
  picking the *latest* amending filing, not the first match. This is the main correctness trap in GB.

### DK — CVR / Erhvervsstyrelsen

- **API:** CVR system-to-system distribution API (Elasticsearch/REST) + Virk data hub
- **Docs:** `https://data.virk.dk/datakatalog/erhvervsstyrelsen/system-til-system-adgang-til-cvr-data`
- **Auth:** credentials from P1; the web portal and annual-report downloads need no account
- **Flow:** query the Elasticsearch endpoint by CVR number or name → entity record incl. owners, board,
  P-units, NACE/DB07 and history → annual reports (`regnskaber`) linked per record as PDF/XBRL
- **Maps to our kinds:** registry extract → the entity record; annual reports → free; **articles
  (`vedtægter`) → UNVERIFIED.** Whether they are retrievable through this API or only via Virk is an open
  question — resolve it in the spike before promising DK articles to anyone.
- **Bonus:** DK returns real ownership data, so the shareholder gap is covered as data without the vendor.

### FR — INPI RNE

Full spec already written: **`docs/FR_INPI_INTEGRATION.md`**, client stub: **`inpi_client.py`**. Do not
re-derive it. Two things to carry forward:

- **Right host:** `registre-national-entreprises.inpi.fr` (RNE Open Data, serves PDFs) — *not*
  `entreprise.api.gouv.fr` (API Entreprise, habilitation-gated, no filing documents)
- **Auth:** `POST /api/sso/login` → session JWT → `Authorization: Bearer`; **re-login on 401**, lifetime
  undocumented. Integration host: `registre-national-entreprises-pprod.inpi.fr`
- **Flow:** `GET /api/companies/{siren}/attachments` → `{actes, bilans}` → `GET /api/actes/{id}/download`
- **Carve-out:** the **Kbis** is not on INPI. FR is our first split-vendor jurisdiction — `inpi.rne` free for
  statuts/actes/comptes, `infogreffe` paid for the certified extract.

---

## 5. Architecture — keep it vendor-neutral

Do not let registry specifics leak upward. Per
[[vendor-neutral-aggregator-architecture]] the contract stays: *jurisdiction + document kind in, document
out*, with the source hidden.

- Each registry gets its own client module, mirroring `inpi_client.py` (same shape as the existing Northdata /
  handelsregister / Transparenzregister / company.info / KYC.com clients).
- A **routing layer** decides per (jurisdiction × document kind) whether the request goes direct or to the
  vendor. FR proves the router must resolve at *document-kind* granularity, not per jurisdiction — one
  jurisdiction can be split across two sources.
- Every returned document carries its provenance internally (source, retrieval date, cost) — needed for the
  attribution obligations in §6 and for the cost reporting the whole least-cost thesis rests on.
- **Fallback, not replacement:** if the direct call fails, the router falls back to the vendor. Direct
  integration lowers cost; it must not lower availability.

---

## 6. Licence obligations — these are conditions, not footnotes

| | Instrument | Obligation | Restriction |
|---|---|---|---|
| **GB** | Statutory disclosure, Companies Act 2006 — no reuse licence imposed | none | Registrar's database right not infringed by extraction (CDPA s.47). We remain responsible for our own data-protection compliance |
| **DK** | **CC BY 4.0** | **Must credit "Det Centrale Virksomhedsregister (CVR)"** | S2S/bulk feed requires registration + signed terms declaration |
| **FR** | Licence de réutilisation des informations du RNE (INPI), homologuée | **Attribution: name the source *and* the last-update date** of the reused information; must not mislead as to content/source/date | The free public feed is **legally reduced for natural persons** (surname, usual name, pseudonym, first names, month+year of birth, municipality only). Full personal detail only to authorities/regulated professions |

Two consequences to design in now rather than retrofit:

1. **Attribution must be a data field, not a template string.** DK needs a credit line, FR needs a credit
   line *plus the last-update date of that specific record*. If provenance is not captured at fetch time, FR
   attribution cannot be produced afterwards.
2. **FR's reduced personal data is a product limitation, not a bug.** Where a natural-person shareholder is
   involved, the free feed will not give full detail. Anyone promising FR beneficial-owner depth from the
   free channel is promising something the licence does not permit.

**PDF redistribution** — whether we may pass registry PDFs on to our customers, as opposed to merely
retrieving them — is flagged as unconfirmed in the FR spec and is equally unconfirmed for DK. It needs legal
sign-off before go-live. It does not block building.

---

## 7. Definition of done for the first integration (GB)

1. API key in `.env`, client module in place, backoff implemented
2. For one real company: data fetched, filing history read, **one PDF downloaded and stored**
3. The document classified into our internal kinds via the mapping — not via a raw registry code
4. Routing layer resolves `GB × constitutional document → direct`, everything else GB → vendor
5. Provenance (source, retrieval date, cost = 0) recorded on the stored document
6. Vendor fallback demonstrably triggers when the direct call fails
7. Measured cost delta versus the vendor path written down — that number is what justifies DK and FR

---

## 8. Open questions to resolve while building

- **DK:** are `vedtægter` (articles) retrievable via the API, or Virk-only? Decides whether DK closes the
  constitutional-document gap.
- **GB:** which filing is authoritative for "current articles" given amending filings?
- **FR:** exact INPI JWT lifetime (undocumented → re-login on 401 is a workaround, not a design).
- **All three:** PDF redistribution rights (§6).
- **IT/ES (Tier B):** worth costing only once Tier A ships. IT needs SPID/CIE/CNS + prepaid Telemaco credit;
  ES's CORPME API channel is offered only to very-high-volume integrators, which we are not yet.
- **KW:** no registry intelligence record exists. Either research it or accept vendor-only permanently.
