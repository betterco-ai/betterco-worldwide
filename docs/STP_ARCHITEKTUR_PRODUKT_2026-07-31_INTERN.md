# STP — Architektur, Produkt und Kosten · INTERNE FASSUNG

**Stand 31. Juli 2026 · nicht an STP · Pendant zu `STP_ARCHITEKTUR_PRODUKT_2026-07-31_EXTERN.md`**

*Was hier steht und im Kundendokument bewusst fehlt: Anbieternamen, Einkaufspreise,
Marge, Connector-Stand, die Widersprüche in unserem eigenen Datenbestand und die
Verhandlungsposition. Companion-Dokumente: `ARCHITECTURE_AGGREGATION_2026-07-28.md` (Design),
`CONNECTOR_FINDINGS_2026-07-28.md` (Messungen), `HK_DOCUMENT_PURCHASE_2026-07-30.md`,
`STATUS_TODO_2026-07-29.md`.*

---

## 0. Die drei Dinge, die im Termin zählen

1. **Colin hat den Bestellweg für Zusatzdokumente bestätigt** — als Landesregel, die Dokumente
   kommen dann mit den Basisdokumenten mit, kosten aber extra (§ 1). Damit ist der größte offene
   Produktpunkt aus dem 22.-Juli-Update geschlossen. **Der Preis fehlt weiterhin.**
2. **FR und GB laufen produktiv über eigene Connectoren** (§ 3). Frankreich ist zugleich STPs
   Land 1 *und* eines der beiden teuersten der fünfzehn — dort schlägt die Direktanbindung am
   stärksten durch.
3. **Zwei Vertragsfelder müssen vor dem Einfrieren entschieden werden**: Nachweisstufe und
   Provenienz-Metadaten (§ 6). Beides ist nachträglich eine brechende Änderung für einen Kunden,
   der gerade erst migriert ist.

---

## 1. Colin Duncan, KYC.com — was tatsächlich zugesagt ist

### 1.1 Der Kern (Mail vom 27.07.2026, 12:26 UTC, Thread „KYC v2 API — ordering & pricing additional documents — our 15 jurisdictions")

Colin bestätigt die Zuordnung und stellt genau eine Rückfrage:

> *„Do BetterCo want this additional documentation to be provided for ALL cases within these four
> Jurisdictions or only those cases specifically called out?*
> *— If ALL, then KYC can set up an internal rule and these documents will be provided in each case*
> *— If for only specific cases, then I will work to identify a process, e.g. email address /
> information required, that will allow BetterCo to call-out for which cases they want the
> additional information."*

Dazu seine Methodenspalte je Land:

| Land | Methode laut Colin | Zusatzdokument |
|---|---|---|
| **Dänemark** | **Automated** | Gesellschaftsvertrag |
| **Israel** | **Via RS Team** | Gesellschafterliste (Annual Return) |
| **Belgien** | **Via RS Team** | Gesellschaftsvertrag („Constitution") |
| **Hongkong** | **Automated** | Gesellschaftsvertrag + Gesellschafterliste (NAR1) |

Und zu Hongkong, wörtlich bestätigt:

> *„the DocumentPurchase is the correct endpoint … 1. GET /v2/DocumentPurchase/{caseCommonId} —
> lists available filings … 2. POST /v2/DocumentPurchase with {caseCommonId, registryDocumentId}"*

Sowie zum Preis: *„In relation to pricing, I will provide this shortly as I am waiting on
colleagues to respond."*

### 1.2 Das Kostenmodell, bestätigt am 23.07.

> *„Yes you are correct, the cost for each document varies and will also vary from jurisdiction to
> jurisdiction. **The case-creation price only covers the Mandatory documents only.** The reason we
> split the documents into 'Mandatory' and 'Non-Mandatory' is to reduce the overall cost for our
> customers for those popular types of documents."*

Und zur API-Verfügbarkeit:

> *„We only have the API functionality to Get 'Non Mandatory' information for the Hong Kong
> registry. All other registries need to be manually handled via myself, and the documentation
> would be provided via email to a BetterCo agent."*

### 1.3 Was das kommerziell bedeutet

**Die Landesregel ist keine Kostenoptimierung, sondern eine Prozessoptimierung.** Der Zuschlag
fällt bei *jedem* Vorgang im betreffenden Land an — auch bei denen, in denen STP das Dokument
nicht gebraucht hätte. Bei einer Trefferquote von x % ist Modus A nur dann günstiger als Modus B,
wenn der Prozessaufwand der Einzelanforderung den Zuschlag der (1−x) unnötigen Abrufe übersteigt.

Für **IL und BE** kommt hinzu: „Via RS Team" heißt **manuell beim Anbieter**, auch als Landesregel.
Das ist eine Laufzeit- und eine Skalierungsfrage, die Colin bisher nicht beziffert hat. Wenn STP
dort Volumen fährt, ist die Landesregel ein Versprechen, das ein Mensch bei KYC.com einlösen muss.

**→ Frage an Colin, die noch nicht gestellt ist:** Was ist bei „Via RS Team" die zugesagte
Laufzeit, und gibt es eine Mengengrenze? Ohne das können wir STP für IL/BE kein SLA geben.

### 1.4 Colins Rückfrage zu Belgien ist noch unbeantwortet

> *„Can you confirm whether the case information provided via the Belgium jurisdiction already
> includes the Constitution information you require or not."*

Unser Prod-Cross-Check (2026-07-23) hat für BE einen echten Case gesehen. Vor der Antwort an Colin
gegen `curation/prod_check.json` prüfen, ob „Constitution" dort im Mandatory-Katalog stand —
sonst behaupten wir eine Lücke, die es nicht gibt, und bezahlen einen Zuschlag für ein
Basisdokument.

**Antwortmail an Colin steht aus.** Der Call vom 29.07. (WhatsApp) ist nicht im Thread
dokumentiert — was dort besprochen wurde, gehört als schriftliche Bestätigung in den Thread,
bevor wir STP etwas zusagen.

---

## 2. Einkaufspreise — die vertraglich vereinbarten Sätze

> **Vertraulich. Diese Beträge sind Vertragskonditionen und gehören unter keinen Umständen in
> ein kundenseitiges Dokument.** Das Kundendokument nennt ausschließlich die Klassen A–D.

**Quelle: `09_Finance/2604_KnowYourCustomer/KYCCOM_F1_Final_Docusign.pdf`** — Flexible Plan
Order Form, Commencement Date **13.04.2026**, Initial Term **12 Monate**, Datenhaltung Irland.
Das ist die maßgebliche Quelle; die öffentliche Preisbandseite ist nur noch für die
**Zuordnung** Land → Band relevant, nicht für die Beträge.

### Entgelte laut Order Form, und was daraus verkauft wird

**Einkauf: Vertragssätze aus dem Order Form. Verkauf: Preisliste je Klasse, Stand 2026-07-30.**

| Band | Extern-Klasse | Einkauf je Vorgang ¹ | **Verkaufspreis** | Marge | Marge % |
|---|:--:|---:|---:|---:|---:|
| Low | **A** | 10,80 € | **15,00 €** | 4,20 € | 28,0 % |
| Medium | **B** | 26,70 € | **35,00 €** | 8,30 € | 23,7 % |
| High | **C** | 54,50 € | **70,00 €** | 15,50 € | 22,1 % |
| Premium | **D** | 70,50 € | **90,00 €** | 19,50 € | 21,7 % |
| *Home Band Ver. Königreich* | *A* | *1,70 €* | *15,00 €* | *13,30 €* | *88,7 %* |
| *Home Band Deutschland* | *A* | *6,30 €* | *15,00 €* | *8,70 €* | *58,0 %* |
| *Home Band USA* | *B* | *17,35 €* | *35,00 €* | *17,65 €* | *50,4 %* |
| Manual Case | — | 3,50 € | **offen** | — | — |
| Individual KYC Case | — | 1,70 € | **offen** | — | — |

¹ *Hinzu kommt eine **Grundgebühr von 322 € monatlich** für Lizenz und Support, unabhängig vom Volumen. Sie steckt in keinem Bandsatz: Bei 100 Vorgängen im Monat sind das 3,22 € je Vorgang, bei 1.000 nur 0,32 €. Ein Verkaufspreis, der bei niedrigem Volumen trägt, ist bei hohem großzügig — und umgekehrt.*

**Margenquote = Marge geteilt durch Verkaufspreis.** Die Quote **sinkt mit steigender Klasse**:
28,0 % bei A, 21,7 % bei D. In absoluten Beträgen ist es umgekehrt — D trägt 19,50 € gegen
4,20 € bei A. Ob das gewollt ist, ist eine Preisentscheidung, keine Rechenfrage.

**Für Manual Case und Individual KYC Case ist kein Verkaufspreis gesetzt.** Beide haben keine
Klasse und fallen damit aus der Staffel. Solange sie offen sind, ist ein manuell erfasster
Vorgang nicht bepreist.

**Zwei weitere Positionen, die nicht in der Bandtabelle stehen:**

1. **Zuschläge für Zusatzdokumente** — im Order Form nicht enthalten, Höhe unbekannt
   (§ 1). Sie kommen bei Dänemark, Israel und Belgien oben drauf.
2. **Direktbezugsländer rechnen anders.** Dort zahlen wir nicht den Bandsatz, sondern die
   amtliche Gebühr oder nichts (§ 3.1). Ein bandbasierter Verkaufspreis erzeugt dort die
   höchste Marge — genau deshalb lohnt der Ausbau der Direktseite.

### Die 15 STP-Länder zum Vertragssatz

| # | Land | Band | **Einkauf €** | Extern-Klasse | Direktkanal |
|---|---|---|---:|:--:|---|
| 1 | Frankreich | High | **54,50** | C | **produktiv** |
| 2 | Italien | Medium | 26,70 | B | Business Case |
| 3 | Ver. Königreich | **Low** | **1,70** ¹ | **A** | **produktiv** |
| 4 | Vereinigte Staaten | **Medium** | **17,35** ¹ | **B** | — |
| 5 | Spanien | Medium | 26,70 | B | — |
| 6 | Dänemark | Low | 10,80 | A | in Vorbereitung |
| 7 | Niederlande | Low | 10,80 | A | — |
| 8 | Luxemburg | High | **54,50** | C | Business Case |
| 9 | Schweiz | Low | 10,80 | A | — |
| 10 | Israel | Medium | 26,70 | B | geplant |
| 11 | Japan | Low | 10,80 | A | — |
| 12 | Belgien | Low | 10,80 | A | geplant |
| 13 | Kuwait | Low | 10,80 | A | — |
| 14 | Singapur | Low | 10,80 | A | — |
| 15 | Hongkong | Medium | 26,70 | B | — |
| — | *Deutschland (nicht im Vendor-Scope)* | *Low* | *6,30* ¹ | *A* | **produktiv** |

¹ *Home-Band-Satz laut Order Form. Die Bandzuordnung bleibt davon unberührt — GB und Deutschland sind **Low Band**, die USA **Medium Band**; entsprechend Klasse A bzw. B. Der Home Band ist eine Konditionsvereinbarung, keine eigene Preisklasse und kein Kundenmerkmal.*

Summe eines Abrufs über alle 15 einmal: **295,55 €**, Mittel **19,70 €**.

### Drei Befunde, die die bisherige Rechnung umstoßen

**1 — Es gibt Home Bands, und sie stehen in keiner öffentlichen Liste.** Das Vereinigte
Königreich kostet **1,70 €**, nicht den Low-Band-Satz. Damit spart die bereits gebaute
GB-Direktanbindung **1,70 € je Fall** — praktisch nichts. Ihr Wert liegt woanders: in der
kostenfreien Aktualitätsprüfung und darin, dass wir die **gültige** Satzungsfassung auflösen,
was der Bündelbezug nicht zuverlässig liefert. Das ist weiterhin ein guter Grund, sie zu haben —
aber kein Kostenargument, und als solches sollte sie nicht verkauft werden.

**2 — Alle bisherigen Ersparnisrechnungen waren zu hoch.** Wir haben mit den Listenpreisen
(18 / 43,50 / 88 / 114 USD) gerechnet. Die Vertragssätze liegen durchgehend darunter, teils um
mehr als die Hälfte. Die Schwellen im Direktanbindungs-Plan sind entsprechend neu gerechnet.

**3 — Der Vertrag kennt weder Zuschläge für Zusatzdokumente noch Live Monitoring.** Beide
Positionen sind im Order Form **nicht enthalten** — kein Preis, keine Erwähnung. Das bestätigt
Colins Aussage, dass der Fallpreis nur die Pflichtdokumente deckt, und es heißt zugleich:
Für beides gibt es **noch keine vertragliche Grundlage**. Was immer vereinbart wird, ist eine
Erweiterung des Order Forms.

### Preisrisiko der externen Klassen-Tabelle

Die extern veröffentlichte Klassen-Tabelle (Anhang A des Kundendokuments) ist eine 1:1-Abbildung
der öffentlichen Bänder von KYC.com — gleiche Länder, gleiche Reihenfolge der Klassen. Wer beides
nebeneinanderlegt, erkennt den Anbieter. **Das ist bewusst in Kauf genommen** (Kundenwunsch:
Preisinformation je Land), aber es ist kein Zufall, den man später wegdiskutieren kann. Wer die
Anbieterneutralität hart braucht, muss die Klassengrenzen verschieben, sobald ein zweiter
Bezugsweg je Land existiert.

---

## 3. Connector-Stand FR und GB — beide produktiv

Alles live gemessen (`CONNECTOR_FINDINGS_2026-07-28.md`), Ort: `betterco_claude_api`,
ein Modul je Vendor, kein Jurisdiktions-Router.

| Connector | Datei | Router | Zustand |
|---|---|---|---|
| Companies House (GB) | `companies_house_client.py` | `/companieshouse` (9 Routen) | **frei**, 25 Selbsttests, live verifiziert |
| INPI RNE (FR, frei) | `inpi_client.py` | `/inpi` (6 Routen) | **Bug behoben**, 26 Selbsttests, 6 Rechtsformen verifiziert |
| DataInfogreffe (FR, kostenpflichtig) | `datainfogreffe_client.py` | `/datainfogreffe` (6 Routen, `PaidGate`) | 29 Selbsttests, auf dem Démo-Wallet verifiziert |
| KYC.com Dokument-Map | `kyc_com_document_map.py` | — | 59 Selbsttests, auf alle 1 082 Matrixzeilen angewandt |

Skills `companieshouse`, `inpi`, `datainfogreffe`; Marketplace `kyc-registries` → 1.2.0.
Commit `cc93a02` auf `feat/ubo-bridge-graph-docs`. **Push-Status prüfen** — `git push` ist in
diesem Projekt classifier-geblockt, der User pusht mit `! git push`.

### 3.1 Frankreich — Kostenbild je Dokumentenart

| Dokumentenart | Kanal | Kosten | Nachweisstufe |
|---|---|---|---|
| Registerauszug (Kbis) | Infogreffe-**Portal, manuell** | 2,03 €HT + 0,52 € Übermittlung = **3,06 € TTC** ¹ | `certified` |
| Gesellschaftsvertrag (statuts) | INPI RNE API | **0,00 €** | `document` |
| Gesellschafterliste (Kapitalverteilung) | DataInfogreffe API | 30 Credits = **3,00 €HT** | `document` — **kein Siegel, kein „certifié conforme"** |
| Jahresabschlüsse | INPI RNE API | 0,00 € | `document` |

¹ zzgl. Abonnement **85,00 €HT/Jahr** (bezahlt), 42,50 € je weiterem Nutzer, max. 5.

**Gegenrechnung gegen den Vendor:** Ein FR-Case über KYC.com kostet **88,00 USD ≈ 81 €** und
liefert davon nur den Registerauszug als Basisdokument. Über den Direktweg kosten Auszug +
Satzung + Gesellschafterliste zusammen **6,06 €** plus anteilig das Abonnement. Selbst bei
niedrigem Volumen ist das eine Größenordnung, keine Marge.

#### Geprüft und verneint: die RNE-Attestation kommt NICHT über unsere API (2026-07-30)

Seit 01/2023 hat das RNE das RCS abgelöst; die INPI gibt dazu eine **Attestation d'immatriculation
au RNE** aus — kostenlos als PDF über `data.inpi.fr`. Naheliegende Hoffnung: Sie kommt über
unsere vorhandenen RNE-Zugangsdaten, deren Lizenz die Weitergabe ausdrücklich deckt. **Das ist
gemessen widerlegt.**

Probe am 2026-07-30, 22 GET-Aufrufe gegen `registre-national-entreprises.inpi.fr/api`, zwei SIREN
(790675037 SAS, 491520680 SARL), elf Kandidatenpfade:

- **Alle elf Pfade → 404.** Jeder Pfad hat mindestens einmal ein sauberes 404 geliefert; die drei
  `ConnectionError` sind Abwehr gegen schnelles Pfad-Raten, kein Signal (dieselben Pfade
  antworteten beim anderen SIREN mit 404).
- **`GET /companies/{siren}` trägt keinen Attestations-Link.** Einziges einschlägiges Feld:
  `formality.content.registreAnterieur.rncs.dateImmatriculation` — ein Datum, kein Dokument.

**Fazit:** Die RNE-API ist eine **Daten- plus Actes/Bilans-API**. Die Attestation ist ein Produkt
des Webportals, nicht der API. Die einzige Attestations-API liegt im API-Entreprise-Bouquet und
ist für uns gesperrt (*„réservée aux agents habilités"*, plus Kommerzialisierungsverbot) — dieselbe
Mauer wie beim Extrait RCS. Die Annahme `KBIS_TYPES → KbisViaInfogreffe` in `inpi_client.py`
**bleibt richtig.** Nicht erneut probieren; Skript liegt im Session-Scratchpad
(`probe_inpi_attestation.py`).

**Was daraus folgt:** Wenn ein Scraper, dann gegen **`data.inpi.fr`** (kostenlos, kein
Bezahlvorgang auslösbar, Lizenz deckt die Weitergabe) und nicht gegen Infogreffe (kostenpflichtig,
403 auf automatisierte Abrufe, Weitergaberecht ungeprüft). Zwei Vorbehalte bleiben: Ob die
*generierte* Attestation unter die Lizenz für *hinterlegte* Dokumente fällt, ist ungeprüft — und
die Attestation ist rechtlich kein Kbis. **Beides ist zu klären, bevor gebaut wird.**

**Der Haken beim Kbis selbst:** manueller Portalprozess, keine Bestell-API (bestätigt).
Entweder Menschenschlange oder ein Playwright-Client nach dem Muster von
`handelsregister_client.py` — letzteres erst nach einem dokumentierten manuellen Lauf und nur
hinter `PaidGate`. **Solange das nicht steht, ist FR/REGISTERAUSZUG nicht volumenfähig.** Das ist
die größte Lücke hinter dem, was das Kundendokument in § 5.3 zusagt.

### 3.2 Vereinigtes Königreich

| Dokumentenart | Kanal | Kosten |
|---|---|---|
| Gesellschaftsvertrag (Articles) | Companies House Document API | **0,00 €** |
| Jahresabschlüsse | Companies House Document API | 0,00 € |
| Registerauszug | **existiert nicht** — kein Kbis-Äquivalent | — |
| Gesellschafterliste | **existiert nicht** — CS01 ist ein Delta, PSC nur > 25 % | — |

Auth = HTTP Basic, **API-Key als Username, leeres Passwort**. Keys sind **host-gebunden**
(Prod-Key auf Sandbox → 401 und umgekehrt). Rate Limit 600 Requests / 5 min → Backoff von Anfang an.

**Die Falle, die uns fast erwischt hätte:** Articles müssen als **jüngste Änderung** aufgelöst
werden (`category=resolution`, Typ `MA`) — das Gründungspaket enthält die Ursprungsfassung. Monzo
hat sechs Fassungen; Gründung 2015, gültig 2024. Ohne diesen Schritt liefern wir eine zehn Jahre
alte Satzung aus und merken es nicht.

### 3.3 Die drei Bugs, die nur durch Ausführen gefunden wurden

1. **INPI `confidentiality` ist ein STRING**, Normalwert `"Public"`. `bool("Public")` ist `True` →
   jedes Dokument galt als vertraulich, **jeder FR-Download schlug fehl**, und es sah aus wie
   „diese Gesellschaft hat nichts eingereicht". Der freie französische Dokumentenkanal war die
   ganze Zeit tot. Regressionstest pinnt `"Public"`.
2. **UK Articles**: siehe § 3.2.
3. **`æ` ist kein Buchstabe mit Akzent.** Unicode NFKD zerlegt es nicht → dänisch „Vedtægter"
   matchte nie. Gleiches gilt für `ø`, `ß`, `ł`, `đ` — genau der lange Schwanz der Matrix
   (Dänemark, Norwegen, Polen, Kroatien). Behoben mit expliziter Ligaturtabelle.

### 3.4 OCR ist Pflicht, nicht Kür

INPI-Actes und Companies-House-Filings sind **Scans ohne Textebene** — gemessen: 0 Textzeichen
über 15 bzw. 43 Seiten. Nur die DataInfogreffe-PDF hat eine. **OCR gehört einmal in die
Aufnahme**, mit dem Text neben der PDF gespeichert — nicht in jeden Konsumenten.

---

## 4. Dänemark — Nebenprojekt, Bauplan

Eigenes Memo: **`DK_CVR_CONNECTOR_PLAN.md`**. Kurzfassung:

- **Kandidat ist stark.** CVR / Erhvervsstyrelsen, `goDirect: direct_strong`. Struktur*daten* und
  Jahresberichte **kostenfrei**, Lizenz **CC BY 4.0** (Attribution „Det Centrale
  Virksomhedsregister (CVR)"), System-zu-System-Zugang gegen kostenlose Registrierung.
- **Der Nutzen liegt aber woanders als gedacht.** DK ist Band Low (18 USD) — die Ersparnis pro
  Case ist die kleinste aller Direktkandidaten. Der eigentliche Grund ist **das Zusatzdokument**:
  DK/Gesellschaftsvertrag ist genau eine der vier Zuschlagspositionen. Wenn *vedtægter* frei über
  CVR kommen, entfällt der Zuschlag ganz — und wir hängen bei DK nicht an einem Preis, den Colin
  uns noch nicht genannt hat.
- **Die entscheidende offene Frage** ist genau diese: Sind **vedtægter** überhaupt per API
  abrufbar? Die Registry-Intelligence sagt ausdrücklich *„Articles of association (vedtægter)
  coverage is less complete than annual reports"*. Jahresberichte ja — Satzung unklar.
- **Der Gmail-Draft an `cvrselvbetjening@erst.dk` ist fertig und nicht gesendet**
  (`r-8111797625774233102`) — es fehlte nur die Mengenangabe. Er fragt genau diese Punkte.
  **Das ist die billigste Aktion im ganzen Paket: eine Mail.**

---

## 5. Widersprüche in unserem eigenen Datenbestand — vor dem Termin kennen

### 5.1 Routing-Datei vs. an KYC.com verifizierte Tabelle

`curation/document_kinds_routing.json` und die am 27.07. an Colin gesendete Tabelle **sagen für
fünf Länder Unterschiedliches** zum Gesellschaftsvertrag:

| Land | Routing-Datei | An Colin gesendet | Im Kundendokument steht jetzt |
|---|---|---|---|
| IT | `additional` (kyc.com) | „–" | **?** (in Prüfung) |
| ES | `additional` (kyc.com) | „–" | **?** |
| NL | keine Zeile | „–" | **?** |
| CH | keine Zeile | „–" | **?** |
| IL | `additional` (kyc.com) | „–" | **?** |
| KW | keine Zeile | „–" | **?** |

Ursache: Die Routing-Datei beschreibt **Registerwahrheit** (was liegt beim Register?), die
Colin-Tabelle **Bündelwahrheit** (was liefert der Vendor?). Beides ist in seiner Sicht richtig,
aber sie sind nie zusammengeführt worden. Das Kundendokument weist die fünf deshalb als „?" aus
und **sagt sie nicht zu** — die einzige Variante, die wir belegen können.

**Zu tun:** eine Spalte „vendorDeliverable" in die Routing-Datei, gespeist aus dem
Prod-Mandatory-Katalog. Ohne die wird derselbe Widerspruch bei der nächsten Jurisdiktion wieder
auftreten.

### 5.2 Lücken in der Rechtsformabdeckung

Gemessen an `document_kinds_routing.json` (446 Routen / 69 Jurisdiktionen):

- **KW fehlt vollständig** — 0 Zeilen.
- **NL, LU, CH, BE** haben **nur** GESELLSCHAFTERLISTE-Zeilen; Registerauszug und
  Gesellschaftsvertrag fehlen für alle dortigen Rechtsformen.
- **GB** unvollständig: PLC-Varianten teils ohne Auszug/Satzung.
- Vollständig über alle drei Arten: **FR, IT, US, ES, DK, IL, JP, SG, HK**.

Das Kundendokument nennt das als offenen Punkt „Rechtsformtiefe … Mitte August". Diese Zusage ist
**nur haltbar, wenn die Recherche jetzt angestoßen wird.**

### 5.3 HK base vs. additional

Die Evidence-Datei stuft HK-Satzung und NAR1 als `additional` ein (Registersicht), die
Vendor-Matrix führt beide als **mandatory** (Bündelsicht), und im Sandbox-Bündel lagen beide drin.
Das Kundendokument sagt korrekt: *„kommen beim Standardabruf meist schon mit"* und warnt vor dem
Doppelkauf. Das `purchased`-Flag ist die Wahrheit für den Einzelfall; die Klassifikation bleibt
unverändert. **Nicht auflösen, bevor eine Prod-Liste gezogen ist.**

### 5.4 Stale-Duplikat `inpi_client.py`

`betterco-worldwide/inpi_client.py` **enthält den Confidentiality-Bug noch**. Kanonisch ist
`betterco_claude_api/inpi_client.py`. Das Duplikat scheitert **still** — es meldet „keine
Dokumente". Löschen oder synchronisieren, aber nicht liegen lassen.

---

## 6. Vertragsentscheidungen — was vor dem Einfrieren fest sein muss

### D2 · Nachweisstufen — **blockierend, hoch**

`data` / `document` / `certified`, Apostille als Attribut. Der konkrete Test: STP fragt eine
französische Gesellschafterliste an.
- auf `certified` → richtige Antwort ist **„nicht verfügbar"**
- auf `document` → richtige Antwort ist der **3,00-€-DataInfogreffe-Nachweis**

Gleiche Anfrage, unterschiedliche Auflösung. Ohne das Feld liefern wir im Zweifel das Billigere
und merken es erst, wenn eine Bank die Akte ablehnt.

Neu untermauert durch einen konkreten Fehlerfall: Das Matrix-Label **„Historical – Shareholders"
(UK)** ist ein **Datenabschnitt**, kein eingereichtes Dokument. Reines Label-Matching würde
behaupten, UK könne eine Gesellschafterliste liefern — direkt gemessen widerlegt. Ohne
Nachweisstufe erreicht dieser Fehler den Case-Store.

### B3 · Provenienz hat keinen Platz — **blockierend**

`upload_customer_document` sendet exakt `{"name": …, "type": …}`. **Es gibt kein Metadatenfeld.**
Vendor, Abrufdatum, Inhaltsdatum, Quellreferenz, Nachweisstufe und Kosten haben kein Zuhause.

Die INPI-Lizenz (Art. 2.4) verlangt Quelle **und Datum der letzten Aktualisierung** — beim Abruf
bekannt, danach **nicht rekonstruierbar**. Hängt an einer unbeantworteten Frage:

> **Heißt „STP ruft BetterCo" das Kernprodukt-API oder unseren Aggregationsdienst davor?**
> - Aggregationsdienst → Provenienz lebt in `sourcing/`, wird beim Lesen gejoint. **Kein
>   Backend-Aufwand.**
> - Kernprodukt-API → das Dokumentmodell braucht ein Metadatenfeld. **Backend-Ticket mit
>   Vorlaufzeit.**

**Diese Frage sollte im Termin gestellt oder vorher intern entschieden werden.** Sie bestimmt, ob
B3 ein Nachmittag oder ein Sprint ist.

### B2 · Zwei kanonische Arten ohne Slot

`GRUENDUNGSURKUNDE` (61 Zeilen) und `STATUSBESCHEINIGUNG` (37 Zeilen) fallen auf
`OTHERKYCDOCS_SONSTIGE` zurück. Entscheidung: zwei Slots anlegen oder den Bucket akzeptieren und
die kanonische Art im Dokumentnamen führen. Maschinenlesbare Liste: `kyc_com_document_map.gaps()`.

Hintergrund, 2026-07-28 bestätigt: **Eine Gründungsurkunde ist kein Registerauszug.** Ein
Certificate of Incorporation bezeugt die Entstehung, nicht den aktuellen Registerinhalt; ein
Certificate of Good Standing bezeugt den Status, ist aber kein Auszug. **98 Matrixzeilen** wären
sonst als Auszüge fehlabgelegt worden.

### D1 · Aktualität · D3 · Aufbewahrung · D4 · Kostenweitergabe

Sichere Vorgaben stehen. Für **D4 gilt: jetzt instrumentieren, auch wenn das Preismodell wartet** —
Kosten je Case lassen sich aus einer monatlichen Vendor-Rechnung **nicht** rekonstruieren.

### N6 · Slot-Semantik vs. Historie

Kundendokumente sind ein **Slot** — „ersetzen, nicht anhängen". Ein neuer Auszug überschreibt den
alten. Richtig für Aktualität, zerstört aber die Historie. Falls STP je ein Dokument *zum Stand
eines vergangenen Datums* braucht, kollidiert das. Vor dem Bau der Ingestion klären.

---

## 7. Nächste Schritte, priorisiert

| # | Schritt | Aufwand | Warum zuerst |
|---|---|---|---|
| 1 | **Colin antworten**: Modus A/B je Land, BE-Rückfrage, RS-Team-SLA, Preise anmahnen | Mail | blockiert das Preisgespräch mit STP |
| 2 | **DK-Mail an `cvrselvbetjening@erst.dk` senden** (Draft fertig, Menge ergänzen) | Mail | billigster Hebel; klärt vedtægter |
| 3 | **B3 intern entscheiden**: Aggregationsdienst oder Kernprodukt-API? | Entscheidung | bestimmt den Backend-Vorlauf |
| 4 | **Webhooks verdrahten** (`CaseReady`, `DocumentUploaded`) → Ingestion | Sprint | ersetzt Polling, Voraussetzung für alles Asynchrone |
| 5 | **Prod-HK-Fall listen** (nur `GET`, nichts kaufen) | Stunde | Payload nie mit echtem Inhalt gesehen |
| 6 | `vendorDeliverable`-Spalte in die Routing-Datei (§ 5.1) | Tag | verhindert Wiederholung des Widerspruchs |
| 7 | Rechtsformtiefe NL LU CH BE KW (§ 5.2) | mehrere Tage | ist STP für Mitte August zugesagt |
| 8 | Stale `inpi_client.py` löschen/synchronisieren (§ 5.4) | Minuten | scheitert still |

### Sicherheitszustand, der wiederhergestellt werden muss

`FR_DATAINFOGREFFE_API_KEY_PROD` heißt in `betterco_claude_api/.env` derzeit
`…_PROD_DISABLED`, damit kein Codepfad echte Credits ausgeben konnte.
**Zum Bestellen zurückbenennen.** Verifiziert im deaktivierten Zustand:
`DataInfogreffeClient(env='prod').api_key is None`.

Ebenfalls in `betterco-worldwide/.env`: `GB_COMPANIES_HOUSE_USERNAME` / `_PASSWORD` werden von der
API **nicht benutzt** (Auth = Key als Username, leeres Passwort) → entfernen. `INPI_USERNAME` hat
einen anhängenden Tab; der Client `.strip()`t inzwischen, also nur noch unsauber.

---

## 8. Was NICHT im Kundendokument steht — Checkliste vor dem Versand

| Weggelassen | Begründung |
|---|---|
| Anbieternamen (KYC.com, INPI, Companies House, Infogreffe, DataInfogreffe, handelsregister.de, CVR) | Anbieterneutralität ist die tragende Entwurfsentscheidung |
| Zahl der Registeranbindungen, Coverage-Zahlen des Vendors | Rückschluss auf den Anbieter |
| Einkaufspreise für die Vendor-Länder (nur Klassen A–D) | Marge |
| Wort „Aggregation" / Aggregationsschicht | dito |
| Bänder-Nomenklatur Low/Medium/High/Premium | wörtliche Übernahme wäre identifizierend |
| Bug-Historie, Selbsttestzahlen, Dateinamen, Commit-Hashes | irrelevant für den Kunden |
| Der Widerspruch aus § 5.1 als solcher | im Kundendokument sauber als „?" + offener Punkt abgebildet |
| Bug-Historie, Selbsttestzahlen, Dateinamen, Commit-Hashes | irrelevant für den Kunden |

**Bewusst NICHT weggelassen:** dass der französische Registerauszug ohne Bestellschnittstelle
läuft. § 5.3 des Kundendokuments nennt Frankreich „produktiv" — das stimmt für Satzung und
Gesellschafterliste, für den **Kbis** aber nur mit dem Zusatz „manueller Portalprozess". Das
steht jetzt als Fußnote 2 offen im Kundendokument, verbunden mit der Rückfrage nach dem
Mengengerüst (Agendapunkt 7). Begründung: Wir hätten sonst eine Kapazität verkauft, die aus
einem Portal-Login und einem Menschen besteht — und STPs Land 1 ist ausgerechnet Frankreich.
Die Rückfrage nach der Menge ist zugleich die Information, die wir für die Priorisierung des
Playwright-Clients ohnehin brauchen.
