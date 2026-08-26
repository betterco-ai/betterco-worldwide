# STP-Simulation „Dokumentenabfrage ausländischer Firmen" — Auswertung und Kalkulation

**Anlass:** E-Mail Fabian Puls (STP Business Information), 25.08.2026 09:25, cc Eric Misfeld,
Björn Hartenstein. Anlage `Ausländische_Firmen.ods`. Antwort gewünscht **bis 26.08. nachmittags**.

**Gefragt:** (1) Was kostet Apple einzelgestellt, (2) was kostet es mit allen Beteiligungen
dahinter, (3) in welchem Zeitraum stünden die Dokumente zur Verfügung.

---

## 1. Was in der Datei steht

69 Datenzeilen: **18 Basisfirmen** (Spalte A nummeriert) und **51 übergeordnete Gesellschafter**.

Die Auswahl ist keine Zufallsliste, sondern ein **6 × 3-Testraster**: sechs Länder, je drei
Rechtsformtypen.

| Land | Kapitalgesellschaft | Personengesellschaft | börsennotiert |
|---|---|---|---|
| Indien | Infosys Technologies Pvt Ltd | Reliance Retail Ventures **LLP** | Tata Motors Ltd |
| USA | Google LLC | Blackstone Group **L.P.** | Apple Inc. |
| Frankreich | Darty Fils SARL | Mireille et Cie **SCS** | L'Oréal S.A. |
| Niederlande | Heineken Nederland B.V. | C&A Nederland **C.V.** | ASML Holding N.V. |
| Brasilien | Cacau Show Ltda. | Gerdau & Cia **Comandita** | Petrobras S.A. |
| Schweiz | Glencore International GmbH | A. Vogel & Co. **KG** | Nestlé S.A. |

Gesellschafter sind **nur bei den sechs börsennotierten** hinterlegt (Tata Motors 9, Google 5,
Apple 5, L'Oréal 12, Petrobras 10, Nestlé 10) — bei Google, das selbst nicht notiert ist, über
die Mutter Alphabet. Bei allen zwölf übrigen Basisfirmen ist die Gesellschafterspalte leer.

**Das ist der eigentliche Test.** Die schwierigen Fälle sind bewusst gesetzt:
Personengesellschaften (in unserer kuratierten Matrix die dünnste Datenlage) und börsennotierte
Gesellschaften (bei denen kein Register der Welt eine Gesellschafterliste führt).

### Weitere Länder, die über die Gesellschafter hereinkommen

Kuwait (15 Zeilen), Norwegen (1 Zeile). **Indien, Brasilien und Norwegen liegen außerhalb der
vereinbarten 15 Prioritätsländer** — bepreisbar sind sie trotzdem, sie stehen in der Bandliste.

---

## 2. Preisklassen der beteiligten Länder

| Land | Klasse | Preis je Vorgang | Zeilen in der Datei |
|---|:--:|---:|---:|
| USA | **B** | 35,00 € | 18 |
| Kuwait | A | 15,00 € | 15 |
| Indien | A | 15,00 € | 12 |
| Schweiz | A | 15,00 € | 10 |
| Brasilien | A | 15,00 € | 7 |
| Frankreich | **C** | 70,00 € | 3 |
| Niederlande | A | 15,00 € | 3 |
| Norwegen | A | 15,00 € | 1 |

Quelle Klassenzuordnung: `curation/price_bands.json`. Klassenpreise: interne Preisliste
Stand 2026-07-30 (`STP_ARCHITEKTUR_PRODUKT_2026-07-31_INTERN.md` § 2).

---

## 3. Kalkulation

### 3.1 Je Basisfirma

| # | Basisfirma | Land | Klasse | einzeln | + Ges. | mit Gesellschaftern |
|---|---|---|:--:|---:|---:|---:|
| 1 | Infosys Technologies Pvt Ltd | IN | A | 15,00 € | 0 | 15,00 € |
| 2 | Reliance Retail Ventures LLP | IN | A | 15,00 € | 0 | 15,00 € |
| 3 | Tata Motors Ltd | IN | A | 15,00 € | 9 | **150,00 €** |
| 4 | Google LLC | US | B | 35,00 € | 5 | **150,00 €** |
| 5 | Blackstone Group L.P. | US | B | 35,00 € | 0 | 35,00 € |
| 6 | **Apple Inc.** | US | B | **35,00 €** | 5 | **150,00 €** |
| 7 | Darty Fils SARL | FR | C | 70,00 € | 0 | 70,00 € |
| 8 | Mireille et Cie SCS | FR | C | 70,00 € | 0 | 70,00 € |
| 9 | L'Oréal S.A. | FR | C | 70,00 € | 12 | **330,00 €** |
| 10 | Heineken Nederland B.V. | NL | A | 15,00 € | 0 | 15,00 € |
| 11 | C&A Nederland C.V. | NL | A | 15,00 € | 0 | 15,00 € |
| 12 | ASML Holding N.V. | NL | A | 15,00 € | 0 | 15,00 € |
| 13 | Cacau Show Ltda. | BR | A | 15,00 € | 0 | 15,00 € |
| 14 | Gerdau & Cia | BR | A | 15,00 € | 0 | 15,00 € |
| 15 | Petrobras S.A. | BR | A | 15,00 € | 10 | **225,00 €** |
| 16 | Glencore International GmbH | CH | A | 15,00 € | 0 | 15,00 € |
| 17 | A. Vogel & Co. KG | CH | A | 15,00 € | 0 | 15,00 € |
| 18 | Nestlé S.A. | CH | A | 15,00 € | 10 | **245,00 €** |

### 3.2 Summen

| Schnitt | Vorgänge | Summe |
|---|---:|---:|
| nur die 18 Basisfirmen, einzeln | 18 | **495,00 €** |
| alle 69 Zeilen, jede Zeile ein Vorgang | 69 | **1.560,00 €** |
| dedupliziert (45 verschiedene Rechtsträger) | 45 | **1.040,00 €** |
| dedupliziert, ohne Staat/Zentralbank/Fonds/Trust | 36 | **905,00 €** |

**Die Spreizung 1.560 € → 905 € ist der eigentliche Kalkulationshebel**, keine Rundungsfrage:

- **24 der 69 Zeilen sind Wiederholungen.** BlackRock, Inc. steht fünfmal in der Datei, die
  Kuwait Investment Authority, die Central Bank of Kuwait und die Kuwait Government je fünfmal,
  Vanguard dreimal, Nestlé zweimal (einmal als Basisfirma, einmal als Gesellschafter von
  L'Oréal). In einem Lauf ist das je **ein** Abruf. Ob STP je Fall oder je Rechtsträger
  abgerechnet bekommt, ist eine Modellfrage, die vor einer Zusage zu klären ist.
- **21 Zeilen (9 verschiedene Rechtsträger) sind keine Handelsregister-Gesellschaften:**
  Kuwait Government, Central Bank of Kuwait, Kuwait Investment Authority, Ministério da Fazenda,
  Presidência da República, Norges Bank, Tata Education Trust, Sir Ratan Tata Trust,
  Sir Dorabji Tata Trust. Für sie existiert kein Registerauszug — weder lieferbar noch sinnvoll
  bepreisbar. Wert dieser Zeilen in der Bruttorechnung: **315,00 €**.
  *Nicht darunter: die BNDES (Banco Nacional de Desenvolvimento Econômico e Social) und die
  BNDESPAR — beide sind eingetragene brasilianische Gesellschaften mit CNPJ und werden bepreist.*

### 3.3 Die beiden konkret gefragten Zahlen

| Frage | Antwort |
|---|---|
| **Apple einzelgestellt** | **35,00 €** (USA, Klasse B), verfügbar in 24 Stunden |
| **Apple mit allen Beteiligungen** | **150,00 €** für alle 6 Zeilen — davon sind 3 der 5 Gesellschafter Staat, Zentralbank und Staatsfonds Kuwaits. Tatsächlich als Registervorgang beschaffbar: **Apple + Vanguard + BlackRock = 105,00 €** |

---

## 4. Der entscheidende Vorbehalt — Gesellschafter börsennotierter Gesellschaften

Die Gesellschafterlisten in der Datei stammen **nicht aus Registern**. Kein Register der sechs
Testländer führt die Aktionäre einer börsennotierten Gesellschaft; die Namen kommen aus Markt-
und Meldedaten (Stimmrechtsmitteilungen, Fondsmeldungen).

Was die Register der acht beteiligten Länder zu Gesellschaftern liefern
(Quelle `jurisdiction_matrix.json`):

| Land | Gesellschafterangaben aus dem Register |
|---|---|
| Brasilien | Name, Adresse, Rolle, Anteilszahl, Steuernummer |
| Frankreich | Name, Adresse, Anteilszahl, Rolle |
| Indien | Name, Adresse, Anteilszahl, Rolle |
| Niederlande | Name, Geburtsdatum/Jurisdiktion, Adresse, Rolle, Anteilszahl |
| Schweiz | Name, Rolle, Anteilszahl |
| Kuwait | Name, Rolle, Nationalität |
| **USA** | **keine** |
| **Norwegen** | **keine** |

Für die USA heißt das: Die fünf Zeilen unter Apple sind über kein US-Register bestätigbar. Wir
können zu jedem genannten Rechtsträger **einen eigenen Vorgang** anlegen und dessen eigene
Registerdokumente liefern — aber die **Beteiligungskette selbst** ist in den USA keine
Dokumentenfrage, sondern eine Datenfrage. Das muss in der Antwort stehen, sonst verkauft man
STP eine Vollständigkeit, die es nicht gibt.

Zweiter Punkt, gleiche Richtung: **Die Kette ist nicht im Voraus bekannt.** In der Simulation
liefert STP die Gesellschafter mit. Im Echtbetrieb ergibt sich Ebene n+1 erst aus dem Ergebnis
von Ebene n — eine Mengen- und damit Preiszusage „inklusive aller Beteiligungen" ist vorab nur
als Schätzung möglich.

---

## 5. Zeitraum

Zugesagte Bearbeitungszeiten je Land (Feld `sla`, `jurisdiction_matrix.json`):

| Land | Zugang | SLA | Zeilen |
|---|---|---|---:|
| Niederlande | automatisiert | **25 Minuten** | 3 |
| Schweiz | automatisiert | **25 Minuten** | 10 |
| Frankreich | hybrid | **40 Minuten** | 3 |
| Brasilien | Registry Services | **40 Minuten** | 7 |
| Norwegen | hybrid | **40 Minuten** | 1 |
| Kuwait | Registry Services | **24 Stunden** | 15 |
| USA | Registry Services | **24 Stunden** (Delaware, Kalifornien) · Wisconsin 10 Arbeitstage | 18 |
| Indien | hybrid | **48 Stunden** | 12 |

**Gesamtaussage:** 24 der 69 Zeilen (NL, CH, FR, BR, NO) liegen **innerhalb einer Stunde** vor,
der Rest binnen **24 bis 48 Stunden**. Die gesamte Datei ist damit in **rund zwei Werktagen**
vollständig. Der Ablauf ist asynchron — es gibt kein Zeitfenster, in dem alles gleichzeitig kommt.

*Das sind die zugesagten Werte des indirekten Bezugswegs, keine gemessenen Latenzen. Für
Frankreich läuft unser Direktbezug (Kbis über Portalvorgang) tendenziell länger, ist dafür
deutlich billiger — siehe § 5.3 des Architekturpapiers.*

---

## 6. Was wir NICHT beantworten können

1. **Zusatzdokumente sind nicht bepreisbar.** Fabian fragt ausdrücklich nach „Basis- **und**
   Zusatzdokumenten". Der Grundpreis deckt die Basisdokumente ab; die Zuschläge für
   Zusatzdokumente liegen uns weiterhin **nicht** vor (angefragt seit Juli, zuletzt 12.08. ohne
   Betrag). Betroffen in dieser Datei: Frankreich (Gesellschaftsvertrag), Indien
   (Gesellschafterliste), Brasilien und Norwegen (Gesellschaftsvertrag).
   → Die Kalkulation gilt **für Basisdokumente**. Das muss so dastehen.
2. **Personengesellschaften.** LLP (IN), L.P. (US), SCS (FR), C.V. (NL), Comandita (BR),
   KG (CH) — genau diese sechs Rechtsformen fehlen in unserer kuratierten Rechtsform-Matrix
   (dort stehen für FR nur SA/SARL/SAS/SNC, für NL nur BV, für CH nur AG/GmbH/Genossenschaft).
   Der Grundpreis gilt je Land, nicht je Rechtsform — der **Preis** steht also. Welche
   Dokumente konkret herauskommen, ist für diese sechs Zeilen ungeprüft.
3. **Was in den USA als „Basisdokument" ankommt**, ist ein Delaware *Status Report* bzw. in
   Kalifornien ein *Statement of Information* — kein Auszug im Sinne eines
   Handelsregisterauszugs. Bei drei US-Basisfirmen und 18 US-Zeilen ist das der wichtigste
   Erwartungsabgleich.
4. **Indien:** Der Katalog führt einen „Registry Extract" als Pflichtdokument. Der Companies
   Act 2013 (s.399) kennt aber kein Auszugsdokument, sondern nur Einsicht und die eingereichten
   Formulare. Was geliefert wird, ist mit hoher Wahrscheinlichkeit ein zusammengestelltes Profil
   — Nachweisstufe `dokument`, nicht `beglaubigt`. **Vor der Antwort zu prüfen.**
5. **Kuwait** hat in unserer Rechtsform-Evidenz **keine einzige Zeile**, obwohl es zu den
   15 Prioritätsländern gehört. Für diese Simulation ohne Folgen (alle KW-Zeilen sind Staat,
   Zentralbank oder Staatsfonds), aber eine offene Lücke.

---

## 7. Entscheidungen zur Antwort (25.08. getroffen)

1. **Beträge werden genannt.** Kein Ankerproblem: Das Deck (`STP_DECK_2026-07-31.html`,
   Folie 18 „Gemeinsamer Business Case") führt Einkauf, Verkauf, Marge und SLA je Markt offen
   aus — Septeo hat die Zahlen bereits. Die Antwort nennt die **Verkaufspreise** 15 / 35 / 70 €.
2. **Servicepauschale wird nicht separat thematisiert.** Der Entwurf verweist stattdessen auf
   das Deck und sagt, die genannten Beträge seien Endpreise je Vorgang. Die Drei-Positionen-
   Formel auf Folie 14 bleibt unangetastet, ist aber bei nächster Gelegenheit zu bereinigen —
   die Verkaufspreise enthalten die Marge bereits.
3. **Abrechnungsmodell je Fall oder je Rechtsträger** (1.560 € gegen 1.040 €) geht als
   Rückfrage an STP. Das ist der größte einzelne Betrag in dieser Kalkulation.

### Weiterhin offen (nicht durch die Antwort erledigt)

- Zuschlagsbeträge für Zusatzdokumente — seit Juli angefragt, zuletzt 12.08. ohne Betrag.
  Steht bereits als offener Punkt auf Folie 14 des Decks.
- Der Indien-Widerspruch aus § 6.4 (Katalog nennt „Registry Extract", Companies Act 2013 s.399
  kennt kein Auszugsdokument). Der Entwurf umgeht die Behauptung; zu klären bleibt sie.
- Kuwait ohne jede Zeile in der Rechtsform-Evidenz (§ 6.5).

---

## 8. Nachtrag 26.08. — Registersuche statt Vermutung

Die Behauptung „kein Register" für neun Rechtsträger war eine **Ableitung aus den Namen**, nicht
geprüft. Da `search()` kostenfrei ist (nur `create_case()` ist abrechnungsrelevant), wurde sie
am 26.08. gegen PROD nachgemessen — jeweils mit Kontrollsuche in derselben Jurisdiktion.

| Prüfobjekt | Ergebnis | Bewertung |
|---|---|---|
| **NORGES BANK** | **937884117, Active** — Treffer über Name **und** über org.nr | Behauptung **widerlegt** |
| *Kontrolle EQUINOR* | 179 Treffer | Suche funktioniert |
| **TATA EDUCATION TRUST** | 0 Treffer | Behauptung **bestätigt** |
| **SIR RATAN TATA TRUST** | 0 Treffer | Behauptung **bestätigt** |
| **SIR DORABJI TATA TRUST** | 0 Treffer | Behauptung **bestätigt** |
| *Kontrolle TATA SONS* | 1 Treffer, CIN U99999MH1917PTC000478 | Suche funktioniert |
| KIA, CBK, Kuwait Government | **HTTP 500** | **nicht prüfbar** |
| Ministério, Presidência, BNDES | **HTTP 500** | **nicht prüfbar** |
| *Kontrolle NATIONAL BANK OF KUWAIT* | HTTP 500 (3 Versuche) | Suche funktioniert **nicht** |
| *Kontrolle PETROLEO BRASILEIRO* | HTTP 500 (3 Versuche) | Suche funktioniert **nicht** |

### Der eigentliche Befund: BR und KW sind nicht automatisiert

`GET /v2/Jurisdictions` führt je Land ein Feld `isautomated`. **53 von 253** sind `True`.

| Land | isautomated |
|---|---|
| FR, DE, IN, NL, NO, CH, GB, US | **True** |
| **Brasilien, Kuwait** | **False** |

Die 500er sind also kein Ausfall, sondern der Normalzustand: In nicht automatisierten
Jurisdiktionen gibt es keine Registersuche, die Beschaffung läuft manuell. Das deckt sich mit
`registryAccess: "Registry Services"` in `jurisdiction_matrix.json`; die USA sind die Ausnahme,
dort trägt `dataSources` die Bundesstaaten.

**Tragweite über diese Simulation hinaus:** **Kuwait ist einer der 15 Prioritätsmärkte.** Dort
ist weder eine Vorabprüfung noch ein Self-Service-Lookup möglich. In dieser Datei betrifft das
**22 der 69 Zeilen** (10 Rechtsträger) — Brasilien 7, Kuwait 15.

### Zweiter Befund: die indischen Registernummern sind GST-Nummern

`TATA SONS PRIVATE LIMITED` steht in Fabians Datei mit `27AAACT4060A1ZV` — einer **GSTIN**. Im
Register läuft die Gesellschaft unter **CIN U99999MH1917PTC000478**. Dasselbe Muster bei allen
indischen Gesellschaftern (`27AAATT9835A1ZF`, `27AAATS0494G2ZE`). Eine Suche über die Nummern
aus der Datei findet dort nichts, auch bei eingetragenen Gesellschaften.

### Korrigierte Kalkulation

Nur die drei Tata-Trusts bleiben ausgenommen — als **geprüfter** Negativbefund. Norges Bank und
die staatlichen Stellen in BR und KW werden bepreist.

| Schnitt | Vorgänge | Summe |
|---|---:|---:|
| alle 69 Zeilen, jede Zeile ein Vorgang | 69 | **1.560,00 €** |
| ohne Dubletten, alle 45 Rechtsträger | 45 | **1.040,00 €** |
| **ohne Dubletten und ohne die drei Trusts** | **42** | **995,00 €** |

*Ersetzt die 905,00 € aus § 3.2 und die 890,00 € aus Fassung 1 des Antwortentwurfs.*

---

## 9. Nachtrag 26.08. nachts — Entity Matching mit Match Score

Letzter Suchlauf über die nicht aufgelösten und die auffälligen Zeilen: je Gesellschaft mehrere
Namensvarianten, **alle** Treffer eingesammelt, danach nach Namensähnlichkeit und Ortstreffer
gerankt statt den ersten Treffer zu nehmen. Ergebnis als Spalte **Match Score** im Sheet.

### Score-Verteilung über die 45 Rechtsträger

| Score | Bedeutung | Anzahl |
|---:|---|---:|
| 100 | Nummer löst auf, Name passt | 11 |
| 95 | Nummer löst auf, Umbenennung dokumentiert | 1 |
| 85 | über exakten Namen gefunden (Nummer ist GSTIN) | 6 |
| 70 | starker Kandidat, Nummer weicht ab | 7 |
| 40 | Zeile in sich widersprüchlich | 2 |
| 10 | kein passender Kandidat | 5 |
| 0 | belegt nicht vorhanden | 3 |
| — | nicht prüfbar (KW, BR) | 10 |

**Von 35 prüfbaren Rechtsträgern sind 25 identifiziert oder als Kandidat aufgelöst.**

### Was der letzte Lauf zusätzlich gefunden hat

| Zeile | Fabians Angabe | Gefunden |
|---|---|---|
| Infosys | CIN U72200KA1981PTC013115 | **INFOSYS LIMITED, L85110KA1981PLC013115** |
| Reliance Retail Ventures **LLP** | LLPIN AAA-1235 | **RELIANCE RETAIL VENTURES LIMITED, U51909MH2006PLC166166** |
| Blackstone Group **L.P.** | 4312543 → THE BATIR, LLC | **BLACKSTONE GROUP INC., 10475679** |
| The Vanguard Group | 604632 (löst nicht auf) | **THE VANGUARD GROUP, INC., 2452336** |
| The Capital Group Companies | 199116300027 (kein DE-Format) | **THE CAPITAL GROUP COMPANIES, INC., 644710** |
| ASML Holding N.V. | KvK 17004321 | **ASML Holding N.V., KvK 17085815** |
| Glencore International **GmbH** | CHE-105.903.625 | **Glencore International AG, CHE-106.909.694** |

### Der Infosys-Befund — Hinweis auf einen Quellenfehler

Fabians CIN `U72200KA1981PTC013115`, real `L85110KA1981PLC013115`. Der **Kern stimmt**
(KA · 1981 · 013115); abweichend sind nur Kategorie-Präfix und die Klasse **PTC statt PLC**.
Eine echte Fremdgesellschaft träfe diesen Kern nicht zufällig. Das deutet auf eine
Transformation in der Quelle hin, nicht auf eine falsche Gesellschaft — dieselbe Richtung wie
die GST-Nummern statt CIN bei allen indischen Gesellschaftern.

### Drei Muster veralteter Bezeichnungen

**Tata Motors** (umbenannt 01.10.2025), **Blackstone Group L.P.** (Umwandlung in Inc. 2019),
**Reliance Retail Ventures LLP** (ist eine Limited). In allen drei Fällen ist die Nummer bzw.
der Kern richtig und der **Name** veraltet — genau das Argument dafür, den *registrierten* Namen
mitzuliefern.

### Apple bleibt der einzige echte Fehlschlag

Weder `770141` noch der Name lösen auf; 52 Namenskandidaten geprüft, keiner passt. In einer
automatisierten Jurisdiktion und ausgerechnet bei Fabians Beispielfall. **Vor der Antwort
klären**, sonst steht die Frage „was kostet Apple" neben einer Zeile, die wir nicht auflösen.
