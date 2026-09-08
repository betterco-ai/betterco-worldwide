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

## 3. Branch state

`test/kyc-stack-on-dev` is **22 commits ahead of `dev`, 0 behind**. That is the number that matters:
the window for a conflict-free merge is open now and closes on its own.

An earlier draft of this document recommended pruning the ~24 branches in the stack before review.
**Withdrawn.** The repository has **461 remote branches**; branch count is invisible noise here and
tidying ours would change nothing for anyone. The merge shape is in §7.


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
| 9 | **Per-artefact vendor cost is not recorded** | D4 says explicitly: instrument now, decide the commercial model later, because unrecorded cost is unrecoverable. It was not done. Every order placed until it is cannot be attributed afterwards. **Cheapest item here, and the only one that loses data by waiting** |
| 10 | **`contentDate` is never populated** | The field is declared on `DocumentAcquisition` and read by `DocumentIngestor`, and nothing writes it — so the second clock is always null and D1's reuse policy reads only the fetch date. That is precisely the trap §5 of the architecture memo was written to prevent, and the field's existence makes it easy to miss |

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

## 7. How this reaches a reviewer

**OPEN: https://github.com/betterco-ai/betterco-backend/pull/2305** — `test/kyc-stack-on-dev` -> `dev`,
to be squash-merged.

**The repo squash-merges.** P1 landed as `93ef2291e Test/p1 on dev (#2293)` - one commit, PR number
in the title - and every recent commit on `dev` has that shape. So "preserve the 22 commits on dev"
is not an option we control; GitHub's squash setting collapses them regardless. The commits stay
readable **in the PR**, permanently, which is where the reasoning actually lives. Same bargain every
other PR in this repo has made.

Merge now rather than after more proving, because:

- the branch is **0 behind `dev`** today, and drift already forced a rebuild once this week;
- `dev`-the-environment is already running this code - the branch is the fiction, not the deploy;
- the risky surface is small and the rest is flag-gated off.

**What makes 22 commits reviewable is the PR description.** State the blast radius explicitly:

| Surface | Reviewer's attention |
|---|---|
| `KycGatewayService` (+195), `KycComUserClient` (+57), `V000097`, `V000098`, 8 lines in `KycApiImpl` / `CustomerService` | **Everything.** Not flag-gated - changes behaviour for anyone using kyc.com today |
| the `aggregation` package + `document-roles.json` | Additive. `aggregation.ingestion.enabled=false` everywhere; nothing runs until someone flips it |

**A two-PR split is not cleanly available**: `SourcePollPolicies` lives in the aggregation package
and `KycGatewayService` depends on it, so carving out "just the fixes" means refactoring for review
convenience. Not worth it.

**Keep out of this PR:**

1. **Flag flips** - `aggregation.ingestion.enabled`, `document-search.create-client`. Own PRs, one
   environment at a time, each revertable alone.
2. **`config/staging-kyc-sandbox`** - must not merge until `know-your-customer-com-sandbox` exists in
   `bc-stg-vault`, or staging starts clean and then fails every call.
3. **`fix/kyc-create-validation-errors`** - one commit, never compiled locally, sitting since
   27 August. Build it or close it; do not let it drift into a third state.

## 8. Documentation state

- `ARCHITECTURE_AGGREGATION_2026-07-28.md` now carries a **§9 reality check** recording where the
  implementation diverged from the memo: built in Java rather than Python, polling rather than
  webhooks with §7's step 2 skipped, and the §6 requirements that are not built (cost, OCR, content
  date, licence obligations). D1 and D3 are marked decided; D2 remains open and blocking.
- The `DocumentRole` vocabulary in code is a **role** vocabulary. It is orthogonal to D2's
  **evidence levels** (`data` / `document` / `certified`) and does not settle that decision — a
  conflation worth guarding against, since both look like "what kind of document is this".
