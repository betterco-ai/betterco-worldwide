# India location check — decoding the CIN to confirm a company's city (free, pre-purchase)

## The problem

A customer comes with just a **company name + city** — e.g. *"Birlanu Limited, Hyderabad."*

The free KYC search finds the company, but the address it returns is only the **state**
("Telangana"), not the city. To the customer that looks wrong — they said **Hyderabad**,
the result says **Telangana** — so they think it's the wrong company and won't pay for the
report. But it *is* their company: **Hyderabad is a city inside Telangana** (its capital).
The search just shows the state and drops the city. We were losing sales to a display quirk,
and the only "proof" was buying the report — the very thing the customer refused to do.

## The key insight

Every Indian company has a **CIN** (Corporate Identification Number) that the free search
**already returns**. The city is encoded inside it.

Birlanu's CIN: **`L74999TG1955PLC000656`**

```
L      74999    TG        1955   PLC    000656
|      |        |         |      |      |
Listed Industry STATE      Year   Type   Serial
       code     (Registrar inc.   (Public
                of Cos.)          Limited Co.)
```

The two letters `TG` are the **Registrar of Companies (RoC) jurisdiction**, and the RoC for
`TG` is in **Hyderabad**. So the CIN itself says "registered at Hyderabad" — free, already in
the search result.

## The solution

The app now **decodes the CIN automatically** on every Indian search result and shows the
registering city, turning the scary "Telangana" into a clear "RoC Hyderabad" **before** any
purchase. The rep also types the customer's city and each result gets a badge:

- ✅ **location matches** → right company, safe to buy
- ⚠️ **verify location** → double-check (rare — e.g. a state with two registrar cities)

No report bought to confirm location. The whole check is free.

---

## How to use the API

**Endpoint:** `GET /api/search?jurisdiction=IN&query=<name>`

For India, every result gains a **`cin`** object:

| Field | Meaning | Example |
|---|---|---|
| `label` | ready-to-show summary | `Listed Public Limited Company · RoC Hyderabad (Telangana) · est. 1955` |
| `rocCity` | **the registering city** ← the answer | `Hyderabad` |
| `state` | state | `Telangana` |
| `listed` | listed on a stock exchange? | `true` |
| `class` | company type | `Public Limited Company` |
| `year` | year incorporated | `1955` |
| `stateCode` / `classCode` / `regNo` | raw CIN segments | `TG` / `PLC` / `000656` |

Confirm location by comparing **`cin.rocCity`** (or `cin.state`) with the city the customer gave.

---

## Examples

### 1) Birlanu — the original case
```
GET /api/search?jurisdiction=IN&query=Birlanu
```
```json
{
  "jurisdiction": "IN", "query": "Birlanu",
  "results": [{
    "rawname": "BIRLANU LIMITED",
    "externalCode": "L74999TG1955PLC000656",
    "rawAddress": "Telangana",
    "companyStatus": "Active",
    "cin": {
      "rocCity": "Hyderabad",
      "state": "Telangana",
      "listed": true,
      "class": "Public Limited Company",
      "year": 1955,
      "label": "Listed Public Limited Company · RoC Hyderabad (Telangana) · est. 1955"
    }
  }]
}
```
Customer said **Hyderabad** → `cin.rocCity` = **Hyderabad** → ✅ match, safe to buy.

### 2) Other companies (verified)
| Search | Address shown | CIN decodes to |
|---|---|---|
| Infosys | Karnataka | RoC **Bengaluru** |
| Tata Consultancy Services | Maharashtra | RoC **Mumbai/Pune** |
| Bharti Airtel | Delhi | RoC **Delhi** |
| ITC | West Bengal | RoC **Kolkata** |

### 3) A genuine mismatch (the safety net)
Customer says *"Birlanu Limited, **Mumbai**"* → "Mumbai" vs `rocCity` "Hyderabad" → ⚠️
**verify location** — stop and investigate instead of buying the wrong report.

---

## One limitation

The CIN pins the **registrar city** (the state's main registration city). For most companies
that is the head-office city (Birlanu = Hyderabad ✅). For a state with two registrar cities
(e.g. Maharashtra = Mumbai *or* Pune) it confirms the **state/region**; the ⚠️ badge tells the
rep to do a quick free CIN lookup (public MCA data) for the exact street address in those cases.

---

## Where this lives

- **API:** `decode_cin()` in `kyc_case_app.py`; `/api/search` enriches every `IN` result with `cin`.
- **UI:** `kyc_case.html` search screen — the **City** field + the per-result CIN chip and ✅/⚠️ badge.
- Pure client-side + a static lookup table — no gateway call, no billing.
