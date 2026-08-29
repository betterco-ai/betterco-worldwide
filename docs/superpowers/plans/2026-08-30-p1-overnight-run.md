# P1 overnight run — T0 to T3

Run date: 2026-08-29 (overnight, unattended)
Plan: `docs/superpowers/plans/2026-08-29-p1-client-and-matter.md`
Repo: `betterco-backend`, base `origin/dev` = `730c8644d` ("Create only client (#2273)")

**Outcome: T0, T1, T2, T3 implemented, committed, pushed. Task 4 not touched.
No push to `dev`, no merge, no PR.**

---

## The one thing to read first: CI cannot verify a branch

The plan's verification model does not work, and this is not a "did not get to it" —
it is structurally impossible with the current workflow file.

`.github/workflows/app-tests.yml` triggers on `workflow_dispatch`, `push` to `dev`, and
`pull_request_review`. Its single job carries:

```yaml
jobs:
  testing:
    if: github.event.review.state == 'approved'
```

So the job body only ever runs when the event is an **approved PR review**. On a push to a
feature branch nothing is triggered at all. On `workflow_dispatch` the workflow starts and
the job is **skipped** — a run that reports green while having executed zero tests.

I proved this rather than assuming it. Dispatched against `p1/task0-fixtures`:

- https://github.com/betterco-ai/betterco-backend/actions/runs/33265091121 → `conclusion: skipped`

The same pattern is visible in the repo's own history: every push to `dev` produces a
`Running tests` run with conclusion `skipped`; only `pull_request_review` runs actually
execute `mvn -B test`.

Getting a real CI run therefore requires opening a PR **and** having a human approve it —
both explicitly out of scope for this run. So there is **no green CI run to point at for
any of the four tasks.** Anyone reading this should treat "CI status" below as "not
obtainable", not as "passed".

### What I did instead

The plan states nothing compiles locally (no Maven, no `~/.m2`, `.mvn/` missing). That was
true of the starting state but is fixable, and a real test run beats an unverifiable one:

- Java 17 was already installed (`17.0.8`).
- Downloaded Apache Maven 3.9.9 into the session scratchpad and resolved the full dependency
  tree from Maven Central (the pom declares no private repositories).
- Ran `mvn test` — the same goal CI runs — against each branch.

Nothing was written into the repo to make this work: no `.mvn/`, no committed wrapper, no
pom change. The local repository lives in the scratchpad. `git status` on every branch is
clean apart from the intended files.

Two local-environment caveats, both worked around and neither affecting results:

1. `git-commit-id-plugin` fails inside a detached `git worktree` ("Missing unknown <sha>").
   Skipped with `-Dmaven.gitcommitid.skip=true` **in the baseline worktree only**, never in
   the runs that verify my branches.
2. The JaCoCo agent's `-javaagent:` path was mangled when the local repo sat under the very
   long scratchpad path. Fixed by exposing the same directory through a short junction
   (`C:\m2r`), so **the verifying runs all had JaCoCo active, exactly as CI has it.** This
   matters: two of the T2/T3 tests use reflection over declared fields, and JaCoCo injects a
   synthetic `$jacocoData` field. Those tests filter synthetics and were confirmed green
   *with* instrumentation, not only without it.

---

## Pre-existing failures in this environment (not caused by this work)

A full `mvn test` on **clean `origin/dev`** in a separate worktree fails in 7 test classes.
These are environmental (Docker/Testcontainers/Mongo and a hosts-file quirk), not code:

| Test class | Result on clean dev |
|---|---|
| `billing.service.ApiCounterTest` | 5 failures — expects `kubernetes.docker.internal`, gets `localhost` |
| `billing.strategy.CreatedClientsStrategyTest` | 3 errors — `ExceptionInInitializerError` at class init |
| `billing.strategy.CreatedFlowsStrategyTest` | 2 errors (162 s — container timeout) |
| `billing.strategy.SyncedClientsStrategyTest` | 1 error (73 s — container timeout) |
| `integration.datev.csv.DatevRiskCsvImportServiceTest` | 2 failures |
| `rest.repository.ProcessRepositoryTest` | 3 errors (221 s — container timeout) |
| `service.InconsistencyDataWorkspaceOverrideTest` | 4 errors (152 s — container timeout) |

Every regression figure below is stated **relative to this baseline**. CI presumably has
Docker and passes these; I cannot confirm that.

### Regression, measured against that baseline

Three full `mvn test` runs, same machine, same command:

| Run | Tests | Failures | Errors | Skipped | Failing classes |
|---|---|---|---|---|---|
| clean `origin/dev` (`730c8644d`) | 735 | 7 | 13 | 8 | the 7 above |
| `p1/task1-organization-resolver` | 749 | 7 | 13 | 8 | **the same 7** |
| `p1/task3-vendor-reference` (= T0+T1+T2+T3) | 786 | 7 | 13 | 8 | **the same 7** |

735 → 749 is +14, exactly the T1 tests. 735 → 786 is +51, exactly the T1+T2+T3 tests.
The failure and error counts are **byte-identical across all three runs**, and no failing
class is in `com.betterco.app.aggregation` or `com.betterco.app.integration.kyc_com`.
This work adds 51 passing tests and breaks nothing that was not already broken here.

The T3 full run had **JaCoCo enabled** (no `-Djacoco.skip`), i.e. CI's exact `mvn -B test`
configuration; both aggregation test classes were green inside it.

---

## Task 0 — fixtures

- **Branch:** `p1/task0-fixtures` (off `origin/dev`)
- **Commit:** `5819909e159d1f5a924184c361812877dd3237aa` — `test: fixtures for aggregation client creation`
- **CI:** not obtainable (see above). Verified locally: the file compiles and is exercised by
  the T1-T3 tests; the full-suite numbers in the regression table cover it.
- **Files:** `src/test/java/com/betterco/app/aggregation/AggregationFixtures.java` (new, only file touched)

**Mandatory reads done first.** `Actor.java` and `CustomerService.createCustomer` were read
before a line was written. Confirmed real signatures:

- `Actor` is a Lombok `@Builder` with `entityInfo` (`EntityInfo.legalName`/`displayName`),
  `customerCategoryType` (`CustomerCategoryType.ENTITY|INDIVIDUAL`), `isWorkspaceRootActor`,
  `workspaceId`, `source` (`CreationSource.REST_API`), `legalData`
  (`LegalData.registerData` → `RegisterData.registerCountry`/`registerId`/`registerLegalType`),
  `externalIdentifiers` (`ExternalIdentifier.externalId`/`system`/`url`/`type`).
- `CustomerService.createCustomer(String workspaceId, String orgId, Boolean createDefaultCase,
  String caseName, Actor customerActor, BusinessRelationType relationType)` returns
  `businessRelation.getId()`. Signature matches the plan exactly.

Produces `entityActor(name, jurisdiction, externalCode)` and `organization(id)` as specified.

**Left alone / worth a reviewer's eye:** `AggregationFixtures.entityActor` ends up unused —
T1 only needs `organization(...)`, and T2/T3 assert on the *production* actor that
`AggregationActorFactory` builds rather than comparing against a fixture, which is the
stronger test. The plan mandated the signature, so it is there. Delete it if you disagree.

---

## Task 1 — resolve the workspace's organisation

- **Branch:** `p1/task1-organization-resolver` — **branched off `p1/task0-fixtures`, not off `dev`.**
  The plan's own test body calls `AggregationFixtures.organization(...)`, so it does not
  compile without T0.
- **Commit:** `aa13bfc9031c13dc4b70f1107915a8526feab410` — `feat: resolve the organisation that owns an API-created client`
- **CI:** not obtainable. **Local full `mvn test`: 749 tests, 7 failures + 13 errors — all in
  the 7 pre-existing classes. Zero new failures.**
  `WorkspaceOrganizationResolverTest`: 14/14 green.
- **Files:** `WorkspaceOrganizationResolver.java` (new), `KycGatewayException.java` (one factory
  added), `WorkspaceOrganizationResolverTest.java` (new)

Verified `OrganizationService.getOrganizationsByWorkspaceId(String)` really returns
`List<Actor>` (there is also a 3-arg paging overload returning `Page<OrganizationPageData>`;
arity keeps the Mockito stubs unambiguous). The repository query
(`findAllByWorkspaceIdAndIsWorkspaceRootActorIsTrue`) applies **no sort**, so "first" means
"first as returned" — the resolver must not reorder, and there is a test for that.

**14 tests:** first-of-many; single; no reordering; id returned verbatim (no case
normalisation); correct workspace queried; empty list → throws; **exception carries HTTP 422
and exactly `"organization_not_found"`**; null list; list containing only null; first org with
a null id; first org with a blank id; no fall-through to a later org when the first has no id;
null workspaceId; blank workspaceId.

**Deviation from the plan's code, flagged deliberately.** The plan's body is
`...stream().findFirst().orElseThrow(...).getId()`, which returns `null` if the first
organisation has a null id — and a null orgId then fails deep inside
`createCustomer` → `validateOrganizationExists` with a much worse message. My version treats a
null/blank id as "not found" and throws the same 422. It does **not** skip to the next
organisation (that would silently change which org owns the client); the no-fall-through test
pins that. Revert it if you want the plan's literal behaviour.

**Merge conflict to expect (as warned).** `organizationNotFound()` was appended at the *end*
of `KycGatewayException`'s factory block. The unmerged branch `fix/kyc-create-validation-errors`
adds `invalidLegalType()` and `unknownJurisdiction()` in the *middle* of that block
(after `invalidCompanyType()`). Placing mine last keeps the overlap to the closing brace.
Not resolved here, as instructed.

---

## Task 2 — create the client and its matter

- **Branch:** `p1/task2-client-and-matter` — **branched off `p1/task1-organization-resolver`.**
  `DocumentOrderClientService` takes `WorkspaceOrganizationResolver` as a constructor argument.
- **Commit:** `298d469f23f24aa0a7e886639eb74d007b541c9b` — `feat: a document order creates a client with one matter`
- **CI:** not obtainable. **Local, JaCoCo active: 38/38 green** across
  `DocumentOrderClientServiceTest` (24) + `WorkspaceOrganizationResolverTest` (14).
  No separate full-suite run for this branch on its own; T3's full run is a superset of it
  (T3 only modifies `DocumentOrderClientService` and its test), and that run showed zero new
  failures.
- **Files:** `DocumentOrderClientService.java`, `AggregationActorFactory.java` (both new, the
  factory is plan Step 4), `DocumentOrderClientServiceTest.java` (new)

`createFor(workspaceId, request)` resolves the org, builds the actor, and calls
`createCustomer(..., Boolean.TRUE, matterName, actor, BusinessRelationType.CLIENT)`.

**24 tests.** Happy path: returns the business-relation id; `createDefaultCase` is always
`TRUE`; relation type is `CLIENT`; matter named after the company; the ordering workspace's org
is the one resolved. Actor shape: `ENTITY` + `REST_API` + workspace-root; legal/display name;
jurisdiction and registry code on `RegisterData`; registry code filed as a `kyc.com`
`ExternalIdentifier`; no external identifier when there is no code; a blank code counts as
absent; `legalType` carried when stated. Failure paths: no organisation → 422 propagates and
`customerService` is untouched; null order rejected before anything is created; missing name;
blank name; null workspace; an exception from `createCustomer` is not swallowed.

**The no-purchase guarantee — tested explicitly, four ways, as asked:**

1. `createsTheClientOnlyThroughCreateCustomerAndNothingElse` — the exact 6-arg call, then
   `verifyNoMoreInteractions(customerService)`. Nothing else on that service is reachable.
2. `neverEnablesDocumentPurchasingOnTheCreatedActor` — the captured actor has null
   `additionalData` (so no `isDocumentPurchaseEnabled`), `isFromTransparencyRegister` false, and
   no external identifier under an `ekrn` system.
3. `doesNotDependOnTheClientCreationPathThatPurchasesDocuments` — reflection over the declared
   fields and the single constructor: the collaborator list is exactly
   `[WorkspaceOrganizationResolver, CustomerService]` and provably contains no
   `com.betterco.app.service.implementation.CustomerService`. That is the class whose
   `createClient` fires `transparenzRegisterService.executeAutoPurchase` /
   `executePurchaseProcess` and `autoKYCService.reCalculateBeneficialOwners`. This service
   cannot purchase because it cannot reach the thing that purchases.
4. `theSanctionedEntryPointHasNoPurchaseParameters` +
   `neverPassesAnEkrnBecauseTheOrderHasNoPlaceToCarryOne` — pins that
   `rest.service.CustomerService.createCustomer` has exactly the 6 parameter types and no
   purchase flag, and that `CreateKycCaseRequest` exposes no `ekrn`/`purchase` accessor at all.
   If either ever changes, these fail loudly instead of the guarantee eroding quietly.

The reflection tests filter `isSynthetic()` so JaCoCo's `$jacocoData` field does not break
them — and that was confirmed by running with instrumentation on, not reasoned about.

**Judgement calls a reviewer should check:**

- `AggregationActorFactory` sets **no** `entityStageType`. The interactive REST path
  (`CustomersApiImpl.createCustomer`) sets `EntityStageType.ENTITY_NON_REGISTERED` for
  companies. The field is `@Deprecated` on `Actor` and the plan says "minimum a customer
  needs", so I left it off. It is a one-line addition if you want parity.
- `matterName` passes `""` for a null/blank name rather than null. `createCustomer` does
  `caseName.isEmpty() ? null : caseName` — a null name would NPE there. `""` is its own
  "use the default name" value.
- `createFor` does `Objects.requireNonNull(request)`. Beyond the plan; makes a null order fail
  at the boundary instead of somewhere inside the factory.

---

## Task 3 — record the vendor reference on the matter

- **Branch:** `p1/task3-vendor-reference` — **branched off `p1/task2-client-and-matter`.**
  It modifies `DocumentOrderClientService`, which T2 creates.
- **Commit:** `93e4e4599969e4241cefb44e658e88943f2eaaab` — `feat: record the vendor case reference on the matter`
- **CI:** not obtainable. **Local, JaCoCo active: 51/51 green** (`DocumentOrderClientServiceTest`
  37 + `WorkspaceOrganizationResolverTest` 14). **Full `mvn test` on this branch: 786 tests,
  7 failures / 13 errors — identical to the clean-`dev` baseline. Zero new failures.**
- **Files:** `DocumentOrderClientService.java` (modified), `DocumentOrderClientServiceTest.java`
  (modified)

**Mandatory read done.** There are two `CaseService` classes. `rest.service.CaseService` has
`save(Case)` but **no** `findByRelation`. The plan's method pair exists only on
`com.betterco.app.service.implementation.CaseService`:
`findByRelation(String) → List<Case>` (backed by
`findAllByBusinessRelationIdOrderByCreatedAtDesc`, i.e. **newest first**) and `save(Case) → Case`.
That is the one injected. No wrapper was added.

**13 new tests.** The plan's exact test; reference lands on the first (newest) matter only and
older matters are untouched; **an existing identifier list is appended to, not replaced** —
asserted with `assertSame` on the list instance plus the original identifier still at index 0;
recording twice keeps both; **a business relation with no matter saves nothing**; a null list of
matters; a list holding only a null; null and blank relation id; null and blank vendor case id
(all no-ops that never touch `caseService`); recording never creates another client; a failure
inside `save` is not swallowed. The T2 structural test was updated to expect the third
collaborator `[WorkspaceOrganizationResolver, CustomerService, CaseService]`.

**One implementation note.** `Case` is `@Builder @NoArgsConstructor` with
`@Builder.Default externalIdentifiers = new ArrayList<>()`. Whether `new Case()` leaves that
field null depends on the Lombok version, and the plan's test constructs `new Case()`. Rather
than depend on that, `externalIdentifiersOf` creates the list only when it is null and
otherwise appends to the existing instance. Correct either way, and the append-not-replace
test pins it.

---

## Task 4 — deliberately NOT executed

Untouched, as instructed. `KycCaseLink` has no `businessRelationId`/`caseId`;
`KycGatewayService.acceptCreate`/`completeCreate` are byte-for-byte unchanged; nothing calls
`DocumentOrderClientService` yet. The three services are dead code on `dev` until a human
wires them in. For whoever picks it up, the shape of the live path is:

- `createCaseProxy` → `createInternal` → (dry-run check) → `acceptCreate`, which does
  `linkRepository.save(buildPendingLink(...))` and submits `completeCreate` to `createExecutor`.
- `completeCreate` is where the vendor's `caseCommonId` first exists — that is where
  `recordVendorReference` belongs.
- Note `retryCreate` is a second path into `completeCreate` (idempotency-key replay of a failed
  create). It must not create a second client. The plan does not mention it.

---

## Everything I could not verify

- **No CI run for any task.** Structural, not an omission — see the top section. Nobody should
  read "green" into this document.
- **Integration tests never ran.** CI's second step is `mvn failsafe:integration-test`. Not run
  locally; it needs infrastructure this machine does not have.
- **7 test classes fail on clean `dev` here**, so my "no new failures" claim is a differential
  against a red baseline, not against a green one. If CI's baseline is genuinely green, those
  7 classes are still unverified for my branches.
- **Whether `new Case()` initialises `externalIdentifiers`** was never determined. The code is
  correct either way; I did not chase the Lombok version.
- **No PR opened, nothing merged, nothing pushed to `dev`.** The four branches are on the remote
  and nothing else changed.
