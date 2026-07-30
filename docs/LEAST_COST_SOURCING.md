# Design memo — least-cost sourcing: one widget, a provider router keyed by jurisdiction

**Status:** design (no code yet) · **Date:** 2026-07-11 · **Author:** Claude (ww ui session)

> **Correction (v2):** an earlier draft claimed Northdata was "net-new, exists nowhere in the
> workspace." **That was wrong.** BetterCo already has a *fleet* of provider clients — Northdata,
> handelsregister.de, Transparenzregister, company.info, KYCnow, KYC.com — each a mature client with
> its own skill under the `kyc-registries` plugin (`betterco_claude_api`, shared package
> `betterco-client`). **The providers are built. The only missing piece is the router that unifies
> them into least-cost sourcing.** The rest of this memo reflects that.

## 1. Problem & goal

Today the app exposes two sourcing surfaces:

- **BetterCo / Northdata search** — company search where *finding* a company is free or near-free.
- **KYC.com report** — `create_case` is **BILLABLE** at four bands (**Low $18 / Medium $43.50 /
  High $88 / Premium $114**). Search + reads are free; the money is spent the moment you crawl a
  company into a report.

Customer challenge: **KYC.com data has a price; Northdata (and the German registries) are free or
cheap.** For every jurisdiction — and, crucially, for every *document/field within it* — we want to
source from the **cheapest provider that still covers it.**

**Goal:** merge the two widgets into **one jurisdiction-driven flow** with a **provider router** that
picks the least-cost route — transparently, showing the chosen source and its price before anything
billable fires.

## 2. The join key is jurisdiction — and the app is already ~80% wired for it

Everything routes off the **ISO jurisdiction code**. `reference()` (`kyc_case_app.py:384`) already
carries per jurisdiction the two facts a cost decision needs:

```jsonc
{ "code": "DE", "auto": true,        // is there a free automatic route?  ← seed of the free/paid switch
  "priceBand": "Low", "priceUsd": 18 } // what the paid KYC.com report costs
```

Coverage — *which fields/documents a jurisdiction returns* — is already modelled in
`jurisdiction_matrix.json` and served by `jurisdiction_detail()` (`kyc_case_app.py:295`):
`dataFields.{companyIdentity, controlling, shareholders}`, `baseDocuments`, `additionalDocuments`,
`sla`. That's the **coverage oracle** the router compares against.

What's missing is a layer that says *"for jurisdiction X (and document Y), here are the providers,
their cost and coverage — pick the cheapest that satisfies this case."* The binary `auto` flag
(`hintAuto` vs `hintManual` in `kyc_case.html`) is a two-value stand-in for that today. We
generalise it into a real **provider router** over the fleet BetterCo already owns.

## 3. The provider fleet already exists (this is the key realisation)

All of these are working clients in `betterco_claude_api`, importable from the shared
`betterco-client` package, each with a skill under the `kyc-registries` plugin:

| Provider | Client | Coverage | Cost | Sweet spot |
|---|---|---|---|---|
| **handelsregister.de** | `handelsregister_client.py` | **DE only** | **FREE** (portal free since Aug 2022, no key, Playwright scraper) | DE registry docs: Aktueller/Chrono Abdruck, **Gesellschafterliste, Satzung/Gesellschaftsvertrag, Jahresabschluss** |
| **Northdata** | `northdata_client.py` | **DE (deep)** + GB/NO/ES + intl (sparse) | low — ~flat sub; docs €0.10–0.20 bundled; person/company search effectively free | DE structured **ownership graph, representatives, financials, events**; chrono-HR + Gesellschafterliste; intl master data |
| **Transparenzregister** | `transparenzregister_client.py` | DE | paid **+ entitlement-gated** (requester must be entitled; per-firm creds) | **UBO / beneficial-ownership Auszüge** |
| **company.info** | `companyinfo_client.py` | DE (official docs + shareholder graph) | paid per doc | **Certified/signed** docs, **Satzung (`SA`)**, ownership structure charts |
| **KYCnow** | `kycnow_client.py` | (to classify) | (to classify) | — |
| **KYC.com** | `kyc_com_client.py` (via gateway) | **217 jurisdictions** (153 live + CA + US) | $18–$114 / report | **breadth** — the long tail & offshore |

**So least-cost sourcing is not a build-from-scratch — it's a wiring exercise over an existing fleet.**

## 4. Least-cost sourcing has TWO levels (this is what makes it powerful)

Not just "which provider per country" — also "which provider per *document/field* within a covered
country." Germany is the flagship case:

```
Required for a DE case:        cheapest source:
  • chronological HR extract  → handelsregister.de (FREE)  or Northdata (~€0)
  • Gesellschafterliste       → handelsregister.de (FREE)  or Northdata (~€0)
  • Satzung / Gesellschaftsvtr → handelsregister.de (FREE)  or company.info (SA, paid, if certified)
  • Jahresabschluss           → handelsregister.de (FREE)
  • structured ownership %     → Northdata (owners+financials, cheap)
  • UBO Auszug                 → Transparenzregister (paid, entitlement)
  • certified/signed PDF       → company.info (paid) — only when certification is required
```

Every one of those is a DE line item a KYC.com **$18 report** would otherwise bundle. On DE we can
assemble the *same* dossier from **free + near-free** sources and fall back to a paid provider only
for the specific artefact that genuinely needs it (certification, entitlement-gated UBO). That is the
core least-cost win, and it's document-level, not just country-level.

For **GB/NO/ES**, Northdata reaches but coverage is *sparse* (shareholders/reps often empty) — so the
router weighs "Northdata master data, free" vs "KYC.com full report, paid." For the **long tail /
offshore** (BVI, Cayman $114, exotic jurisdictions) KYC.com is the only coverage → it wins by default.

## 5. The combined flow

```
                       [ pick jurisdiction ]  ── the switch
                                │
                                ▼
              ┌──────────────────────────────────────────┐
              │  PROVIDER ROUTER                            │
              │  (ISO code, required docs/fields)           │
              │   → ordered providers per line item,        │   ← the ONLY missing piece
              │     each with { cost, covers?, sla }        │
              └──────────────────────────────────────────┘
                                │  cheapest provider that COVERS each required item
     ┌───────────────┬──────────┴───────────┬─────────────────┬──────────────┐
     ▼               ▼                      ▼                 ▼              ▼
 handelsregister  Northdata            Transparenzreg.    company.info    KYC.com
   DE · FREE      DE/intl · ~€0        DE UBO · paid      DE certified    breadth · $18–114
```

The UX is **one widget**: choose jurisdiction → enter name → the router resolves the route(s) and
shows *"Sources: handelsregister.de (free) + Northdata (€0) · KYC.com not needed"* or *"KYC.com ·
$43.50 (Medium)"* → the user confirms → the selected providers execute. The two widgets stop being
separate UIs; they become the **free end and the paid end of one cost-ordered decision.**

## 6. The provider abstraction & routing

Wrap each existing client behind one interface so KYC.com stops being the hardcoded upstream:

```python
class Provider(Protocol):
    id: str                                        # "handelsregister" | "northdata" | "kyc.com" | ...
    def covers(self, iso: str, item: DataItem) -> bool   # does it serve this jurisdiction + line item?
    def cost(self, iso: str, item: DataItem) -> Money    # 0 for free routes; band price for KYC.com
    def fetch(self, iso: str, item: DataItem, ref) -> Result
```

`DataItem` = a required field group or document type (ownership %, Satzung, UBO Auszug, …). `Coverage`
mirrors the shape `jurisdiction_detail()` already produces, so a provider is asked *"do you return
what this case requires?"* without a new schema.

**Routing table** — per (jurisdiction, item), cost-ordered providers; seeded from what the app already
knows (`auto`, `priceUsd`, the coverage matrix) + the fleet's known coverage, then hand-tuned:

```jsonc
// routing_table.json (illustrative — DE line items)
"DE": {
  "chronoExtract":   ["handelsregister", "northdata", "kyc.com"],
  "shareholderList": ["handelsregister", "northdata", "kyc.com"],
  "satzung":         ["handelsregister", "companyinfo", "kyc.com"],
  "ownershipPct":    ["northdata", "kyc.com"],
  "uboAuszug":       ["transparenzregister", "kyc.com"],
  "certifiedPdf":    ["companyinfo"]
},
"GB": { "*": ["northdata", "kyc.com"] },   // ND sparse → often KYC.com
"KY": { "*": ["kyc.com"] },                // offshore, no free route
"AF": { "*": [] }                          // KYC.com matrix gap (AF/BD/GH) → declare unsupported
```

**Selection rule** (per required item): walk providers cheapest-first; pick the first that `covers`;
if none cover → mark that item unsupported (don't silently bill). A case's total cost = sum of the
chosen provider per item — which is exactly how we *minimise* it (free German artefacts, pay only for
the certified/entitlement-gated ones).

## 7. Integration path (concrete)

1. `pip install -e betterco_claude_api` in this app → import `northdata_client`,
   `handelsregister_client`, `transparenzregister_client`, `companyinfo_client`, `kycnow_client`
   directly (they're all in the shared `betterco-client` package). No re-implementation.
2. Write thin `Provider` adapters over each client's existing methods (e.g. Northdata
   `get_owners(...)` → `fetch(DE, ownershipPct)`; handelsregister `download Gesellschafterliste` →
   `fetch(DE, shareholderList)`).
3. Author `routing_table.json` from the coverage facts already documented in each provider's skill.
4. Point `/api/search` (`kyc_case_app.py:481`) and `/api/create-case` (`:577`) at the router.

## 8. Schema reconciliation (additive — frontend shapes unchanged)

- Map each provider's results onto the app's existing result shape (`rawname`, `externalCode`,
  `rawAddress`, `companyStatus`) + the uniform `enrichment` object (`enrich_search_result()`,
  `kyc_case_app.py:215`). Northdata already returns structured location/registry/ownership data → many
  `enrichment` fields come for free rather than via ID decoders.
- Map provider documents onto the `baseDocuments/additionalDocuments` + `dataFields` shape from
  `jurisdiction_detail()`, so a handelsregister-sourced, a Northdata-sourced and a KYC.com-sourced
  case all look identical downstream. (Northdata→BetterCo MasterData mapping is already tabulated in
  the northdata skill — reuse it.)

## 9. UI changes (`kyc_case.html`)

- One search box; the router decides source(s) after jurisdiction + name are known.
- Replace binary `hintAuto`/`hintManual` with a **route panel**: per required item, *provider + price
  + SLA* (e.g. `Gesellschafterliste · handelsregister.de · free · minutes`), and a **total** shown
  **before** any billable action.
- Keep "Dry run" — now it previews *which providers would run and the total cost.*

## 10. Rollout phases

1. **Router scaffold, KYC.com-only.** Wrap the gateway as `Provider("kyc.com")`; routing table returns
   `["kyc.com"]` for every item. Pure refactor, no behaviour change.
2. **Add the German fleet.** Adapters for handelsregister.de (free) + Northdata (cheap) + Transparenz-
   register (UBO) + company.info (certified), ahead of KYC.com for DE line items. Measure $ saved on DE.
3. **Coverage-aware, item-level selection + route panel in UI.**
4. **Expand.** Northdata GB/NO/ES routes; classify & slot KYCnow; direct-registry integrations for
   more countries; hybrid dossiers (free base + paid specific artefact).

## 11. Open questions

- **Entitlement gating** — Transparenzregister orders are tied to an entitled requester + per-firm
  creds (compliance-critical). The router must carry *whose* credentials fire a paid/entitlement route,
  not just "cheapest." (Same for company.info per-firm keys.)
- **"Free" at volume** — Northdata is flat-sub/cheap, handelsregister.de is genuinely free (but a
  Playwright scraper → reliability/captcha risk at scale). Quantify the reliability/cost trade of free
  scraper vs paid API for the same DE artefact.
- **KYCnow** — coverage + cost unknown; classify before adding to the table.
- **Required-data definition** — is the required item set per customer, per case type, or a fixed
  BetterCo minimum? The selection rule needs this input.
- **Where the router lives** — app-side now vs the BetterCo document-search gateway (aligns with the
  APIs already proposed in `BACKEND_DEV_MEMO.md`; gateway-side means every client benefits).
- **Certification threshold** — when does a case actually *require* a certified company.info PDF vs a
  free handelsregister.de download? That rule decides how often we touch a paid provider at all.

## Appendix — provenance

- Provider fleet: `betterco_claude_api` (shared `betterco-client`), `kyc-registries` plugin skills:
  `northdata`, `handelsregister`, `transparenzregister`, `companyinfo`, `knowyourcustomer`.
- KYC.com cost model & bands: `knowyourcustomer` skill.
- App reference data: `reference()` `kyc_case_app.py:384`; coverage `jurisdiction_detail()` `:295` +
  `jurisdiction_matrix.json`; enrichment `enrich_search_result()` `:215`.
- Related backend proposals: `docs/BACKEND_DEV_MEMO.md`.
