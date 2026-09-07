# Overnight implementation plan — 7 September 2026

**For an unattended session.** Read §3 (rules) before §4 (tasks). Every task is one branch, one
commit, tests first, pushed. Nothing here needs a person, a deploy, or money.

---

## 1. Where we actually are

**The stack has now run.** That changes the risk picture I wrote yesterday. `test/kyc-stack-on-dev`
is deployed on the Hetzner box at `:8081` against the **production** vendor, and a real order went
through it today: TATE & LYLE, case `189`, ~$18.

| | State |
|---|---|
| **P1 — client + matter** | ✅ proven on **production**, not just the sandbox: client `6a9f1170…`, one matter, vendor reference filed, register identity `GB/00076535` |
| **R1 — status truthfulness** | built, deployed on `:8081`, stored status tracking the vendor through the build |
| **R2 — vendor target** | built, deployed, untested against a world-switch |
| **R3 — idempotency** | built, deployed; the charged-order path has not been exercised |
| **R4a — acquisition record** | built, inert. Lifecycle, entity, repository, service |
| **F3 — pending-download 500** | **found and fixed today** (`fix/kyc-user-client-error-handling`), not yet deployed |
| **M3 — storage** | **not started. This is the whole remaining MVP.** |
| M4 contract · M5 flag · M6 deny-guard | not started |

**Nothing is merged.** Six branches now, stacked in review order behind `test/kyc-stack-on-dev`.

## 2. What today's live order changed in the plan

Four findings, each of which alters how M3 must be built:

1. **Documents arrive during the build, not at the end.** Case `189` exposed 7 downloadable
   documents at 50% complete, via `includePending=true`. The plan already said the worker must not
   wait for case-ready; that is now demonstrated rather than assumed, and it means **the ingestion
   worker is driven by the document list, not by case status**.
2. **Real files are megabytes.** A single 1903 incorporation document was **2.1 MB**; the case was
   3.3 MB and still building. The sandbox's uniform 904-byte stubs told us nothing. Do not buffer a
   whole case in memory, and do not size anything against the sandbox.
3. **On the pending path, `type` is a status** (`Received`), not a kind. The label is in `name`
   (`CS01 <17/12/2025>.pdf`). Anything that maps types must read `name`.
4. **The pending path was completely unguarded** (F3). Ingestion must therefore assume individual
   documents will fail, record the failure against that document, and carry on with the rest — never
   let one bad document fail a case.

## 3. Rules for the unattended session

**Hard stops — never do these without a person:**

- **No billable calls.** No `POST …/document-search/cases`, ever. The dev box at `:8081` is armed
  and pointed at the production vendor.
- **No deploys**, no workflow dispatches, no restarting anything on the Hetzner box.
- **No merging**, no pushing to `dev`, no deleting branches, no force-pushes.
- **No changes to `fix/kyc-create-validation-errors`** — it is kept deliberately.

**Method:**

- One task per branch, branched from the previous task's branch to keep the stack ordered.
- **Tests first.** Where the change is a fix, prove the test fails against the unfixed code before
  fixing it. Where it is new inert code, that is not possible — say so rather than implying it.
- Verify with the local Maven (`mvn -o -Dmaven.repo.local=<scratchpad>/m2repo -Djacoco.skip=true`),
  running the **affected packages**; the full suite is killed by this environment about half the
  time, so treat a completed full run as a bonus, not a gate.
- Judge by **no new failures** against a freshly measured baseline. Never claim a green suite.
- Commit messages say what was wrong and why the fix is shaped as it is. Push the branch. Do not
  open a PR — six is already more than one reviewer should be asked to hold.
- **If a real signature differs from what the plan quotes, the real signature wins** — and note it
  in the commit.

**When to stop and write it up rather than guess:**

- A design decision the documents do not already settle.
- Tests that will not go green within one iteration.
- Anything that would need a deploy to verify.

## 4. The task list, in order

Each is a task from `docs/superpowers/plans/2026-08-29-p2-acquisitions-and-ingestion.md`, adapted by
§2. Do them in this order; each builds on the last.

| # | Task | Plan ref | Notes |
|---|---|---|---|
| **N1** | **Read the four ingestion seams and write the fixtures** | Task 0 | `DocumentManagementService.uploadDocument(UploadData, actorId, workspaceId)`, `Document`, `UploadData` (a record with a validating compact constructor), `KycGatewayService.listDocumentsById/downloadDocumentById`, `KycCaseLink`. **Nothing after this may be written from memory.** |
| **N2** | **`SourcePollPolicy` + `SourcePollPolicies`** | Task 3 | Schedule, give-up point, terminal action, per source. kyc.com is the only entry |
| **N3** | **`refreshTrackedStatuses` obeys the policy** | Task 4 | The ready-flag half is already done and deployed; only the backoff and give-up remain |
| **N4** | **`DocumentIngestor` — fetch, store, attach, record** | Task 5 | The heart of M3. Store **every** document; roles are an overlay and usually empty. Built-in `documentType` where one genuinely fits, otherwise a process document keeping the vendor label in the filename. Send an explicit `application/pdf`. One document failing must not fail the case |
| **N5** | **`DocumentIngestionWorker` — the per-document pass** | Task 6 | Driven by the document list with `includePending=true`, **never** by case-ready |
| **N6** | **Serve content from our storage**, fetch-store-serve on a miss | Task 7 | Behind `aggregation.ingestion.enabled`, default off |
| **N7** | **Cascade on client deletion** | Task 8 | `CustomerService.deleteAllClientInfo` currently orphans documents |
| **N8** | **Account-scope degrades instead of 400** | Task 10 | F2. Small, independent — a good one to end on |

**Out of scope tonight:** the reuse window (task 9 — blocked on the vendor licence question), the
contract cut-over (M4), and the type-mapping layer beyond what N4 needs inline.

## 5. What to leave behind

Append to `docs/HANDOVER_2026-09-06.md`, or start a new dated handover if it grows past a screen:

- which tasks completed, with branch names and test counts
- **anything where the real signature differed from the plan**
- every decision taken that the documents did not already settle
- what the next session should do first
