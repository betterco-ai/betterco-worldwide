# Dänemark — Machbarkeit und Bauplan für einen eigenen Connector

*Intern, 2026-07-30. Nebenprojekt zur STP-Arbeit. Kein Code geschrieben, nichts bestellt,
keine Registrierung eingereicht. Companion: `STP_ARCHITEKTUR_PRODUKT_2026-07-31_INTERN.md` § 4,
`curation/registry_intelligence.json` (DK-Zeile), `CONNECTOR_FINDINGS_2026-07-28.md` (Muster
FR/GB).*

> ## Nachtrag 05.08.2026 — der Plan ist ausgeführt, **Frage 1 ist beantwortet**
>
> Zugang beantragt 31.07., freigeschaltet 04.08., Connector gebaut
> (`betterco_claude_api/dk_cvr_client.py`, 51 Selbsttests grün).
>
> **Frage 1 — vedtægter per API? Nein.** Erhvervsstyrelsen am 05.08.2026 wörtlich:
> *„Articles of association/vedtaegter are not available via the system-to-system solution.
> These must be ordered for a fee."* Damit tritt genau der in § 1 beschriebene Fall ein:
> **Hälfte 2 bleibt geschlossen**, DK sieht bei der Satzung aus wie Frankreich/Kbis.
> Offen ist nur noch der Preis.
>
> **Hälfte 1 ist dafür größer als hier angenommen:** Die **reelle ejere** kommen kostenfrei
> mit — über den Index `cvr-re` auf `https://distribution.virk.dk:8443` (TLS, seit 05.08.).
> Der Rest dieses Dokuments beschreibt den Stand *vor* diesen beiden Antworten; die
> gemessene Lage steht in `registry-access/DK_CVR/NOTIZ.md`.

---

## 1. Das Ergebnis vorweg

**Dänemark zerfällt in zwei sehr unterschiedliche Hälften — und die günstige ist nicht die,
die STP braucht.**

| | Was | Kanal | Aufwand |
|---|---|---|---|
| **Hälfte 1 — offen** | Strukturdaten, Eigentümer, Jahresberichte | freie APIs, teils **ohne Authentifizierung** | klein |
| **Hälfte 2 — geschlossen** | **vedtægter** (Satzung), Gründungsdokument, Protokolle | **Bestellung bei der Behörde**, keine API | offen, vermutlich manuell |

Für STP ist DK genau wegen **Hälfte 2** interessant: Der dänische Gesellschaftsvertrag ist eine
der vier Zuschlagspositionen, für die uns der Preis noch fehlt. Wenn *vedtægter* nicht per API
kommen, löst der Connector dieses Problem **nicht** — er sieht dann aus wie Frankreich/Kbis:
ein Dokument hinter einem manuellen Bestellprozess.

**Empfehlung: bauen, aber in der richtigen Reihenfolge und mit korrekter Erwartung.** Zuerst
die kostenlose Mail, die die entscheidende Frage klärt. Erst danach Code.

---

## 2. Was gesichert ist

### 2.1 Jahresberichte — frei, ohne Authentifizierung, sofort nutzbar

Erhvervsstyrelsens Regnskabs-Verteilung:

```
http://distribution.virk.dk/offentliggoerelser
http://distribution.virk.dk/offentliggoerelser/_search
```

- Elasticsearch + JSON, **kostenlos**, **keine Authentifizierung**
- Alle digital eingereichten Jahresberichte in **XBRL und PDF**
- Aktualisierung alle **10 Minuten**

Das ist der einfachste Connector, den wir je gebaut hätten — er braucht keinen Zugang, keinen
Vertrag und kein Warten. Für STPs drei Dokumentenarten allerdings **irrelevant**: Jahresberichte
sind keine der drei.

### 2.2 Strukturdaten und Eigentümer — frei, mit Registrierung

CVR System-zu-System-Zugang (Elasticsearch/REST-Distribution), beantragt per Mail an
**`cvrselvbetjening@erst.dk`**, danach kommen die Zugangsdaten per Mail.

- **Kosten: keine.** Weder pro Suche noch pro Datensatz.
- **Lizenz: CC BY 4.0**, Attribution *„Det Centrale Virksomhedsregister (CVR)"* — für uns
  unproblematisch, aber die Quellenangabe muss in die Provenienz (dieselbe Mechanik wie die
  INPI-Auflage Art. 2.4).
- **Auflage:** Registrierung und Unterzeichnung einer Erklärung zur Einhaltung der Bedingungen.
- Inhalt: Entitäten, P-Einheiten, **Eigentümer**, Vorstand, Branchencodes, Historie.

Der **ejerregister** (Eigentümerregister, legale Eigentümer ab 5 %) steckt hier drin. Das ist
genau die Spalte „Gesellschafter als Daten", die wir STP für Dänemark zusagen — heute über den
Vendor, künftig aus erster Hand und kostenlos.

### 2.3 Was die Rechtslage sagt

Aus unserer eigenen Registry-Intelligence (`goDirect: direct_strong`, Confidence *high*):

> *„Best DIRECT-integration candidate. Both structured data AND financial-statement documents come
> free via official channels … **Articles of association (vedtægter) coverage is less complete than
> annual reports**, but the accounts themselves are fully open."*

Diese Einschränkung war schon 2026-07-19 notiert. Die Recherche vom 2026-07-30 bestätigt sie und
verschärft sie: Satzung, Gründungsdokument und Generalversammlungsprotokolle sind **Dokumente, die
man bei Erhvervsstyrelsen bestellt** — sie fallen ausdrücklich nicht unter das CVR-Gesetz und
damit nicht unter die offenen Datenkanäle.

---

## 3. Was offen ist — die vier Fragen, die alles entscheiden

| # | Frage | Warum sie zählt |
|---|---|---|
| **1** | Sind **vedtægter** überhaupt per API/S2S abrufbar — oder ausschließlich per Bestellung? | Bestimmt, ob DK den Zuschlag für das Zusatzdokument eliminiert oder nur verlagert |
| **2** | Was kostet eine Dokumentenbestellung, und wie lange dauert sie? | Vergleichsgröße gegen den noch unbekannten Vendor-Zuschlag |
| **3** | Ist das **Sammenskrevet resumé** (der dänische Registerauszug) frei herunterladbar? | Wenn ja, entfällt für den Auszug der komplette Case-Preis |
| **4** | Mengengerüst für die S2S-Registrierung | Die Behörde fragt danach — deshalb liegt die Mail seit Tagen ungesendet |

**Die Mail, die drei davon beantwortet, ist bereits geschrieben.** Gmail-Draft
`r-8111797625774233102` an `cvrselvbetjening@erst.dk`, fertig formuliert, **nicht gesendet** —
es fehlte ausschließlich die Mengenangabe. Sie fragt zugleich nach *regnskaber per API* und
*vedtægter per API*.

> **Das ist die billigste Aktion im gesamten STP-Paket: eine Mail abschicken.** Sie kostet nichts,
> blockiert nichts und klärt die eine Frage, an der die DK-Entscheidung hängt.

---

## 4. Der Bauplan

Vier Phasen, jede für sich abnehmbar. Muster durchgehend `inpi_client.py` / `companies_house_client.py`:
ein Modul je Vendor, Selbsttest im Modul, Router in `api/routers/`, Skill dazu.

### Phase 0 — die Mail (heute, 10 Minuten)

Mengenangabe ergänzen, Draft senden. Antwort auf Fragen 1, 2 und 4 abwarten.
**Nichts danach hängt an Code, alles hängt an dieser Antwort.**

### Phase 1 — `dk_regnskab_client.py` (0,5 Tage, kein Zugang nötig)

`distribution.virk.dk/offentliggoerelser`, ohne Auth. Suche nach CVR-Nummer, Liste der
Veröffentlichungen, Download von PDF und XBRL. Selbsttest offline gegen gespeicherte Antworten,
plus ein Live-Smoke-Test — kostet nichts, kann also gefahrlos in CI laufen.

Deckt: Jahresabschlüsse. **Keine der drei STP-Arten.**
Wert: der Beweis, dass der dänische Kanal trägt, zum Preis eines halben Tages.

### Phase 2 — `dk_cvr_client.py` (1–2 Tage, nach Zugangsdaten)

CVR-S2S-Elasticsearch. Firmensuche, Stammdaten, Vorstand, **ejerregister**.

Zwei Dinge von Anfang an mitbauen, nicht nachrüsten:
- **Attribution** *„Det Centrale Virksomhedsregister (CVR)"* in jeden Provenienzsatz — CC-BY-Auflage.
- **Abrufdatum und Inhaltsdatum getrennt.** Derselbe Fehler wie bei DataInfogreffe (Abruf 2026,
  Inhalt 2019) ist hier ebenso möglich.

Deckt: die Datenspalte für DK. Damit fällt für DK-Daten der Vendor weg.

### Phase 3 — Registerauszug (*Sammenskrevet resumé*), abhängig von Frage 3

Wenn frei herunterladbar: in `dk_cvr_client.py` mit aufnehmen, ~0,5 Tage. Dann ist DK/Registerauszug
kostenfrei statt Teil eines 18-USD-Case.
Wenn nur über die Bestellstrecke: wie Phase 4 behandeln.

### Phase 4 — vedtægter, abhängig von Frage 1

- **Fall A: per API/S2S abrufbar** → in `dk_cvr_client.py`, ~1 Tag. **Der DK-Zuschlag entfällt
  vollständig.** Bestes Ergebnis.
- **Fall B: nur per Bestellung** (wahrscheinlicher) → dieselbe Form wie FR/Kbis: manuelle
  Warteschlange, optional später ein Playwright-Client hinter `PaidGate`, und erst **nach** einem
  dokumentierten manuellen Lauf. Dann bleibt die Vendor-Landesregel (Modus A) für DK die
  praktikablere Option — sofern Colins Zuschlag unter unseren Bestellkosten liegt.

**In Fall B ist die richtige Entscheidung nicht „trotzdem bauen", sondern „Preise vergleichen".**

---

## 5. Wirtschaftlichkeit — ehrlich gerechnet

| Position | Vendor heute | Direkt (Fall A) | Direkt (Fall B) |
|---|---|---|---|
| Registerauszug | im Case enthalten (18 USD) | 0 € *(wenn Frage 3 = ja)* | 0 € oder Bestellgebühr |
| Gesellschaftsvertrag | **Zuschlag, Höhe unbekannt** | **0 €** | Bestellgebühr + manueller Aufwand |
| Gesellschafterdaten | im Case enthalten | 0 € | 0 € |
| Jahresberichte | Zusatzdokument | 0 € | 0 € |

**DK ist Band Low — 18,00 USD je Case.** Das ist die *kleinste* Ersparnis aller
Direktkandidaten; Frankreich (88 USD) und Luxemburg (88 USD) sind die lohnenden Ziele. Der Grund,
DK trotzdem zu bauen, ist **nicht der Case-Preis**, sondern:

1. **Der Zuschlag verschwindet** (Fall A) — und damit eine der vier Positionen, deren Preis wir
   STP heute nicht nennen können.
2. **Unabhängigkeit von einem Preis, den wir nicht kennen.** Solange Colin die Zuschläge nicht
   liefert, ist jede DK-Kalkulation gegenüber STP eine Lücke.
3. **Der billigste Test der Architektur.** DK ist ein sauberer, kostenloser, gut dokumentierter
   Kanal — ideal, um die Aggregationsschicht an einem dritten Land zu prüfen, ohne Geld zu
   riskieren.

**Was DK *nicht* löst:** die Gesellschafterliste. In Dänemark gibt es dafür **kein
Registerdokument** — nur die Eigentümerdaten aus dem ejerregister. Das ist eine Eigenschaft des
dänischen Gesellschaftsrechts und durch keinen Connector zu beheben.

---

## 6. Fallstricke, die aus FR/GB schon bekannt sind

1. **`æ` ist kein Buchstabe mit Akzent.** Unicode-NFKD zerlegt es nicht — dänisch „Vedtægter"
   matchte in unserem Label-Abgleich **nie**. Bereits behoben (explizite Ligaturtabelle), aber
   beim DK-Connector der erste Punkt, den ein Test abdecken muss. Gleiches gilt für `ø`.
2. **Zwei Uhren.** Abrufdatum ≠ Inhaltsdatum. Bei Jahresberichten ist der Unterschied ein Jahr
   und mehr.
3. **Lizenzauflage beim Schreiben erfassen, nicht nachträglich.** Die CC-BY-Attribution ist zum
   Abrufzeitpunkt bekannt und später nicht rekonstruierbar — exakt die Falle, die bei INPI
   Art. 2.4 dokumentiert ist.
4. **Kein DK-Prod-Case vorhanden.** Unser Tiering für DK stützt sich auf Statut und Sandbox, nicht
   auf einen echten produktiven Vorgang. Der Flip „DK-Gesellschaftsvertrag base→additional" wurde
   deshalb bewusst **zurückgenommen**. Wer den Connector gegen die Vendor-Aussage prüfen will,
   braucht zuerst einen echten DK-Case.

---

## 7. Empfehlung in einem Satz

**Mail heute senden, Phase 1 als Halbtagsarbeit mitnehmen, Phase 2 nach Zugangserteilung — und
die Entscheidung über Phase 4 erst treffen, wenn beide Preise auf dem Tisch liegen: die dänische
Bestellgebühr und Colins Zuschlag.**

---

## Quellen

- [Erhvervsstyrelsen — Hent oplysninger fra CVR](https://erhvervsstyrelsen.dk/hent-oplysninger-fra-cvr)
- [Erhvervsstyrelsen — Support: Bestil dokumenter](https://erhvervsstyrelsen.dk/support-oplysninger-fra-cvr) *(403 für automatisierte Abrufe; Inhalt über Suchindex)*
- [Virk Data — System-til-system adgang til regnskabsdata](http://datahub.virk.dk/dataset/system-til-system-adgang-til-regnskabsdata)
- [Erhvervsstyrelsen — Kom godt i gang med Elasticsearch](https://erhvervsstyrelsen.dk/kom-godt-igang-med-elasticSearch)
- [datacvr.virk.dk — System-til-system adgang til CVR-data](https://datacvr.virk.dk/artikel/system-til-system-adgang-til-cvr-data) *(403 für automatisierte Abrufe)*
- [Datafordeler — Brugervilkår CVR (CC BY 4.0)](https://datafordeler.dk/vejledning/brugervilkaar/det-centrale-virksomhedsregister-cvr/)
- intern: `curation/registry_intelligence.json`, DK-Zeile, erhoben 2026-07-19/23
