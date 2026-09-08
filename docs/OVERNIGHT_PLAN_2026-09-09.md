# Overnight plan — 9 September 2026 (P4: safety, cost, then the Germany guard)

**For an unattended, looped session.** Read §2 (rules) before §3 (tasks). One task per branch, tests
first, commit, push. No PRs, no merges, no deploys, no money. Go-live is **1 October**.

Predecessor: `OVERNIGHT_PLAN_2026-09-07.md` (all eight tasks done). Current entry point for state:
`HANDOVER_2026-09-08-P3.md`.

---

## 1. Where we are, in one table

| | State |
|---|---|
| P1 client + matter | merged into `dev` (#2293), live |
| P2 acquisitions + ingestion | built, **proven on the sandbox** 8 Sep, off by default |
| P3 contract cut-over (M4) | built and **verified on dev 8081**, 8 Sep |
| M5 flag · M6 Germany deny-guard | **not started** |
| §5 open items | 13, of which four are pure code — this plan |

Everything lives on **one branch, `test/kyc-stack-on-dev`** @ `ae1f59306`, 25 commits ahead of `dev`,
clean, pushed. PR #2305 is a **draft and stays one**.

Tonight closes the four code-able items from `HANDOVER_2026-09-08-P3.md` §5 — in the order in which
they lose value by waiting — and then starts M6 if there is time.

## 2. Rules for the unattended session

**Hard stops — never do these without a person:**

- **No billable calls.** No `POST …/document-search/cases`, on any host, ever. Reads on production
  are free; creating a case is not.
- **No deploys**, no workflow dispatches, no restarting anything on the Hetzner box.
- **No merging into `dev`**, no PRs, no marking #2305 ready, no deleting branches, no force-pushes.
- **No changes to `fix/kyc-create-validation-errors`** — it is kept deliberately.
- **Do not "fix" `application-development.properties:52`** (the unguarded `${AZURE_USER_USERNAME}`)
  and do not point staging at the production secret. Both are §5 items that need a person.

**Method:**

- One task per branch, branched from the previous task's branch, keeping the stack ordered behind
  `test/kyc-stack-on-dev`.
- **Tests first.** Where the change is a fix, prove the test fails against the unfixed code before
  fixing it. Where the code is new and inert, say so rather than implying a red-green cycle.
- Build with the local Maven and its populated repo:

  ```
  M=".../4399718c-9344-4d71-8df8-e23bd0de46db/scratchpad"
  "$M/apache-maven-3.9.9/bin/mvn" -o -B -Dmaven.repo.local="$M/m2repo" -Djacoco.skip=true test
  ```

  Run the **affected packages**; the full suite is killed by this environment about half the time.
  **Full-suite baseline is 7 failures, all environmental**: 5 × `ApiCounterTest` (Docker hostname),
  2 × `DatevRiskCsvImportServiceTest` (locale). Anything beyond those seven is yours.
- **Verify from build output, never from `target/surefire-reports`** — a stale report once reported
  green for a fixture that had never compiled.
- Judge by **no new failures** against a freshly measured baseline. Never claim a green suite.
- **If a real signature differs from what this plan quotes, the real signature wins** — and say so in
  the commit.
- The REST API is **generated** from `betterco_api.yaml` at `generate-sources`. A spec edit
  regenerates the interface, so the controller must follow in the same change.

**Each tick, before starting work:**

1. `git fetch origin && git merge origin/dev` into the working branch — it has drifted twice, and
   `betterco_api.yaml` is a 648 KB shared hotspot. Merge early.
2. Run the §1c contract-leak assertion from `HANDOVER_2026-09-08-P3.md` (it checks prose, not just
   field names — it has already caught one real defect).

**Stop and write it up rather than guess when:**

- a design decision arises that the documents do not already settle,
- tests will not go green within one iteration,
- anything would need a deploy, a person, or money to verify.

## 3. The task list, in order

### O1 — Read the seams first. Nothing after this may be written from memory.

Read and record the real shapes before touching them:

- `KycCaseLink` — where an order is recorded, and what it already carries (this is where a
  chargeable event has to land; the billable unit at kyc.com is the **case**, not the document).
- `DocumentAcquisition` — confirmed to have `fetchedAt`, `contentDate` (declared, **never
  assigned**), `vendorName`, `vendorCategory`, `vendorTarget`, `sourceRef`, `sourceRefSpace`; **no
  cost field of any kind**.
- The order path: whatever calls `POST /document-search/cases`, and what it knows at that moment
  (jurisdiction, ordered tier, actor, vendor world).
- `KycVendorTarget` and how the active world is resolved at runtime.
- The listing shapes: on the **ready** listing the label lives in `name` (`CS01 <17/12/2025>.pdf`)
  and `availability` is null; on the **pending** listing `type` is a status (`Received`), not a kind.

Correct this plan's §3 in the handover wherever the code disagrees. O1 produces no branch.

### O2 — A startup assertion against the fail-open vendor config (§5 #1 — the money one)

**Measured, not hypothetical:** `application.properties:179-183` defaults
`kyc-com.base-url=https://api.knowyourcustomer.com` with `create-enabled=false`; sandbox is only an
override (`application-development.properties:35`, `application-staging.properties:61`).
`bc-dev-vault-dev` holds the **production** secret. A jar started without its profile therefore
authenticates against the paying world **silently**.

Build the assertion half only — a startup check that refuses to start on a money-spending
combination:

- ordering is enabled (`kyc-com.create-enabled=true`) **and** the resolved base-url is the
  production host **and** the active profiles do not include `production`.
- The message must name all three inputs and the profile that was actually active. A config error
  that reads like a bean cycle costs an hour — see §2 of the P3 handover.

**Do not invert the default.** It is right in shape but nobody has confirmed production runs with its
profile active; inverting it unverified could take production ordering down. Say so in the commit.

Tests: the failing combination refuses to start; production-with-profile starts; sandbox starts;
production host with `create-enabled=false` starts (reads are free).

### O3 — Record the chargeable event (§5 #5 / D4 — the only item that loses data by waiting)

D4: *"unrecorded cost is unrecoverable. Instrument now, decide the commercial model later."* Every
order placed before this exists is a case whose vendor cost cannot be attributed afterwards.

**Scope, so the night does not have to invent a commercial model:** record the *event*, not a price
list. On the case link, at the moment an order is placed: source, `vendorTarget`, jurisdiction, the
ordered tier/product, the ordering actor, `orderedAt`, and a **nullable** `costAmount` +
`costCurrency` with a `costSource` enum (`CONFIGURED` / `UNKNOWN`). The vendor does not return a
price, so `UNKNOWN` with everything else populated is a correct and useful row — it keeps the
billing decision open at no cost, which is exactly what D4 asks for.

**Out of scope:** per-document allocation (derivable later), the price table itself, and any
re-billing logic. If a configured price band is genuinely available in the backend, use it; if it is
not, do **not** import one from the `betterco-worldwide` repo tonight.

### O4 — Populate `contentDate` (§5 #6 — the second clock)

The field is declared and read but never assigned, so D1's reuse rule reads only the fetch clock —
the trap §5 of the architecture memo was written to prevent. A 2019 filing currently looks current.

The date is in the vendor's own label: `CS01 <17/12/2025>.pdf`. Parse it at ingestion, from the
verbatim `vendorName` / `vendorCategory` already stored.

**Rules:** never guess. If the label carries no date, or one that does not parse unambiguously,
leave `contentDate` null — a null is honest and a wrong date is not. Confirm the real format against
the labels actually stored on dev before relying on `dd/MM/yyyy`; the dev box has two clients with
ten acquisitions between them. No backfill migration tonight.

### O5 — Make the wrong user-portal world impossible to be silent (§5 #10)

`kyc-com.user.base-url=https://betterco.knowyourcustomer.com` sits in `application.properties` and is
**overridden in no profile** — `application-staging.properties:72` says so explicitly. That is how a
sandbox instance asked the *production* user portal about a sandbox case and got `200` with no
groups: a silence, not an error. The worker works around it; the config is still wrong.

If a sandbox user-portal host is documented, override it in the development and staging profiles.
**If one is not** — likely — then make the misconfiguration loud instead: outside production the
property resolves to empty and the pending path refuses with a named error rather than asking the
wrong world. Keep the worker's guard either way; belt and braces is correct here.

### O6 — M6, the Germany deny-guard (only if O2–O5 are done and pushed)

**Hard constraint:** kyc.com's scope **excludes Germany** — we source DE ourselves. A DE order must
be refused before it can reach the vendor, with a message a consumer can act on, and a test that
asserts no vendor call is made. Nothing about DE routing to our own sources belongs in tonight.

**Out of scope tonight:** M5 (the create-client flag beyond `development`), the reuse window, the
evidence level (D2 — a decision, not a commit), and anything on the §5 list marked as needing a
person.

## 4. What to leave behind

A new dated handover, `docs/HANDOVER_2026-09-09.md`, in the `betterco-worldwide` repo:

- which tasks completed, with branch names and test counts, and which did not and why
- **anything where the real signature differed from this plan**
- every decision taken that the documents did not already settle
- what the next session should do first

## 5. Repos

- Backend (all branch work): `2601_Claude/betterco-backend/betterco-backend`, branch
  `test/kyc-stack-on-dev`
- Docs and curation (plan, handover): `2601_Claude/betterco-worldwide/betterco-worldwide`
