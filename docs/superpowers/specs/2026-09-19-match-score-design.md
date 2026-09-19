# Match score in the Document Search API — design

**19 September 2026, revision 2.** Branch `feat/match-score` in `betterco-backend`, worktree
`C:/bcwt/match-score`, off `origin/dev@3a3345605`. Target release: 1 October.

**What it is:** a free endpoint that answers "is this registry entry the company in your record?" before
the caller spends money on a case, returning every candidate it considered, with the rule that ranked
them published and versioned.

**Why now:** Septeo (Eric Misfeld, 17 September) do not want to open a case below a score threshold. The
score exists today only as a hand-built column in our September simulation. Of the two options they
offered, the chosen one puts the score in front of the caller and leaves the decision with them: a
threshold inside our `create` would refuse orders silently and move a rule the caller owns into our
release cycle.

**What changed in revision 2.** Revision 1 performed one lookup, by name, and compared the caller's
number against the hits. That cannot detect the case that motivated the whole feature: a name search for
"Sur la Pree B.V." never returns Barcarolle Holding B.V., so the number pointing at a different company
goes unseen and the row scores 85. The number must be resolved **independently of the name** — as the
simulation did ("gesucht haben wir mit eurer Registernummer bzw. mit mehreren Namensvarianten"). Revision
2 therefore performs up to two lookups and returns the candidates rather than one opaque winner.

---

## 1. Surface

Two endpoints, both free reads. Creating a case remains the only billable action.

```
POST /restapi/v1/workspaces/{workspace_id}/document-search/match
GET  /restapi/v1/workspaces/{workspace_id}/document-search/match/rules
```

### Request

```json
{ "jurisdiction": "NL", "name": "Sur la Pree B.V.", "registerNumber": "24175625" }
```

| Field | Required | Notes |
|---|---|---|
| `jurisdiction` | yes | ISO 3166-2, as everywhere else in this API area |
| `name` | yes | the caller's company name, as they hold it |
| `registerNumber` | no | absent is legitimate, and scores 85 at best |

No address, no legal form. Every additional input is another rule to publish, and no band needs them.

### Response

```json
{ "score": 70,
  "bandId": "NUMBER_AND_NAME_CONFLICT",
  "rulesVersion": "2026-09-19.2",
  "checkable": true, "orderable": true, "automated": true,
  "selection": "a conflict governs; otherwise the highest band; ties to foundBy=NUMBER, then nameMatch=EQUAL, then first returned",
  "signals": { "lookups": ["NUMBER", "NAME"], "numberSupplied": true,
               "numberComparable": true, "candidateCount": 2 },
  "candidates": [
    { "foundBy": "NUMBER", "score": 70, "bandId": "NUMBER_AND_NAME_CONFLICT",
      "rawname": "Barcarolle Holding B.V.", "externalCode": "24175625",
      "companyStatus": "Active", "dataSource": "…",
      "signals": { "numberMatches": true, "nameMatch": "DIFFERENT", "scriptDiffers": false } },
    { "foundBy": "NAME", "score": 85, "bandId": "NAME_ONLY",
      "rawname": "Sur la Pree B.V.", "externalCode": "54406951",
      "companyStatus": "Active", "dataSource": "…",
      "signals": { "numberMatches": false, "nameMatch": "EQUAL" } }
  ] }
```

Each candidate carries its own score, band and signals. The top-level score is the best of them under
the published `selection` rule — which is stated in the response, not only in documentation, because a
ranking nobody can see is the same problem as a score nobody can audit.

**A conflict governs, and this was a correction found while implementing.** Revision 2 first
published "highest band wins". Writing the scorer showed that wrong: in the Sur la Pree case the
candidates are Barcarolle at 70 and the real Sur la Pree at 85, so the highest band reports **85** — a
reassuring score for exactly the record whose number points at somebody else. A
`NUMBER_AND_NAME_CONFLICT` therefore outranks everything, and `match-rules.json` states that and its
reason. The same ordering sorts the candidate list, so the order a caller reads is the ranking that
chose the score.

Candidate fields reuse `KycSearchResult` exactly, so a caller who already consumes `cases/search` needs
no new model. `candidates` is an empty array when nothing was found. Every `signals` field is present on
every response; inapplicable ones are `null` rather than omitted, so nobody has to tell *false* from
*absent*.

---

## 2. How it works

### Up to two lookups, both free

Both use the existing free vendor search (`POST /v2/Companies/search`, wrapped by
`KycGatewayService.search(jurisdiction, query, datasource)`).

1. **By number**, when `registerNumber` is supplied and the jurisdiction's id scheme is comparable
   (§4). Answers "whose company is this number?" independently of the name.
2. **By name**, always. Answers "is there a company by this name?"

Results are merged and de-duplicated on `externalCode`; a company found by both carries
`foundBy: "NUMBER"`. `signals.lookups` records which ran, so a caller can see whether the number was
resolved at all. Two searches roughly double the latency of one; both are free, and the caller is about
to spend money, so the trade is worth stating but not agonising over.

### The join key is `externalCode`

`KycSearchEnrichment.registryId` is documented as "the company's registry id (same value as
`externalCode`)", with an `idScheme` decoder covering CRN, CIN, OGRN, USCC and UEN. So `numberMatches`
is a comparison against data the lookups already returned — no additional vendor capability.

### The bands

Scored per candidate; the response's top-level score is the best of them.

| Score | `bandId` | Condition |
|---|---|---|
| 100 | `NUMBER_AND_NAME` | this candidate's `externalCode` equals the number **and** its name equals theirs |
| 95 | `NUMBER_RESOLVES_SCRIPT_DIFFERS` | number matches, names differ, and the two names are in **different scripts** |
| 85 | `NAME_ONLY` | found by name; the number matched nothing, or none was supplied |
| 70 | `NUMBER_AND_NAME_CONFLICT` | the number resolves to this company **and** the name resolves to a different one |
| 70 | `NUMBER_RESOLVES_OTHER_COMPANY` | the number resolves here, the name differs in the same script, and no competing name candidate exists |
| 10 | `NO_HIT` | neither lookup returned anything |
| 0 | `NO_COMPANY_REGISTER` | the number matches a published non-company-register pattern for this jurisdiction (§4) |

Two ids share the score 70 deliberately. The score is what a threshold compares against and Septeo have
already seen these six numbers; the id is what tells them *which* kind of doubt they are looking at.
`NUMBER_AND_NAME_CONFLICT` is the stronger evidence — two lookups, two different companies — and it is
the Sur la Pree case.

**Where the script rule now sits.** In revision 1 it carried the whole 95/70 split. With the number
resolved independently, the conflict case identifies itself, and script only separates 95 from 70 when
there is no competing name candidate to compare against: different scripts mean the names cannot be
compared and the number is treated as authoritative (the Bulgarian rows, same company in Cyrillic); the
same script and a different name mean the number points elsewhere. No similarity metric, and no
transliteration table that would itself need publishing.

### Name normalisation, published with the rules

Applied to both sides before comparison, in order:

1. trim, then collapse internal whitespace runs to one space
2. uppercase with `Locale.ROOT`
3. remove diacritics (NFD, drop combining marks)
4. drop punctuation `. , ' " ( ) -` and substitute `&` → `AND`
5. strip **one** trailing legal-form token from the published per-jurisdiction list (`B.V.`, `GMBH`,
   `LIMITED`, `LTD`, `S.L.`, `S.À R.L.`, …), at the end only

`nameMatch` is then `EQUAL` or `DIFFERENT`. There is deliberately no fuzzy score: a continuous 0–100
invites a threshold nobody can reason about, whereas a band can be argued about in words.

---

## 3. Transparency as a code property

The band table, the selection rule, the legal-form tokens and the non-company-register patterns live in
**one versioned resource file**, `src/main/resources/kyc/match-rules.json`, carrying a `rulesVersion`.

- `MatchScoringService` reads it.
- `GET …/match/rules` serves it verbatim.
- A test fails if the file the scorer reads and the file the endpoint serves are not the same resource.
- Every scored response carries the `rulesVersion` that produced it, and a test pins the current value so
  a rule change cannot ship without bumping it.

**The trap this closes:** a caller sets a threshold at 85, we later change how a band is computed, and
their threshold silently means something else with nothing failing visibly. Published and stamped, that
change is diffable instead of invisible.

---

## 4. Three answers, not one

**The score and the candidates** — §2.

**Whether a check was possible.** Where the jurisdiction has no searchable index there is nothing to look
the company up in: `checkable: false`, `reason: NO_SEARCHABLE_REGISTRY`, `score: null`,
`automated: false`. Driven off the **same** `isAutomated(jurisdiction)` helper that already gates
`cases/search` (`KycGatewayService:983`), so the two can never disagree. A `200`, not an error —
un-checkable is a real answer, six of the twenty simulation rows were un-checkable, and all six were
still orderable.

**Whether it may be ordered at all.** Germany returns `orderable: false`,
`reason: JURISDICTION_NOT_AVAILABLE`, from the same `document-search.deny-jurisdictions` list the create
path enforces. Without it a caller scores a German company successfully and then meets a blind `409`.

### Preconditions — to be confirmed, with defined fallbacks

Three assumptions this design rests on, none of them yet measured. Each has defined behaviour if it
fails, so none is a TODO:

| Assumption | If it does not hold |
|---|---|
| The vendor's `query` accepts a **register number**, not only a name | The number lookup is impossible. `signals.lookups` omits `NUMBER`, `numberComparable: false`, band 85 at most — i.e. revision 1's weaker behaviour. Resolving numbers would then need our own per-jurisdiction connectors, which is **well past a 1 October change**. |
| `externalCode` is the registry number in the jurisdiction concerned | The number cannot be compared there: `numberComparable: false`, band 85 at most. Confirmed jurisdictions are listed in `match-rules.json`; absent from the list means not comparable. |
| Non-company registers are recognisable from the number's shape | Band 0 is simply never produced for that jurisdiction, which is correct rather than a gap. |

**One free sandbox search settles the first two** — `query=00364890` for GB. If Cropwell Bishop comes
back, both hold and this design is buildable as drawn. That same call also reveals which vendor staging
is talking to, which is worth doing first for an unrelated and more urgent reason.

---

## 5. Errors

The existing envelope, code in `message` (`RestApiExceptionHandler`):

| Status | `message` | When |
|---|---|---|
| 422 | `jurisdiction_required` | missing, or not a known code |
| 422 | `name_required` | missing or blank |
| 503 | `upstream_unavailable` | the vendor search is not answering |
| 504 | `upstream_timeout` | the vendor search timed out |

If the **number** lookup fails upstream but the name lookup succeeds, the call returns `200` with
`signals.lookups: ["NAME"]` and `numberComparable: null` — a partial answer beats an error, provided it
says which half is missing. Only both halves failing produces a 5xx.

Not errors: a non-automated jurisdiction, a German company, and a zero-hit search all return `200` with
the relevant field set. `search_not_supported` is deliberately not reused — it is right for
`cases/search` and wrong for a call whose purpose is to say what can and cannot be checked.

---

## 6. Where the code goes

| Unit | Responsibility | Depends on |
|---|---|---|
| `MatchScoringService` | pure: (caller record, candidates, rules) → per-candidate bands, best, selection trace. No I/O | `MatchRules` |
| `MatchRules` | loads and validates `match-rules.json`; bands, selection rule, tokens, patterns, version | — |
| `CompanyMatchService` | orchestration: automated? deny-listed? run one or two lookups, merge, de-duplicate, delegate | `KycGatewayService`, `MatchScoringService` |
| ~~`MatchApiImpl`~~ | **Not built, and cannot be.** `useTags=true` generates one interface per tag and
`KycApiImpl` already implements `DocumentSearchApi`, so a second class cannot implement half of it. The
two methods are two-line delegations in `KycApiImpl`, which is why `MatchResponses` was extracted: the
mapping is unit-tested, the controller is glue. | `CompanyMatchService` |
| `MatchResponses` | pure: domain result → the published DTOs. Where a field quietly fails to travel | the generated domain |
| `MatchConfiguration` | the three beans; the rules are a startup singleton that fails the context if the resource is missing | — |

Declared contract-first under the existing `Document Search` tag, so the endpoints appear in
`apidoc.html` beside the rest and Septeo can regenerate their client. The scorer being pure is the
point: the whole band table, the merge and the ranking are testable without a vendor, a database or a
Spring context.

---

## 7. Tests come from measured data

The twenty rows Fabian Puls sent on 9 September and our answers of the 11th become the fixture —
`src/test/resources/kyc/match-vectors.json`:

| Case | Expected |
|---|---|
| Sur la Pree B.V., NL, `24175625` | two candidates; best = 70 `NUMBER_AND_NAME_CONFLICT`, Barcarolle by number, real Sur la Pree (`54406951`) by name |
| the two Bulgarian rows | 95, `scriptDiffers: true`, one candidate |
| Modern Hero Academy, AT, ZVR number | 0, `NO_COMPANY_REGISTER` |
| the six rows with no country code | `checkable` per jurisdiction; no crash on a null number |
| any German company | `orderable: false` |
| the seven clean rows | 100 |
| a company returned by **both** lookups | one candidate, not two — de-duplicated on `externalCode`, `foundBy: NUMBER` |
| two candidates in the same band | the published tie-break decides, and the test asserts the order |
| the number lookup 503s, the name lookup succeeds | `200`, `lookups: ["NAME"]` |

Plus: the rules file is served byte-identical to the one the scorer reads, `rulesVersion` is pinned, and
one integration test through the real filter chain proves the endpoint is reachable and refuses an
unauthenticated caller — the gap that once let an endpoint pass 101 unit tests while being uncallable.

---

## 8. Cut, and why

- **Per-partner configurable rules, and a minimum-score gate inside `create`.** Both were asked for.
  Published, versioned rules plus the caller's own threshold cover the need, and a threshold inside our
  create refuses orders silently — the failure mode this design exists to avoid.
- **Fuzzy similarity scoring.** Bands are arguable in words; a percentage is not.
- **Address and postcode signals.** More inputs, more published rules, no band that needs them.
- **Transliteration.** §2's script rule makes it unnecessary.
- **More than two lookups** — name variants, for instance, which the simulation used by hand. It would
  raise recall on band 85 and it is a defensible later addition, but each variant is another published
  rule and another call.

## 8b. Built, and what is verified

As of 19 September, on `feat/match-score` (`cc26463b6`), seven classes and **65 tests**: the
normalisation, the published rules, the scorer, the orchestration, the gateway adapter, the simulation
vectors and the response mapper. Each report's timestamp was checked against the clock, twice after a
stale surefire report reported a class green that had not run.

**Five corrections came out of writing it, not out of reviewing it:**

1. A conflict must govern the ranking - "highest band wins" reported 85 for Sur la Pree.
2. The scorer must not claim a number resolved when the lookup that would have resolved it failed.
3. The deny list must have one reading, not a copy in the adapter.
4. A company **in liquidation is the same company** - the vectors caught row 7 scoring 70 because the
   Firmenbuch appends "in Liqu." to the name. Those are the rows the customer called the most
   interesting for a monitoring test, so a threshold would have discarded exactly them.
5. `MatchApiImpl` cannot exist under this generator; see §6.

**Not verified, and not claimable:** the full unit suite has not run to completion (the background run
was killed for system memory pressure before any test executed) and the Spring context has never been
started. A targeted check stands in for the first: no test constructs `KycApiImpl`, so the constructor
change cannot break one. The integration test in §7 needs Docker and has not been written.

## 9. Still open

- **The three preconditions in §4**, the first of which decides whether this is a 1 October change at all.
- **Septeo's threshold**, and whether they adopt the bands as published. Asked in the 17 September draft,
  not in the version sent on the 18th. Not a blocker — they set their own threshold against published
  rules — but worth one line when the call happens next week.
- **Recall on band 85** is inherited from the vendor's own name matching. Where only a name lookup is
  possible, what we get to evaluate is what they chose to return.
