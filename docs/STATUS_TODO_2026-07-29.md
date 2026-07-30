# Status and to-dos — 2026-07-29

*Session of 2026-07-27/28/29. Companion documents:*
*`ARCHITECTURE_AGGREGATION_2026-07-28.md` (design) · `CONNECTOR_FINDINGS_2026-07-28.md` (measurements).*

---

## 1. Done

### Connectors — all live-tested, none of it costing money

| Connector | Location | State |
|---|---|---|
| Companies House (UK) | `betterco_claude_api/companies_house_client.py` | free, 25 self-checks, live-verified |
| INPI RNE (FR, free) | `betterco_claude_api/inpi_client.py` | **bug fixed**, 26 self-checks, 6 legal forms verified |
| DataInfogreffe (FR, paid) | `betterco_claude_api/datainfogreffe_client.py` | 29 self-checks, verified on the free démo wallet |
| kyc.com document map | `betterco_claude_api/kyc_com_document_map.py` | 59 self-checks, applied to all 1 082 matrix rows |

Routers: `/companieshouse` (9 routes), `/inpi` (6), `/datainfogreffe` (6, behind `PaidGate`).
Wired in `api/deps.py` + `api/main.py`. `handelsregister` untouched.
Skills `companieshouse`, `inpi`, `datainfogreffe`; marketplace `kyc-registries` → 1.2.0.

### Access resolved

* **INPI works.** The long-standing `403 connection_type_not_allowed` is gone; the JWT carries
  `"connectionType":"API"`. Password `P1l01lt033!!` is the working one.
* **Companies House**: live key verified against the live host; test key against the sandbox.
* **DataInfogreffe**: démo wallet returns real data — 109 credits left of 200.

### The three bugs found by running the code, not reading it

1. **INPI `confidentiality` is a STRING** whose normal value is `"Public"`. `bool("Public")` is
   `True`, so every document was flagged confidential and **every FR download failed**. The whole
   free French document channel was dead and looked like "this company filed nothing".
   An earlier diagnosis in `CONNECTOR_FINDINGS` blamed `typeRdd` — that was wrong and is corrected
   there.
2. **UK articles need the amendment, not the incorporation pack.** Monzo has six `MA` filings; the
   current articles are from 2024, the incorporation pack from 2015. Without checking
   `category=resolution` first we would ship a decade-old constitution as current.
3. **`æ` is not a letter-plus-accent.** Unicode NFKD does not decompose it, so Danish "Vedtægter"
   never matched. Same for `ø`, `ß`, `ł`, `đ` — precisely the matrix's long tail (Denmark, Norway,
   Poland, Croatia). Fixed with an explicit ligature table.

### Decisions taken

* **A Gründungsurkunde is not a Registerauszug** (confirmed by EO 2026-07-28). A Certificate of
  Incorporation attests creation, not current register content; a Certificate of Good Standing
  attests status but is not an extract. Both got their own kinds — **98 matrix rows** that would
  otherwise have been mis-filed as extracts.
* **One module per vendor, no per-jurisdiction router.** FR has two connectors because it has two
  vendors, not because FR is special.
* **BetterCo is the system of record**; STP reads only from BetterCo. See the architecture memo.

---

## 2. Open — blocking

### B1. Evidence levels must be decided before the STP contract is frozen
`data` / `document` / `certified`, apostille as an attribute rather than a fourth level. This is
**D2** in the architecture memo's decision register. Retrofitting the field is a breaking change for
a customer who has already migrated — and the entire point of step 1 is that STP migrates once.

Now backed by a concrete failure: the matrix label "Historical – Shareholders" (UK) is a *data
section*, not a filed document. Label matching alone would claim the UK can deliver a shareholder
list — contradicted by direct measurement (the UK files none). Without an evidence level that
error reaches the case store.

### B2. Two canonical kinds have no BetterCo slot
`GRUENDUNGSURKUNDE` (61 rows) and `STATUSBESCHEINIGUNG` (37 rows) fall back to
`OTHERKYCDOCS_SONSTIGE`. Backend decision: create two slots, or accept the bucket and carry the
canonical kind in the document name. `kyc_com_document_map.gaps()` is the machine-readable list.

### B3. Provenance has nowhere to live
`upload_customer_document` sends exactly `{"name": ..., "type": ...}`. There is **no metadata
field**. Vendor, fetch date, content date, source reference, evidence level and cost have no home.

The architecture requires provenance to be written *with* the document — the INPI licence (art. 2.4)
demands source **and date of last update**, and that is unknowable afterwards.

Depends on an unanswered question: **does "STP calls BetterCo" mean the core product API or our
aggregation service in front of it?**
* aggregation service → provenance lives in `sourcing/`, joined on read. No backend work.
* core product API → the document model needs a metadata field. **Backend ticket, with lead time.**

---

## 3. Open — not blocking

### N1. Stale duplicate of `inpi_client.py`
`betterco-worldwide/inpi_client.py` **still contains the confidentiality bug**. The canonical copy
is `betterco_claude_api/inpi_client.py` (as the skill states). The worldwide copy also carries
uncommitted dry-run work from an earlier session, so it was deliberately left untouched here.
Decide: delete it, or sync the fix. Leaving a broken duplicate is a trap — it fails silently by
reporting "no documents".

### N2. OCR is mandatory, not optional
INPI actes and Companies House filings are **scans with no text layer** (measured: 0 text characters
across 15 and 43 pages). Only the DataInfogreffe PDF has one. OCR belongs in ingestion, once, with
the text stored beside the PDF — not in every consumer.

### N3. Freshness policy (D1), retention (D3), cost pass-through (D4)
Safe defaults exist for all three. For D4: **instrument now even if the commercial model waits** —
per-case cost cannot be reconstructed from a monthly vendor invoice.

### N4. Kbis is a manual portal process
No ordering API exists, confirmed. `FR/REGISTERAUSZUG` is a human queue or a Playwright client
modelled on `handelsregister_client.py`. The latter only after one manual run is recorded, and only
behind `PaidGate`. The 85 €HT/yr subscription is already paid, so the capability exists.

### N5. Structured data mapping
kyc.com also serves `get_members`, `get_org_chart`, `get_aml_checks`. Mapping those onto BetterCo
customer/contacts/relations is a second translation layer nobody has written.

### N6. Slot semantics vs. history
Customer documents are a *slot* — "replace, don't append". A new register extract overwrites the
old. Correct for freshness, but it destroys history. If STP ever needs a document *as of* a past
date, that conflicts. Settle before building ingestion.

### N7. Hong Kong per-filing purchase — wired, not yet seen live
`GET /v2/DocumentPurchase/{caseCommonId}` + `POST /v2/DocumentPurchase {caseCommonId,
registryDocumentId}` is the **only** upstream route where kyc.com is document-level rather than
case-level, and it is **HKCR-only** (400 elsewhere). Contract read off the prod swagger and wired:
`kyc_com_client.list_document_filings / find_document_filings / purchase_document(confirm=…)`,
routes `GET /kyccom/cases/{id}/filings` + `POST …/filings/{id}/purchase?confirm=true`, HK rows in
`document_kinds_routing.json` now say `howToObtain: "document_purchase"`, gateway ask in
`BACKEND_DEV_MEMO.md`. **Open:** the sandbox *stubs* the route (200 for any case, `documents: null`),
so the filing payload has never been seen with real content — needs one prod HK case, list only,
**nothing purchased**. Also unresolved: the evidence file calls HK Articles/NAR1 `additional`, while
the kyc.com matrix lists both as *mandatory* for HK CR (and the sandbox bundle contained them) — so
for most HK cases the purchase route is for the filings the bundle does *not* carry (older NAR1s,
altered articles), not for the current ones. The `purchased` flag encodes that; the base/additional
classification itself is left as is.

---

## 4. Next step

Build the ingestion path: webhook → fetch → `resolve()` → correct BetterCo slot.
`CaseReady` and `DocumentUploaded` already exist in `kyc_com_client.py` (`subscribe_webhook`);
wiring them replaces polling and is the prerequisite for everything asynchronous.

B1 and B3 should be answered first — both shape the contract, and both are expensive to retrofit.

---

## 5. Safety state to restore

`FR_DATAINFOGREFFE_API_KEY_PROD` was renamed `..._PROD_DISABLED` in `betterco_claude_api/.env` for
the unattended run, so no code path could spend real credits. **Rename it back to place paid
orders.** Verified while disabled: `DataInfogreffeClient(env='prod').api_key is None`.

Also in `betterco-worldwide/.env`: `GB_COMPANIES_HOUSE_USERNAME` / `_PASSWORD` are unused by the API
(auth is the key as username, empty password) and should be removed; `INPI_USERNAME` has a stray
trailing tab. The client now `.strip()`s, so it is no longer harmful — only untidy.
