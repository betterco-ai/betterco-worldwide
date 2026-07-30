# KYC.com — E-Mail-Entwurf Live Monitoring, 2026-07-30

*An: latikap@knowyourcustomer.com (technische Rückfragen Q3–Q6 kamen von ihr)*
*Cc: cduncan@knowyourcustomer.com, moriordan@knowyourcustomer.com*
*Neuer Thread — der laufende Thread dreht sich um Preise für Zusatzdokumente und sollte davon
nicht überlagert werden.*

**Alle Zahlen unten sind gemessen (2026-07-30), nicht geschätzt. Nur lesende Aufrufe;
`lm-alerts-action` wurde bewusst nicht aufgerufen.**

---

**Subject:** KYC v2 API — Live Monitoring: endpoints respond but return nothing

Hi Latika,

thanks again for your answers on the download flow and the readiness signal — both are implemented
and working.

A new question, and it is the one that matters most for our next phase. We are designing the
**periodic review** side of our product: for an existing case, how do we learn that something at
the registry has changed — a new or replaced document, or a change in shareholders — without
re-ordering the case?

Reading the production swagger, Live Monitoring looks like exactly that mechanism. We found:

* `POST /v2/Companies/lm-cases`
* `GET  /v2/Companies/{caseCommonId}/lm-alerts`
* `POST /v2/Companies/{caseCommonId}/lm-alerts-action`

and the `Models.Changes` payload, which carries `newDocument`, `updatedDocument` and
`removedDocument`, plus `shareholder` with `sharesHeld`, `officer`,
`personWithSignificantControl`, `amlAlert` and `expirationAlert`.

**What we measured.** All four calls below returned **HTTP 200 with an empty list**
(`itemCount: 0`) — no error, no 403:

| Environment | Call | Result |
|---|---|---|
| Production | `POST /v2/Companies/lm-cases` (empty filter) | 200, `itemCount: 0` |
| Production | `POST /v2/Companies/lm-cases` (`caseLevel: All`, `alertType: All`) | 200, `itemCount: 0` |
| Production | `GET /v2/Companies/{id}/lm-alerts` — two real cases | 200, `itemCount: 0` |
| Sandbox | the same two routes | 200, `itemCount: 0` |

So the routes exist and our credentials reach them, but we have **never seen a single alert**, and
therefore have never seen an alert payload. One of our production cases is a large UK plc with
filings recorded in May 2026; if monitoring were active on it, we would have expected at least a
document alert.

Two further observations:

* **`CreateCompanyModel` has no monitoring field.** We cannot find a way to place a case under
  monitoring through the API.
* **The sandbox has no swagger** — `GET /swagger/v2/swagger.json` returns 404 there, so the
  sandbox documents nothing about this feature, and we cannot exercise it in a test environment.

**Our questions:**

1. **Is Live Monitoring enabled for our tenant?** We assume not — but an empty list looks exactly
   the same as "enabled, nothing has changed", so we cannot tell the two apart.
2. **How is a case placed under monitoring?** Per tenant, per journey, per case — and is it doable
   via the API at all, given there is no field on case creation?
3. **Which jurisdictions does registry monitoring cover?** We would not expect all of them.
4. **What does it cost**, and on what basis — per case, per case per year, or a subscription?
5. **How current is it?** How often is the registry re-polled, and what is the typical delay
   between a filing at the registry and the alert appearing?
6. **Does `updatedDocument` fire when a document is replaced** — and does the replacement carry a
   new `documentId`? This decides whether an alert alone is enough for us to act on, or whether we
   have to compare content ourselves.
7. **Is there a webhook for alerts?** The subscription API lists `AmlMatch`, but we could not find
   an event for registry changes. If there is none, we would be polling `lm-cases` — please
   confirm that is the intended pattern and tell us an acceptable frequency.
8. **Can we try it in the sandbox?** A test case that actually raises an alert would let us build
   against a real payload instead of the schema.

If it is easier to cover this on a short call, we are happy to do that — but written answers to
1 to 4 would already unblock our planning.

Thanks,
Eckhard

---

## Notizen zum Entwurf (nicht mitsenden)

**Empfänger prüfen.** Der Auftrag nannte „Robins Kollegin". Im Thread gibt es keinen Robin —
technische Fragen (Q3–Q6) hat **Latika Puri** beantwortet, kaufmännische **Colin Duncan**,
Terminorganisation **Miriam O'Riordan**. Latika ist deshalb die naheliegende Adressatin. Falls
ein anderer Name gemeint war, vor dem Versand korrigieren.

**Warum ein neuer Thread.** Der laufende Thread wartet auf die Zuschläge für Zusatzdokumente und
auf Colins Belgien-Rückfrage. Live Monitoring ist ein anderes Produkt mit eigenem Preis; in
denselben Thread gepackt, verzögert es die Preisantwort.

**Bewusst nicht in der Mail:**
- Keine Vermutung, dass es nicht freigeschaltet ist — nur die Beobachtung. Die Schlussfolgerung
  soll der Anbieter ziehen.
- Kein Hinweis auf unsere Direktanbindungen. Wo dort geprüft wird, kostet es nichts; das ist
  unsere Verhandlungsposition und gehört nicht in die Frage.
- Der Betrag der Case-Preise bleibt draußen — es geht hier nur um Monitoring.

**Was von der Antwort abhängt:**
- Frage 1 bis 4 entscheiden, ob laufende Überwachung überhaupt anbietbar ist. Solange sie offen
  sind, steht im Kundendeck (Folie 22) korrekt „im Bezugskanal angelegt, für uns noch nicht
  nutzbar".
- Frage 6 entscheidet, ob ein Alert als Auslöser reicht oder ob wir zusätzlich Inhalte vergleichen
  müssen. Das ist ein Architekturpunkt, kein Detail.
- Frage 7 entscheidet zwischen Push und Polling — und damit über die Betriebskosten auf unserer
  Seite.
