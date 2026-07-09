# KYC.com search response — catalog & enrichment potential (by jurisdiction)

A **persisted, extensible** record of what the free KYC.com search actually returns per
jurisdiction, so we know (a) the **standard** that always comes back and (b) what we can
**enrich** per country (like India's CIN → city).

- **Coverage (last sweep):** **35 / 44** automated jurisdictions observed. 6 return HTTP 500 on a
  generic query (`AU CY FI FR GR NO` — need a real company name, see Reliability below); 3 timed out
  on the slow upstream (`IM KY MY` — fill by re-running).
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
| **CN** | `91450500MA5KDYN63R` | — | **USCC** (18-char) | **province/city** (chars 3–8) + org type | ⭐ observed — build next |
| **AR** | `30500005862` | country | **CUIT** (tax ID) | entity type (first 2 digits) | to-verify |
| **CA** | `1001630592` | city+region | provincial corp no. | province already in `dataSource` | low need |
| **CH** | `CHE-243.571.513` | city+country | **UID** | — (no location in ID) | low |
| **AT** | `480817 i` | city | Firmenbuch no. | — (address has city) | low |
| **BE** | `0456.766.763` | country | **KBO/BCE** enterprise no. | — (no location in ID) | low* |
| **BW** | `BW00000921008` | — | registration no. | — | low |
| **BM** | `202403382` | — | registration no. | — | low |
| **BZ** | `168941` | country | registration no. | — | low |
| **CW** | `148786` | — | registration no. | — | low |
| **DE** | `Köln HRB 116890` | city+country | HRB/HRA + **court** | **court city (Köln) = city/Land** — in `externalCode` | ⭐ observed — high value |
| **RU** | `1077746661013` | **country only** | **OGRN** (13-digit) | **region (digits 4–5) + year (2–3)** | ⭐ observed — high value |
| **US** | `7219511` | country only | state corp no. | state already in `dataSource` (`Delaware`) | low need |
| **SG** | `195300108N` | country | **UEN** | incorporation **year** (first 4 digits) | to-verify |
| **GB** | `11791594` | care-of addr | company number + **prefix** | jurisdiction (SC/NI) + type (OC/FC) | observed — prefix present |

*(Full, current list — including every jurisdiction the sweep has reached — is in `search-catalog.json`.)*

---

## What this tells us for enrichment

1. **There is no universal decodable field** — every `externalCode` is a different national ID
   scheme. So the **generic `enrichment` object** (same schema, per-jurisdiction decoders) is the
   correct design; there's nothing to unify at the source.
2. **Priority to build next** (biggest gain = coarse address + rich ID — all observed):
   - **RU (OGRN)** — address is **country-only**; OGRN encodes **region + year**. ⭐
   - **CN (USCC)** — coarse address; USCC encodes **province/city** (region code observed). ⭐
   - **DE** — the registration **court city is in `externalCode`** (e.g. `Köln HRB…`) = city/Land; core market. ⭐
   - **AR (CUIT)** — country-only address; CUIT gives at least entity type.
   - **GB** — company-number **prefix** (SC/NI/OC/FC) → jurisdiction + type.
3. **Low value** — CA/CH/AT already return a city; BE/BZ/BM/CW/BW IDs are plain sequential numbers
   with nothing extra to decode.

Each new decoder just fills the same `enrichment` fields in `enrich_search_result()` — the response
shape never changes.

---

## Search reliability findings (re-tested with real flagship companies)

Retesting the failing jurisdictions with **real, well-known company names** (BHP, Nokia, Renault,
Bank of Cyprus, Alpha Bank, Equinor, Tencent, Genting) splits them into three clearly different
problems:

1. **🔴 GENUINELY BROKEN — escalate to KYC.com.** Return **HTTP 500 even for the country's flagship
   company:** **AU** (BHP), **FI** (Nokia), **FR** (Renault). France and Finland are core markets, so
   this is a real search outage in the gateway/upstream, not a query problem.
2. **🟡 Generic-query sensitivity (search-robustness).** 500 on broad terms (`holding`/`bank`) but
   **work fine with a real name:** **CY** (`ΗΕ 44168`), **GR** (returns a full street address),
   **NO** (`993888621`). Fix: the search should degrade gracefully on broad queries instead of 500-ing;
   meanwhile always query with a specific name/number.
3. **🟠 Slow / timeout (affects the UI too).** **KY** (Tencent) and **MY** (Genting) **time out even
   with real names** — genuinely slow upstream. Since the UI hits the same `/api/search` path, it will
   time out there as well → needs a longer client timeout / async fetch, or upstream escalation. **IM**
   is NOT a timeout — it responded (just no match for the test name); retest with a real IoM company.

Per-jurisdiction verdicts are in `search-catalog.json` (`searchVerdict` + `realNameTest`).
