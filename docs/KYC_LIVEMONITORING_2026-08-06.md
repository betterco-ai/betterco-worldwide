# Live Monitoring bei KYC.com — Antworten und Nachmessung

*2026-08-06. Latika Puri (Business Analyst Lead) hat am 05.08. um 09:47 auf die Mail vom
30.07. geantwortet, inline zu allen acht Fragen. Antwort gelesen, danach in der Sandbox
nachgemessen. Zwei ihrer Aussagen sind bestätigt, eine ist zu eng formuliert, und der
Sandbox-Testfall trägt weniger, als er auf den ersten Blick verspricht.*

---

## 1. Die eine Aussage, die alles andere ordnet

> „This isn't currently possible without creating a fresh case from the registry — our live
> monitoring process compares the existing case against freshly pulled registry data and
> flags the differences. **What you're describing is perpetual KYC.**"

**Live Monitoring ist keine Änderungsmeldung, sondern eine terminierte Neubestellung.** Die
Frage „liegt etwas Neueres vor?" lässt sich indirekt nicht billiger beantworten als mit einem
vollen Fall. Dazu ausdrücklich:

> **„Each scheduled review generates a new review case pulled from the registry, so it's
> billed as a standard case rather than a flat subscription."**

Das ist die vom Anbieter bestätigte Fassung dessen, was im Septeo-Deck auf Folie 6 steht
(*„indirekt: in der Regel wie ein Abruf"*). Die Kernaussage des Decks — die kostenfreie
Aktualitätsprüfung des Direktkanals wiegt schwerer als der Stückpreis — ist damit nicht mehr
unsere Behauptung, sondern die des Vorlieferanten. **Für ReKYC ist das der eigentliche Hebel:**
bei jährlicher Prüffrequenz kostet der indirekte Weg jedes Jahr den vollen Fallpreis, der
direkte nichts.

Perpetual KYC ist bei KYC.com in Arbeit, zuerst für **Singapur, Hongkong und
Vereinigtes Königreich**, danach „as registry data allows".

---

## 2. Die übrigen Antworten, gekürzt

| # | Frage | Antwort |
|---|---|---|
| 1 | Für unseren Mandanten freigeschaltet? | „**From my understanding** it is enabled" — sonst Mail an Colin/Helpdesk. Nicht belastbar, siehe § 4 |
| 2 | Wie kommt ein Fall unter Beobachtung? | Kein Flag beim Anlegen. Ist Registry Review für den Mandanten aktiv, kommt **jeder Fall bei Abschluss** automatisch darunter |
| 3 | Welche Jurisdiktionen? | Alle mit Live-Registeranbindung. Sonst manuelle Prüfung — der Alert kommt trotzdem zum Termin und fordert Handarbeit an |
| 4 | Kosten? | **je Review ein Standardfall**, kein Abonnement |
| 5 | Aktualität? | Pull nach ihrem Zeitplan, **kein Push vom Register**. Änderungen werden markiert, sobald der Review-Fall fertig ist |
| 6 | Feuert `updatedDocument` bei Ersetzung? | „only alerts about an updated document", Annehmen ersetzt, Ablehnen behält. **Die gestellte Frage — trägt die Ersetzung eine neue `documentId`? — ist nicht beantwortet** |
| 7 | Webhook für Alerts? | **Nein.** Empfohlen: `POST /v2/Companies/lm-cases` **täglich** pollen |
| 8 | Sandbox-Testfall? | **Dragon Pearl Holdings Limited**, HK, Datenquelle HKCR |

Dazu zwei Nebenantworten:

- **Review-Datum:** wird bei Abschluss automatisch gesetzt (Abschlussdatum + Prüfperiode,
  **derzeit 5 Jahre** laut unserer Plankonfiguration). Änderbar über
  `PUT /v2/Companies/{caseCommonId}/review-date`.
- **Sandbox-Swagger:** liegt unter `https://api.knowyourcustomer.dev/docs`. Unser 404 vom
  30.07. war der falsche Pfad — siehe § 3.

---

## 3. Was die Nachmessung ergeben hat

### 3.1 Der Sandbox-Spec existiert — wir haben am falschen Pfad gesucht

`GET /swagger/v2/swagger.json` → 404 (unser Befund vom 30.07., weiterhin gültig).
`GET /openapi.json` → **200, 108 Pfade**, Titel „KYC Sandbox". Die von Latika genannte
`/docs`-Seite ist eine Swagger-UI, die genau darauf zeigt.

Zwei Funde, die in der Mail nicht vorkommen:

**Die Preset-Tokens für das Review-Datum stehen im Spec:**
`Do not review · Review now · 3 months · 6 months · 9 months · 1 year · 2 years · 3 years ·
5 years · 10 years` — oder ein explizites `DD/MM/YYYY`. Leer/`null` löscht das Datum.
Damit ist die Prüffrequenz je Fall über die API steuerbar; die 5-Jahres-Vorgabe des Plans
ist für ReKYC belanglos, weil wir sie fallweise überschreiben.

**Eine Sandbox-Uhr:** `/sandbox/admin/clock`, `/clock/set`, `/clock/advance` — laut
Beschreibung, um einen Fall an seinem `caseReadyDatetime` vorbeizuschieben, ohne zu warten.
**Gemessen: `controllable: false`** (sie läuft nicht im Manual-Modus). Ein terminierter
Review lässt sich also nicht vorspulen. Falls das umschaltbar ist, wäre es die einzige Art,
den Review-Mechanismus überhaupt zu testen — Frage an Latika.

### 3.2 Der erste echte Alert-Payload — und warum er weniger beweist als gedacht

Der genannte Testfall existiert (`externalCode 0987654`, synthetisch). Angelegt, Ready nach
84 s, geschlossen, `PUT review-date "Review now"` → 200. Danach zum ersten Mal überhaupt
Alerts gesehen:

```json
{"changeId": 9001,
 "officer": {"name": "Tang Wai Hung", "address": "Suite 2801, Two IFC, Central, Hong Kong",
             "role": "Director"}}

{"changeId": 9002,
 "expirationAlert": {"explanation": "Business Registration Certificate expires soon.",
                     "expiration": 21, "name": "Business Registration Certificate",
                     "expirationDate": "2026-07-18T00:00:00+00:00"}}
```

Hülle je Alert: `name`, `caseId`, `address`, `caseType`, `jurisdiction`, `caseStatus`,
`caseStepId`, `changes`. **Eine Änderung je Zeile**, typisiert über den Schlüsselnamen.
`lm-cases` liefert dieselben Fälle mit Zählern je Typ: `reviewAlertCount`,
`expiredDocumentsAlertCount`, `manualReviewAlertCount`, `amlAlertCount`.

**Kontrolltest — und der ist der Punkt.** Ein zweiter Fall derselben Firma, **nie
geschlossen, nie „Review now"**, trägt bereits **dieselben zwei Alerts mit denselben
`changeId` 9001/9002**.

> **Die Alerts sind beim Anlegen mitgeliefert. Sie sind eine Attrappe, kein Ergebnis des
> Review-Laufs.** Wir können den Parser dagegen bauen — die Form ist echt. Bewiesen ist
> damit **nicht**, dass die Review-Strecke funktioniert.

### 3.3 Zwei kleinere Abweichungen

**„Reviews only apply to closed cases" ist zu eng.** `PUT review-date` mit `"1 year"` auf
einem offenen Fall (Status Ready) → **200**, Antwort `{"reviewDate": "2027-08-06T…"}`. Die
Aussage beschreibt, wann das Datum *automatisch* gesetzt wird, nicht eine Sperre am Endpunkt.

**Feldabbildung beim Auslesen:** Das gesetzte Datum steht in
`caseDetail.details.common.scheduledReviewDate` — **nicht** in `caseDetail.caseReviewDate`,
das `null` bleibt. Wer das falsche Feld liest, hält jeden Fall für ungeprüft.

---

## 4. Was offen bleibt

| Punkt | Warum es zählt |
|---|---|
| **Trägt eine Dokumentersetzung eine neue `documentId`?** | Frage 6 ist nicht beantwortet, und die Attrappe enthält **keinen** Dokument-Alert (kein `newDocument`/`updatedDocument`/`removedDocument`). Entscheidet, ob der Alert allein zum Handeln reicht oder ob wir Inhalte selbst vergleichen müssen |
| **Ist Live Monitoring produktiv wirklich freigeschaltet?** | „From my understanding" ist keine Zusage. Produktiv liefert `lm-cases` weiterhin 0 — nicht unterscheidbar von „nichts hat sich geändert" |
| **Lässt sich die Sandbox-Uhr auf `manual` stellen?** | Ohne sie ist die Review-Strecke nicht testbar, nur ihre Datenform |
| **Was kostet ein Review-Fall genau?** | „billed as a standard case" — also Klassenpreis. Bei DK/IL/BE käme der noch unbezifferte Zuschlag obendrauf |

**Nicht anfassen, bis das geklärt ist:** eine ReKYC-Planung, die auf Alerts als billiges
Änderungssignal setzt. Indirekt kostet jede Prüfung einen vollen Fall — das ist eine
Produktentscheidung, keine Implementierungsfrage.

---

## 5. Was daraus folgt, in Reihenfolge

1. **Rückfrage an Latika** mit den vier Punkten aus § 4 — die `documentId`-Frage zuerst,
   sie ist die einzige, die eine Implementierung blockiert.
2. **Polling statt Webhook einplanen.** `POST /v2/Companies/lm-cases` täglich, wie empfohlen.
   Das ändert die Webhook-Planung: `CaseReady` und `DocumentUploaded` bleiben Push,
   Registeränderungen werden gepollt.
3. **Review-Datum je Fall setzen**, nicht die 5-Jahres-Vorgabe stehen lassen — über
   `PUT /v2/Companies/{caseCommonId}/review-date`, ausgelesen aus `scheduledReviewDate`.
4. **LM-Methoden in `kyc_com_client.py` ergänzen** — bisher keine vorhanden. Vier Endpunkte:
   `lm-cases`, `lm-alerts`, `lm-alerts-action`, `review-date`.

## Belege

Sandbox-Mandant, Fälle `1000004429` (geschlossen + „Review now") und `1000004435`
(Kontrolle, unberührt). Skripte und Payloads im Sitzungs-Scratchpad
(`lm_probe.py`, `lm_walk.py`, `lm_control.py`, `kyc_sandbox_openapi.json`).
