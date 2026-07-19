# Registry intelligence — build vs. buy (INTERNAL)

For each analysed jurisdiction: what the registry is, whether it has an open API (and whether that API serves **documents** or only data), and the cost — to decide where we can integrate **directly** instead of paying an aggregation vendor.

> Verdict driver: the prize is a registry we can hit directly that also serves the **documents** (not just data), cheaply. Data-only or no-API → keep the vendor for filings.

## Scorecard

| Verdict | Jurisdictions |
|---|---|
| 🟢 Go direct (strong) | DK, FR, GB, PL |
| 🟢 Go direct (paid docs) | IE, IT, NO |
| 🟡 Direct, contract needed | AT, ES, SE |
| 🟠 Direct for DATA only — vendor for documents | BE, CH, CZ, FI, JE, LU, MT, NL |
| 🔴 Vendor only (no usable API) | CY, GG, IM, LI, PT |

## Per jurisdiction

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
