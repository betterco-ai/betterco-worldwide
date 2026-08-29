# Aggregator — Phase 2, Phase 3, and the Project Plan

**Date:** 2026-08-29
**Companion to:** `2026-08-28-aggregator-phase1-design.md`
**Deadline:** Septeo go-live 1 October 2026

---

## 0. Programme overview

| Phase | What it delivers | Needed for 1 Oct |
|---|---|---|
| **1** | The aggregator exists. The platform owns the case, documents are stored with provenance, kyc.com is the only source. | **Yes** |
| **2** | More than one source behind the same aggregator, chosen by a routing table. France is source two, Britain third. | **Yes** |
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
| GB | $18.00 | Companies House — **full document route**, downloads filing PDFs free | $18 |
| DK | $18.00 | `dk_cvr_client.py` returns **data, not documents**; no route; vedtægter are paid | not a document source yet |
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
4. Britain via Companies House — the same shape as France, and its route already downloads filing
   PDFs.
5. Afterwards: Germany once the sidecar drift (D4) is resolved, and Denmark only if a data-only
   source belongs in a document aggregator at all (D5).

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

## 4. The plan, by phase

No weeks. The build is small — the connectors already exist and the Java side reuses existing
patterns — so a calendar padded into weeks misrepresents the work. What sets the pace is two gates
we do not control.

### The phases

| | Phase | Exit criterion |
|---|---|---|
| **P1** | **Client and matter.** An order creates client + `Case`; vendor ref into `externalIdentifiers`; orphan `KycCaseLink` retired. | An order produces a client with one matter in the platform. |
| **P2** | **Acquisitions and ingestion.** Per-document worker, per-source backoff, storage with provenance. | Documents land in the client before the vendor case is ready. |
| **P3** | **Contract cut-over.** Opaque `caseId`, `bettercoDocumentId`, derived status, `includePending` accepted-and-ignored. | One break, and Septeo is on the new ids. |
| **P4** | **Cost.** Charge records, `PER_CASE` for kyc.com. | Ten documents, one charge. |
| **P5** | **The aggregator becomes a router.** `SourceAdapter` port, routing table, per-source policy. | All P1–P4 tests pass unchanged; the Germany rule is enforced rather than remembered. |
| **P6** | **Sources.** France via INPI, Britain via Companies House. | A French and a British order cost nothing at the vendor and return documents. |

**Why ownership comes before the contract.** An opaque `caseId` only means something once a `Case`
owns it; shipped earlier it is an alias table over kyc.com's number, and the shape may change again
when ownership lands. Derived status has the same dependency — it is computed from acquisitions,
which arrive in P2. Building the substance first buys one contract break instead of two. Telling
Björn is decoupled from shipping: the migration note is a message, not a deploy, so it goes out on
day one and the cut-over lands at P3.

**Where the code lives.** `com.betterco.app.aggregation` exists from P1 — ownership and ingestion are
written there rather than in `integration/kyc_com` and moved later. With one source there is nothing
to route, so the aggregator only *becomes* a router at P5, which makes P5 an addition, not a refactor.

P1 through P5 are sequential. P6 is parallel per source once P5 lands.

### What actually sets the pace

Three gates, none of them our typing speed:

1. **The backend dev's review and release train.** We branch and push; they review and merge to `dev`,
   and it reaches staging on their cadence. Every phase is one PR, so this gate is hit six times.
   Note it is also the *test* gate: `app-tests.yml` only runs after an approving review, so nothing
   is verified by CI until a human has already looked at it.
2. **Septeo's own migration.** P3 changes `Long` to `String` in Björn's client, though he is told at P1. That is his work on
   his calendar, and nothing after P3 can be validated end-to-end until he has done it.
3. **The retention decision (D1).** A person, not a commit. Storing documents forces it and it
   cannot be answered by code.

The correct move is therefore to send the migration note **immediately** and start gates 2 and 3 in parallel with
building P2–P6, rather than sequencing them.

### Scope for 1 October

Everything above, including France and Britain. What stays out is not effort but unknowns:
Germany until the sidecar drift (D4) is resolved, Denmark until we decide whether a data-only
source belongs in a document aggregator at all.

## 5. Decisions, with the date each is needed

| | Decision | Needed by | Default if unanswered |
|---|---|---|---|
| D1 | Retention and deletion — **DECIDED 2026-08-29** | — | Kept indefinitely; cascaded on client deletion; reusable while fresh (`fetchedAt` < 7 days, per-source configurable) |
| D2 | Evidence level in the contract | P3, only if it rides along | Defer to phase 3; adding it later is additive |
| D3 | Do document orders count as billable client creations | P4 | Tagged by `CaseOrigin`, billing rule decided later |
| D4 | DE sidecar drift: which build is current | Only if Germany is pulled forward | DE is out of the 1 Oct path, so this can wait |
| D5 | DK needs a service built | When Denmark is picked up | Out of scope for 1 October |

## 6. Risks

| Risk | Assessment | Mitigation |
|---|---|---|
| **The gates, not the build** | The likeliest way this misses 1 October is six PR round-trips through another team's release train plus Septeo's own client change — not our coding | Send the migration note at once; start Septeo's migration and the retention decision in parallel with building P1–P6 |
| Septeo migration slips | Moderate — it is their calendar | Tell Björn on day one, agree a cut-over date in writing |
| Reuse forbidden by vendor licence (D6) | Moderate | Ask kyc.com now; if forbidden, the least-cost saving shrinks to same-customer reuse |
| CI verifies nothing before review | Certain | The job is gated on an approving review, so run the suite locally against the `dev` baseline (735 tests / 7 failures / 13 errors) and judge by *no new failures* |
| DE sidecar drift (D4) | Contained | Germany is out of the 1 October path, so the drift is not on the critical path |

## 7. The honest summary

The connectors are built. France, Britain and Germany all have working document routes, and the Java
side reuses patterns that already exist — the case, the storage, the billing strategy. The remaining
build is small and the earlier week-by-week calendar overstated it.

What is not small is the coordination: six pull requests through the backend dev's release train, and one
client change on Septeo's side that only they can make. Those are the schedule, so the migration note goes out
on day one and the two external gates open in parallel with the build.
