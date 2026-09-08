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
| Two clients can hold the same vendor document | **Unit-tested, not observed** | Vendor ids repeat across cases (35459-35463 seen twice); index fixed, scenario never fired live |
| **Storing a real registry document** | **NO** | Every sandbox file is the same 904-byte stub |
| Reading real registry documents | Yes, but read-only | HSBC case 92 on staging: 9 PDFs, 44 KB–464 KB |

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
| 1 | `bc-stg-vault` is missing `know-your-customer-com-sandbox` | Staging points at the **live** vendor; every staging order is billable. Fix branch `config/staging-kyc-sandbox` is pushed but cannot merge without the secret |
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
