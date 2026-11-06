# Memo 2026-11-06 — Document SLA per jurisdiction, grouped

**Source:** `jurisdiction_matrix.json` (commit `ecfce3d`): 217 rows parsed from the KYC.com
jurisdiction coverage workbook by `build_jurisdiction_matrix.py`. This is the snapshot that the
document-search panel shows as "Usual delivery". When the panel gets an ISO code and the gateway is
reachable, it shows the gateway's live SLA instead. The gateway was **not** queried for this memo.

**Normalisation:** `"24"` and `"24hours"` were merged into `"24 hours"`. Nothing else was changed.

## Grouped by SLA

"With base / additional" = jurisdictions with at least one document of that kind.
"Titles" = total document titles in that group.

| SLA | Jurisdictions | With base docs | With additional docs | Base titles | Additional titles | Which |
|---|---:|---:|---:|---:|---:|---|
| 25 minutes | 13 | 13 | 11 | 36 | 112 | AU, KY, DE, HK (×2), IE, IT, MH, NL, SG, CH, GB, Canada Federal |
| 40 minutes | 31 | 31 | 21 | 61 | 166 | all international ("Live") rows |
| 70 minutes | 6 | 6 | 4 | 6 | 28 | BN, EE, FI, JP, MM, PH |
| 8 hours | 2 | 2 | 0 | 7 | 0 | ID, TH |
| 12 hours | 1 | 1 | 0 | 1 | 0 | CN |
| **24 hours** | **155** | 155 | 77 | 252 | 344 | 94 international + 49 US states + 12 Canadian provinces |
| 30 hours | 1 | 1 | 1 | 1 | 26 | GG |
| 48 hours | 1 | 1 | 1 | 4 | 15 | IN |
| 3 days | 1 | 1 | 1 | 1 | 2 | PT |
| 96 hours | 1 | 1 | 0 | 1 | 0 | Nunavut |
| 7 days | 2 | 2 | 1 | 3 | 3 | BZ, PH |
| 10 business days | 1 | 1 | 1 | 1 | 7 | Wisconsin |
| no SLA (`-`) | 2 | 0 | 0 | 0 | 0 | CA, US (parent rows only) |

## Broader bands

| Band | Jurisdictions |
|---|---:|
| Within 70 minutes | 50 |
| Same day (8–12 h) | 3 |
| 24 hours | 155 (71 %) |
| Longer than 24 hours | 7 |
| No SLA | 2 |

Every row that has an SLA (215) has at least one base (standard) document. 117 of them also offer
additional documents, which are on request and billed extra.

## Data issues in the snapshot

- **HK** appears twice (both 25 minutes).
- **PH** appears twice, at **70 minutes** and at **7 days**. The panel shows whichever row it
  finds first, so the delivery time shown for PH depends on the row order.
- **US** and **CA** are parent rows with no SLA and no documents. The real data sits on the
  state and province rows. Those rows have no ISO code, so the gateway cannot look them up live.

## Reproduce

```python
import json, collections
J = json.load(open("jurisdiction_matrix.json", encoding="utf-8"))["jurisdictions"]
norm = lambda s: "24 hours" if (s or "").strip() in ("24", "24hours") else ((s or "").strip() or "-")
g = collections.defaultdict(list)
for j in J:
    g[norm(j["sla"])].append(j)
for k, L in g.items():
    print(k, len(L),
          sum(bool(j.get("documentsMandatory")) for j in L),
          sum(bool(j.get("documentsNonMandatory")) for j in L))
```
