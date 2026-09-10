# Memo — wB-Monitor Pre-Process-Test, 20 ausländische Firmen (Stand 10.09.2026)

**Anlass:** Fabian Puls (STP/Septeo) am 09.09.2026, Betreff *„Simulation Dokumentenabfrage
ausländischer Firmen #2"*, Anhang `2026-09-08_Testkundenliste_wB-Monitor_Pre-Process-Test-
ausländische.Firmen.xlsx`. 20 Gesellschaften, 8 Spalten, Kontext § 24c KWG / wB-Monitor.
Verteiler: Fabian Puls, cc Eric Misfeld, Manuel Schneider, Björn Hartenstein.
**Fabian ist 14.–18.09. im Urlaub, Antworten an den gesamten Verteiler.**

Gleiche Methodik wie `STP_SIMULATION_2026-08-25.md`: Registerabgleich je Zeile über die
kostenfreie Suche (keine Fallanlage, keine Kosten), plus Bepreisung und Match Score.

**Kunden-Sheet (bereinigt, ohne Vorlieferantenbezug):**
`1oQp3atZKwGU3lGwN6hJll2mfqM8u3JrOQ8ozmEZMjyc`
**Interne v1 (mit API-Details), umbenannt in „ÜBERHOLT":**
`1PrSRr7weQGETiUu34xLYMnFuLjZcOl1POClRHDQUkus`

> ⚠️ **Der Vorlieferant wird gegenüber STP nicht genannt.** Eckhard hat kyc.com als Quelle
> bewusst aus der Kommunikation entfernt. Kundenseitige Artefakte enthalten weder den
> Produktnamen noch API-Pfade, HTTP-Codes oder `datasource`-Parameter. Dieses Memo ist intern.

---

## 1. Ergebnis in einem Satz

Von 20 Zeilen sind **12 vorab prüfbar**, davon **10 sauber identifiziert** (7 × Score 100,
2 × 95, 1 × 85). **19 Registervorgänge, 465,00 €.** Eine Zeile ist gar kein Registervorgang.

| Score | | Zeilen |
|---:|---|---|
| 100 | Nummer löst auf, Name passt | 1, 2, 3, 4, 5, 6, 18 |
| 95 | Nummer löst auf, Name abweichend | 19, 20 (kyrillisch) |
| 85 | über den Namen gefunden, keine Nummer in der Datei | 7 |
| 70 | Nummer gehört zu einer anderen Gesellschaft | 15 |
| 10 | kein Treffer | 11, 12 |
| 0 | belegt kein Gesellschaftsregister | 16 |
| — | nicht vorab prüfbar | 8, 9, 10, 13, 14, 17 |

Preisklassen live geprüft am 10.09. auf der Coverage-Seite: GB/NL/SK/HU/BG = Low $19 = A,
CA/AT/ES/LU/HK = Medium $49 = B. **Luxemburg bestätigt erneut B statt C** (siehe
`PREISBAENDER_UPDATE_2026-08-26.md` § 2). Bänder jetzt Low 105 · Medium 35 · High 12 ·
Premium 1 = **153** Jurisdiktionen (26.08. waren es 149).

---

## 2. Drei Befunde in der Kundendatei

**2.1 Zeile 15 — Vestigingsnummer statt KvK-Nummer, und sie kollidiert.**
`Sur la Pree B.V.` trägt in der Datei `24175625`. Das ist die **Vestigingsnummer**
(`000024175625`), nicht die KvK-Nummer. Als KvK-Nummer gelesen löst sie auf **eine andere
Gesellschaft** auf: `Barcarolle Holding B.V.`, Oostvoorne. Die richtige KvK-Nummer ist
**54406951** — über den Namen gefunden, unabhängig über KVK/Drimble bestätigt.
Gleiche Fehlerklasse wie GSTIN-statt-CIN in der Augustdatei.

**2.2 Zeile 16 ist ein Verein, kein Unternehmen.**
`Modern Hero Academy` — 0 Treffer auf Nummer und Namen, Kontrollsuche `OMV
Aktiengesellschaft` im selben Lauf positiv. Die Datei nennt als Registerstelle die
**Bezirkshauptmannschaft Baden** (Vereinsbehörde, kein Firmenbuchgericht), und `1545796600`
ist eine **ZVR-Nummer**, keine Firmenbuchnummer (`FN` + Prüfbuchstabe). Vereine stehen im
Zentralen Vereinsregister. **Kein Registervorgang, kein Preis** — analog zu den Tata-Trusts
beim Charity Commissioner.

**2.3 Zwei Gesellschaften sind nicht aktiv — für einen wB-Monitor-Test der Punkt.**
- Zeile 7 `E.M.A. Pharma GmbH` firmiert als **„E.M.A. Pharma GmbH in Liqu."**, FN 292363 x.
- Zeile 19 `NOVA-TEX EOOD` heißt im Register **„НОВА-ТЕКС" ЕООД – в несъстоятелност**
  (in Insolvenz).

Kleinere Punkte: Zeile 10 nennt zwei Rechtsformen gleichzeitig (`S. L.` + `Sociedad
Comanditaria`); Zeile 8 führt mit „38059 / B" Einlage- und Abteilungsnummer statt der
achtstelligen IČO; Zeile 20 transliteriert `З` als `S` statt `Z`; vier Zeilen haben
Adressdrift gegen das Register (Feldhaus nach Staines, die beiden Venlo-Gesellschaften
Venrayseweg 214 statt Hollandlaan 23).

---

## 3. Abdeckungslücken beim Vorlieferanten — das eigentliche Ergebnis

Das Muster ist dasselbe wie bei Brasilien/„Jucesp Online" im Augustmemo: **die
Jurisdiktion ist als `isautomated=true` geführt, aber nur ein Teilregister antwortet.**

| | Befund | Beleg |
|---|---|---|
| **Kanada** | faktisch **nur Ontario** | `datasource=British Columbia` und `Federal Companies` → HTTP 500; ohne `datasource` fällt die Suche auf Ontario zurück und ignoriert die Anfrage. `GET /v2/Jurisdictions` führt 14 kanadische `dataSources`. |
| **USA** | faktisch **nur Delaware** | `datasource=California` → 0 Treffer **auch für die Kontrollsuche „Apple Inc."**; `datasource=Delaware` antwortet normal. |
| **Ungarn** | **kaputt** | `/v2/Companies/search` läuft bei **jeder** Anfrage in den Read-Timeout, inkl. Kontrollsuche „MOL Nyrt". `isautomated=true`. |

Dazu die vier bekannten nicht automatisierten: **SK, ES (×2), LU**.

**Wichtig für die Kundenkommunikation:** Das betrifft die **Vorabprüfung**, nicht die
Beschaffung. Die Matrix führt für BC, Kalifornien und Ungarn sehr wohl Basisdokumente
(BC: Corporate Summary + Certificate of Incorporation + BC Annual Report; CA: Statement of
Information + Initial Filing; HU: Cégkivonat). Das Band bepreist den Vorgang, nicht den
Beschaffungsweg.

**Offen — an Colin zu stellen:**
1. Sind BC/Federal und die übrigen 12 kanadischen `dataSources` überhaupt suchbar, oder ist
   die Liste in `/v2/Jurisdictions` aspirational?
2. Dito USA: 50 `dataSources` gelistet, geantwortet hat nur Delaware.
3. Ungarn-Timeout: temporär oder dauerhaft?
4. **USA-Tab der Coverage-Seite weiterhin nicht erreichbar** (`/coverage/usa` → 404,
   `/pricing` verlinkt ihn nicht). Offenes Item 3 aus dem Augustmemo, jetzt zum zweiten Mal
   relevant. Ohne den Tab sind US-Zeilen nur vorläufig mit Klasse B bepreist.

---

## 4. Fabians drei Fragen — Datenlage

Beantwortet aus `jurisdiction_matrix.json` (`documentsMandatory` / `documentsNonMandatory` /
`shareholders` / `sla`), angereichert um die Rechtsrecherche in
`shareholder-list-equivalence-by-registry`.

**Basispaket vs. Zusatz** — pro Land im Sheet ausgewiesen. Bemerkenswert:
- **LU** liefert **Satzung + Jahresabschluss bereits im Basispaket** (4 Dokumente).
- **HK** liefert **M&A of Association im Basispaket** (6 Dokumente).
- **GB** hat **keinen Registerauszug** — das Basispaket ist eine Filing-Liste
  (New Incorporation, CS01, Annual Return, SH01/03/06, Accounts).
- **ES, HU** haben **keine** Zusatzdokumente.

**Gesellschafterliste / Gesellschaftsvertrag.** Eine eigene Gesellschafterliste nach
§ 40 GmbHG führt **keines der elf Länder**. Aber:
- **AT GmbH**: der Firmenbuchauszug selbst weist die Gesellschafter nach (§ 5 Z 6 FBG).
- **LU S.à r.l.**: der RCS-Auszug selbst weist die Anteilseigner nach.
- Als **strukturierte Daten** kommen Gesellschafter mit dem Auszug in GB, NL, AT, SK, HU,
  LU, HK, BG und CA-BC — nicht in ES, CA-Ontario, US-Kalifornien.
- **NL**: rechtlich veröffentlicht die B.V. nur den **Alleingesellschafter**.
- **GB**: die CS01 ist eine **Änderungsmeldung**, kein vollständiger Nachweis.
- Gesellschaftsvertrag/Satzung als Dokument: LU + HK im Basispaket; AT, NL, GB, BG als
  Zusatzdokument; SK, ES, HU, CA, US nicht.

**Zeiträume** (`sla`): GB/NL/HK 25 Minuten · AT/SK/ES/HU/LU/BG 40 Minuten ·
CA (Ontario, BC) und US (Kalifornien) 24 Stunden.

**Nicht beantwortbar: der Preis je Zusatzdokument.** Der Vorlieferant hat ihn weiterhin
nicht geliefert (siehe `kyc-additional-docs-ordering`). Im Entwurf als Nachlieferung
angekündigt.

---

## 5. Was an STP geht

Antwortentwurf als Gmail-Draft im Thread `1a0856659a35382d`, Struktur analog zur Mail vom
26.08.: was wir gemacht haben → ergänzte Spalten → Ergebnis Matching → Ergebnis Geld →
Fabians drei Fragen → Rückfragen. Positiv gehalten, Vorlieferant nicht genannt.

**Rückfragen an STP im Entwurf:**
1. Zeile 15 — KvK 54406951 bestätigen?
2. Zeile 16 — Verein: soll der wB-Monitor Vereine überhaupt abdecken?
3. Fehlende Kennungen nachreichen: IČO (SK), CIF (ES ×2), Cégjegyzékszám (HU),
   RCS-Nummer (LU), BC Incorporation Number (CA) — damit werden aus 12 prüfbaren 17.

---

## 6. Reproduzieren

Skripte im Scratchpad dieser Session (`rows.py`, `run_search.py`, `pass2.py`,
`build_csv.py`, `build_csv_v2.py`). Suche über `kyc_com_client.KYCComClient.search()` aus
`betterco_claude_api` — kostenfrei, solange kein Fall angelegt wird.
