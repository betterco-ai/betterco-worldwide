# Document Search API — what's new

**For:** STP team · **Date:** 14 July 2026 · **Environment:** staging (`stg.betterco.ai`)
**Status:** DRAFT — internal review before sending

---

Four additions are live on the Document Search API in staging. Together they answer the two
questions that previously required either a guess or a purchase: *"what will I get for this
jurisdiction?"* and *"is my document ready yet?"*

All four are **free calls** — none of them place an order. Ordering a case remains the only
billable action.

## 1. See what a jurisdiction covers — before you order

`GET …/jurisdictions/{code}/coverage`

For any jurisdiction, you now get the retrieval **SLA**, the **source registries**, the **data
fields** returned, and the documents split into **base** (provided as standard) and **additional**
(on request, may cost extra).

The spread is wide and worth knowing up front: the UK returns in **25 minutes** with around ten
base documents; other jurisdictions quote **24 hours** and a single registry extract. Checking
coverage first sets the right expectation before anything is ordered.

**128 of 131 supported jurisdictions have a coverage entry.** Three (Afghanistan, Bangladesh,
Ghana) have no coverage data available and return a 404 — they are still orderable, but we cannot
describe the outcome in advance.

## 2. One call for the whole picture

`GET …/jurisdictions/coverage`

The same detail for **every** jurisdiction in a single call — intended for building an overview
screen or an internal reference table without making 128 requests.

## 3. Track documents while a case is still building

Add `?includePending=true` to the documents list (and to the download call).

Previously the document list stayed empty until a case reached **Ready**. You can now see the
documents **as the case is being built**, each tagged:

| Tag | Meaning |
|---|---|
| `available` | Retrieved — download it now |
| `pending` | Still being retrieved — keep checking |
| `missing` | Not obtainable for this case |

This turns a silent wait into a progress view. One caveat worth designing around: a `missing`
entry is a **placeholder describing a gap** — it names the document but carries no download link,
because there is nothing to fetch.

## 4. A free location and type check before you buy

Company look-up results now carry an **`enrichment`** object, decoded from the registry identifier
itself: entity type, incorporation year, city/region, listed status, and a one-line summary. It
costs nothing and needs no order.

It is most valuable exactly where the registry is least forthcoming. **India** is the clearest
case: the registry returns only the state ("Maharashtra"), but the CIN decodes to give you the
city as well —

> *Listed Public Limited Company · Mumbai / Pune (Maharashtra) · est. 1995*

— enough to confirm you have the right entity before spending anything.

**Depth varies by jurisdiction, by design.** India and Germany decode richly (type, city, year).
The UK, China, Argentina, Hungary and Singapore return the identifier scheme and a summary.
Elsewhere the object falls back to the registry's own data — the identifier and the country. It is
a **confirmation aid, not a guarantee**: treat a rich result as a useful check, and its absence as
neutral rather than a red flag.

---

## Known limits today

Being straight about the current edges:

- **Malaysia look-up is unavailable.** Searches time out rather than return results. Ordering is
  unaffected — you can still create a Malaysian case by entering the company details directly.
  We have this open with the registry provider.
- **Cayman Islands look-up finds companies but cannot be ordered from directly.** Results come
  back (in around 60–70 seconds, so allow for the wait), but they arrive without the registry
  identifier that an order needs. For now, Cayman cases need their details entered manually.
- **Look-up is available in 44 of 131 jurisdictions.** The remainder are manual by nature — you
  supply the company details rather than picking from a search result. This is a property of the
  underlying registries, not a gap in the API.
- **Broad searches are rejected, not truncated.** A very common name may come back with *"More
  than 200 records found — please refine your search criteria."* That message is the registry's
  own, and the fix is a narrower query.

## Also landed

The **legal-form reference data** is now ingested: `…/legal-forms` returns **414 forms across 96
jurisdictions**, up from 14 jurisdictions previously. This is what maps a local legal form
("GmbH", "S.L.") to the values a new case expects, and it substantially widens the jurisdictions
where a case can be created without guesswork.

## Next

- Confirming the extra company detail fields (second address line, province, registry number,
  unregistered-entity flag) are carried through on manual orders.
- Malaysia look-up and the Cayman identifier gap, both with the registry provider.

Questions or anything you'd like prioritised — let us know.
