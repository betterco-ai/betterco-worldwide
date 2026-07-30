# Direktanbindungen — Plan

*Intern, 2026-07-30. Ergänzt `ARCHITECTURE_AGGREGATION_2026-07-28.md` (Entwurf) und
`CONNECTOR_FINDINGS_2026-07-28.md` (Messungen). Die Zugangs-Dossiers zu IT/ES/LU und BE/IL
liegen vor; die Abschnitte 3 und 5 sind danach neu geschrieben.*

---

## 1. Worum es geht

Jeder Vorgang, den wir indirekt beziehen, kostet den Grundpreis seiner Preisklasse. Jeder
Vorgang, den wir direkt beziehen, kostet die amtliche Gebühr — oder nichts.

Der zweite, oft übersehene Effekt: **Bei Direktanbindungen ist die Frage „liegt etwas Neueres
vor?" kostenlos.** Indirekt kostet sie einen ganzen Vorgang. Für Erstprüfungen zählt der
Stückpreis, für **ReKYC** zählt die Prüffrequenz — und dort ist der Unterschied nicht
prozentual, sondern grundsätzlich.

**Nicht das Ziel:** alle Märkte direkt anzubinden. Das lohnt sich nur, wo das Register
Dokumente herausgibt und die Preisklasse hoch genug ist.

---

## 2. Ausgangslage

| | Märkte | Stand |
|---|---|---|
| Direkt, produktiv | DE, FR, GB | Connectoren live, selbstgetestet |
| Direkt, in Vorbereitung | DK | Bauplan liegt, Mail an die Behörde ungesendet |
| Indirekt | 12 der 15 + über 120 weitere | |

**Einschränkung bei Frankreich:** Satzung und Gesellschafterliste laufen über eigene Kanäle,
der **Kbis** aber über einen manuellen Portalvorgang ohne Bestellschnittstelle. FR ist damit
nicht vollständig volumenfähig.

---

## 3. Kandidaten, nach Fixkosten des Zugangs sortiert

*Neu geschrieben am 2026-07-30 nach den Zugangsdossiers. Die erste Fassung dieses Abschnitts
sortierte nach Ersparnis je Fall und stellte Luxemburg als Portal-Client an die Spitze. **Beides
war falsch** — die Dossiers haben drei tragende Annahmen widerlegt (§ 3.1).*

Entscheidend ist nicht die Ersparnis je Fall, sondern die **Fixkosten des Zugangs**. Erst die
Dossiers haben sie belegt, und sie ordnen die Kandidaten neu.

| Rang | Markt | Klasse | Fixkosten Zugang | Kosten je Dokument | Dokumente direkt? |
|---|---|:--:|---|---|---|
| **1** | **Israel** | B | **keine** — kein Konto, keine Landes-ID | Auszug **12 ₪**, Satzung 39 ₪ | ja, alle drei Arten |
| **2** | **Belgien** | A | **keine** für Jahresabschlüsse | **0 €** über das Behörden-API | Jahresabschlüsse ja; Satzung nur über die Notarkammer, lückenhaft |
| **3** | **Luxemburg** | **C** | **5.000 €/Jahr** (API) | Auszug **10,43 €**, hinterlegte Dokumente 0 € | **ja, per API** |
| **4** | **Italien** | B | **~13.000 € einmalig + ~12.000 €/Jahr** | Visura ~1,40 € zzgl. Tarif | ja, per API — weitergabefähig nur im Operator-Vertrag |
| — | **Spanien** | B | — | — | **nein** (§ 3.1) |
| — | Dänemark | A | keine | 0 € | Daten und Jahresberichte ja; **vedtægter offen** |
| — | NL, CH, SG | A/A/A | gering | — | nein, nur Daten |
| — | US, JP, HK | B/A/B | — | — | **keine Schnittstelle** |
| — | KW | A | — | — | **nicht erhoben** |

### 3.1 Was die Dossiers widerlegt haben

**Luxemburg ist kein Portal-Client.** Die Nutzungsbedingungen verbieten automatisierten Zugriff
ausdrücklich: *„l'accès au site internet est strictement limité à une utilisation manuelle et
individuelle. L'accès robotisé y est donc interdit."* Der kostenlose Download bleibt richtig —
aber nur von Hand. Der legitime maschinelle Weg ist die API zu **5.000 € im Jahr**, die es
entgegen unserer Notiz sehr wohl gibt: Art. 22 (2) RGD in der Fassung vom 17.02.2025 nennt
wörtlich *„données publiques inscrites **et des documents publics déposés**"*.

**Italien ist nicht der günstige Einstieg.** Der Selfservice verbietet die Weitergabe
(*„è espressamente vietata la rivendita, la distribuzione informatica e/o la riproduzione"*).
Tragfähig ist nur der Operator-Vertrag: rund 13.000 € Aktivierung, rund 12.000 € im Jahr,
**kein Caching erlaubt**, dedizierte Leitung mit IP-Whitelisting. Das kolportierte
„250-€-Abo" existiert in keiner amtlichen Quelle.

**Spanien fällt aus.** Drei Klauseln, jede für sich ausreichend: automatisierter Zugriff
verboten (§ 4.5, Kündigungsgrund), Weitergabe an Dritte verboten **auch unentgeltlich** (§ 4.4),
und keine Aufnahme in eine abfragbare Datenbank — ausdrücklich **einschließlich eigener
Mitarbeiter** (§ 6). Dazu eine Prüfung des berechtigten Interesses je Anfrage mit
24-Stunden-Fenster. Ein Direktanschluss ist nur denkbar, wenn jede Anfrage **im Namen des
benannten Endkunden** gestellt wird — eine Lesart, die der Betreiber schriftlich bestätigen
müsste.

### 3.2 Ab wann sich ein Fixkosten-Zugang trägt

*Neu gerechnet am 2026-07-30 auf Basis der **vertraglich vereinbarten** Sätze aus dem Order Form
(`09_Finance/2604_KnowYourCustomer/KYCCOM_F1_Final_Docusign.pdf`). Die erste Fassung rechnete mit
den öffentlichen Listenpreisen und war durchgehend zu optimistisch.*

Vertragssätze je Vorgang: Low **10,80 €** · Medium **26,70 €** · High **54,50 €** ·
Premium **70,50 €**. Dazu **322 € monatlich** für Lizenz und Support, unabhängig vom Volumen.
Der Vertrag kennt außerdem **Home Bands**: Ver. Königreich **1,70 €**, Deutschland 6,30 €,
USA 17,35 €.

| Markt | Band | Ersparnis je Fall | Fixkosten | Schwelle |
|---|---|---:|---|---:|
| Israel | Medium | ~23,70 € | keine | **ab dem ersten Fall** |
| Belgien | Low | ~10,80 € | keine | **ab dem ersten Fall** |
| Luxemburg | High | ~44,07 € | 5.000 €/Jahr | **~114 Fälle im Jahr** |
| Italien | Medium | ~23,45 € | 25.000 € im ersten Jahr | **~1.070 Fälle im Jahr 1**, danach ~510 |

**Zwei Folgerungen, die vorher nicht sichtbar waren:**

**Italien ist rechnerisch aus der Reichweite.** Über tausend Fälle im ersten Jahr allein für
Italien ist ein Volumen, das wir nicht unterstellen können. Der Markt bleibt technisch der
sauberste, aber er ist der letzte, der sich trägt — nicht der zweite.

**Die britische Direktanbindung spart nichts.** Das Vereinigte Königreich läuft im Vertrag als
Home Band zu **1,70 €**. Der bereits gebaute Connector rechtfertigt sich über die kostenfreie
Aktualitätsprüfung und darüber, dass er die **gültige** Satzungsfassung auflöst — nicht über den
Stückpreis. Das ist bei der Argumentation gegenüber Septeo zu beachten: Der UK-Kanal ist ein
Qualitäts-, kein Kostenargument.

**Die Entscheidung fällt damit nicht an der Technik, sondern am Mengengerüst.** Ohne erwartete
Fallzahlen je Markt sind die beiden unteren Zeilen nicht entscheidbar. Die beiden oberen tragen
sich ohne jede Mengenannahme.

---

## 4. Was zuerst gebaut werden muss — und nicht ein Land ist

Vor dem zweiten Direktkanal steht eine Aufgabe, die bisher aufgeschoben wurde: die
**jurisdiktionsagnostische Vermittlungsschicht**, gespeist aus `document_kinds_routing.json`.

Heute ist jeder Connector ein eigenes Modul, und die Auswahl trifft ein Mensch. Mit fünf
Kanälen geht das noch, mit zehn nicht mehr. Ohne diese Schicht wird jeder weitere Markt teurer
als der vorige — das Gegenteil des Ziels.

Ebenfalls kanalunabhängig und ebenfalls offen: **OCR bei der Aufnahme**, **Provenienz beim
Schreiben** (Vendor, beide Datumsangaben, Quellreferenz, Kosten) und die **Nachweisstufe** im
Vertrag. Alle drei sind in der Architekturnotiz beschrieben, keine ist gebaut.

---

## 5. Ablauf

*Neu geschrieben nach den Dossiers. Die frühere Reihenfolge — Italien zuerst, Luxemburg als
Portal-Client, Spanien als kommerzieller Strang — ist in allen drei Punkten überholt.*

### Phase 1 — Die beiden Märkte ohne Fixkosten, sofort

**Israel und Belgien** tragen sich ab dem ersten Fall. Beide brauchen keinen Vertrag, keine
Jahresgebühr und keine Verhandlung.

* **Israel:** Auszug für 12 ₪ ohne Konto und ohne Landes-ID, und er **enthält die
  Gesellschafterliste** — genau die Dokumentenart, die uns anderswo fehlt. Offen ist der
  amtlich belegte, aber undokumentierte API-Kanal und die Frage, ob ausländische Karten
  akzeptiert werden.
* **Belgien:** Jahresabschlüsse kostenlos über ein echtes Behörden-API, Weiterverwendung
  ausdrücklich erlaubt. Die Satzung liegt **nicht** im Staatsblatt, sondern bei der Notarkammer;
  deren Abdeckung ist lückenhaft und vor jeder Zusage an 50 bis 100 echten Aufträgen zu messen.

### Phase 2 — Dänemark abschließen

Der Bauplan liegt, die Mail an die Behörde ist geschrieben und ungesendet. Sie klärt die letzte
offene Frage. Kostet nichts.

### Phase 3 — Luxemburg, sobald das Mengengerüst vorliegt

Ab rund 73 Fällen im Jahr trägt sich die API-Gebühr. Luxemburg ist Klasse C und damit der
größte Hebel je Fall — aber die Schwelle ist real und ohne Mengenzahlen nicht zu bewerten.
Der manuelle Gratis-Download bleibt in der Zwischenzeit für Einzelfälle nutzbar.

### Phase 4 — Italien, nur bei hohem Volumen

Die Schwelle liegt im ersten Jahr bei rund 680 Fällen. Das ist eine Volumenentscheidung, keine
technische. **Vor jeder Zusage:** Der Selfservice-Zugang darf die Dokumente nicht weitergeben —
wer Italien über diesen Weg anbindet, baut einen Kanal, der beim ersten Kundendokument
vertragswidrig wird.

### Nicht verfolgen

**Spanien** unter den heutigen Bedingungen (§ 3.1). **US, Japan, Hongkong** mangels
Schnittstelle. **Kuwait** erst nach der ausstehenden Erhebung.

---

## 6. Was die Reihenfolge kippen würde

- **Ein Mengengerüst.** Alle Ersparnisse oben sind **je Vorgang**. Ohne erwartete Fallzahlen je
  Markt ist die Rangfolge eine Vermutung über Volumen. Die Frage steht als Agendapunkt 7 im
  Kundendokument — **die Antwort ist die wichtigste offene Eingangsgröße dieses Plans.**
- **Die Zuschläge für Zusatzdokumente.** Liegen sie hoch, verschieben sich DK, IL und BE nach
  vorn, weil dort der Zuschlag und nicht der Grundpreis der Treiber ist.
- **Live Monitoring.** Wird laufende Änderungsmeldung freigeschaltet und ist sie bezahlbar,
  sinkt der ReKYC-Vorteil der Direktanbindungen. Wird sie es nicht, steigt er.

---

## 7. Risiken

| Risiko | Wirkung | Umgang |
|---|---|---|
| Portalbetreiber untersagt automatisierten Zugriff | LU und der Kbis fallen auf manuelle Bearbeitung zurück | Nutzungsbedingungen **vor** dem Bau lesen, nicht danach |
| Weitergabe an Kunden nicht gedeckt | Dokument ist beschaffbar, aber nicht lieferbar | Lizenzfrage in Phase 0 klären — bei INPI war genau das der Blocker |
| Datenlage stützt sich auf Sekundärquellen | Fehlentscheidung über sechsstellige Beträge | Dossiers akzeptieren nur Primärquellen mit wörtlichem Zitat |
| Jeder Kanal wird einzeln angebaut | Grenzaufwand steigt statt zu sinken | Vermittlungsschicht vor dem zweiten Kanal (§ 4) |

---

## 8. Nächste drei Schritte

1. **Dossiers abwarten und die zwei Einzelfragen entscheiden** (LU-Downloads, BE-Staatsblatt).
2. **DK-Mail senden.** Kostet nichts, klärt die letzte offene DK-Frage.
3. **Mengengerüst bei Septeo erfragen** — ohne es bleibt jede Priorisierung geraten.
