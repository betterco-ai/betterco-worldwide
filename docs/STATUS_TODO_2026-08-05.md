# Status und offene Punkte — 2026-08-05

*Nachfolger von `STATUS_TODO_2026-08-04.md`. Deckt eine kurze Sitzung ab: die Antwort von
Erhvervsstyrelsen prüfen und einarbeiten. **Alles, was hier nicht steht, gilt unverändert
aus dem Vorgängerdokument weiter** — insbesondere die Septeo-Punkte, die Vertragssätze und
die Arbeitsregeln in dessen § 5.*

---

## 1. Was in dieser Sitzung passiert ist

Erhvervsstyrelsen hat am 05.08. um 06:29 auf die Nachfassmail vom 04.08. geantwortet
(Sagsnummer 169988, Charlotte Schierbeck). **Alle drei technischen Fragen sind beantwortet,
und zwar so, dass Dänemark nun als Direktkanal fertig ist — bis auf die Satzung.**

Die Antwort wurde nicht geglaubt, sondern nachgemessen. Zwei der drei Aussagen stimmen,
eine Begründung ist falsch herum. Einzelheiten und Zahlen: `registry-access/DK_CVR/NOTIZ.md`.

| Gefragt | Antwort | Nachgemessen |
|---|---|---|
| UBO-Freischaltung | Index `cvr-re` benutzen | ✅ 601.877 Firmen mit `Reelle ejere`, auf `cvr-permanent` 0 |
| „cvr-re enthält nur die UBO-Information" | — | ❌ **umgekehrt**: voller Firmensatz **plus** UBO; es fehlen nur `penhedRelationer` und `fortroligBeriget` |
| HTTPS | Port **8443** | ✅ trägt `cvr-re`, `cvr-permanent` und `offentliggoerelser`; ohne Auth 401 |
| vedtægter | **nein, kostenpflichtig bestellen** | ✅ auch im Jahresberichtskanal 0 Treffer |

**Commits:** `b1e480d` in `betterco-claude-apis` (Branch `feat/ubo-bridge-graph-docs`),
`5de5117` in `betterco-worldwide` (Branch `document-kinds-evidence`). Beide gepusht.

### Der Fehler, der dabei aufgefallen ist — er betraf auch die legalen Eigentümer

Jeder Attributwert im CVR ist eine **Historie mit Gültigkeitszeitraum, und die Reihenfolge
ist nicht chronologisch.** Der Client las das letzte Listenelement. An CVR 37467057 gemessen:
gemeldet wurden **50 % für eine 2019 beendete Beteiligung**, wo das Register 25 % sagt — vier
Anteile summierten sich auf 150 %. Behoben, drei Selbsttests pinnen es, `validUntil` und
`isCurrent` liegen jetzt am Datensatz.

**Verallgemeinern, nicht als DK-Eigenheit abheften.** Register liefern Historien; wer das
letzte Element nimmt, bekommt irgendeinen Stand, nicht den heutigen. Beim nächsten Connector
zuerst prüfen, ob Werte Perioden tragen — und bei **FR/GB/DE rückblickend nachsehen**.

---

## 2. Was Dänemark jetzt ist

**Die erste Jurisdiktion mit Registerauszug, legalen Eigentümern (Kapital **und** Stimmrecht
getrennt) und wirtschaftlich Berechtigten — direkt, kostenfrei, über TLS.** Ein Abruf gegen
`https://distribution.virk.dk:8443/cvr-re/_search` liefert alles davon zusammen.

Zwei Dinge, die beim Verwenden entscheidend sind:

1. **Ersatz-UBO.** `BETYDELIG_INDFLYDELSE_VIA_ROLLE` heißt: die Geschäftsleitung wurde
   eingetragen, **weil kein echter Eigentümer ermittelbar war**. Ohne Prozente. Der Client
   markiert das als `managementFallback`. Wer es als Eigentum meldet, produziert einen
   falschen KYC-Befund.
2. **UBO ≠ legaler Eigentümer.** An CVR 39052784 sichtbar: legale Eigentümer je 33,33 %
   Kapital mit **0 % Stimmrecht** (B-Anteile), das UBO-Register führt dieselben Personen mit
   **45 %**. Genau deshalb lohnt der getrennte Abruf.

Börsennotierte sind von der UBO-Eintragung befreit und tragen die Organisation gar nicht.
Eine leere Liste heißt deshalb jetzt **„keiner eingetragen"** — eine Antwort, kein blinder Fleck.

---

## 3. Was das für die Planung ändert

**Die Satzung bleibt in DK ein kostenpflichtiges Einzeldokument.** Damit tritt der Fall ein,
vor dem `DK_CVR_CONNECTOR_PLAN.md` § 1 gewarnt hat: der Connector löst das Zuschlagsproblem
**nicht**, er verlagert es. DK sieht bei der Satzung aus wie Frankreich/Kbis.

Für die Zuschlagsfrage bei KYC.com heißt das: **die DK-Position bleibt offen und wird nicht
durch den Direktkanal erledigt.** Colins Zusage von „shortly" (seit 27.07.) steht weiter aus.
Der Direktkanal drückt in DK nur die *Daten*seite auf null, nicht die Dokumentenseite.

---

## 4. Offen — geändert gegenüber dem 04.08.

| Punkt | Stand |
|---|---|
| ~~DK: UBO-Freischaltung, vedtægter, HTTPS~~ | **erledigt 05.08.** |
| **DK-Routine abschalten** | Die werktägliche Prüfroutine `trig_01PmPJVisy6ucCM9qGE5D7m3` wartet auf eine Antwort, die da ist. Läuft vermutlich weiter — **abschalten** (`/schedule`), sonst weckt sie ohne Anlass. In dieser Sitzung nicht geprüft. |
| **DK-Satzung: Preis und Bestellweg** | **neu.** Dass sie kostet, steht fest; was und über welchen Weg, ist nie gefragt worden. Eine Mail an `cvrselvbetjening@erst.dk` — die letzte offene DK-Frage. |
| **Perioden-Prüfung FR/GB/DE** | **neu.** Siehe § 1. Tragen die dortigen Clients dasselbe Problem? |
| **`registry_intelligence.json`, DK-Zeile** | **neu.** Trägt noch „keine UBO". Gehört zu den 31 ohnehin anstehenden Änderungsvorschlägen (§ 4 im Vorgängerdokument) — mit einspielen. |

Alles Übrige aus `STATUS_TODO_2026-08-04.md` § 3 und § 4 steht unverändert: Septeo-Mengengerüst,
Zuschläge bei Colin, Live Monitoring bei Latika, `vendorDeliverable`-Spalte, Rechtsformtiefe
NL/LU/CH/BE, Kuwait, Vermittlungsschicht, stale `inpi_client.py`, HK-Prod-Liste.

**Der Ausgang des Septeo-Termins vom 31.07. ist weiterhin nirgends dokumentiert.** Er ist die
größte Unbekannte in diesem Stapel — zuerst erfragen.

---

## 5. Woran man ansetzt

Wer kalt weitermacht, hat drei sinnvolle Anfänge, in dieser Reihenfolge:

1. **Septeo-Termin nachtragen.** Ohne den arbeitet man an Annahmen.
2. **Die Perioden-Frage bei FR/GB/DE** — eine falsche Prozentzahl in einer KYC-Akte ist
   schlimmer als eine fehlende.
3. **Vermittlungsschicht bauen**, bevor der nächste Direktkanal dazukommt. DK ist der zweite
   Kanal mit eigener Feldsprache; ab dem dritten wird das Nachziehen teurer als das Bauen.
