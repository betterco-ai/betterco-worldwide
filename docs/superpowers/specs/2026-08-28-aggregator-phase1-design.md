# Aggregator — Phase 1 Design (kyc.com as source 1)

**Date:** 2026-08-28
**Deadline:** 1 October 2026 (phase 1 *and* phase 2)
**Implemented by:** us, in `betterco-backend`, branch per step, CI-verified, backend dev reviews
**Status:** design agreed in conversation; open decisions listed in §10

---

## 1. Why

The BetterCo platform is the reference system. It must call an **aggregator**, which routes to the
right **source** and returns a document into a BetterCo client. Today none of that is true for
document search.

Measured in `betterco-backend` on 2026-08-28:

- `KycCaseLink` — the record a document order creates — holds `workspaceId`, `customerId`,
  `kycCaseCommonId`, `jurisdiction`, `companyName`, `statusName`, `ready`, `idempotencyKey`.
  It has **no `businessRelationId` and no reference to `domain/Case`**. Ordered documents never
  reach a client.
- Every read is a live vendor call: `getCaseStatusById` → `client.getCompany(...)`,
  `listDocumentsById` → `client.getCompanyDocuments(...)`, download → `client.downloadDocument(...)`.
  Nothing is stored, so there is no stock to reuse and no per-case cost record.
- The consumer's handle is the vendor's identifier: `extractCaseCommonId()` reads kyc.com's
  `caseCommonId` and it becomes the path parameter in `/cases/{case_common_id}`. No second source
  can mint that number.

So routing STP to `stg.betterco.ai` instead of kyc.com looks like the strangler step but is the
same coupling under our hostname.

## 2. Scope

**Phase 1 (this spec):** the aggregator exists, kyc.com is its only source, and a document order
produces a BetterCo client with one matter whose documents are stored by us.

**Phase 2 (separate spec):** additional sources behind the same aggregator — DE via the
Handelsregister sidecar first, then FR (INPI / Datainfogreffe), then DK.

**Not in scope:** replacing the kyc.com Java client with the python route; changing search,
jurisdictions, coverage, company-types or legal-forms; the customer-facing UI.

## 3. Architecture

```
        User (BetterCo app)                 User (Septeo/STP staff)
                │                                     │
        betterco-frontend                    partner REST API
                └──────────────┬──────────────────────┘
                               ▼
   ┌────────────────────────────────────────────────────────┐
   │ BETTERCO PLATFORM  (Java, reference system)            │
   │ client (businessRelation) → Case (one matter)          │
   │ documents → doc_management → S3 / Azure                │
   │ vendor ref → Case.externalIdentifiers                  │
   └───────────────────────┬────────────────────────────────┘
                           ▼
   ┌────────────────────────────────────────────────────────┐
   │ AGGREGATOR   com.betterco.app.aggregation              │
   │ route: jurisdiction + document kind → source           │
   │ acquisition record per fetch                           │
   │ per-source policy: charging model · backoff · route    │
   └────────┬──────────────────────────────┬────────────────┘
            ▼ phase 1                       ▼ phase 2
   ┌──────────────────┐        ┌────────────────────────────┐
   │ kyc.com (Java)   │        │ provider sidecar (FastAPI) │
   │ charge: PER_CASE │        │ 127.0.0.1:8090             │
   └──────────────────┘        └────────────────────────────┘
```

The aggregator sits in **Java, inside the backend**. Its job is to write clients, matters and
documents into the BetterCo domain, and that domain is Java. A python aggregator would have to
reach back into the platform, inverting the reference system.

kyc.com keeps its **Java client** in phase 1 — STP is in production on it, the sidecar is loopback
with a shared secret and no stated availability story, and the deadline is five weeks out. The
source interface is defined in HTTP-shaped terms so that swapping kyc.com onto the sidecar later is
a configuration change rather than a redesign.

## 4. Domain model

**The aggregate already exists.** `domain/Case` carries `businessRelationId` (the client),
`workspaceId`, `status`, `caseAML`, `caseOrigin` and `externalIdentifiers`. A BetterCo *client with
one matter* IS the case; kyc.com's case maps onto it 1:1.

| Concept | Where it lives | Notes |
|---|---|---|
| Client | `businessRelationId` on `Case` | created by the order |
| Matter / case | `domain/Case` | one per order |
| Vendor reference | `Case.externalIdentifiers` | kyc.com `caseCommonId` goes here, internal only |
| Document | `doc_management` + `FileStorage` | handle is `bettercoDocumentId` |
| Fetch | **new** `DocumentAcquisition` | one per document per source |
| Cost | **new** charge record | per chargeable unit, see §7 |

`KycCaseLink` mostly dissolves. What survives moves onto the acquisition (source ref, status,
`lastPolledAt`) and onto the Case (`idempotencyKey` handling, which already works — it is persisted
by `buildPendingLink` and enforced by a unique partial index on `(workspaceId, idempotencyKey)`).

**Acquisition lifecycle**, mirroring the Handelsregister sidecar's `PipelineStatus` so both sources
speak one language:

```
REQUESTED → IN_PROGRESS → STORED
                        ↘ MISSING        registry has no such document
                        ↘ MANUAL_QUEUED  needs a human (the DE case)
                        ↘ FAILED
```

Each acquisition holds: case, source, source ref, requested kind, delivered kind + `substituted`,
`bettercoDocumentId`, storage key, `fetchedAt`, `contentDate`, cost.

`fetchedAt` and `contentDate` are deliberately separate: a statement fetched today can carry a 2019
filing date.

## 5. The contract STP sees

Unchanged: `search`, `jurisdictions`, `jurisdictions/coverage`, `company-types`, `legal-forms`.

```
POST /document-search/cases
  → { "caseId": "bc_7f3a91c4", "status": "processing" }
     creates client + Case; vendor ref → externalIdentifiers; idempotencyKey preserved

GET  /document-search/cases/{caseId}
  → status derived from OUR acquisitions, not kyc.com's statusName passthrough
     `ready` is retained so existing polling logic survives

GET  /document-search/cases/{caseId}/documents
  → [ { documentId, kind, availability, source, fetchedAt, contentDate } ]
     ONE id space, retiring today's pending(numeric) / ready(string) split

GET  /document-search/cases/{caseId}/documents/{documentId}/content
  → served from our storage; if not yet stored: fetch, store, serve
```

`kind` is the **vendor-neutral document kind** resolved from our document-kinds curation, not the
vendor's label. The vendor's own `category` / `name` are preserved on the acquisition for
traceability but are not the contract. `availability` is one of `available` | `pending` | `missing`,
derived from the acquisition status (`STORED` → available; `REQUESTED`/`IN_PROGRESS` → pending;
`MISSING` → missing).

`status` on the case is derived as: `processing` while any requested kind is still
`REQUESTED`/`IN_PROGRESS`; `ready` once every requested kind has reached a terminal state
(`STORED`, `MISSING` or `FAILED`). `ready` therefore means "nothing more is coming", which is what
it means today — not "everything was found".

Three deliberate choices:

1. **`includePending` is accepted and ignored** for one release. With per-document ingestion
   "pending" is just an `availability` value, but STP should not have to change its calls twice.
2. **Status becomes ours.** Today `statusName` is kyc.com's string passed through — the source of
   the "always Initializing Case" bug reported in July. Derived from acquisitions it means the same
   thing for every future source.
3. **Content falls back.** A document not yet stored is fetched, stored and served in one pass,
   covering gaps between polls without a second code path for the caller.

### Migration for STP

The case id changes from `Long` (kyc.com's) to an opaque `String` (ours). Agreed to break **now**,
while Björn Hartenstein is still integrating, rather than after his polling loop ships — the whole
point of step 1 is that STP migrates once. Document ids likewise become `bettercoDocumentId`, which
also removes the pending/ready id split they would otherwise have to special-case.

## 6. Ingestion

Documents arrive **progressively**, long before the case is ready — that is what `includePending`
exposed and what we sold STP in July. Ingestion is therefore driven **per document, never by
case-ready**.

**Backoff is a per-source policy object**, not one global scheduler: a schedule, a give-up point,
and a terminal action. kyc.com builds over hours → 1h, 6h, 12h, 24h, then flag. A synchronous
source such as INPI declares no polling at all. The scheduler only executes what the source
declares. This replaces today's flat `@Scheduled(fixedDelayString = "${kyc-com.status-poll-interval:PT5M}")`.

Each pass lists the case's documents, and for every one newly `available` and not yet stored:
fetch bytes → store via `FileStorage` → attach to the Case → write the acquisition record.
`missing` rows carry no document id and nothing to fetch; they stay as recorded gaps and are never
charged.

## 7. Cost and billing

A single BetterCo case may draw documents from **several sources at once**, so cost cannot live on
the case. It lives in charge records, one per *chargeable unit*, and what a unit is depends on the
source's charging model:

| Charging model | Unit | Effect |
|---|---|---|
| `PER_CASE` (kyc.com) | one per (case, source) | first acquisition charges; further documents free |
| `PER_DOCUMENT` (sidecar sources) | one per acquisition | each document charges |
| future models | — | new strategy, no schema change |

A case total is the sum of its charge records. This mirrors the existing
`BillingComputationStrategy` / `BillingComputationStrategyType` pattern
(`CreatedClientsStrategy`, `CreatedFlowsStrategy`, `SyncedClientsStrategy`) rather than inventing a
second mechanism.

**Vendor cost and customer billing are different meters.** This spec instruments the first. For the
second, document orders get their own `CaseOrigin` value so that `CreatedClientsStrategy` can
distinguish them from ordinary client creations. That converts a blocking commercial decision into a
reversible one: the data is tagged from day one, the billing rule can be decided later without a
migration.

## 8. Error handling

- Vendor unavailable → acquisition stays `IN_PROGRESS`, retried on the source's schedule; after the
  give-up point → `FAILED` with the reason recorded, case status reflects it.
- Document listed but not fetchable → `MISSING`, never charged, surfaced as a gap.
- Duplicate order with the same `idempotencyKey` → the existing case is returned (already
  implemented and enforced by a unique index).
- Validation errors keep the codes now on branch `fix/kyc-create-validation-errors`:
  `invalid_legal_type` and `unknown_jurisdiction` alongside the existing
  `legal_type_or_company_type_required`, `invalid_company_type`, `not_confirmed`.

## 9. Testing

Nothing compiles on the development machine — no Maven, no `~/.m2`, `.mvn/` is untracked — so
**CI is the only verification** (`.github/workflows/app-tests.yml`, `mvn -B test`). Every step ships
as a branch with tests that fail before the change and pass after it.

- Unit: routing table resolution; charging model per source; backoff schedule advance; acquisition
  state machine including `MISSING` and `MANUAL_QUEUED`.
- Integration: order → client + Case created with the vendor ref in `externalIdentifiers`;
  progressive ingestion stores documents as they appear; content served from storage without a
  vendor call; content fallback path fetches once and stores.
- Contract: the new case/document id shapes, and `includePending` accepted-and-ignored.

## 10. Open decisions

1. **Retention** — how long stored documents are kept, and what happens on customer deletion.
   Forced by storing bytes; not answered here.
2. **Evidence level** — whether `data` / `document` / `certified` rides along in this contract break
   or arrives later as an optional field. Adding it later is additive, so deferring is defensible.
3. **Customer billing rule** for document-order clients (§7) — tagged now, decided later.
4. **DE sidecar drift** (phase 2 input) — the Java `HandelsregisterSidecarClient` calls
   `/companies/search`, `/companies/documents/available`, `/documents/retrieve`,
   `/documents/convert`, `/documents/upload`, `/documents/acquisitions/{id}`, while
   `hr_scraper/app.py` implements only `/search`, `/documents/available`, `/documents/fetch`.
   Establish which build is current before phase 2.
5. **DK has no service** — `dk_cvr_client.py` is a library with no route. Phase-2 scope nobody has
   costed.

## 11. Risks

| Risk | Mitigation |
|---|---|
| Five weeks for phase 1 **and** phase 2 | Phase 1 contract lands in week 1 so the customer-visible half is safe even if phase 2 slips |
| No local build | Every step is a branch; CI runs the tests; no "works on my machine" claims |
| We push into a repo the backend dev releases from | Branch per step, PR review by them, no direct pushes to `dev` |
| kyc.com case-centric vs sidecar document-centric | Resolved by the model in §4: case is ours, acquisitions are per document |
| Storing documents raises retention/GDPR | Named as open decision 1, to be settled before go-live |
