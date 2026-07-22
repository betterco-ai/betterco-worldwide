# KYC.com — vendor questions (v2 API), 2026-07-22

*Internal/vendor-facing (provider names are fine here — this is NOT an STP-facing document).*
*Also drafted as a Gmail draft. Primary ask: how to order & price additional documents.*
*Each question notes how far we actually verified it against the sandbox.*

---

**Subject:** KYC v2 API — ordering & pricing additional documents (+ a few integration questions)

Hi KYC team,

thanks again for the sandbox access — we've integrated against the v2 API and the full flow works well
end to end (search → create → members/org-chart → documents → report). Before we move toward production,
a few questions came up. The first is the most important for us:

**1) Ordering additional documents (priority).** For documents that are *not* returned in the base case —
e.g. articles/constitution, annual returns, financial statements (the "Non-Mandatory" set in the
Jurisdiction Matrix) — how do we request a *specific* document for an existing case via the API? We found
`GET /v2/DocumentPurchase/{caseCommonId}`, but it appears to be HKCR-only (400 elsewhere). Is there a
general, cross-jurisdiction document-order endpoint? What is the request/response shape, and how is the
ordered document then delivered (webhook `DocumentUploaded`, then download)?

**2) Pricing / quoting additional documents.** What does an additional document cost, and does it vary by
jurisdiction and document type? Is there a way to quote the price via the API before ordering? And to
confirm the cost model: does the case-creation price cover the "Mandatory" documents only, with
Non-Mandatory/additional documents charged separately?

**3) Document download auth** (sandbox observation — please confirm the intended production flow). When we
read a case's documents, each document object is `{link, name, category, dataSource}`, and the `link`
points to a separate host (in the sandbox: `https://api-service-uathk.knowyourcustomer.com/v2/documents/{id}`).
In the sandbox that link returns **401** both with our OAuth `PublicApi` bearer token *and* with no auth,
while the API host (`api.knowyourcustomer.dev`) returns **404** for the same document id. What is the
intended way to download the document bytes in production — is there an OAuth-authorized endpoint, or is a
workspace/session context required? We'd prefer a pure OAuth path if one exists.

**4) Production webhooks.** We've validated the subscription API in the sandbox (subscribe / list /
delete-by-id all work). We have not yet observed an actual delivery, and sandbox deliveries are documented
as unsigned and posted to `/sandbox/webhooks/subscriptions`. For production, could you confirm: (a) the
subscription endpoint, (b) how deliveries are authenticated/signed (HMAC secret + header?), and (c) that
`CaseReady` and `DocumentUploaded` can be relied upon to replace polling?

**5) Document-type catalogue per jurisdiction.** `category` is the classifying field (e.g. `CS01`), while
`name` is free text (e.g. `"CS01 <13/01/2026>"`), so we don't build logic on `name`. Is there a complete
list of the possible `category` codes per jurisdiction, beyond the per-case mandatory catalogue at
`/documents/rules/mandatory`? A canonical per-jurisdiction list would let us map delivered documents to our
internal categories reliably.

**6) Readiness signal.** We observed a case whose status *text* still read an intermediate value
("Google Search") while `caseReadyDatetime` was already set, and which later read `statusName "Ready"` /
`statusId 3`. Can you confirm the canonical "ready to read" signal is `statusId == 3` together with the
structure being populated (members/steps present), rather than the status text?

Happy to jump on a short call for the ordering/pricing part if that's easier.

Thanks,
Eckhard

---

## Verification status (what we actually tested, for our own records)

| # | Claim | Tested? | Result |
|---|-------|---------|--------|
| 1 | `DocumentPurchase` is HKCR-only; no general order endpoint found | partial | Endpoint known from skill; not exhaustively probed for a cross-jurisdiction order endpoint → asked as a question |
| 2 | No price/quote path for additional docs | not tested | Cost model for base is known; additional-doc pricing is genuinely unknown → asked |
| 3 | Sandbox doc `link` rejects OAuth (401), API-host id 404 | **verified live 2026-07-22** | `link`+Bearer → 401, `link`+no-auth → 401, api-host `/v2/documents/{id}` → 404. **Sandbox only** — prod may differ |
| 4 | Webhook subscription CRUD works; delivery + prod signing unknown | subscription **verified**, delivery **not** | subscribe/list/delete-by-id return real ids; no delivery ever received; signing/prod endpoint from docs only |
| 5 | `category` classifies, `name` is free text; no full catalogue found | field roles **verified**, catalogue **not** | Live doc object `{link,name,category,dataSource}`, `category="CS01"`, `name="CS01 <13/01/2026>"`; no catalogue endpoint found (not exhaustively searched) |
| 6 | `statusId == 3` is the canonical ready signal; status text lags | **verified live 2026-07-22** | Case 1000002771 now reads `statusName "Ready"`, `statusId 3`, `caseReadyDatetime` set; earlier harvest showed status text "Google Search" with `caseReadyDatetime` already set |
