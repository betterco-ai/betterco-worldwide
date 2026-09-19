# Document search — status for the go-live decision

**17 September 2026. Go-live 1 October — 14 days.** For the owner of the date, not for the
engineers. The working detail is `HANDOVER_2026-09-14.md`; the phase view is
`MEMO_2026-09-11_PHASE_STATUS.md`.

**Updated 17 September:** the work merged on 16 September and deployed itself to the dev
environment. Two things need checking today as a direct result — see *What the merge changed*.

---

## In one paragraph

**The software does what it was built to do, and it is now on the dev environment.** On 15 September
it was run end to end against the vendor's test system and did all of it: placed an order, refused
the orders it is supposed to refuse, recorded what each order costs, fetched the documents, filed
them under the client, and served them back under BetterCo's own identifiers rather than the
supplier's. One defect was found and fixed in the process. On 16 September the nine changes merged
into `dev` as a single change (#2319), which automatically deployed to the dev environment.

**What has still not happened:** the customer has not been told the interface is changing, staging
cannot be used, and no real registry document has ever passed through the system — every file used in
testing is the same 904-byte placeholder the vendor's test system returns.

---

## What the merge changed, and what to check today

Merging lifted the standing "nothing goes into dev" rule. That rule existed for one reason, and the
reason has not gone away.

**1. The ordering screen on dev may now have dead links.** The case list returns a different field
than it used to — `caseId` where it used to say `caseCommonId`. Any screen still reading the old
field gets nothing back. If the front-end change did not ship in the same window, the ordering screen
on dev is broken right now. **This is the first thing to verify**, and it is a five-minute check for
whoever owns that screen.

**2. Dev will show the old document identifiers, and look like the change did not work.** Filing
documents under the client is controlled by a setting that no deployed environment turns on — dev has
only ever had it from a hand-typed flag. So on the dev environment the documents are ordered but
never filed, and the supplier's identifiers are served instead of ours.

The effect is the worst of both: **the disruption of the change without the benefit of it.** Anyone
testing dev this week will reasonably conclude the identifier work did not land. It did; it is one
line of configuration away from being visible.

Turning it on for **dev** is a small, safe change — dev already creates client records, orders there
are free, and it is the environment whose job is to test. Turning it on for **staging and
production** is the open business decision below, and a different question.

---

## What was tested, and passed

Run on 15 September on a developer machine, against the vendor's test system. No money was spent;
test orders are free and were confirmed as such before anything was ordered.

| What was proven | Why it matters commercially |
|---|---|
| An order can be placed and completed | The core of the product works |
| An order for a German company is refused | Germany is sourced by BetterCo directly. Ordering it from the vendor would buy something we already own — this refusal is money not spent |
| Every order records what it cost, at the moment it becomes chargeable | Spend can be attributed afterwards. Until this was built, it could not be |
| Test orders record "not billable" rather than a price | The cost figures will not be inflated by test activity |
| Documents are fetched, filed under the client, and served back | The end-to-end path a customer actually uses |
| Documents carry BetterCo identifiers; the supplier's identifiers are rejected | This is the change that lets us switch supplier later without breaking customers |
| A document cannot be read through the wrong case | Basic separation between customers' records |
| Each document carries its own filing date | Needed for "is this document current?" decisions |
| Re-requesting a document serves the stored copy and does not re-buy it | Prevents paying twice for the same document |
| The price table matches the vendor's current published prices | Quotes and cost records are based on current figures, not August's |

**One defect was found and fixed.** In an environment that has not yet stored any documents, the case
list either failed outright or silently returned nothing. That is precisely the state a brand-new
environment is in on its first day — so this would have been the customer's first impression of the
feature. It is fixed, with a test to stop it returning, and both are in the merged change.

---

## What has not been tested, and cannot be yet

| Not proven | What it would take |
|---|---|
| **The feature on a shared environment** | It is deployed to dev as of 16 September, but nothing above has been re-run there. Every result in this memo comes from one developer's machine |
| **A real registry document** | Every test file is the same 904-byte placeholder. The pipeline is proven; carrying a genuine document through it is not. One paid order settles this and nothing else can |
| **The spending safeguard actually firing** | A safeguard exists that refuses to start the system if it is pointed at the paying vendor by mistake. It has never been seen to trigger. A safeguard nobody has watched work is an assumption, not a control |
| **Staging** | The staging environment is missing a credential it needs (confirmed against Azure on 15 September). Until it is added, every vendor call there fails |
| **Real timings** | The 25-minute / 40-minute / 24-hour figures quoted to the customer have never been measured against the live vendor |

---

## The decision that is still open

There is a setting that controls whether the system creates a client record when an order is placed,
and a second that controls whether ordered documents are filed. Dev has the first; no deployed
environment has the second.

**Without both, documents are ordered but never filed** — and the customer is served the supplier's
document identifiers instead of ours. In other words, the headline change of this release silently
does not happen. This was measured both ways on 15 September: off, nothing was stored; on, everything
worked.

Two consequences the decision-maker should know:

1. **Turning it on later does not fix orders already placed.** Cases ordered while it is off are never
   filed retrospectively. An environment containing both kinds of case shows both sets of
   identifiers at once, which reads to a customer as the change having half-shipped.
2. **It has to be decided before the customer is invited in**, not after. Inviting them into an
   environment with the setting off demonstrates the old behaviour.

This is a business decision about which environments file documents and create client records, not an
engineering one. It is item **M5** on the open list and has been open since early September.

---

## Also needing a person, not a commit

| | Item | Status |
|---|---|---|
| 1 | **Tell the customer the interface is changing** | Note drafted 11 September, **still unsent**. Corrected on 17 September — an earlier version described the change inaccurately in two places. The change is now live on dev, so the window for "we told you first" is closing |
| 2 | **The staging credential** | Missing. Must not be worked around by pointing staging at the paying account — that turns every customer test order into a real, billed order |
| 3 | **One paid order** | The only way to prove a real document survives the pipeline. Also settles three other open questions. Needs explicit approval — it costs money |
| 4 | **The United States price** | Priced per US state; our table cannot represent it in one row. A priority market for the customer |
| 5 | **The nine superseded branches and their pull requests** | The work merged as one squashed change. The originals are now redundant and should be closed so nobody reviews or merges them a second time |

---

## Overall status

**Build: done. Merged and on dev: done. Proven on a shared environment, and everything commercial:
not yet.**

| | |
|---|---|
| Nine changes written | **merged 16 September as #2319** |
| Deployed | **dev environment only, automatically on merge** |
| Feature proven end to end | **on one developer machine; not yet re-run on dev** |
| Money safeguards | **built and correct in configuration; never watched to fire** |
| A real registry document | **never retrieved** |
| Customer informed | **no** |
| Staging usable | **no — missing credential** |
| Days to 1 October | **14** |

**The honest read on the date.** The engineering risk is low: the feature works, the one defect found
last week was found and fixed, and the merge — the thing identified as the schedule risk on
5 September — is done. What remains is a decision that has been open for two weeks, a credential
someone has to create, a note someone has to send, and one paid order someone has to approve. None of
those is hard; all of them need a named person, and none can be done by the engineer who wrote the
code.

**This week, in order:** check the ordering screen on dev, turn document filing on for dev so the
change is actually visible there, send the customer note, and decide M5 for staging.

**One date worth noting:** the vendor's test system expires **19 October**, eighteen days after
go-live. Testing after that point requires either a renewal or the paid account.
