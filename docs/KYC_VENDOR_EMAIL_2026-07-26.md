# KYC.com — email draft, 2026-07-26

*Reply in the thread "KYC v2 API — ordering & pricing additional documents".*
*To: cduncan@ · Cc: latikap@, moriordan@*
*Answers Colin's 6 July question ("which jurisdictions are involved") with the verified table, then asks
the two things still open: the ordering process and the price.*

---

**Subject:** Re: KYC v2 API — ordering & pricing additional documents — our 15 jurisdictions

Hi Colin,

thanks for your answers, and thanks to Latika for Q3–Q6 — all clear and already implemented on our side
(document download via `GET /v2/Documents/{documentId}`, `statusId = 3` as the readiness signal, and our
document mapping rebuilt on `name` rather than `category`).

You asked back in July which jurisdictions are involved. Here is the answer, and it is now based on real
retrievals rather than the matrix: we ran all 15 of our priority jurisdictions through the v2 sandbox and
cross-checked 8 of them against our existing production cases.

**What we need per company.** Our customers' onboarding requires three documents, which are German KYC
concepts: a **registry extract** (the current official register record), the **constitutional document**
(articles / memorandum / statutes / charter), and a **shareholder list** (evidence of who holds the shares,
as a standing record). Every jurisdiction names and keeps these differently, so we mapped them document by
document instead of assuming equivalence.

**How to read the table.** *base* = arrives with the standard case. *additional* = the document exists for
that jurisdiction but is not in the mandatory set — this is the column that matters for the ordering and
pricing question. *"–"* = we found nothing that evidences that kind. The last column is not a document at
all: it is the structured `shareholders` data your Jurisdiction Matrix lists.

| # | Jurisdiction | Registry extract | Constitutional doc | Shareholder list (document) | Shareholders as data |
|---|---|---|---|---|---|
| 1 | France | base | – | – | Name, Address, Share count, Role |
| 2 | Italy | base | – | – | Name, Nationality, Share count, Role |
| 3 | United Kingdom | – (no equivalent) | – | no (CS01/AR01 = delta) | Name, Share count, Role, Address (if available) |
| 4 | United States | base | base ("Incorporation") | – | none |
| 5 | Spain | base | – | – | none |
| 6 | Denmark | base (2 docs) | **additional** | – | Name, Address, Reg. number, Role, Share count |
| 7 | Netherlands | base | – | – | Name, Birth date, Jurisdiction, Address, Role, Share count |
| 8 | Luxembourg | base | base | – | Name, Role, Address, Nationality, Share count |
| 9 | Switzerland | base (2 docs) | – | – | Name, Role, Share count |
| 10 | Israel | base | – | **additional** (Annual Return) | Name, Address, Role, Nationality, Share count, ID number, Appointed on |
| 11 | Japan | base | – | – | none |
| 12 | Belgium | base | **additional** ("Constitution") | – | Name, Share count, Role |
| 13 | Kuwait | base | – | – | Name, Role, Nationality — no share count |
| 14 | Singapore | base (Business Profile) | – | – (carried inside the Business Profile) | Name, Address, Nationality, Jurisdiction, Reg. number, Role, Share count, National ID |
| 15 | Hong Kong | base | **additional** | **additional** (NAR1) | Name, Role, Address, Share count, Appointed on, ID card number, Other names |

**In short:** the registry extract is covered almost everywhere (14 of 15). The constitutional document is
base in only two jurisdictions (US, LU). A standing shareholder list is base in none. So the documents our
customers actually still need sit in the *additional* tier — concretely:

- **Denmark** — Memorandum & Articles of Association
- **Belgium** — Constitution
- **Hong Kong** — Articles of Association, and NAR1 (Annual Return)
- **Israel** — Annual Return

**1) How do we order these?** You wrote that API ordering exists only for the Hong Kong registry and that
everything else is handled manually through you, with the document sent by email. Could you describe that
process concretely, so we can build our workflow around it: what does a request need to contain (case ID,
company, document type?), where does it go — you personally, or a shared mailbox we should use — and what is
the realistic turnaround? For Hong Kong, we would like to use the API path; is `DocumentPurchase` the right
endpoint for Articles and NAR1 specifically?

**2) What do these cost?** You confirmed that the price varies by jurisdiction and document type, and that
case creation covers the mandatory set only — but we do not yet have any figures. Could you send us the
per-document prices for the four cases listed above? Even indicative ranges would let us decide which of
them we pass on to our customers, and where we look for another route.

Two smaller points while we are at it:

**3) Please correct the table where we got it wrong.** For GB, US, ES, NL, LU, CH, IL and BE we could
compare against real production cases, so the base/additional split there rests on your mandatory
catalogue. For **FR, IT, DK, JP, KW, SG and HK** we only had sandbox evidence, so the tier is inferred.
Specifically: is the Danish Memorandum & Articles really additional rather than base?

**4) Do the shareholder data fields actually populate?** The last column is what the matrix promises; we have
not measured how often the fields come back filled. For the eight jurisdictions with no shareholder-list
document at all (FR, IT, DK, NL, LU, CH, BE, KW) that data is our only route to the ownership structure. Is
there a realistic coverage expectation? And is Kuwait correct in having no share count — shareholders named,
but holdings not returned?

Happy to take the ordering and pricing part on a short call if that is quicker.

Thanks,
Eckhard
