# Signup instructions — France (INPI RNE) and UK (Companies House)

*Step 1 of the agreed process: research → signup instructions → **your validation** → implementation.*
*Nothing is built against these until you confirm the accounts and credentials are real.*
*Researched 2026-07-26 against the official sources; confidence marked per item.*

---

## A. France — INPI RNE

### What you are signing up for
The **Registre National des Entreprises** open-data access at `data.inpi.fr`. This gives us the
structured company data **and** the filed document PDFs — *statuts* (articles / Gesellschaftsvertrag),
*actes* (deeds and amendments), *comptes annuels* (annual accounts). Free of charge.

**Not included:** the **Kbis** register extract. INPI does not issue it — that is Infogreffe, paid,
~3,06 € electronic. Separate signup, only if a customer needs a legally-recognised extract.

### Steps

1. Go to **`https://data.inpi.fr/register`** and create an account.
   The login is an **INPI Connect** identifier — the same account also works on `inpi.fr` and
   `eprocedures.inpi.fr`. If you already have an INPI Connect login, use it instead of creating a second.
2. Sign in, then open your personal space → **"Mes accès API / SFTP"**.
   This is the section where API access is managed; it is not granted automatically at registration.
3. Activate the accesses we need:
   - **Base RNE** (company data, JSON)
   - **Actes** (legal documents, PDF — this is the one that carries the *statuts*)
   - **Comptes annuels** (annual accounts, JSON + PDF)
   - *Optional:* **SFTP** — bulk delivery of the whole corpus with daily updates. Worth taking if we
     ever want the full dataset instead of per-company calls.
4. Note down the resulting **username + password**. The API authenticates with those credentials
   against a login endpoint that returns a session JWT — there is no separate API key to copy.
5. Send them to me for the `.env`, as **`INPI_USERNAME`** and **`INPI_PASSWORD`**
   (these are the exact names `inpi_client.py` already reads).

### ⚠️ ANSWERED BY A LIVE TEST, 2026-07-26 — step 3 is NOT optional

We tried the API with the new account. The login returns **403**:

```json
{"code":"403","webserviceCode":"api_sso_post_login_password",
 "errorCode":"connection_type_not_allowed",
 "message":"Accès impossible pour API","type":"access_forbidden"}
```

This is **not** a wrong password — the account is recognised, but **this login type is not
authorised for API use**. Registering at `data.inpi.fr` alone does not grant API access; the
accesses under **"Mes accès API / SFTP"** must be activated, and INPI's documentation states that
API use requires **"identifiants techniques"** (technical identifiers).

So one of two things is true, and only you can see which from inside the account:

1. The accesses (Base RNE / Actes / Comptes annuels) are not activated yet — activate them; or
2. Activation issues **separate technical credentials**, distinct from the portal login we are
   currently using. In that case those are what belong in `INPI_USERNAME` / `INPI_PASSWORD`.

Also worth checking there: whether activation is instant or INPI validates it first.

*(Diagnosed with a single request. We deliberately did not retry, to avoid tripping a lockout.)*

### What to verify while you are in there
- **What exactly are the accesses called in the UI?** The names above are from the documentation;
  the actual labels may differ.
- **Is a company account possible, or is it personal-only?** Relevant for who owns the credentials.

### Cost
**Free.** No payment rail, no card, no contract. INPI's statutory mission is to make RNE data
available "sous forme électronique et gratuite".

### Licence — resolved, and it is good news
I read the licence in full today (*Licence de réutilisation des informations du RNE*, 2024,
state-homologated under art. L.323-2 / D.323-2-2 CRPA). This closes the open ⚠️ item in
`FR_INPI_INTEGRATION.md`, which said PDF redistribution was unconfirmed:

- **Art. 1** defines "Information" as data in the register **"et dans les documents communiqués ou
  reçus par l'INPI"** — the filed documents are explicitly in scope, not just the structured data.
- **Art. 2.1** grants a non-exclusive, free right of reuse **"à des fins commerciales ou non, dans le
  monde entier et pour une durée illimitée"**.
- **Art. 2.2** explicitly permits **"de la communiquer, la diffuser, la redistribuer, la publier et la
  transmettre"** — passing the PDFs on to our customers is covered.

Three obligations we must build in, not read and forget:

1. **Art. 2.4 — attribution.** We must state the source **and the date of last update** of the reused
   information. This has to be captured per record at fetch time; it cannot be reconstructed later.
   The same article forbids suggesting any official endorsement by INPI.
2. **Art. 2.5 — search-criteria restriction.** We must respect art. A.123-69 code de commerce, which
   restricts which criteria may be used to search the data. Practically: we must not offer
   free search by natural-person criteria over RNE data. **This constrains the search widget**, not
   just this integration.
3. **Art. 4.4** — our reuse must not mislead as to the content, source or update date.

Personal data (art. 3) may be reused, subject to GDPR and livre III CRPA. Note separately that the
free public feed is legally reduced for natural persons (name, first names, month+year of birth,
municipality) — that is a statutory limit on what INPI publishes, not a licence restriction.

---

## B. United Kingdom — Companies House

### What you are signing up for
The **Companies House Public Data API** (structured company, officer and filing-history data) and
the **Document API** (the filing images as PDF). Both free, no per-call charge. This is where the
UK articles come from — the document that KYC.com bills as *additional*.

### Steps

1. Create a Companies House user account at
   **`https://find-and-update.company-information.service.gov.uk/signin`** (if you do not already
   have one). This is the same account type used for the public register.
2. Go to the developer portal: **`https://developer.company-information.service.gov.uk`** and sign in
   with that account.
3. Open **`/manage-applications/add`** and create an application. Required fields:
   - **Application name**
   - **Application description**
   - **Environment** — you must choose **test** (against the sandbox) or **live** (production).
     *Create both.* We develop against test and only point at live once the flow is proven.
     They are separate applications with separate keys.
   - Optional: privacy policy URL, terms and conditions URL — can be left empty for now.
4. Open the application → **"Create new key"**. Give the key a name and choose the client type:
   - **API key** ← this is the one we need (REST, HTTP Basic)
   - *Stream key* — for the Streaming API, not needed now
   - *OAuth web client* — only for authenticated user actions such as filing, not needed
5. Copy the generated key immediately and send it to me for the `.env`, as
   **`GB_COMPANIES_HOUSE_API_KEY`** (plus a second one for the test app if you create both).

### Restrictions to be aware of
- **Rate limit: 600 requests per 5 minutes.** Exceeding it returns `429 Too Many Requests` for the
  remainder of the window; repeated or deliberate violation can get the account suspended. The client
  will implement backoff from the start rather than after the first incident.
- Companies House guidance says to **restrict key use by IP address and domain** where possible, and
  never to commit keys to source control. The `.env` pattern already covers the second point.

### Cost
**Free.** Public Data API, Document API and the bulk products all carry no charge.

### Licence
No reuse licence is imposed. Companies House data is statutory disclosure under the Companies Act
2006, and s.47 CDPA means extraction does not infringe the registrar's database right. No attribution
obligation. We remain responsible for our own data-protection compliance.

---

## C. France, second half — Infogreffe (the paid Kbis route)

France is a **split vendor**: INPI free for statuts/actes/comptes, Infogreffe paid for the Kbis. The
section above only covers the free half. This is the other one. Researched in-browser 2026-07-26
(both sites are JS apps that return 403 to plain fetches).

**There are two separate Infogreffe products, and only one of them serves documents.**

### C1. DataInfogreffe API — self-service, credits, DATA ONLY

`https://datainfogreffe.fr/offres` → "S'INSCRIRE GRATUITEMENT". Free account, then buy credits at
**0,10 €HT per credit**. Full published catalogue:

| API | Credits | €HT |
|---|---|---|
| Fiche Identité | 1 | 0,10 |
| Représentants | 5 | 0,50 |
| Comptes Annuels (*data*) | 5 | 0,50 |
| Procédures Collectives | 5 | 0,50 |
| **Associés, actionnaires** | **30** | **3,00** |
| Entreprise Représentant | 50 | 5,00 |
| Diagnostic Financier (NOTA-PME / AFDCC) | 30–70 | 3,00–7,00 |

**No document product exists in this API.** No Kbis, no statuts, no actes PDFs. DataInfogreffe is a
data portal, not a document channel — so it is *not* the paid route our router needs for the Kbis.

**But note the fourth row.** *"Associés, actionnaires — identification des associés (ou actionnaires)
et répartition du nombre de parts (ou actions)"*, 3,00 €HT via self-service API. Our current position
is that France's shareholder list is `not_provable_from_registry` for SAS/SA and only available as
KYC.com data. This is a cheap, direct, per-call alternative. **It does not make a proof document** —
it is data, same category as the KYC.com `shareholders` fields — but it changes the sourcing options
for the FR Gesellschafterliste and deserves its own look.

### C2. Infogreffe subscription — the actual document channel

`https://www.infogreffe.fr` — an **abonnement**, not a credit wallet:

- **85,00 €HT / year** for the first user, **42,50 €HT** per additional user (max 5), beyond that on
  request. Monthly consumption is billed on top of the subscription.

Document tariffs at subscriber rates (statutory, art. R.743-140 code de commerce):

| Document | €HT | €TTC |
|---|---|---|
| **Extrait Kbis** | 2,03 | 2,44 |
| + electronic transmission | 0,52 | 0,62 |
| **→ Kbis delivered electronically** | **2,55** | **3,06** |
| Actes et statuts | 6,05 | 7,26 |
| Copie intégrale des comptes annuels | 6,05 | 7,26 |
| Bilan simple (données saisies) | 3,00 | 3,60 |
| Liste des actes déposés au Greffe | **free** | **free** |
| Chiffres clés | **free** | **free** |

**This reconciles the 3,06 € we have been quoting** — it is the Kbis TTC *including* electronic
transmission (2,44 + 0,62), not a base price.

**And it validates the split-vendor design in hard numbers:** Infogreffe charges **7,26 € TTC** for
*actes et statuts* — the exact documents INPI serves **free**. Routing statuts to INPI and only the
Kbis to Infogreffe is not a stylistic choice; it is 7,26 € saved per company.

### What is still open — do not build against this yet

**Whether documents can be ordered through an API at all, or only through the portal.** The document
tariffs above are the *subscription* price list; nothing on those pages establishes a programmatic
ordering endpoint. The one government document API (API Entreprise "Extrait RCS", which is
Infogreffe-sourced) is restricted to public administrations and local authorities — **not available
to us**. So the realistic assumption for now is portal-based ordering, possibly manual.

That question has to be answered before the annual 85 € is worth committing, because a manual portal
route changes what Phase 4 even is — a client, or a human process with a queue.

---

## D. What I could not verify, and where that leaves us

| Item | Status |
|---|---|
| GB signup flow, key types, 600/5min rate limit | **Verified** against the official developer portal today |
| FR licence incl. document redistribution | **Verified** — full licence text read today |
| FR: registering alone is not enough — API access must be activated | **Verified the hard way** — live login returns `connection_type_not_allowed` |
| FR: whether activation is instant or approved | **Unverified** — the one thing that could change the timeline |
| FR: exact UI labels of the accesses | **Unverified** |
| Infogreffe: DataInfogreffe API catalogue + credit pricing | **Verified** in-browser today — data only, no documents |
| Infogreffe: subscription price + statutory document tariffs | **Verified** in-browser today |
| Infogreffe: whether documents are orderable via API or portal-only | **Unverified** — decides what Phase 4 is |

Nothing else is blocked. Once the FR credentials exist, the first real task is validating the parts of
`inpi_client.py` marked `# SECONDARY` — the JSON field names in `/companies/{siren}/attachments` and
the two download paths — against a live account. Those were written defensively from a third-party
implementation and have never seen a real response.

**Sources:** INPI licence PDF (inpi.fr, 2024) · data.inpi.fr register + API access pages ·
inpi.fr acces-lapi-formalite-rne · developer.company-information.service.gov.uk (get-started,
how-to-create-an-application, developer-guidelines)
