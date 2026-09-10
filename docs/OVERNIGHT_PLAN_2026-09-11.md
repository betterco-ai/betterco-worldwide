# Overnight plan — 11 September 2026 (P5: catch up with dev, then reuse + flag)

**For an unattended, looped session.** Read §2 (rules) before §3 (tasks). One task per branch, tests
first, commit, push. No PRs, no merges into `dev`, no deploys, no money. Go-live is **1 October**.

Predecessor: `OVERNIGHT_PLAN_2026-09-09.md` (all six tasks done). Current entry point for state:
`HANDOVER_2026-09-09.md`; `HANDOVER_2026-09-08-P3.md` still holds the P3 contract and the §5 open list.

Scope was chosen by the user on 11 September: **T1–T4 plus the Septeo draft (T5). No full suite —
Docker will not be running.**

---

## 1. Where we are, measured 11 September

| | State |
|---|---|
| P1 client + matter | merged into `dev` (#2293), live |
| P2 + P3 | `test/kyc-stack-on-dev`, PR **#2305 is a draft and stays one**; P3 verified on dev 8081 |
| P4 (O2–O6) | five branches stacked on that, all pushed, **none merged**, no PRs |
| Shared checkout | was on `p4/o6-germany-deny-guard` @ `06c840e1f`, clean but for untracked `graphify-out/` |
| **Drift** | the stack is now **3 commits behind `origin/dev`** (it was 0 at the start of the P4 round) |
| §5 open items | 13; four need a person, the rest are code or data |

Tonight: absorb the drift, then close the two remaining *code-able* items (D1 reuse window, M5 flag)
and the one *data* item (price bands), and leave a Septeo note ready for a person to send.

## 2. Rules for the unattended session

**Work in a dedicated worktree.** The checkout at `2601_Claude/betterco-backend/betterco-backend` is
shared with ~32 other Claude contexts; branch-switching there is not safe.

**It already exists** — created 11 September at `C:/bcwt/p5-overnight`, on `p4/o6-germany-deny-guard`
@ `06c840e1f`. Adding it required parking the shared checkout back on `dev` first, because a branch
cannot be checked out in two worktrees at once; the shared tree was clean apart from an untracked
`graphify-out/`. Note that the shared tree's local `dev` is **10 commits behind `origin/dev`** —
always merge `origin/dev`, never the local ref. Tear the worktree down at the **end** of the round
(`git worktree remove C:/bcwt/p5-overnight`), not at the start of the next one.
**Assert HEAD before every task** — never assume the branch you left is the branch you find.

**Hard stops — never do these without a person:**

- **No billable calls.** No `POST …/document-search/cases`, on any host, ever. Reads on production
  are free; creating a case is not.
- **No deploys**, no workflow dispatches, no restarting anything on the Hetzner box.
- **No merging into `dev`**, no PRs, no marking #2305 ready, no deleting branches, no force-pushes.
- **Do not send anything** — not to Septeo, not to the vendor. T5 produces a draft only.
- **Do not "fix" `application-development.properties:52`** (the unguarded `${AZURE_USER_USERNAME}`),
  do not point staging at the production secret, and **do not invert the vendor-config default**.
  All three are §5 items that need a person.
- **No changes to `fix/kyc-create-validation-errors`** — it is kept deliberately.

**Method:**

- One task per branch, each branched from the previous task's branch, keeping the stack ordered
  behind `test/kyc-stack-on-dev`.
- **Tests first.** Where the change is a fix, prove the test fails against the unfixed code before
  fixing it. Where the code is new, say so plainly rather than dressing a compile error up as
  red-green.
- Build with the local Maven and its populated repo. Both were verified to exist on 11 September:

  ```
  M="C:/Users/unzer/AppData/Local/Temp/claude/C--Users-unzer-Dropbox-02-4Ventures-04-4V-Projects-2104-Founders1-07-Projects-2601-Claude-betterco-worldwide/4399718c-9344-4d71-8df8-e23bd0de46db/scratchpad"
  "$M/apache-maven-3.9.9/bin/mvn" -o -B -Dmaven.repo.local="$M/m2repo" -Djacoco.skip=true test
  ```

- **Run the affected packages only** (`integration.kyc_com`, `aggregation`). **Docker is NOT running
  tonight**, so 14 `MongoTestContainer` classes would die as `ExceptionInInitializerError` — which
  reads nothing like a Docker problem. Do not attempt a full-suite baseline and do not quote the
  "7 environmental failures" figure; it is only true with Docker up.
- **Verify from build output, never from `target/surefire-reports`** — a stale report once reported
  green for a fixture that had never compiled.
- **If a real signature differs from what this plan quotes, the real signature wins** — and say so in
  the commit message.
- The REST API is **generated** from `betterco_api.yaml` at `generate-sources`. A spec edit
  regenerates the interface, so the controller must follow in the same change. None of tonight's
  tasks should need a spec edit; if one seems to, stop and write it up instead.

---

## 3. Tasks, in order

### T1 — Absorb `dev` into the stack (prerequisite, do this first)

`origin/dev` is 3 commits ahead of the stack. Merge **`dev` INTO the branch**, never the other way.

1. `git fetch origin`, then merge `origin/dev` into `test/kyc-stack-on-dev`.
2. Cascade the stack: merge each branch into its child in order —
   `test/kyc-stack-on-dev` → `p4/o2-ordering-safety-check` → `p4/o3-chargeable-event` →
   `p4/o4-content-date` → `p4/o5-user-portal-world` → `p4/o6-germany-deny-guard`.
3. Compile, run the affected packages on the top branch, push all six.

**Stop condition:** if any merge conflicts in a file that P2/P3/P4 touched, **do not resolve it by
guessing** — leave that branch unmerged, record the conflicting paths, and carry on with T2 from the
last clean branch. A wrong conflict resolution in the ordering path costs more than a night.

### T2 — Refresh `src/main/resources/kyc/price-bands.csv` (data, smallest, loses value by waiting)

Measured today: the file is 132 rows of `code,band,priceUsd` and holds the **pre-26-August** list —
`Low 18.00 / Medium 43.50 / High 88.00 / Premium 114.00`. The vendor repriced on **26 August** to
**Low 19 / Medium 49 / High 89 / Premium 119 USD**.

1. Update the four band prices.
2. Apply the three recorded band changes: **BR** Low → **Medium**, **LU** High → **Medium**,
   **IL** Medium → **Low**.
3. **Attempt** a fresh pull of `records.knowyourcustomer.com/pricing` and `/coverage` (free reads;
   the old `knowyourcustomer.com/products/buy-kyc-report/…` URLs 301 there). The 26 August pull
   counted **149** jurisdictions against our 132 rows, so roughly 17 are missing entirely.
   **If the pull fails or the page is bot-blocked, say so and change nothing beyond steps 1–2.**
   Do not invent a row.
4. **Do not** try to resolve the **US**: the coverage page prices it *per state*, not as a flat band,
   and that tab has never been read. Leave the US row as it is and note it.

Two things that must survive into the commit message: the recorded number is a **list price**
(`KycCostSource.LIST_PRICE_CONFIGURED`), not an invoiced amount; and **our purchase rates come from
the Order Form of 13 April 2026 and did not change** — what a band change moves is which contract
rate applies.

### T3 — Implement the D1 reuse window (the largest item, and the point of the night)

Decided by the user 2026-08-29: **reuse a stored document across customers while it is fresh — a
window on `fetchedAt` (age of our copy, NOT `contentDate`), default 7 days, configurable per
source.** Confirmed today by grep: only comments exist; there is no reuse logic.

- The window belongs to the **per-source policy** layer, not to the kyc.com client — other sources
  will want other windows, and the second clock is only now actually populated (`contentDate` landed
  in P4/O4).
- kyc.com has **no free freshness check**, so the clock is all we have there. Where a source does
  offer one (INPI, Companies House), the design should leave room to ask rather than trust the clock;
  do not build those paths tonight.
- **D6 is still open and is a different question**: whether the vendor's licence permits serving a
  document bought for customer A to customer B has never been asked. So the reuse path must sit
  **behind a flag that is off by default**, and the commit must say why. Building it is right;
  switching it on is not ours tonight.
- Tests first, and include the boundaries: an acquisition exactly at the window edge, one past it,
  and one with a `null` `fetchedAt`.

### T4 — M5: `document-search.create-client` beyond the development profile

Confirmed today: the flag is `document-search.create-client=true` in
`application-development.properties` only; `KycGatewayService` reads it with a default of `false`
("off means the order path behaves exactly as it did before P1").

Give it an explicit, documented setting in `application.properties` — **defaulting to off** — plus
tests covering both states of the flag. Do **not** turn it on for any other profile; which
environments get it is a person's call, and the failure mode of guessing is a client created in an
environment nobody expected.

### T5 — Draft the Septeo note (document only, in `betterco-worldwide`, English)

One note, covering all three consumer-visible changes together:

1. the **P3 contract cut-over** (still unsent — `HANDOVER_2026-09-08-P3.md` §5 #2; Björn is
   integrating against the vendor ids *now*, which is what makes it urgent),
2. a **DE order now returns `409 jurisdiction_not_available`** where it used to be accepted,
3. on a **sandbox-scoped instance the pre-Ready path returns `503 pending_path_unavailable`** where
   it used to return an empty listing — the empty listing was a lie, so this is not a regression.

Write it to `docs/SEPTEO_CONTRACT_NOTE_2026-09-11.md`, commit it on `document-kinds-evidence`, and
**do not send it**. House style: answer first, no sales language, no upselling, no staged candour.

---

## 4. Explicitly NOT in tonight's scope

- Any billable order, and therefore the real-document proof and case 189's missing
  `businessRelationId`.
- The vendor-config inversion, the `bc-stg-vault` sandbox secret, the Azure placeholder, evidence
  level D2 — every §5 item that needs a person.
- Backfilling `contentDate` over the ten existing acquisitions on dev.
- The cascade-delete of documents with their client (§5 #9) — it wants a ticket first, and the
  reading being wrong is irreversible.
- A full-suite run. See §2.

## 5. What to leave behind

`docs/HANDOVER_2026-09-11.md`, in the shape of its predecessor: what was produced (branch, commit,
one line each), what the plan got wrong and was corrected before being built on, decisions taken
that the documents did not settle, anything a consumer will see, and what the next session should do
first. **State plainly what was not achieved** — a task stopped at a conflict, or at a bot-blocked
price page, is a result, not a failure to hide. Then update the resume memory pointer.
