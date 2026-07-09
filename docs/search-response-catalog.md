# KYC.com search response — catalog & enrichment potential (by jurisdiction)

A **persisted, extensible** record of what the free KYC.com search actually returns per
jurisdiction, so we know (a) the **standard** that always comes back and (b) what we can
**enrich** per country (like India's CIN → city).

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
| **DE** | *(pending sweep)* | — | HRB/HRA + **court** | court city = **city/Land** | to-verify (high) |
| **GB** | *(pending sweep)* | — | company number + **prefix** | jurisdiction (SC/NI) + type (OC/FC) | to-verify |
| **RU** | *(pending sweep)* | — | **OGRN** (13-digit) | region + year | to-verify |

*(Full, current list — including every jurisdiction the sweep has reached — is in `search-catalog.json`.)*

---

## What this tells us for enrichment

1. **There is no universal decodable field** — every `externalCode` is a different national ID
   scheme. So the **generic `enrichment` object** (same schema, per-jurisdiction decoders) is the
   correct design; there's nothing to unify at the source.
2. **Priority to build next** (biggest gain = coarse address + rich ID):
   - **CN (USCC)** — address is coarse, USCC encodes province/city; region code observed. ⭐
   - **DE** — the registration **court** (in `externalCode`) is the city/Land; core market. (verify format)
   - **RU (OGRN)** — encodes region + year.
   - **AR (CUIT)** — address is country-only; CUIT gives at least entity type.
3. **Low value** — CA/CH/AT already return a city; BE/BZ/BM/CW/BW IDs are plain sequential numbers
   with nothing extra to decode.

Each new decoder just fills the same `enrichment` fields in `enrich_search_result()` — the response
shape never changes.
