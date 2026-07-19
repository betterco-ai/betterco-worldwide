# Registry intelligence — build vs. buy (INTERNAL)

For each analysed jurisdiction: what the registry is, whether it has an open API (and whether that API serves **documents** or only data), and the cost — to decide where we can integrate **directly** instead of paying an aggregation vendor.

> Verdict driver: the prize is a registry we can hit directly that also serves the **documents** (not just data), cheaply. Data-only or no-API → keep the vendor for filings.

## Scorecard

| Verdict | Jurisdictions |
|---|---|
| 🟢 Go direct (strong) | DK, FR, GB, PL |
| 🟢 Go direct (paid docs) | IE, IT, NO |
| 🟡 Direct, contract needed | AT, AU, ES, SE, ZA |
| 🟠 Direct for DATA only — vendor for documents | BE, CA, CH, CZ, FI, IL, IN, JE, LU, MT, NL, NZ, SG |
| 🔴 Vendor only (no usable API) | AE, BM, BR, BS, CN, CY, GG, HK, IM, JP, KR, KY, LI, MU, MX, PA, PT, SC, TR, US, VG |

## Per jurisdiction

### AE — DIFC Public Register + ADGM Registration Authority Online Registry (plus fragmented mainland DED/DET registries)

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** DIFC Registrar of Companies (DIFC Authority); ADGM Registration Authority; mainland: each emirate's Department of Economic Development (Dubai DET, Abu Dhabi ADDED, etc.) — no single national registrar
- **Open API:** no · DIFC Public Register (web search); ADGM Online Registry Solution / public register (web search) — no open developer API on either · docs: <https://www.adgm.com/registration-authority/registration-and-incorporation>
- **Delivers:** data | documents via API: **no**
- **Auth:** Public register web search is unauthenticated (no login) but has no programmatic API; filing/document ordering requires a portal account.
- **Cost (free):** Basic entity lookup (name, registration number, status, registered address, licence/activity) is free via the DIFC and ADGM public registers. Certificates and filed documents are ordered for per-document fees through the respective portals; mainland trade-licence verification is per-emirate and largely free/manual.
- **Notes:** UAE is fragmented — three worlds. DIFC and ADGM are separate common-law free zones, each with its own online public register (free structured search, no API, documents orderable for a fee). Mainland is split across each emirate's DED/DET plus dozens of free zones (JAFZA, DMCC, RAKEZ...), each with its own system and mostly no public bulk search or API. NO unified UAE registry and NO open API anywhere; direct integration would mean building multiple bespoke scrapers. An aggregation vendor is hard to avoid for broad UAE coverage.
- **Confidence:** medium
- **Sources:** [DIFC public register page (official difc.com)](https://www.difc.com/business/public-register); [ADGM Registration Authority / Online Registry Solution (official adgm.com)](https://www.adgm.com/registration-authority/registration-and-incorporation)

### AT — Firmenbuch (Austrian Company/Business Register)

**🟡 Direct, contract needed** — documents via API but access is contract/gated (negotiation needed)

- **Body:** Kept by the Austrian courts under the Federal Ministry of Justice; commercial online access resold only through contracted Verrechnungsstellen (e.g. firmenbuchgrundbuch.at / Compass)
- **Open API:** partial · No official open developer API. Machine/API access only via the paid Verrechnungsstellen (JustizOnline offers a free single web lookup, not an API) · docs: <https://www.firmenbuchgrundbuch.at/en>
- **Delivers:** data, documents | documents via API: **yes**
- **Auth:** Contract/registration with a licensed Verrechnungsstelle; requires Austrian identification. No open self-serve key.
- **Cost (per_document):** Charged per extract via Verrechnungsstellen. Current Firmenbuchauszug approx EUR 4.63, with historical data ~EUR 7.80, certified (beglaubigt) ~EUR 9.50; annual financial statements ~EUR 10.90. Data is not free.
- **Notes:** Austria is an outlier: NO free open government API and NO free bulk data. Everything per-document behind paid intermediaries. Direct-integration savings vs an aggregator are marginal — the state fee itself is per-extract; an aggregator here largely resells the same Verrechnungsstelle access. Euro amounts from the firmenbuchgrundbuch.at price list may drift.
- **Confidence:** high
- **Sources:** [e-Justice portal + firmenbuchgrundbuch.at (Verrechnungsstellen model, per-extract fees)](https://e-justice.europa.eu/topics/registers-business-insolvency-land/business-registers-eu-countries/at_en); [firmenbuchgrundbuch.at official query-service portal](https://www.firmenbuchgrundbuch.at/en)

### AU — ASIC Registers (Company / Organisation register)

**🟡 Direct, contract needed** — documents via API but access is contract/gated (negotiation needed)

- **Body:** Australian Securities and Investments Commission (ASIC). Note: business/company registers are being consolidated under the Australian Business Registry Services (ABRS), operated by the ATO.
- **Open API:** partial · No open public register API for extracts; programmatic access is via registered ASIC Information Brokers. (Free, separate: ABN Lookup web services on the ABR, and ASIC/ABR datasets on data.gov.au) · docs: <https://asic.gov.au/online-services/search-asics-registers/additional-searches/access-asic-data-through-a-broker/>
- **Delivers:** data, documents | documents via API: **yes**
- **Auth:** Via commercial Information Broker accounts (contract + broker credentials). ABN Lookup web services use a free registered GUID/API key but cover ABN/ABR data only, not ASIC company extracts or documents.
- **Cost (per_document):** Basic name/status search on ASIC Connect is free. Purchased products are PAID per item, prescribed and indexed annually (approx AUD, verify current schedule): current company/organisation extract ~A$19; current+historical extract ~A$38; relational extract ~A$57; copy of a lodged document (image) ~A$19 each; +A$3 mail/certification surcharge. Brokers add their own margin on top. Exact amounts not confirmed from a live fee table this session.
- **Notes:** No free open REST API delivering company extracts/documents. Real programmatic access = pay a registered ASIC Information Broker who resells searches, extracts and document images. Documents (filed PDFs / images) ARE obtainable but per-document paid. Free open data exists on data.gov.au (company dataset, business names dataset) but it is a limited snapshot, not documents. Exact fee figures should be re-verified against ASIC's current search product fee schedule (indexed each 1 July).
- **Confidence:** medium
- **Sources:** [ASIC 'Access ASIC data through a broker' — confirms broker-mediated programmatic access model](https://asic.gov.au/online-services/search-asics-registers/additional-searches/access-asic-data-through-a-broker/); [ASIC search fees page — confirms basic search free, extracts/document copies paid, structure present but exact $ shown as placeholders; +$3 certified-by-mail surcharge](https://asic.gov.au/online-services/search-asics-registers/search-fees/); [ASIC fees overview — confirms fees charged for some searches and $3 certified-document mail charge](https://asic.gov.au/for-business/payments-fees-and-invoices/asic-fees/)

### BE — Crossroads Bank for Enterprises — KBO / BCE

**🟠 Direct for DATA only — vendor for documents** — API delivers data but NOT documents — vendor still needed for filings

- **Body:** FPS Economy (FOD Economie / SPF Économie)
- **Open API:** partial · KBO Open Data (free bulk CSV via SFTP/download) + KBO Web Services (paid REST API) + CBE 'Public Search' web service · docs: <https://economie.fgov.be/en/themes/enterprises/crossroads-bank-enterprises/services-everyone/public-data-available-reuse/cbe-open-data>
- **Delivers:** data | documents via API: **no**
- **Auth:** Open Data: free registration + email verification (kbopub.economie.fgov.be/kbo-open-data). Web Services API: contract/subscription with FPS Economy.
- **Cost (free):** KBO Open Data is FREE after registration — full CSV extract refreshed monthly + monthly deltas, via download/SFTP. The programmatic 'KBO Web Services' REST API is PAID; pricing not published, quoted on request. Public Search web portal is free, no account.
- **Notes:** KBO/BCE holds STRUCTURED DATA ONLY (identification, address, legal form, NACE activity, status) — it does NOT hold filing documents. Company statuts/acts are published separately in the Belgian Official Gazette (Moniteur belge / Belgisch Staatsblad); annual accounts live at the National Bank of Belgium Central Balance Sheet Office (low per-document fee). A 'documents' integration in BE means wiring Staatsblad + NBB, not KBO. For data alone, the free monthly bulk Open Data is the cheapest direct route; the live REST API is paid and opaquely priced.
- **Confidence:** high
- **Sources:** [FPS Economy 'CBE - Open data' — free bulk data for reuse](https://economie.fgov.be/en/themes/enterprises/crossroads-bank-enterprises/services-everyone/public-data-available-reuse/cbe-open-data); [FPS Economy 'CBE Public Search' — free web consultation, no account](https://economie.fgov.be/en/themes/enterprises/crossroads-bank-enterprises/services-everyone/consultation-and-research-data/cbe-public-search); [KBO Open Data registration portal](https://kbopub.economie.fgov.be/kbo-open-data/login)

### BM — Companies and Partnerships Register (Catalyst online registry system)

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** Registrar of Companies (Government of Bermuda)
- **Open API:** no · Catalyst (online registry portal; no open developer API) · docs: <https://www.registrarofcompanies.gov.bm/>
- **Delivers:** data, documents | documents via API: **no**
- **Auth:** Registered portal account with identity verification (government-issued ID upload at registration); login-gated. No API keys/OAuth for third-party integration.
- **Cost (per_document):** Public name/entity search available to registered users; certificates (compliance/good standing) and document requests carry per-item statutory fees. 'Update Profile' is free; most transactional services fee-based. No bulk/API pricing published.
- **Notes:** Bermuda runs the 'Catalyst' online portal. Login-and-per-document model, not a data feed: registered users search the register and order certificates/documents individually. No open API found. Direct programmatic integration not offered; depend on manual portal use or an aggregation vendor.
- **Confidence:** high
- **Sources:** [Bermuda Registrar of Companies official portal (Catalyst) — registration/ID and search flow](https://www.registrarofcompanies.gov.bm/)

### BR — Registro Público de Empresas Mercantis — 27 state Juntas Comerciais (e.g. JUCESP, JUCERJA, JUCEMG)

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** State Juntas Comerciais, nationally coordinated by DREI (Ministério do Desenvolvimento, Indústria, Comércio e Serviços); CNPJ tax registry held separately by Receita Federal
- **Open API:** no · No unified national registry API. Each Junta runs its own portal for certidões/document copies (paid). Separately, Receita Federal publishes the full CNPJ base as FREE open data (bulk + community APIs like BrasilAPI/ReceitaWS) — structured data only. · docs: <https://dados.gov.br>
- **Delivers:** data, documents | documents via API: **no**
- **Auth:** Per-Junta portal login (usually gov.br account) + payment for certidões/document copies. CNPJ open data: no auth. No standardized registry document API.
- **Cost (per_document):** Junta certidão simplificada / ficha cadastral and document copies (contrato social, atos): paid per document, roughly BRL 30-90, varying by state. CNPJ open data (Receita Federal): free. No single price — fragmented across 27 states.
- **Notes:** Brazil is STATE-FRAGMENTED: 27 Juntas Comerciais, DREI only coordinates — no unified national registry API and no single document endpoint. Registry DOCUMENTS (contratos sociais, atos, certidões) come from each state Junta's own paid portal, one integration per state. For structured company DATA, the Receita Federal CNPJ open dataset (free, bulk/API) is the practical source, but it does NOT contain Junta filing documents. Direct integration for documents = 27 separate paid integrations; not practical vs an aggregator.
- **Confidence:** high
- **Sources:** [DREI coordinates 27 state-level Juntas Comerciais; no unified registry API; certidões referenced (fetched live this session)](https://www.gov.br/empresas-e-negocios/pt-br/drei); [Federal CNPJ structured data available as open data (free)](https://dados.gov.br)

### BS — Bahamas Companies Registry (Registrar General's Department)

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** Registrar General's Department (RGD), Office of the Attorney General / Ministry of Legal Affairs
- **Open API:** no
- **Delivers:** data | documents via API: **no**
- **Auth:** Portal accounts for filers/registered users; no public open API. Public company verification is limited and largely request/fee based.
- **Cost (per_document):** Company searches, certified extracts and certificates (certificate of good standing) charged per document/per request via the registry; amounts not verified this run. No free open bulk/public search comparable to Panama's consulta.
- **Notes:** Registrar General's Department handles companies (Companies Act) and IBCs (IBC Act). There is an online registry system for filing but NO documented open API and no robust free public search — verification/documents are per-document by request/fee, historically in person or via the portal. OpenCorporates openness 20/100. Primary gov.bs pages returned 403 / DNS not found from this environment, so details are from prior knowledge. No direct-integration API; documents per-document and gated — aggregation vendor likely still required.
- **Confidence:** low
- **Sources:** [OpenCorporates register listing: Bahamas Registrar General's Department, ~253k companies, no documented API, openness 20/100](https://opencorporates.com/registers); [Official government portal (attempted primary source; returned 403 / DNS blocked)](https://www.bahamas.gov.bs/)

### CA — Federal Corporation Search / Corporations Canada database

**🟠 Direct for DATA only — vendor for documents** — API delivers data but NOT documents — vendor still needed for filings

- **Body:** Corporations Canada (Innovation, Science and Economic Development Canada / ISED)
- **Open API:** yes · Corporations Canada API (Federal corporation data) · docs: <https://api.ised-isde.canada.ca/en/docs?api=corporations#?route=overview>
- **Delivers:** data | documents via API: **no**
- **Auth:** Open/public real-time API; no paid key required (public government data). Bulk open dataset also downloadable without auth.
- **Cost (free):** API and bulk open dataset both free of charge. Federal corporation search on the website is free. Note: obtaining certified copies of specific corporate documents is a separate paper/online request with fees and is NOT delivered via the API.
- **Notes:** FEDERAL ONLY. The free API/dataset covers CBCA/NFP/Coop etc. federal corporations and returns structured data (status, registered office, directors) — NOT filing PDFs or certified extracts. CRITICAL fragmentation: most Canadian companies are incorporated PROVINCIALLY (Ontario, BC, Quebec, Alberta, etc.), each with its own registry, access model, and largely PAID access — there is no single national registry. Direct integration solves federal only; provinces require separate integrations or an aggregator.
- **Confidence:** high
- **Sources:** [Corporations Canada Data services page: confirms free public API for real-time federal corporation data and free open dataset](https://ised-isde.canada.ca/site/corporations-canada/en/data-services); [Official API documentation portal](https://api.ised-isde.canada.ca/en/docs?api=corporations#?route=overview); [Federal open dataset on open.canada.ca](https://open.canada.ca/data/en/dataset/0032ce54-c5dd-4b66-99a0-320a7b5e99f2)

### CH — Handelsregister; national search via Zefix (Zentraler Firmenindex)

**🟠 Direct for DATA only — vendor for documents** — API delivers data but NOT documents — vendor still needed for filings

- **Body:** Zefix operated federally by the Federal Office of Justice (EHRA/OFRC); underlying registers maintained by the 26 cantonal commercial register offices
- **Open API:** yes · Zefix Public REST API (also Linked Data via LINDAS SPARQL) · docs: <https://www.zefix.admin.ch/ZefixPublicREST/>
- **Delivers:** data | documents via API: **no**
- **Auth:** None for basic name/UID queries (free, no key). Extended access can require an API key, but core lookups are open.
- **Cost (free):** Structured data (company master data, UID/VAT, SHAB/SOGC gazette publications) is free. Certified/official PDF Handelsregisterauszug extracts are NOT delivered by the API — ordered and paid per canton (typically ~CHF 20-50).
- **Notes:** Genuinely open data API. Catch: it gives structured register data and gazette notices, but NOT the certified PDF extract customers often need — those stay behind the cantonal offices and are paid. Direct integration replaces an aggregator for DATA cheaply, but not for certified documents.
- **Confidence:** high
- **Sources:** [Zefix Public REST API endpoint (JSON, no auth for basic queries)](https://www.zefix.admin.ch/ZefixPublicREST/); [opendata.swiss / i14y catalog listing of the Zefix REST dataservice](https://www.i14y.admin.ch/de/catalog/dataservices/6ef8f5d2-3d6a-4d84-bf60-5e65fde98a87)

### CN — National Enterprise Credit Information Publicity System (国家企业信用信息公示系统, GSXT)

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** State Administration for Market Regulation (SAMR); local AMR bureaus hold archive files
- **Open API:** no · None. GSXT is a free public web lookup only, protected by CAPTCHA/slider verification and IP throttling; no official developer API.
- **Delivers:** data | documents via API: **no**
- **Auth:** No account for public search, but human CAPTCHA / anti-bot verification and rate limiting block automation. Certified archive copies (企业档案) require in-person or authorized request at the local AMR office.
- **Cost (free):** GSXT web lookup of structured registration/credit data: free. Certified archive/register copies from local AMR: obtained offline, fees nominal and vary by locality; no online/API channel.
- **Notes:** GSXT delivers STRUCTURED data only (registration, shareholders, annual reports, penalties) and is deliberately anti-bot (CAPTCHA), so even the free data is not integrable via a supported API. Filing/register DOCUMENTS are not downloadable — certified 档案 copies are pulled in person at provincial/municipal AMR bureaus. Commercial providers (Tianyancha, Qichacha, QCC) scrape GSXT and resell via APIs; that is effectively the only programmatic path. Direct integration NOT viable.
- **Confidence:** high
- **Sources:** [GSXT is SAMR's free public disclosure portal, structured data, CAPTCHA-gated, no API (established knowledge; gsxt.gov.cn 521 to automated fetch this session)](https://www.gsxt.gov.cn)

### CY — Department of Registrar of Companies and Intellectual Property (DRCIP)

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** DRCIP (formerly DRCOR), Companies Section, under the Ministry of Energy, Commerce and Industry, Republic of Cyprus
- **Open API:** no
- **Delivers:** — | documents via API: **no**
- **Auth:** No developer API. eSearch basic search needs no login; the EUR 10 detailed search needs card payment. e-filing (documents/certified copies) requires a gov.cy government-gateway account plus a business authorisation code. Open-data bulk CSV on data.gov.cy needs no auth (CC BY 4.0).
- **Cost (per_document):** Basic company data FREE. Detailed historic search EUR 10.00/search. Certified copy/certificate EUR 20 each; certified Memorandum & Articles EUR 40; accelerated/express +EUR 20 per item. Open-data bulk CSV FREE. No subscription and no API pricing.
- **Notes:** DRCIP exposes NO developer/REST API. The eSearch/e-filing system is a web UI only (ASP.NET WebForms). Cyprus participates in EU BRIS via e-Justice, but that is a cross-border UI lookup, not a developer feed. The only machine-consumable channel is a MONTHLY BULK CSV on data.gov.cy (whole-file, not query-by-company; the CKAN datastore query API returned 404). Documents (certified PDFs) only through the e-filing web portal — no API delivers documents. Real-time per-company lookup or document retrieval means scraping the UI or self-hosting the bulk CSV.
- **Confidence:** medium
- **Sources:** [Official eSearch description; free vs EUR 10 detailed search; no API](https://www.companies.gov.cy/en/21-eservices/esearch-in-business-entity-s-registry); [Certified copies online: EUR 20 / EUR 40 M&A / +EUR 20 accelerated](https://www.companies.gov.cy/en/business-entities/2-company/5-lifecycle/1-running-a-company/5-guidance/obtaining-certified-copies-certificates/obtaining-certified-copies-certificates-online); [data.gov.cy DRCIP group — bulk open data, not a query API (CKAN action API 404)](https://data.gov.cy/en/group/30)

### CZ — Obchodní rejstřík (Commercial Register), part of the Veřejné rejstříky; aggregated for lookup via ARES

**🟠 Direct for DATA only — vendor for documents** — API delivers data but NOT documents — vendor still needed for filings

- **Body:** ARES run by the Ministry of Finance aggregates source registers; the commercial register itself is kept by the regional courts under the Ministry of Justice (justice.cz / or.justice.cz)
- **Open API:** yes · ARES REST API v3 (public); court register front-end at or.justice.cz · docs: <https://ares.gov.cz/swagger-ui/>
- **Delivers:** data | documents via API: **no**
- **Auth:** None / free for public queries, no registration (rate/volume limits apply). OpenAPI spec defines Basic/Bearer schemes, but public economic-subject endpoints are open.
- **Cost (free):** ARES REST API is free and returns JSON structured data (/ekonomicke-subjekty/{ico}, /ekonomicke-subjekty-vr/{ico} for the commercial-register view). No PDF/binary document endpoint exists in the ARES spec.
- **Notes:** ARES gives free structured commercial-register data via a clean REST API — strong candidate to replace an aggregator for DATA. Documents differ: the PDF výpis and sbírka listin (deeds/statutes/financials) are downloadable free from or.justice.cz, but that portal has no clean official REST API, so PDF retrieval needs scraping or the CzechPOINT ověřený výpis (paid, certified). Data via API = free & easy; documents via API = not officially available.
- **Confidence:** high
- **Sources:** [ARES OpenAPI spec (endpoint list; JSON-only, no PDF endpoints)](https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/v3/api-docs); [ARES portal + Ministry of Finance (free, no-registration public API)](https://ares.gov.cz/)

### DK — CVR — Det Centrale Virksomhedsregister (Central Business Register)

**🟢 Go direct (strong)** — open API delivers documents, free/low cost

- **Body:** Erhvervsstyrelsen (Danish Business Authority), Ministry of Industry, Business and Financial Affairs
- **Open API:** yes · CVR system-til-system adgang (Elasticsearch/REST distribution API) + Virk datahub bulk distribution · docs: <https://data.virk.dk/datakatalog/erhvervsstyrelsen/system-til-system-adgang-til-cvr-data>
- **Delivers:** data, documents | documents via API: **yes**
- **Auth:** Web portal and lookup: none. System-to-system Elasticsearch API: free registration required (request credentials from cvrselvbetjening@erst.dk). Annual reports downloadable without account.
- **Cost (free):** Fully free — the strongest open case. Structured company data (entities, P-units, owners, board, NACE/DB07, history) is free; annual reports (regnskaber) published free as PDF/XBRL and linked from each record. No per-search or per-document charge. Only cost is registering for the bulk/S2S feed.
- **Notes:** Best DIRECT-integration candidate. Both structured data AND financial-statement documents come free via official channels, so an aggregation vendor adds little beyond convenience. Articles of association (vedtægter) coverage is less complete than annual reports, but the accounts themselves are fully open.
- **Confidence:** high
- **Sources:** [Erhvervsstyrelsen CVR data catalog — system-to-system access page](https://data.virk.dk/datakatalog/erhvervsstyrelsen/system-til-system-adgang-til-cvr-data); [datacvr.virk.dk — download regnskaber (annual-reports)](https://datacvr.virk.dk/data/cvr-hj%C3%A6lp/f%C3%A5-hj%C3%A6lp-til-cvr/download-regnskaber)

### ES — Registro Mercantil (Central + provincial commercial registries)

**🟡 Direct, contract needed** — documents via API but access is contract/gated (negotiation needed)

- **Body:** Colegio de Registradores de la Propiedad, Mercantiles y de Bienes Muebles de España (CORPME)
- **Open API:** partial · CORPME 'servicios apificados' — automated (API-based) request channel for high-volume requesters; no public open API brand published · docs: <https://www.registradores.org/en/informacion-al-ciudadano/servicion-on-line>
- **Delivers:** data, documents | documents via API: **yes**
- **Auth:** Contract with CORPME + bespoke technical integration + electronic certificate/signature; offered only to entities planning very high daily request volumes. Not a self-service key.
- **Cost (per_document):** Per-document fees set by the statutory arancel. Nota simple informativa mercantil ~€6–9 + VAT; certificaciones, cuentas anuales and estatutos priced separately/higher. Exact amounts governed by the arancel registral, not disclosed on the API page.
- **Notes:** CORPME confirms 'apificado' API-based systems for automated requests, available to entities planning very high daily volumes, delivering DATA and DOCUMENTS (notas simples, certificaciones, cuentas anuales, estatutos). BUT no published developer portal, no public docs, no self-service onboarding — contract-based with custom technical work. 'partial': direct integration technically possible but requires a negotiated CORPME agreement. Some limited Open Data Registradores exists but is not a document channel.
- **Confidence:** medium
- **Sources:** [CORPME Servicios Online page ('apificado' systems for high-volume requesters)](https://www.registradores.org/en/informacion-al-ciudadano/servicion-on-line); [CORPME commercial registry sede](https://sede.registradores.org/site/mercantil?lang=en_EES); [CORPME description of Registro Mercantil Central](https://www.registradores.org/en/-/%C2%BFque-es-el-registro-mercantil-central-)

### FI — Kaupparekisteri (Trade Register), via the YTJ Business Information System

**🟠 Direct for DATA only — vendor for documents** — API delivers data but NOT documents — vendor still needed for filings

- **Body:** Patentti- ja rekisterihallitus / PRH (Finnish Patent and Registration Office), jointly operated with the Finnish Tax Administration (Vero)
- **Open API:** partial · PRH avoindata / opendata-ytj-api (YTJ open data), Registered Notifications API, Digital Financial Statements (XBRL) API · docs: <https://avoindata.prh.fi/en>
- **Delivers:** data | documents via API: **no**
- **Auth:** None — free open JSON, no API key, no login, no signup (attribution to PRH required).
- **Cost (per_document):** Open data (basic company details, registered notifications, digital financial statements filed in iXBRL) is FREE with no key. But this is DATA only — the open API does NOT deliver documents. Register extracts (kaupparekisteriote, ~EUR 35–50), articles of association (yhtiöjärjestys) and auditor's reports are sold as paid documents via PRH's Virre service.
- **Notes:** Free structured-data direct-integration is easy (no auth). But documents are portal/paid-only, and financial-statement data via API is limited to companies that filed in iXBRL — coverage gaps. If the use-case needs official PDF extracts or articles, direct = still paying PRH per document; an aggregator's value is mainly normalization/coverage, not cost avoidance.
- **Confidence:** high
- **Sources:** [PRH — Open data landing page (lists YTJ, notifications, XBRL APIs)](https://avoindata.prh.fi/en); [PRH — Trade Register page + document pricing (extract EUR 35–50, articles via Virre)](https://www.prh.fi/en/kaupparekisteri.html)

### FR — Registre National des Entreprises (RNE) — consolidates company registration data; the RCS remains the commercial-court register

**🟢 Go direct (strong)** — open API delivers documents, free/low cost

- **Body:** INPI operates the RNE and its open API. The RCS itself is kept by the greffes des tribunaux de commerce, consolidated commercially via Infogreffe.
- **Open API:** yes · INPI API Formalités / RNE (data.inpi.fr Open Data). Adjacent: DataInfogreffe open-data portal and the access-restricted 'API Entreprise' on api.gouv.fr (admin/authorized bodies only). · docs: <https://www.inpi.fr/ressources/formalites-dentreprises/acces-lapi-formalite-rne>
- **Delivers:** data, documents | documents via API: **yes**
- **Auth:** Free registration for technical identifiers via the INPI 'Espace Open Data' (credentials issued on request); no payment. REST/JSON + SFTP bulk.
- **Cost (free):** INPI RNE structured data (JSON, daily) and non-confidential DOCUMENTS are free/open: statuts and actes since 1993 (PDF) and comptes annuels/bilans since 2017 (only non-confidential accounts distributed). SEPARATE and PAID: the Kbis extract and certified/authentic documents only via Infogreffe/greffes at regulated tariffs (base digital doc ~EUR 3.20 as of 2025; tariffs set by decree). INPI does NOT issue the Kbis.
- **Notes:** Best direct-integration target of the four: one free, documented, open API (INPI RNE) delivers BOTH structured data and filing PDFs (statuts/actes/comptes) at zero marginal cost. Caveat: a certified Kbis or certified copy must come from Infogreffe (paid, per-document). API Entreprise on api.gouv.fr is richer but gated to public administrations — not open to a commercial vendor-replacement.
- **Confidence:** high
- **Sources:** [INPI 'Accès aux API - Entreprises' — RNE API delivers data + documents/comptes, only public documents distributed](https://data.inpi.fr/content/editorial/Acces_API_Entreprises); [INPI 'Accès à l'API formalité / RNE' developer page](https://www.inpi.fr/ressources/formalites-dentreprises/acces-lapi-formalite-rne); [Infogreffe tariffs — certified Kbis/actes/comptes paid at regulated greffe tariffs](https://www.infogreffe.fr/tarifs); [DataInfogreffe open-data portal (141 greffes)](https://www.infogreffe.fr/services/datainfogreffe)

### GB — Companies House

**🟢 Go direct (strong)** — open API delivers documents, free/low cost

- **Body:** UK executive agency of the Department for Business & Trade
- **Open API:** yes · Companies House Public Data API + Document API + Streaming API · docs: <https://developer.company-information.service.gov.uk>
- **Delivers:** data, documents | documents via API: **yes**
- **Auth:** free API key (register an application; HTTP Basic auth with the key as username). OAuth2 additionally available for filing/authenticated user actions.
- **Cost (free):** Public Data API (JSON company/officer/filing-history data) and Document API (filing images as PDF/TIFF) both free with no per-call charge. Rate-limited (~600 requests / 5 min). Bulk products also free.
- **Notes:** Strongest direct-integration candidate. Reference model: genuine open developer portal, both structured data AND downloadable document images via API, zero marginal cost. No reason to pay an aggregator for GB coverage.
- **Confidence:** high
- **Sources:** [official developer portal](https://developer.company-information.service.gov.uk); [official API specifications site](https://developer-specs.company-information.service.gov.uk)

### GG — The Guernsey Registry

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** States of Guernsey (arms-length statutory body under the Companies (Guernsey) Law)
- **Open API:** no
- **Delivers:** — | documents via API: **no**
- **Auth:** none (no API exists); basic web search free, no login; document purchase via portal checkout. Programmatic access would require a bespoke commercial arrangement with the Registry.
- **Cost (per_document):** Search free. Flat per-document fees (Dec 2025 schedule): electronic document GBP 15; certified electronic GBP 50; certified paper GBP 100. Entire company file GBP 100; companies-by-resident-agent report GBP 250; companies-at-registered-office report GBP 350. No subscription.
- **Notes:** No open/developer API, no portal, no bulk data. Access via the human-facing Online Services Portal (JS SPA). Free structured data covers only basic fields; shareholder register not held at registry level. Documents delivered only through the portal purchase flow — never via API. Direct integration not available off the shelf.
- **Confidence:** high
- **Sources:** [Company search guidance — free fields, portal-only, no API](https://www.guernseyregistry.com/Companysearches); [Limited Companies fee schedule — per-document GBP amounts](https://www.guernseyregistry.com/companyfees); [Online Services Portal — the only access channel (SPA)](https://portal.guernseyregistry.com/)

### HK — ICRIS e-Search Services (Cyber Search Centre) / e-Services Portal

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** Companies Registry, Government of the Hong Kong SAR
- **Open API:** no · none — web e-Services Portal (ICRIS) + Company Search Mobile Service app only; no third-party developer API
- **Delivers:** — | documents via API: **no**
- **Auth:** n/a for API. Portal: registered account or ad-hoc access; payment by prepaid Cyber Search Centre account, PPS or credit card.
- **Cost (per_document):** Chargeable per record/per document. e-Search charges a per-company particulars search fee and a separate per-document fee to view/download imaged copies of filed documents; certified copies cost more. Exact HKD amounts per the CR fee schedule (roughly single-digit-to-low-tens HKD per search/image; certified higher) — NOT confirmed from a fetched fee page.
- **Notes:** Portal (not an API) DOES deliver both data and imaged copies of filed documents (PDFs) for a per-item fee — good coverage, but only via manual/portal access. No open/developer API, so 'direct integration' means screen-scraping a paid portal (against ToS) — not a clean build. No viable direct API; aggregator or portal automation only.
- **Confidence:** medium
- **Sources:** [CR site nav confirms e-Services Portal + e-Search Services; no API surfaced](https://www.cr.gov.hk/en/home/index.htm); [e-Services Portal (ICRIS) — JS SPA, confirmed a login/portal not an API](https://www.e-services.cr.gov.hk/)

### IE — Companies Registration Office (CRO) / CORE

**🟢 Go direct (paid docs)** — open API delivers documents; per-document/subscription cost

- **Body:** Companies Registration Office, statutory office under the Department of Enterprise, Trade & Employment (DETE)
- **Open API:** yes · CRO Open Services (RESTful Web Services for CORE account holders) · docs: <https://services.cro.ie/account-holders-intro.aspx>
- **Delivers:** data, documents | documents via API: **yes**
- **Auth:** registration required — must be a registered CRO Customer/CORE account holder registered for Open Services; simple authenticated GET requests. Not an anonymous public key.
- **Cost (per_document):** API access itself not a subscription, but priced per item and billed to the CORE account. Document image = EUR 2.50 each; company printout = EUR 3.50 each — same tariff as manual CORE purchase. Basic company data also free via the separate CRO Open Data Portal (opendata.cro.ie), but that portal does NOT include document images.
- **Notes:** Good direct-integration candidate: Open Services REST API streams document images into your own application at the standard per-image CRO fee (no aggregator markup). Requires a CRO account. Verify current tariff.
- **Confidence:** high
- **Sources:** [official CRO developer/account-holder page](https://services.cro.ie/account-holders-intro.aspx); [official CRO access-to-data page](https://cro.ie/services-and-help/access-to-cro-data/); [official CRO fees leaflet No.4](https://cro.ie/wp-content/uploads/2024/04/Leaflet-4-v6.2.pdf)

### IL — Registrar of Companies (Rasham HaHavarot)

**🟠 Direct for DATA only — vendor for documents** — API delivers data but NOT documents — vendor still needed for filings

- **Body:** Israel Corporations Authority (Rashut HaTagidim), Ministry of Justice
- **Open API:** partial · data.gov.il CKAN datastore_search (open government dataset of registered companies); no official API on the Registrar's own paid-extract service · docs: <https://data.gov.il/dataset/ica_companies>
- **Delivers:** data | documents via API: **no**
- **Auth:** data.gov.il CKAN datastore_search: public/unauthenticated (optional API key for write; read is open). Registrar extract purchase: gov.il user + online payment, no API.
- **Cost (free):** Open dataset via data.gov.il is FREE and unauthenticated (~728,150 company records, ~28 structured fields: company number, name, type, status, incorporation date, address, last annual-report year, etc.). The official company extract (nesach mahshevi) — a formal certificate/document — is sold per-document through the Registrar/gov.il for a small statutory fee (order of ~NIS 10, exact amount not confirmed here), and is NOT available via an API.
- **Notes:** Best case of the four for DATA: a genuine open CKAN API (datastore_search) returns live structured registry data with no auth — usable directly, no aggregator needed for basic company data. BUT it delivers DATA ONLY; the official signed extract/document must be bought per-document on the Registrar site and there is no document API. If you only need structured company data, integrate data.gov.il directly; if you need the certified extract PDF, that stays manual/paid.
- **Confidence:** high
- **Sources:** [data.gov.il CKAN datastore_search returned JSON: ~728,150 company records, 28 fields, unauthenticated, with pagination](https://data.gov.il/dataset/ica_companies); [Registrar of Companies portal (Israel Corporations Authority) — search/extract service; host repeatedly reset connection during fetch; gov.il service pages return 403 to automated fetch, so extract fee not verified from primary page](https://ica.justice.gov.il)

### IM — Isle of Man Companies Registry

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** Central Registry, Isle of Man Government (Companies Registry division)
- **Open API:** no
- **Delivers:** data | documents via API: **no**
- **Auth:** n/a — no public developer API. Access via the web search portal at services.gov.im/companies-registry; programmatic/bulk access would require direct arrangement with the Registry.
- **Cost (per_document):** Basic online name/number search free and instant. Viewing/downloading document images and certified copies is paid per-document via portal/counter. Exact per-image online fee not confirmed from a primary page; certified documents via third parties run GBP 100+ (reseller pricing, not raw registry fee).
- **Notes:** No open API. Cannot integrate directly via a documented developer interface — web portal only (free basic search, paid documents). Automated retrieval would require scraping (fragile/ToS risk), a bespoke registry data feed, or an aggregator/CSP. Document-fee amount is the main open uncertainty.
- **Confidence:** medium
- **Sources:** [official IoM Government Companies Registry page](https://www.gov.im/categories/business-and-industries/companies-registry); [official IoM online services / company search](https://services.gov.im/companies-registry/)

### IN — Register of Companies / LLPs (MCA21)

**🟠 Direct for DATA only — vendor for documents** — API delivers data but NOT documents — vendor still needed for filings

- **Body:** Ministry of Corporate Affairs (MCA), Registrar of Companies (RoC)
- **Open API:** partial · No real-time company API on MCA21 itself; limited open bulk/master datasets via data.gov.in with API keys. 'View Public Documents' (VPD) and certified copies are paid, login-gated portal services (not APIs). · docs: <https://www.data.gov.in>
- **Delivers:** data, documents | documents via API: **no**
- **Auth:** data.gov.in: free API key. MCA21 VPD/certified copies: registered MCA21 login + per-transaction payment. No official document-delivery API.
- **Cost (per_document):** Company master data view on portal: free. 'View Public Documents' (filing PDFs): approx INR 100 per company for a time-limited viewing window. Certified copies: per-page statutory fee (roughly INR 5-25/page). data.gov.in open datasets: free.
- **Notes:** Structured master data is partly open (data.gov.in datasets, free API key) but is snapshot/bulk, not a live per-company lookup API. Filing DOCUMENTS come only through the paid, login-gated 'View Public Documents' / certified-copy flow on MCA21 V3 — NO API delivers them. Commercial aggregators wrap this manually. Direct integration gives open structured data but NOT documents.
- **Confidence:** high
- **Sources:** [MCA21 is the RoC portal; VPD/certified copies paid & login-gated (established knowledge; mca.gov.in 403 to automated fetch this session)](https://www.mca.gov.in); [Open MCA company/LLP datasets published with free API key](https://www.data.gov.in)

### IT — Registro delle Imprese

**🟢 Go direct (paid docs)** — open API delivers documents; per-document/subscription cost

- **Body:** Camere di Commercio; operated technically by InfoCamere S.C.p.A. under Unioncamere
- **Open API:** yes · InfoCamere Accesso alle Banche Dati Online (ABDO) API — companion to the Telemaco service · docs: <https://accessoallebanchedati.registroimprese.it/abdo/api>
- **Delivers:** data, documents | documents via API: **yes**
- **Auth:** Registration + contract: a Telemaco/InfoCamere account authenticated via SPID/CIE/CNS with a prepaid credit balance; institutional onboarding, not a free self-service key
- **Cost (per_document):** Pay-per-call against prepaid Telemaco credit; no mandatory annual subscription on the base tier (optional Web Telemaco subscription ~€250 + VAT). Light lookups from ~€0.68; a full visura camerale ordinaria ~€5–8; XBRL bilancio and atti/statuti priced separately per InfoCamere's Listino Telemaco.
- **Notes:** Strongest direct-integration candidate of the three. ABDO API exposes the same official data as Telemaco in structured JSON across Ricerca Anagrafica, Protesti, Visura Amministratori, Visure, Bilancio XBRL — both DATA and DOCUMENTS (visura/statuto/atti PDFs). Contract/credit-based, not free/open, but a genuine first-party channel, so an aggregator is avoidable. Verify per-visura tariffs against the current Listino Telemaco.
- **Confidence:** high
- **Sources:** [Official InfoCamere API service page (ABDO)](https://accessoallebanchedati.registroimprese.it/abdo/api); [Official Registro Imprese portal (InfoCamere)](https://www.registroimprese.it/infocamere); [Official InfoCamere Listino Prezzi Servizio Telemaco](https://registroimprese.infocamere.it/documents/20182/3303865/listino+telemaco/731e68a1-2e69-4ecc-a8d8-82e75deb5597)

### JE — JFSC Companies Registry (myRegistry)

**🟠 Direct for DATA only — vendor for documents** — API delivers data but NOT documents — vendor still needed for filings

- **Body:** Jersey Financial Services Commission (JFSC) — statutory financial regulator operating the Registry
- **Open API:** partial · JFSC Registry API (SOAP-based suite of services) · docs: <https://www.jerseyfsc.org/registry/application-programme-interface-registry/>
- **Delivers:** data | documents via API: **no**
- **Auth:** restricted — JFSC-issued API key plus a Digicert client signing certificate; access limited to registered nominated persons (Jersey trust companies / regulated service providers). Not open to arbitrary third-party developers.
- **Cost (free):** The API itself is free / no fees, but returns structured entity data and supports submissions (amend parties, file confirmation statements, check status) — it does NOT deliver filing document images. Public document/data purchase is via the myRegistry web portal, which charges per search/document.
- **Notes:** An API exists but is a regulated-industry filing/data interface, not an open documents API. Two blockers: (1) access restricted to nominated persons / regulated Jersey service providers, and (2) no document-image delivery. Direct integration for filing PDFs not feasible; only route is becoming/partnering with a regulated Jersey entity, and even then no doc images via API.
- **Confidence:** high
- **Sources:** [official JFSC API registry page](https://www.jerseyfsc.org/registry/application-programme-interface-registry/); [official JFSC Registry landing page](https://www.jerseyfsc.org/registry/)

### JP — Commercial and Corporate Register (商業・法人登記)

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** Legal Affairs Bureau (法務局) under the Ministry of Justice (法務省). Certificates issued by Legal Affairs Bureaus; online delivery via MOJ-affiliated services.
- **Open API:** no · No open developer REST API for the commercial register. Online access channels: Registration Information Provision Service (登記情報提供サービス, touki.or.jp) for viewing register info; Touki-Kyoutaku Online (touki-kyoutaku-online.moj.go.jp) for requesting certified extracts, via browser or dedicated software (not a public REST API). Separate FREE open APIs exist for basic corporate identity only (National Tax Agency Corporate Number System API; METI gBizINFO). · docs: <https://www1.touki.or.jp/>
- **Delivers:** data, documents | documents via API: **no**
- **Auth:** Registration Information Provision Service: registered individual/corporate account (or one-day credit-card temporary use). Touki-Kyoutaku Online: applicant registration (annual renewal); dedicated software for programmatic-style use. No open token/API-key developer model for the register itself.
- **Cost (per_document):** PAID per record. Registration Information Provision Service commercial/corporate full record (全部事項) ~331 yen per record (non-certified, no legal proof force). Certified register extract (登記事項証明書) from Legal Affairs Bureau: ~600 yen at counter, ~500 yen via online request + mail, ~480 yen online request + counter pickup. Amounts from prior knowledge — re-verify against current MOJ/touki.or.jp fee schedule.
- **Notes:** Hardest to integrate directly. There is NO free/open REST API delivering commercial-register documents. The touki-kyoutaku-online system is a filing/certificate-request portal (browser or MOJ-supplied dedicated software), not a modern API. Documents (certified extracts) are obtainable but paid per item and not via a clean developer API. For lightweight structured data (corporate number, legal name, address) the National Tax Agency Corporate Number API and METI gBizINFO are FREE and open — but they do NOT provide register extracts, directors, or filing documents. For document-grade register data at scale in JP, an aggregator/local agent is likely more practical than direct integration.
- **Confidence:** medium
- **Sources:** [MOJ Touki-Kyoutaku Online — online commercial/corporate registration filing and certificate requests; browser or dedicated software; developer section exists but no open API spec](https://www.touki-kyoutaku-online.moj.go.jp/); [Registration Information Provision Service — online viewing of register records, account/temporary-use models, credit-card payment (paid, non-certified)](https://www1.touki.or.jp/); [Fee amounts (331 yen online record; ~500-600 yen certified extract) from prior knowledge of MOJ/touki.or.jp schedules — not confirmed from a live fee page this session](https://www.touki.or.jp/)

### KR — Commercial (Corporate) Registry — 법인등기 / 등기사항증명서

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** Supreme Court of Korea, Court Registry Offices; online via IROS (Internet Registry Office)
- **Open API:** no · None for the registry itself (IROS is login/payment-gated). Separate 등기정보광장 / data.iros.go.kr offers only aggregate statistics, not per-company extracts. · docs: <https://data.iros.go.kr>
- **Delivers:** documents | documents via API: **no**
- **Auth:** Real-name login + Korean auth (공동/금융인증서 or mobile ID) and per-transaction payment; effectively closed to non-Korean automated clients. No developer API keys.
- **Cost (per_document):** Certified corporate register extract (등기사항증명서): online view approx KRW 700, issuance approx KRW 1,000 per document; paid online. Not billed via any API.
- **Notes:** Corporate registration in Korea is a JUDICIAL function run by court registry offices; IROS is the online front-end and issues certified register PDFs per document, but there is NO open/developer API and access is real-name + payment gated. Direct programmatic integration not feasible. NOTE: DART (opendart.fss.or.kr, Financial Supervisory Service) DOES offer a genuine free OpenAPI for corporate DISCLOSURE filings of listed/large firms — filings, not the registry extract — worth considering for that subset.
- **Confidence:** medium
- **Sources:** [IROS is the Supreme Court online registry issuing certified register copies per document; login/payment-gated, no open API (established knowledge; live fetch 404/403 this session)](https://www.iros.go.kr); [Registry statistics portal (data only, not per-company extracts)](https://data.iros.go.kr)

### KY — CORIS (Cayman Online Registry Information System) / General Registry

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** General Registry, Cayman Islands Government (Registrar of Companies)
- **Open API:** no · none — CORIS portal (registered-user search) + CAP / Cayman Business Portal; no public API
- **Delivers:** — | documents via API: **no**
- **Auth:** n/a — CORIS requires a registered government-portal user account even to search; corporate filings done via registered agents through CAP/CBP.
- **Cost (per_search):** Company search is registration-gated (registered CORIS user account) and returns only limited public fields (name, type, status, registration date, registered office). Certificate of Good Standing / certified extracts orderable for a fee (~KYD/US low tens-hundreds; e.g. good standing ~KYD 50) — amounts NOT confirmed; the fetched fees page exposed only new-registration capital-based fees (CI$700-3,268).
- **Notes:** Weakest for direct integration: portal-only, account-gated, minimal public data, and Cayman filings (directors, M&A) and beneficial ownership are NOT public (explicit Beneficial Ownership Access Restriction). No API, no downloadable public documents. Direct registry integration effectively impossible; substantive data via the registered agent or a specialist vendor.
- **Confidence:** low
- **Sources:** [ciregistry.ky homepage — search requires registered login via CORIS; Beneficial Ownership Access Restriction; no API](https://www.ciregistry.ky/); [Fees page — Companies Act 2025 registration (capital-based) fees only, not search/document fees](https://www.ciregistry.ky/fees/)

### LI — Handelsregister des Fürstentums Liechtenstein (Commercial Register), public front-end 'Firmenindex'

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** Amt für Justiz (Office of Justice), Handelsregister division, Vaduz
- **Open API:** no
- **Delivers:** — | documents via API: **no**
- **Auth:** No API. Free partial extract needs no registration (session cookie only). Paid extracts/copies billed by invoice in CHF (in advance or within 30 days).
- **Cost (per_document):** Per fee ordinance GbHr-GebV (LR 214.011, Anhang 2): electronic uncertified extract CHF 10; electronic certified CHF 15; certified paper CHF 15 (min CHF 20 if posted). File inspection (gate to Statuten/Belege) CHF 50/file; copies CHF 1/page; certified transcript copies CHF 4/page. No subscription/bulk model.
- **Notes:** No open developer API. The portal is a server-rendered JSF/XHTML app — no /api, no OpenAPI/Swagger; root returned HTTP 403 to automated fetching. Liechtenstein IS an EEA participant in EU BRIS, so LI companies are searchable via the e-Justice UI — but BRIS is a UI/interconnection, NOT a developer API. Free partial extract is on-screen data; certified full Handelsregisterauszug is a paid document; filing images (Statuten/Belege) via per-file inspection — none exposed via API. Per-extract cost is trivial (CHF 10-15); the blocker is the total absence of a machine channel. For automation, an aggregator remains the pragmatic path.
- **Confidence:** high
- **Sources:** [Registry portal — free partial + paid certified extract, JSF app, no API](https://handelsregister.li/cr-portal/suche/suche.xhtml); [Official fee ordinance GbHr-GebV LR 214.011 Anhang 2 — CHF fee amounts](https://www.gesetze.li/konso/pdf/2003067000?version=6); [Liechtenstein participates in BRIS via EEA; register run by Amt für Justiz](https://www.llv.li/en/national-administration/office-of-justice/commercial-register-hr-)

### LU — Registre de Commerce et des Sociétés (RCS)

**🟠 Direct for DATA only — vendor for documents** — API delivers data but NOT documents — vendor still needed for filings

- **Body:** Luxembourg Business Registers (LBR) — a GIE under State supervision (Ministry of Justice + Chamber of Commerce + Chambre des Métiers). LBR also runs the RESA gazette and the RBE beneficial-owners register.
- **Open API:** partial · LBR B2B API for the private sector (electronic RCS services; launched Oct 2022, distributed e.g. via i-Hub) + open datasets on data.public.lu. No confirmed free high-volume public-search API. · docs: <https://www.lbr.lu>
- **Delivers:** data, documents | documents via API: **no**
- **Auth:** Portal (lbr.lu): free user account. B2B API: contract/registration with LBR. Open-data portal: no auth.
- **Cost (per_document):** On lbr.lu, searching by name/RCS number and downloading FILED documents (articles, annual accounts, board resolutions PDFs) is free with an account; only the certified 'Extrait RCS' (digitally signed) carries a fee (order of ~EUR 5–13). The LBR B2B API is a contractual/commercial service — pricing not public. Some datasets on data.public.lu are free (open licences).
- **Notes:** LOWEST confidence of the four on API specifics. Primary sources confirm the free-portal + paid-certified-extract model and a contractual B2B API; but the widely-cited 'open, no-auth REST/XML company-search API' claims come from aggregator/marketing sites (zephira, topograph, kyckr), NOT an LBR developer portal — treat as unproven. Realistic direct path: contractual LBR B2B API, or scrape the free portal, or data.public.lu open datasets for bulk. Documents are cheap/free but access is portal/account-gated rather than cleanly API-delivered.
- **Confidence:** medium
- **Sources:** [LBR press item — LBR API for the private sector (i-Hub)](https://www.i-hub.com/b2b/wp-content/uploads/sites/3/2022/10/LBR-API-i-Hub-PR-October-2022-EN.pdf); [Luxembourg national open-data portal (LBR/RCS datasets)](https://data.public.lu); [Guichet.lu — RCS filings/publications and extract ordering via LBR](https://guichet.public.lu/en/entreprises/creation-developpement/constitution/entreprise-individuelle/immatriculation-entreprise-publication-rcs.html); [European e-Justice Portal — LU business register overview](https://e-justice.europa.eu/topics/registers-business-insolvency-land/business-registers-eu-countries/lu_en)

### MT — Malta Business Registry

**🟠 Direct for DATA only — vendor for documents** — API delivers data but NOT documents — vendor still needed for filings

- **Body:** Malta Business Registry (MBR) — autonomous government agency under the Ministry for the Economy; statutory Registrar of Companies
- **Open API:** partial · MBR API packages (Company Search API, Basic Company Details, Full Company Details, Bundle API)
- **Delivers:** data | documents via API: **no**
- **Auth:** Application/registration-gated, restricted to AML/CFT-regulated 'Subject Persons'. No public developer portal, no self-serve key, no published spec. Onboarding by email; machine-to-machine access on approval. Portal search (non-API) needs a free registered account since 1 Aug 2025.
- **Cost (subscription):** API pricing NOT published — handled via email onboarding (treat as must-ask-MBR; low confidence). Portal search free (registered account). Documents (portal/email, per-document, secondary sources): certificate of good standing ~EUR 5-10, company extract ~EUR 10-20, certified M&A ~EUR 10-15, UBO extract ~EUR 10-25 — NOT confirmed on MBR's own fee pages, which publish only incorporation fees EUR 100-1,900.
- **Notes:** Real but CLOSED API, launched ~March 2026, restricted to Subject Persons — not open. Returns structured DATA only: Full Company Details includes a list of filings as METADATA (title/type/date), NOT the images/PDFs. Document images/certified copies via the registry portal with card payment or email — no API path for documents. Malta participates in EU BRIS but BRIS is a UI/interconnection, not a developer API. Direct integration can replace an aggregator for DATA only, contingent on Subject-Person onboarding; does not cover document retrieval.
- **Confidence:** medium
- **Sources:** [MBR API packages, payloads, 'Subject Persons' restriction](https://www.mbr.mt/post/malta-business-registry-to-offer-apis-to-subject-persons); [API packages launched (four packages), March 2026](https://thebusinesspicture.com/2026/03/04/malta-business-registry-launches-application-programming-interface-packages/); [EU e-Justice Malta page (free basic search, paid documents, BRIS not an API)](https://e-justice.europa.eu/topics/registers-business-insolvency-land/business-registers-eu-countries/mt_en)

### MU — CBRIS (Companies and Businesses Registration Integrated System) / online company search

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** Corporate and Business Registration Department (CBRD), Ministry of Finance — system operated via Mauritius Network Services (MNS)
- **Open API:** no · CBRIS (MNS-operated e-services + free public search at onlinesearch.mns.global); no documented open developer API · docs: <https://cbris.mns.global/>
- **Delivers:** data, documents | documents via API: **no**
- **Auth:** Free public search is unauthenticated; e-filing and document ordering require an MNS/CBRIS login. No public API keys documented.
- **Cost (free):** Company/partnership/business and name-availability search is free at onlinesearch.mns.global (structured data: name, number, status, type). Filed documents and certificates are ordered for per-document fees via CBRIS (CBRD 'Fees Payable to the Registrar').
- **Notes:** Mauritius is the most open of the four for DATA: a genuinely free public online search returning structured company data, plus the CBRIS e-services platform run by Mauritius Network Services. Documents/certificates are login-gated and per-document. No open/documented REST API for third-party integration found — web-portal only. MNS is a commercial operator, so a data-sharing arrangement might be negotiable, but no self-serve public API today.
- **Confidence:** medium
- **Sources:** [CBRD official site (companies.govmu.org) — links to free search and CBRIS login](https://companies.govmu.org/); [CBRIS / MNS online system and free public search](https://cbris.mns.global/)

### MX — Registro Público de Comercio (RPC) — SIGER 2.0

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** Secretaría de Economía, operated jointly with state governments; publications via PSM (Sistema Electrónico de Publicaciones de Sociedades Mercantiles)
- **Open API:** no · None (public web consulta + SIGER 2.0 login portal + PSM publications portal)
- **Delivers:** data, documents | documents via API: **no**
- **Auth:** Public consulta: none. SIGER 2.0 transactional portal: login-gated (credentials/e.firma, for notaries/fedatarios/authorized users). PSM: e.firma/registration to publish, public to consult.
- **Cost (per_document):** Online consulta of registration data is free; PSM publications are free to consult. Certified extracts/certifications (certificaciones, boletas registrales) are charged per document under the state/federal fee schedule (Ley Federal/Estatal de Derechos), typically obtained at the local RPC office, not via any API. No API pricing because there is no API.
- **Notes:** RPC is the mercantile registry; SIGER 2.0 is the electronic operating platform (rpc.economia.gob.mx/siger2/ redirects to a login) and is NOT open — it serves notaries/authorized filers. A public 'consulta' returns structured data only. PSM (psm.economia.gob.mx) hosts mandatory company publications (share registrations, dissolutions/liquidations) as documents you can query, but again no programmatic API. Direct integration is NOT viable without a private arrangement; an aggregator or screen-level integration would be required.
- **Confidence:** medium
- **Sources:** [rpc.economia.gob.mx homepage (portal reachable but resource error at fetch time; identifies Secretaría de Economía internal services)](https://rpc.economia.gob.mx); [SIGER 2.0 portal 302-redirects to login.xhtml — login-gated, not open](https://rpc.economia.gob.mx/siger2/); [PSM portal — publishes mercantile company notices (share registrations, dissolutions/liquidations); has 'Consulta publicaciones'; no API mentioned; registration by e-credential to publish](https://psm.economia.gob.mx)

### NL — Handelsregister (Netherlands Commercial / Business Register)

**🟠 Direct for DATA only — vendor for documents** — API delivers data but NOT documents — vendor still needed for filings

- **Body:** KVK — Kamer van Koophandel (Netherlands Chamber of Commerce)
- **Open API:** yes · KVK API suite — Zoeken (Search), Basisprofiel, Vestigingsprofiel, Naamgeving · docs: <https://developers.kvk.nl>
- **Delivers:** data | documents via API: **no**
- **Auth:** Free registration for an API key; free test/sandbox; production requires a paid subscription tied to the key.
- **Cost (per_search):** Monthly fee EUR 6.40 per API key (connection) + EUR 0.02 per query for profile calls (Basisprofiel, etc.); the Zoeken/Search API is free per query after the base fee. Up to 300,000 queries/month, 100/sec. VAT-exempt. The official extract (Uittreksel) PDF is a SEPARATE product at EUR 14.95 per download — not delivered by the standard data APIs.
- **Notes:** KVK API = clean, well-documented STRUCTURED DATA (KVK number, address, legal form, directors/officers, SBI codes) at low per-query cost — strong direct-integration candidate for data. But DOCUMENTS are the gap: the standard APIs do NOT return the official Uittreksel or deposited annual accounts; the digital Uittreksel is ordered separately at EUR 14.95, and there is no fully-open bulk register (Dutch law restricts open re-publication of KVK data). NL gives cheap data-by-API but document retrieval stays a paid, order-based side channel.
- **Confidence:** high
- **Sources:** [KVK Developer Portal pricing — EUR 6.40/month per key + EUR 0.02/query, Search free, VAT-exempt](https://developers.kvk.nl/pricing); [KVK Developer Portal API documentation](https://developers.kvk.nl/documentation); [KVK ordering products / API + official Uittreksel EUR 14.95 separate](https://www.kvk.nl/en/ordering-products/kvk-api/)

### NO — Enhetsregisteret + Foretaksregisteret (Register of Business Enterprises); financials in Regnskapsregisteret

**🟢 Go direct (paid docs)** — open API delivers documents; per-document/subscription cost

- **Body:** Brønnøysundregistrene (The Brønnøysund Register Centre)
- **Open API:** yes · data.brreg.no open-data APIs (Enhetsregisteret, roles, signature/procuration, beneficial owners, Regnskapsregisteret key-figures API) · docs: <https://data.brreg.no/enhetsregisteret/api/dokumentasjon/en/index.html>
- **Delivers:** data, documents | documents via API: **yes**
- **Auth:** None for open data — Norwegian Licence for Open Government Data (NLOD), no registration. The 'closed' full-accounts feed is restricted to public authorities.
- **Cost (per_document):** Structured data is FREE and fully open. Annual-accounts API: OPEN part (key figures from the latest annual report) free to all; CLOSED part (near-full figures, last three years incl. group accounts) for public authorities only. Full annual-report PDF image copies, plus firmaattest and vedtekter, are FEE-BASED per document via BRREG's ordering service — not via the free open API.
- **Notes:** Excellent for structured-data direct-integration (free, no key, high quality). But if you need actual PDF documents (full accounts image, certificates, articles), those still cost per document from BRREG — an aggregator wouldn't be cheaper than BRREG's own fee, but direct is entirely feasible.
- **Confidence:** high
- **Sources:** [Brønnøysundregistrene — Datasets and API (lists APIs + NLOD, no registration)](https://www.brreg.no/en/use-of-data-from-the-bronnoysund-register-centre/datasets-and-api/); [data.norge.no — Regnskapsregisteret dataset (free key figures vs fee-based full report image)](https://data.norge.no/en/datasets/7c87f169-2520-4e56-ba2a-b7a3cc7de2e9/regnskapsregisteret)

### NZ — New Zealand Companies Register

**🟠 Direct for DATA only — vendor for documents** — API delivers data but NOT documents — vendor still needed for filings

- **Body:** Companies Office (part of the Ministry of Business, Innovation and Employment — MBIE)
- **Open API:** yes · Companies Register API (via MBIE api.business.govt.nz), plus NZBN Register API · docs: <https://api.business.govt.nz/api/explore-apis/by-category?tag=Companies-group>
- **Delivers:** data | documents via API: **no**
- **Auth:** Developer registration on api.business.govt.nz; OAuth2 for the NZBN API. Free to connect.
- **Cost (free):** Public register search is FREE. NZBN API explicitly free to connect and use. Bulk data (monthly CSV snapshots) free once access is granted. Companies Register API access is free. No per-search or per-document charge for the online register.
- **Notes:** Most open of the four. Free public register, free bulk CSV, free APIs. IMPORTANT nuance: the public web register lets anyone VIEW/DOWNLOAD filed documents (constitutions, annual returns, financial statements) free — but whether the Companies Register API itself returns those document PDFs (vs. only structured company data + directors/shareholders) is NOT confirmed; APIs appear to serve structured data. Documents likely require the public register front-end / document endpoints rather than the data API. Register-owned data — no aggregation vendor needed for NZ.
- **Confidence:** medium
- **Sources:** [Companies Office 'ways to get our data' — free register search, free bulk CSV, APIs for Companies/NZBN/Disclose/PPSR](https://www.companiesoffice.govt.nz/data-services/ways-to-get-our-data); [NZBN API page — 'free to connect to and use', OAuth2, register-backed](https://www.nzbn.govt.nz/using-the-nzbn/nzbn-services/api/); [MBIE API portal — Companies group API catalogue](https://api.business.govt.nz/api/explore-apis/by-category?tag=Companies-group)

### PA — Registro Público de Panamá — Consulta de Persona Jurídica (servicios en línea)

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** Registro Público de Panamá (RPP), autonomous state entity
- **Open API:** no
- **Delivers:** data | documents via API: **no**
- **Auth:** None — free public web-form 'consulta' (no login); paid certified certificates require an account/payment, still no API.
- **Cost (free):** Basic public entity search (name/ficha/folio) is free and returns structured data (agent, directors, capital, status). Certified certificates (Certificado de Persona Jurídica / existencia) are purchasable online for a per-document fee, exact amount unconfirmed (historically ~USD 25-35; NOT verified this run).
- **Notes:** Free online consulta exists and is scrapeable for DATA only — no documented open API, no developer portal. Filing 'documents' in Panama are notarial escrituras; the registry sells certified certificates via the web portal, not via any API. Primary site rp.gob.pa was geo-blocked/connection-refused from this environment, so specifics (esp. cost, document flow) are from prior knowledge, not freshly verified. Direct data integration only feasible by scraping the public consulta.
- **Confidence:** low
- **Sources:** [OpenCorporates register listing corroborates a public online register for Panama (~945k companies) with no documented API](https://opencorporates.com/registers); [Official registry site (attempted primary source; unreachable/geo-blocked — connection refused)](https://www.rp.gob.pa/)

### PL — Krajowy Rejestr Sądowy (KRS) — National Court Register (register of entrepreneurs)

**🟢 Go direct (strong)** — open API delivers documents, free/low cost

- **Body:** Ministry of Justice, maintained by the registration courts; served via the Portal Rejestrów Sądowych (PRS)
- **Open API:** yes · API Krajowego Rejestru Sądowego (Open API KRS) · docs: <https://prs.ms.gov.pl/krs/openApi>
- **Delivers:** data, documents | documents via API: **yes**
- **Auth:** None for the Open API (free, no key). A separate 'Full API' exposing personal data (names/PESEL) requires a ministerial decision and is limited to legally specified entities.
- **Cost (free):** Free. The Open API returns an odpis aktualny/pełny corresponding to the official Central Information copy, in BOTH JSON and PDF. Base: https://api-krs.ms.gov.pl — e.g. /api/krs/OdpisAktualny/{krs}?rejestr=P&format=json (or format=pdf).
- **Notes:** Standout for direct integration: PL delivers the actual PDF odpis (current and full) for FREE via the government Open API, plus JSON — exactly what an aggregator resells. Only limitation: the free Open API anonymizes sensitive personal data (representatives' names/PESEL); the personal-data 'Full API' needs a ministerial grant. Statutes/deeds beyond the odpis are a separate document repository. Beware third parties (MGBI, nip24, rejestr.io) marketing paid 'KRS API' PDFs — the official api-krs.ms.gov.pl is free.
- **Confidence:** high
- **Sources:** [Ministry of Justice announcement of the KRS Open API + PRS OpenAPI page (JSON+PDF, free; Full API needs ministerial decision)](https://www.gov.pl/web/sprawiedliwosc/uruchomienie-otwartego-api-krajowego-rejestru-sadowego); [PRS Open API documentation portal + api-krs.ms.gov.pl base endpoint (odpis in PDF/JSON)](https://prs.ms.gov.pl/krs/openApi)

### PT — Registo Comercial — Certidão Permanente de Registo Comercial

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** Instituto dos Registos e do Notariado (IRN, I.P.), via the Plataforma de Serviços do Registo
- **Open API:** no
- **Delivers:** documents | documents via API: **no**
- **Auth:** Web portal only: online request (Cartão de Cidadão / Chave Móvel Digital or anonymous); consultation via a 12-digit access code with no authentication. No API auth exists.
- **Cost (per_document):** Fixed price per certificate by validity (official IRN tariff): Commercial Registration Certificate €25 (1yr)/€40 (2yr)/€60 (3yr)/€70 (4yr); Registration + Documents €55/€88/€132/€154; Memorandum/Articles (estatutos) €20/€35/€45/€50. Online consultation free once purchased, during validity.
- **Notes:** No direct API. The Certidão Permanente is a web product: pay per certificate, receive an access code granting online consultation for the paid validity window (1–4 years) — economically a subscription-per-entity. Delivers DOCUMENTS (certidão, estatutos, IES accounts) but NO programmatic channel, so scraping the code-access page is the only DIY route (fragile, likely against terms). The jurisdiction where an aggregation vendor is hardest to avoid. The access-code model does make re-fetching a known entity cheap within its validity window.
- **Confidence:** high
- **Sources:** [IRN permanent-certificate request page (types + per-validity pricing)](https://registo.justica.gov.pt/en/Companies/Request-permanent-certificate); [IRN Consultar Certidão Permanente page (access-code model; no API)](https://registo.justica.gov.pt/Empresas/Consultar-Certidao-Permanente); [gov.pt service page for the certidão permanente](https://www.gov.pt/servicos/consultar-a-certidao-permanente-de-registo-comercial)

### SC — Seychelles FSA — Registrar of International Business Companies / Registry of Companies

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** Financial Services Authority (FSA) of Seychelles, acting as Registrar (IBC Act 2016 and related)
- **Open API:** no · Struck-Off IBC Search (public web tool, not an API) · docs: <https://ibcsearch.fsaseychelles.sc/>
- **Delivers:** data | documents via API: **no**
- **Auth:** Public struck-off IBC search is open/free (no login) but limited to struck-off entities; full IBC register access is agent-gated — company info and documents obtained through the licensed registered agent, not by public API.
- **Cost (free):** The only public tool (struck-off IBC search) is free and returns limited DATA. Active-company data, certificates of good standing and extracts are obtained via a registered agent for a fee (agent/FSA fees; amounts not verified). No open API, no public documents.
- **Notes:** Confirmed from FSA site: the only public search is the 'Struck-Off IBC Search' — struck-off entities only, data not documents, web form (no API). No public register of active IBC directors/officers/documents; the IBC registry is agent-gated by design (registered agents hold and file records). FSA maintains registers of LICENSED entities but not a public searchable company register. OpenCorporates openness 10/100. Direct integration effectively impossible without registered-agent access; no official API and no documents via API.
- **Confidence:** medium
- **Sources:** [FSA Seychelles website: only public search is the Struck-Off IBC Search; no public IBC register search or API](https://fsaseychelles.sc/); [FSA public Struck-Off IBC Search tool](https://ibcsearch.fsaseychelles.sc/); [OpenCorporates register listing: Seychelles Business Register, no documented API, openness 10/100](https://opencorporates.com/registers)

### SE — Bolagsregistret / Näringslivsregistret (companies register)

**🟡 Direct, contract needed** — documents via API but access is contract/gated (negotiation needed)

- **Body:** Bolagsverket (Swedish Companies Registration Office)
- **Open API:** partial · Two tracks: (1) paid 'API för att hämta företagsinformation' (WSO2 developer portal); (2) free 'API för värdefulla datamängder' (EU Open Data Directive valuable datasets) · docs: <https://bolagsverket.se/apierochoppnadata.2531.html>
- **Delivers:** data, documents | documents via API: **yes**
- **Auth:** Paid company-info API: signed agreement with Bolagsverket + OAuth client_id/client_secret (test env first). Free valuable-datasets API: no contract, open access.
- **Cost (subscription):** The main company-information API is PAID: one-time connection fee plus a monthly fee scaled to a transaction tier (each query = one transaction; change-notification push included free at the 3,000+ transactions/month tier). It can return the list of documents linked to a company and retrieve them (documents generally chargeable). Exact SEK amounts not published in reviewed pages — MUST confirm the fee schedule with Bolagsverket. A separate FREE but limited 'valuable datasets' API exists (no contract).
- **Notes:** The Nordic OUTLIER — Sweden is NOT open like DK/NO/FI. Rich data/documents require a contract, OAuth and a paid subscription. The free 'valuable datasets' API is limited structured data only. This is where a direct integration is the most work (legal agreement + OAuth) and an aggregation vendor's value is strongest. Verify exact SEK connection/monthly fees before deciding.
- **Confidence:** medium
- **Sources:** [Bolagsverket — API to retrieve company information (agreement + OAuth + connection fee + tiered monthly fee)](https://bolagsverket.se/apierochoppnadata/hamtaforetagsinformation/apiforatthamtaforetagsinformation.3988.html); [Bolagsverket — APIs and open data hub, incl. free 'valuable datasets' API](https://bolagsverket.se/apierochoppnadata.2531.html)

### SG — BizFile+ (ACRA register) / ACRA API Marketplace

**🟠 Direct for DATA only — vendor for documents** — API delivers data but NOT documents — vendor still needed for filings

- **Body:** Accounting and Corporate Regulatory Authority (ACRA)
- **Open API:** yes · ACRA API Marketplace (delivered via the Singapore Government API Exchange / APEX) · docs: <https://www.acra.gov.sg/how-to-guides/buying-information/acra-api-marketplace>
- **Delivers:** data | documents via API: **no**
- **Auth:** Portal: Singpass/Corppass login. API: onboard a registered application via APEX with API key/OAuth (commercial agreement).
- **Cost (per_document):** Free basic entity search on BizFile+. Paid products via BizFile or authorized providers: Business Profile ~S$5.50; certificates/extracts ~S$16.50 (ACRA standard pricing but NOT confirmed from a fetched price page). API access is commercial/per-transaction via APEX.
- **Notes:** Best of the four hubs for direct integration: ACRA explicitly runs an API Marketplace and info products are downloadable. BUT the APIs chiefly return STRUCTURED DATA; the actual documents (Business Profile PDF, extracts) are bought through the BizFile portal purchase flow — document-via-API is unconfirmed and likely not first-class. Treat data-via-API as real, documents-via-API as uncertain; confirm a document-retrieval API with ACRA before dropping a vendor for filings.
- **Confidence:** medium
- **Sources:** [ACRA 'buying information' page confirms an ACRA API Marketplace and downloadable information products](https://www.acra.gov.sg/how-to-guides/buying-information); [ACRA info-products overview (buy/download/verify flow)](https://www.acra.gov.sg/how-to-guides/buying-information/information-products)

### TR — Ticaret Sicili (Trade Registry) + MERSIS + Türkiye Ticaret Sicili Gazetesi (Trade Registry Gazette)

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** Trade Registry Directorates under local chambers of commerce; MERSIS (Merkezi Sicil Kayıt Sistemi) central system run by Ministry of Trade (Ticaret Bakanlığı); Gazette published by TOBB (Union of Chambers)
- **Open API:** no · None public (MERSIS login-gated end-user portal; Gazette web search portal)
- **Delivers:** data, documents | documents via API: **no**
- **Auth:** MERSIS: login-gated (e-Devlet / e-Government login), end-user operations only, no developer API. Trade Registry Gazette (ticaretsicil.gov.tr): free membership/login to search; certified copies purchased online. No API keys anywhere.
- **Cost (free):** MERSIS access is free but restricted to authenticated end users (no bulk/API). Trade Registry Gazette search is free (requires free membership); announcements can be viewed/printed for free. CERTIFIED gazette copies (digital or wet-signature) are paid per copy per the 'İlan Ücretleri/announcement fee tariff'; exact per-copy amount not confirmed from primary page. No API pricing because there is no API.
- **Notes:** Two distinct sources: MERSIS holds structured company DATA (registration/modification/deletion records) but is login-gated for end users with no programmatic access; the Trade Registry Gazette is the DOCUMENT source — announcements (incorporation, changes, etc.) are free-searchable and viewable/printable, with certified copies sold per copy. Neither exposes a clean open API. Direct integration is NOT viable via an official API; you would need screen-level/portal automation or a vendor. Documents (Gazette announcements) are the reliably free, publicly reachable asset.
- **Confidence:** medium
- **Sources:** [MERSIS portal — central registry system for companies; only end-user guides (login/establishment/modification); no API/developer docs; e-Devlet integration noted](https://mersis.ticaret.gov.tr); [Türkiye Ticaret Sicili Gazetesi portal — free membership to search announcements; announcements saveable/printable; certified copies (digital/wet signature) purchasable; 'announcement fee tariff' referenced; no API](https://www.ticaretsicil.gov.tr)

### US — Delaware General Information Name Search / Document Filing & Certificate Request Service

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** Delaware Division of Corporations (Delaware Department of State)
- **Open API:** no · none — web portal (name/status search) + online certificate/document request; also phone/mail/fax orders
- **Delivers:** — | documents via API: **no**
- **Auth:** n/a — public web search (no login) for name/status; ordering via Document Filing & Certificate Request Service, phone, or mail.
- **Cost (per_document):** Free but very thin online entity/name/status search (name, file number, incorporation date, registered agent only). Paid, per-document: short-form Certificate of Good Standing ~US$50; long-form ~US$175; certified copy ~US$50; plain photocopy ~US$10; expedited ~US$50-1000. Amounts from Delaware's published fee schedule PDF, NOT fetched this session.
- **Notes:** Two decision-killers for direct integration: (1) NO API of any kind; ordering is portal/phone/mail and per-document paid. (2) Delaware's public record is extremely thin for KYC — no officers, directors, shareholders or UBOs; even a certified certificate of incorporation reveals little beyond incorporator/registered agent. Direct integration not possible, and manual retrieval yields limited KYC value — a vendor or the registered agent is usually needed.
- **Confidence:** medium
- **Sources:** [Delaware Division of Corporations homepage — free entity search, online request service, no API](https://corp.delaware.gov/); [Fee page — fees live in a downloadable Corporate Fee Schedule PDF; phone ordering; no API](https://corp.delaware.gov/fee/)

### VG — VIRRGIN (Virtual Integrated Registry and Regulatory General Information Network)

**🔴 Vendor only (no usable API)** — no registry API — portal/per-document only

- **Body:** Registry of Corporate Affairs, BVI Financial Services Commission (BVI FSC)
- **Open API:** no · VIRRGIN (agent-gated electronic filing/search system; no open developer API) · docs: <https://www.bvifsc.vg/>
- **Delivers:** data, documents | documents via API: **no**
- **Auth:** Restricted accounts issued by the FSC to licensed BVI registered agents/law firms only; no public/self-service credentials, no OAuth/API keys for third parties.
- **Cost (per_document):** No public API. Searches, certificates of good standing and filed documents are ordered through a registered agent for per-item statutory fees (~US$25-50+ per certificate/search) plus the agent's markup. Beneficial ownership (BOSS/RA-BO) is not publicly accessible.
- **Notes:** VIRRGIN is agent-gated: only FSC-licensed registered agents can incorporate, file and pull records. NO open public API and only limited public-facing data. Direct integration is effectively impossible without being (or contracting) a BVI registered agent; in practice route through an agent or an aggregation vendor. bvifsc.vg returns 403 to automated fetches, so specifics rest on established registry facts.
- **Confidence:** medium
- **Sources:** [BVI FSC Registry of Corporate Affairs / VIRRGIN official domain (blocked automated fetch, 403)](https://www.bvifsc.vg/)

### ZA — CIPC company register

**🟡 Direct, contract needed** — documents via API but access is contract/gated (negotiation needed)

- **Body:** Companies and Intellectual Property Commission (CIPC)
- **Open API:** partial · CIPC e-Services / electronic transacting (enrolled customer code); BizPortal for registrations · docs: <https://www.cipc.co.za>
- **Delivers:** data, documents | documents via API: **yes**
- **Auth:** Enrolled CIPC customer: customer code + password, backed by a prepaid deposit/balance (minimum R250 deposit into the CIPC account). Not a public/open API — access is gated to registered/enrolled customers.
- **Cost (per_document):** Prepaid per-transaction against customer-code balance. Electronic disclosure certificate: R30.00 (a document). Data/records extract: R10.00 plus R0.04 per record. Certificate re. company information: R20-R50. Certified document copies: R5-R20. Company registration: R125-R475; name reservation R30-R50. Requires ~R250 minimum prepaid deposit.
- **Notes:** CIPC runs electronic transacting for enrolled customers (customer code + prepaid balance) and BizPortal; the disclosure certificate and record extracts are obtainable electronically, so DOCUMENTS (disclosure certificate) and DATA (record extracts) both flow through the electronic channel on a prepaid per-transaction basis. However, the fetched public pages document the products/fees and the customer-code/prepaid model but do NOT publish clean API/developer specs — real-time system-to-system integration exists in practice for enrolled parties (e.g. banks/bureaus) but is not openly documented. Direct integration is feasible via enrolment; expect a private onboarding rather than self-serve keys.
- **Confidence:** medium
- **Sources:** [CIPC e-services page: register as customer, obtain customer code, deposit R250; transaction fee ranges](https://www.cipc.co.za/?page_id=4844); [CIPC disclosure/fees: electronic disclosure certificate R30.00; data extract R10 + R0.04/record; certificate R20-R50; certified copies R5-R20](https://www.cipc.co.za/?page_id=3167); [CIPC services overview listing e-Services, BizPortal, Mobile App, disclosure certificates and B-BBEE certificates](https://www.cipc.co.za/?page_id=3272)
