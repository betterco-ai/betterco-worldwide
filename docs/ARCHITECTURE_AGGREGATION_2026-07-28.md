# Least-cost aggregation architecture — BetterCo as the system of record

*Design memo, 2026-07-28. Supersedes nothing; complements `CONNECTOR_FINDINGS_2026-07-28.md`
(measured vendor facts) and `curation/document_kinds_routing.json` (the decision table).*

---

## 1. The invariant

**BetterCo is the system of record. No consumer talks to a vendor.**

```
vendors ──▶ [aggregator: route · fetch · OCR · provenance] ──▶ BetterCo case ──▶ consumers (STP)
                                                                    ▲
                                                       the only externally readable source
```

This is write-through ingestion, not a pass-through proxy. STP becomes a pure read path over
BetterCo and cannot reach a vendor, because it is never given a vendor address. That is what
makes vendor-neutrality **enforceable** rather than merely intended — a proxy would leak the
vendor's shape and semantics into the consumer contract, and the neutrality would erode with
the first special case.

Consequences that follow directly and are not optional:

* The **case** is the unit of record. Documents and data hang off it, with provenance.
* Vendor identity is an internal implementation detail. It may appear in provenance metadata;
  it must never appear in a consumer-facing field name, path, id or status vocabulary.
* Adding a vendor must be invisible to consumers. If adding one requires a consumer change,
  the boundary is in the wrong place.

---

## 2. Layers

Existing pieces stay untouched. The new work is a `sourcing/` package in
`betterco_claude_api`, alongside the vendor clients.

| Layer | Responsibility | State |
|---|---|---|
| Vendor clients | one module per vendor, no knowledge of each other | **done** — 7 clients |
| `sourcing/router.py` | `(jurisdiction, legalForm, kind, evidence_level)` → candidate vendors | to build |
| `sourcing/planner.py` | case stock + freshness + bundling → what is *actually* fetched, priced up front | to build |
| `sourcing/fetchers.py` | thin adapters onto the vendor clients | to build |
| `sourcing/ingest.py` | OCR, provenance, `create_case` → `create_process` → `upload_process_document` | to build |
| `sourcing/state.py` | order lifecycle incl. the manual queue | to build |
| BetterCo client | case/document persistence | **done** — `betterco_client.py` |

The router reads `curation/document_kinds_routing.json` (446 routes) — it does not
re-implement the decision. One source of truth; a second one would drift.

---

## 3. Where least cost actually comes from

Vendor price is the **smallest** of the three levers. In order of impact:

### 3.1 Do not fetch at all — the dominant saving

If the case already holds the document and it is fresh enough, the cost is zero regardless of
vendor. A Kbis "not older than 3 months" is the normal requirement, not an exception. Every
request must therefore consult the case stock **before** routing.

### 3.2 Bundle awareness

Two real cases, both measured:

* **kyc.com is `case_level`.** Base documents arrive with the case. Ordering them
  individually from another vendor is paying twice for the same paper.
* **An INPI acte is a bundle.** One PDF can contain the procès-verbal *and* the updated
  statuts. A single fetch can satisfy several `doc_kinds`; the planner must recognise that
  instead of issuing one fetch per kind.

### 3.3 Vendor price — last, and mostly already decided

Per document kind there is usually exactly one vendor. Measured prices:

| Vendor | Model | Cost |
|---|---|---|
| handelsregister.de | document | free |
| INPI RNE | document | free |
| Companies House | document | free |
| DataInfogreffe | document | 3,00 €HT (shareholder statement) |
| Infogreffe (Kbis) | document, **manual portal** | 3,06 € TTC + 85 €HT/yr subscription |
| kyc.com | **case** | per case; base docs included, additional on request |

**Hard constraint: kyc.com's scope excludes Germany.** DE is served by our own connectors.

---

## 4. The gate that must sit above least cost: evidence level

Sources are **not** substitutes for one another. A DataInfogreffe shareholder statement
(3,00 €, greffe-headed, **no seal, no "certifié conforme"**) and a Kbis (3,06 €, sealed by
the greffier) are not the same instrument. PSC data is not a shareholder list.

The router must therefore resolve **"the cheapest source that meets the required evidence
level"**, never "the cheapest source". The level is supplied by the caller; it is never
inferred. Without this gate, least-cost silently degrades into *legally unusable but cheap*,
and nobody notices until a bank rejects a file.

Proposed levels — the routing table already carries the inputs (`completeness`,
`dataBackup.isProof`, `flags`):

| Level | Meaning | Examples |
|---|---|---|
| `data` | a fact, no document. Never evidence. | PSC JSON, kyc.com structured shareholders, DataInfogreffe JSON |
| `document` | a genuine filed document, unsealed | INPI acte, Companies House filing image, DataInfogreffe PDF |
| `certified` | issued and sealed by the registry authority | Kbis, German AD, certified extracts |

**Apostille is an attribute, not a fourth level.** It is post-processing applied to a
`certified` document (see the existing `apostille` skill), not a different source. Modelling
it as a level would force every route to be duplicated.

Practical effect: if STP asks for a `GESELLSCHAFTERLISTE` at `certified` in France, the answer
is *unavailable* — not "here is the 3 € statement". At `document` the statement is the right
answer. Same input, different resolution; that difference must be explicit.

---

## 5. Freshness: two clocks, not one

Every stored document has **two** dates and they answer different questions:

* **Fetch date** — when we retrieved it. Answers "how stale is our copy?"
* **Content date** — what the document is *as of*. Answers "how stale is the fact?"

They diverge sharply. A DataInfogreffe statement fetched today can carry a 2019 `Depot` date,
because it reflects the last deposited act. A freshness rule that looks only at the fetch date
would call that document current. Both must be stored and both must be evaluated.

**The check is cheaper than the document — exploit that.** For the free vendors, asking
"is there anything newer?" costs nothing:

* Companies House — `filing_history` is free
* INPI — `/companies/{siren}/attachments` is free
* handelsregister.de — a search is free

So for those, prefer an **event check** over a time-based TTL: refetch only when a newer
filing exists. Time-based TTL is the fallback for sources where checking costs the same as
fetching (Infogreffe/Kbis) or where the document is a point-in-time attestation whose value
*is* its issue date (again the Kbis).

Recommended starting policy — see §8, this is a business decision:

| Kind | Rule | Rationale |
|---|---|---|
| Register extract / Kbis | TTL **3 months** | matches what banks and notaries demand |
| Articles / statuts | **event-based**, free check | rarely change, but a superseded version is *wrong*, not merely stale |
| Shareholder list | event-based **plus** surface the content date | the content date is the fact users must judge |
| Accounts | event-based, annual cadence | new filing ⇒ refetch |

---

## 6. What the design forces

**Asynchronous, not request/response.** The Kbis is a human portal order. handelsregister.de
can hit a captcha. kyc.com delivers case documents over time. A synchronous call cannot model
this. The case needs states:

```
required → ordered → delivered → stored
              ↓          ↓
           failed    manual_queue     (the Kbis path is a legitimate branch, not an error)
```

**kyc.com webhooks are the delivery signal.** `CaseReady` and `DocumentUploaded` already exist
in `kyc_com_client.py` (`subscribe_webhook`, `WEBHOOK_EVENTS`). Wiring them is what replaces
polling, and it is what tells the aggregator when to ingest. This was already an open item; in
this architecture it becomes load-bearing.

**Provenance is captured at write time, never reconstructed.** The INPI reuse licence (art.
2.4) requires stating the source **and the date of last update**. That is knowable at fetch
and unknowable afterwards. Same for DataInfogreffe's `Depot`. Provenance must be written in
the same operation as the document, or it is lost.

Minimum provenance record per stored artefact: vendor, endpoint, fetch timestamp, content
date, source reference (`numNat` / `barcode` / `Depot` no.), evidence level, cost incurred,
licence obligations attaching to it.

**OCR once, at ingestion.** INPI actes and Companies House filings are **scans with no text
layer** (measured: 0 text characters across 15 and 43 pages respectively). If every consumer
OCRs, the same page is recognised repeatedly. OCR at ingestion; store the text as an artefact
beside the PDF.

---

## 7. Step 1 — put BetterCo in front of the live kyc.com/STP integration

STP retrieves documents from kyc.com **today, in production**. Step 1 is to redirect those
calls to BetterCo without changing what STP receives, then replicate the pattern for the other
vendors.

This is the right first move: it is a **strangler**, proving the consumer contract against a
vendor that already works, rather than building the whole aggregator and migrating STP onto an
untested surface. One unknown at a time.

```
before:  STP ──────────────▶ kyc.com
after:   STP ──▶ BetterCo ──▶ kyc.com          (then: ──▶ + 6 more vendors, invisibly)
```

### The decision that determines whether step 2 is cheap or expensive

**Does BetterCo's API mirror kyc.com's shape, or is it vendor-neutral?**

Mirroring is tempting — STP would barely have to change. It is the wrong choice. It bakes one
vendor's vocabulary (`caseCommonId`, its status names, its document ids) into our public
contract, and every later vendor has to be forced through a shape it does not fit. Worse, STP
would have to migrate **twice**: once to the mirror, once to the real API.

**Recommendation: define the vendor-neutral contract now and migrate STP once.** STP is a
customer; a contract change needs coordination, a version and a migration window regardless.
Spend that once.

Neutral surface, roughly:

```
POST /cases                     {jurisdiction, legalForm, identifiers, required_kinds, evidence_level}
GET  /cases/{id}                status + per-kind state
GET  /cases/{id}/documents      list with provenance, evidence level, both dates
GET  /cases/{id}/documents/{d}  the file, served from BetterCo
```

No vendor name anywhere in path, field or status vocabulary.

### Open questions for step 1

* **Case ownership and identity.** BetterCo creates and owns the kyc.com case and mirrors it
  as a BetterCo case. STP references the BetterCo id only. Needs an id mapping table.
* **Migration window.** STP runs against kyc.com today. Both paths must work simultaneously
  until STP has cut over — with reconciliation, so we can prove BetterCo returns the same
  documents before the direct route is switched off.
* **Retention and data protection.** BetterCo now stores customer documents that previously
  only transited. Retention period and deletion path must be settled before go-live.
* **Cost attribution.** Once BetterCo places the orders, the vendor bill arrives at BetterCo,
  not at STP. Per-case cost must be recorded to bill it on.

### Sequence

1. Freeze the neutral contract (above) with STP.
2. Wire `CaseReady` / `DocumentUploaded` → ingestion. Removes polling; prerequisite for
   everything asynchronous.
3. Ingestion path: kyc.com case → BetterCo case, documents + provenance + OCR.
4. Read path: STP endpoints served **from BetterCo**, never live from the vendor.
5. Run both in parallel and reconcile. Cut over. Retire the direct route.
6. **Only then** add vendors behind the unchanged contract: DE (handelsregister), FR (INPI +
   DataInfogreffe), UK (Companies House). Each one is invisible to STP — which is the proof
   the boundary is right.

---

## 8. Decision register

*Framing confirmed as sound 2026-07-28. The recommendations stand; the values are still open.*

Each entry states what is actually being decided, why it cannot be decided technically, and
what happens if it is decided late.

### D1 — Freshness policy

**Being decided:** when may a stored document be reused instead of refetched?

**Why it is not a technical call:** it is an assertion about what age *your customers* accept.
Engineering can enforce any number; it cannot know which number is defensible to a bank.

**The trap:** there are **two clocks** (§5). A DataInfogreffe statement fetched today carried a
`Depot` date of **2019** — measured, not hypothetical. A rule reading only the fetch date calls
that document current. Store and evaluate both dates.

**The lever:** for Companies House, INPI and handelsregister.de the *check* ("is there anything
newer?") is **free**. Prefer event-based refresh there and reserve time-based TTL for sources
where checking costs as much as fetching (Kbis), or where the issue date *is* the value (Kbis
again).

**Recommendation:** the table in §5 — Kbis TTL 3 months; articles/statuts, shareholder list and
accounts event-based, with the content date surfaced.

**Cost of deciding late:** low. The policy is configuration, and until it exists the safe
default is "always refetch" — correct, merely expensive.

### D2 — Evidence levels

**Being decided:** may the router substitute a cheaper source, and where is the line?

**Why it is not a technical call:** it is a legal-sufficiency judgement per use case.

**The concrete test:** STP asks for a French `GESELLSCHAFTERLISTE`.
* at `certified` → the answer is **"unavailable"**, *not* "here is the 3 € statement"
* at `document` → the 3 € DataInfogreffe statement **is** the right answer

Same request, different resolution. The difference must be explicit in the contract, because
the two artefacts are not the same instrument: the statement is greffe-headed but carries **no
seal and no "certifié conforme"**.

**Recommendation:** `data` / `document` / `certified`. Apostille is an **attribute** of a
`certified` document, not a fourth level — as a level it would duplicate every route.

**Open specifically:** must STP distinguish `document` from `certified`? Given the jurisdiction
list (JP, KW, SG, HK, IL …) and the existing `apostille` skill, almost certainly yes.

**Cost of deciding late: HIGH.** This field belongs in the consumer contract from day one.
Retrofitting it is a breaking change for a customer who has already migrated — and the whole
point of step 1 is that STP migrates exactly once. **Decide before the contract is frozen.**

### D3 — Retention

**Being decided:** how long does BetterCo keep vendor documents, and who may delete them?

**Why it arises now:** documents that previously only transited STP↔kyc.com are now *stored*
by us. That is a new data-protection posture, not a technical detail.

**Cost of deciding late:** medium — it must be settled before go-live, not before build.

### D4 — Cost pass-through

**Being decided:** is per-case vendor cost re-billed, and at what granularity?

**Why it arises now:** once BetterCo places the orders, the vendor invoice arrives at BetterCo
rather than at STP. Whatever the billing model, per-case cost has to be *recorded* at ingestion
— it cannot be reconstructed from a monthly vendor invoice.

**Recommendation:** record cost per artefact in the provenance record (§6) regardless of the
billing decision. That keeps the option open at no cost.

**Cost of deciding late:** low for billing, **high for instrumentation** — unrecorded cost is
unrecoverable. Instrument now, decide the commercial model later.

---

# 9. Reality check — 2026-09-08

*Appended six weeks later, after P1 and P2 were built and deployed. The memo above is left as
written; this section records where the implementation diverged from it and why. Where the two
disagree, **this section is what exists**.*

## 9.1 The layer table in §2 is wrong about the language and the repository

§2 planned a `sourcing/` package in `betterco_claude_api` (Python), alongside the vendor clients.
**It was built in the Java backend instead**, as `com.betterco.app.aggregation` in
`betterco-backend`.

That was not a considered architectural decision — it followed from step 1 (§7). Redirecting the
live kyc.com/STP route meant touching the service that already serves that route, and that service
is Java. A Python sidecar would have needed the Java backend to call it on the request path for
every document read: a network hop and a second deployment in front of a customer-facing endpoint.

| §2 planned | What exists |
|---|---|
| `sourcing/router.py` | not built — routing is still one vendor |
| `sourcing/planner.py` | not built |
| `sourcing/fetchers.py` | `DocumentIngestor` (fetch, store, attach, record) |
| `sourcing/ingest.py` | `DocumentIngestionWorker` |
| `sourcing/state.py` | `DocumentAcquisition` + `AcquisitionStatus` |

The Python provider sidecars (DE/FR/DK) still exist and are unaffected. What this changes is that
**the aggregator's system of record is Mongo in the Java backend**, not a Python service.

## 9.2 Polling was built, not webhooks — and §7's sequence was not followed

§6 called webhooks "the delivery signal", and §7 made wiring `CaseReady` / `DocumentUploaded`
step 2, a prerequisite for everything asynchronous. **Step 2 was skipped.** Ingestion (step 3) was
built on **polling** with a cumulative backoff (`SourcePollPolicy`), currently
`PT1M, PT5M, PT15M, PT1H, PT6H, PT12H, PT24H`.

Two measurements drove this, and both undercut the webhook premise:

- **Documents arrive during the build, not at the end.** Production case 189 had seven downloadable
  documents at 50% complete and was still not ready four hours later. A `CaseReady` webhook would
  have delayed ingestion until well after documents were already available.
- **The spread is enormous.** A sandbox case was Ready 40 seconds after the order; case 189 was
  still building after 4.5 hours.

So the worker is driven by the **document list**, never by case-ready. Webhooks remain the right end
state — polling is a cost paid per case — but they are now an optimisation rather than a
prerequisite. §6's claim that wiring them "is what replaces polling, and it is what tells the
aggregator when to ingest" is superseded: what tells the aggregator when to ingest is the document
list.

## 9.3 What §6 required and is NOT built

| §6 requirement | State |
|---|---|
| Provenance: vendor, endpoint, fetch timestamp, source reference, evidence level | **partial** — `source`, `vendorTarget`, `sourceRef`, `sourceRefSpace`, `fetchedAt`, `vendorName`, `vendorCategory` recorded. Endpoint and evidence level are not |
| **Cost incurred per artefact** | **NOT built.** No cost field exists |
| Content date (the second clock, §5) | **modelled but never populated.** `DocumentAcquisition.contentDate` is declared and read by `DocumentIngestor`; nothing ever writes it, so it is always null — and the stored document's `documentDate` is always null with it |
| OCR once, at ingestion | **NOT built.** Documents are stored as delivered |
| Licence obligations attaching to the artefact | **NOT built** |

Two deserve emphasis, because the memo predicted the consequence:

**Cost.** D4 says "unrecorded cost is unrecoverable. Instrument now, decide the commercial model
later" — and the instrumentation was not done. Every order placed between now and the fix is a case
whose vendor cost cannot be attributed afterwards. It is the cheapest item on this list to build and
the only one that loses data permanently by waiting.

**The second clock.** §5 and D1 both warn that a rule reading only the fetch date will call a 2019
document current. `contentDate` exists in the schema, which makes the gap easy to miss — the field
is there, it is simply never assigned. The reuse policy decided under D1 therefore reads **only**
the fetch clock, which is exactly the trap §5 was written to prevent.

## 9.4 Decision register: what has been settled since

- **D1 (freshness) — DECIDED.** Documents are kept for ever; deletion cascades when the client is
  deleted; a stored document is reused while `fetchedAt` is under 7 days old. **Caveat:** that is a
  time-based TTL reading one clock, which §5 recommends against and §9.3 explains is currently
  unavoidable. The event-based check the memo prefers is not built.
- **D2 (evidence levels) — STILL OPEN, and now on the critical path.** M4 exposes a document `kind`
  to Septeo, and the memo rates deciding late as **HIGH** cost because it is a breaking change for a
  customer who has already migrated. A partial vocabulary now exists in code as `DocumentRole`
  (`REGISTERAUSZUG`, `GESELLSCHAFTERLISTE`, `GESELLSCHAFTSVERTRAG`), driven by a hand-authored
  curation of 218 rows. **That is a role vocabulary, not an evidence level** — the two are
  orthogonal, and D2 is untouched by it.
- **D3 (retention) — DECIDED** with D1: kept for ever, cascade on client delete. One contradiction
  is open: deleting a client currently orphans its documents rather than deleting them.
- **D4 (cost pass-through) — instrumentation NOT done.** See §9.3.

## 9.5 What of the memo still stands

Unchanged and still correct: the invariant in §1 (BetterCo is the system of record; no consumer
talks to a vendor), the vendor-neutral contract in §7 and the reasoning against mirroring kyc.com's
shape, the evidence-level gate in §4, the two-clock analysis in §5, and the decision-register
framing in §8. Nothing measured since has contradicted any of them.

**Status against §7's sequence:** step 1's ingestion half is built and proven on the sandbox
(PR #2305), and **the neutral contract of §7 is now built** on `p3/contract-cutover` — opaque case
id, one document id space, derived status, `includePending` accepted and ignored. The memo's
recommendation was followed: the contract is vendor-neutral rather than a mirror of kyc.com's
shape, so Septeo migrates once.

Two qualifications. The contract is built but **not frozen and not communicated** — the note to
Septeo has not been sent, and until it is, "migrates once" is an intention rather than a fact. And
**D2's evidence level is not in it**, which the memo rates as HIGH cost to add late for exactly the
reason that applies here: retrofitting a field into a contract a customer has already migrated onto
is a second break. If it is going in, it goes in before this freezes.

Steps 4-6 — read path served from BetterCo, parallel running with reconciliation, cut-over, then
additional vendors behind the unchanged contract — are not started.
