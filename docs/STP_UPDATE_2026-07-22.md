# STP update — 2026-07-22 (email draft)

*Merge of the 2026-07-21 memoed draft + sandbox ground-truth. Factual, explanatory, alignment-call
proposal. Now integrates: (a) the "no separate document, but shareholder data in the profile" case, and
(b) the base vs. additional distinction incl. the open point that additional documents currently have no
price and no automatic order path. No provider names / no aggregation. Attachment:
`STP_document_availability_api.pdf`.*

---

Hallo zusammen,

kurz zur Einordnung, worum es geht, dann der Stand und ein Vorschlag zum weiteren Vorgehen.

**Ausgangsfrage.** Ihr möchtet zu einer ausländischen Gesellschaft jeweils die drei Dokumente zuordnen
können, die ihr aus dem deutschen Kontext kennt: Registerauszug, Gesellschafterliste und
Gesellschaftsvertrag/Satzung. Die Schwierigkeit dabei: Jedes Land benennt, führt und veröffentlicht diese
Unterlagen anders – teils gibt es ein direktes Gegenstück, teils nur ein anderes Dokument mit demselben
Inhalt, teils gar keins. Genau diese Zuordnung – pro Land und pro Rechtsform – haben wir jetzt aufgebaut und
an einzelnen Beispielen mit echten Dokumentenabrufen gegengeprüft.

**Warum ein einfacher Kategorie-Filter nicht reicht.** In einem Land heißt das Registerdokument z. B.
„Handelsregisterauszug", in einem anderen „Certificate of Incorporation", in einem dritten gibt es gar keinen
Registerauszug im deutschen Sinn (etwa in den USA – dort nur eine Existenz-/Good-Standing-Bescheinigung). Ein
einzelnes category/type-Kennzeichen bedeutet also je Land etwas anderes; darauf lässt sich keine verlässliche
„Kategorie X = nur Registerdokumente"-Garantie bauen. Belastbar ist stattdessen eine Nachschlage-Zuordnung je
Jurisdiktion und Rechtsform.

**Die drei Dokumentenarten – Grundverfügbarkeit.**

- **Registerauszug:** in den meisten Ländern als Standarddokument vorhanden. Ausnahme USA (nur
  Good-Standing-Bescheinigung).
- **Gesellschaftsvertrag/Satzung:** fast überall erhältlich, aber häufig als *zusätzliches*, separat zu
  beschaffendes Dokument – nicht als Teil des Standardauszugs.
- **Gesellschafterliste:** hängt an der Rechtsform. Bei GmbH-ähnlichen Gesellschaften sind die Eigentümer
  öffentlich im Register; bei AG-ähnlichen Gesellschaften nicht (Aktien sind übertragbar und werden im
  firmeninternen Aktienbuch bzw. bei einer zentralen Verwahrstelle geführt) – wie bei der deutschen AG.

**Entscheidend für eure Umsetzung: *wie* ihr die jeweilige Dokumentenart tatsächlich bekommt.** Pro Fall
(Land × Rechtsform × Dokumentenart) unterscheiden wir vier Ergebnisse – und genau diese Einordnung liefert
auch die Abfrage im Anhang:

1. **Basisdokument** – das Dokument kommt mit dem Standardabruf mit (kein Zusatzschritt, im Case-Preis
   enthalten). Beispiel: österreichische GmbH – die Gesellschafter stehen direkt im Firmenbuchauszug.

2. **Nur als Daten im Profil** – es gibt *kein eigenes Nachweisdokument*, die Angaben stehen aber als **Daten
   im Firmenprofil/Registerauszug**. Beispiel Singapur: der Standardabruf liefert das Firmenprofil, das die
   Gesellschafter enthält – eine separate „Gesellschafterliste" als Dokument gibt es nicht. Ihr bekommt also
   die Information, aber nicht als eigenständiges Nachweisdokument.

3. **Zusätzliches Dokument** – das Dokument existiert im Register, ist aber nicht Teil des Standardabrufs und
   muss separat beschafft werden. Beispiel: französische SARL – die Satzung (statuts) getrennt vom
   Registerauszug. **Wichtig und aktuell noch offen:** für diese zusätzlichen Dokumente haben wir derzeit
   weder einen hinterlegten Preis noch einen automatischen Bestellweg – das müssen wir für die relevanten
   Fälle noch gemeinsam definieren.

4. **Nicht verfügbar** – die Dokumentenart ist aus dem Register nicht belegbar. Beispiel UK: keine
   fortlaufende Gesellschafterliste (die Confirmation Statement / CS01 ist nur eine periodische
   Veränderungsmeldung, keine Bestandsliste).

Der Unterschied zwischen Fall 1/2 (kommt mit dem Standardabruf) und Fall 3 (separat zu beschaffen) ist für
eure Verarbeitung der wichtigste: „grundsätzlich im Register vorhanden" heißt nicht automatisch „kommt im
Abruf als eigene Datei an".

**Anhang.** Beigefügt ist ein Vorschlag für den passenden API-Aufruf: eine kostenlose Nachschlage-Abfrage je
Jurisdiktion × Rechtsform × Dokumentenart. Sie gibt pro Fall genau diese Einordnung zurück (Basisdokument /
nur Daten im Profil / zusätzliches Dokument / nicht verfügbar) samt Hinweisen, ob ein Dokument automatisch
mitkommt oder separat zu beschaffen ist. So könnt ihr die Erwartung pro Fall vorab abfragen, ohne einen
(kostenpflichtigen) Case anzulegen. Auf den Dokument-`name` solltet ihr weiterhin keine Logik bauen – der ist
nicht stabil.

**Umfang und Stand.** Abgedeckt sind derzeit rund 69 Jurisdiktionen mit ihren wichtigsten Rechtsformen,
jeweils anhand des lokalen Gesellschaftsrechts. Der Abgleich mit echten Abrufen ist bisher stichprobenartig
(bislang u. a. GB, HK, SG) und wird schrittweise ausgeweitet.

**Kosten.** Für die im Standardabruf enthaltenen Dokumente (Basisdokumente und die Daten im Profil) gilt
unverändert: nur die Anlage eines Case ist kostenpflichtig; die Zahl der abgerufenen Dokumente ändert daran
nichts. Für die zusätzlich zu beschaffenden Dokumente gibt es – wie oben erwähnt – derzeit noch keinen
hinterlegten Preis und keinen automatischen Bestellweg; das ist ein offener Punkt, den wir gerne mit euch
klären.

**Vorschlag zum weiteren Vorgehen.** Das Thema hat einige Feinheiten, die sich mündlich schneller klären
lassen als per Mail – insbesondere der Umgang mit den zusätzlichen Dokumenten (Preis/Bestellweg). Ich schlage
einen kurzen Abstimmungs-Call (ca. 30 Minuten) vor, in dem wir die Zuordnung und den API-Vorschlag gemeinsam
durchgehen, die Feldnamen/den Endpoint an eure Seite anpassen und die nächsten Schritte festlegen. Björn,
Fabian – passt euch nächste Woche etwas? Schickt mir gern zwei, drei Zeitfenster, dann stelle ich einen
Termin ein.

Herzliche Grüße
Eckhard
