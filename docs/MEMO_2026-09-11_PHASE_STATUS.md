# Memo — where the aggregator stands after two unattended rounds

**11 September 2026. Internal.** Go-live 1 October.

This maps what the nights of 9 and 11 September produced onto the programme phases, because the two
do not share a vocabulary and that has already caused confusion. Working detail is in
`HANDOVER_2026-09-11.md`; the programme itself is `aggregator-roadmap.html`.

---

## 1. Read this first: two things called P4 and P5

The overnight rounds were named after the night — "the P4 round", "the P5 round" — and the programme
phases are also numbered P1 to P6. **They are different things and they do not line up.**

| | Means |
|---|---|
| **Phase P4** | Cost. Charge records, `PER_CASE` for kyc.com |
| **"the P4 round"** | the night of 9 September, which happened to build phase P4 *and* part of P5 |
| **Phase P5** | The aggregator becomes a router: `SourceAdapter` port, routing table, per-source policy |
| **"the P5 round"** | the night of 11 September, which moved parts of P4 and P5 but is not phase P5 |

From here on: **rounds are dates, phases are phases.**

## 2. Phase status

| # | Phase | Status |
|---|---|---|
| P1 | Client and matter | **Met 4 September**, live on `dev` |
| P2 | Acquisitions and ingestion | **Met 8 September.** Caveat unchanged: every sandbox file is the same 904-byte stub |
| P3 | Contract cut-over | **Met 8 September**, verified on dev. Septeo still has not been told |
| P4 | Cost | **Built 9 September. Exit criterion unproven** — "ten documents, one charge" needs a real multi-document order |
| P5 | The aggregator becomes a router | **Half met.** Germany enforced not remembered; per-source policy has a second member. Port and routing table not built |
| P6 | Sources — France, Britain | Not started; out of the go-live by the 5 September scope cut |

Nine branches stand behind this, **none merged, nothing deployed, no money spent.**

## 3. What the two nights actually moved

**9 September.** A startup assertion that refuses to run ordering against the paying vendor outside
production; the charge record; `contentDate` written for the first time; the pre-Ready path refusing
the wrong vendor world; the Germany deny-guard.

**11 September.** `dev` absorbed into the stack after it had drifted three commits; the price table
refreshed from the live coverage page; D1's reuse window built; `document-search.create-client`
written into the shipped configuration with a ratchet over the four flags whose failure mode is a
bill.

## 4. Two corrections the roadmap carried on 8 September are now retired

- **`contentDate` was declared and never written**, so the reuse rule could only read the fetch clock.
  Both clocks now exist.
- **The cost meter was not instrumented**, and that gap lost data permanently while it waited. Every
  order now records amount, currency, band and `chargedAt`.

Two decisions inside those are worth keeping in mind because they shape how the numbers read. The
recorded amount is a **list price**, never an invoiced one, and it says so in the record. A sandbox
order records `NOT_BILLABLE` rather than a price that was never paid.

## 5. What the price refresh exposed

The table feeding those cost records held the pre-26-August list. Refreshing it found the drift was
worse than the note on file said: **nine band changes, not three**, and **26 jurisdictions missing
outright** — 131 rows to 157.

Nothing was mis-invoiced, because the figures are labelled list prices and our purchase rates come
from the Order Form of 13 April, which did not change. What a band change moves is *which contract
rate applies*. But any figure quoted from that table before 11 September was quoting an out-of-date
shape of the vendor's catalogue.

**The United States is still wrong** and cannot be fixed from that page: it is priced per state, and
one row cannot represent it. It is an STP priority market.

Method note for whoever refreshes it next: **do not use a summarised web read.** Two separate reads
of the same coverage page returned 145 of 152 rows and contradicted each other. The file was rebuilt
by parsing the page's HTML directly, and the generator refuses to write if any jurisdiction fails to
map to an ISO code.

## 6. The reuse window, and the thing it revealed

D1 is implemented as a per-source window on `fetchedAt`, default seven days, **flag off by default**.
It sits on the serve path, which is the only place a stored copy is handed to a reader — the
ingestion worker drops every case after 24 hours, so a window measured in days could never have fired
there.

**Cross-customer reuse is not built and cannot be yet.** Serving customer A's document to customer B
needs an identity for the *company* that survives across clients, and the record carries none:
vendor document ids repeat across cases and mean different things, and jurisdiction plus company name
is not an identity. D6 — whether the vendor's licence even permits it — is also still unasked.
**That missing key is the open decision, not the window.**

One consequence is deliberately unresolved: a refresh stores a new document and leaves the previous
one behind. That is the orphaned-document problem in a new place, and it is why the flag is off.

## 7. What still needs a person

1. **Tell Septeo.** The P3 contract change plus the two refusals added on 9 September. Drafted in
   `SEPTEO_CONTRACT_NOTE_2026-09-11.md`, unsent. Until it goes, "one break" is an intention.
2. **The vendor-config inversion.** The dangerous configuration now fails loudly at startup; the safe
   one is still not the default, because nobody has confirmed how production starts.
3. **A real registry document.** Still never retrieved. One billable order settles it and nothing else
   can.
4. **The United States price**, and confirmation of the four jurisdictions the vendor has delisted —
   AF, BD, GH and Saudi Arabia.
5. **The cross-client company key**, if reuse is to go beyond same-client freshness.
6. **M5** — which environments get client creation.
