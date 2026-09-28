# MEMO 2026-09-28 — Match score: merged, verified on dev, not yet on prod

**Status:** PR #2343 is in `dev` and passes the full checklist there. Staging and production do not
have it until their next image build. The STP guide (section 06) is updated but not sent.

## What is where

| | dev | stg | prod |
|---|---|---|---|
| Match score (`POST …/document-search/match`, `GET …/match/rules`) | **yes** — merged 28.09. 15:52 UTC, squash `46dca5c05` | no — image of 21.09. | no — image of 21.09. 18:37 |
| Supplier behind it | test system (sandbox) | test system | live |

The PR was approved by the backend developer. The squash contains the band-0 fix (`e4d8d2647` on
the branch) and both test fixes (`bc009d418`).

## Verified before the merge — on 178, 27.09.

| | Result |
|---|---|
| Match unit tests | 70 / 70 |
| `MatchApiIT` (real Spring context, Mongo container, registry mocked) | 7 / 7 |
| Full unit suite | 1218 tests, 0 failures, 0 errors, 8 skipped |

Three defects found by running things for the first time, none of them visible to the existing tests:

1. **`MatchApiIT` could not start** — Javers auto-configuration excluded without the `@MockBean Javers`
   every other IT has. Test-only.
2. **Every IT call returned 500** — the generated API requires an `Authorization` header; the test
   sent none. Test-only.
3. **Band 0 (`NO_COMPANY_REGISTER`) was unreachable over the API.** The check ran in the scorer, which
   only sees a *looked-up* number; in jurisdictions where numbers are not comparable (Austria) no
   lookup runs. Fixed in `CompanyMatchService`: the *supplied* number is checked before any search.
   Red test first, then green. The scorer's own vectors could not see this because they call the
   scorer directly.

Decided, not changed: every candidate from the name search scores **85** (`NAME_ONLY`) whether or not
its name is equal. Documented in the guide — gate on 85 together with `candidates[].signals.nameMatch`.

## Verified on dev — 28.09.

Script: `scripts/match_checklist.py` (reads only; the one create is `confirm:false`, a dry run).

| # | Check | Result |
|---|---|---|
| 1–2 | jurisdictions, case list, search | 200 |
| 3 | create a case **without** calling match (dry run) | 428 `not_confirmed` — unchanged |
| 4 | `match/rules` | `2026-09-21.1`, comparable GB/IE/SG/HK |
| 5 | GB name + number | 100 `NUMBER_AND_NAME` |
| 6 | GB name only | 85, `numberSupplied: false` |
| 7 | GB right name, wrong number | 85, not 100 |
| 8 | DE | `orderable: false`, `JURISDICTION_NOT_AVAILABLE` |
| 9 | a jurisdiction dev cannot search (AX) | `checkable: false`, `NO_SEARCHABLE_REGISTRY` |
| 10 | no jurisdiction | 400 |
| 11 | AT association number (row 16) | 0 `NO_COMPANY_REGISTER` |

Row 9 was first run with **Spain** and failed: dev's test system marks Spain as automated, so the
answer there is a search with no hit (10). Not a defect — see the next section.

## Measured on prod — 28.09. (reads only, own workspace)

- **157 jurisdictions, 97 not automated** — including the STP priority markets **ES, LU, IL, KW**.
- A search on them returns a clean **409 `search_not_supported`**, not a 500.
- The match checks `automated` **before** searching, so on prod it answers those with
  `checkable: false` without calling the supplier. The feared 500 for Spain cannot happen.
- Dev marks only 17 as not automated. **Automation behaviour measured on dev does not predict prod.**

## What dev can and cannot tell you

Dev talks to the supplier's test system: a few fixed example companies per country (GB 5, IE 5,
HK 8, NL 3, US 3, FR/SG/DK 1), found by substring. A real name ("TESCO") finds nothing.

- **Can:** wiring, contract, error codes, every band on purpose (GB/IE/SG/HK), the whole order flow
  free of charge (`NOT_BILLABLE`), the Germany refusal.
- **Cannot:** score quality against real registers (prod returned 200 hits where dev returns 1),
  which countries are searchable, real documents (every one is the same stub PDF), real turnaround.

## Open — in this order

1. **Staging/production build.** Neither deploys from `dev` on its own. The next build carries
   everything merged since 21.09., not only the match — agree it before it goes to production.
2. **Run `scripts/match_checklist.py` on prod** once `matchCompany` appears in
   `https://app.betterco.ai/bcapi/betterco_api.yaml`. Free calls.
3. **Send STP the updated guide** (section 06 in `SEPTEO_INTEGRATION_GUIDE_2026-09-17.html`) once the
   match is on stg — and tell them that on prod four of their priority markets (ES, LU, IL, KW) answer
   "check not possible".

## Contract — state for the next round

- **Draft 2 went to Martin on 27.09. 07:29, sent by Uwe** (cc Jens, Eckhard), file
  `Vertragsentwurf_BetterCo_-_Entwurf_2_2026-09-25-2.docx`. It carries Uwe's changes on top of ours:
  EUR 20.000 liability floor, EUR 750 minimum throughout the pilot, a new clause 5.6.
- **The next round must start from Uwe's file**, not from `SEPTEO_RESELLER_AGREEMENT_2026-09-14.html`
  — the repo HTML does not contain Uwe's edits.
- Austria: the sent version excludes it; Fabian asked to keep it. Decision 27.09.: no correction mail —
  technically Austria is served anyway (the backend refuses only DE), the contract wording is separate.
  The repo generator already restores it (`c69a8c1`).
