# Connector findings — FR + UK, measured 2026-07-27/28

*Everything here was produced by a live call, not by reading documentation. Byte counts are actual
downloads. This file exists so the facts survive; the durable documentation will be the three
skills (`inpi`, `datainfogreffe`, `companieshouse`) once the clients are written.*

**Scope note:** this is connector work. It does **not** revise the KYC.com analysis
(`document_kinds_evidence.json`, `document_kinds_routing.json`, coverage assessment) — those stay
as they are.

---

## 1. Credential state

| Env var (in `betterco-worldwide/.env`) | Status |
|---|---|
| `INPI_USERNAME` / `INPI_PASSWORD` | **works** — password is `P1l01lt033!!`. Username has a stray trailing TAB; trim it. |
| `xxINPI_PASSWORD` | dead entry, delete |
| `GB_COMPANIES_HOUSE_API_KEY_PROD` | **works** against `api.company-information.service.gov.uk` |
| `GB_COMPANIES_HOUSE_API_KEY_TEST` | works against `api-sandbox.…` only |
| `GB_COMPANIES_HOUSE_USERNAME` / `_PASSWORD` | **unused by the API** — portal login only; remove from `.env` |
| `FR_DATAINFOGREFFE_API_KEY_TEST` | **works, returns REAL data.** Démo wallet: 200 credits, **109 left** |
| `FR_DATAINFOGREFFE_API_KEY_PROD` | never exercised (every prod call spends money) |

---

## 2. INPI — the 403 is resolved

The long-standing blocker (`403 connection_type_not_allowed`, "Accès impossible pour API") is **gone**:

```
POST https://registre-national-entreprises.inpi.fr/api/sso/login  →  200
JWT payload contains:  "connectionType":"API"
```

Registering was never enough; the access had to be granted. Where it lives:

* **Access overview:** `https://data.inpi.fr/espace_personnel/acces` → tab **"Accès APIs RNE"**.
  Lists three bases: *Informations d'entreprises* (JSON), *Comptes annuels* (JSON/PDF), *Actes* (PDF).
* **The request form:** `https://data.inpi.fr/demande-de-donnees-rne` — "Demande de téléchargement et
  de réutilisation des données": project description, *Mode d'accès* API/FTP, base selection.
  On the access page the words "ce formulaire" are **not a link** — that is why it was unfindable.
* `api-gateway.inpi.fr` is the **wrong portal**: "Gestion des APIs PI — Brevets, Marques, Dessins et
  modèles". Nothing there applies to the RNE.
* There is **no API key** for the RNE API at all. Auth is username+password → JWT.

### Endpoints validated (these were the untested `# SECONDARY` paths in `inpi_client.py`)

| Call | Result |
|---|---|
| `GET /companies/552081317` | 200, 14 206 441 bytes JSON |
| `GET /companies/552081317/attachments` | 200 — sections `actes`, `bilans`, `bilansSaisis` |
| `GET /actes/{id}/download` | 200, **4 679 818 bytes, `application/pdf`, `%PDF-1.7`, 15 pages** |

### BUG in `inpi_client.py` — FIXED 2026-07-28. Note the corrected diagnosis.

An earlier version of this file blamed the statuts needle for missing `typeRdd`. **That was wrong**
— `_norm_attachment` already flattened `typeRdd[].typeActe` into the label, and the "statut" stem
matched fine. Running the client is what settled it.

The real defect was one line, and it broke **every** download:

```python
confidential = bool(item.get("confidentiality") or ...)   # WRONG
```

`confidentiality` is a **string**, and its normal value is **`"Public"`**. `bool("Public")` is
`True`, so every acte and every bilan was flagged confidential, `downloadable` was always `False`,
and `download()` raised `DocumentUnavailable` for every company in every legal form. The free FR
document channel was completely dead and looked like "this company filed nothing".

Fixed via `_is_confidential()`: strings are compared against a known confidential vocabulary, real
booleans are honoured, and anything unrecognised is treated as distributable — a false "confidential"
silently hides documents we are entitled to. A regression check pins `"Public"` in the self-test.

Two response shapes do genuinely occur and both are handled: large companies carry `typeDocument` +
`libelle` as plain strings, small ones carry `typeRdd`, a list of dicts whose `typeActe` holds the
label ("Statuts mis à jour", "Statuts constitutifs").

Also fixed: the module never called `load_dotenv()` (unlike every other client in the repo), and
credentials are now `.strip()`ed — the stray tab in `INPI_USERNAME` would otherwise come back as an
indistinguishable 401.

### Verified across six legal forms after the fix

| Form | SIREN | actes | downloadable | statuts | downloaded |
|---|---|---|---|---|---|
| SARL | 491520680 | 5 | 5 | 5 | 4 679 818 B |
| SAS | 978162170 | 2 | 2 | 1 | 330 749 B |
| SA | 344122262 | 37 | 37 | 15 | 1 172 474 B |
| SNC | 732014964 | 30 | 30 | 3 | 1 070 811 B |
| SCI | 849817283 | 2 | 2 | 1 | 7 610 677 B |
| SA (large, EDF) | 552081317 | 164 | 164 | 68 | 1 998 362 B |

Before the fix the `downloadable` column would have been 0 in every row.

### One acte is a BUNDLE, not one document

The `typeRdd` list above is a single downloadable PDF containing all three items. We deliver the
deposit PDF *containing* the statuts, never an isolated statuts file.

---

## 3. Companies House

`GET /company/{n}` → `/filing-history?category=incorporation` → `document_metadata` → PDF, all free:

```
GET https://document-api.company-information.service.gov.uk/document/{id}/content
→ 200, 1 135 516 bytes, application/pdf, 43 pages   (company 10913418, filing NEWINC 2017-08-14)
```

* Auth = HTTP Basic, **API key as username, empty password**. No username/password auth exists.
* Keys are **host-bound**: prod key on the sandbox host → 401, test key on the live host → 401.
* The sandbox holds **no real register data** — a valid test key returns **404, not 401**, for a real
  company number. Test companies must be created via `test-data-sandbox.company-information.service.gov.uk`.
  Conclusion: the sandbox cannot validate real documents; the live key is the one that matters.
* Rate limit 600 requests / 5 min → backoff from the start.
* **No certified extract via API.** UK has no Kbis equivalent; register content *is* the profile JSON
  plus filing history. Certificates are portal-only (not verified).
* **No shareholder list.** Consistent with the existing analysis: CS01 is a delta, PSC covers >25% only.

---

## 4. DataInfogreffe

Base `https://api.datainfogreffe.fr/api/v1/Entreprise`, auth via **query parameter `?token=`** (not a
header). Every response carries `Metadata: {CreditsUsed, CreditsLeft}`. Errors: 400 / 401 / **402
(credits exhausted)** / 404.

Because the token travels in the URL: **never log full request URLs.**

### `RepartitionCapital` — works for SARL and SASU, returns data *and* a PDF

Tested on 491520680 (SARL) and 978162170 (SASU) — both returned named shareholders with share counts
and percentages, plus the source deposit:

```
CapitalSocial:     Montant 8000.00, NbrParts 800, PourcentageDetentionPP 100.00
CapitalDetention:  MAUBLANC Patrick Roger, b. 1960-01-09 Bourg-en-Bresse — 800 parts, 100.00 %
Depot:             2019-12-18, no. 3944, Acte 2019-10-01 no. 1
PdfUrl:            https://api.datainfogreffe.fr/pdf/…  → 557 151 bytes, %PDF-1.4, 2 pages
```

Three implementation facts:

1. **Always call with `restitution=pdf`.** That one response contains the full JSON *and* `PdfUrl`.
   With `restitution=json`, `PdfUrl` is empty — fetching both would cost 60 credits instead of 30.
2. The payload is **double-nested**: `Data.Data.{ReferentielGreffe, SocieteInfos, CapitalSocial,
   CapitalDetention, RepresentantsDetail, Depot}`.
3. The **`PdfUrl` is unauthenticated and public**. Do not pass it to customers as a permalink —
   download and store it ourselves.

### What the PDF actually is

Letterhead **"Greffe du Tribunal de Commerce de ANTIBES"** with the greffe's address, then RCS number,
seat, legal form, `CAPITAL SOCIAL`, `DETENTION DU CAPITAL` (named person, birth date, parts, %),
`DIRIGEANTS` with qualité, dated "Le 27 juillet 2026". A greffe-issued statement — **but no
"certifié conforme" wording and no seal.** Legally weaker than a Kbis; substantially more than
vendor data. Content reflects the **last deposited act** (2019 here), not a live cap table.

Note this is a connector observation. It is **not** a revision of the FR shareholder-list position in
the curated dataset.

---

## 5. Kbis — portal only, confirmed

No API path exists. Infogreffe's own API page points at DataInfogreffe (data only), and the document
packs (Kbis, Statuts, État d'endettement) are ordered "depuis la fiche de l'entreprise" in the portal.
The only non-public API channel is *État d'endettement* for banks and regulated professions — a
commercial conversation, not self-service.

Price 2,03 €HT + 0,52 € electronic transmission = **3,06 € TTC** (statutory, art. R.743-140 c. com.).
Subscription is paid (85 €HT/year). Consequence: FR/REGISTERAUSZUG is a **human portal process with a
queue**, or a Playwright client modelled on `handelsregister_client.py` — the latter only after one
manual run is recorded, and only behind `PaidGate`.

---

## 6. The finding that affects downstream processing

**INPI actes and Companies House filing images have NO text layer.** Measured: 0 text characters on
all 15 pages of the INPI acte and all 43 pages of the UK filing. Only the DataInfogreffe PDF carries
extractable text.

**OCR is mandatory, not optional**, for anything that reads content out of these documents. This was
not in our previous assumptions.

Content confirmed by rendering pages:

* INPI acte p2 — *Procès-verbal des décisions extraordinaires de l'associé unique* of 17/07/2023,
  signed, handwritten "Certifié sincère et conforme à l'original".
* UK filing p6 — IN01 PSC statement; p20 — **bespoke** articles of association (art. 22–25
  Directors' remuneration / expenses / alternate directors), not model articles.

---

## 7. Architecture decisions taken

* **One module per vendor**, mirroring DE (`handelsregister_client` + `northdata_client` +
  `transparenzregister_client`). So: `companies_house_client.py` (UK), `inpi_client.py` +
  `datainfogreffe_client.py` (FR). FR needs two because they are two vendors with separate auth —
  not because FR is special.
* **No per-jurisdiction router.** Each FR document kind has exactly one vendor, so a FR router would
  be a three-row lookup table duplicating `document_kinds_routing.json`. One jurisdiction-agnostic
  dispatch layer comes later, driven by that table, serving FR/UK/DE alike.
* DataInfogreffe routes go behind the existing `PaidGate` (`api/deps.py:83`) — its first real user.
  INPI and Companies House are free and ungated.

## 8. Document coverage as measured

| Document | UK | FR |
|---|---|---|
| Articles / statuts | Document API, free, 43 p | INPI actes, free, 15 p |
| Register extract | none (no Kbis equivalent) | Kbis, Infogreffe portal, 3,06 €, manual |
| Shareholder list | **not available** | DataInfogreffe, 3,00 €HT, JSON + PDF |
| Accounts | Document API, free | INPI bilans, free (+ structured `bilansSaisis`) |
| Company data | Public Data API, free | INPI `/companies/{siren}`, free |
