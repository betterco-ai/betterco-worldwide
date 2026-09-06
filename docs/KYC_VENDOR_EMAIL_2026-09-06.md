# Vendor mail — KYC.com, 6 September 2026

**To:** Latika Puri · **Cc:** Colin Duncan
**Status:** DRAFT — not sent.

Four questions, in the order they cost us something. Each is answerable in one line; none needs a
call. Question 3 is the one that decides an architecture choice on our side, so it is worth the
most attention.

---

**Subject:** Sandbox after 19 October, document reuse, and two API questions

Latika,

four things, all short.

**1. The sandbox trial expires on 19 October.** We would like to extend it. If an extension is not
possible, we will move our testing to the production account and keep it to read-only calls against
cases that already exist — but an extension is simpler for both of us, and we would rather ask than
assume.

**2. Does your licence permit serving a document to more than one of our customers?** Concretely:
we buy a UK filing for customer A, and three weeks later customer B needs the same filing for the
same company. May we serve the copy we already hold, or does each customer require its own order?
We have not found this in the contract and would rather have your answer in writing than infer one.

**3. Is there a way to ask whether a case or document has changed, without ordering a new case?**
Our own rule is that we only reuse a document we can prove is still current — a stored copy plus a
cheap "has anything changed?" check. For registries that publish a filing history this is free. For
your API we have not found an equivalent: Live Monitoring appears to be the mechanism, and you told
us in August that each review is billed as a standard case. If that is the only route, then reuse
is not economic on your data and we will treat every request as a fresh order — which is fine, but
we would rather know than discover it later.

**4. A concrete API question.** `POST /v2/Case/search-by-properties` returns
`400 "One or more validation errors occurred."` on the sandbox for us. We send
`{"pageSize": 50, "pageNumber": 0, "propertyName": "Company Status", "propertyValue": null}`.
The same call works against production. Is `propertyValue` required, is `pageNumber` 1-based, or is
the endpoint simply not seeded in the sandbox? We have left the payload alone rather than change
something that works in production.

Nothing here is urgent except the first, which has a date on it.

Best regards,
Eckhard

---

## Why each question is asked (internal, do not send)

| | Question | What it decides |
|---|---|---|
| 1 | Sandbox extension | Whether free testing survives past 19 Oct. We already decided we can live without it — reads against production cases are free, and creating needs permission anyway — so this is convenience, not a blocker |
| 2 | Licence for cross-customer reuse | The least-cost thesis. Our own policy (reuse only with proof of no change) is settled; their permission is not, and our willingness is not their consent |
| 3 | A free change check | **The architectural one.** If no cheap check exists, reuse is uneconomic on this vendor and the saving has to come from going direct to registries — which strengthens the case for INPI and Companies House rather than weakening it |
| 4 | `search-by-properties` 400 | Our `scope=account` case list is down on any sandbox-pointed environment because of it. Low stakes, but free to ask while we are writing |

**Deliberately not asked:** anything about pricing (we have the bands), and anything that reads as
a negotiation opener. Question 2 is a contract question and may get routed to their commercial
side — expect a slower answer there than on 1, 3 and 4.
