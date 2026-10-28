# Memo 2026-10-28 — Septeo: the jurisdictions endpoint shows the wrong price; it should show the tier

**Trigger.** Fabian (27.10.) asked whether all US states sit in his category A2 (24,85 €). Eckhard
confirmed the same day. Björn (28.10.) then asked whether `/document-search/jurisdictions` stays and
whether its prices can be given in EUR, because Septeo is billed in EUR.

## 1. Was the 27.10. answer consistent? Yes.

- **One US price, all states.** The supplier Order Form (13.04.2026) has a flat US fee of 17,35 €.
  "Per state" is only the supplier's public retail model. All 23 states sit in one band in
  `curation/price_bands.json`.
- **23 states.** The list in the mail matches `curation/price_bands.json` (`US-*`) and Annex 2.2.
- **Search finds only Delaware.** Matches our measurements; other states go through Fall B.
- **24,85 €** = 17,35 € US procurement + 7,50 € fixed fee — the same rule as
  A 18,30 / B 34,20 / C 62,00 / D 78,00.

Not verified: whether Draft 3 (Uwe's docx) writes 24,85 € into the contract. The 14.09. repo version
calls the US cost "agreed separately and provisional".

## 2. What is actually wrong: the endpoint

`/document-search/jurisdictions` (backend `origin/dev`, `KycGatewayService` + `KycPriceBands`,
`src/main/resources/kyc/price-bands.csv`) returns `priceBand` (Low/Medium/High/Premium) and
`priceUsd`, taken from the supplier's **public list in USD** (19 / 49 / 89 / 119).

- This is **neither our cost nor Septeo's price.** Our cost is in EUR per the Order Form
  (A 10,80 · B 26,70 · C 54,50 · D 70,50 · US 17,35 €). Septeo pays in EUR (cost + 7,50 €).
- **The US is wrong:** the CSV says `US,Medium,43.50` → reads as B, Septeo's price is A2 24,85 €.
  We do **not** pay 43,50; nobody does.
- The band names + USD amounts map one to one onto the supplier's public price page, so the
  supplier can be traced from our API.
- The OpenAPI description still states the July list (Low 18 / Medium 43.50 / High 88 / Premium 114).
- `KycOrderCharge` records our per-order cost from the same USD list (`LIST_PRICE_CONFIGURED`), so
  our internal cost records are wrong as well.

## 3. Decision (Eckhard, 28.10.)

**The endpoint shows the tier, not a price.**

- Replace `priceBand` with `tier: A1 | A2 | B | C | D` (Low→A1, Medium→B, High→C, Premium→D,
  US→A2). Remove `priceUsd`.
- The EUR price per tier lives only in the contract table. It changes only through the contract.
- No new data needed: the tier mapping already exists in `curation/price_bands.json` →
  `scripts/build_annex2.py` → Annex 2.2. Fabian's table matches it once DE and AT are left out
  (A 104 − DE = 103, B 35 − AT = 34).
- **DE and AT are not a Septeo gap** — STP uses its own direct routes and ignores those rows. For
  every other consumer DE and AT stay in our offer and documentation.

## 4. To build (backend, not started)

1. `price-bands.csv` → tier column; US = A2.
2. `KycJurisdiction` schema in `betterco_api.yaml`: `tier`, drop `priceBand` / `priceUsd`.
3. `KycOrderCharge`: record the EUR Order Form rate per tier, not the USD list price.
4. Deploy to staging, tell Björn.

## 5. Mail

Reply to Björn is a **Gmail draft, not sent** (thread "Rückfrage US-Bundesstaaten"): endpoint stays;
it will show the tier; EUR price from the contract table; today's `priceBand`/`priceUsd` are not
their price and go away; all 23 US states are A2 at 24,85 €; we report when it is on staging.
