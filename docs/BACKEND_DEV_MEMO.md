# Backend memo — new APIs to add to the document-search gateway

From the KYC-worldwide work. The app currently works around two gaps with app-side
code; both should move into the **BetterCo document-search backend** so every client
benefits and the app can drop its workarounds. Reference implementations exist and are
proven against the staging tenant (`stg-stp-kyccom`).

Related hand-off (already delivered, not an API): `curation/legal_forms_curation_ALL.json`
— 330 legal-form rows for the 82 unmapped manual jurisdictions, to be ingested into the
same `legal-forms` store that holds the existing 14. See `curation/README.md`.

---

## 🔧 Action for backend — 2026-07-29: expose the Hong Kong per-filing document order

**Why this is new:** we modelled KYC.com as purely *case-level* — order a case, take what the
bundle contains, no per-document SKU. **Hong Kong is the exception.** The HKCR sells filings
individually and KYC.com exposes that: a case's filings can be **listed** and then **bought one by
one**. This is the first upstream route that matches our aggregation layer's document-level request
**1:1**, so it should not stay hidden behind "order the whole case".

Upstream contract (verified against the prod v2 swagger 2026-07-29 — *"Works only for HKCR cases"*;
other jurisdictions answer **400**):

| | Upstream | Cost |
|---|---|---|
| List filings | `GET /v2/DocumentPurchase/{caseCommonId}?refreshList=false` | free |
| Buy one filing | `POST /v2/DocumentPurchase` `{caseCommonId, registryDocumentId}` → `{message}` | **billable, per filing** |

Response `{caseDetail:{company:{caseCompanyId, lastRefreshedDate, registryDocuments:{documents:[…]}}}}`,
each filing `{caseDocumentId?, registrydocumentId, name, filingDate, status, category, updateDatetime}`.

**Proposed gateway routes** (vendor-neutral naming — the client must not learn the word
*DocumentPurchase*):

```
GET  /document-search/cases/{caseCommonId}/orderable-documents[?refresh=true]
     -> [{documentId, name, category, filingDate, status, alreadyOnCase: bool}]
POST /document-search/cases/{caseCommonId}/orderable-documents/{documentId}/order
     {confirm: true}   -> {message}   # billable, gated like case creation
```

**Four things the gateway must get right:**

1. ⚠️ **Casing trap.** The upstream **GET response** field is `registrydocumentId` (**lowercase d**);
   the **POST body** field is `registryDocumentId` (**capital D**). Both spellings are correct in
   their own place — reading the id with the POST spelling silently yields `null`.
2. **`caseDocumentId` set ⇒ the filing is already on the case** (bought earlier, or delivered with
   the bundle) → serve it from the existing document-download route; **never buy it again**. HK CR
   lists *Memorandum & Articles of Association* and *Annual Return (FNAR1)* as **mandatory**, so the
   bundle usually already carries them — the purchase route is for what it does *not* carry (older
   NAR1s, altered articles, special resolutions). Surface this as `alreadyOnCase`.
3. **Billing gate + explicit confirm.** Treat the order like case creation: paid gate *and* an
   explicit `confirm` — an accidental retry buys a second copy.
4. **Delivery is asynchronous.** After a 200, the filing appears on the case later — poll the list
   (or use the `DocumentUploaded` webhook) until it carries a `caseDocumentId`.

**Reference implementation (working, contract-tested):** `kyc_com_client.py` in `betterco_claude_api`
— `list_document_filings()`, `find_document_filings()`, `purchase_document(confirm=…)`, plus our own
API routes `GET /kyccom/cases/{id}/filings` and
`POST /kyccom/cases/{id}/filings/{registryDocumentId}/purchase?confirm=true`.

**Routing data already updated:** `curation/document_kinds_routing.json` — the HK
Gesellschafterliste/Gesellschaftsvertrag rows now carry `order.howToObtain = "document_purchase"`
plus an `order.channel` block with the exact list/buy calls, instead of the old (for HK wrong)
"no per-document SKU exists" note.

⚠️ **Not yet exercised against a live HK case — nothing was purchased.** The v2 sandbox *stubs* this
route (200 for any case, `documents: null`), so the filing list can only be seen on prod, against a
real HKCR case. Do that before building UI on the payload shape.

---

## 🔧 Action for backend — 2026-07-11: forward the extra manual-create fields

The app's **create** call (`POST /document-search/cases`) now sends **more optional fields** for
**manual (no-registry-search) jurisdictions**. Manual cases can't anchor on an `externalCode` from a
search hit, so the **address block + province + a user-typed registry number** are what let the
upstream locate the right entity — and `unregisteredEntity` flags an entity with no register entry
at all. These map 1:1 to KYC.com's `CreateCompanyModel`.

**Please make the gateway pass these through** to KYC.com create (some may currently be dropped):

| Field (app → gateway) | KYC.com `CreateCompanyModel` | Notes |
|---|---|---|
| `addressLine1` | `addressLine1` | already forwarded |
| `addressLine2` | `addressLine2` | **new — please forward** |
| `postcode` | `postcode` | already forwarded |
| `city` | `city` | already forwarded |
| `province` | `province` | **new — please forward** (state/province/region) |
| `externalCode` | `externalCode` | now also user-enterable in manual mode (registry no.) |
| `unregisteredEntity` | `unregisteredEntity` | **new — boolean** |

App side is done (`kyc_case_app.py` `/api/create-case` whitelist + `kyc_case.html` manual form). No
new required fields — all optional; behaviour is unchanged when they're empty. Just don't silently
drop them at the gateway.

---

## Update — 2026-07-10 (since first handover)

Read this first — a few things changed after the initial memo:

1. **The "broken search" flag was mostly OUR bug — corrected.** What looked like "5 broken markets"
   is really **1 (MY)**. The registry replies to broad queries with a 400 *"More than 200 records
   found, please refine your search criteria"*, and the app was masking it as a 500. Corrected:
   - **AU / FI / FR** — NOT broken; "too many results" (refine the query). Registry works.
   - **KY** — works, just **slow (~62 s)**; earlier 500s were client timeouts. Also returns an
     **empty `externalCode`** (data gap worth raising with KYC.com).
   - **MY** — the only genuine 500 to escalate (see the FLAG section below, already updated).

2. **App-side fixes the gateway should mirror:**
   - **Surface upstream messages** — the "refine" / error text arrives as a 4xx body; pass it
     through, don't wrap it as a 500.
   - **Longer / async search timeout** — we raised search 60 s → 90 s so slow-but-valid registries
     (KY) succeed, and fail fast with a clean message beyond that.

3. **New capability: generic search enrichment + 8 ID decoders** (IN CIN, RU OGRN, CN USCC, DE court
   city, AR CUIT, HU, GB, SG). Every search result now carries a uniform `enrichment` object
   (location / type / year). Relevant to **API 1** — the gateway could return the same shape or
   adopt the decoder pattern. Explainer: `docs/india-cin-location-check.md`.

4. **New reference:** `docs/search-catalog.json` + `docs/search-response-catalog.md` +
   `scripts/search_response_sweep.py` — what the KYC.com search returns per automated jurisdiction
   (standard fields, each jurisdiction's ID scheme, reliability verdicts).

The 3 core asks are unchanged: **legal-forms ingest**, **API 1 (coverage)**, **API 2 (pre-Ready docs)**.

---

## API 1 — Per-jurisdiction coverage

**Why:** the app needs, per jurisdiction, KYC.com's coverage: the retrieval **SLA**, the
**registries / access mode**, the **data fields** returned, and the **documents** split
into *base* (mandatory, provided as standard) and *additional* (non-mandatory, on request,
extra charge). Today the app parses this out of a **static Excel snapshot**
(`jurisdiction_matrix.json`, built by `build_jurisdiction_matrix.py`) and serves it at
`GET /api/jurisdiction`. That snapshot goes stale and the app shouldn't own reference data.

**Proposed gateway endpoint** (mirror the existing reference endpoints under
`/restapi/v1/workspaces/{ws}/document-search`):

```
GET /document-search/jurisdictions/{codeISO}/coverage
```

**Response shape** (what the app already produces — match it so the frontend is unchanged):
```json
{
  "code": "GB",
  "name": "United Kingdom",
  "sla": "25 minutes",
  "registries": ["Automated"],                     // access mode / source registries
  "dataFields": {
    "companyIdentity": ["Entity Name", "Entity Type", "..."],
    "controllingEntitiesAndIndividuals": ["Name", "Role", "..."],
    "shareholdersPartnersAndUBOs": ["Name", "Share count", "..."]
  },
  "baseDocuments":       [ { "type": "NEW_INCORPORATION", "description": "New Incorporation" }, ... ],
  "additionalDocuments": [ { "type": "MEMORANDUM_AND_ARTICLES_OF_ASSOCIATION",
                             "description": "Memorandum and Articles of Association" }, ... ]
}
```
- `type` is a canonical machine key (UPPER_SNAKE of the label); `description` is the human label.
- **base vs additional** maps KYC.com's Mandatory vs Non-Mandatory document split — keep it,
  it drives cost expectations (additional docs are billable on request).
- Source of truth = KYC.com's coverage matrix (the app snapshot is a stopgap).
- Note: 3 app-supported jurisdictions (**AF, BD, GH**) are absent from KYC.com's matrix →
  no coverage row exists for them (return 404 / empty, not an error).

**App reference:** `jurisdiction_detail()` in `kyc_case_app.py` + `jurisdiction_matrix.json`.

---

## API 2 — Pre-Ready document access (KYC.com "User API" path)

**Why:** the app's "Dokumente abrufen" can only show documents once a case is **Ready**,
because the gateway's upstream is the KYC.com **OAuth v2 REST API**, which withholds
documents until full Ready. Proven in a two-API race on the staging tenant:

| | USER API (session) | REST API (OAuth v2, what the gateway uses today) |
|---|---|---|
| Energizer (GB) | **11 docs in ~49 s** during processing | **0** (case stalled pre-Ready) |
| HSBC | 9 docs within seconds | 0 |

The KYC.com **tenant web-app "User API"** exposes filings **as the crawl progresses**,
hours before REST. Adding it as a second upstream path lets the app surface documents
pre-Ready.

**Upstream endpoints** (host `betterco.knowyourcustomer.com`, **ASP.NET Identity session
cookie** — email+password login, NOT the OAuth PublicApi token, which 403s here):
```
POST /Account/Login/            # form login -> .AspNetCore.Identity.Application cookie
GET  /bff-api/CaseDocuments/all/{caseCommonId}     # list (authoritative, per case)
GET  /bff-api/CaseDocuments/{caseDocumentId}       # download PDF bytes
```
List item fields: `caseDocumentId`, `status` ("Received"/"Missing"), `description`,
`fileName`, `caseStepId`, `estimatedDownloadDate`, `isDocumentPdf`.

**Availability logic:** `caseDocumentId > 0` → **available (download now)** ·
`caseDocumentId == 0` + `estimatedDownloadDate` set → **pending (keep polling)** ·
else → **missing / not retrieved**.

**Proposed gateway change:** add a session-cookie upstream client and expose e.g.
`GET /document-search/cases/{caseCommonId}/documents?includePending=true`, returning the
same document list plus `available|pending|missing` status, and a matching download route.

**Caveats:** the gateway must hold KYC.com tenant user creds (email+password) per tenant;
**2FA is not supported** by the scripted login; the session cookie is short-lived (re-login
as needed).

**Reference implementation (working, tested):** `kyc_com_client.py` in the
`betterco_claude_api` repo (branch `stage-test`) — methods `bff_login`,
`bff_list_case_documents`, `bff_case_document_status`, `bff_download_document`,
`download_case_documents` (poll + download-all-as-available).

---

## 🚩 FLAG — automated search broken / slow in some jurisdictions (escalate to KYC.com)

From sweeping every automated jurisdiction and re-testing failures with **flagship companies**
(details + data: `docs/search-response-catalog.md`, `docs/search-catalog.json`):

**⚠️ Correction:** most of what first looked "broken" was **our own error-masking**. The registry
replies to broad queries with an HTTP 400 *"More than 200 records found in <country>, please refine
your search criteria"*, and the app was re-wrapping it as a 500. **Fixed in the app** (`/api/search`
now returns `{error, refine:true}` and the UI shows an amber "refine" hint). Corrected picture:

- **✅ NOT broken — "too many results":** **AU** (BHP), **FI** (Nokia), **FR** (Renault) — flagship
  names match hundreds of subsidiaries → refine the query. Registry is fine.
- **🐢 KY — works, just slow:** "Tencent" → 17 results in ~62 s (earlier "500s" were client timeouts).
  Fix is client-side: **longer / async search timeout** (the gateway search should allow ≥90 s or go
  async). Also KY results come back with an **empty `externalCode`** — a data-quality gap worth raising.
- **🟡 CY, GR, NO** — 500 on broad terms only; work with a real name (helped by the catch above).
- **🔴 MY — the one genuine issue to escalate to KYC.com:** Maybank/Petronas/Genting/AirAsia all →
  **HTTP 500 after ~62 s**, consistently (not a "too many" 400).

Net: **43/44 automated jurisdictions effectively work** (AU/FI/FR = refine, KY = slow-but-works, IM =
works). Only **MY** is a genuine search outage to raise with KYC.com; the secondary asks are a longer
search timeout (KY) and KY's empty `externalCode`.
