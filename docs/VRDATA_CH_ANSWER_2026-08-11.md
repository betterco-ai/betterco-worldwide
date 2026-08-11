# VR-Data: Rückfragen Schweiz — Antwort (2026-08-11)

VR-Data hat vier Fragen zur Schweiz gestellt und dabei eigene Einschätzungen mitgeliefert.
Dieses Dokument hält die belegte Antwort fest, korrigiert eine der Einschätzungen und
enthält den versandfertigen (anbieterneutralen) E-Mail-Entwurf.

**Quellen:** `curation/document_kinds_curation.json`, `curation/document_kinds_evidence.json`,
`curation/document_kinds_routing.json`, `jurisdiction_matrix.json`,
`curation/registry_intelligence.json`, `curation/sandbox_harvest/CH/result.json`
(Fall CHE-449.572.759, BLUEROCK SWITZERLAND GMBH).

---

## 1. Basisdokumente CH — was heißt „2 Dok."?

| # | Kanal-Label | Entspricht |
|---|---|---|
| 1 | `Registry Extract` | Handelsregisterauszug (aktueller Stand) |
| 2 | `Company Registration` | Registrierungs-/Gründungsnachweis |

Bestätigt durch den Sandbox-Harvest: genau diese beiden Kategorien kamen zurück
(je zweifach, einmal mit Datumsstempel `<15/08/2023>`). Das `mandatory`-Feld derselben
Antwort nennt als Pflichtdokument `Certificate of Incorporation`.

**OFFEN → beim Anbieter nachfragen:** Die inhaltliche Abgrenzung von `Company Registration`
zum `Registry Extract` ist nirgends dokumentiert. Vor einer verbindlichen Kundenaussage klären.

## 2. Zusatzdokumente CH (auf Anfrage, Aufpreis)

Aus `jurisdiction_matrix.json` → `documentsNonMandatory`, alle beglaubigt:

- Commercial register extract – certified
- Register document – certified
- **Statutes – certified** ← das ist der „beglaubigte Gesellschaftsvertrag" (Einschätzung VR-Data korrekt)
- Certificate of incorporation – certified

## 3. Gesellschafter-/Aktionärslisten — KORREKTUR der Einschätzung

VR-Data hatte „Gesellschaftsliste / nur GmbH" unter die **Zusatz**dokumente gesetzt.
Richtig ist: bei der GmbH ist die Liste **Teil des Basis-Registerauszugs**, kein Zusatzdokument.

| Rechtsform | Verfügbar | Kategorie | Rechtsgrundlage |
|---|---|---|---|
| **GmbH** | ja | **Basis** (im Registerauszug) | Art. 791 Abs. 1 OR — Gesellschafter mit Name, Wohnsitz, Anzahl + Nennwert der Stammanteile sind gesetzlicher Registerinhalt |
| **AG** | **nein** | — | Art. 686 OR — Aktienbuch ist intern, wird nie eingereicht, nicht öffentlich. Nur VR, Zeichnungsberechtigte, Revisionsstelle im Register. **Keine** Einpersonen-Ausnahme (anders als AT) |
| **Genossenschaft** | eingeschränkt | **Zusatz** | Art. 837/877 OR — nur bei persönlicher Haftung/Nachschusspflicht in den Statuten; beim HR-Amt hinterlegt und einsehbar, aber nicht im Auszug |

Kernaussage nach außen: **Aktionärslisten für die AG gibt es in der Schweiz nicht** — das ist
Rechtslage, keine Abdeckungslücke. Die strukturierten Beteiligungsdaten
(`shareholders`: Name, Rolle, Anteilszahl), die der Kanal mitliefert, sind ein Datensatz,
kein Nachweisdokument (`dataBackup.isProof = false`).

## 4. Direktanbindung CH

Bewertung aus `registry_intelligence.json`: **`goDirect.verdict = direct_data_only`**.

| Kanal | Liefert | Kosten / Lizenz |
|---|---|---|
| Zefix Public REST API (`zefix.admin.ch/ZefixPublicREST/`), EHRA/BJ, deckt alle 26 kantonalen Register | Stammdaten (Name, UID/MWST, Sitz, Status, Rechtsform), SHAB-Publikationen | kostenlos, Basisabfragen ohne Key; opendata.swiss, kommerziell mit Quellenangabe |
| LINDAS SPARQL | dieselben Daten als Linked Data | kostenlos |
| Beglaubigte PDF-Auszüge | **nicht über die API** | pro Kanton bestellt, ~CHF 20–50 |

Noch ungeprüft, aber naheliegend: SHAB/SOGC-Feed für Änderungsmonitoring, UID-Register des BFS.

**Empfehlung:** hybrid — Identität/Organe/Monitoring direkt über Zefix, Nachweisdokumente
weiter über den bestehenden Bezugsweg. CH-Konnektor ist **noch nicht gebaut** (gebaut: FR, GB, DK).
Preisband CH = `Low` (Klasse A), also der günstigste Einkauf.

---

## E-Mail-Entwurf (anbieterneutral, noch nicht versandt)

**Betreff:** AW: Rückfragen Schweiz — Basis-/Zusatzdokumente und Aktionärslisten

Hallo [Name],

gerne, hier die Antworten der Reihe nach.

**1. Basisdokumente Schweiz — was steckt hinter „2 Dok."?**

Es sind zwei Dokumente, die standardmäßig und ohne Aufpreis mitgeliefert werden:

1. **Registerauszug** (Handelsregisterauszug, aktueller Stand)
2. **Registrierungsnachweis** (Company Registration / Certificate of Incorporation)

Deine Einschätzung „Registerauszug" ist also richtig, es kommt nur ein zweites Dokument hinzu.
Die genaue inhaltliche Abgrenzung des zweiten Dokuments zum Auszug klären wir gerade noch ab
und melden uns dazu nach.

**2. Zusätzliche Dokumente Schweiz**

Auf Anfrage und gegen Aufpreis sind vier Positionen verfügbar, jeweils in beglaubigter Form:

- Beglaubigter Handelsregisterauszug
- Beglaubigtes Registerdokument
- **Beglaubigte Statuten** (entspricht dem Gesellschaftsvertrag) — wie von dir vermutet
- Beglaubigte Gründungsurkunde

**3. Gesellschafter- und Aktionärslisten**

Hier müssen wir nach Rechtsform unterscheiden, und ein Punkt weicht von eurer Annahme ab:

- **GmbH:** Die Gesellschafter sind in der Schweiz gesetzlicher Registerinhalt — mit Name,
  Wohnsitz sowie Anzahl und Nennwert der Stammanteile (Art. 791 Abs. 1 OR). Sie stehen damit
  **bereits im Basis-Registerauszug**, also in Kategorie a) und nicht in c). Eine separate
  Gesellschafterliste gibt es nicht und wird auch nicht benötigt.
- **AG:** **Aktionärslisten sind in der Schweiz nicht verfügbar** — weder als Basis- noch als
  Zusatzdokument. Das Aktienbuch (Art. 686 OR) ist ein internes Dokument der Gesellschaft, wird
  nie beim Handelsregisteramt eingereicht und ist nicht öffentlich einsehbar. Im Register
  erscheinen nur Verwaltungsrat, Zeichnungsberechtigte und Revisionsstelle. Anders als in
  Österreich gibt es auch keine Ausnahme für die Einpersonen-AG. Das ist keine Lücke in der
  Abdeckung, sondern die Rechtslage — für AG-Fälle bleibt in der Praxis nur die Selbstauskunft
  bzw. ein Auszug aus dem Aktienbuch durch die Gesellschaft selbst.
- **Genossenschaft:** Ein Genossenschafterverzeichnis existiert, aber nur wenn die Statuten
  persönliche Haftung oder eine Nachschusspflicht vorsehen (Art. 837/877 OR). Es wird beim
  Handelsregisteramt hinterlegt und ist einsehbar, steht aber nicht im Auszug — daher
  **Zusatzdokument**, Kategorie c).

Ergänzend: Strukturierte Beteiligungsdaten (Name, Rolle, Anteilszahl) liefern wir für Schweizer
Gesellschaften mit aus. Das ist ein Datensatz, kein beglaubigtes Nachweisdokument — je nach
Verwendungszweck relevant zu unterscheiden.

**4. Direktanbindung Schweiz**

Die Schweiz ist einer der wenigen Märkte mit einer echten offenen Registerschnittstelle:

- Über **Zefix**, den zentralen Firmenindex des Eidgenössischen Amtes für das Handelsregister,
  sind Stammdaten aller 26 kantonalen Register per REST-API abrufbar — kostenlos, für
  Basisabfragen ohne Schlüssel, kommerziell nutzbar unter Quellenangabe. Dieselben Daten stehen
  zusätzlich als Linked Data zur Verfügung.
- **Beglaubigte Dokumente liefert diese Schnittstelle jedoch nicht.** Beglaubigte Auszüge werden
  weiterhin pro Kanton bestellt und kosten dort typischerweise CHF 20–50.

Unsere Empfehlung ist daher ein hybrider Ansatz: Firmenidentität, Organe und laufendes Monitoring
direkt über Zefix, Nachweisdokumente über den bestehenden Bezugsweg. Die Basisdokumente sind im
Länderpreis bereits enthalten; die Schweiz liegt bei uns in der günstigsten Preisklasse.

Bei Rückfragen gerne melden.

Viele Grüße
Eckhard

---

**Vor Versand entscheiden:** (a) bleibt die Preisklassen-Erwähnung drin? (b) offene Frage zum
zweiten Basisdokument transparent ankündigen oder erst nach Klärung antworten?
