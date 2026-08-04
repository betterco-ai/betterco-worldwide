# Status und offene Punkte — 2026-08-04

*Nachfolger von `STATUS_TODO_2026-07-29.md`. Deckt die Sitzungen vom 30./31. Juli
(Septeo-Termin) und den 4. August (dänischer Direktzugang) ab. Dieses Dokument ist so
geschrieben, dass man von hier aus kalt weiterarbeiten kann.*

---

## 1. Was ausgeliefert wurde

### Septeo-Paket, Termin am 31.07.

| Datei | |
|---|---|
| `STP_DECK_2026-07-31.html` | 24 Folien, offline lauffähig, keine externen Requests |
| `STP_ARCHITEKTUR_PRODUKT_2026-07-31_EXTERN.md` | Kundendokument — keine Anbieternamen, Preisklassen A–D |
| `STP_ARCHITEKTUR_PRODUKT_2026-07-31_INTERN.md` | Anbieter, Vertragssätze, Verkaufspreise, Margen, Widersprüche |

**Der Ausgang des Termins ist hier nicht dokumentiert** — er wurde nach dem Termin nicht
zurückgespielt. Wer weiterarbeitet, sollte ihn zuerst erfragen; mehrere offene Punkte unten
hängen an Entscheidungen, die dort gefallen sein könnten.

### Dänemark — erster neuer Direktkanal seit FR/GB

Zugang produktiv, `dk_cvr_client.py` in `betterco_claude_api` (31 Selbsttests, 20 live,
Commit `67b3413`). Einzelheiten in `registry-access/DK_CVR/NOTIZ.md`.

### Zugangs-Dossiers

`REGISTRY_ACCESS_IT_ES_LU_2026-07-30.md` und `REGISTRY_ACCESS_BE_IL_2026-07-30.md` —
nur Primärquellen, wörtliche Zitate, Fehlliste der nicht erreichbaren Seiten.

---

## 2. Die Befunde, die die Planung umgestoßen haben

**Spanien fällt als Direktkanal aus.** Automatisierter Zugriff ist vertraglich verboten
(§ 4.5, Kündigungsgrund), die Weitergabe an Dritte ebenfalls — **auch unentgeltlich**
(§ 4.4) — und die Aufnahme in eine abfragbare Datenbank einschließlich eigener Mitarbeiter
(§ 6). Im Deck von „aussichtsreich" auf „indirekt" zurückgesetzt.

**Italien ist rechnerisch außer Reichweite.** Nutzbar nur über den Operator-Vertrag
(~13.000 € Aktivierung + ~12.000 €/Jahr, kein Caching, IP-Whitelisting). Schwelle rund
1.070 Fälle im ersten Jahr. Der Selfservice-Zugang **verbietet die Weitergabe**.

**Luxemburg ist kein Portal-Client.** Die AGB verbieten robotisierten Zugriff wörtlich.
Der legitime Weg ist die API zu 5.000 €/Jahr, die es entgegen unserer alten Notiz gibt.
Schwelle rund 114 Fälle im Jahr.

**Israel und Belgien tragen sich ab dem ersten Fall** — keine Fixkosten. IL: Auszug 12 ₪
ohne Konto, **enthält die Gesellschafterliste**. BE: Jahresabschlüsse über ein kostenloses
Behörden-API, Weiterverwendung ausdrücklich erlaubt.

**Die Vertragssätze liegen deutlich unter den Listenpreisen.** Aus dem Order Form
(`09_Finance/2604_KnowYourCustomer/KYCCOM_F1_Final_Docusign.pdf`): Low 10,80 € · Medium
26,70 € · High 54,50 € · Premium 70,50 €, dazu 322 € monatlich. Und es gibt **Home Bands**,
die in keiner öffentlichen Liste stehen: GB **1,70 €**, DE 6,30 €, US 17,35 €. Alle früheren
Ersparnisrechnungen waren zu hoch.

**Die britische Direktanbindung spart nichts.** 1,70 € je Fall. Ihr Wert ist die kostenfreie
Aktualitätsprüfung und die Auflösung der **gültigen** Satzungsfassung — ein Qualitäts-, kein
Kostenargument. Nicht als Kostenargument verkaufen.

---

## 3. Offen — wartet auf Dritte

| Punkt | Bei wem | Seit |
|---|---|---|
| **Zuschläge für Zusatzdokumente** (DK, IL, BE) | Colin Duncan, KYC.com | 27.07., zugesagt „shortly" |
| **Belgien: ist die Constitution Pflicht- oder Zusatzdokument?** | Colin | 27.07., seine eigene Rückfrage, von uns unbeantwortet |
| **Laufzeit und Mengengrenze bei „Via RS Team"** (IL, BE) | Colin | nie gestellt — ohne das kein SLA |
| **Live Monitoring: Freischaltung, Preis, Jurisdiktionen** | Latika Puri | Gmail-Entwurf erstellt, **Sendestatus unbekannt** |
| **DK: UBO-Freischaltung, vedtægter, HTTPS** | Erhvervsstyrelsen | Mail 04.08. gesendet, Routine `trig_01PmPJVisy6ucCM9qGE5D7m3` prüft werktags |
| **Mengengerüst je Markt** | Septeo | Agendapunkt 7 — **die wichtigste offene Eingangsgröße** |
| **Nachweisstufen: braucht Septeo `dokument` vs. `beglaubigt`?** | Septeo | vor dem Einfrieren des Vertrags |
| **Kbis oder RNE-Bescheinigung?** | Septeo | entscheidet über den Preis in ihrem Land 1 |

---

## 4. Offen — bei uns

**31 Änderungsvorschläge für `curation/registry_intelligence.json`** aus den beiden Dossiers,
**bewusst nicht eingespielt**. Sie sind belegt, gehören aber geprüft. Die Listen stehen am Ende
der jeweiligen Dossier-Berichte.

**`vendorDeliverable`-Spalte in der Routing-Datei.** Registerwahrheit und Kanalwahrheit sind
im Datenmodell nicht getrennt — daraus sind an einem Tag zwei falsche Kundenaussagen
entstanden. Ohne diese Spalte wiederholt sich das.

**Rechtsformtiefe NL, LU, CH, BE** — bisher nur die jeweilige Gesellschafterliste erfasst;
Registerauszug und Gesellschaftsvertrag fehlen für alle dortigen Rechtsformen.
**Kuwait: null Zeilen**, gar nichts erhoben. Septeo gegenüber für Mitte August zugesagt.

**Gesellschaftsvertrag IT, ES, IL** — im Register hinterlegt, kein bestätigter Beschaffungsweg.
**NL und CH** sind über den Katalog bestellbar, dort fehlt die Rechtsgrundlage.

**Israel Gesellschafterliste** — Rechtsrecherche sagt Registerauszug, bisheriger Bezug sagt
Jahresmeldung. Als „?" markiert, nicht aufgelöst.

**Provenienz (B3)** — `upload_customer_document` hat kein Metadatenfeld. Hängt an der
unbeantworteten Frage: **Aggregationsdienst oder Kernprodukt-API?** Das entscheidet, ob es ein
Nachmittag oder ein Sprint ist.

**Vermittlungsschicht** — jurisdiktionsagnostisch, gespeist aus `document_kinds_routing.json`.
Vor dem nächsten Direktkanal, sonst wird jeder weitere Markt teurer als der vorige.

**Stale `inpi_client.py`** in diesem Repo trägt weiterhin den Confidentiality-Bug. Kanonisch ist
`betterco_claude_api/inpi_client.py`. Das Duplikat scheitert **still** — es meldet „keine
Dokumente". Löschen oder synchronisieren.

**HK-Prod-Liste ziehen** — ein echter HKCR-Fall, nur `GET`, nichts kaufen. Der Payload wurde
nie mit echtem Inhalt gesehen.

---

## 5. Was beim Arbeiten an den Kundenunterlagen zu beachten ist

**Zahlen nicht tippen.** `scripts/build_customer_tables.py` erzeugt die Tabellen aus
`curation/price_bands.json` und den Kuratierungsdateien nach `docs/generated/`. Der Generator
meldet außerdem Lücken und doppelte Ländercodes — er hat gefunden, dass der Katalog **zwei
HK-Einträge** führt und ein naives Nachschlagen die Dokumentenliste der Steuerbehörde statt des
Gesellschaftsregisters liest.

**Keine Allaussagen ohne vollständige Abdeckung.** „nie", „alle", „nur in N" — an einem Tag
sind daraus drei falsche Kundenaussagen entstanden. Ein Scan über Allwörter gehört vor jeden
Versand.

**Der Überlauftest muss Container prüfen**, nicht nur die Folienhöhe. Die Tabellen sitzen in
`overflow-y: hidden`-Containern; ein Test auf Folienebene gibt falsche Entwarnung. Das ist
dreimal passiert, zuletzt mit abgeschnittenem Hongkong.

**Schreibstandard**: Skill `betterco-writing-style`, seit 30.07. mit **R11** — kein Abstraktum
und kein Land als Subjekt eines Verbs des Denkens, Sprechens oder Kennens. Die Änderung liegt
uncommitted im Marketplace-Repo auf `master`.
