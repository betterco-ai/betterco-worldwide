# Status und offene Punkte — 2026-08-07

*Nachfolger von `STATUS_TODO_2026-08-05.md`. Deckt eine Sitzung mit zwei Strängen ab: das
Septeo-Deck rechnerisch geradeziehen, und Latikas Antwort zu Live Monitoring auswerten.
**Alles, was hier nicht steht, gilt unverändert aus den Vorgängerdokumenten weiter** —
insbesondere die Septeo-Punkte, die Vertragssätze und die Arbeitsregeln in § 5 des Dokuments
vom 04.08.*

---

## 1. Deck: die Direktmärkte trugen fremde Kosten

`docs/STP_DECK_2026-07-31.html`, Folien 17 und 18.

Auf Folie 18 standen bei **Frankreich, Ver. Königreich und Dänemark** die Klassenpreise des
indirekten Wegs — also der Preis eines Bezugswegs, den wir dort gar nicht benutzen. Die
Fußnote wies zwar darauf hin, die Zahlen taten es nicht.

| Markt | Einkauf vorher | jetzt | Marge |
|---|---|---|---|
| Frankreich | 54,50 € | **6,06 €** (3,06 Kbis + 3,00 Kapitalverteilungsnachweis) | 15,50 → **63,94 €** |
| Ver. Königreich | 10,80 € | **0,00 €** | 4,20 → **15,00 €** |
| Dänemark | 10,80 € | **0,00 €**, Satzung offen | 4,20 → **15,00 €** |

Summe über die 15 Märkte: Einkauf **258,86 €** · Verkauf 435,00 € · Marge **176,14 €**
(vorher 328,90 / 435,00 / 106,10).

**Neu dazugekommen:**

- **SLA-Spalte** für alle 15 Märkte, Quelle `jurisdiction_matrix.json`, Feld `sla`. Zwölf der
  fünfzehn unter 70 Minuten; nur US, IL und KW bei 24 Stunden. US mit Fußnote: 49 Staaten
  24 Std., Wisconsin 10 Arbeitstage. „Weitere Jurisdiktionen" trägt die Spannweite
  25 Min. – 7 Tage.
- **Fußnote zum Monatspreis**: 322 € für Lizenz und Support, 3.864 € im Jahr, unabhängig von
  Volumen und Zahl der Märkte. **Bewusst ohne Anbieternamen** — das Deck nennt durchgehend
  keinen Vorlieferanten, und das bleibt so. Entscheidung in der Sitzung bestätigt.
- **SLA-Fußnote für die Direktmärkte**: Angegeben ist der Wert des indirekten Wegs, der als
  Rückfallebene bestehen bleibt. Für den Direktbezug ist **kein Wert zugesagt** — GB und DK
  liegen über synchrone Schnittstellen darunter, der französische Kbis über den Portalvorgang
  darüber. Es wurde keine Sekundenzahl erfunden; gemessene Latenzen liegen nirgends vor.
- **Folie 17, Dänemark** auf den Stand vom 05.08. gebracht: Registerauszug kostenfrei, Satzung
  kostenpflichtig mit offenem Betrag, Gesellschafterliste als Dokument nicht existent, Daten
  kostenfrei. Sonst hätte das Deck sich selbst widersprochen.

Beide Folien liefen nach der Änderung über die Folienhöhe (Folie 18 schnitt die Tabelle um
86 px ab). Folienlokal verdichtet und im Browser nachgeprüft: **keine Folie schneidet ab.**

### Nicht angefasst, aber zu entscheiden

- **Home Bands aus dem Order Form**: GB 1,70 €, US 17,35 €, DE 6,30 €. Folie 18 rechnet US
  weiter mit 26,70 € (Klasse B). Gilt der Home-Band-Satz für uns, ist der US-Einkauf um
  9,35 € zu hoch angesetzt und die Summe stimmt nicht.
- **DK-Status-Tags** stehen weiter auf „direkt i. V." / „in Vorbereitung" (Folien 7, 15, 16,
  18), obwohl der CVR-Direktzugang für Daten produktiv ist. Umhängen berührt vier Folien und
  hängt am Ausgang des Septeo-Termins.
- **FR-Einkauf 6,06 €** ist die konservative Lesart. Genügt die kostenlose RNE-Bescheinigung
  statt des Kbis, sind es 3,00 €. Steht als Bedingung in der Fußnote, bleibt Septeos Frage.

---

## 2. Live Monitoring: Latika hat geantwortet, und die Antwort ändert die Produktseite

Vollständig in `docs/KYC_LIVEMONITORING_2026-08-06.md`. Der Kern:

> **Live Monitoring ist keine Änderungsmeldung, sondern eine terminierte Neubestellung —
> „billed as a standard case".**

Damit ist die Kernaussage von Deck-Folie 6 — indirekte Aktualitätsprüfung kostet „in der Regel
wie ein Abruf" — **vom Vorlieferanten bestätigt** und nicht mehr unsere Behauptung. Für ReKYC
ist das der eigentliche Hebel: jährliche Prüfung kostet indirekt jedes Jahr den vollen
Fallpreis, direkt nichts. Echte Änderungserkennung („perpetual KYC") ist erst geplant, zuerst
SG/HK/GB.

**Kein Webhook** für Registeränderungen — empfohlen wird tägliches Pollen von
`POST /v2/Companies/lm-cases`. Das ändert die Webhook-Planung: `CaseReady` und
`DocumentUploaded` bleiben Push, Registeränderungen werden gepollt.

### Nachgemessen, nicht geglaubt

- **Der Sandbox-Spec existiert** — `/openapi.json`, 108 Pfade. Unser 404 vom 30.07. war der
  falsche Pfad (`/swagger/v2/swagger.json` 404t weiter). Darin die **Review-Presets**
  (`Review now`, `3 months` … `10 years`, oder `DD/MM/YYYY`): die Prüffrequenz ist je Fall
  über die API steuerbar, die 5-Jahres-Vorgabe des Plans ist belanglos.
- **Erster echter Alert-Payload** aus Latikas Testfall — `officer` und `expirationAlert`, eine
  Änderung je Zeile, typisiert über den Schlüsselnamen.
- **Kontrolltest, und das ist der Punkt:** ein zweiter Fall derselben Firma, nie geschlossen,
  nie „Review now", trägt **dieselben zwei Alerts mit denselben `changeId` 9001/9002**. Die
  Alerts sind beim Anlegen mitgeliefert. **Die Form ist echt, der Mechanismus ist unbewiesen.**
- **Feldabbildung:** das gesetzte Review-Datum steht in
  `caseDetail.details.common.scheduledReviewDate`, **nicht** in `caseReviewDate`, das `null`
  bleibt. Wer das falsche Feld liest, hält jeden Fall für ungeprüft.
- **„Reviews only apply to closed cases" ist zu eng:** `PUT review-date` auf einem offenen
  Fall liefert 200.

Sandbox-Fälle `1000004429` und `1000004435` im Mandanten, kostenlos, vom Anbieter so
vorgeschlagen.

---

## 3. Offen — neu gegenüber dem 05.08.

| Punkt | Bei wem | Stand |
|---|---|---|
| **Neue `documentId` bei Dokumentersetzung?** | Latika | **blockiert die Implementierung.** Frage 6 nur halb beantwortet; die Sandbox-Attrappe enthält gar keinen Dokument-Alert |
| **Sandbox-Uhr auf `manual` schaltbar?** | Latika | `controllable: false`. Ohne sie ist die Review-Strecke nicht testbar, nur ihre Datenform |
| **LM produktiv wirklich freigeschaltet?** | Latika / Colin | „From my understanding" ist keine Zusage; prod `lm-cases` liefert weiter 0 |
| **Was kostet ein Review-Fall genau?** | Colin | Klassenpreis — kommt der Zusatzdokument-Zuschlag obendrauf? Und kostet ein Review ohne Befund dasselbe? |
| **Gmail-Entwurf an Latika** | bei uns | **liegt fertig im Thread, nicht gesendet.** Enthält die vier Punkte oben plus zwei Doku-Korrekturen. Vor dem Senden entscheiden: bleiben die Doku-Korrekturen drin, und gehört die Preisfrage nicht besser in Colins Zuschlag-Thread? |
| **LM-Methoden in `kyc_com_client.py`** | bei uns | bisher keine. Vier Endpunkte: `lm-cases`, `lm-alerts`, `lm-alerts-action`, `review-date` |
| **Home-Band-Frage (§ 1)** | Entscheidung | ändert die Summe auf Deck-Folie 18 |

Alles Übrige aus `STATUS_TODO_2026-08-05.md` § 4 und `STATUS_TODO_2026-08-04.md` § 3/§ 4 steht
unverändert: DK-Routine abschalten, DK-Satzung Preis und Bestellweg, Perioden-Prüfung FR/GB/DE,
`registry_intelligence.json` DK-Zeile, Zuschläge bei Colin, `vendorDeliverable`-Spalte,
Rechtsformtiefe NL/LU/CH/BE, Kuwait, Vermittlungsschicht, stale `inpi_client.py`,
HK-Prod-Liste.

**Der Ausgang des Septeo-Termins vom 31.07. ist weiterhin nirgends dokumentiert.** Er ist die
größte Unbekannte in diesem Stapel — zuerst erfragen.

---

## 4. Woran man ansetzt

1. **Septeo-Termin nachtragen.** Unverändert der erste Schritt; ohne ihn arbeitet man an
   Annahmen — und das Deck ist jetzt rechnerisch scharf genug, dass falsche Annahmen teuer
   werden.
2. **Entwurf an Latika sichten und senden.** Zwei Fragen darin sind billig zu beantworten und
   machen den ReKYC-Bau frei.
3. **Die Perioden-Frage bei FR/GB/DE** — eine falsche Prozentzahl in einer KYC-Akte ist
   schlimmer als eine fehlende.
