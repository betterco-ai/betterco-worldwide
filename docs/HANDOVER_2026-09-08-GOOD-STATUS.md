# Handover — 8 September 2026, closing state

Current entry point. Supersedes `HANDOVER_2026-09-08.md` (overnight run) and
`HANDOVER_2026-09-06.md` (risk memo, branch hygiene — both still worth reading).

**One line: the aggregator's ingestion path is built and proven end to end on the sandbox.
It is merged nowhere and off by default. Storing a REAL registry document is still unproven.**

---

## 1. What is proven, and by what evidence

| Claim | Proven? | Evidence |
|---|---|---|
| An order creates a BetterCo client with one matter (P1) | **Yes** | Sandbox and production (case `189`) |
| Documents are listed, acquired, fetched, stored, attached to the client file | **Yes** | 8 Sep 06:40 — `Ingestion pass: 1 case(s) considered, 5 document(s) ingested`; client document area `total: 5` |
| Roles are attached functionally, not textually | **Yes** | GB `CS01` → `{REGISTERAUSZUG, GESELLSCHAFTERLISTE}`; 4 of 5 documents correctly untyped |
| Two clients can hold the same vendor document | **Yes** | 8 Sep 08:59 — 10 acquisitions, 5 per client, same vendor ids 35459-35463 under two `businessRelationId`s. Before V000098 dropped the stale index the second set could not have been inserted |
| **Storing a real registry document** | **NO** | Every sandbox file is the same 904-byte stub |
| Reading real registry documents | Yes, but read-only | HSBC case 92 on staging: 9 PDFs, 44 KB–464 KB |

All ten stored documents are the same 904-byte sandbox stub. What is proven is the **pipeline**;
what is unproven is that it can carry a real registry PDF.

**The gap that matters: nothing has ever stored a real file.** Reading real ones works; ingesting
one does not have a single data point. That needs a production-pointed instance, and the one
production case we own (`189`) is blocked by its missing `businessRelationId` (§4).

## 2. Poll cadence — fixed, and still only half-evidenced

A sandbox case was `Ready` **40 seconds** after the order; BetterCo still said "Initializing Case"
52 minutes later. Nothing was broken — the poll policy's first offset was `PT1H`. Now:

```
PT1M, PT5M, PT15M, PT1H, PT6H, PT12H, PT24H
```

Offsets are cumulative from the order, so the dense front costs three cheap reads and the long
tail is unchanged.

**Open question, honestly stated.** The only production timing we have is case `189`: still
building after 4½ hours. There is **no measured fast production case** — the front of the curve is
justified by the sandbox and by internal testing, not by customer evidence. If real cases cluster
around twenty minutes, the middle of the curve (`PT15M` → `PT1H` → `PT6H`) is too sparse. Revisit
once production ordering volume exists.

## 3. Branch state — needs a decision before review

`test/kyc-stack-on-dev` is **22 commits ahead of `dev`, 0 behind**, and there are ~24 remote
branches in the stack. That is far too much to put in front of one reviewer.

**Recommendation: squash the P2 branches into one reviewable change before opening PRs.** The
per-task branches were right for an unattended overnight run — one build per task, each revertable
— but they are the wrong unit for review. The commit messages carry the reasoning and should be
preserved in the squashed message.

The user asked to keep PRs open; nothing has been merged or deleted.

## 4. Open items that need a person

| | Item | Why it is blocked |
|---|---|---|
| 1 | **The vendor config fails OPEN into the paying environment** | See §6 — this is the item with a live cost attached, and it is bigger than the missing staging secret |
| 2 | Case `189` has no `businessRelationId` on its `kycCaseLink` | Client, matter and vendor ref are all correct — only the back-reference is absent. Blocks the real-document proof. Run 2 log greps are specified but not run |
| 3 | Vendor email drafted in Gmail, **not sent** | Asks KYC.com for sandbox files with real bytes, which would close §1's gap without spending money |
| 4 | Role vocabulary not agreed | M4 exposes `kind` to Septeo; changing it after go-live is a breaking contract change |
| 5 | Owners for `BLOCKED` and `"Create incomplete"` | Both are states a human must resolve; no queue, no alert, no owner |
| 6 | Deleting a client orphans its documents | Contradicts D1. Deliberately **not** fixed — the asymmetry looks intentional and a document delete is irreversible. Wants a ticket |
| 7 | `kyc-com.user.base-url` is production-only in every profile | A sandbox instance asks the production user portal about sandbox cases and gets `200` with nothing. Worked around in the worker; the config is still wrong |
| 8 | **BCP-8429** — `UploadData`'s inverted validation | Filed. Not ours; sits under every uploader in the codebase |

## 5. What remains for the MVP

`M3` (BetterCo owns the document) is **complete**. Outstanding: **M4** the contract cut-over,
**M5** turning `document-search.create-client` on beyond `development`, **M6** the Germany
deny-guard, and **M2**'s second half (the vendor-target switcher plus item 1 above).

Deadline for Septeo/STP is **1 October**.

## 6. The vendor configuration fails open — ranked first

`application.properties` defaults to the **live** vendor:

```
:179  kyc-com.base-url = https://api.knowyourcustomer.com
:182  kyc-com.secret   = know-your-customer-com
```

Sandbox is an *override* (`development:35/38`, `staging:61/70`). Production correctly inherits.
So any environment whose profile does not load gets the live vendor.

**Measured, 8 September:** `bc-dev-vault-dev` holds the production secret `know-your-customer-com`
— that is how Run 2 authenticated when it ordered case `189`. So a dev jar started without
`-Dspring.profiles.active=development` does not fail. It resolves the live base URL, finds the live
secret in its own vault, authenticates, and places **real billable orders silently**.

This inverts the earlier ranking of the two environments:

| | Failure mode | Cost |
|---|---|---|
| Staging (`know-your-customer-com-sandbox` absent from `bc-stg-vault`) | Loud, lazy, per call | **Zero** — it fails before spending |
| Dev (live secret present, live default) | **Silent success** | Real orders |

Staging's missing secret is the *safe* failure. Dev is the dangerous one, because it fails
successfully. The staging risk only becomes real if someone "fixes" it by pointing staging at the
production secret — which would give staging dev's exact failure mode.

**Recommended, in order:**

1. **A startup assertion** — refuse to start when the resolved base URL is production while the
   active profile is `development` or `staging`. It can only ever block a configuration that would
   have spent money, so it is safe in both directions. Small, and the right first move.
2. **Invert the default** — sandbox in `application.properties`, production opted into explicitly
   in `application-production.properties`. Correct in shape, but **NOT yet verified safe**: nobody
   has confirmed that production actually runs with `spring.profiles.active=production`. If it does
   not, this silently points the paying environment at the sandbox. **Confirm before touching.**

Neither is built. Both need a deploy to validate, and neither should be guessed at.

## 7. How this should reach a reviewer

**One PR from `test/kyc-stack-on-dev` into `dev`, all 22 commits preserved.**

The ~24 branches are an artefact of how the run was executed — one build per task so each was
separately revertable. They are not how the change should be read. But the *commits* are the
record: N9 through N13 each exist because deploying found something unit tests structurally could
not, and squashing them would flatten exactly the reasoning a reviewer needs. Drop the branches,
keep the commits.
