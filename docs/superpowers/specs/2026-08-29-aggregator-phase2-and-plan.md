# Aggregator — Phase 2, Phase 3, and the Project Plan

**Date:** 2026-08-29
**Companion to:** `2026-08-28-aggregator-phase1-design.md`
**Deadline:** Septeo go-live 1 October 2026 — 4½ working weeks from today

---

## 0. Programme overview

| Phase | What it delivers | Needed for 1 Oct |
|---|---|---|
| **1** | The aggregator exists. The platform owns the case, documents are stored with provenance, kyc.com is the only source. | **Yes** |
| **2** | More than one source behind the same aggregator, chosen by a routing table. France is source two. | **Yes, scoped to FR** |
| **3** | The aggregator *decides* rather than looks up: evidence levels, least-cost routing, reuse of stock. | No |
| **4** | Housekeeping: webhooks replace polling, the kyc.com Java exception is retired, ordering UI in the app. | No |

Phases 1 and 2 make sources **interchangeable**. Phase 3 makes the choice between them **intelligent**.
That distinction is why phase 3 is real work and not a wish-list, and also why it can wait.

## 1. Phase 2 — a second source

### 1.1 What it adds

1. **A `SourceAdapter` port**, extracted from two working implementations rather than guessed — the
   kyc.com Java client and the FastAPI sidecar. Operations: `search`, `availableDocuments`,
   `retrieve` (→ acquisition), `pollAcquisition`.
2. **A routing table**: `(jurisdiction, document kind) → ordered list of sources`. Static and
   deterministic in phase 2; phase 3 is what makes it a decision.
3. **A sidecar transport adapter** — HTTP over loopback to `127.0.0.1:8090`, shared-secret auth,
   the contract already briefed in `api/INTEGRATION.md`.
4. **Per-source policy for the new sources** — charging model `PER_DOCUMENT`, and a backoff policy
   of *none* for synchronous sources such as INPI.

Phase 1's domain model is unchanged. A second source adds rows to a routing table and one adapter;
it does not touch the case, the acquisition, or the contract STP sees. That is the test of whether
phase 1 was designed correctly.

### 1.2 Which source is second — measured, not assumed

Prices are one case in each market, measured on staging 2026-08-29:

| Market | kyc.com price | Direct route today | Saving per case |
|---|---|---|---|
| **FR** | **$88.00** (High) | INPI + Datainfogreffe, routers live in `api/main.py` | **$88** |
| IT | $43.50 | none | — |
| GB | $18.00 | Companies House, router live | $18 |
| DK | $18.00 | `dk_cvr_client.py` — **library only, no route** | $18, after a service is built |
| DE | $18.00 | HR sidecar | policy: we never buy DE from kyc.com |

**France is source two.** It is the most expensive market we buy (five times GB or DK), it is first
on Septeo's own priority list, and its route already exists behind FastAPI with no known drift.

**Germany is *not* in the 1 October path.** Björn's opening mail states the requirement: *"we would
like to find and download registration documents for companies outside of Germany."* DE matters for
our own product, not for this go-live. This corrects the ordering asserted in the phase-1 spec §2,
which put DE first.

> **Policy leak worth naming.** DE *is* present in kyc.com's jurisdiction list at $18, so after
> phase 1 the aggregator would happily buy German documents from kyc.com — against the standing rule
> that we source DE ourselves. Until the routing table exists, that rule is remembered rather than
> enforced. The table is the fix.

### 1.3 Sequence within phase 2

1. Extract the port; kyc.com becomes adapter one with **no behaviour change** (tests prove it).
2. Add the routing table with a single rule: everything → kyc.com. Still no behaviour change.
3. Add the sidecar adapter and FR as source two; route FR document kinds to INPI, everything else
   unchanged.
4. Then, in priority order and *after* go-live: DE (needs decision D4 resolved), GB, DK (needs a
   service built first).

## 2. Phase 3 — the decision layer

Phases 1 and 2 leave a static table. Phase 3 replaces the lookup with a decision, and it is where
the aggregation thesis actually pays:

- **Evidence levels** — `data` / `document` / `certified`. A Datainfogreffe statement is not a Kbis
  substitute; without the level, "cheapest source" is a meaningless instruction.
- **Least-cost routing** — the cheapest source *that meets the required evidence level*, with the
  bundle awareness that kyc.com is charged per case while an INPI acte is a bundle.
- **Reuse of stock** — do not fetch what we already hold fresh. Needs the freshness policy, and both
  clocks phase 1 stores: `fetchedAt` and `contentDate`.
- **Per-case cost reporting** — phase 1 instruments the meter; phase 3 is where anyone can read it.

Not required for 1 October. A static routing table is correct, just not clever.

## 3. Phase 4 — housekeeping

Named so it is not mistaken for phase 3, and so it does not quietly attach itself to the deadline:

- Replace polling with the kyc.com v2 webhooks (`CaseReady`, `DocumentUploaded`) — the backend has
  no webhook endpoint today; the client methods exist only in python.
- Retire the kyc.com Java exception, so every source reaches the aggregator through one shape.
- Ordering UI in the BetterCo app — today only STP and our internal tool can order.
- Resolve the DE sidecar drift permanently (see D4).

## 4. Project plan

Four and a half working weeks. One work package per branch, CI-verified, reviewed by Jappware.

### Week 1 — 1 to 5 September · the contract

| # | Activity | Depends on | Done when |
|---|---|---|---|
| A1 | Freeze the contract: opaque `caseId`, `bettercoDocumentId`, derived status, `includePending` accepted-and-ignored | — | PR merged, spec §5 matches the code |
| A2 | Send Björn the migration note: `Long` → `String`, agree a cut-over date | A1 | Written confirmation from Septeo |
| A3 | Schema: `DocumentAcquisition`, charge record, new `CaseOrigin` value | — | Migration written, indexes in place |

**Week 1 is the immovable one.** Björn is integrating now; the contract must land before his polling
loop ships, or STP migrates twice.

### Week 2 — 8 to 12 September · ownership and ingestion

| # | Activity | Depends on | Done when |
|---|---|---|---|
| A4 | An order creates client + `Case`, vendor ref into `externalIdentifiers`; orphan `KycCaseLink` retired | A3 | Integration test: order → client exists with the documents attached |
| A5 | Ingestion worker: per-document, store via `FileStorage`, write acquisitions | A3, A4 | Documents appear in storage before case-ready |
| A6 | Per-source backoff policy replacing the flat 5-minute poll | A5 | kyc.com runs 1h/6h/12h/24h; give-up flags |

### Week 3 — 15 to 19 September · serving and cost

| # | Activity | Depends on | Done when |
|---|---|---|---|
| A7 | Content served from our storage, with fetch-store-serve fallback | A5 | No vendor call on a second download |
| A8 | Charge records; `PER_CASE` model for kyc.com | A3, A5 | One charge per (case, source), ten documents free |
| A9 | Phase 1 end-to-end on staging; Septeo migrates against it | A1–A8 | Björn's integration green on the new ids |

### Week 4 — 22 to 26 September · the second source

| # | Activity | Depends on | Done when |
|---|---|---|---|
| A10 | Extract `SourceAdapter`; kyc.com becomes adapter one | A9 | All phase-1 tests pass unchanged |
| A11 | Routing table `(jurisdiction, kind) → source`, per-source policy | A10 | DE rule enforced, not remembered |
| A12 | Sidecar adapter + **France via INPI** as source two, `PER_DOCUMENT` | A11 | A French order costs €0 at the vendor and returns a document |

### Week 5 — 29 September to 1 October · hardening

| # | Activity | Depends on | Done when |
|---|---|---|---|
| A13 | Retention implemented (decision D1), monitoring, cost sanity check | A8 | Retention job runs; per-case cost readable |
| A14 | Go-live checks with Septeo | all | Sign-off |

Only **three days** of buffer. See §6.

## 5. Decisions, with the date each is needed

| | Decision | Needed by | Default if unanswered |
|---|---|---|---|
| D1 | Document retention and deletion | Week 5 (A13) | Keep indefinitely — **not acceptable**, must be answered |
| D2 | Evidence level in the contract | Week 1 (A1) if it rides along | Defer to phase 3; adding it later is additive |
| D3 | Do document orders count as billable client creations | Week 3 (A8) | Tagged by `CaseOrigin`, billing rule decided later |
| D4 | DE sidecar drift: which build is current | Week 4 only if DE is pulled forward | DE is out of the 1 Oct path, so this can wait |
| D5 | DK needs a service built | Post go-live | Out of scope for 1 October |

## 6. Risks

| Risk | Assessment | Mitigation |
|---|---|---|
| **Phase 2 at full scope does not fit** | Near-certain. DE + FR + GB + DK behind a new port in one week is not a five-day job. | Scope phase 2 for 1 October to **France only**. One second source proves the abstraction; the rest follow after go-live. |
| Three days of buffer | Real | Phase 1 is independently shippable at end of week 3; France can drop without endangering the go-live |
| No local build | Certain | Every step is a branch, CI is the verification, no local claims |
| STP migration slips | Moderate | A2 in week 1, cut-over date agreed in writing |
| Retention unanswered at week 5 | Moderate | D1 escalated now, not in week 5 |

## 7. The honest summary

Phase 1 and **France** are achievable by 1 October. Phase 2 as originally described — every direct
route — is not, and saying so now is cheaper than discovering it on 26 September. Germany, Great
Britain and Denmark are the first work after go-live, and none of them is on Septeo's critical path.
