# P1 — Client and Matter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A document-search order creates a BetterCo client with one matter, and records the vendor's case reference on that matter — so ordered documents land in the platform instead of beside it.

**Architecture:** A new `com.betterco.app.aggregation` package owns the order-to-client path. It resolves the workspace's organisation, calls the existing REST `CustomerService.createCustomer(...)` with `createDefaultCase=true`, and writes the vendor reference into `Case.externalIdentifiers`. `KycGatewayService` calls into it at create time; nothing else changes. The package exists from this task so that later routing work is an addition, not a refactor.

**Tech Stack:** Java 17, Spring Boot 2.7.5, MongoDB (Spring Data + Mongock), JUnit 5 + Mockito, Maven (`./mvnw`).

**Spec:** `docs/superpowers/specs/2026-08-28-aggregator-phase1-design.md` and `docs/superpowers/specs/2026-08-29-aggregator-phase2-and-plan.md`

## Global Constraints

- Repository: `betterco-backend`. Branch off `dev`, one branch per task, PR reviewed by the backend dev. **Never push to `dev` directly.**
- **Nothing compiles locally** — no Maven, no `~/.m2`, `.mvn/` untracked. CI (`.github/workflows/app-tests.yml`, `mvn -B test`) is the only verification. Never claim a test passes without a CI run.
- Reuse, do not reimplement: `CustomerService.createCustomer(...)` is the only sanctioned way to create a client with a matter.
- **`purchaseDocuments` stays false and `ekrn` stays null** on any client we create. `CustomerService.createClient` triggers Transparenzregister purchasing and `autoKYCService.reCalculateBeneficialOwners` when they are set — a French document order must never trigger a German paid purchase.
- The hierarchy is `workspace → organization → clients → matters → processes`. Take the **first** organisation of the workspace.
- Do not change the public contract in this task. Ids stay as they are until P3.

---

## File Structure

| File | Responsibility |
|---|---|
| `src/main/java/com/betterco/app/aggregation/WorkspaceOrganizationResolver.java` | Resolve the organisation a workspace's API orders belong to |
| `src/main/java/com/betterco/app/aggregation/DocumentOrderClientService.java` | Create the client + matter for one order and record the vendor reference |
| `src/main/java/com/betterco/app/domain/KycCaseLink.java` | Gains `businessRelationId` and `caseId` |
| `src/main/java/com/betterco/app/integration/kyc_com/KycGatewayService.java` | Calls the aggregation service when a create is accepted |
| `src/test/java/com/betterco/app/aggregation/WorkspaceOrganizationResolverTest.java` | Unit tests for resolution and the no-organisation case |
| `src/test/java/com/betterco/app/aggregation/DocumentOrderClientServiceTest.java` | Unit tests for creation, the vendor reference, and the no-purchase guarantee |
| `src/test/java/com/betterco/app/integration/kyc_com/KycGatewayServiceTest.java` | Extended: an accepted create produces a client |

---

### Task 0: Fixtures — how an entity Actor is built

**Files:**
- Read: `src/main/java/com/betterco/app/domain/actor/Actor.java`, `src/main/java/com/betterco/app/rest/service/CustomerService.java:267-305`
- Create: `src/test/java/com/betterco/app/aggregation/AggregationFixtures.java`

**Interfaces:**
- Produces: `AggregationFixtures.entityActor(String name, String jurisdiction, String externalCode)` returning `Actor`, and `AggregationFixtures.organization(String id)` returning `Actor`.

- [ ] **Step 1: Read the two files above** and note the exact `Actor` builder fields for a company (name, type/entity flag, workspace, external identifiers). Do not guess — the builder is the contract every later task depends on.

- [ ] **Step 2: Write the fixture helper** using only fields that exist on `Actor`. Keep it to the minimum a customer needs: display name, entity type, and the workspace.

- [ ] **Step 3: Commit**

```bash
git checkout -b p1/task0-fixtures
git add src/test/java/com/betterco/app/aggregation/AggregationFixtures.java
git commit -m "test: fixtures for aggregation client creation"
```

---

### Task 1: Resolve the workspace's organisation

**Files:**
- Create: `src/main/java/com/betterco/app/aggregation/WorkspaceOrganizationResolver.java`
- Test: `src/test/java/com/betterco/app/aggregation/WorkspaceOrganizationResolverTest.java`

**Interfaces:**
- Consumes: `OrganizationService.getOrganizationsByWorkspaceId(String workspaceId)` returning `List<Actor>`.
- Produces: `WorkspaceOrganizationResolver.resolve(String workspaceId)` returning `String` (the organisation's id); throws `KycGatewayException.organizationNotFound()` when the workspace has none.

- [ ] **Step 1: Write the failing tests**

```java
@ExtendWith(MockitoExtension.class)
class WorkspaceOrganizationResolverTest {

  @Mock private OrganizationService organizationService;
  private WorkspaceOrganizationResolver resolver;

  @BeforeEach
  void setUp() {
    resolver = new WorkspaceOrganizationResolver(organizationService);
  }

  @Test
  void resolvesTheFirstOrganizationOfTheWorkspace() {
    when(organizationService.getOrganizationsByWorkspaceId("ws1"))
        .thenReturn(List.of(AggregationFixtures.organization("org1"),
                            AggregationFixtures.organization("org2")));

    assertEquals("org1", resolver.resolve("ws1"));
  }

  @Test
  void workspaceWithoutOrganization_throws() {
    when(organizationService.getOrganizationsByWorkspaceId("ws1")).thenReturn(List.of());

    KycGatewayException ex = assertThrows(KycGatewayException.class, () -> resolver.resolve("ws1"));
    assertEquals("organization_not_found", ex.getMessage());
  }
}
```

- [ ] **Step 2: Run the tests and watch them fail**

Push the branch; CI runs `mvn -B test`. Expected: compilation failure — `WorkspaceOrganizationResolver` does not exist.

- [ ] **Step 3: Add the exception factory**

In `src/main/java/com/betterco/app/infrastructure/exception/KycGatewayException.java`, beside the existing factories:

```java
  public static KycGatewayException organizationNotFound() {
    return new KycGatewayException(HttpStatus.UNPROCESSABLE_ENTITY, "organization_not_found");
  }
```

- [ ] **Step 4: Write the implementation**

```java
package com.betterco.app.aggregation;

import com.betterco.app.infrastructure.exception.KycGatewayException;
import com.betterco.app.rest.service.OrganizationService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

/**
 * An API order carries a workspace but no user, so the organisation that owns the
 * resulting client is the workspace's first organisation.
 */
@Component
@RequiredArgsConstructor
public class WorkspaceOrganizationResolver {

  private final OrganizationService organizationService;

  public String resolve(String workspaceId) {
    return organizationService.getOrganizationsByWorkspaceId(workspaceId).stream()
        .findFirst()
        .orElseThrow(KycGatewayException::organizationNotFound)
        .getId();
  }
}
```

- [ ] **Step 5: Push and confirm CI is green**

- [ ] **Step 6: Commit and open the PR**

```bash
git add src/main/java/com/betterco/app/aggregation/WorkspaceOrganizationResolver.java \
        src/main/java/com/betterco/app/infrastructure/exception/KycGatewayException.java \
        src/test/java/com/betterco/app/aggregation/WorkspaceOrganizationResolverTest.java
git commit -m "feat: resolve the organisation that owns an API-created client"
```

---

### Task 2: Create the client and its matter

**Files:**
- Create: `src/main/java/com/betterco/app/aggregation/DocumentOrderClientService.java`
- Test: `src/test/java/com/betterco/app/aggregation/DocumentOrderClientServiceTest.java`

**Interfaces:**
- Consumes: `WorkspaceOrganizationResolver.resolve(String)`; `CustomerService.createCustomer(String workspaceId, String orgId, Boolean createDefaultCase, String caseName, Actor customerActor, BusinessRelationType relationType)` returning the customer id.
- Produces: `DocumentOrderClientService.createFor(String workspaceId, CreateKycCaseRequest request)` returning `String` — the created customer's `businessRelationId`.

- [ ] **Step 1: Write the failing tests**

```java
@ExtendWith(MockitoExtension.class)
class DocumentOrderClientServiceTest {

  @Mock private WorkspaceOrganizationResolver organizationResolver;
  @Mock private CustomerService customerService;
  private DocumentOrderClientService service;

  @BeforeEach
  void setUp() {
    service = new DocumentOrderClientService(organizationResolver, customerService);
  }

  private CreateKycCaseRequest order() {
    return new CreateKycCaseRequest().jurisdiction("FR").name("ACME SARL").externalCode("552100554");
  }

  @Test
  void createsAClientWithADefaultMatterInTheWorkspaceOrganization() {
    when(organizationResolver.resolve("ws1")).thenReturn("org1");
    when(customerService.createCustomer(eq("ws1"), eq("org1"), eq(Boolean.TRUE),
        anyString(), any(Actor.class), any())).thenReturn("br1");

    assertEquals("br1", service.createFor("ws1", order()));
  }

  @Test
  void namesTheMatterAfterTheCompany() {
    when(organizationResolver.resolve("ws1")).thenReturn("org1");
    ArgumentCaptor<String> caseName = ArgumentCaptor.forClass(String.class);
    when(customerService.createCustomer(any(), any(), any(), caseName.capture(), any(), any()))
        .thenReturn("br1");

    service.createFor("ws1", order());

    assertTrue(caseName.getValue().contains("ACME SARL"));
  }
}
```

- [ ] **Step 2: Push and watch the tests fail** — `DocumentOrderClientService` does not exist.

- [ ] **Step 3: Write the implementation**

```java
package com.betterco.app.aggregation;

import com.betterco.app.domain.actor.Actor;
import com.betterco.app.domain.enums.BusinessRelationType;
import com.betterco.app.rest.generated.domain.CreateKycCaseRequest;
import com.betterco.app.rest.service.CustomerService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Turns one document-search order into a BetterCo client with a single matter.
 *
 * Deliberately routed through CustomerService.createCustomer so the client is
 * indistinguishable from any other. purchaseDocuments/ekrn are never set here:
 * that path triggers Transparenzregister purchasing and beneficial-owner
 * recalculation, which must not fire because someone ordered a French extract.
 */
@Service
@RequiredArgsConstructor
public class DocumentOrderClientService {

  private final WorkspaceOrganizationResolver organizationResolver;
  private final CustomerService customerService;

  public String createFor(String workspaceId, CreateKycCaseRequest request) {
    String orgId = organizationResolver.resolve(workspaceId);
    Actor customerActor = toActor(workspaceId, request);
    return customerService.createCustomer(
        workspaceId, orgId, Boolean.TRUE, request.getName(), customerActor, BusinessRelationType.CLIENT);
  }

  private Actor toActor(String workspaceId, CreateKycCaseRequest request) {
    // built with the Actor builder established in Task 0
    return AggregationActorFactory.entityActor(workspaceId, request);
  }
}
```

- [ ] **Step 4: Extract the actor construction** into `AggregationActorFactory` (same package), using exactly the `Actor` fields confirmed in Task 0, carrying the company name, the jurisdiction and the registry code.

- [ ] **Step 5: Push and confirm CI is green**

- [ ] **Step 6: Commit**

```bash
git add src/main/java/com/betterco/app/aggregation/ src/test/java/com/betterco/app/aggregation/
git commit -m "feat: a document order creates a client with one matter"
```

---

### Task 3: Record the vendor reference on the matter

**Files:**
- Modify: `src/main/java/com/betterco/app/aggregation/DocumentOrderClientService.java`
- Test: `src/test/java/com/betterco/app/aggregation/DocumentOrderClientServiceTest.java`

**Interfaces:**
- Produces: `DocumentOrderClientService.recordVendorReference(String businessRelationId, String vendorCaseId)` — writes an `ExternalIdentifier` onto the matter.

- [ ] **Step 1: Write the failing test**

```java
  @Test
  void recordsTheVendorCaseIdOnTheMatter() {
    Case matter = new Case();
    when(caseService.findByRelation("br1")).thenReturn(List.of(matter));

    service.recordVendorReference("br1", "8842137");

    assertTrue(matter.getExternalIdentifiers().stream()
        .anyMatch(id -> "8842137".equals(id.getExternalId()) && "kyc.com".equals(id.getSystem())));
    verify(caseService).save(matter);
  }
```

- [ ] **Step 2: Push and watch it fail.**

- [ ] **Step 3: Implement**

```java
  public void recordVendorReference(String businessRelationId, String vendorCaseId) {
    caseService.findByRelation(businessRelationId).stream().findFirst().ifPresent(matter -> {
      matter.getExternalIdentifiers().add(ExternalIdentifier.builder()
          .externalId(vendorCaseId)
          .system(VENDOR_KYC_COM)
          .build());
      caseService.save(matter);
    });
  }
```

Check `CaseService` for the exact save method name before writing this; if it differs, use the real one rather than adding a wrapper.

- [ ] **Step 4: Push, confirm CI green, commit**

```bash
git commit -am "feat: record the vendor case reference on the matter"
```

---

### Task 4: Wire it into the create path

**Files:**
- Modify: `src/main/java/com/betterco/app/integration/kyc_com/KycGatewayService.java` (`acceptCreate`, `completeCreate`)
- Modify: `src/main/java/com/betterco/app/domain/KycCaseLink.java`
- Test: `src/test/java/com/betterco/app/integration/kyc_com/KycGatewayServiceTest.java`

**Interfaces:**
- Consumes: `DocumentOrderClientService.createFor(...)`, `.recordVendorReference(...)`.
- Produces: `KycCaseLink.businessRelationId` and `KycCaseLink.caseId`, both `String`.

- [ ] **Step 1: Write the failing test** — extend the existing suite, whose fixtures and mocking style are already established there.

```java
  @Test
  void acceptedCreate_createsAClientAndLinksIt() {
    when(referenceService.jurisdictions()).thenReturn(jurisdictions());
    when(documentOrderClientService.createFor(eq(WS), any())).thenReturn("br1");
    service = createEnabledService();

    service.createCaseProxy(WS, req(DE));

    ArgumentCaptor<KycCaseLink> saved = ArgumentCaptor.forClass(KycCaseLink.class);
    verify(linkRepository).save(saved.capture());
    assertEquals("br1", saved.getValue().getBusinessRelationId());
  }
```

- [ ] **Step 2: Push and watch it fail.**

- [ ] **Step 3: Add the two fields** to `KycCaseLink` (`businessRelationId`, `caseId`) and set them in `buildPendingLink`.

- [ ] **Step 4: Call the aggregation service** from `acceptCreate`, before `linkRepository.save(...)`, and call `recordVendorReference` from `completeCreate` once the vendor's `caseCommonId` is known.

- [ ] **Step 5: Push, confirm CI green, commit and open the PR**

```bash
git commit -am "feat: link every document order to its client and matter"
```

---

## Self-review notes

- **Spec coverage:** this plan implements P1 only — client, matter, vendor reference. Ingestion (P2), the contract cut-over (P3), cost (P4), routing (P5) and additional sources (P6) each get their own plan.
- **Deliberately not here:** `KycCaseLink` is extended rather than deleted. It is retired in P3, when the contract stops exposing the vendor id and there is a replacement for everything it still carries.
- **Two reads the implementer must do before writing code:** the `Actor` builder (Task 0) and `CaseService`'s save/find methods (Task 3). Both are named at the step that needs them; nothing in this plan invents a field name.
