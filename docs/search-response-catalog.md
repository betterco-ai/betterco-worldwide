# KYC.com search response — catalog & enrichment potential (by jurisdiction)

A **persisted, extensible** record of what the free KYC.com search actually returns per
jurisdiction, so we know (a) the **standard** that always comes back and (b) what we can
**enrich** per country (like India's CIN → city).

- **Coverage (last sweep):** **39 / 44** automated jurisdictions observed. 5 return HTTP 500 even for flagship companies (`AU FI FR KY MY` — need a real company name, see Reliability below); 3 (`CY GR NO`) only fail on generic queries and work with a real name.
- **Live data:** `docs/search-catalog.json` (one record per automated jurisdiction).
- **Refresh/extend:** `python scripts/search_response_sweep.py [CODES…]` — free, re-runnable,
  merges into the JSON (fills in jurisdictions that timed out last run).
- **Sourcing note:** the `externalCode` / address rows below are **observed** from live searches.
  The "enrichment potential" column is what the ID *scheme* can encode — **verify per decoder
  before shipping** (except India, already shipped, and CN, whose USCC region code we observed).

---

## The standard (every result, every jurisdiction)

| Field | Always? | Notes |
|---|---|---|
| `rawname` | ✅ | company name |
| `externalCode` | ✅ | the **national registry / tax ID** — format differs per country (this is the enrichable part) |
| `rawAddress` | usually | **granularity varies a lot** — country → state → city (see below) |
| `companyStatus` | usually | Active / Dissolved |
| `street`, `city`, `zip` | ❌ rarely | **empty in practice** — everything is in `rawAddress` |
| `dataSource` | sometimes | e.g. CA = `Ontario`, HK = `IRD`/`HKCR` |

**Key finding:** the standard is thin — name + a registry ID + one address string + status. The
parsed city/zip fields are **not populated**, so you cannot rely on them. Everything worth
deriving is either in `rawAddress` (coarse) or encoded in `externalCode`.

**Address-granularity spectrum (observed):**
- **Country only** — AR (`Argentina`), BE (`Belgium`), BZ (`Belize`) → worst case
- **State/province** — IN (`Telangana`)
- **City** — AT (`Wattenberg`)
- **City + region** — CA (`Ottawa, Ontario`), CH (`Vandoeuvres, Switzerland`)

Where the address is coarse, the **`externalCode` is the only way to recover location** — exactly
the India case.

---

## Per-jurisdiction (observed sample + enrichment potential)

| Code | Observed `externalCode` | Address | ID scheme | Enrichment potential | Status |
|---|---|---|---|---|---|
| **IN** | `L74999TG1955PLC000656` | state | **CIN** | city (RoC) + type + listed + year | ✅ **shipped** |
| **CN** | `91450500MA5KDYN63R` | — | **USCC** (18-char) | **province/city** (chars 3–8) + org type | ✅ shipped |
| **AR** | `30500005862` | country | **CUIT** (tax ID) | entity type (first 2 digits) | ✅ shipped |
| **CA** | `1001630592` | city+region | provincial corp no. | province already in `dataSource` | low need |
| **CH** | `CHE-243.571.513` | city+country | **UID** | — (no location in ID) | low |
| **AT** | `480817 i` | city | Firmenbuch no. | — (address has city) | low |
| **BE** | `0456.766.763` | country | **KBO/BCE** enterprise no. | — (no location in ID) | low* |
| **BW** | `BW00000921008` | — | registration no. | — | low |
| **BM** | `202403382` | — | registration no. | — | low |
| **BZ** | `168941` | country | registration no. | — | low |
| **CW** | `148786` | — | registration no. | — | low |
| **DE** | `Köln HRB 116890` | city+country | HRB/HRA + **court** | **court city (Köln) = city/Land** — in `externalCode` | ✅ shipped |
| **RU** | `1077746661013` | **country only** | **OGRN** (13-digit) | **region (digits 4–5) + year (2–3)** | ✅ shipped |
| **US** | `7219511` | country only | state corp no. | state already in `dataSource` (`Delaware`) | low need |
| **SG** | `195300108N` | country | **UEN** | incorporation **year** (first 4 digits) | ✅ shipped |
| **GB** | `11791594` | care-of addr | company number + **prefix** | jurisdiction (SC/NI) + type (OC/FC) | ✅ shipped |

*(Full, current list — including every jurisdiction the sweep has reached — is in `search-catalog.json`.)*

---

## What this tells us for enrichment

1. **There is no universal decodable field** — every `externalCode` is a different national ID
   scheme. So the **generic `enrichment` object** (same schema, per-jurisdiction decoders) is the
   correct design; there's nothing to unify at the source.
2. **✅ SHIPPED decoders** (built with the same pattern as India — each fills the same `enrichment`
   fields in `enrich_search_result()`):
   - **IN** CIN → city (RoC) + type + listed + year
   - **RU** OGRN → **region + year** (address is country-only, so the ID is the only location)
   - **CN** USCC → **province** (admin-division code)
   - **DE** registry → **court city** (Köln/Wiesbaden) + entity-type hint (HRB/HRA/…)
   - **AR** CUIT → entity type (company vs individual)
   - **HU** Cégjegyzékszám → **county** (01=Budapest, …)
   - **GB** company-no. **prefix** → jurisdiction (Scotland/N.Ireland/E&W) + LLP hint (OC/SO/NC)
   - **SG** UEN → incorporation **year** (first 4 digits)
3. **Low value — intentionally NOT decoded** (audit showed the address already has the city, or the
   ID is a plain sequential number): CA/CH/AT (address has a city); BE/BZ/BM/CW/BW/IT/NL (sequential IDs).

Each new decoder just fills the same `enrichment` fields in `enrich_search_result()` — the response
shape never changes.

---

## Search reliability findings (corrected — most "failures" were OUR error-masking)

The initial "6 jurisdictions return 500" was largely **our own bug**: the registry replies to broad
queries with a helpful **HTTP 400 "More than 200 records found in <country>, please refine your search
criteria"**, and the app was re-wrapping that 400 as a generic 500 — hiding the message. **Fixed:**
`/api/search` now catches the upstream message and returns `{error, refine:true}` (400); the UI shows
it as an amber "refine your search" hint, not a red error.

Re-tested with flagship companies, corrected verdicts:

1. **✅ NOT broken — "too many results" (now handled).** **AU** (BHP), **FI** (Nokia), **FR** (Renault):
   the flagship name matches hundreds of subsidiaries → "refine your search". Registry is fine; use a
   more specific name/number.
2. **🟡 Generic-query sensitivity.** **CY, GR, NO** — 500 on broad terms, work with a real name (same
   root cause; also improved by the catch above).
3. **🐢 KY — works, just slow.** "Tencent" → **17 results in ~62 s**. The earlier "500s" were client
   timeouts cutting it off. Needs a longer/async client timeout, not a KYC.com escalation. (Note: KY
   results come back with an **empty `externalCode`** — a data-quality gap.)
4. **✅ IM works** — "Playtech" → 7 hits in 4.2 s (`014453V`).
5. **🔴 MY — the only genuine issue.** Maybank/Petronas/Genting/AirAsia all → **HTTP 500 after ~62 s**.
   Consistent, not a "too many" 400. **This is the one to escalate to KYC.com.**

> Lesson: always surface the upstream message. What looked like "5 broken markets (AU/FI/FR/KY/MY)"
> was really **3 refine-cases + 1 slow-but-works + 1 genuine (MY)**.

Per-jurisdiction verdicts are in `search-catalog.json` (`searchVerdict` + `realNameTest`).
