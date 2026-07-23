# Doc-kinds ground-truth vs the KYC.com v2 sandbox

**Date:** 2026-07-22 · **Method:** created golden-reference cases in the KYC.com v2 trial sandbox
(`api.knowyourcustomer.dev`), read the documents actually delivered at Ready, and diffed the delivered
`category` codes against what `curation/document_kinds_evidence.json` claims for that jurisdiction.

This turns the doc-kinds table from *inferred* (per statute) into *verified* against a real sourcing channel
— and surfaces one important distinction: **"provable from the registry" (our table) is not always the same
as "what the sourcing channel actually delivers."**

## Results

| Jurisdiction | Company (case) | Delivered `category` codes | Verdict vs our table |
|---|---|---|---|
| **GB** | Cropwell Bishop Creamery (1000002771) | `NEWINC`, `CS01`, `AR01`, `AA`, `CERTNM` | ✅ Register extract = CR particulars (base). No shareholder-list or articles document delivered for this company — **CS01 is a confirmation-statement delta, not a standing shareholder list** — matching our "GB shareholder list not provable from registry." |
| **HK** | Ubizense (1000002799) | `HK CR Company Particulars`, `Articles of Association`, `Certificate of Incorporation`, `FNAR1`/annual return, `FNNC1` | ✅✅ Strong match: CR Particulars = register extract (base ✓); Articles of Association = constitution (our *additional* ✓); Annual Return (NAR1) = shareholder list (our *additional* ✓). |
| **SG** | SC Engineering (1000002792) | `Registration` (the ACRA business profile) — single document | ◑ Partial. The ACRA business profile **is** the register extract and carries the shareholders (base ✓, ✓), but **KYC delivered no separate constitution (M&A) document**, even though the constitution is registry-obtainable in principle. Registry-availability ≠ channel delivery. |

## Takeaways

1. **Where documents were delivered, our registry-availability classifications hold up** — HK is a clean,
   full confirmation (extract / articles / annual-return-as-shareholder-list all as classified).
2. **The sourcing channel can deliver *less* than the registry makes available.** SG's KYC delivery is a
   single ACRA business profile (no separate M&A doc); GB's is a set of Companies House filings (no articles
   for this particular company). So a customer sees *what the channel returns*, which may be narrower than
   *what the registry could provide*.
3. **Document `category` codes are registry-specific form codes** (GB Companies House: NEWINC/CS01/AR01/AA/
   CERTNM; HK CR: NAR1/NNC1/CR Particulars; SG ACRA: a single "Registration"). A "category ⇒ only register
   documents" filter therefore works *within* a jurisdiction but not as a universal taxonomy — which is why
   the **per-jurisdiction × legal-form mapping is the right abstraction**, not a flat category filter.

## STP relevance

This directly supports the STP answer: the delivered-document reality confirms the mapping, **and** adds the
honest nuance that the shareholder-list / constitution a customer actually receives depends on the sourcing
channel's coverage, not only on what the registry holds. The lookup table should carry both signals where
they differ.

*(Full flow also verified live: auth → search → create → ready(statusId 3) → members → org-chart → documents
→ mandatory → amlchecks → report(PDF). See the `knowyourcustomer` skill "Canonical KYB flow" section.)*

---

# Round 2 — STP priority jurisdictions vs the sandbox (2026-07-23)

**Goal:** extend the GB/HK/SG spot-check to the 15 STP-priority jurisdictions (FR, IT, GB, US, ES, DK, NL,
LU, CH, IL, JP, BE, KW, SG, HK). **Method:** for each, `search()` the sandbox seed → `create_case_from_search`
→ `poll_until_ready` → `get_case_documents` (metadata) + mandatory catalogue. Harvest saved under
`curation/sandbox_harvest/<CC>/result.json`.

## Seed coverage — what the sandbox actually contains

The v2 sandbox `search()` matches ONLY its **demo-harvest seed** (**353 companies across 142 jurisdictions**,
tagged `dataSource=demo-harvest`), NOT a live registry, and it is a **name-substring match**. The authoritative
seed list is the catalog at `knowyourcustomer.com/developers/test-cases/` (JS-rendered; extract the rows via the
browser — a blind token probe misses entries).

⚠️ **Correction (2026-07-23):** an earlier pass using guessed name tokens wrongly concluded ES/JP/BE/KW were
"not seeded" and FR had "no documents". Reading the actual catalog disproved that — **all 15 STP jurisdictions
are seeded** and (except the stub cases below) return real documents. The misses were a search-method failure:

| JD | Seeded company | externalCode | why the token probe missed it |
|---|---|---|---|
| FR | ETABLISSEMENTS J BLONDEAU (2nd FR co.) | 572 820 629 | only Schneider (no-docs) was found first |
| ES | POSA REALTY ES SL | B42644112 | "Posa/Realty" not guessed |
| JP | 株式会社ブルーキャピタルマネジメント | 0104010967… | Japanese-script name — romaji tokens don't substring-match |
| BE | JVG MANAGEMENT | 0764.938.733 | "JVG" not guessed |
| KW | CALI UNITED REAL ESTATE … WLL | 237369 | "Cali/United" not guessed |

**All 15 STP jurisdictions are now sandbox-verified** (metadata + delivered docs). Note FR's *Schneider* case
genuinely returns 0 documents; FR's *Blondeau* case returns a Registry Extract — so pick Blondeau for FR.

## Delivered documents vs our evidence classification

| JD | Company (case) | Delivered docs (category → name) | vs our evidence |
|---|---|---|---|
| **IT** | Quick Light Food S.R.L. (1000003788) | Registry Extract | ✅ REG=base delivered; articles (add) not delivered; Srl shareholders ride the extract as data. Match. |
| **US** | SALEM FARMS, INC. (1000003791) | Registry Extract · Annual Report · Incorporation | ⚠️ REG=base ✓, GLISTE=none ✓, **but NO articles/bylaws** — our evidence marks US GESELLSCHAFTSVERTRAG *base ×7*. US bylaws aren't filed at the state registry → **our "base" is wrong, should be not-provable/additional.** |
| **DK** | KLARAVIK APS (1000003794) | Registry Extract · Registration certificate · Register Report · **M&A (ADDAS)** · Annual Accounts | ⚠️ REG=base ✓✓, GLISTE=none ✓, **but the M&A/Gesellschaftsvertrag was delivered in the bundle** — we classified it *additional*. Channel delivers it (at least in demo). |
| **NL** | Whitford B.V. (1000003802) | Company Registration Extract · Status Report | ✅ REG=base ✓, articles (additional) not delivered ✓, shareholders data-only (no doc) ✓. **Fills the NL gap** (we had 1 evidence row). |
| **LU** | UNIVERSAL-INVESTMENT-LUXEMBOURG S.A. (1000003807) | Official Registry Extract · **M&A (Articles)** · Annual Accounts | ✅✅ REG=base ✓, **GESELLSCHAFTSVERTRAG=base confirmed** (articles delivered in bundle), no separate shareholder doc ✓. |
| **CH** | BLUEROCK SWITZERLAND GMBH (1000003815) | **Registration Extract** · Company Registration | ⚠️ we classified CH REGISTERAUSZUG *additional* (certified, per-canton). Sandbox delivered an (uncertified) **extract in the bundle**; statutes (add) not delivered ✓. **Fills the CH gap.** |
| **IL** | OPTIVAL LTD (1000003818) | Certificate of Incorporation · **Annual Return** | ✅ REG≈base (delivered as Certificate), articles (add) not delivered ✓, **Annual Return carries shareholders** (like HK) → GLISTE source. |
| **GB** | Cropwell Bishop (1000003766) | NEWINC · CS01 · AR01 · AA · CERTNM | ✅ re-confirms round 1: extract=base, CS01=delta not a standing list, no articles for this co. |

## Candidate corrections — SUPERSEDED, see the FINAL section below

> ⚠️ This block records the first-pass reading. On closer inspection **only DK survived**; the US and CH
> claims were withdrawn. The authoritative outcome is in "FINAL coverage" at the bottom. Kept for the trail:
>
> 1. ~~US GESELLSCHAFTSVERTRAG is not "base ×7"~~ — **WITHDRAWN.** The delivered "Incorporation" doc IS the
>    filed Certificate of Incorporation (the charter = the Satzung equivalent); our evidence already says the
>    charter is base and the internal bylaws aren't filed. US is a **match**, not an error.
> 2. **DK Gesellschaftsvertrag delivered in-bundle** → additional→base (**applied, with a prod-confirm caveat**).
> 3. ~~CH Registerauszug is channel-delivered~~ — **NOT applied.** CH's delivered extract is only a 1 KB sandbox
>    stub; too weak to reclassify. Left as additional.
>
> Caveat that drove the caution: the sandbox is demo data and can inline *more* than prod (journey="All"),
> so "delivered in the bundle" is not proof of base-tier in prod.

## Document BYTES — pure OAuth path works (CORRECTED 2026-07-23 after KYC.com support reply)

> ✅ **UPDATE:** The section below concluded "REST cannot download bytes". That was WRONG — a case-sensitivity
> miss. KYC.com support confirmed and it's verified live: **`GET /v2/Documents/{documentId}`** (capital `D`,
> NO suffix) returns the bytes with the ordinary OAuth PublicApi bearer (DK doc 2000470 → 200 `application/pdf`
> 579 071 B; GB 35459 → 904 B). Extract `documentId` from the doc `link` and call that route — **do NOT call the
> `link`** (it's an internal service host, 401s, not meant to be called directly). The Workspace-console route
> below still works but is **not needed**. `download_document()` in `kyc_com_client.py` was fixed to this path.
> The 404s I saw were all lowercase `/v2/documents/{id}` or `/document`-suffixed — the working route is capital-D.

**(superseded) earlier conclusion — kept for the trail:** *the `/v2` REST API cannot download document bytes* —
- `/v2/documents/{id}` on the api base (`api.knowyourcustomer.dev`) → **404** *(because lowercase; capital-D works)*.
- the doc `link` host (`api-service-hk` / `api-service-uathk`.knowyourcustomer.com) → **401** *(internal host, correct — don't call it)*.
- the auth server only grants scope `PublicApi` *(fine — that scope authorizes `/v2/Documents/{id}`)*.
- `get_report()` (whole-case PDF via OAuth) **409s on freshly-created cases** *(still true)*.

**What works:** the **Workspace console** (`https://workspace.knowyourcustomer.dev`) — log in by pasting the
same **client_id + client_secret** (no email/password). It sets an httpOnly session cookie and exposes its own
same-origin Next.js API that proxies bytes server-side (with a token the console's server obtains, not our
PublicApi one):
- `GET /api/cases/{caseCommonId}/documents` → doc tree (metadata + `link`s, incl. nested shareholders)
- `GET /api/documents/{docId}` → **the actual PDF bytes** (200, `application/pdf`)
- `GET /api/cases/{caseCommonId}/report` → whole-case report

**Bytes now in hand.** All documents for the 8 verifiable cases were pulled through the console session and
saved under `curation/sandbox_harvest/<CC>/documents/` — **29 PDFs, all valid `%PDF-`**:

| JD | PDFs | sizes | note |
|---|---|---|---|
| DK | 5 | 91–565 KB | real filings (Registry Extract, Certificate, M&A/ADDAS, Register Report, Accounts) |
| LU | 3 | 110–353 KB | real (Registration, Articles, Financial info) |
| US | 3 | 99–154 KB | real (Registry Extract, Incorporation, Annual Report) |
| IL | 2 | 143 + 745 KB | real (Certificate of Incorporation, Annual Return) |
| NL | 2 | 67 + 76 KB | real (Company Registration Extract, Status Report) |
| IT | 1 | 69 KB | real (Registry Extract) |
| **GB** | 9 | ~1 KB each | ⚠️ **sandbox stub placeholders**, not real filings |
| **CH** | 4 | ~1 KB each | ⚠️ **sandbox stub placeholders** |

So the sandbox serves real-sized documents for DK/LU/US/IL/NL/IT but only 1 KB stubs for GB and CH — a
sandbox data-quality quirk, not a channel limitation. FR (0 docs) and ES/JP/BE/KW (not seeded) yield nothing.

**Reusable method:** browser-drive the console login (form: client_id+secret), then run an in-page `fetch()`
loop over `/api/documents/{id}` and pack the results into a single store-only ZIP downloaded in one shot
(avoids Chrome's multi-download gate and keeps bytes out of the agent context). `https→http://localhost`
streaming does NOT work (mixed-content stalls). Prod remains the alternative for real bytes at scale (billable,
prod links work with OAuth).


---

# FINAL coverage — all 15 STP jurisdictions (2026-07-23)

Every priority jurisdiction was created, brought to Ready, its delivered documents diffed against the evidence
file, and its document **bytes pulled to disk** via the Workspace-console session. Files:
`curation/sandbox_harvest/<CC>/documents/` — **42 PDFs, 4.9 MB total**.

| JD | Company (case) | Delivered kinds | PDFs | bytes | vs evidence |
|---|---|---|---|---|---|
| FR | ETABLISSEMENTS J BLONDEAU (…823) | Registry Extract | 1 | 361 KB real | ✅ REG=base; Schneider co. returns 0 docs |
| IT | Quick Light Food S.R.L. (…788) | Registry Extract | 1 | 69 KB real | ✅ REG=base |
| GB | Cropwell Bishop (…766) | NEWINC/CS01/AR01/AA/CERTNM | 9 | ~1 KB **stub** | ✅ extract=base, CS01=delta, no articles |
| US | SALEM FARMS, INC. (…791) | Registry Extract, Incorporation, Annual Report | 3 | 128 KB real | ✅ REG + charter(=Certificate of Incorporation)=base, no bylaws, GLISTE=none |
| ES | POSA REALTY ES SL (…826) | Informacion Imprimible | 1 | 48 KB real | ✅ REG(nota/extract)=base |
| DK | KLARAVIK APS (…794) | Extract, Certificate, M&A, Register Report, Accounts | 5 | 300 KB real | REG=base ✓, GLISTE=none ✓. M&A delivered in the All-journey bundle but **NOT proven base** — see the PROD section: the additional→base flip was **reverted** (no DK prod case to confirm) |
| NL | Whitford B.V. (…802) | Company Registration Extract, Status Report | 2 | 71 KB real | ✅ REG=base, articles(add) not delivered, GLISTE data-only |
| LU | UNIVERSAL-INVESTMENT S.A. (…807) | Registration, Articles, Financial info | 3 | 271 KB real | ✅ REG + GVERTRAG(articles)=base confirmed |
| CH | BLUEROCK SWITZERLAND GMBH (…815) | Registration Extract, Company Registration | 4 | ~1 KB **stub** | ⚠️ extract delivered in-bundle but only a stub → left as additional |
| IL | OPTIVAL LTD (…818) | Certificate of Incorporation, Annual Return | 2 | 444 KB real | ✅ REG≈base, Annual Return carries shareholders |
| JP | 株式会社ブルーキャピタルマネジメント (…828) | Registry Extract | 1 | 161 KB real | ✅ REG=base |
| BE | JVG MANAGEMENT (…833) | Registry Extract, Annual Account, +1 | 3 | 139 KB real | ✅ REG=base, no articles/list doc |
| KW | CALI UNITED … WLL (…835) | Registry Extract | 1 | 244 KB real | ✅ REG=base — **fills the KW gap** (KW had 0 evidence rows) |
| SG | SC ENGINEERING (…845) | Registration (ACRA profile) | 1 | ~1 KB **stub** | ✅ profile=extract+shareholders, no separate M&A |
| HK | Ubizense (…840) | CR Particulars, Articles, Certificate, FNAR1, FNNC1 | 5 | ~1 KB **stub** | ✅ all three kinds present |

**Real document bytes: 11 jurisdictions** (BE DK ES FR IL IT JP KW LU NL US). **1 KB sandbox stubs: 4**
(CH GB HK SG) — placeholder data in the demo tenant, not a channel limitation.

**Evidence-file corrections — FINAL state after the prod cross-check** (see the PROD section below): US
GESELLSCHAFTSVERTRAG ×7 annotated as sandbox+prod-confirmed base (no change — charter is base, bylaws aren't
filed); the earlier "US base is wrong" reading was withdrawn. **DK GESELLSCHAFTSVERTRAG: the sandbox-based
additional→base flip was REVERTED** — it stays *additional* (no DK prod case to confirm base tier). **CH
REGISTERAUSZUG additional→base was applied to the curation file** (prod delivers it as mandatory).

---

# PROD cross-check — existing cases only (2026-07-23)

**Constraint:** read-only against **existing** KYC.com prod cases (`api.knowyourcustomer.com`); NO new
(billable) cases created. Prod tenant has **67 existing cases**; STP-priority jurisdictions with a Ready
(statusId=3) case: **GB, US, ES, NL, LU, CH, IL, BE** (8/15). Absent in prod: FR, IT, DK, JP, KW, SG, HK.
One representative Ready case per jurisdiction was read (documents + mandatory catalogue). Saved:
`curation/prod_check.json`.

**Key insight:** the **mandatory catalogue** is the reliable base-vs-additional signal, NOT "what was
delivered" (the sandbox ran journey="All", which also pulls additional-tier docs; and the *sandbox* mandatory
catalogue is a generic stub — it returns "Certificate of Incorporation" for every jurisdiction, so it is
useless for tiering). The **prod** mandatory catalogue is real and jurisdiction-specific:

| JD | case | prod mandatory (= base) | delivered extras | reading |
|---|---|---|---|---|
| LU | SPEEDTRACING SARL (119) | Registration, **Articles**, Financial info, Registration Certificate | — | ✅ LU GESELLSCHAFTSVERTRAG=base **confirmed** (articles are mandatory) |
| CH | BIO DEVELOPMENT AG (28) | **Registration Extract**, Company Registration | — | ⤴ CH REGISTERAUSZUG is mandatory=base → curation additional→base |
| US | INTREPID CONTROL SYSTEMS (149) | (none returned) | Registry Extract, **Incorporation** (charter), Annual Report | ✅ US GESELLSCHAFTSVERTRAG=base **confirmed** (charter delivered, same as sandbox) |
| ES | AURO HOLDCO SL (37) | Informacion Imprimible (extract) | — | ✅ REG=base; no articles → GVERTRAG additional (matches) |
| NL | Dyna Dental Engineering BV (29) | CompanyRegistration (extract) | — | ✅ REG=base; articles not mandatory → additional (matches) |
| BE | ENNOO MOBILITY BELGIUM (22) | Company Identity, Registry Extract, Annual Account | **Constitution** (statuten) | REG=base; constitution delivered but NOT mandatory → GVERTRAG additional |
| IL | PHOENIX FINANCIAL LTD (157) | Registry Extract | — | ✅ REG=base |
| GB | HSBC HOLDINGS PLC (92) | NEWINC | CS01, AA, CERTNM×… | ✅ extract/CR particulars=base, CS01=delta, no standing list |

## Corrections resulting from the prod cross-check

1. **CH REGISTERAUSZUG additional → base** *(applied to `document_kinds_curation.json`)* — prod delivers the
   extract as a mandatory document. The per-canton CHF20-50 fee applies to the *certified* extract ordered
   direct from the canton, not to the channel-delivered one.
2. **DK GESELLSCHAFTSVERTRAG base → additional — REVERTED** *(in `document_kinds_evidence.json`)*. The earlier
   sandbox-based flip was premature: "delivered in the All-journey bundle" does not prove base tier, the
   sandbox mandatory catalogue is a stub, and there is no DK prod case to confirm. The statute reading
   (vedtægter = a separately filed document) stands until a real DK prod case says otherwise.
3. **US GESELLSCHAFTSVERTRAG=base and LU GESELLSCHAFTSVERTRAG=base — both confirmed in prod** (no change).

Net: prod confirmed US & LU, corrected CH, and walked back the DK flip. **FR, IT, DK, JP, KW, SG, HK have no
prod case** — their tiering rests on statute + sandbox only and still wants a prod pull when a case exists.
