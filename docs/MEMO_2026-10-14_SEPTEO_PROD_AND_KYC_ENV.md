# MEMO 2026-10-14 — Björn's questions, prod credentials, and the staging cliff on 19 Oct

**Status:** two Gmail drafts written, **neither sent**. Prod credentials **not yet delivered** to STP.
Staging loses its vendor access on **19 Oct 2026, 11:17 UTC** unless kyc.com extends it.

## What arrived

**13.10.2026, 09:27Z** — Björn Hartenstein (STP), cc Fabian Puls, Eric Misfeld, Manuel Schneider, in
reply to our 30 Sep release mail (`BetterCo_Document_Search_Integration_2026-09-30.pdf`).

His three questions:

1. Can `/document-search/match` search by **company name + address** (street, zip, city)? They often
   lack the correct foreign register number.
2. Has anyone at STP received the **prod credentials**? He hasn't.
3. Can the **staging test data** stay available longer (next week, ideally a year)?

His answers to section 10 of the guide:

| # | Question | Answer |
|---|---|---|
| 1 | Who decides on a match? | They decide per score; the threshold may vary over time and per customer |
| 2 | Full staging run | Around the end of this week |
| 3 | First prod jurisdictions | UK, NL, CA, AT, SK, ES, US, LU, BG, HK |
| 4 | What they store | The caseId |

## The answers, measured against origin/dev

**Address is not a match input, and that is by design.** `KycMatchRequest` takes `jurisdiction` and
`name` (required) plus optional `registerNumber`. `MatchCandidate.java` deliberately leaves address out
of scoring. But `GET …/document-search/cases/search` already returns `rawAddress`, `street`, `city`,
`zip`, `companyStatus` — they can compare addresses on their side today.

**The threshold trap.** Name-only tops out at **85** (`NAME_ONLY`). Register numbers are compared only
for **GB, IE, SG, HK** (rules 2026-09-30.1); everywhere else `numberComparable:false` and 85 is a
ceiling, not a verdict. Of Björn's ten countries, only **UK and HK** can ever score above 85. A
threshold > 85 silently excludes the other eight.

**Coverage of the ten, as far as measured:**

| Country | State | Measured |
|---|---|---|
| UK, HK | Number-comparable, full score range | rules 2026-09-30.1 |
| ES, LU | `checkable:false, NO_SEARCHABLE_REGISTRY` — orderable, not searchable | prod, 2026-09-28 |
| CA | Ontario only | 2026-09-10 |
| US | Delaware only | 2026-09-10 |
| NL, AT, SK, BG | **Not probed on prod** | — |

The free prod probe for NL/AT/SK/BG is promised to Björn "this week" and has **not been run**.

## Where "staging until 19 October" comes from

Not from us. kyc.com's automated mail *"Your KYC Sandbox access is approved"* (21 Jul 2026) says the
sandbox credential **expires 2026-10-19T11:17:54 UTC**. Staging runs on that credential (stg
runtime measured on the sandbox 2026-09-29), so the date travelled from handover docs into
the 30 Sep guide, `docs/SEPTEO_INTEGRATION_GUIDE_2026-09-30.html` ~l.236.

- The extension request `docs/KYC_VENDOR_EMAIL_2026-09-06.md` was **drafted, never sent**.
- The same 21 Jul mail carries the client secret in plaintext, and it was forwarded externally on
  22 Jul. **Rotate the sandbox secret** once the extension is settled.

## kyc.com: the second environment

Thread *"KYC - contract und mail"*:

- **24 Sep** — Jamie Anderson sends a POC agreement: second environment, 6 months, reseller terms, for
  the large prospect.
- **30 Sep** — signed by us (DocuSign).
- **2 Oct** — countersigned, with the first month's invoice: *access is switched on once settled.*
  **Payment status unverified.**
- **2 Oct + 12 Oct** — Colin Duncan sends the environment questionnaire (MS Form, multi-page; page 1 has
  5 required fields: company, contact, preferred URL, admin email, 2FA). Setup ~5 working days after.

Suggested page-1 answers: Founders1 GmbH · Eckhard Ortwein · a neutral subdomain (no partner name) ·
a **shared** admin mailbox (admins manage API credentials) · 2FA yes.

**Correction on prices.** We had *not* gone unanswered: Colin replied on **2 Oct** — DK Vedtægter not
offered; IL Annual Return €30.80 instead of €26.70 per case, only if **all** IL cases carry it from a
nominated date. Still open: whether it changes the **24h SLA**.

## Drafts (Gmail, not sent)

| To | Thread | Content |
|---|---|---|
| Colin (cc Uwe, Jamie) | "KYC - contract und mail" | Questionnaire + walkthrough this week; extend sandbox to the second env's go-live; does the second env get its own test access; IL SLA; can the "all IL" rule apply to the second env only |
| Björn (cc Fabian, Eric, Manuel @septeo.com) | his 13 Oct mail | Answers above; optional offer to return registry address per match candidate (**commits backend work**); per-country coverage this week; prod credentials "today, separately"; extension "requested"; asks them to store `rulesVersion` |

**Send Colin first** — Björn's draft says the extension has been requested. Björn wrote from
@stp.one on 13 Oct; the draft uses @septeo.com per the 5 Oct switch.

## Prod credentials for STP

Send **only** four values: base URL `https://app.betterco.ai/bcapi`, workspace ID (workspace "STP"),
API key, API secret (from `betterco_claude_api/workspaces/prod-stp_kyccom.env`). Login is
`POST /auth/login {key, secret}` → 1h token + rotating refresh token.

**Never send:** tenant/org IDs, the user email/password pair, the vendor credentials (they would name
the vendor), the swagger Basic pair.

**Channel**, per Eric's own rule from the staging handover (2 Jul): URL + workspace + key in one new mail
(Björn, cc Eric); the secret separately — 1Password share, a separate new mail to Björn only, or phone.

**Before sending:** consider issuing a fresh key. The current one placed our own paid prod order
(Barclays, 30 Sep) and sits in local `.env` files. Whether the platform can rotate keys is unverified.

## Open

1. Send the Colin draft, then the Björn draft.
2. Deliver prod credentials (promised "today" in the Björn draft).
3. Run the free prod probe for NL, AT, SK, BG (promised this week).
4. Decide the registry-address-per-candidate offer → BCP ticket if yes, otherwise strike it from the draft.
5. Fill in the questionnaire, book the walkthrough, confirm the POC invoice is paid.
6. Decide on IL Annual Return.
7. Rotate the sandbox secret.
8. Correct the 30 Sep guide's "19 October" once the extension is known.
