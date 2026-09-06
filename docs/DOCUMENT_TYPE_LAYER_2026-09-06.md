# Do we need a document-type standardisation layer?

**Date:** 6 September 2026 · **Decides:** part of R4 (P2 core), but the vocabulary must be fixed
**before** R4 ships, because P3 exposes it to Septeo.

---

## CORRECTED 6 September, after review

**The decision: every delivered file is stored. The three German roles are a SEPARATE mapping
layer on top of that, not the filing rule.**

This inverts what the rest of this note originally proposed. The earlier version treated the
canonical kind as the primary classification and let unmapped documents fall through to a
"fallback". That is backwards, and it would have let a document be dropped for the crime of not
playing a German KYC role. The corrected model is two independent layers:

| | Layer | Question it answers | Applies to |
|---|---|---|---|
| **0** | **Storage** | Is every file the vendor delivered held by us, with its own label? | **every** document, always |
| **1** | **Role overlay** | Does this document play one of the three German roles? | some documents; most carry **none** |

Layer 0 has no concept of kinds. It stores what arrived, keeps `vendorName` and `vendorCategory`
verbatim, and its success condition is a count: **delivered == stored**, with anything else
explicitly recorded as missing or blocked, never silently absent.

Layer 1 is the existing curation, run over what was stored. A document carries **zero, one or
several** roles - `kinds_of()` already returns a list and returns `[]` for most documents, which is
the correct answer and no longer a problem to be handled.

**Three consequences for the build:**

- The acquisition carries `roles: []` (a set, often empty) **alongside** the vendor label, not a
  single `kind` that has to be true for the row to exist.
- **The filing target is decided by whether a built-in `documentType` fits, not by whether a role
  was found.** Most foreign documents have no built-in equivalent and are filed as process
  documents with their own label. That is now the normal path, not a fallback.
- `requestedKind` is meaningful only for sources you can ask a specific document of (INPI). For
  kyc.com you order a **case** and receive whatever set it yields, so it stays null there.

Everything below still holds for layer 1 - in particular that the role vocabulary is
contract-visible and must be settled before P3.

---

## The answer

**Yes — and it mostly exists already, in the wrong language and in the wrong repository.**
`betterco-worldwide/document_kinds.py` plus `curation/document_kinds_curation.json` is a
hand-authored, role-based mapping from vendor document labels to document *kinds*, per
jurisdiction. The Java aggregator cannot see it. That is the whole gap.

## Why a layer is not optional here

There are **four** vocabularies in play, and today nothing reconciles them:

| | Vocabulary | Owner | Shape |
|---|---|---|---|
| 1 | **Source-native labels** | each source, per jurisdiction | `CS01`, `Annual Return`, `Certificate of Change of Name` (kyc.com GB); `Kbis`, `actes`, `comptes annuels` (INPI); `AD`/`CD`/`HD`/`SI`/`UT`/`GS` (handelsregister) |
| 2 | **Canonical kinds** | us | `REGISTERAUSZUG`, `GESELLSCHAFTERLISTE`, `GESELLSCHAFTSVERTRAG` — functional roles, not titles |
| 3 | **BetterCo storage types** | the platform | a closed built-in enum, German-KYC shaped |
| 4 | **The consumer's kinds** | Septeo/STP | the same three roles as (2) today — which is why (2) exists at all |

Without a layer, every adapter invents its own path from 1 to 3, and the mapping becomes N sources
x M jurisdictions x each developer's judgement. Three consequences, all avoidable:

- **The same document is labelled differently depending on which source fetched it.** A French
  extract bought from kyc.com and one fetched from INPI would file differently. That destroys the
  premise that sources are interchangeable.
- **P5's routing table has nothing to key on.** It is defined as
  `(jurisdiction, document kind) -> ordered sources`. Without a shared kind, there is no table.
- **P2's `requestedKind` / `deliveredKind` / `substituted` cannot be expressed.** "We asked for a
  shareholder list and got something that plays that role" is a statement about kinds. In vendor
  labels it is not sayable.

## What the existing curation already gets right

Do not re-author this in Java. It encodes three things that took real work to establish:

1. **The mapping is functional, not textual.** GB's `CS01` *is* the shareholder list, though
   nothing in the name says so.
2. **One document can serve several roles.** `kinds_of("CS01 <14/02/2026>", "GB")` returns
   **both** `GESELLSCHAFTERLISTE` and `REGISTERAUSZUG` — so the mapping is many-to-many, and any
   schema assuming one type per document is already wrong.
3. **Some roles are filled by data, not by a document at all** (`via: "data"` — AT, NL). A layer
   that can only map document-to-document cannot represent those jurisdictions honestly.

It also carries `tier` (`base` vs `additional`), which is a **commercial** fact, not a type fact —
useful, but it belongs to routing and cost, not to the type mapping.

## The shape to build

**One layer, two mappings, kept apart on purpose:**

```
source-native label  --(A)-->  canonical kind(s)  --(B)-->  BetterCo documentType
   per source,                    ours,                        the platform enum
   per jurisdiction               vendor-neutral               + process-doc fallback
```

- **(A) is per source and belongs to the source adapter**, seeded from the existing curation JSON.
  kyc.com's own `category` field must not be used: the vendor stated on 23 July that it "is not
  normalized across jurisdictions and should not be considered a canonical document type". The
  name minus its date suffix is the input, which is what the curation already parses.
- **(B) is single and global.** Where a canonical kind has a genuine built-in equivalent
  (`GESELLSCHAFTERLISTE` -> `SHAREHOLDER_LIST`, `GESELLSCHAFTSVERTRAG` -> `ARTICLES_OF_ASSOCIATION`)
  it files into the customer slot. **Where it has none — which is most foreign documents — it files
  as a process document** (`OTHERKYCDOCS_<LABEL>`, "Sonstige Dokumente") keeping its vendor label in
  the filename. Never invent a `documentType`: a custom type round-trips through the API and is
  **invisible in the UI**, which is worse than not filing it.

**Keep the canonical vocabulary small.** It answers "does this document play a KYC role we care
about?", not "what is this document called?". A GB `Certificate of Change of Name` maps to no role
and that is a correct answer — it still gets stored, with its own label, as a process document.

**Where it lives:** a registry in `com.betterco.app.aggregation`, reading a JSON resource. The
pattern is already established in the backend — `KycCoverageMatrix`, `KycLegalForms` and
`KycPriceBands` are each constructed from a `ClassPathResource` under `kyc/`. This is the fourth of
the same kind, not a new mechanism. The curation JSON is generated from `betterco-worldwide` and
checked in, so the hand-authored source of truth stays where it is maintained.

## The timing constraint that decides when

**The canonical kind is contract-visible.** P3 exposes documents to Septeo as
`{documentId, kind, availability, source, fetchedAt, contentDate}`. Fix the vocabulary after P3 and
changing it later is a second contract break — the exact thing the whole phase ordering exists to
avoid.

So: **build the layer inside R4, but settle the vocabulary now**, before either ships.

## What this is not

- Not a new service, and not a normalisation of the vendor's data. We do not correct the vendor's
  labels; we record what they sent and add our reading of it alongside.
- Not a replacement for the vendor label. Both are kept: `vendorName`/`vendorCategory` verbatim for
  traceability, canonical kind for routing and for the contract. P2's acquisition schema already
  reserves fields for exactly this.
