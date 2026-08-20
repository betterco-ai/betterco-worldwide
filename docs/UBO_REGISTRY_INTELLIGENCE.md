# UBO registers — market analysis and direct-connectivity map (INTERNAL)

**Scope:** EU-27 + GB, CH, NO, LI (31 jurisdictions) · **Generated:** 2026-08-20 · **Pass:** round-1-fast

> FAST PASS. Verdicts lean on secondary sources - Transparency International's field test of 14 Member States (Sept 2025) and vendor research by Kyckr and Topograph (2026) - except where a row is marked IN-HOUSE or cites an official registry page. Rows at confidence 'low' must not be quoted to a customer before the dossier treatment used in docs/REGISTRY_ACCESS_*.md.

Sibling of `REGISTRY_INTELLIGENCE.md`. That document answers *can we reach the COMPANY register directly*. This one asks the same question of the **beneficial-ownership register** — a different register, a different legal basis, and a far harsher access regime.

---

## 1. Is there an aggregator? (Q1)

**No usable one. Three archetypes exist and each fails a different requirement.**

### BORIS - the official EU interconnection

- **Who:** European Commission / e-Justice Portal
- **What it is:** The legally mandated interconnection of national UBO registers.
- **Why it fails us:** Access still runs through your own national register, so a gated home register gates BORIS too. Reported coverage is 17 of 30 EU/EEA states; output is a static PDF extract one company at a time, with no API and no bulk download.
- **Sources:** [European e-Justice Portal — Beneficial ownership registers interconnection system (BORIS)](https://e-justice.europa.eu/topics/registers-business-insolvency-land/beneficial-ownership-registers-interconnection-system-boris_en); [Transparency International — 'Countdown to new EU beneficial ownership rules', field-tested access in 14 MS (Sept 2025)](https://www.transparency.org/en/news/countdown-to-new-eu-beneficial-ownership-rules); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe)

### Derived / inferred ownership graphs

- **Who:** Moody's (Orbis, Bureau van Dijk), Dun & Bradstreet, Sayari, LSEG World-Check UBO Check (which resells D&B or Sayari), Creditsafe
- **What it is:** Global ownership networks computed by walking shareholding chains across company registers - LSEG cites 430m+ ownership connections across 220+ territories.
- **Why it fails us:** It is a calculation, not a filing. It answers 'who probably owns this' but cannot produce the register document an auditor asks for, and it is not what the UBO register says. Sayari itself reports 20-40% discrepancy against self-reported UBO questionnaires on high-risk counterparties.
- **Sources:** [LSEG World-Check UBO Check data catalogue](https://www.lseg.com/en/data-catalogue/risk/worldcheck-data/ubo-check); [Sayari - beneficial ownership for KYC](https://sayari.com/enterprise/kyc-beneficial-ownership/)

### Real-time official-register retrieval

- **Who:** Moody's/kompany, Kyckr, Topograph, Zavia, Global Database
- **What it is:** Fetch the actual official filing on request and time-stamp it. kompany advertises real-time access across 200+ jurisdictions with named integrations into the German Transparenzregister and the French INPI UBO register.
- **Why it fails us:** Their UBO-REGISTER coverage collapses to the handful of registers that are actually reachable, because they face exactly the same national access walls we do. Coverage claims of '200+ jurisdictions' describe COMPANY registers, not UBO registers.
- **Sources:** [Moody's - kompany KYC API product page (real-time official sources)](https://www.moodys.com/web/en/us/kyc/products/kompany.html); [Kyckr UBO Verify - extracts shareholder data from official filings](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025)

### The measurement we already own

Our own vendor catalogue is the sharpest measurement available: across 217 jurisdictions in jurisdiction_matrix.json, only four list a beneficial-owner DOCUMENT (EE, MT, KH, GG) - two of them in our 31-country scope. Everything else labelled 'shareholders' or 'controlling' is company-register data, not a UBO-register filing.

### Also relevant

Open Ownership closed its transnational Open Ownership Register on 29 November 2024 after seven years; the republished open datasets remain at bods-data.openownership.org.

### The regulatory clock

- **CJEU:** Joined Cases C-37/20 and C-601/20 (WM and Sovim, 22 Nov 2022) struck down public access - the cause of every closure in this dataset.
- **AMLD6:** Directive (EU) 2024/1640 Art. 11-15: obliged entities and legitimate-interest applicants regain access. Transposition of the register-access articles falls due 10 July 2026; the AMLR applies fully from 10 July 2027.
- **AMLD6 Art. 13:** From 10 November 2026 registers must answer legitimate-interest requests within 12 working days, and approved applicants get 3-year certificates - the first provision that would make an automated pipeline realistic.
- **Reality check:** As of Sept 2025 the Commission had opened infringement proceedings against 11 Member States for missing the July 2025 notification deadline. Do not plan on the 2026 dates holding.
- **Sources:** [Directive (EU) 2024/1640 (AMLD6), Art. 11-15 — register access rules](https://eur-lex.europa.eu/eli/dir/2024/1640/oj/eng); [Transparency International — 'Countdown to new EU beneficial ownership rules', field-tested access in 14 MS (Sept 2025)](https://www.transparency.org/en/news/countdown-to-new-eu-beneficial-ownership-rules)

---

## 2. Direct connectivity by country (Q2)

### Scorecard

| Verdict | Jurisdictions |
|---|---|
| 🟢 Open — reachable now | DK, GB, LV, PL |
| 🟡 Direct, credentials or contract needed | AT, DE, EE, FI, FR, LU, MT, SE, SI |
| 🟠 Only under a local obliged entity's credentials | BE, BG, HR, IE, LT, NL, NO, PT, RO |
| 🔴 Closed, suspended or authorities-only | CY, CZ, ES, GR, HU, IT, LI, SK |
| ⚫ No register exists | CH |

### At a glance

| | Register | Access regime | Foreign access | Machine access | Cost | Verdict | Conf. |
|---|---|---|---|---|---|---|---|
| **DK** | Reelle ejere (inside CVR) | public_via_s2s | yes | API | free | 🟢 | high |
| **GB** | People with Significant Control (PSC) register | public | yes | API | free | 🟢 | high |
| **LV** | Patiesa labuma guveji (Uznemumu registrs) | public | yes | portal only | free | 🟢 | medium |
| **PL** | Centralny Rejestr Beneficjentow Rzeczywistych (CRBR) | public | yes | portal only | free | 🟢 | medium |
| **AT** | Register der wirtschaftlichen Eigentuemer (WiEReG) | legitimate_interest | conditional | portal only | per_document | 🟡 | medium |
| **DE** | Transparenzregister | legitimate_interest | conditional | portal only | per_document | 🟡 | medium |
| **EE** | Tegelikud kasusaajad (e-Aeriregister) | public_local_credentials | conditional | API | free | 🟡 | medium |
| **FI** | Tosiasialliset edunsaajat | legitimate_interest | conditional | manual / email | contract | 🟡 | medium |
| **FR** | Registre des beneficiaires effectifs (RBE) | legitimate_interest | conditional | API | free | 🟡 | medium |
| **LU** | Registre des beneficiaires effectifs (RBE) | legitimate_interest | conditional | manual / email | per_document | 🟡 | medium |
| **MT** | Register of Beneficial Owners | legitimate_interest | yes | API | contract | 🟡 | medium |
| **SE** | Registret over verkliga huvudman | legitimate_interest | conditional | manual / email | per_document | 🟡 | medium |
| **SI** | Register dejanskih lastnikov (RDL) | legitimate_interest | conditional | manual / email | free | 🟡 | low |
| **BE** | UBO-register / Registre UBO | legitimate_interest | no | manual / email | free | 🟠 | low |
| **BG** | Targovski registar / registar BULSTAT (UBO declarations) | public_local_credentials | no | portal only | mixed | 🟠 | low |
| **HR** | Registar stvarnih vlasnika | legitimate_interest | no | portal only | free | 🟠 | low |
| **IE** | Register of Beneficial Ownership (RBO) | obliged_entities_only | no | none | free | 🟠 | medium |
| **LT** | JANGIS - naudos gaveju posistemis | legitimate_interest | no | API | per_query | 🟠 | medium |
| **NL** | UBO-register | obliged_entities_only | no | API | unknown | 🟠 | high |
| **NO** | Register over reelle rettighetshavere | obliged_entities_only | no | API | unknown | 🟠 | medium |
| **PT** | Registo Central do Beneficiario Efetivo (RCBE) | public_local_credentials | no | portal only | free | 🟠 | low |
| **RO** | Registrul beneficiarilor reali | public_local_credentials | conditional | portal only | per_document | 🟠 | low |
| **CY** | Register of Beneficial Owners | obliged_entities_only | no | portal only | unknown | 🔴 | low |
| **CZ** | Evidence skutecnych majitelu (ESM) | closed | no | none | unknown | 🔴 | low |
| **ES** | Registro Central de Titularidades Reales (RCTIR) | legitimate_interest | no | none | free | 🔴 | medium |
| **GR** | Kentriko Mitroo Pragmatikon Dikaiouchon (GEMI) | obliged_entities_only | no | portal only | unknown | 🔴 | low |
| **HU** | Tenyleges tulajdonosi nyilvantartas | closed | no | none | per_document | 🔴 | medium |
| **IT** | Registro dei titolari effettivi | suspended | no | none | unknown | 🔴 | medium |
| **LI** | Verzeichnis der wirtschaftlich berechtigten Personen (VwbP) | authorities_only | no | none | unknown | 🔴 | low |
| **SK** | Register pravnickych osob - konecny uzivatel vyhod | closed | no | none | free | 🔴 | medium |
| **CH** | none yet - Transparenzregister under the new LETA/TJPG law | none | no | none | n/a | ⚫ | medium |

---

## 3. What we do about it

| # | Where | Action | Why it matters | Cost |
|---|---|---|---|---|
| 1 | FR / INPI | Ask INPI whether ROLE_RBE_BENEFICIAL_OWNERS can be added to our EXISTING DATA INPI account, and whether a French SIREN is truly mandatory or only the default path. | France is the only large Member State with a real UBO API and we already run the client. This is the single highest-leverage question in the whole dataset, and it costs one email. | one email |
| 2 | LU / LBR | Ask LBR whether the EUR 5,000/year document API already covers the RBE, or only the company register. | We have already established the LBR contact path and the price. If the RBE rides on the same subscription, LU flips from manual-per-request to automated at no extra cost — and LU is in our most expensive price band. | one email |
| 3 | NL / KVK | Ask KVK whether a technical service provider may query the UBO API on behalf of a recognised Wwft institution, and what the fee model is. | The Dutch register reopened on 01.04.2026 with a certified extract available BY API — the cleanest new channel in Europe. Whether we can operate it for a customer decides if the customer-credential model works at all. | one email |
| 4 | AT + SI | File legitimate-interest applications. Both are documented as granting to foreign applicants; SI is free and AT costs ~EUR 4 per extract. | Cheapest way to convert two 'medium confidence' rows into measured fact, and to learn what the LIA process actually demands of a German applicant before we need it elsewhere. | two applications, < EUR 50 |
| 5 | EE | Re-measure and decide: obtain Smart-ID, or fall back to the vendor's EE beneficial-owner document. | Estonia's BO query now forces eID and its open data is being withdrawn from ~July 2026. Every published market comparison still calls Estonia 'fully public' — including ones a customer may quote at us. | measurement |
| 6 | LT | Add Lithuania to the vendor matrix or find another route. | LT is missing from jurisdiction_matrix.json entirely, so we currently have NO route to Lithuania at all — neither direct nor vendor. That is a coverage hole, not a UBO problem. | vendor question |
| 7 | Product | Introduce UBO as a FOURTH document kind alongside Registerauszug / Gesellschaftsvertrag / Gesellschafterliste, with the existing via='data'|'document' distinction. | Our own research already found the Gesellschafterliste is effectively unavailable outside Germany. In most Member States the UBO register is the nearest legal substitute — but it is a different document with different evidential weight, and conflating the two would be wrong. | modelling |
| 8 | Data model | Do not normalise UBO into a single ownership percentage. | Sweden records bands of control ('Omfattning'), not percentages, and several UBOs can each show the maximum. Denmark records capital and voting rights separately, and marks management as a substitute UBO (BETYDELIG_INDFLYDELSE_VIA_ROLLE) when nobody crosses 25%. A single percentage field silently falsifies both. | modelling |
| 9 | Watchlist | Put IT, CH, NL, EE and the AMLD6 transposition tracker on a scheduled re-check. | Five of the 31 rows are mid-transition with dated triggers: IT pending a CJEU ruling, CH expecting a register in autumn 2026, NL adding a JSON API in 2027, EE closing open data in July 2026, and the Art. 13 twelve-working-day rule starting 10 November 2026. | recurring |

---

## 4. Per jurisdiction

### DK — Reelle ejere (inside CVR)

**🟢 Open — reachable now** — live free S2S API delivering UBO data - already in production

- **Body:** Erhvervsstyrelsen (Danish Business Authority) · *held inside the company register, not separately*
- **Who may access:** Formally LIA since 01.09.2025 - but the system-to-system data feed was granted to us, a German non-obliged company, on written application
- **Foreign access:** yes · **credentials:** System-til-system application to Erhvervsstyrelsen plus a Tro-og-loveerklaering; HTTP Basic credentials issued. No MitID required.
- **Machine access:** API · delivers: data · document via API: **no**
- **Cost (free):** Free. No per-search or per-record charge. Only the articles of association (vedtaegter) are excluded and must be ordered for a fee.
- **BORIS:** True · **vendor today:** vendor not needed - we source DK ourselves
- **Notes:** PROVEN IN-HOUSE AND LIVE. Applied 31.07.2026, credentials 04.08.2026, UBO index confirmed by Erhvervsstyrelsen 05.08.2026. cvr-re carries 601,877 REELLE EJERE records with capital AND voting-right percentages held separately. TRAP: the Danish substitute UBO, BETYDELIG_INDFLYDELSE_VIA_ROLLE ('reel ejer som udpeget daglig ledelse'), records management because no natural person crosses 25% - that is not a beneficial owner and must not be presented as one. This row is the counter-example to the whole 'Europe is closed' narrative: a plain written application to the registry succeeded where the eID/LIA front door would have failed.
- **Confidence:** high
- **Sources:** [IN-HOUSE, measured: registry-access/DK_CVR/NOTIZ.md — S2S access granted 04.08.2026; cvr-re carries 601,877 'REELLE EJERE' records](https://distribution.virk.dk:8443/cvr-re/_search); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [Transparency International — 'Countdown to new EU beneficial ownership rules', field-tested access in 14 MS (Sept 2025)](https://www.transparency.org/en/news/countdown-to-new-eu-beneficial-ownership-rules)
- **URL:** <https://distribution.virk.dk:8443/cvr-re>

### GB — People with Significant Control (PSC) register

**🟢 Open — reachable now** — free public REST API and bulk data - nothing in Europe comes close

- **Body:** Companies House
- **Who may access:** Everyone. Free REST API and bulk downloads, no credentials beyond a free API key.
- **Foreign access:** yes · **credentials:** Free Companies House API key
- **Machine access:** API · delivers: data · document via API: **no**
- **Cost (free):** Free API, free bulk product data
- **BORIS:** False · **vendor today:** we already run a GB connector
- **Notes:** THE BENCHMARK, and proof that open UBO data is technically trivial once it is legally permitted. Not EU, so untouched by the CJEU ruling. QUALITY CAVEAT: historically self-declared and unverified - roughly a fifth of records miss an individual owner and a fifth sum above 100%. The ECCTA identity-verification reform is closing that gap.
- **Confidence:** high
- **Sources:** [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025)
- **URL:** <https://developer.company-information.service.gov.uk/>

### LV — Patiesa labuma guveji (Uznemumu registrs)

**🟢 Open — reachable now** — public and free; machine access still has to be built or licensed

- **Body:** Latvijas Republikas Uznemumu registrs · *held inside the company register, not separately*
- **Who may access:** Everyone - Latvia decided explicitly to keep the register public after the CJEU ruling
- **Foreign access:** yes · **credentials:** None for the public view; login needed to download supporting documents
- **Machine access:** portal only · delivers: data, document · document via API: **no**
- **Cost (free):** Free public view of current UBO data; free downloadable UBO statements
- **BORIS:** True · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** One of only three genuinely open registers left in the EU, and TI independently confirms it. There is no official bulk or API channel for UBO: the machine path is either a licensed Latvian redistributor or our own scraper. New national requirements were announced for 2026 - check whether they touch access or only filing duties.
- **Confidence:** medium
- **Sources:** [Transparency International — 'Countdown to new EU beneficial ownership rules', field-tested access in 14 MS (Sept 2025)](https://www.transparency.org/en/news/countdown-to-new-eu-beneficial-ownership-rules); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025)
- **URL:** <https://www.ur.gov.lv/>

### PL — Centralny Rejestr Beneficjentow Rzeczywistych (CRBR)

**🟢 Open — reachable now** — fully public and free, but needs a scraper because there is no official API

- **Body:** Ministerstwo Finansow
- **Who may access:** Everyone. No registration and no fee - Poland kept the register fully public.
- **Foreign access:** yes · **credentials:** None
- **Machine access:** portal only · delivers: data, document · document via API: **no**
- **Cost (free):** Free, unlimited public search
- **BORIS:** unclear · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** Legally the easiest UBO source in the EU and technically the most annoying: there is NO official API. Access is portal-only, so everyone operating at scale either scrapes CRBR or buys a Polish redistributor such as Transparent Data. Our commercial-register intelligence already rates PL a strong go-direct; the UBO piece is a separate, unofficial build.
- **Confidence:** medium
- **Sources:** [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025)
- **URL:** <https://crbr.podatki.gov.pl/>

### AT — Register der wirtschaftlichen Eigentuemer (WiEReG)

**🟡 Direct, credentials or contract needed** — LIA granted to foreign applicants in practice; per-extract fee; no API

- **Body:** Bundesministerium fuer Finanzen (Registerbehoerde)
- **Who may access:** Authorities, obliged entities under WiEReG, and applicants showing legitimate interest since 01.09.2023
- **Foreign access:** conditional · **credentials:** Application to the Registerbehoerde (wiereg-registerbehoerde@bmf.gv.at); TI's tester was asked for an employment contract; eID for the portal path
- **Machine access:** portal only · delivers: document · document via API: **no**
- **Cost (per_document):** ~EUR 4 per simple extract, up to ~EUR 10 extended. TI measured EUR 4 and ~20 days to approval.
- **BORIS:** True · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** The extract carries a 'Vollstaendigkeitspruefung' completeness flag - a data-quality signal no other MS provides. Refusals are formal administrative decisions and therefore appealable. Austria is one of the few LIA states that demonstrably approves foreign applicants.
- **Confidence:** medium
- **Sources:** [Transparency International — 'Countdown to new EU beneficial ownership rules', field-tested access in 14 MS (Sept 2025)](https://www.transparency.org/en/news/countdown-to-new-eu-beneficial-ownership-rules); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025)
- **URL:** <https://www.bmf.gv.at/themen/betrugsbekaempfung/wirtschaftliche-eigentuemer-register.html>

### DE — Transparenzregister

**🟡 Direct, credentials or contract needed** — cheap and open in principle to obliged entities; the queue is the barrier

- **Body:** Bundesanzeiger Verlag (beliehen), supervised by the BVA
- **Who may access:** Authorities, obliged entities under the GwG, and legitimate-interest applicants since the CJEU ruling
- **Foreign access:** conditional · **credentials:** Online registration, German-language process, written justification of legal need
- **Machine access:** portal only · delivers: document · document via API: **no**
- **Cost (per_document):** ~EUR 1.65 per extract (TI). Registration free.
- **BORIS:** True · **vendor today:** OUT OF KYC.COM SCOPE - we source Germany ourselves
- **Notes:** A build row, not a buy row. Processing time is the barrier, not price: TI had no response since March 2025 and Topograph reports an application pending over a year against official guidance of 'several weeks'. Moody's/kompany advertises a Transparenzregister integration, which is evidence the channel can be made to work commercially.
- **Confidence:** medium
- **Sources:** [Transparency International — 'Countdown to new EU beneficial ownership rules', field-tested access in 14 MS (Sept 2025)](https://www.transparency.org/en/news/countdown-to-new-eu-beneficial-ownership-rules); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025)
- **URL:** <https://www.transparenzregister.de/>

### EE — Tegelikud kasusaajad (e-Aeriregister)

**🟡 Direct, credentials or contract needed** — API is free but the BO endpoint now needs Estonian eID and open data is being withdrawn

- **Body:** Registrite ja Infosuesteemide Keskus (RIK) · *held inside the company register, not separately*
- **Who may access:** Was fully public and free. Measured 2026-08-20: the BO query now forces authentication (ID-card / Mobile-ID / Smart-ID). An amendment removes BO data from the open-data files and restricts individual queries and API services from ~July 2026.
- **Foreign access:** conditional · **credentials:** Estonian eID means. Smart-ID is obtainable by some non-residents - the only realistic foreign path.
- **Machine access:** API · delivers: data, document · document via API: **yes**
- **Cost (free):** Register data free since the 2023 open-data reform; BO data now being pulled out of the open-data set
- **BORIS:** True · **vendor today:** KYC.com lists a 'Beneficial owners' DOCUMENT for EE
- **Notes:** THE HEADLINE CHANGE. Estonia was the EU's most open UBO register and every published comparison still calls it 'fully public'. That is now outdated - we measured the auth redirect ourselves. Because our vendor lists an EE beneficial-owner document, we have a fallback if the direct route closes entirely.
- **Confidence:** medium
- **Sources:** [IN-HOUSE, measured 2026-08-20: the BO query returns HTTP 303 to auth.rik.ee (idcard/mid/smartid) — no longer anonymous](https://ariregister.rik.ee/eng/beneficial_owners_query); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [IN-HOUSE: jurisdiction_matrix.json (KYC.com catalogue, 217 jurisdictions) — only EE, MT, KH, GG list a beneficial-owner DOCUMENT](file://betterco-worldwide/jurisdiction_matrix.json)
- **URL:** <https://ariregister.rik.ee/eng/beneficial_owners_query>

### FI — Tosiasialliset edunsaajat

**🟡 Direct, credentials or contract needed** — contractual access open to foreign institutions, but no API and an entity-type coverage gap

- **Body:** Patentti- ja rekisterihallitus (PRH)
- **Who may access:** Authorities, obliged entities and legitimate-interest applicants under a data-use contract
- **Foreign access:** conditional · **credentials:** Data-use contract with PRH; foreign banks accepted with justification
- **Machine access:** manual / email · delivers: document · document via API: **no**
- **Cost (contract):** Topograph: EUR 200 up front plus EUR 0.90 per extract. TI measured EUR 7-200. Contract-based, so the real number is negotiated.
- **BORIS:** unclear · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** COVERAGE GAP no other MS has: the register covers private limited companies (Oy) only - no data for Oyj, associations, foundations or sole traders. Sources disagree on price; the contract is the thing to negotiate.
- **Confidence:** medium
- **Sources:** [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [Transparency International — 'Countdown to new EU beneficial ownership rules', field-tested access in 14 MS (Sept 2025)](https://www.transparency.org/en/news/countdown-to-new-eu-beneficial-ownership-rules); [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025)
- **URL:** <https://www.prh.fi/en/kaupparekisteri/beneficial-owners.html>

### FR — Registre des beneficiaires effectifs (RBE)

**🟡 Direct, credentials or contract needed** — real API and we already hold an INPI account; needs the RBE entitlement and likely a French SIREN

- **Body:** INPI (since the RNE transfer)
- **Who may access:** Authorities, obliged entities, legitimate interest. Public access withdrawn after the CJEU ruling.
- **Foreign access:** conditional · **credentials:** INPI account plus AML documentation plus a French SIREN; full BO fields require the ROLE_RBE_BENEFICIAL_OWNERS entitlement on the DATA INPI API
- **Machine access:** API · delivers: data · document via API: **no**
- **Cost (free):** Free once approved
- **BORIS:** True · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** STRATEGICALLY THE MOST IMPORTANT ROW. France is the only large MS with a real UBO API - and we already run an INPI client for the RNE (inpi_client.py, docs/FR_INPI_INTEGRATION.md). The blocker is the entitlement, not the plumbing. The SIREN requirement means a cross-border mandate needs a French registration. ACTION: ask INPI whether ROLE_RBE_BENEFICIAL_OWNERS can be granted on our existing account.
- **Confidence:** medium
- **Sources:** [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [Transparency International — 'Countdown to new EU beneficial ownership rules', field-tested access in 14 MS (Sept 2025)](https://www.transparency.org/en/news/countdown-to-new-eu-beneficial-ownership-rules); [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025)
- **URL:** <https://data.inpi.fr/>

### LU — Registre des beneficiaires effectifs (RBE)

**🟡 Direct, credentials or contract needed** — manual today; the paid LBR API may already cover it - unverified

- **Body:** Luxembourg Business Registers (LBR)
- **Who may access:** Article 2 professionals have a standing channel under Circular LBR 22/01; everyone else applies case by case
- **Foreign access:** conditional · **credentials:** Article 2 professional status, or a manual application per company
- **Machine access:** manual / email · delivers: document · document via API: **no**
- **Cost (per_document):** EUR 5 per request
- **BORIS:** True · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** Partly suspended since July 2022 and still not fully operational. NOTE THE CONTRAST with our LU company-register finding: the LBR API is confirmed to deliver documents but costs EUR 5,000/year (docs/REGISTRY_ACCESS_IT_ES_LU_2026-07-30.md). Whether that paid API also carries the RBE is UNVERIFIED and is the cheapest open question in this dataset - we already have the LBR contact path. LU sits in the High price band together with FR, our most expensive pair.
- **Confidence:** medium
- **Sources:** [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [Transparency International — 'Countdown to new EU beneficial ownership rules', field-tested access in 14 MS (Sept 2025)](https://www.transparency.org/en/news/countdown-to-new-eu-beneficial-ownership-rules); [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025)
- **URL:** <https://www.lbr.lu/>

### MT — Register of Beneficial Owners

**🟡 Direct, credentials or contract needed** — cheapest API subscription in the set - and already covered by the vendor

- **Body:** Malta Business Registry (MBR)
- **Who may access:** Authorities, obliged entities and legitimate interest; email requests accepted; open to EU citizens holding a digital ID
- **Foreign access:** yes · **credentials:** EU digital ID, or an AML-justified email request
- **Machine access:** API · delivers: document · document via API: **yes**
- **Cost (contract):** EUR 5 per scanned extract on the manual path; API subscription reported at EUR 450/year, pending validation
- **BORIS:** True · **vendor today:** KYC.com lists a 'Beneficial Owner Printout' DOCUMENT for MT
- **Notes:** One of only two EU/EEA jurisdictions where our vendor already delivers a UBO-register DOCUMENT, so Malta is covered today. The EUR 450/year API only pays off at volume.
- **Confidence:** medium
- **Sources:** [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025); [IN-HOUSE: jurisdiction_matrix.json (KYC.com catalogue, 217 jurisdictions) — only EE, MT, KH, GG list a beneficial-owner DOCUMENT](file://betterco-worldwide/jurisdiction_matrix.json)
- **URL:** <https://mbr.mt/>

### SE — Registret over verkliga huvudman

**🟡 Direct, credentials or contract needed** — clear process with an email path for foreigners; PDF only, no API

- **Body:** Bolagsverket
- **Who may access:** Authorities, obliged entities and legitimate interest; TI got immediate access via eID and describes the process as clear
- **Foreign access:** conditional · **credentials:** Swedish BankID for instant access; email request otherwise, answered in days
- **Machine access:** manual / email · delivers: document · document via API: **no**
- **Cost (per_document):** Topograph: SEK 120 per extract. TI recorded no fee. Discrepancy unresolved.
- **BORIS:** unclear · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** DATA-MODEL TRAP: Sweden records 'Omfattning' - the extent of control in bands - not an ownership percentage, and several UBOs can each show the maximum band. Any normalisation into a percentage model will be wrong. Output is PDF and has to be parsed. Otherwise one of the smoothest LIA processes tested.
- **Confidence:** medium
- **Sources:** [Transparency International — 'Countdown to new EU beneficial ownership rules', field-tested access in 14 MS (Sept 2025)](https://www.transparency.org/en/news/countdown-to-new-eu-beneficial-ownership-rules); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025)
- **URL:** <https://bolagsverket.se/>

### SI — Register dejanskih lastnikov (RDL)

**🟡 Direct, credentials or contract needed** — free, manual, and reportedly broad in granting AML-justified access

- **Body:** AJPES
- **Who may access:** Authorities, obliged entities and legitimate-interest applicants; AJPES applies a broad reading of AML justification
- **Foreign access:** conditional · **credentials:** Email application with supporting documents; eID for the portal path
- **Machine access:** manual / email · delivers: data · document via API: **no**
- **Cost (free):** Free
- **BORIS:** unclear · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** Both secondary sources describe Slovenia as one of the more cooperative LIA regimes, and it costs nothing. Cheap to test - a good candidate for an early application alongside Austria.
- **Confidence:** low
- **Sources:** [Transparency International — 'Countdown to new EU beneficial ownership rules', field-tested access in 14 MS (Sept 2025)](https://www.transparency.org/en/news/countdown-to-new-eu-beneficial-ownership-rules); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025)
- **URL:** <https://www.ajpes.si/>

### BE — UBO-register / Registre UBO

**🟠 Only under a local obliged entity's credentials** — access tied to Belgian obliged-entity status; no API

- **Body:** FOD Financien / SPF Finances - Algemene Administratie van de Thesaurie
- **Who may access:** Authorities, Belgian AML-obliged entities and legitimate-interest applicants; public access withdrawn Nov 2022
- **Foreign access:** no · **credentials:** Belgian legal presence in practice: FPS Finance whitelisting, document submission and (per Topograph) a video call. ForReg credentials only cover filing your own entity, not third-party lookups.
- **Machine access:** manual / email · delivers: document · document via API: **no**
- **Cost (free):** No fee reported. TI: free, response in under a week where granted.
- **BORIS:** True · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** SOURCE CONFLICT: TI obtained email-based access in under a week; Topograph reports Belgian establishment is required. Both can hold if the email path is open to EU obliged entities but not to a foreign software vendor. Our own BE dossier (docs/REGISTRY_ACCESS_BE_IL_2026-07-30.md) covers the COMPANY register only - the UBO register was never tested. Needs the dossier treatment.
- **Confidence:** low
- **Sources:** [Transparency International — 'Countdown to new EU beneficial ownership rules', field-tested access in 14 MS (Sept 2025)](https://www.transparency.org/en/news/countdown-to-new-eu-beneficial-ownership-rules); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025)
- **URL:** <https://finance.belgium.be/en/E-services/ubo-register>

### BG — Targovski registar / registar BULSTAT (UBO declarations)

**🟠 Only under a local obliged entity's credentials** — UBO detail gated behind a Bulgarian e-signature

- **Body:** Agenciya po vpisvaniyata (Registry Agency) · *held inside the company register, not separately*
- **Who may access:** Basic register data public; UBO detail behind a Bulgarian qualified electronic signature
- **Foreign access:** no · **credentials:** Bulgarian qualified electronic signature (KEP)
- **Machine access:** portal only · delivers: data · document via API: **no**
- **Cost (mixed):** Basic search free; certified extracts fee-based (not verified)
- **BORIS:** unclear · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** UBO data sits INSIDE the commercial register rather than in a separate one, so our existing BG company-register route may already carry part of it. Untested, single secondary source.
- **Confidence:** low
- **Sources:** [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe)
- **URL:** <https://portal.registryagency.bg/>

### HR — Registar stvarnih vlasnika

**🟠 Only under a local obliged entity's credentials** — NIAS eID cannot be obtained by a foreign company

- **Body:** Financijska agencija (FINA) / Ministarstvo financija
- **Who may access:** Authorities, obliged entities, legitimate interest; sign-in through the national NIAS identity system
- **Foreign access:** no · **credentials:** NIAS (Croatian national eID) - residents and local entities only
- **Machine access:** portal only · delivers: data · document via API: **no**
- **Cost (free):** Free where access is granted
- **BORIS:** unclear · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** Named by both secondary sources as a national-credential lock. Not tested.
- **Confidence:** low
- **Sources:** [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe)
- **URL:** <https://rsv.fina.hr/>

### IE — Register of Beneficial Ownership (RBO)

**🟠 Only under a local obliged entity's credentials** — BOR4 access is reserved to Irish designated persons

- **Body:** Registrar of Beneficial Ownership (with the CRO)
- **Who may access:** Irish AML-designated persons via Form BOR4; legitimate-interest applicants via Form BOR5
- **Foreign access:** no · **credentials:** Irish designated-person status; paper/PDF forms
- **Machine access:** none · delivers: document · document via API: **no**
- **Cost (free):** No fee reported
- **BORIS:** unclear · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** Ireland issued an outright refusal to TI, demanding proof that the target company was linked to convicted money launderers or to assets in high-risk countries. The BOR4 route does work - but only for an Irish designated person. A textbook customer-credential row.
- **Confidence:** medium
- **Sources:** [Transparency International — 'Countdown to new EU beneficial ownership rules', field-tested access in 14 MS (Sept 2025)](https://www.transparency.org/en/news/countdown-to-new-eu-beneficial-ownership-rules); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025)
- **URL:** <https://rbo.gov.ie/>

### LT — JANGIS - naudos gaveju posistemis

**🟠 Only under a local obliged entity's credentials** — cheap and bulk-capable but locked behind Lithuanian eID - and no vendor fallback

- **Body:** Registru centras
- **Who may access:** Authorities, obliged entities and legitimate-interest applicants; TI reports both general and case-by-case access exist
- **Foreign access:** no · **credentials:** Lithuanian ID card or mobile signature; Lithuania-based entities in practice
- **Machine access:** API · delivers: data · document via API: **no**
- **Cost (per_query):** EUR 0.03-2.93 per query; bulk querying available to holders of access
- **BORIS:** unclear · **vendor today:** NONE - LT is absent from jurisdiction_matrix.json entirely
- **Notes:** TWO PROBLEMS. (1) Access needs Lithuanian eID. (2) LITHUANIA IS NOT IN OUR VENDOR MATRIX AT ALL - so we have neither a direct route nor a vendor route today. TI also flagged a 20-plus question balancing form available only in Lithuanian. At EUR 0.03 per query it would be the cheapest source in Europe if the door could be opened.
- **Confidence:** medium
- **Sources:** [Transparency International — 'Countdown to new EU beneficial ownership rules', field-tested access in 14 MS (Sept 2025)](https://www.transparency.org/en/news/countdown-to-new-eu-beneficial-ownership-rules); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [IN-HOUSE: jurisdiction_matrix.json (KYC.com catalogue, 217 jurisdictions) — only EE, MT, KH, GG list a beneficial-owner DOCUMENT](file://betterco-worldwide/jurisdiction_matrix.json)
- **URL:** <https://www.registrucentras.lt/>

### NL — UBO-register

**🟠 Only under a local obliged entity's credentials** — certified extract via API exists, but only recognised Dutch Wwft institutions are eligible

- **Body:** Kamer van Koophandel (KVK)
- **Who may access:** Recognised Wwft and sanctions institutions since 01.04.2026: civil-law notaries, banks, trust offices, DNB-licensed life insurers, AFM-licensed investment firms and credit providers. Notification runs through the sector organisations.
- **Foreign access:** no · **credentials:** Recognition as a Dutch Wwft/sanctions institution; eHerkenning for the web-ordering path from Q2 2026
- **Machine access:** API · delivers: document · document via API: **yes**
- **Cost (unknown):** Not published on the access page
- **BORIS:** True · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** THE MOST CONCRETE NEW OPPORTUNITY, and the only fully official source in this dataset. Shut in Nov 2022, reopened 01.04.2026 with a digitally certified UBO extract (PDF) orderable BY API; a JSON 'UBO API 2.0' is planned for ~2027. The catch is the eligibility list - a German software vendor is not on it. This is the archetype for the customer-credential model: the customer is the Wwft institution, we are the pipe. KVK's page does not address third-party or foreign access, so ASK KVK directly.
- **Confidence:** high
- **Sources:** [KVK (OFFICIAL) — 'Access to UBO Register for vennootschappen easier', reopening 1 April 2026](https://www.kvk.nl/en/ubo/ubo-access-expanded/); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025)
- **URL:** <https://www.kvk.nl/en/ubo/ubo-access-expanded/>

### NO — Register over reelle rettighetshavere

**🟠 Only under a local obliged entity's credentials** — API-only register restricted to authorities and obliged entities

- **Body:** Bronnoysundregistrene
- **Who may access:** Authorities and obliged entities. Filing became mandatory in July 2025. There is no public web interface at all.
- **Foreign access:** no · **credentials:** Norwegian obliged-entity status
- **Machine access:** API · delivers: data · document via API: **no**
- **Cost (unknown):** Not published
- **BORIS:** True · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** Inverted from everywhere else: Norway built an API-ONLY register with no portal. The data is machine-shaped and the entitlement is the wall. The public Bronnoysund business-register API - which we can already use - does NOT expose the UBO data.
- **Confidence:** medium
- **Sources:** [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe)
- **URL:** <https://www.brreg.no/>

### PT — Registo Central do Beneficiario Efetivo (RCBE)

**🟠 Only under a local obliged entity's credentials** — Portuguese citizen-card authentication only

- **Body:** Instituto dos Registos e do Notariado (IRN)
- **Who may access:** Was public; a legitimate-interest decree of October 2025 is not yet deployed. Access in practice needs a Portuguese Cartao de Cidadao.
- **Foreign access:** no · **credentials:** Cartao de Cidadao / Chave Movel Digital
- **Machine access:** portal only · delivers: data · document via API: **no**
- **Cost (free):** Free where accessible
- **BORIS:** unclear · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** In transition: the new access framework is announced but not live. Re-check once the decree is deployed.
- **Confidence:** low
- **Sources:** [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe)
- **URL:** <https://rcbe.justica.gov.pt/>

### RO — Registrul beneficiarilor reali

**🟠 Only under a local obliged entity's credentials** — local e-signature plus explicit resale restrictions

- **Body:** Oficiul National al Registrului Comertului (ONRC) · *held inside the company register, not separately*
- **Who may access:** Public in principle and transitioning to legitimate interest; requests are filed with ONRC
- **Foreign access:** conditional · **credentials:** Romanian qualified electronic signature for the online channel
- **Machine access:** portal only · delivers: document · document via API: **no**
- **Cost (per_document):** Fee-based; ONRC restricts API-based resale
- **BORIS:** unclear · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** Both sources agree ONRC restricts redistribution - which matters more to us than the fee, because our product IS redistribution. Same pattern we already found in Italy, where standard Telemaco forbids passing data to customers without an operator contract. Verify the licence terms before building.
- **Confidence:** low
- **Sources:** [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe)
- **URL:** <https://www.onrc.ro/>

### CY — Register of Beneficial Owners

**🔴 Closed, suspended or authorities-only** — authorities and local obliged entities only

- **Body:** Department of Registrar of Companies and Intellectual Property (DRCIP)
- **Who may access:** Competent authorities and obliged entities; public access ceased 03.01.2023 after the CJEU ruling
- **Foreign access:** no · **credentials:** Cypriot authentication plus obliged-entity status
- **Machine access:** portal only · delivers: data · document via API: **no**
- **Cost (unknown):** Not published for the restricted channel
- **BORIS:** unclear · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** Cyprus has run the register on and off since 2023. Any published status here is perishable - re-check before quoting.
- **Confidence:** low
- **Sources:** [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe)
- **URL:** <https://www.companies.gov.cy/en/business-entities/ubo-register>

### CZ — Evidence skutecnych majitelu (ESM)

**🔴 Closed, suspended or authorities-only** — public channel withdrawn Dec 2025, court application only

- **Body:** Ministerstvo spravedlnosti - municipal courts
- **Who may access:** Partial public access ended December 2025; access reverted to a court-application model
- **Foreign access:** no · **credentials:** Court application
- **Machine access:** none · delivers: document · document via API: **no**
- **Cost (unknown):** Court fee, not verified
- **BORIS:** unclear · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** The clearest REGRESSION in the dataset: Czechia had a working partial public channel and closed it. Both secondary sources agree on the December 2025 date; the replacement procedure is unverified.
- **Confidence:** low
- **Sources:** [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe)
- **URL:** <https://esm.justice.cz/>

### ES — Registro Central de Titularidades Reales (RCTIR)

**🔴 Closed, suspended or authorities-only** — nominally LIA, non-functional in practice for a foreign applicant

- **Body:** Ministerio de Justicia (alongside the notarial Base de Datos de Titularidad Real of the Consejo General del Notariado)
- **Who may access:** Authorities, obliged entities, legitimate interest - but TI found the access channel entirely non-functional
- **Foreign access:** no · **credentials:** DNI/NIE or a Spanish electronic certificate; Spanish-language process
- **Machine access:** none · delivers: data · document via API: **no**
- **Cost (free):** Free today, fees announced
- **BORIS:** unclear · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** TI's tester waited about six months and called the eID path entirely non-functional. Spain has TWO sources: the state RCTIR and the notaries' own titularidad real database, which the notarial network sells to obliged entities - that second path is what Spanish banks actually use and it is NOT assessed here. Our ES company-register dossier already found that a certificado electronico or Cl@ve is mandatory even for the company register - the same wall.
- **Confidence:** medium
- **Sources:** [Transparency International — 'Countdown to new EU beneficial ownership rules', field-tested access in 14 MS (Sept 2025)](https://www.transparency.org/en/news/countdown-to-new-eu-beneficial-ownership-rules); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025)
- **URL:** <https://www.mjusticia.gob.es/>

### GR — Kentriko Mitroo Pragmatikon Dikaiouchon (GEMI)

**🔴 Closed, suspended or authorities-only** — suspended for all but authorities and local obliged entities

- **Body:** Ypourgeio Oikonomikon / GEMI
- **Who may access:** Authorities and local obliged entities; public access suspended 01.12.2022
- **Foreign access:** no · **credentials:** TAXISnet / Greek national authentication
- **Machine access:** portal only · delivers: data · document via API: **no**
- **Cost (unknown):** Not published
- **BORIS:** True · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** Reported among the countries with searchable BORIS records while the domestic channel is closed - the same contradiction as Liechtenstein. Worth one probe if BORIS access is ever obtained.
- **Confidence:** low
- **Sources:** [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe)
- **URL:** <https://www.businessportal.gr/>

### HU — Tenyleges tulajdonosi nyilvantartas

**🔴 Closed, suspended or authorities-only** — circular criteria, applied to refuse in practice

- **Body:** NAV / BISZ Zrt.
- **Who may access:** Authorities; others must prove a family, legal, ownership or business tie to the target company
- **Foreign access:** no · **credentials:** Proof of a pre-existing connection to the target entity
- **Machine access:** none · delivers: document · document via API: **no**
- **Cost (per_document):** ~EUR 3.79 per extract (TI)
- **BORIS:** unclear · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** The criterion is circular: to look up who owns a company you must already show a link to its owners. TI waited four months against a stated 30-day limit and was refused. Treat as unavailable.
- **Confidence:** medium
- **Sources:** [Transparency International — 'Countdown to new EU beneficial ownership rules', field-tested access in 14 MS (Sept 2025)](https://www.transparency.org/en/news/countdown-to-new-eu-beneficial-ownership-rules); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe); [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025)
- **URL:** <https://nav.gov.hu/>

### IT — Registro dei titolari effettivi

**🔴 Closed, suspended or authorities-only** — register frozen pending a CJEU ruling

- **Body:** Camere di Commercio / InfoCamere (Registro Imprese) · *held inside the company register, not separately*
- **Who may access:** Nobody outside authorities pending the CJEU reference. A legitimate-interest basis exists on paper from January 2026 but the register is frozen.
- **Foreign access:** no · **credentials:** n/a while frozen
- **Machine access:** none · delivers: document · document via API: **no**
- **Cost (unknown):** n/a while frozen
- **BORIS:** unclear · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** Italy built the register, the Consiglio di Stato suspended it and referred trust-access questions to the CJEU, and a March 2026 decree reportedly restarts the framework. We already hold a Telemaco/ABDO route to the Italian COMPANY register (docs/REGISTRY_ACCESS_IT_ES_LU_2026-07-30.md) and the UBO section would ride on the same access once it reopens. Highest-value row to re-check on a schedule.
- **Confidence:** medium
- **Sources:** [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe)
- **URL:** <https://www.registroimprese.it/>

### LI — Verzeichnis der wirtschaftlich berechtigten Personen (VwbP)

**🔴 Closed, suspended or authorities-only** — authorities only, with per-entity applications for banks

- **Body:** Amt fuer Justiz (AJU)
- **Who may access:** Authorities and the FIU; banks apply per entity
- **Foreign access:** no · **credentials:** n/a
- **Machine access:** none · delivers: document · document via API: **no**
- **Cost (unknown):** Not published
- **BORIS:** True · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** Extracts explicitly carry no public reliance - the authority does not verify the data. Liechtenstein is connected to BORIS while being closed domestically, the same contradiction as Greece.
- **Confidence:** low
- **Sources:** [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe)
- **URL:** <https://www.llv.li/>

### SK — Register pravnickych osob - konecny uzivatel vyhod

**🔴 Closed, suspended or authorities-only** — public UBO access withdrawn July 2025; only the public-sector RPVS subset remains

- **Body:** Statisticky urad SR (the separate RPVS is run by the Ministry of Justice)
- **Who may access:** Authorities only - public access to beneficial-ownership data was discontinued on 10.07.2025, the exact AMLD6 Art. 74 date
- **Foreign access:** no · **credentials:** n/a
- **Machine access:** none · delivers: data · document via API: **no**
- **Cost (free):** n/a
- **BORIS:** unclear · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** PARTIAL WORKAROUND: the Register partnerov verejneho sektora (RPVS) is a DIFFERENT, still-public register that discloses verified beneficial owners - but only for entities doing business with the Slovak public sector. Useful for a subset, useless as general coverage. Slovakia is rated a strong go-direct for the company register, so the split between its two registers is unusually sharp.
- **Confidence:** medium
- **Sources:** [Kyckr — 'EU UBO Register Access for Obliged Entities (2026 Guide)' (vendor blog; SECONDARY)](https://kyckr.com/guides-and-reports/eu-ubo-register-access-for-obliged-entities-2025); [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe)
- **URL:** <https://rpo.statistics.sk/>

### CH — none yet - Transparenzregister under the new LETA/TJPG law

**⚫ No register exists** — no register exists; the coming one is authorities-and-Swiss-banks only

- **Body:** Eidgenoessisches Justiz- und Polizeidepartement; delivery expected via EasyGov
- **Who may access:** Nobody today. The law adopted in September 2025 creates a register expected in autumn 2026, restricted to domestic authorities and Swiss financial intermediaries.
- **Foreign access:** no · **credentials:** n/a
- **Machine access:** none · delivers: nothing · document via API: **no**
- **Cost (n/a):** Non-filing penalty reported up to CHF 500,000; access pricing unknown
- **BORIS:** False · **vendor today:** shareholder data only (no UBO-register document)
- **Notes:** Switzerland has NO beneficial-ownership register at all right now. The honest answer to a customer asking for a Swiss UBO document is that it does not exist, and that when it does it will be closed to us. Ties directly to the open VR-Data CH vendor question (docs/VRDATA_CH_ANSWER_2026-08-11.md): if a vendor claims a Swiss UBO source today, ask precisely what it is.
- **Confidence:** medium
- **Sources:** [Topograph — 'UBO register access in Europe: a country-by-country reality check' (vendor blog, hands-on detail; SECONDARY)](https://www.topograph.co/blog/ubo-register-access-in-europe)
- **URL:** <https://www.easygov.swiss/>

