# Antwortentwurf an Fabian Puls — NICHT VERSANDT

**An:** Fabian.Puls@stp.one · **Cc:** Eric.Misfeld@stp.one, Bjoern.Hartenstein@stp.one
**Betreff:** AW: Simulation Dokumentenabfrage ausländischer Firmen
**Anlage:** eure Datei mit unseren Spalten — Sheet als `.xlsx` exportieren und anhängen

**Fassung 4.** Aufbau: erst was wir gemacht haben, dann die Spalten, dann die Ergebnisse
(Matching und Geld). Preisangaben = Verkaufspreise aus dem Deck, Folie 18.

> **Vor dem Senden zu entscheiden:** Der Satz zu Kuwait und Brasilien sagt, dass wir dort keine
> Registersuche haben — Kuwait ist einer ihrer 15 Prioritätsmärkte. Er ist nötig, weil 22 der
> 70 Zeilen daran hängen. Soll das zuerst zu Colin, dann ersetzen durch „für Kuwait und
> Brasilien liefern wir die Angaben nach".

---

Moin Fabian,

## Was wir gemacht haben

Wir haben eure Datei genommen und jede der 70 Zeilen zweierlei behandelt: bepreist und im
jeweiligen Handelsregister gesucht.

Gesucht haben wir überall dort, wo das Register eine automatische Suche anbietet — Indien,
USA, Frankreich, Niederlande, Schweiz, Norwegen. Für **Kuwait und Brasilien** gibt es keine
Suche; dort ist die Beschaffung ein manueller Vorgang, und wir können eine Gesellschaft vorab
nicht prüfen. Das betrifft 22 der 70 Zeilen.

Gesucht wurde mit eurer Registernummer und, wo die nicht auflöste, mit mehreren Namensvarianten.
Es wurde **nichts bestellt** — Suchen kostet nichts, angelegt wurde kein einziger Vorgang.

## Die Spalten, die wir ergänzt haben

Eure neun Spalten stehen unverändert in eurer Reihenfolge. Danach kommen acht neue:

| Spalte | Bedeutung |
|---|---|
| **Preisklasse** | Preisklasse des Landes. A = 15,00 € · B = 35,00 € · C = 70,00 € je Vorgang, Endpreis. Die Klasse hängt am Land, nicht am Dokument und nicht an der Rechtsform. |
| **Dublette** | `Y`, wenn derselbe Rechtsträger weiter oben in der Datei schon steht. Ein Abruf, ein Preis. |
| **Preis EUR** | Preis dieser Zeile. Leer bei Dubletten und bei Zeilen ohne Registereintrag. |
| **Registerart** | Welches Register für dieses Land zuständig ist. |
| **Match Score** | Wie sicher wir eure Gesellschaft getroffen haben. Skala unten. |
| **Reg-ID (gefunden)** | Die Registernummer, die wir gefunden haben. Nur gefüllt, wenn wir **eure** Gesellschaft getroffen haben — nicht eine ähnlich heißende. |
| **Registrierter Name** | Wie die Gesellschaft im Register tatsächlich heißt. |
| **Kommentar** | Was wir konkret gefunden haben und was zu klären ist. |

**Match Score:**

- **100** — eure Nummer löst auf, der Name passt. Belegt.
- **95** — eure Nummer löst auf, der Name weicht durch eine dokumentierte Umbenennung ab.
- **85** — über den exakten Namen gefunden; eure Nummer ist eine GST-Nummer und damit nicht suchbar.
- **70** — Gesellschaft über den Namen gefunden, eure Nummer löst aber nicht auf. **Bitte
  bestätigen, bevor ihr das als identifiziert behandelt.**
- **40** — die Zeile ist in sich widersprüchlich.
- **10** — kein passender Treffer.
- **0** — gesucht und belegt nicht vorhanden.
- **leer** — nicht prüfbar, weil das Land keine Suche hat (Kuwait, Brasilien).

## Ergebnis Matching

70 Zeilen enthalten **45 verschiedene Rechtsträger**. Davon sind 35 prüfbar, 10 liegen in Kuwait
oder Brasilien.

| Score | | Rechtsträger |
|---:|---|---:|
| 100 / 95 / 85 | sicher identifiziert | **18** |
| 70 | gefunden, eure Nummer weicht ab | 7 |
| 40 | Zeile widersprüchlich | 2 |
| 10 | kein Treffer | 5 |
| 0 | belegt nicht vorhanden | 3 |
| leer | nicht prüfbar | 10 |

**25 der 35 prüfbaren Gesellschaften haben wir gefunden.** Vier Punkte daraus:

- **Drei Bezeichnungen sind veraltet, die Nummern stimmen.** Eure CIN für Tata Motors löst auf;
  die Gesellschaft heißt seit der Abspaltung zum 01.10.2025 *Tata Motors Passenger Vehicles
  Limited*. Blackstone hat 2019 von L.P. auf Inc. umgestellt. Reliance Retail Ventures ist eine
  *Limited*, keine LLP. Deshalb liefern wir den registrierten Namen mit.
- **Bei den indischen Gesellschaftern stehen GST-Nummern statt CIN.** Tata Sons steht bei euch
  mit `27AAACT4060A1ZV`, im Register unter `U99999MH1917PTC000478`. Über eure Nummern findet
  dort keine Suche etwas, auch nicht bei eingetragenen Gesellschaften.
- **Apple lösen wir nicht auf.** Weder die Delaware-Nummer 770141 noch der Name führen zu einem
  Treffer, bei 52 geprüften Namenskandidaten. Der einzige echte Fehlschlag in einem
  automatisierten Register — und euer Beispielfall. Könnt ihr Nummer und Registerstaat prüfen?
- **Zeile 10 ist widersprüchlich.** Sie nennt *Heineken Nederland B.V.*, trägt aber die Adresse
  der *Heineken N.V.* in Amsterdam. Zwei verschiedene Rechtsträger. Welcher ist gemeint?

## Ergebnis Geld

| | Vorgänge | Summe |
|---|---:|---:|
| **eure Datei, so wie wir sie rechnen** | **42** | **995,00 €** |
| ohne Dublettenbereinigung, jede Zeile ein Vorgang | 70 | 1.575,00 € |
| ohne Dubletten, aber inklusive der Trusts | 45 | 1.040,00 € |

Von 70 Zeilen bleiben 42 Vorgänge: 25 Zeilen sind Wiederholungen, 3 sind die Tata-Trusts, die
kein Gesellschaftsregister führt.

Eure beiden Fragen:

- **Apple einzeln: 35,00 €** (USA, Klasse B).
- **Apple mit allen Beteiligungen: 105,00 €.** Über alle sechs Zeilen wären es 150,00 € — drei
  der fünf Gesellschafter sind aber Staat, Zentralbank und Staatsfonds Kuwaits und damit keine
  Registervorgänge.

**Zeitraum:** Niederlande und Schweiz 25 Minuten, Frankreich, Brasilien und Norwegen 40 Minuten,
Kuwait und USA 24 Stunden, Indien 48 Stunden. 24 Zeilen liegen innerhalb einer Stunde vor, die
vollständige Datei in rund zwei Werktagen. Der Ablauf ist asynchron, die Dokumente kommen
einzeln.

**Eine Einschränkung:** Die Preise gelten für Basisdokumente. Der Preis je Vorgang deckt alle
Basisdokumente eines Landes ab; die Zuschläge für Zusatzdokumente liegen uns noch nicht vor —
der offene Punkt von Folie 14. In eurer Datei betrifft das Frankreich, Indien, Brasilien und
Norwegen.

## Drei Fragen

1. Rechnet ihr je Fall oder je Rechtsträger ab? Das ist hier der Unterschied zwischen 1.575 €
   und 1.040 €.
2. Sollen Staaten, Zentralbanken, Staatsfonds und Trusts in eurer Strecke als Vorgang
   auftauchen oder vorher aussteuern?
3. Woher stammt die Datei? Das Muster der Kennungen spricht für einen Datenanbieter. Wenn wir
   das wissen, berücksichtigen wir die Nummernformate beim Abgleich, statt sie als Fehler zu
   behandeln.

Viele Grüße
Eckhard

---

## Änderung gegenüber Fassung 3

Fassung 3 begann mit dem Preis und erklärte die Tabelle nebenbei. Diese Fassung folgt der
Reihenfolge, in der Fabian sie lesen muss: **erst was wir gemacht haben, dann was die Spalten
bedeuten, dann die beiden Ergebnisse — Matching und Geld.** Die Befunde stehen nicht mehr als
eigener Abschnitt, sondern unter dem Matching-Ergebnis, wo sie hingehören.
