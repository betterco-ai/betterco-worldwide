# Kundentabellen — ERZEUGT, nicht getippt

*Ausgabe von `scripts/build_customer_tables.py`. Jede Zahl unten ist abgeleitet.*
*Nicht von Hand bearbeiten — Aenderungen gehoeren in die Datendateien oder das Skript.*


## A · Anbindungsart je Jurisdiktion (Folien 7 und 17)

Herleitung: *produktiv* und *in Vorbereitung* sind Projektzustand (im Skript benannt).
*Aussichtsreich* wird abgeleitet: `goDirect.verdict` in ['direct_contract', 'direct_good', 'direct_strong'] **und** `documentsViaApi == true`.
Liefert das Register nur Daten per API, bleibt der bisherige Bezug fuer Dokumente noetig —
das zaehlt ausdruecklich **nicht** als Kandidat.

| Markt | Stufe | goDirect | Dokumente per API |
|---|---|---|---|
| Frankreich (FR) | **produktiv** | `direct_strong` | True |
| Italien (IT) | **aussichtsreich** | `direct_good` | True |
| Vereinigtes Königreich (GB) | **produktiv** | `direct_strong` | True |
| Vereinigte Staaten (US) | **kein Direktweg absehbar** | `vendor_only` | False |
| Spanien (ES) | **aussichtsreich** | `direct_contract` | True |
| Dänemark (DK) | **in Vorbereitung** | `direct_strong` | True |
| Niederlande (NL) | **kein Direktweg absehbar** | `direct_data_only` | False |
| Luxemburg (LU) | **kein Direktweg absehbar** | `direct_data_only` | False |
| Schweiz (CH) | **kein Direktweg absehbar** | `direct_data_only` | False |
| Israel (IL) | **kein Direktweg absehbar** | `direct_data_only` | False |
| Japan (JP) | **kein Direktweg absehbar** | `vendor_only` | False |
| Belgien (BE) | **kein Direktweg absehbar** | `direct_data_only` | False |
| Kuwait (KW) | **nicht erhoben** | `—` | None |
| Singapur (SG) | **kein Direktweg absehbar** | `direct_data_only` | False |
| Hongkong (HK) | **kein Direktweg absehbar** | `vendor_only` | False |

- **produktiv** (2): FR, GB
- **in Vorbereitung** (1): DK
- **aussichtsreich** (2): IT, ES
- **kein Direktweg absehbar** (9): US, NL, LU, CH, IL, JP, BE, SG, HK
- **nicht erhoben** (1): KW

Deutschland ist zusaetzlich produktiv, zaehlt aber nicht zu den 15.


## B · Gesellschaftsvertrag im Bezugskatalog (Folien 10/11, Spalte 4)

Herleitung: Treffer auf Satzungs-Stichwoerter in `documentsMandatory` / `documentsNonMandatory` des Katalogs.
**Wichtig:** Das ist die *Kanalwahrheit*. Ob das Register die Satzung haelt, steht in der Evidenzdatei — beides ist getrennt zu lesen.

| Markt | Pflichtdokument | Zusatzdokument | abgeleitet |
|---|---|---|---|
| Frankreich (FR) | Memorandum & Articles of Association | — | **●** |
| Italien (IT) | — | — | **?** |
| Vereinigtes Königreich (GB) | — | Memorandum and Articles of Association | **◐** |
| Vereinigte Staaten (US) | — | — | **?** |
| Spanien (ES) | — | — | **?** |
| Dänemark (DK) | — | Vedtægter (Articles of association) | **◐** |
| Niederlande (NL) | — | Documenten zoals statuten, fusie- ofsplitsingsvoorstellen (Documents such as articles of association, merger or division proposals) | **◐** |
| Luxemburg (LU) | Articles of association | Non-statutory modification of the agents (corrective); Non-statutory modification of the agents | **●** |
| Schweiz (CH) | — | Statutes - certified | **◐** · **beglaubigt** |
| Israel (IL) | — | — | **?** |
| Japan (JP) | — | — | **?** |
| Belgien (BE) | Constitution | — | **●** |
| Kuwait (KW) | — | — | **?** |
| Singapur (SG) | — | — | **?** |
| Hongkong (HK) | Memorandum & Articles of Association | FNAA1 - Notice of Alteration of Company's Articles; Altered Articles of Association; FM2 - Memorandum of Satisfaction or Release of Property from Charge | **●** |

**Lies das nicht blind ab.** Fuer Belgien fuehrt der Katalog *Constitution* als **Pflicht**dokument, waehrend wir es gegenueber dem Anbieter als Zusatzdokument verhandeln. Ein Widerspruch dieser Art ist erst zu klaeren, bevor die Zelle gesetzt wird.


## C · Preisklassen (Folien 15 und 16)

Erfasste Jurisdiktionen: **139**. Verteilung: A=93 · B=33 · C=11 · D=2

Von den 15 Maerkten liegen **13** in den Klassen A und B, **2** darueber.

### Die 15 Maerkte

| Markt | Klasse | Anbindung |
|---|---|---|
| Frankreich | **C** | **direkt** |
| Italien | **B** | indirekt |
| Vereinigtes Königreich | **A** | **direkt** |
| Vereinigte Staaten | **B** | indirekt |
| Spanien | **B** | indirekt |
| Dänemark | **A** | direkt i. V. |
| Niederlande | **A** | indirekt |
| Luxemburg | **C** | indirekt |
| Schweiz | **A** | indirekt |
| Israel | **B** | indirekt |
| Japan | **A** | indirekt |
| Belgien | **A** | indirekt |
| Kuwait | **A** | indirekt |
| Singapur | **A** | indirekt |
| Hongkong | **B** | indirekt |

*Die Klasse beschreibt den Preis der **indirekten** Anbindung. Fuer die Direktlaender gilt sie nicht — dort zaehlen die eigenen Betraege.*

### Alle Jurisdiktionen nach Region und Klasse


**Amerika** (18)

- **A** — Amerikanische Jungferninseln, Argentinien, Brasilien, Chile, Ecuador, Guadeloupe, Kolumbien, Martinique, Mayotte, Mexiko, Panama, Paraguay, Peru, Puerto Rico, Trinidad und Tobago
- **B** — Costa Rica, Kanada, Vereinigte Staaten

**Asien-Pazifik** (39)

- **A** — Aserbaidschan, China, Cookinseln, Französisch-Polynesien, Georgien, Indien, Japan, Kambodscha, Kasachstan, Kirgisistan, Laos, Malediven, Marshallinseln, Myanmar, Nepal, Neuseeland, Papua-Neuguinea, Salomonen, Samoa, Singapur, Südkorea, Taiwan, Thailand, Tonga, Usbekistan, Vanuatu
- **B** — Armenien, Australien, Hongkong, Hongkong (Steuerbehörde), Kokosinseln, Malaysia, Pakistan, Philippinen, Sri Lanka, Vietnam, Weihnachtsinsel
- **C** — Brunei, Indonesien

**Europa** (49)

- **A** — Albanien, Belarus, Belgien, Bosnien und Herzegowina, Bulgarien, Deutschland, Dänemark, Estland, Färöer, Griechenland, Grönland, Irland, Island, Jersey, Kroatien, Lettland, Moldau, Montenegro, Niederlande, Norwegen, Polen, Russland, Schweiz, Serbien, Slowakei, Slowenien, Tschechien, Ukraine, Ungarn, Vereinigtes Königreich
- **B** — Finnland, Gibraltar, Isle of Man, Italien, Liechtenstein, Malta, Nordmazedonien, Rumänien, San Marino, Spanien, Zypern, Åland, Österreich
- **C** — Frankreich, Guernsey, Luxemburg, Monaco, Portugal, Schweden

**Finanz- und Offshore-Plaetze** (8)

- **A** — Curaçao, St. Vincent und die Grenadinen
- **B** — Aruba, Bahamas, Bermuda
- **C** — Belize
- **D** — Britische Jungferninseln, Kaimaninseln

**Naher Osten & Afrika** (25)

- **A** — Angola, Bahrain, Botsuana, Dschibuti, Irak, Iran, Jemen, Jordanien, Katar, Kuwait, Lesotho, Mauritius, Oman, Palästina, Saudi-Arabien, Senegal, Südafrika, Türkei, Vereinigte Arabische Emirate, Äthiopien
- **B** — Israel, Kenia, Tunesien
- **C** — Marokko, Seychellen


### Doppelt vergebene Laendercodes im Katalog

Erster Eintrag wurde verwendet. Wer hier den falschen erwischt, liest die Dokumentenliste eines anderen Registers.

- `HK` — **HK CR** · HK IRD  (verwendet: der erste)
- `PH` — **Philippines - SEC** · Philippines - DTI  (verwendet: der erste)
- `SC` — **Seychelles - Business Register** · Seychelles - FSA  (verwendet: der erste)
- `VN` — **Viet Nam - NBR** · Viet Nam - GDT  (verwendet: der erste)


## D · Selbstpruefung

**Luecken im Datenbestand — Aussagen dazu sind NICHT gedeckt:**

- NL: keine Zeilen fuer REGISTERAUSZUG, GESELLSCHAFTSVERTRAG
- LU: keine Zeilen fuer REGISTERAUSZUG, GESELLSCHAFTSVERTRAG
- CH: keine Zeilen fuer REGISTERAUSZUG, GESELLSCHAFTSVERTRAG
- BE: keine Zeilen fuer REGISTERAUSZUG, GESELLSCHAFTSVERTRAG
- **KW: keine einzige Routenzeile** — jede Aussage ueber KW ist ungedeckt
