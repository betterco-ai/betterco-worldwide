# P2 — Acquisitions and Ingestion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Documents land in the client *before* the vendor case is ready. Every fetch leaves a record of what was asked for, what was delivered, from which source, when, and at what cost — and the bytes are served from our storage, not the vendor's.

**Architecture:** `com.betterco.app.aggregation` (created in P1) gains a `DocumentAcquisition` entity and a per-document ingestion worker. The worker lists a case's documents on every pass and ingests each one that is newly available and not yet stored; it never waits for case-ready. Storage and attachment reuse `DocumentManagementService.uploadDocument(UploadData, actorId, workspaceId)` — the same call every other auto-loaded document in the platform goes through — so an ordered registry extract is indistinguishable from an uploaded one. Polling cadence moves out of a hard-coded `@Scheduled` interval into a per-source policy object, which is what makes a synchronous source (P6's INPI) expressible at all.

**Tech Stack:** Java 17, Spring Boot 2.7.5, MongoDB (Spring Data + Mongock), JUnit 5 + Mockito, Maven (`./mvnw`).

**Spec:** `docs/superpowers/specs/2026-08-28-aggregator-phase1-design.md` §4, §6, §7 and `docs/superpowers/specs/2026-08-29-aggregator-phase2-and-plan.md`

## Global Constraints

- Repository: `betterco-backend`. Branch off `dev`, one branch per task, PR reviewed by the backend dev. **Never push to `dev` directly.**
- **Verify locally; CI is not a gate you can rely on.** (Corrected 2026-09-05 — the earlier claim that nothing compiles locally is wrong.) A Maven 3.9.9 plus a populated repo live in the session scratchpad and Java 17 is installed, so `mvn -o -Dmaven.repo.local=<repo> -Djacoco.skip=true test` runs the real suite. Judge a branch by **no new failures** against a freshly measured `origin/dev` baseline, never by a green suite. `app-tests.yml` only runs after an **approved** `pull_request_review`, so pushing a branch verifies nothing. Note the baseline moves with the machine: with no Docker daemon it is 795/7 failures/13 errors; with one, the Testcontainers classes pass and it is 806/7/0.
- **Everything in P2 ships behind a config flag defaulting to off**: `aggregation.ingestion.enabled=false` in `src/main/resources/application.properties`. With the flag off the scheduler does nothing and the content endpoint falls through to today's `KycGatewayService.downloadDocumentById(...)` path unchanged. This mirrors `kyc-com.create-enabled`, which is `false` in `application.properties` and `true` in `application-staging.properties` / `application-production.properties`.
- **Two document id spaces, and they are not interchangeable.** `KycGatewayService.listDocumentsById(workspaceId, caseCommonId, includePending)` branches: `includePending=true` uses `KycComUserClient.listCaseDocuments(long)` and yields `caseDocumentId` (numeric, downloaded by `KycComUserClient.downloadDocument(long)`); `includePending=false` uses `KycComClient.getCompanyDocuments(long)` and yields an id parsed out of the document's `link` field (downloaded by `KycComClient.downloadDocument(String)`). **An acquisition must record which space its `sourceRef` came from and always download through the matching pair.** Crossing them silently returns the wrong document or a 404.
- **An acquisition records the source *and* the vendor world** (`vendorTarget`), decided 2026-09-06
  and already implemented for `KycCaseLink` in PR #2296. A case id minted in the KYC.com sandbox does
  not exist in production, so `{source, sourceRef}` is **not** unique across worlds — the unique
  index must be `{source, vendorTarget, sourceRef}` or a sandbox document and a production document
  sharing a reference will be silently treated as the same acquisition. This is separate from
  `SourceRefSpace`, which says which *document id space* a reference came from; both are needed.

- **N1 seam reads, 7 September — three things the plan and the API notes got wrong.** The real
  signature wins:
  1. **`KYCDocumentType` has exactly SEVEN values**, not the nine the API notes list:
     `CURRENT_COMPANY_REGISTER_EXCERPT`, `CHRONOLOGICAL_COMPANY_REGISTER_EXCERPT`,
     `STRUCTURED_XML_REGISTRY_CONTENT`, `SHAREHOLDER_LIST`, `TRANSPARENCY_REGISTER`,
     `ARTICLES_OF_ASSOCIATION`, `SUPERVISORY_BOARD_LIST`. There is **no
     `AML_GENERAL_CHECK_DOCUMENT`** and no `STRUCTURE_CHART_INTERACTIVE`.
  2. **`DocumentScope` has exactly ONE value: `PROCESS`.** The customer-slot-versus-process-document
     distinction is therefore *not* expressed through scope. It is expressed by which ids the
     document carries - `companyId` and `processId` on `Document`. Any design that routes on
     `DocumentScope` is routing on a field that cannot vary.
  3. **`UploadData`'s validation is inverted and does not guard anything.** Its compact constructor
     reads
     `documentType != null && !isValidEnum(KYCDocumentType) && isValidEnum(IdDocType) && !isValidEnum(FinancialReportType)`
     - the `IdDocType` check is missing its `!`. So an arbitrary string such as
     `custom_1784016204186` passes silently (it is not a valid `IdDocType`, so the condition is
     false), while a legitimate ID-document type like `PASSPORT` throws. **This is how the
     `custom_<epoch>` types in F4 reached live data.** The ingestor must validate `documentType`
     against `KYCDocumentType` itself and must not rely on `UploadData` to do it.

- **Store every delivered file; the German roles are a separate overlay** (decided 2026-09-06).
  A document is never dropped, deferred or left unstored because it plays none of the three roles -
  most do not. The success condition of ingestion is a count: **delivered == stored**, with any
  exception recorded explicitly (missing at the source, or blocked by the malware scan), never
  silently absent. Roles are computed afterwards from the curation and attached as a set that is
  usually empty. See `docs/DOCUMENT_TYPE_LAYER_2026-09-06.md`.

- **`documentType` must land on a BUILT-IN enum value, or the reviewer cannot see the document.**
  Measured on the platform (betterco-api skill, 2026-08-04): REST **accepts any custom type string**
  and reads it back exactly, and the OpenAPI description even advertises custom types - but the
  customer document area **renders only the built-in enum**. A custom-typed document therefore
  exists in the API and is unfindable in the UI, which is worse than not filing it: it looks filed.
  The built-in customer types are `CHRONOLOGICAL_COMPANY_REGISTER_EXCERPT`,
  `CURRENT_COMPANY_REGISTER_EXCERPT`, `SHAREHOLDER_LIST`, `ARTICLES_OF_ASSOCIATION`,
  `SUPERVISORY_BOARD_LIST`, `TRANSPARENCY_REGISTER`, `STRUCTURED_XML_REGISTRY_CONTENT`,
  `AML_GENERAL_CHECK_DOCUMENT`.

  **That enum is German-KYC shaped, and most foreign registry documents do not fit it.** The GB
  case we ordered returned `CS01`, `Annual Return`, `Certificate of Change of Name`, `Accounts`,
  `New Incorporation` - none of which is an HR-Auszug, a Gesellschafterliste or a Satzung. Forcing
  them into a German slot mislabels them; inventing a type hides them. **So a document whose kind
  has no built-in equivalent is filed as a PROCESS document** (`OTHERKYCDOCS_<LABEL>`, "Sonstige
  Dokumente"), where the suffix is a free label and the dedup key is the **filename** - name it
  `<Kind>_<Company>_<Date>.pdf`. Only where the kind genuinely matches (a Satzung, a
  Gesellschafterliste) does it belong in a customer slot. Task 5 must decide this per document,
  not per case.

- **Send an explicit `application/pdf`; the server does not sniff.** It stores whatever
  Content-Type the multipart part carries, so a vendor byte stream forwarded with its claimed type
  lands as `application/octet-stream` and the browser refuses to preview it - download-only, and it
  looks broken to the reviewer. Detect the type from the bytes (`%PDF-`) and set it ourselves.
- **The malware scan is asynchronous.** An upload returns 200 immediately and the file can serve
  correctly, then later answer `400 "Document is corrupted. Potential malware detected"`. Valid
  PDFs from registries do false-positive (measured on Bundesanzeiger Transparenzregister files).
  An acquisition is therefore not provably complete at upload time - task 6 should re-check, and a
  document that flips to blocked needs a visible state rather than a silent gap.

- Reuse, do not reimplement: `DocumentManagementService.uploadDocument(...)` is the only sanctioned way to put bytes in storage and attach them to a client. Do not call `FileStorage` directly from `aggregation`.
- Do not change the public contract in this task. `caseCommonId` stays `Long`, document ids stay as they are, `includePending` still means what it means. P3 is the one contract break.
- **`KycCaseLink.ready` is not trustworthy — never select work by it.** Measured on dev 2026-09-04
  (case `1000005421`): `KycGatewayService.isReady` returns true when *either* `statusName == "Ready"`
  **or** `caseReadyDatetime` is non-blank, and the vendor stamps `caseReadyDatetime` at creation. So
  `completeCreate` saves the link `ready=true, statusName="Initializing Case"`, and
  `refreshTrackedStatuses` — which queries `findByReadyFalseAndKycCaseCommonIdNotNull()` — never sees
  it again. Forty minutes later the stored row still read `Initializing Case` while the vendor read
  `Ready`. **Task 4 fixes this first**; until it is fixed, any P2 worker that filters on `ready`
  inherits a permanently frozen status. The ingestion worker (Task 6) must key off acquisitions and
  document availability, never `ready`.

- No retention job. **Decided 2026-08-29:** documents are kept indefinitely; deletion happens only as a cascade of client deletion. **Refined 2026-09-05:** a document may be reused for another customer **only where we can prove it has not changed at the source** — no new version. The `fetchedAt` clock is a cheap pre-filter, not the gate. Where a source has no free way to answer that question (kyc.com, as far as we know), reuse does not apply — so **task 9 is out of the MVP** and belongs with the direct registry sources.

---

## File Structure

| File | Responsibility |
|---|---|
| `src/main/java/com/betterco/app/aggregation/AcquisitionStatus.java` | The lifecycle and which transitions are legal |
| `src/main/java/com/betterco/app/aggregation/SourceRefSpace.java` | Which vendor id space a `sourceRef` belongs to |
| `src/main/java/com/betterco/app/aggregation/DocumentAcquisition.java` | One fetch of one document from one source |
| `src/main/java/com/betterco/app/aggregation/DocumentAcquisitionRepository.java` | Mongo repository |
| `src/main/java/com/betterco/app/aggregation/DocumentAcquisitionService.java` | Find/save wrappers, mirroring `service/implementation/CaseService` |
| `src/main/java/com/betterco/app/aggregation/SourcePollPolicy.java` | Schedule, give-up point, terminal action for one source |
| `src/main/java/com/betterco/app/aggregation/SourcePollPolicies.java` | The registry of policies; kyc.com's is the only entry in P2 |
| `src/main/java/com/betterco/app/aggregation/DocumentIngestor.java` | Fetch bytes → store → attach → record the acquisition |
| `src/main/java/com/betterco/app/aggregation/DocumentIngestionWorker.java` | The per-document scheduled pass |
| `src/main/java/com/betterco/app/aggregation/AggregatedDocumentContentService.java` | Serve from storage, with fetch-store-serve fallback |
| `src/main/java/com/betterco/app/aggregation/DocumentReusePolicy.java` | Is a stored document still fresh enough to reuse |
| `src/main/java/com/betterco/app/integration/kyc_com/KycGatewayService.java` | `refreshTrackedStatuses` consults the policy instead of polling flat |
| `src/main/java/com/betterco/app/rest/api/KycApiImpl.java` | Content endpoint routed through the aggregator |
| `src/main/java/com/betterco/app/service/implementation/CustomerService.java` | `deleteAllClientInfo` cascades to documents and acquisitions |
| `src/main/resources/application.properties` | `aggregation.*` defaults, all off |
| `src/test/java/com/betterco/app/aggregation/*Test.java` | Unit tests per class above |

---

### Task 0: Read the ingestion seams, then write the fixtures

Nothing in this task is written from memory. The four reads below are the contract the rest of the plan depends on; if a signature differs from what a later task quotes, **the real signature wins**.

**Files:**
- Read: `src/main/java/com/betterco/app/doc_management/service/DocumentManagementService.java` — specifically `uploadDocument(UploadData uploadData, String actorId, String workspaceId)` (returns `Document`), `downloadDocument(String id)` (returns `byte[]`), `deleteDocumentsByCompanyId(String companyId)`, and `deleteDocument(String fileId)`.
- Read: `src/main/java/com/betterco/app/doc_management/model/Document.java` and `.../model/UploadData.java` — note `Document.id` is the `bettercoDocumentId` and `Document.path` is the storage key; note `UploadData` is a `record` with a compact constructor that validates `documentType`.
- Read: `src/main/java/com/betterco/app/integration/kyc_com/KycGatewayService.java:517-560` — `listDocumentsById`, `toPendingDocument`, `downloadDocumentById`, `availabilityOf`. This is where the two id spaces live.
- Read: `src/main/java/com/betterco/app/domain/KycCaseLink.java` and `src/main/java/com/betterco/app/rest/repository/KycCaseLinkRepository.java` — the local pattern for a Mongo entity (Lombok `@Data @Builder @NoArgsConstructor @AllArgsConstructor @EqualsAndHashCode(callSuper = true)`, `extends AuditMetadata`, `@Document(collection = ...)`, `@CompoundIndex`) and its repository.
- Create: `src/test/java/com/betterco/app/aggregation/AcquisitionFixtures.java`

**Interfaces:**
- Produces: `AcquisitionFixtures.acquisition(String caseId, String sourceRef, AcquisitionStatus status)` returning `DocumentAcquisition`, and `AcquisitionFixtures.storedDocument(String id, String path)` returning `com.betterco.app.doc_management.model.Document`.

- [ ] **Step 1: Do the five reads above** and write down, in the PR description, the exact signature of `uploadDocument`, `downloadDocument(String)` and `deleteDocumentsByCompanyId`. Every later task cites them; none of them may be guessed.

- [ ] **Step 2: Note two facts that change later steps.**
  1. `Document` has **no** `caseId` field. Attachment to a client is by `companyId`, which `uploadDocument` sets from its `actorId` argument — i.e. the client's actor. `BusinessRelation.getCustomerActorId()` is that id, reachable via `BusinessRelationService.findById(String)`. "Attach to the Case" therefore means: `companyId` = the client's customer actor, and the link back to the matter lives on the `DocumentAcquisition`, not on the `Document`.
  2. There is **no vendor-neutral document-kind vocabulary in this repository.** `com.betterco.app.domain.KYCDocumentType` is a seven-value German-KYC enum, not the curation the phase-1 spec §5 refers to. P2 therefore stores the vendor's own label verbatim and leaves the neutral mapping to P3. Do not invent an enum for it.

- [ ] **Step 3: Write the fixture helper**, using only fields that exist on the classes read above. Do not write it until Task 1 and Task 2 have defined `AcquisitionStatus` and `DocumentAcquisition` — commit it with Task 2 if that is simpler.

- [ ] **Step 4: Commit**

```bash
git checkout -b p2/task0-seams
git add src/test/java/com/betterco/app/aggregation/AcquisitionFixtures.java
git commit -m "test: fixtures for document acquisitions"
```

---

### Task 1: The acquisition lifecycle

**Files:**
- Create: `src/main/java/com/betterco/app/aggregation/AcquisitionStatus.java`
- Test: `src/test/java/com/betterco/app/aggregation/AcquisitionStatusTest.java`

**Interfaces:**
- Produces: `AcquisitionStatus` enum with `REQUESTED`, `IN_PROGRESS`, `STORED`, `MISSING`, `MANUAL_QUEUED`, `FAILED`; `isTerminal()` returning `boolean`; `canTransitionTo(AcquisitionStatus next)` returning `boolean`.

- [ ] **Step 1: Write the failing tests**

```java
class AcquisitionStatusTest {

  @Test
  void storedMissingManualQueuedAndFailedAreTerminal() {
    assertTrue(AcquisitionStatus.STORED.isTerminal());
    assertTrue(AcquisitionStatus.MISSING.isTerminal());
    assertTrue(AcquisitionStatus.MANUAL_QUEUED.isTerminal());
    assertTrue(AcquisitionStatus.FAILED.isTerminal());
    assertFalse(AcquisitionStatus.REQUESTED.isTerminal());
    assertFalse(AcquisitionStatus.IN_PROGRESS.isTerminal());
  }

  @Test
  void requestedMayOnlyAdvance() {
    assertTrue(AcquisitionStatus.REQUESTED.canTransitionTo(AcquisitionStatus.IN_PROGRESS));
    assertTrue(AcquisitionStatus.IN_PROGRESS.canTransitionTo(AcquisitionStatus.STORED));
    assertTrue(AcquisitionStatus.IN_PROGRESS.canTransitionTo(AcquisitionStatus.MISSING));
  }

  @Test
  void aTerminalStatusNeverMovesAgain() {
    for (AcquisitionStatus next : AcquisitionStatus.values()) {
      assertFalse(AcquisitionStatus.STORED.canTransitionTo(next));
      assertFalse(AcquisitionStatus.FAILED.canTransitionTo(next));
    }
  }
}
```

- [ ] **Step 2: Push and watch it fail** — `AcquisitionStatus` does not exist. CI runs on an approved review or a manual dispatch; do not assert failure without seeing the run.

- [ ] **Step 3: Write the enum.** The lifecycle is the one in phase-1 spec §4, mirroring the Handelsregister sidecar's `PipelineStatus` so both sources speak one language:

```
REQUESTED → IN_PROGRESS → STORED
                        ↘ MISSING        registry has no such document
                        ↘ MANUAL_QUEUED  needs a human
                        ↘ FAILED
```

`REQUESTED` may also go straight to a terminal state — a document listed as `missing` on the very first pass is never `IN_PROGRESS`.

- [ ] **Step 4: Push, confirm CI green, commit**

```bash
git commit -am "feat: the document acquisition lifecycle"
```

---

### Task 2: The `DocumentAcquisition` entity, repository and service

**Files:**
- Create: `src/main/java/com/betterco/app/aggregation/SourceRefSpace.java`
- Create: `src/main/java/com/betterco/app/aggregation/DocumentAcquisition.java`
- Create: `src/main/java/com/betterco/app/aggregation/DocumentAcquisitionRepository.java`
- Create: `src/main/java/com/betterco/app/aggregation/DocumentAcquisitionService.java`
- Test: `src/test/java/com/betterco/app/aggregation/DocumentAcquisitionServiceTest.java`

**Interfaces:**
- Consumes: `DocumentAcquisitionRepository extends MongoRepository<DocumentAcquisition, String>`.
- Produces: `DocumentAcquisitionService.save(DocumentAcquisition)`, `.findBySourceAndVendorTargetAndSourceRef(String source, KycVendorTarget target, String sourceRef)` returning `Optional<DocumentAcquisition>`, `.findOpenByCaseId(String caseId)` returning `List<DocumentAcquisition>`, `.findOpen()` returning `List<DocumentAcquisition>`, `.deleteAllByBusinessRelationId(String)`.

- [ ] **Step 1: Write the failing tests** — pure Mockito over the repository; there is no Mongo in unit tests.

```java
@ExtendWith(MockitoExtension.class)
class DocumentAcquisitionServiceTest {

  @Mock private DocumentAcquisitionRepository repository;
  private DocumentAcquisitionService service;

  @BeforeEach
  void setUp() {
    service = new DocumentAcquisitionService(repository);
  }

  @Test
  void anAcquisitionIsIdentifiedBySourceAndSourceRef() {
    DocumentAcquisition a = AcquisitionFixtures.acquisition("case1", "77", AcquisitionStatus.STORED);
    when(repository.findBySourceAndSourceRef("kyc.com", "77")).thenReturn(Optional.of(a));

    assertSame(a, service.findBySourceAndSourceRef("kyc.com", "77").orElseThrow());
  }

  @Test
  void openMeansNotTerminal() {
    service.findOpen();

    verify(repository).findByStatusIn(List.of(AcquisitionStatus.REQUESTED, AcquisitionStatus.IN_PROGRESS));
  }
}
```

- [ ] **Step 2: Push and watch it fail.**

- [ ] **Step 3: Write `SourceRefSpace`.** Two values, named for what they actually are, with the reason in the javadoc:

```java
package com.betterco.app.aggregation;

/**
 * kyc.com hands out document ids in two unrelated spaces, and the download call differs per space.
 * KYC_CASE_DOCUMENT is the numeric caseDocumentId from KycComUserClient.listCaseDocuments(long),
 * downloaded by KycComUserClient.downloadDocument(long).
 * KYC_COMPANY_DOCUMENT is the id parsed out of the "link" field of KycComClient.getCompanyDocuments(long),
 * downloaded by KycComClient.downloadDocument(String).
 * Recording the space is what stops a later fetch from crossing them.
 */
public enum SourceRefSpace {
  KYC_CASE_DOCUMENT,
  KYC_COMPANY_DOCUMENT
}
```

- [ ] **Step 4: Write the entity**, following `KycCaseLink` exactly for annotations and inheritance. `createdAt` comes from `AuditMetadata` and is the acquisition's *requested at* — do not add a second field for it.

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(callSuper = true)
@Document(collection = "documentAcquisition")
@CompoundIndex(name = "acq_unique_source_ref_idx", def = "{'source': 1, 'vendorTarget': 1, 'sourceRef': 1}",
        unique = true, partialFilter = "{'sourceRef': {'$type': 'string'}}")
@CompoundIndex(name = "acq_case_idx", def = "{'caseId': 1}")
@CompoundIndex(name = "acq_status_idx", def = "{'status': 1}")
public class DocumentAcquisition extends AuditMetadata {

  @Id
  private String id;

  private String workspaceId;
  private String businessRelationId;   // the client
  private String caseId;               // the matter (domain/Case.id)
  private String customerActorId;      // == Document.companyId once stored

  private String source;               // "kyc.com" in P2
  private KycVendorTarget vendorTarget; // SANDBOX or PRODUCTION - see below
  private String sourceRef;
  private SourceRefSpace sourceRefSpace;

  // Decided 2026-09-06: EVERY delivered file is stored. Roles are an overlay, not a filing key.
  private Set<DocumentRole> roles;     // REGISTERAUSZUG | GESELLSCHAFTERLISTE | GESELLSCHAFTSVERTRAG
                                       // 0..n - EMPTY IS NORMAL and must never block storage
  private String requestedKind;        // only where a source lets you ask for one document (INPI);
                                       // null for kyc.com, where you order a case and take the set
  private String vendorCategory;       // KycDocument.category, kept verbatim for traceability
  private String vendorName;           // KycDocument.name, likewise

  private String bettercoDocumentId;   // doc_management Document.id
  private String storageKey;           // doc_management Document.path

  private AcquisitionStatus status;
  private LocalDateTime fetchedAt;
  private LocalDate contentDate;
  private LocalDateTime lastPolledAt;
  private String failureReason;

  private BigDecimal costUsd;
}
```

`fetchedAt` and `contentDate` stay separate on purpose: a statement fetched today can carry a 2019 filing date. `costUsd` is the vendor cost of *this fetch*; the per-case charge records of phase-1 spec §7 are P4 and are not created here.

- [ ] **Step 5: Write the repository and the service.** No `@Query` is needed — derived method names cover all of it (`findBySourceAndSourceRef`, `findByStatusIn`, `findByCaseIdAndStatusIn`, `deleteAllByBusinessRelationId`). Indexes need no Mongock change unit: `spring.data.mongodb.auto-index-creation=true` is already set in `application.properties`.

- [ ] **Step 6: Push, confirm CI green, commit**

```bash
git add src/main/java/com/betterco/app/aggregation/ src/test/java/com/betterco/app/aggregation/
git commit -m "feat: DocumentAcquisition records one fetch of one document"
```

---

### Task 3: Backoff as a per-source policy object

Today's cadence is a single line — `@Scheduled(fixedDelayString = "${kyc-com.status-poll-interval:PT5M}")` on `KycGatewayService.refreshTrackedStatuses()`. Every source polls every five minutes forever, because there is nowhere to say otherwise. A policy object is that place, and it is what makes P6's synchronous INPI expressible at all: its policy is *no polling*.

**Files:**
- Create: `src/main/java/com/betterco/app/aggregation/SourcePollPolicy.java`
- Create: `src/main/java/com/betterco/app/aggregation/SourcePollPolicies.java`
- Test: `src/test/java/com/betterco/app/aggregation/SourcePollPolicyTest.java`

**Interfaces:**
- Produces: `SourcePollPolicy` — a record of `List<Duration> schedule` (cumulative offsets from the request), and `TerminalAction terminalAction`; methods `nextPollAt(LocalDateTime requestedAt, LocalDateTime lastPolledAt)` returning `Optional<LocalDateTime>` (empty = given up) and `isDue(LocalDateTime requestedAt, LocalDateTime lastPolledAt, LocalDateTime now)` returning `boolean`.
- Produces: `SourcePollPolicy.TerminalAction` enum — `FLAG`, `MANUAL_QUEUE`, `FAIL`; and `SourcePollPolicy.none()` for synchronous sources.
- Produces: `SourcePollPolicies.forSource(String source)` returning `SourcePollPolicy`.

- [ ] **Step 1: Write the failing tests.** Offsets are cumulative from the request, not gaps between polls, so no attempt counter has to be persisted anywhere.

```java
class SourcePollPolicyTest {

  private static final LocalDateTime T0 = LocalDateTime.of(2026, 8, 29, 9, 0);

  private final SourcePollPolicy kycCom = new SourcePollPolicy(
      List.of(Duration.ofHours(1), Duration.ofHours(6), Duration.ofHours(12), Duration.ofHours(24)),
      SourcePollPolicy.TerminalAction.FLAG);

  @Test
  void notDueBeforeTheFirstOffset() {
    assertFalse(kycCom.isDue(T0, null, T0.plusMinutes(30)));
  }

  @Test
  void dueAtTheFirstOffset() {
    assertTrue(kycCom.isDue(T0, null, T0.plusHours(1)));
  }

  @Test
  void notDueAgainUntilTheNextOffset() {
    assertFalse(kycCom.isDue(T0, T0.plusHours(1), T0.plusHours(2)));
    assertTrue(kycCom.isDue(T0, T0.plusHours(1), T0.plusHours(6)));
  }

  @Test
  void givesUpAfterTheLastOffset() {
    assertTrue(kycCom.nextPollAt(T0, T0.plusHours(24)).isEmpty());
    assertFalse(kycCom.isDue(T0, T0.plusHours(24), T0.plusDays(3)));
  }

  @Test
  void aSynchronousSourceNeverPolls() {
    SourcePollPolicy none = SourcePollPolicy.none();
    assertFalse(none.isDue(T0, null, T0.plusYears(1)));
    assertTrue(none.nextPollAt(T0, null).isEmpty());
  }
}
```

- [ ] **Step 2: Push and watch it fail.**

- [ ] **Step 3: Implement `SourcePollPolicy`.** `nextPollAt` = the first offset whose absolute time is strictly after `lastPolledAt` (or the first offset when `lastPolledAt` is null); empty when none remains. `isDue` = `nextPollAt` is present and not after `now`.

- [ ] **Step 4: Implement `SourcePollPolicies`** as a `@Component` holding a `Map<String, SourcePollPolicy>`. In P2 it has exactly one entry — kyc.com, `1h / 6h / 12h / 24h`, then `FLAG` — and returns `SourcePollPolicy.none()` for anything unknown. Read the schedule from configuration so staging can shorten it:

```properties
aggregation.poll.kyc-com.schedule=PT1H,PT6H,PT12H,PT24H
aggregation.poll.kyc-com.terminal-action=FLAG
```

Leave `kyc-com.status-poll-interval` in place: it is the *tick* of the scheduler, not the backoff. The policy decides which links each tick actually touches.

- [ ] **Step 5: Push, confirm CI green, commit**

```bash
git commit -am "feat: per-source poll policy replaces a flat interval"
```

---

### Task 4: Fix the `ready` flag, then make `refreshTrackedStatuses` obey the policy

Two changes to the same method, in this order. The backoff policy is pointless while the poller is
handed an empty work list, which is what happens today (see the `ready` constraint above).

**Files:**
- Modify: `src/main/java/com/betterco/app/integration/kyc_com/KycGatewayService.java` (`refreshTrackedStatuses`, `refreshLinkStatus`, the constructor)
- Test: `src/test/java/com/betterco/app/integration/kyc_com/KycGatewayServiceTest.java`

**Interfaces:**
- Consumes: `SourcePollPolicies.forSource(String)`.
- Unchanged: `KycCaseLinkRepository.findByReadyFalseAndKycCaseCommonIdNotNull()`, `KycCaseLink.getLastPolledAt()`, `KycCaseLink.getCreatedAt()` (inherited from `AuditMetadata`), `KycCaseLink.isReady()`.

- [ ] **Step 0a: Write the failing test for the frozen status.**

```java
  @Test
  void aCaseIsNotReadyMerelyBecauseTheVendorStampedACaseReadyDatetime() {
    // The vendor stamps caseReadyDatetime at creation; only statusName says the case is done.
    KycCaseStatus status = service.getCaseStatusById(1L);   // stub: statusName "Initializing Case",
                                                            // caseReadyDatetime "2026-09-04T13:55:52"
    assertThat(status.getReady()).isFalse();
  }
```

- [ ] **Step 0b: Fix `isReady` (`KycGatewayService.java:766`).** Drop the `caseReadyDatetime` half;
  readiness is `"ready".equals(statusName.toLowerCase(Locale.ROOT))` and nothing else. **Open
  question for the reviewer, state it in the PR:** if the live vendor ever reports a finished case
  under a `statusName` other than `Ready`, that case now never flips — the sandbox only ever showed
  `Initializing Case -> Performing AML checks -> Ready`, so the live status vocabulary is unverified.
  If the reviewer will not accept that risk, the fallback is to keep `caseReadyDatetime` but require
  it to be *in the past by more than a minute*, which the creation stamp never is.

- [ ] **Step 0c: Backfill the links already frozen.** Every case created before this fix is stored
  `ready=true` with a creation-time status and will never be re-polled. Add a Mongock changeset that
  sets `ready=false` on `kycCaseLink` documents whose `statusName` is not `Ready`, so the poller
  picks them up once and corrects them.

- [ ] **Step 1: Read `KycGatewayService.java:449-500`** — `refreshTrackedStatuses` and `refreshLinkStatus` — and its constructor at `:87-107`, before changing either. The constructor is ten arguments long and every existing test builds the service by hand, so an added dependency is an edit to `KycGatewayServiceTest.setUp()` as well.

- [ ] **Step 2: Write the failing tests** in the existing suite, whose fixture and mocking style is already established there.

```java
  @Test
  void aLinkPolledMinutesAgoIsSkipped() {
    KycCaseLink fresh = KycCaseLink.builder().kycCaseCommonId(1L).ready(false)
        .lastPolledAt(LocalDateTime.now().minusMinutes(5)).build();
    when(linkRepository.findByReadyFalseAndKycCaseCommonIdNotNull()).thenReturn(List.of(fresh));

    service.refreshTrackedStatuses();

    verify(client, never()).getCompany(anyLong());
  }

  @Test
  void aLinkPastItsGiveUpPointIsNeverPolledAgain() {
    KycCaseLink old = KycCaseLink.builder().kycCaseCommonId(1L).ready(false)
        .lastPolledAt(LocalDateTime.now().minusDays(3)).build();
    old.setCreatedAt(LocalDateTime.now().minusDays(4));
    when(linkRepository.findByReadyFalseAndKycCaseCommonIdNotNull()).thenReturn(List.of(old));

    service.refreshTrackedStatuses();

    verify(client, never()).getCompany(anyLong());
  }
```

- [ ] **Step 3: Push and watch them fail** — today every tracked link is polled unconditionally.

- [ ] **Step 4: Implement.** Inject `SourcePollPolicies` and filter the tracked list by `policy.isDue(link.getCreatedAt(), link.getLastPolledAt(), LocalDateTime.now())` before submitting to the pool. Where the policy has given up, apply its `TerminalAction`: for `FLAG`, log at `warn` with the `caseCommonId` and leave the link alone — do not mark it ready, because it is not.

- [ ] **Step 5: Fix `KycGatewayServiceTest.setUp()`** for the extra constructor argument, and check every other construction site of `KycGatewayService` in `src/test` before pushing.

- [ ] **Step 6: Push, confirm CI green, commit**

```bash
git commit -am "fix: ready means the vendor is done; status polling backs off on its own schedule"
```

---

### Task 5: Fetch, store, attach, record

The ingestion primitive. One document, one source, one acquisition. It is written before the worker so the worker has something real to call.

**Files:**
- Create: `src/main/java/com/betterco/app/aggregation/DocumentIngestor.java`
- Test: `src/test/java/com/betterco/app/aggregation/DocumentIngestorTest.java`

**Interfaces:**
- Consumes: `KycGatewayService.downloadDocumentById(String documentId, boolean includePending)` returning `byte[]`; `DocumentManagementService.uploadDocument(UploadData uploadData, String actorId, String workspaceId)` returning `com.betterco.app.doc_management.model.Document`; `BusinessRelationService.findById(String)` returning `BusinessRelation`; `DocumentAcquisitionService.save(...)`.
- Produces: `DocumentIngestor.ingest(DocumentAcquisition acquisition)` returning the saved `DocumentAcquisition`.

- [ ] **Step 1: Re-read `DocumentManagementService.uploadDocument(...)` before writing anything.** Confirm three things by reading, not by assuming: it builds a `FileContent`-backed `UploadData`; it sets `Document.companyId` from its `actorId` argument; and it puts `uploadData.processId()` into the storage tags map. A document ordered through the aggregator has **no process**, so verify what a null `processId` does to that `HashMap` before you pass one.

- [ ] **Step 2: Write the failing tests**

```java
@ExtendWith(MockitoExtension.class)
class DocumentIngestorTest {

  @Mock private KycGatewayService gatewayService;
  @Mock private DocumentManagementService documentManagementService;
  @Mock private DocumentAcquisitionService acquisitionService;
  @Mock private BusinessRelationService businessRelationService;
  private DocumentIngestor ingestor;

  @Test
  void storesTheBytesAndRecordsTheDocumentIdAndStorageKey() {
    DocumentAcquisition a = AcquisitionFixtures.acquisition("case1", "77", AcquisitionStatus.REQUESTED);
    when(gatewayService.downloadDocumentById("77", true)).thenReturn("pdf".getBytes());
    when(documentManagementService.uploadDocument(any(), eq("actor1"), eq("ws1")))
        .thenReturn(AcquisitionFixtures.storedDocument("doc1", "actor1-documents/abc"));

    DocumentAcquisition out = ingestor.ingest(a);

    assertEquals(AcquisitionStatus.STORED, out.getStatus());
    assertEquals("doc1", out.getBettercoDocumentId());
    assertEquals("actor1-documents/abc", out.getStorageKey());
    assertNotNull(out.getFetchedAt());
  }

  @Test
  void downloadsThroughTheClientThatMatchesTheIdSpace() {
    DocumentAcquisition a = AcquisitionFixtures.acquisition("case1", "abc", AcquisitionStatus.REQUESTED);
    a.setSourceRefSpace(SourceRefSpace.KYC_COMPANY_DOCUMENT);

    ingestor.ingest(a);

    verify(gatewayService).downloadDocumentById("abc", false);
  }

  @Test
  void aVendorFailureLeavesTheAcquisitionInProgressWithAReason() {
    DocumentAcquisition a = AcquisitionFixtures.acquisition("case1", "77", AcquisitionStatus.REQUESTED);
    when(gatewayService.downloadDocumentById("77", true)).thenThrow(new RuntimeException("502"));

    DocumentAcquisition out = ingestor.ingest(a);

    assertEquals(AcquisitionStatus.IN_PROGRESS, out.getStatus());
    assertNotNull(out.getFailureReason());
  }
}
```

- [ ] **Step 3: Push and watch them fail.**

- [ ] **Step 4: Implement.** `includePending` is derived from `SourceRefSpace`, never passed in — `KYC_CASE_DOCUMENT` → `true`, `KYC_COMPANY_DOCUMENT` → `false`. That single mapping is the whole defence against crossing the id spaces. Build the `UploadData` with `FileContent.build(name, bytes, "application/pdf")`, `isAutoLoaded(true)`, `documentScope(DocumentScope.COMPANY)`, `source` and `sourceName` carrying the vendor, and `documentDate` from the acquisition's `contentDate` when it is known. Use the exact `UploadData` component names read in Task 0 — it is a `record`, so the builder names are the component names.

- [ ] **Step 5: Handle failure the way phase-1 spec §8 says.** A vendor error is not terminal: leave the acquisition `IN_PROGRESS` with a `failureReason`, and let the poll policy decide when to give up. Only the policy's give-up point produces `FAILED` or `MANUAL_QUEUED`.

- [ ] **Step 6: Push, confirm CI green, commit**

```bash
git commit -am "feat: ingest one document into the client's storage"
```

---

### Task 6: The per-document ingestion worker

Driven **per document, never by case-ready** — that is the whole point. Documents arrive progressively, long before a case is ready, and this is what `includePending` exposed and what STP was sold in July.

**Files:**
- Create: `src/main/java/com/betterco/app/aggregation/DocumentIngestionWorker.java`
- Test: `src/test/java/com/betterco/app/aggregation/DocumentIngestionWorkerTest.java`
- Modify: `src/main/resources/application.properties`

**Interfaces:**
- Consumes: `KycCaseLinkRepository.findByReadyFalseAndKycCaseCommonIdNotNull()` returning `List<KycCaseLink>`; `KycGatewayService.listDocumentsById(String workspaceId, long caseCommonId, boolean includePending)` returning `KycCaseDocuments`; `KycCaseDocuments.getDocuments()` returning `List<KycDocument>`; `KycDocument.getDocumentId()`, `.getAvailability()`, `.getCategory()`, `.getName()`; `DocumentAcquisitionService`; `DocumentIngestor.ingest(...)`; `SourcePollPolicies.forSource(...)`.
- Produces: `DocumentIngestionWorker.ingestPass()` — package-private, `@Scheduled`.

- [ ] **Step 1: Read the generated DTOs before writing the test** — `KycCaseDocuments` and `KycDocument` are generated from `betterco_api.yaml`; confirm the getter names and the exact type of `KycDocument.getAvailability()` (it is an enum, `KycDocument.AvailabilityEnum`, with values `available` / `pending` / `missing`) in the generated sources rather than from the YAML.

- [ ] **Step 2: Write the failing tests**

```java
  @Test
  void ingestsAnAvailableDocumentThatIsNotYetStored() {
    when(linkRepository.findByReadyFalseAndKycCaseCommonIdNotNull()).thenReturn(List.of(link(42L)));
    when(gatewayService.listDocumentsById("ws1", 42L, true)).thenReturn(documents(available("77")));
    when(acquisitionService.findBySourceAndSourceRef("kyc.com", "77")).thenReturn(Optional.empty());

    worker.ingestPass();

    verify(ingestor).ingest(any(DocumentAcquisition.class));
  }

  @Test
  void doesNotFetchTheSameDocumentTwice() {
    when(linkRepository.findByReadyFalseAndKycCaseCommonIdNotNull()).thenReturn(List.of(link(42L)));
    when(gatewayService.listDocumentsById("ws1", 42L, true)).thenReturn(documents(available("77")));
    when(acquisitionService.findBySourceAndSourceRef("kyc.com", "77"))
        .thenReturn(Optional.of(AcquisitionFixtures.acquisition("case1", "77", AcquisitionStatus.STORED)));

    worker.ingestPass();

    verify(ingestor, never()).ingest(any());
  }

  @Test
  void ingestsBeforeTheCaseIsReady() {
    // the link under test has ready == false; there is no ready check anywhere in the worker
    when(linkRepository.findByReadyFalseAndKycCaseCommonIdNotNull()).thenReturn(List.of(link(42L)));
    when(gatewayService.listDocumentsById("ws1", 42L, true)).thenReturn(documents(available("77")));

    worker.ingestPass();

    verify(ingestor).ingest(any());
  }

  @Test
  void aMissingDocumentIsRecordedAsAGapAndNeverFetched() {
    when(linkRepository.findByReadyFalseAndKycCaseCommonIdNotNull()).thenReturn(List.of(link(42L)));
    when(gatewayService.listDocumentsById("ws1", 42L, true)).thenReturn(documents(missing()));

    worker.ingestPass();

    verify(ingestor, never()).ingest(any());
    ArgumentCaptor<DocumentAcquisition> saved = ArgumentCaptor.forClass(DocumentAcquisition.class);
    verify(acquisitionService).save(saved.capture());
    assertEquals(AcquisitionStatus.MISSING, saved.getValue().getStatus());
    assertNull(saved.getValue().getSourceRef());
  }

  @Test
  void doesNothingWhenTheFlagIsOff() {
    worker = new DocumentIngestionWorker(/* ... */ false);

    worker.ingestPass();

    verifyNoInteractions(gatewayService);
  }
```

- [ ] **Step 3: Push and watch them fail.**

- [ ] **Step 4: Implement the pass.** For each tracked link with a `kycCaseCommonId`: list with `includePending=true`, and for each returned `KycDocument`
  - `availability == available` and no `STORED` acquisition for `("kyc.com", documentId)` → build the acquisition (`sourceRefSpace = KYC_CASE_DOCUMENT`, `vendorCategory = getCategory()`, `vendorName = getName()`, status `REQUESTED`) and hand it to `DocumentIngestor.ingest(...)`;
  - `availability == pending` → upsert an acquisition in `IN_PROGRESS` and move on;
  - `availability == missing` → record `MISSING` once. Per phase-1 spec §6, missing rows carry no document id, have nothing to fetch, and are **never charged**.

- [ ] **Step 5: Put the whole thing behind the flag.**

```java
  @Scheduled(fixedDelayString = "${aggregation.ingestion.interval:PT5M}")
  void ingestPass() {
    if (!ingestionEnabled) {
      return;
    }
    ...
  }
```

```properties
aggregation.ingestion.enabled=false
aggregation.ingestion.interval=PT5M
```

Do not put the flag in `application-staging.properties` or `application-production.properties` in this task. Turning it on is a separate, deliberate change the backend dev makes.

- [ ] **Step 6: Push, confirm CI green, commit**

```bash
git commit -am "feat: ingest documents per document, not per ready case"
```

---

### Task 7: Serve content from our storage, with a fetch-store-serve fallback

**Files:**
- Create: `src/main/java/com/betterco/app/aggregation/AggregatedDocumentContentService.java`
- Modify: `src/main/java/com/betterco/app/rest/api/KycApiImpl.java` (`downloadDocumentSearchDocumentById`)
- Test: `src/test/java/com/betterco/app/aggregation/AggregatedDocumentContentServiceTest.java`

**Interfaces:**
- Consumes: `DocumentAcquisitionService.findBySourceAndSourceRef(...)`; `DocumentManagementService.downloadDocument(String id)` returning `byte[]`; `DocumentIngestor.ingest(...)`; `KycGatewayService.downloadDocumentById(String, boolean)`.
- Produces: `AggregatedDocumentContentService.content(String workspaceId, long caseCommonId, String documentId, boolean includePending)` returning `byte[]`.

- [ ] **Step 1: Read `KycApiImpl.downloadDocumentSearchDocumentById`** (it is the last method in the file) and note that it wraps the bytes in `FileContent.build(...)` and `FileResponseMapper.mapFileToResourceResponseEntity(file)`. That wrapping stays exactly as it is; only the source of the `byte[]` changes.

- [ ] **Step 2: Write the failing tests**

```java
  @Test
  void aStoredDocumentIsServedFromOurStorage() {
    when(acquisitionService.findBySourceAndSourceRef("kyc.com", "77"))
        .thenReturn(Optional.of(stored("doc1")));
    when(documentManagementService.downloadDocument("doc1")).thenReturn("pdf".getBytes());

    assertArrayEquals("pdf".getBytes(), service.content("ws1", 42L, "77", true));
    verifyNoInteractions(gatewayService);
  }

  @Test
  void anUnstoredDocumentIsFetchedStoredAndServedInOnePass() {
    when(acquisitionService.findBySourceAndSourceRef("kyc.com", "77")).thenReturn(Optional.empty());
    when(ingestor.ingest(any())).thenReturn(stored("doc1"));
    when(documentManagementService.downloadDocument("doc1")).thenReturn("pdf".getBytes());

    assertArrayEquals("pdf".getBytes(), service.content("ws1", 42L, "77", true));
  }

  @Test
  void withTheFlagOffItIsTodaysBehaviourExactly() {
    service = new AggregatedDocumentContentService(/* ... */ false);
    when(gatewayService.downloadDocumentById("77", true)).thenReturn("pdf".getBytes());

    assertArrayEquals("pdf".getBytes(), service.content("ws1", 42L, "77", true));
    verifyNoInteractions(acquisitionService);
  }
```

- [ ] **Step 3: Push and watch them fail.**

- [ ] **Step 4: Implement**, and keep the fallback honest: if storing fails but the bytes were fetched, **serve the bytes anyway**. A storage problem must not turn into a 500 for a document we are holding in memory.

- [ ] **Step 5: Route `KycApiImpl` through it.** One line changes — `gatewayService.downloadDocumentById(...)` becomes `contentService.content(workspaceId, caseCommonId, documentId, ...)`. The response wrapping is untouched.

- [ ] **Step 6: Push, confirm CI green, commit**

```bash
git commit -am "feat: serve document content from our storage, fetching on miss"
```

---

### Task 8: Retention — cascade on client deletion

Decided 2026-08-29: **no retention job.** Documents are kept indefinitely. Deletion happens only when the client is deleted, and there it must actually happen. There is a real gap here today.

**Files:**
- Modify: `src/main/java/com/betterco/app/service/implementation/CustomerService.java` (`deleteAllClientInfo`)
- Test: `src/test/java/com/betterco/app/service/implementation/CustomerServiceTest.java` (extend if it exists; otherwise a focused new test class)

**Interfaces:**
- Consumes: `DocumentManagementService.deleteDocumentsByCompanyId(String companyId)` — already a field on `CustomerService` (`documentManagementService`); `DocumentAcquisitionService.deleteAllByBusinessRelationId(String)`.

- [ ] **Step 1: Read `CustomerService.deleteAllClientInfo` and `deleteAdvisorRelatedClientInfo` side by side** (both are private, near the end of the class). The asymmetry is the bug: `deleteAdvisorRelatedClientInfo` calls `documentManagementService.deleteDocumentsByCompanyId(businessRelation.getCustomerActorId())` and `deleteDocumentsByProcessId(...)` for each process; `deleteAllClientInfo` calls neither. It calls `actorDeletionManager.delete(...)`, which has no `DocumentManagementService` dependency at all — so on that branch the blobs and their `Document` rows are simply orphaned. Confirm this by reading `ActorDeletionManager`'s field list before changing anything.

- [ ] **Step 2: Write the failing test.** Check whether a `CustomerServiceTest` already exists and follow its construction style; `CustomerService` has a long constructor, so this is a Mockito `@InjectMocks` case rather than hand-construction.

```java
  @Test
  void deletingAClientRemovesItsStoredDocuments() {
    // ... arrange the branch that reaches deleteAllClientInfo:
    // invitationDataService.findByIdAndStatus(..., ACCEPTED) returns empty
    customerService.deleteClient(businessRelation, "ws1", true);

    verify(documentManagementService).deleteDocumentsByCompanyId("actor1");
  }

  @Test
  void deletingAClientRemovesItsAcquisitions() {
    customerService.deleteClient(businessRelation, "ws1", true);

    verify(acquisitionService).deleteAllByBusinessRelationId("br1");
  }
```

- [ ] **Step 3: Push and watch the first test fail** — this one is a real defect, not scaffolding. Say so in the PR description; the backend dev will want to know it predates P2.

- [ ] **Step 4: Implement.** Add the `deleteDocumentsByCompanyId` call to `deleteAllClientInfo`, next to `actorDeletionManager.delete(businessRelation.getCustomerActorId())`, and add `acquisitionService.deleteAllByBusinessRelationId(businessRelation.getId())` to **both** private methods. Do not refactor the two methods into one — that is a bigger change than this plan is entitled to, and it touches the ordinary client-deletion path.

- [ ] **Step 5: Add no scheduled job, and write down why.** A short javadoc on `DocumentAcquisition` recording the 2026-08-29 decision — kept indefinitely, cascaded on client deletion — so the next reader does not add a TTL index on `fetchedAt`.

- [ ] **Step 6: Push, confirm CI green, commit**

```bash
git commit -am "fix: client deletion removes the client's stored documents and acquisitions"
```

---

### Task 9: The reuse window

The other half of the retention decision: a stored document may be reused across customers while `fetchedAt` is under 7 days, per-source configurable.

**Files:**
- Create: `src/main/java/com/betterco/app/aggregation/DocumentReusePolicy.java`
- Modify: `src/main/java/com/betterco/app/aggregation/DocumentIngestor.java`
- Test: `src/test/java/com/betterco/app/aggregation/DocumentReusePolicyTest.java`

**Interfaces:**
- Produces: `DocumentReusePolicy.maxAgeFor(String source)` returning `Duration`; `.isReusable(String source, LocalDateTime fetchedAt, LocalDateTime now)` returning `boolean`.

- [ ] **Step 1: Write the failing tests**

```java
  @Test
  void aDocumentFetchedSixDaysAgoIsReusable() {
    assertTrue(policy.isReusable("kyc.com", NOW.minusDays(6), NOW));
  }

  @Test
  void aDocumentFetchedEightDaysAgoIsNot() {
    assertFalse(policy.isReusable("kyc.com", NOW.minusDays(8), NOW));
  }

  @Test
  void neverFetchedIsNeverReusable() {
    assertFalse(policy.isReusable("kyc.com", null, NOW));
  }

  @Test
  void theWindowIsPerSource() {
    assertEquals(Duration.ofDays(7), policy.maxAgeFor("kyc.com"));
    assertEquals(Duration.ofDays(7), policy.maxAgeFor("anything-unconfigured"));
  }
```

- [ ] **Step 2: Push and watch them fail.**

- [ ] **Step 3: Implement**, reading the window from configuration with a 7-day default:

```properties
aggregation.reuse.default-max-age=P7D
aggregation.reuse.kyc-com.max-age=P7D
```

- [ ] **Step 4: Wire it into `DocumentIngestor.ingest(...)`.** Before downloading, look for a `STORED` acquisition of the same source, `sourceRef` and kind whose `fetchedAt` is inside the window; if one exists, do not fetch. Reuse means: create a *new* `DocumentAcquisition` for this case, pointing at the same `bettercoDocumentId` and `storageKey`, with `costUsd` zero and `fetchedAt` copied from the original — the fetch clock belongs to the bytes, not to the row.

- [ ] **Step 5: Add one test to `DocumentIngestorTest`** asserting the vendor is not called when a fresh acquisition already exists, and that the new acquisition carries a zero cost.

- [ ] **Step 6: Push, confirm CI green, commit and open the PR**

```bash
git commit -am "feat: reuse a stored document while it is still fresh"
```

---

### Task 10: A vendor failure must not take an endpoint down

Found verifying P1 on dev 2026-09-04: `GET /document-search/cases?scope=account` answers **HTTP 400
"One or more validation errors occurred."** That string is not ours — `KycComClient.map4xx` copies
the vendor's body through — so the sandbox is rejecting `POST /v2/Case/search-by-properties`
(we send `propertyValue: null`, `pageNumber` 0-based). Staging never showed it because staging talks
to the *live* vendor. It is not a P1 regression, but it is the wrong behaviour either way: one
unhappy vendor query returns 400 for the whole scope instead of the cases we can see.

**Files:**
- Modify: `src/main/java/com/betterco/app/integration/kyc_com/KycGatewayService.java` (`allAccountCases`)
- Test: `src/test/java/com/betterco/app/integration/kyc_com/KycGatewayServiceTest.java`

**Interfaces:**
- Unchanged: `KycComClient.listCasesByProperty(int, int)`, `KycGatewayService.listCases(...)`.

- [ ] **Step 1: Write the failing test.**

```java
  @Test
  void accountScopeDegradesWhenTheVendorRejectsTheQuery() {
    when(client.listCasesByProperty(anyInt(), anyInt()))
        .thenThrow(new KycGatewayException(HttpStatus.BAD_REQUEST, "One or more validation errors occurred."));

    assertThat(service.listCases(WS, null, false, false, "account")).isEmpty();
  }
```

- [ ] **Step 2: Push and watch it fail** — today the exception propagates to the caller as 400.

- [ ] **Step 3: Implement.** Wrap the `client.listCasesByProperty(...)` call in `allAccountCases`:
  catch `KycGatewayException` whose status is 4xx, log at `warn` with the page number and the vendor
  message, and stop paging — returning whatever pages already succeeded. A 5xx keeps propagating;
  a vendor outage is not the same as a query this vendor will not answer.

- [ ] **Step 4: Do not "fix" the payload blind.** Whether `propertyValue: null` or the 0-based
  `pageNumber` is what the sandbox rejects is unmeasured, and the live vendor accepts both today.
  Changing the payload to satisfy the sandbox risks breaking the vendor that works. Ask kyc.com
  what `search-by-properties` requires before touching the body.

- [ ] **Step 5: Push, confirm CI green, commit**

```bash
git commit -am "fix: account-scope case list degrades instead of 400 when the vendor rejects the query"
```

---

## Self-review notes

- **Spec coverage:** this plan implements P2 only — the acquisition entity, per-document ingestion, per-source backoff, storage-backed content, and the retention decision. The contract cut-over (P3), charge records (P4), the `SourceAdapter` port and routing table (P5) and the second and third sources (P6) each get their own plan.
- **Deliberately not here.** No `SourceAdapter` port: with one source there is nothing to abstract, and P5 extracts it from two *working* implementations rather than a guess. No charge records: phase-1 spec §7 needs `PER_CASE` vs `PER_DOCUMENT` and the existing `BillingComputationStrategy` pattern, which is a P4 conversation. No vendor-neutral `kind` vocabulary: it does not exist in this repository (see Task 0 Step 2), and inventing one here would be the exact mistake this plan is written to avoid. `KycCaseLink` is still not deleted — it carries the poll state P2 leans on, and it is retired in P3.
- **The defect found while planning.** `CustomerService.deleteAllClientInfo` does not delete the client's documents, while its sibling `deleteAdvisorRelatedClientInfo` does. That is pre-existing and unrelated to the aggregator, but storing ordered documents makes it matter, so Task 8 fixes it and flags it as pre-existing in the PR.
- **The trap this plan is mostly built around.** kyc.com has two document id spaces with two different clients and two different download signatures. `SourceRefSpace` exists so that the pairing is recorded once, at ingestion, and derived everywhere else — never re-decided by a caller.
- **Reads the implementer must do before writing code**, each named at the step that needs it: `DocumentManagementService.uploadDocument` and `UploadData`'s record components (Task 0, Task 5); the generated `KycDocument` / `KycCaseDocuments` getters and `AvailabilityEnum` (Task 6); `KycGatewayService`'s constructor and its test's `setUp` (Task 4); `KycApiImpl.downloadDocumentSearchDocumentById`'s response wrapping (Task 7); `CustomerService`'s two private delete methods and `ActorDeletionManager`'s field list (Task 8). Nothing in this plan invents an existing symbol; every new name is a class this plan creates.
