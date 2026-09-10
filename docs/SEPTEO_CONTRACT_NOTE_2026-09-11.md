# Note to Septeo — API contract change before go-live

**Status: DRAFT, not sent.** Written 11 September 2026. Covers the P3 cut-over plus two refusals
added on 9 September. Send as one message, not three — see §5.

---

## Draft

**Subject:** Document-search API: identifier change and two new refusals before 1 October

Three things change in the document-search API before go-live. All three are in the branch we are
testing now, none is deployed to an environment you use, and the first one requires a change on
your side.

**1. Case and document identifiers become ours, not the provider's.**

Today the API hands back the provider's case number and the provider's document numbers, and accepts
them as keys. From this change on, it hands back BetterCo identifiers (24 hex characters) and only
those address a case or a document. The provider's numbers return `404`.

The list response changes shape at the same time:

| Field today | Field after the change |
|---|---|
| `caseCommonId` | `caseId` |
| `statusName` | `status` |

This is not a format change that a translation layer can absorb — the list shape changes, so code
reading `caseCommonId` will read `undefined`. If you are integrating against the provider's numbers
right now, this is the point to switch.

The reason is that the identifier has to survive a change of source. A case will not always be
served by the same provider, and an identifier that belongs to one of them cannot be the key that
you store.

**2. An order for a German company is now refused, with `409 jurisdiction_not_available`.**

Germany is sourced by BetterCo directly, from the German registers, not through the provider used
for the other jurisdictions. An order routed the old way would have bought a document we already
have. The refusal is explicit rather than silent so that it is visible in your integration rather
than showing up as a cost later.

**3. On a test instance, documents that are not yet ready return `503 pending_path_unavailable`.**

This path previously returned an empty list. The empty list was wrong: it said "this case has no
documents" when the true answer was "this instance cannot answer that question". A test instance
is not connected to the environment that holds the pending documents, so it cannot know. Production
behaviour does not change.

**What we need from you**

- Confirm who owns the identifier change on your side and whether 1 October is workable for it.
- Tell us if you are already storing the provider's case numbers anywhere durable. If you are, we
  should talk about that before the change ships, not after.

Everything else stays as it is. We would rather make this one change now than the same change twice.

---

## §5 — Notes for whoever sends this (not part of the message)

- **Send it as one message.** These are three parts of the same migration; split across three mails
  they read as three regressions. That was the whole argument for doing the identifier change before
  go-live rather than after.
- **Do not name the provider.** The note deliberately says "the provider" and "a change of source".
  Naming the upstream supplier to Septeo has never been done and should not start here.
- **Point 1 is the only one that costs them work.** Points 2 and 3 are informational; leading with
  all three as equals invites a longer conversation than the deadline allows.
- **What is not in the note, deliberately:** prices, the evidence-level question (D2), and the
  reuse policy. None of them is settled, and raising an unsettled question here would reopen the
  contract discussion this note is meant to close.
- Recipients: the integration contact currently working against the API, plus whoever owns the
  1 October date on their side.
