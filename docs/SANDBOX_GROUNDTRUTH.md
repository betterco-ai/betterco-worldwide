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
