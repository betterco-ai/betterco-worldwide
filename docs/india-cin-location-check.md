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

**Endpoint:** `GET /api/search?jurisdiction=<ISO>&query=<name>`

**Every** search result — for **every jurisdiction** — carries ONE generic `enrichment`
object with the **same schema**. Jurisdiction-specific decoders fill what they can (India via
the CIN); fields we can't derive yet are `null`. The shape never changes, so one client handles
all countries.

```jsonc
"enrichment": {
  "registryId":         "L74999TG1955PLC000656",   // the externalCode / registration number
  "idScheme":           "CIN",                       // recognised ID scheme, else null
  "entityType":         "Public Limited Company",    // else null
  "listed":             true,                        // else null
  "incorporationYear":  1955,                         // else null
  "status":             "Active",
  "location": {
    "city":        "Hyderabad",                       // decoded/parsed city, else null
    "region":      "Telangana",                       // state/province, else null
    "countryCode": "IN",
    "raw":         "Telangana"                         // the raw address string as returned
  },
  "summary": "Listed Public Limited Company · Hyderabad (Telangana) · est. 1955",  // human one-liner (null if nothing to add)
  "source":  "cin-decode"                              // "cin-decode" | "registry"
}
```

Confirm location by comparing **`enrichment.location.city`** (or `.region`) with the city the
customer gave. Today only India (`idScheme: "CIN"`) is fully populated; other jurisdictions return
the same object, sparsely filled, ready for their own decoders (DE registry court, CN USCC, …).

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
    "enrichment": {
      "registryId": "L74999TG1955PLC000656",
      "idScheme": "CIN",
      "entityType": "Public Limited Company",
      "listed": true,
      "incorporationYear": 1955,
      "status": "Active",
      "location": { "city": "Hyderabad", "region": "Telangana", "countryCode": "IN", "raw": "Telangana" },
      "summary": "Listed Public Limited Company · Hyderabad (Telangana) · est. 1955",
      "source": "cin-decode"
    }
  }]
}
```
Customer said **Hyderabad** → `enrichment.location.city` = **Hyderabad** → ✅ match, safe to buy.

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

- **API:** `/api/search` attaches a **generic `enrichment` object to every result, every
  jurisdiction** (`enrich_search_result()` in `kyc_case_app.py`). Jurisdiction decoders fill it —
  India via `decode_cin()`; add DE/CN/RU/… the same way (they write into the same fields, the JSON
  shape never changes).
- **UI:** `kyc_case.html` search screen reads `enrichment.summary` for the chip, `enrichment.location`
  for the ✅/⚠️ match against the **City** field.
- Pure logic + static lookup tables — no gateway call, no billing.

> The mechanism is generic; India (CIN) is just the first populated decoder because that's where the
> problem surfaced. The response contract is **one enrichment schema across all jurisdictions.**
