# Aggregator — audit against the target, and the MVP cut

**Date:** 5 September 2026 · **Deadline:** Septeo go-live 1 October 2026

**Supersedes the scope claim in** `2026-08-29-aggregator-phase2-and-plan.md` §4 ("all six phases,
France and Britain included"). That is no longer credible; see §3.

---

## 1. The target, stated so it can be audited

Agreed 2026-08-28: **platform → aggregator → source.** BetterCo is the system of record; a client
with one matter *is* the case; sources differ only in billing model and backoff; kyc.com is source
one. In terms of what Septeo can observe, the target is five statements:

1. Björn calls BetterCo, never kyc.com.
2. He is handed **BetterCo** identifiers.
3. The document lands in a **BetterCo client file**.
4. **BetterCo holds the bytes.**
5. We can change the source underneath without him noticing.

## 2. Audit — what is true on 5 September

Everything in this table was measured this week against the running systems, not recalled.

| # | Target property | Today | Evidence |
|---|---|---|---|
| 1 | Client + one matter per order | **Built, dev only** | Order on dev 4 Sep: client `6a9acdb2…`, exactly one matter, vendor ref filed |
| 2 | Vendor reference kept internal | **Done** | `externalIdentifiers [{1000005421, kyc.com}]` on the matter |
| 3 | Documents stored with provenance | **Not built** | `downloadUrl` is our proxy; bytes stream from the vendor per request; no acquisition record, no cost record |
| 4 | BetterCo identifiers in the contract | **Not done** | `caseCommonId` is still the vendor's `Long`; two document id spaces; `includePending` still meaningful |
| 5 | Status you can trust | **Broken everywhere** | F1: `ready` true at creation, stored status frozen. Dev still shows `Initializing Case` while the vendor says `Ready` |
| 6 | Cost per case | **Not built** | No charge record; `PER_CASE` vs `PER_DOCUMENT` unmodelled |
| 7 | Source is swappable | **Not built** | One source hardwired; no port, no routing table |
| 8 | Second source (FR, GB) | **Not reachable** | Connectors exist in python; the Java path has no sidecar adapter |
| 9 | Environments | **Only dev carries P1** | `document-search.create-client=true` exists solely in `application-development.properties` |
| 10 | Staging safe to test on | **No** | GB/LIMITED on stg returns 200 rows of real Companies House data — staging still orders from the LIVE vendor, billable |
| 11 | Operational resilience | **Weak** | Flat 5-minute polling, no backoff, no give-up; `scope=account` returns 400; no webhooks |

### What this adds up to

**Of the five target statements, one and a half hold.** Björn can call BetterCo and get a document
(1 ✓) — that is the passthrough, and it predates this programme. The order now produces a client
with a matter (3 ✓ **on dev only**). He still receives the vendor's identifiers (2 ✗), we still do
not hold the bytes (4 ✗), and the source cannot be changed underneath him (5 ✗).

**The most consequential gap is #3 and #4 together.** Without stored documents the platform is a
shim; without our own identifiers, every later change breaks Septeo's client again.

**The most dangerous item is #10**, because it is not a gap in the build — it is a live invitation
to spend money. Anyone told to "test on staging" places real orders at $18–$88 each.

## 3. Why the old scope no longer fits

The 29 August plan put all six phases, France and Britain included, before 1 October. Three things
say otherwise, and none of them is coding speed:

- **P2 alone is ten tasks** and it has not started. Today is 5 September.
- **Every phase is one pull request through another team's review train**, and CI verifies nothing
  until a human has approved. Six phases is six round-trips we do not control. Decided 5 Sep: we
  **keep the PRs open** rather than wait on merges — which unblocks the build but pushes the
  integration risk to the end (see §7).
- **Septeo's own migration** sits between us and any end-to-end validation of the new contract.

Carrying FR and GB inside the deadline hides the real risk instead of managing it.

## 4. The MVP — what must close before 1 October

The MVP is exactly the promise *"order through BetterCo, and BetterCo owns the result"*. Six items,
roughly five pull requests.

| | Item | Why it is MVP | State |
|---|---|---|---|
| **M1** | **F1 — status truthfulness** plus the backfill of frozen links | A consumer polling `ready` gets nonsense, and nothing downstream can derive status from data that never updates | **Committed locally**, unmerged |
| **M2** | **A vendor-target switcher.** One setting per environment selects `sandbox` or `production`, moving base-url, token-url and secret name together; `create-enabled` stays a second, independent dial | Decided 5 Sep: dev and staging must be switchable, BetterCo production always uses kyc.com production. The two dials together give exactly "read production freely, create only with permission" | First dial built 6 Sep (`kyc-com.target`, PR #2296); still **blocked on one missing secret** in `bc-stg-vault` |
| **M3** | **P2 core**: acquisition record, store the bytes, serve from our storage, cascade on client deletion, bounded polling | This is target statement 4, and the only thing that makes an audit trail real | Not started |
| **M4** | **P3 contract cut-over**: opaque `caseId`, one document id space, derived status, `includePending` accepted-and-ignored | Target statement 2. Must land **before** Björn builds against the vendor ids, or he migrates twice | Not started; the note to him is already agreed |
| **M5** | **Turn `document-search.create-client` on beyond development** | P1 is invisible to every environment a customer touches until this flips | One line of config per profile |
| **M6** | **Germany deny-guard** | Without the routing table the aggregator would buy German documents from kyc.com, against standing policy. A deny rule is small; the routing table is not | Not started |

**Deliberately trimmed out of P2 for the MVP:** cross-customer reuse (see B4) and the per-source
policy registry beyond a single bounded schedule.

### M2 in detail — the switcher, and the landmine under it

Two dials, not one:

| Dial | Values | What it decides |
|---|---|---|
| `kyc-com.target` | `sandbox` \| `production` | Which vendor world we read and write. Resolves base-url, token-url and secret name as a set, so they cannot drift apart |
| `kyc-com.create-enabled` | `true` \| `false` | Whether billable orders are allowed at all |

`production` + `create-enabled=false` is the configuration that makes the 19 October trial expiry a
non-event: we read real cases on the live vendor for free, and a new case needs someone to turn the
second dial on.

**Two facts measured on 5 September that this depends on:**

- **`bc-stg-vault` does not contain `know-your-customer-com-sandbox`.** `bc-dev-vault-dev` and
  `bc-app-vault` both do. The merged `application-staging.properties` already names that secret, and
  `KycComOAuthClient` resolves it **lazily, on the first token request** — so the next routine
  deploy of `dev` to staging starts cleanly and then fails every document-search call with
  `IllegalStateException`. **Add the secret to `bc-stg-vault` before that deploy**, not after.
- **Case ids do not cross vendor worlds.** A sandbox `caseCommonId` does not exist in production.
  Any environment that switches target renders its stored links unreadable unless each link records
  the target that produced it. The acquisition record in M3 already carries `source`; it must carry
  **source *and* target** (`kyc.com:sandbox` vs `kyc.com:production`), and reads must ignore links
  whose target is not the current one. This is a one-field decision that is expensive to retrofit.

## 5. Beyond the MVP

In the order that pays:

| | Item | Why it waits |
|---|---|---|
| **B1** | **France via INPI**, then Britain via Companies House | Pure margin — $88 per French case, $18 per British one. Invisible to Septeo, which is why it can follow the go-live |
| **B2** | **Routing table and the `SourceAdapter` port** | Prerequisite for doing B1 properly; M6's deny-guard holds the line until then |
| **B3** | **Cost and charge records** | Internal accounting, reconstructable from the acquisition records M3 creates |
| **B4** | **Reuse of stock across customers** | Policy decided 5 Sep: reuse **only where we can prove the document has not changed at the source** — no new version. Still blocked on the vendor licence question |
| **B5** | **Webhooks replace polling**; retire the kyc.com Java exception | Housekeeping; polling works |
| **B6** | **Ordering UI in the app**; live monitoring / re-KYC | Today only STP and our internal tool can order |

## 6. What only a person can decide

| | Decision | Blocks | Needed by |
|---|---|---|---|
| **S1** | Sandbox trial expiry (19 Oct) | — | **Answered 5 Sep: after it lapses we test on production.** Reads against existing production cases are free and possible today; creating a new case needs permission. Delivered by M2's two dials |
| **S2** | Vendor target for dev and staging | — | **Answered 5 Sep: a switcher.** BetterCo production always uses kyc.com production |
| **S3** | Merge slots in the release train | — | **Answered 5 Sep: keep the PRs open.** We stack branches and let the backend dev merge on their cadence — see §7 for what that costs us |
| **D6** | May a document bought for one customer be served to another? | B4, and the least-cost thesis | **Our policy answered 5 Sep** (only with proof of no change). The **vendor licence question is still unasked** — our willingness is not their permission |
| **D3** | Do document orders count as billable client creations? | B3 | With the cost work |

### What "prove it has not changed" costs, by source

The reuse rule is stricter than D1's seven-day clock, and it lands differently per source:

| Source | Free way to ask "is there a newer version?" | Consequence |
|---|---|---|
| Companies House (GB) | Yes — filing history is public and free | Reuse is cheap and safe |
| INPI (FR) | Yes — filing/acte listing | Reuse is cheap and safe |
| kyc.com | **Not known to exist.** Its change product is Live Monitoring, and each review is billed as a fresh case | Reuse may be uneconomic exactly where documents cost the most |

So the clock becomes a cheap pre-filter and the change check is the gate — and the rule quietly
strengthens the case for **B1 and B2**: direct registry sources are not only cheaper per fetch, they
are the only ones where a bought document can be reused at all.

## 7. The honest summary

P1 is real and proven, but it is switched on in exactly one environment nobody outside the team
uses. Everything a customer would call the aggregator for — our identifiers, our stored documents, a
status that updates — is still ahead of us, and the calendar to 1 October holds about five pull
requests through a queue we do not control.

The recommendation is to **cut France and Britain out of the go-live**, ship the six MVP items, and
give Septeo one migration date instead of two. What those two sources save is real, but it is
margin, not the promise.

**What stacking open PRs costs, stated plainly.** Building ahead of merges is the right call — it
keeps us off someone else's cadence — but it moves risk rather than removing it. Each branch is cut
from the last, so `dev` moving underneath us means rebases; nothing is verified by CI until a human
approves; and the MVP items have a required merge order (M1 before the bounded polling it depends
on, M3 before M4, since derived status is computed from acquisitions). The mitigations are to keep
running the local suite against a fresh `dev` baseline, to state the merge order in every PR body,
and to re-verify on dev after each merge rather than assuming the stack still applies.
