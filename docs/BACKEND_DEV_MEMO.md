# Backend memo — two new APIs to add to the document-search gateway

From the KYC-worldwide work. The app currently works around two gaps with app-side
code; both should move into the **BetterCo document-search backend** so every client
benefits and the app can drop its workarounds. Reference implementations exist and are
proven against the staging tenant (`stg-stp-kyccom`).

Related hand-off (already delivered, not an API): `curation/legal_forms_curation_ALL.json`
— 330 legal-form rows for the 82 unmapped manual jurisdictions, to be ingested into the
same `legal-forms` store that holds the existing 14. See `curation/README.md`.

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
