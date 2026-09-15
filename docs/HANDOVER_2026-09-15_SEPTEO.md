# Handover — Septeo contract + the generator behind it, 15 September 2026

**Supersedes `HANDOVER_2026-09-14_SEPTEO_CONTRACT.md` for everything about the pricing annex.**
That note is still the right read for the clause-level reasoning of 14.09 (clause 8, liability, DORA,
Annex 5). It is wrong on three points of fact, corrected below. `HANDOVER_2026-09-14.md` remains the
entry point for the branch stack and the 1 October go-live; none of that is touched here.

Branch `document-kinds-evidence`, HEAD `28e2ebe`, pushed, tree clean.

---

## The one line

The contract, the price table and the coverage list are now **generated from
`curation/price_bands.json`** and verified against it; the Word file for the counterparty is
generated too, and both generators refuse to produce output that has lost content. What remains is
commercial, not technical.

---

## 1. Where everything is

| | |
|---|---|
| `docs/SEPTEO_RESELLER_AGREEMENT_2026-09-14.html` | the source of truth. Clauses 1–15, Annexes 1–5. Internal notes live in an amber block that is `display:none` in print |
| `…-09-14.pdf` | 17 pp, rendered with Playwright on **py -3.13** |
| `…-09-14.docx` | **19 pp**, TOC, track changes on — the file STP marks up |
| `docs/SEPTEO_LEGAL_REVIEW_BRIEF.{html,pdf}` | 4 pp instruction to counsel. **Internal. Never goes to STP** |
| `docs/SEPTEO_COUNTERPARTY_REDTEAM.md` | how the draft reads from Karlsruhe. Cites items A2/B5 of a *consistency review* that is **not in the repo** — find it |
| `curation/price_bands.json` | 153 jurisdictions + a `subJurisdictions` block (23 US states, 3 CA provinces) |
| `curation/price_bands_2026-07-30.json` | the superseded July pull, kept |
| `curation/kyc_jurisdictions_api_2026-09-15.json` | the vendor's own `/api/jurisdictions`, 179 rows, with `buyable` / `searchable` / `searchSlow` and the document set per jurisdiction |

## 2. How to regenerate, in order

```bash
python scripts/build_annex2.py --check      # exits 1 on drift; run before any send
python scripts/build_annex2.py --write      # regenerate Annex 2.1 and 2.2
py -3.13 <render.py> <in.html> <out.pdf>    # Playwright; PyMuPDF is on py -3.9, neither has both
python scripts/build_docx_source.py         # flattens + strips internal notes -> build/
powershell -ExecutionPolicy Bypass -File scripts/to_docx.ps1
```

**Never hand-edit Annex 2.1 or 2.2.** They sit between `BEGIN/END generated` markers.

## 3. Three traps, each of which already bit once

- **`@media print` does not exist in Word.** Converting the contract HTML directly puts the internal
  notes in the counterparty's file. `build_docx_source.py` strips them by class and refuses to write
  if a marker survives.
- **Check output against the SOURCE, never against itself.** Every check that compared the output to
  its own structure passed while content was missing. The `.docx` shipped Annex 2.2 with **1 of 153**
  jurisdictions and three separate checks called it fine. Both generators now compare the set of
  names to `price_bands.json` and fail loudly.
- **Cross-references are hand-typed and survive every structural check.** Four wrong ones were found
  only by reading the document end to end (15.5→6.2, 11.1→Annex 2, the annex list order, 7.2→Annex 2).
  Read the rendered PDF before any send.

Minor: `ComputeStatistics(2)` reports nonsense headless (4 for a 19-page document). To check
pagination, export the `.docx` to PDF from Word. And this tree is under Dropbox — a `.docx` on disk
was silently replaced by an older copy *after* being committed; `git status` caught it. Trust the
commit, not the file.

## 4. Corrections to the 14.09 handover

1. **The US coverage page is not a 404.** It is `/coverage/united-states`, not `/coverage/usa`.
2. **The US price is not at risk; the coverage is.** The Order Form contracts a flat US case fee, so
   "per state" is the vendor's retail model, not our cost. What was unknown — and is now known — is
   *which states resolve*: **23**, without California, Texas, Nevada or Wyoming.
3. **GB/DE/US were never "direct routes".** 1,70 / 6,30 / 17,35 € are the supplier's Home Band fees.
   Our own direct routes are **DE, FR, DK**. Those figures are now out of the customer-facing pack.

## 5. What changed in the document on 15.09

Decisions taken: upstream licence **out of scope** for this document · minimum **ramped, 750 €/month
for three months then 1.500 €**, measured on our share · procurement costs **in Annex 2.1** (a separate
Annex 2a existed for part of the day and was folded back) · **no contractual penalty** · **24 months**
plus new **14.2a** (a jurisdiction falls away if supply ceases; >50 % of recent Cases → 30 days' exit).

Six red-team defects fixed: the 8.7/Annex 1.3 charging contradiction · 6.2 rebuilt as a real standstill
in **6.2a** (it had no subject matter once 8.5 removed End Client identities) · 6.1 narrowed with
**6.1a** carve-outs, because it barred STP from approaching Companies House · 5.2 time-limited with a
residual-knowledge carve-out in **5.2a** · **Annex 3.5** on third-country transfers, which did not
exist at all while we procure in Russia, Belarus and Iran · 15.2 assignment now needs consent.

**Annex 2.2 now names the sub-registers**: "United States resolves only in the following 23, and a
Case can be placed only in one of them", and the same for Canada's three provinces.

## 6. Open — all commercial, none technical

1. **The upstream supply licence.** GTC cl. 10.2 bars use "for the benefit of any other entity";
   cl. 16.3 forces deletion to statutory minimum on termination. Out of scope for the document by
   decision, but it gates what clause 3.5 can honestly promise. Addendum, or restrict to direct routes.
2. **The three deal-stallers** in the red-team's section 1: case-level margin visibility against our
   free right to compete (8.5 + 3.6); the liability asymmetry, with no IP or title indemnity and STP's
   own liability unlimited; take-or-pay. Decide before the first call, not in it.
3. **Present the ramp as a concession.** It is already in the draft. Per the red-team's section 5, a
   *visible* give on clauses 5, 6.1, 12.2 and 13.2 is what evidences *Aushandeln* — accepting them
   quietly and relying on § 307 later is the counterparty's better move.
4. **Ask the supplier** which US states and which Brazilian Juntas, in one mail. Brazil is Jucesp,
   São Paulo only, one of 27.
5. **Spain is `searchable: false`** in the vendor API — STP's fifth priority market. Annex 2.2 does
   not say so yet. Eleven jurisdictions are unsearchable; the flag is in the API capture.
6. **Counsel review**, on the characterisation question first: the compensation is a profit share,
   not a purchase price, which drives both § 89b HGB and where DORA Art. 30 lands.

## 7. Next technical step, if wanted

Repoint `build_annex2.py` at `kyc_jurisdictions_api_2026-09-15.json` instead of the scraped coverage
page. It carries `searchable`, `buyable`, `searchSlow` **and the document set per jurisdiction**,
which would let Annex 1.3's four availability cases be generated from vendor data rather than
asserted — and would surface the Spain problem in the annex automatically.
