# MEMO 2026-09-22 — STP's first commentary on the reseller agreement

**Status:** their legal read is in, our position sheet is written, the call is not yet scheduled.

## What arrived

**21.09.2026, 20:47** — Martin Ripke (STP Business Information GmbH), subject *"WG: Vertragsvorschlag
BetterCo Septeo"*, attachment **`Vertragsentwurf (erste Kommentierungen) BetterCo.docx`**.

- **22 comments, all by RAin Anja Nöth**, timestamps 21.09. 17:33–18:16.
- **Comments only. No tracked changes in the body text.** Nothing has been rewritten — this is a first
  legal read, not a redline, and every point is still as open for us as for them.
- Ripke: *"es gibt doch einige essentiellere Punkte die wir kurz klären sollten"*, asks for a slot.
  Eckhard replied 22.09. 07:05 offering **Wed or Thu, 13–17h**. No confirmation yet.

Our draft under review: `docs/SEPTEO_RESELLER_AGREEMENT_2026-09-14.{html,pdf,docx}` (17 pp, §§1–15 +
Annexes 1–5).

## The finding

Taken together the 22 comments do not ask for clause repairs — they describe **a different deal**:
a wholesale data purchase at fixed prices, with permanent storage and multi-client reuse in STP's own
data holdings, no group mechanics, no non-circumvention, and DE + AT carved out of the coverage annex.
Our draft is a per-case reseller agreement.

**The two comments that matter are one question, not two.** #20 (fixed prices) and #13 (Mehrfachnutzung
muss zulässig sein) cannot both be granted: we buy **per retrieval**, so a stored copy serving a second
end client is a second delivery nobody paid for. Any fixed price built on a pool assumption is wrong
within months. Settle that first — minimum, term, liability and §6 all follow from it.

**The lever is in their own file.** On §2 Subject matter, comment #4 reads
*"Registerinformationen auf Anfrage (Einzelfallbezogen)"* — their counsel wrote our model four clauses
before the comments asking for the pool.

## The 22, grouped

| Theme | Comments | Clause | Our stance |
|---|---|---|---|
| Fixed prices instead of the 50 % share | #20, #21 | §8, §8.2 | Accept — prices are already open to them from the deck; condition is *per Case* |
| Permanent storage, reuse for several clients | #6, #7, #9, #13 | §3.1, §3.5, §5.1 | Not for free; a priced reuse/pool licence or nothing |
| Minimum recalculated as a top-up on our margin | #22 | §8.4 | Accept their formula; it drops the 750 € ramp, and it only computes if they see our procurement cost |
| Cost changes: evidenced, capped, stable, symmetric | #23 | §8.6 | Give all four, including passing decreases on |
| DE + AT out of the coverage annex | #17 | Annex 2 | Grant — paired with §6 surviving |
| Delete §6 non-circumvention | #16 | §6 | No. §6 is the price of Annex 2's transparency; fallback 24 → 12 months |
| Delete §4 Septeo group scope | #11 | §4 | Ask what is meant; if "STP only", delete gladly |
| Explain §5.2 non-compete | #14 | §5.2 | Answer plainly, offer an express carve-out for their existing register business |
| No Annex 5 pass-through | #25 | §9, Annex 5 | Drop the annex, keep three obligations in substance, their wording |
| Wider warranty on content | #29, #30, #31 | §12 | Accept in substance; their #30 preserves our register-correctness carve-out |
| Liability cap rejected, no number given | #33 | §13.2 | Make them name it; ours = fees paid in the preceding 12 months |
| 6-month test phase | #35 | §14.1 | Tradeable: 6 months rolling into 24 unless terminated at month 6 |
| Define loss-of-supply triggers | #36 | §14.2a | Define: register closes/barred, or supplier lost with no replacement in 60 days |
| §3.2/3.3 and survival — "zu besprechen" | #8, #37 | §3.2, §3.3, §14.4 | Answer and ask back; what they want to build on the API also reveals how serious the pool ask is |

## Deliverables from this session

- `docs/SEPTEO_REVIEW_RESPONSE_2026-09-22.html` — negotiation sheet, EN, 4 pp A4, house style.
  Artifact: <https://claude.ai/artifact/D8cvvFPnyuzWe9ry69GvWG>
- `docs/SEPTEO_REVIEW_RESPONSE_2026-09-22_DE.html` — same sheet in German, with their counsel's
  wording verbatim so it can be read out in the call.
  Artifact: <https://claude.ai/artifact/GAiiEg4GcJqHUssyn1SouK>

Both are **internal — not for the counterparty**; every footer says so. Both artifacts are private
until shared from the page's Share menu. Neither names the upstream supplier: the §6 section speaks of
"the supply terms upstream of us", so an accidental screen share costs nothing.

**Not done:** PDF render (Playwright on `py -3.13`) — offered, not requested.

## Four questions to take into the call

1. Case-by-case or pool? Their §2 comment and their §3/§5 comments say opposite things.
2. §4 deleted — STP alone, or the whole group without the accession mechanics?
3. What liability figure do they actually want?
4. What do they intend to build on the API? ("Zu besprechen" on §3.2/3.3.)

## Open, and unchanged by this review

- The upstream resale bar is still the hard gate, and comment #13 makes it worse, not better.
  Permanent multi-client reuse is further from what our supply terms allow than per-case resale is.
- AGB risk from the legal review brief now applies to the conduct of the negotiation, not just the
  drafting: if this is read as AGB, §13.2, §12.2 and §5 are the clauses at risk under § 307 BGB, and
  light resistance is not agreement. **Minute each call** — which clauses were discussed, what each
  side proposed, what was conceded for what — and send a short written summary the same day.
