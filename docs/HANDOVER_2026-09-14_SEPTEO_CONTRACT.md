# Handover — Septeo reseller contract, 14 September 2026 (evening)

**Scope: the contract pack only.** This does not touch the branch stack, the merge train or the
1 October go-live — `HANDOVER_2026-09-14.md` remains the entry point for all of that and is not
superseded. Read this one only when working on the Septeo agreement or on `price_bands.json`.

**The document:** `docs/SEPTEO_RESELLER_AGREEMENT_2026-09-14.html` — 16 pages, self-contained
(agreement clauses 1–15, Annexes 1–5, signature block, internal notes). Untracked, on branch
`document-kinds-evidence`. **Commit it.**

**One line: the commercial terms and the liability cap were both measuring the wrong base and are
fixed; the pricing annex is now hand-edited and has already diverged from `price_bands.json`, which
is the next thing to repair.**

Two files were deleted today as superseded — `SEPTEO_RESELLER_ANNEX_2026-09-14.html` and
`SEPTEO_RESELLER_SERVICE_DESCRIPTION_2026-09-14.md`. Both still described the old wholesale model
and carried two stale tiers. Their content lives in the agreement's Annex 1. Do not restore them.

---

## 0. The divergence to fix first

`curation/price_bands.json` is the 30 July pull. The contract annex was hand-corrected today. They
now disagree:

| Tier | `price_bands.json` | Annex 2.1 |
|---|---:|---:|
| Low / A | 93 | 93 |
| Medium / B | **33** | **34** |
| High / C | **11** | **10** |
| Premium / D | 2 | 2 |

Tier A is the trap: both say 93 but the **sets differ** — the JSON's includes Brazil and excludes
Israel, the annex's is the reverse. The totals match by coincidence, so a count check will pass and
the data is still wrong.

The live page has also moved twice since the JSON was pulled: **153 jurisdictions** now
(Low 105 · Medium 35 · High 12 · Premium 1), against 149 in August and the 139 in both our files.

### T1 — re-pull `price_bands.json`

Source: `records.knowyourcustomer.com/coverage` (the old
`knowyourcustomer.com/products/buy-kyc-report/…` URLs 301 to it). The page names the band **and the
source register** per jurisdiction; take both — the register name is wanted for
`registry_intelligence.json` and the August memo records at least one error there (Kuwait is the
*Chamber of Commerce & Industry*, not the Ministry).

Confirmed against the live page on 14.09 and already corrected **in the annex only**:

| Jurisdiction | JSON still says | Truth |
|---|---|---|
| Brazil | Low | **Medium — US$49** |
| Luxembourg | High | **Medium — US$49** |
| Israel | Medium | **Low — US$19** |

This was flagged in `PREISBAENDER_UPDATE_2026-08-26.md` § 2 and never actioned. Doing it now also
closes that memo's open point 3.

### T2 — write `scripts/build_annex2.py` so this cannot happen again

The annex must become a generated artefact. `price_bands.json` already carries everything needed —
`band`, `en`, `de`, `region` — and its regions map 1:1 onto the annex groupings
(Europa 49 · Asien-Pazifik 39 · Naher Osten & Afrika 25 · Amerika 18 · Finanz- und
Offshore-Plätze 8).

Generate, between marker comments in the HTML:

- **Annex 2.2** — the jurisdiction chips, grouped by region, `<b>` carrying the tier letter, class
  `chip stp` for the fifteen STP priority jurisdictions.
- **Annex 2.1** — the four `Jurisdictions` count cells only.

Do **not** generate the tier prices (10,80 / 26,70 / 54,50 / 70,50 €) or the list prices
(15 / 35 / 70 / 90 €). Those are contracted Order Form rates, not derived from the public bands, and
they did not change.

The STP fifteen are not in `price_bands.json` today; either add a `stp_priority: true` flag during
the re-pull or keep the list in the script. Flag in the JSON is better — the deck needs it too.

Follow the house pattern in `scripts/build_routing.py`: docstring naming inputs, outputs and the run
line; idempotent; prints what changed.

### T3 — the same pull feeds product, not just the contract

`PREISBAENDER_UPDATE_2026-08-26.md` lists the downstream consumers: `PRICE_BAND_BY_CODE` in the
`knowyourcustomer` skill, deck slides 15/16/18 (Luxembourg is no longer the joint-most-expensive
country and slide 18 still says it is), and the STP simulation figures. Ripple the re-pull through
all of them in one pass.

---

## 1. Three open questions that gate signature

### The upstream licence — the blocker

Unchanged and unresolved. `KYCCOM_F1_Final_Docusign.pdf` is only an Order Form; the General Terms it
incorporates say at clause 10.2 that reports are for "the internal use and benefit of the Customer's
organisation and not for re-sale or other transfer or disposition to, or use by, or for the benefit
of, any other entity or person."

**Note what was tested today and failed:** recharacterising the Septeo relationship does not escape
this. The wording bars use *for the benefit of any other entity*, not merely re-sale, so neither the
reseller framing nor an agency framing helps. The fix is an upstream distribution addendum, or
moving the jurisdiction to a direct route. Nothing in the pack should reach Karlsruhe before this is
settled.

### The United States is not a fixed band

Annex 2.1 fixes the US at 17,35 € and clause 8.6 freezes it for 12 months. The coverage page answers
**"See USA tab for details. Per state"**, and that tab is still unreachable —
`/coverage/usa` returns 404, and `/pricing` only points back to Coverage. Tried again today;
same wall as 26 August.

18 of 70 rows in the STP simulation were US companies, so this is material. Either get the state
detail from the vendor directly, or carve the US out of the 12-month freeze in 8.6 before signing.
A generator built before this is answered will emit a flat 17,35 € that may be wrong.

### Brazil may be São Paulo only

The coverage page names "Jucesp Online" — the Junta Comercial do Estado de São Paulo, one of 27
state registers. If coverage is limited to São Paulo, **Petrobras (Rio) and Gerdau (Porto Alegre)
are unfulfillable** while Brazil is listed as a covered jurisdiction in a signed annex. Open since
26 August. Our own `registry_intelligence.json` correctly describes Brazil as 27 Juntas; the
question is how many the vendor connects.

---

## 2. What changed in the agreement today

Each of these is recorded in the document's own internal notes with its reasoning. Summary only here.

**Clause 8 — the commercial construction.** 8.2 previously gave Founders1 50 % of *gross* with
procurement cost carried out of that half. That is not a net-revenue share: it moved the economics
against us by half the cost on every case, and its break-even against simply selling STP cases at
list came out at exactly twice the list price — i.e. it only beat the status quo if STP marked up
more than 100 %. 8.2 now pays **procurement cost plus 50 % of the Net Amount** (invoiced amount less
procurement cost), so each side carries half the cost and the break-even falls to 2L − C, about a
30 % markup on tier A. 8.4 now measures the **EUR 1.500 minimum on our share**, not on total
receipts. 8.7 splits the three no-document cases (declined before procurement / definitive "not
available" after procurement / our own failure). 8.3 kept, adapted.

**Clauses 12 and 13 — liability.** 13.2 capped at "the fees paid by STP", which under the new 8.2
includes reimbursed procurement cost — inflating the cap to 2–3× actual earnings, worst where
margins are thinnest. Now caps on **Founders1's share under 8.2**, pass-through expressly excluded.
New **12.4** closes the larger hole: 13.1 accepts unlimited liability "for guarantees given" and
12.1 *warrants* provenance-metadata accuracy; under German law (clause 15.3) "warrants" can read as
*Garantie*, which would switch the 13.2 cap off entirely for machine-generated metadata. 12.4 states
clause 12 is a contractual obligation and not a Garantie.

**Annex 5 and clause 9.1 — pass-through.** 9.1 said STP imposes "the restrictions of clause 5" on
End Clients. Not performable: 5.2–5.5 are meaningless against an End Client who never touches the
API. 9.1 now points at **Annex 5**, eight terms STP carries into its own End Client terms *in
substance* — not verbatim, no disclosure of the Agreement, no privity with End Clients.

**The bank chain.** Founders1 → Septeo → bank → the bank's own customers, where the bank uses the
Documents **to evaluate its own customers**. The bank's customers are therefore *subjects*, not
recipients: no fourth tier, no sub-licence, no recursive pass-through. Annex 5(a) now says own-use
covers Documents *about* the End Client's customers; 5(c) now permits disclosure to a supervisory
authority and **to the company a Document concerns** (a bank showing a corporate customer what it
holds on it was previously a breach of its own terms); 3.4 names regulated institutions as
professional End Clients.

**Clauses 9.5 and 9.6 — DORA.** 9.5 puts supervisory requirements on STP and bars it agreeing audit
rights, route or sub-supplier disclosure, exit assistance, incident-reporting periods or register
entries on Founders1's behalf. 9.6 defines the cooperation that *will* be given: documentation and
certifications first, audits exercised **through STP**, satisfied by a report or pooled audit where
possible, on-site limited to the service and **not extending to procurement-route identity**
(clause 6.1), chargeable beyond the standard set.

**Consolidation.** End-client use was described in three places — 3.5, Annex 2.5, Annex 5(a)/(b).
Now: 3.5 is the grant, **Annex 5** is the single statement, Annex 2.5 is a pointer. The
upstream-licence limiter moved into Annex 5(b).

**Reseller characterisation.** A profit share rather than a purchase price is the classic indicator
that an arrangement is *not* a resale, which matters twice: § 89b HGB Ausgleichsanspruch by analogy,
and — more importantly — **DORA**. As a reseller, STP is the bank's ICT third-party provider and
Founders1 is STP's subcontractor, so the Art. 30 apparatus lands on STP. Under an agency reading
Founders1 would be supplying the bank directly. Fixes: 3.1 now carries "in its own name and **for
its own account**" (2.1 already did); 8.5 lets STP report by its own reference rather than naming End
Clients, closing the customer-base prong of the § 89b analogy; new **15.5** is an express
no-agency / no-Kommission / no-partnership clause, which the Agreement previously lacked entirely.
A phrase in 9.5 reading "Founders1 is the supplier of record" was corrected — it said the agency
position by accident.

**Do not concede in negotiation:** "Gross Revenue" is net of credits and refunds but **not** of bad
debt, so STP bears End Client credit risk. That is a load-bearing reseller indicator. The moment our
share is reduced by an End Client's non-payment, the agency reading strengthens and the DORA shield
weakens.

---

## 3. Smaller open items

1. **Additional-document surcharge amounts** (Danish articles, Israeli annual return) — outstanding
   on the supply side. Annex 2.3 promises them in "the price list in force"; Annex 2 cannot close
   without them, and the per-country choice between a standing rule and a per-case request depends
   on them. *Rescued from a deleted file; not yet recorded in the document.*
2. **Evidence level** — has STP confirmed whether their process distinguishes `document` from
   `certified`? It decides whether a French shareholder list is answered "not available" or with the
   €3 filing. Adding the field after they integrate is a breaking change. *Same provenance.*
3. **Contractual penalty** — the Agreement contains none. Clause 6.1 (non-circumvention) and
   clause 11 (confidentiality) rely on provable damage, and circumvention damage is close to
   unprovable. The 2024 Whitelabel agreement with STP Informationstechnologie carried EUR 25.000.
   Decide whether to add one.
4. **Procurement costs are in a document going to Septeo's procurement team.** Deliberate, per the
   earlier instruction, but it is the one number revealing our buying position, and the class table
   maps 1:1 onto the vendor's public bands — anyone comparing them identifies the supplier. Confirm
   this is still wanted.
5. **Term mismatch** — 14.1 commits 24 months; the upstream Order Form's initial term runs to
   12.04.2027 and 8.6 freezes costs for 12 months. Do not commit a longer firm term downstream than
   is secured upstream.
6. **German lawyer review** before signature, on the characterisation question specifically. The
   analysis in the internal notes is structural, not advice.
7. **If Septeo asks to make clause 13 mutual** — do not simply agree. Any cap they obtain must carve
   out breaches of clause 5, clause 6 and the Annex 5 pass-through: that loss is upstream-licence
   exposure and bears no relation to fee volume.
8. **Critical-or-important function** — once the bank is named, establish whether the service will be
   treated as supporting one. If yes, expect the full DORA Art. 30(3) catalogue and price the effort
   in; if no, 9.6 as drafted is probably sufficient.

---

## 4. Working notes

**Rendering.** The pack is HTML with `@media print` and `@page A4`. To produce a PDF, load it in
Chromium, `emulate_media("print")`, then `page.pdf(format="A4", print_background=True)`. Playwright
is available on **py -3.13**; PyMuPDF for reading the result back is on **py -3.9**. Neither
interpreter has both.

**Verify by reading the rendered PDF, not the source.** Two real bugs today were invisible in the
HTML. Clause numbers are CSS counters and cross-references are hand-typed, so after any clause
insertion re-check that every `Sec. n.n` still points where it should.

**A caution on text extraction.** Clause numbers are absolutely positioned `::before`
pseudo-elements, so the PDF text stream emits them out of visual order — a number read from the
stream belongs to the *previous* clause. Map numbers to text by shared baseline (geometry), or count
the clause divs in the source. Reading order alone gives the wrong answer and looks plausible.

**A CSS trap now fixed, worth knowing.** `ol.steps li` used `display:grid`. In a grid container every
element child becomes a grid item — including inline ones — so `<strong>` broke out of sentences and
a nested `<ul>` was placed in the 20px counter column. Replaced with `position:relative` +
absolutely positioned `::before`, and scoped to `ol.steps > li` so nested items keep their own
marker. If new markup misbehaves inside a grid container, this is why.

**Marketing repo.** An earlier parallel draft under
`BetterCoProductMarketing/BetterCo/Offers/Vertraege/STP-BI/` was deleted along with its folder; this
document superseded it. The marketing repo keeps the German Kanzlei-channel Offers and the
`cpq/style_master.py` Word pipeline — relevant only if Septeo's legal asks for a `.docx` to redline,
which is likely and which the HTML cannot provide.

**Contracting party.** STP **Business Information** GmbH (AG Mannheim HRB 110915, GF Fabian Padilla
Crisol, Laurent Rueff, Martin Ripke) is a different legal entity from STP **Informationstechnologie**
GmbH, the counterparty to the 2024 Whitelabel agreement. This is a standalone contract, not an
amendment; the 2024 agreement is referenced once in the preamble and nowhere else. Confirm Ripke's
sole representation authority — three managing directors are registered, so joint representation is
the GmbH default. Founders1's own register details in the pack (Berger Str. 224, 60385 Frankfurt,
AG Charlottenburg HRB 234373 B, VAT DE347408472) should be checked against the Handelsregister before
signature.
