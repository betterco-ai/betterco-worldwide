# MEMO 2026-11-26 — STP round of 17.11 ("Version Telco"), FX correction, our line

**Status:** STP's counsel sent the version agreed in principle on the 06.11 call; Uwe reviewed it on 26.11.
Our line: `docs/STP_VERHANDLUNGSLINIE_2026-11-26.{html,pdf}` (internal, German), replacing the 06.11 sheet.
A reply to Uwe with the sheet attached sits as a Gmail draft in his thread "WG: Vertragsentwurf BetterCo";
not sent at the time of writing. Next step: Uwe sends Martin a points list; redline only after agreement.

## What arrived

| Date | From | What |
|---|---|---|
| 06.11. 13:00 | Martin (Teams) | Call "Vertragsfinalisierung BetterCo" with RAin Nöth; outcome recorded only in her comments dated 06.11 |
| 17.11. 16:46 | RAin Nöth → all | `Vertrag BetterCo Version Telco 17_11_2026.docx` — now `docs/SEPTEO_STP_VERSION_TELCO_2026-11-17.docx` |
| 23.11. | Uwe → Eckhard | "How do we continue with Ripke?"; manual jurisdictions: STP must tell the bank there is no liability, or we find direct routes |
| 26.11. 17:51 | Uwe → Eckhard | His assessment `STP-Vertrag Bewertung Entwurf vom 06.11.2026.md` (not in the repo: names the supplier) |

## Correction: we buy in EUR, not USD

The 05.11 memo and the 06.11 line said "we buy in USD and sell in EUR" and asked for an FX clause in 8.6.
**That was wrong (Eckhard).** Measured 26.11: both supplier order forms (30.07.2026, and the 6-month POC
from 01.10.2026 to 31.03.2027) price every band in EUR, and the invoices state "All payments due under this
Agreement will be paid in EUR". The USD figures are only the supplier's public list prices.

STP built 8.6(a)/(b) from our remark on the call: (a) has us *acknowledge that we pay in USD* — a false
statement we must not sign — and (b) adjusts the **whole** document price, including our 7,50 € fee, to the
ECB rate each quarter (base rate and threshold left blank). With EUR costs the clause only cuts our price
when the euro rises. We withdraw it ourselves:

> „Wir haben das geprüft: Unser Bezug ist vertraglich in EUR vereinbart, ein Währungsrisiko besteht für
> uns nicht. Den Hinweis aus unserem Gespräch nehmen wir zurück, 8.6(a) und (b) können entfallen."

The real exposure is the supplier's follow-on contract from 01.04.2027: aim for a EUR price hold until the
anniversary of the STP agreement.

## What STP changed on 17.11

| Clause | Change | Our line |
|---|---|---|
| 6.1 / 6.1a / 11 | Non-circumvention gone **even during the term**; any disclosure (also by a third party) frees STP unless obtained by hacking/deception/breach of law; 6.1a deleted; 11.1 sentence on Annex 2.1 garbled | Back to 06.11 state: protected during term, free after; Annex 2.1 explicitly confidential. Limit: prices not confidential = no |
| 8.6 | (a)/(b) FX clause; (c) supplier-cost change only at the anniversary and only by agreement, else 3 months' termination; deleted: fee renegotiation at renewal, "route change does not change cost", STP's 14-day country exit | Delete (a)/(b); accept (c) **plus** an exception for proven register/supplier increases > 10 % on 30 days' notice, STP may drop the country within 14 days; reductions passed on at once; restore renewal renegotiation |
| 8.7 | Nothing delivered (incl. "not available") → free; partial → delivered documents paid | Full case price once a base document or the structured data is delivered; free if our availability display said "available"; procurement cost if ordered against "not available"/"unknown". Fallback: Uwe's 5 % monthly free quota |
| 5.2 | Narrowed to API purpose binding + no bulk export "with the intent" of a competing product; 24 months deleted | Accept with "for the purpose of", add systematic querying, term + 12 months |

**Unmoved:** 13.2 cap (our 50.000 € still tracked; "BetterCo prüft 12 und 13" — the ball is ours: send the
ladder 50k/7,50 · 100k/8,50 · 250k/10,00) · 8.2 fee ("BetterCo denkt darüber nach" — hold 7,50 € in the pilot)
· 12.1 delivery times (STP asks its banks; we warrant recorded timestamps only) · 14.2a 50 % still tracked,
no comment · 14.4, 5.1, last sentence of 12.3 tracked, no objection · 3.2 STP internal.

**Agreed:** 8.4, 14.1, 13.1, 2.1, 12.2 ("i.O."), 3.1 / 5.2a / 5.3, 12.3 recourse via STP.

## Where we go beyond Uwe's assessment

Uwe's review is right on every point and is adopted. Three additions:

1. **14.2a depends on 8.6.** "Where a replacement is available only at a higher cost, clause 8.6 applies" —
   under the new 8.6(c) that means the anniversary and STP's consent. The > 10 % exception is therefore a
   must, not a trade.
2. **Timing:** signing in December puts the first anniversary in December 2027; without the exception we
   carry an April 2027 supplier increase for at least eight months.
3. **Broken references:** 14.3 cites a non-existent clause 6.2a and "clause 5.2 for the period stated in
   it" although 5.2 no longer states one. 8.6 has blanks and a broken formula.

## Homework

- Insurance cover for 100.000 € / 250.000 € (Eckhard; never in mails).
- Supplier: deliveries without its branding — under the new 6.1 visible branding would count as disclosure.
- Follow-on supplier contract from April 2027: EUR price hold to the STP anniversary.
- Decide the 8.7 variant before the points list goes out.

## Our own pressure

We have delivered in production since 01.10 with no signed agreement, i.e. with no liability cap at all.
Closing in December matters more than the last wording.
