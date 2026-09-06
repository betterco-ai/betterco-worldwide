# Roadmap to the first billable order

**Date:** 6 September 2026 · **Companion to** `AUDIT_AND_MVP_2026-09-05.md`

A billable order is the only thing that proves the live path, and the only thing that cannot be
undone. This is the order of work that makes it a controlled step instead of a leap — plus the
design decision agreed today, which has to land before we spend anything.

---

## 1. Why a billable order is eventually unavoidable

The sandbox cannot prove three things, and all three are the product:

- **Real documents.** Every sandbox PDF is the same 904-byte stub. We have never retrieved a real
  registry document through our own stack.
- **Real coverage and timings.** Sandbox fixtures are five GB companies. Nothing about French,
  Luxembourgish or Danish behaviour is exercised.
- **Real vendor semantics under load** — how long a case actually takes, what a partial result looks
  like, what happens when a jurisdiction returns nothing.

So the question is not whether, but **what must be true first** so that the money buys evidence
rather than a lesson.

## 2. The decision agreed 6 September — record the vendor target

**Every case link and every acquisition records which vendor world produced it.** Not inferred, not
retrofitted.

### Why it is not optional

Measured on the Hetzner box (`178.104.137.27:8080`) the same day: its workspace holds exactly one
case, `1000005319`, created against the **sandbox** in August. The instance now points at the
**live** vendor, and asking it for that case returns `HTTP 400 "Api Error"` — the id does not exist
in that world. The case is unreadable, and nothing in the row says why.

That is today, with one link and no switcher. The moment dev or staging can be flipped between
worlds — which is M2 in the audit, and what we agreed to build — every stored case in that
environment inherits the same failure.

### The shape

| Field | On | Values |
|---|---|---|
| `vendorTarget` | `KycCaseLink` | `PRODUCTION` \| `SANDBOX` \| `null` (legacy, unknown) |
| `source` + target | `DocumentAcquisition` (P2) | `kyc.com:production`, `kyc.com:sandbox`, later `inpi`, `companies-house` |

Not to be confused with P2's `SourceRefSpace`, which says which *document id space* a reference came
from (pending-numeric vs ready-string). Different axis, both needed.

### The rules

1. **Written at creation** from the active configuration — `buildPendingLink` and `completeCreate`.
2. **The poller only touches links whose target matches the current one**, plus `null` ones (below).
3. **Legacy rows are not guessed.** A `null` target is probed **once**. If the vendor answers, the
   target is stamped with the current one. If it rejects the id as unknown (the `400 Api Error` /
   `404` shape), the link is marked as belonging to another world and **never polled again**.
4. **A foreign link is still listed**, with an honest status rather than an error — it is a real
   case someone paid for, just not readable from here. *(Rules 1-3 shipped in PR #2296; rule 4
   changes an API response shape, so it was deferred to the contract cut-over — see R2 in §3.)*

Rule 3 is what makes this self-healing: no migration has to guess where a historical case came from,
and the noise problem below solves itself.

### It also fixes a problem the F1 fix would otherwise create

`V000097` un-freezes stale links and hands them to the poller. On a box holding foreign case ids —
exactly the Hetzner situation — that means hitting the vendor with an unknown id **every five
minutes, forever**, one warning per pass. Rule 3 retires those links after a single probe. This is
the cheaper of the two options put forward yesterday, and it is strictly better than waiting for
P2's give-up point to mop it up.

## 3. The sequence

Each step is one pull request. Sizes are honest estimates, not padding.

| | Step | Why it precedes the order | Size |
|---|---|---|---|
| **R1** | **F1 — status truthfulness** (**PR #2294**, open) | You cannot tell when a paid case is finished if its status never updates | Built, tests green, awaiting review |
| **R2** | **Vendor target on `KycCaseLink`** — write on create, filter the poller, probe-once for legacy | §2. Also retires the polling noise R1 introduces | **Built 6 Sep — PR #2296**, stacked on #2294. Reporting a foreign case honestly through the *API* was deferred to the contract cut-over |
| **R3** | **Prove idempotency, do not assume it** — a retried create with the same `idempotencyKey` must return the same case and **not** order twice | This is the difference between one charge and two, and it has never been tested against a vendor that actually bills | Test-first; code only if it fails |
| **R4** | **P2 core — storage and acquisition records**, carrying source *and* target from the first commit | Without it we pay for a document that exists only at the vendor: no copy, no audit trail, no record it existed | Large — the real work |
| **R5** | **Cost visibility, minimal** — every order records what was ordered, on which target, when, and the expected price band | So the first live order can be reconciled against an invoice | Small, falls out of R4 |

**R1 → R2 → R3 can run this week.** R4 is the substance and the schedule risk; R5 rides on it.

## 4. The checklist for the order itself

Run in this order, and stop at the first surprise.

1. **Confirm the world.** `…/document-search/cases/search?jurisdiction=GB&query=LIMITED` — hundreds
   of real rows means production. (Five fixtures with `CROPWELL BISHOP CREAMERY LIMITED` means you
   are on the sandbox and the test proves nothing new.)
2. **Confirm the target is recorded** — order one case on the *sandbox* first and check the link
   carries `vendorTarget: SANDBOX`. If that does not work, stop; R2 is not really deployed.
3. **Pick the cheapest useful jurisdiction.** GB at $18 exercises the full path — search, order,
   documents, download — for a fifth of the French price. Save FR for when the path is proven.
4. **Flip `create-enabled` deliberately**, order **one** case, and flip it back. Record the
   `idempotencyKey` used.
5. **Verify, in this order:** the case reaches `Ready`; a client with exactly one matter exists; the
   matter carries the vendor reference; the documents list; **each document downloads as a real PDF
   of plausible size** — not 904 bytes; and after R4, that the bytes are served from our storage.
6. **Reconcile** the charge against the expected price band within the billing cycle.

## 5. What we still owe the vendor conversation

Independent of the code, and none of it blocks R1–R3:

- **The sandbox trial expires 19 October.** Agreed 5 September: after that we test against
  production, reads free, creates by permission. Worth telling kyc.com anyway — an extension costs
  nothing to ask for.
- **The licence question (D6)** — may a document bought for one customer be served to another? Our
  own policy is decided (only with proof the document has not changed); their contract has never
  been asked.
- **Whether a free "has anything changed?" check exists** for a case or document. If it does not,
  reuse is uneconomic on this vendor and the least-cost thesis rests on going direct.

## 6. The honest summary

The first billable order should buy one thing: proof that a real document reaches a BetterCo client
file and stays there. Today it would buy a stub-free PDF we do not keep, attached to a case whose
status never updates, in a world we do not record. R1 through R4 turn that same $18 into evidence.
