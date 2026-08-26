# Memo — Preisbänder, Automatisierung und Registerabdeckung, Stand 26.08.2026

**Anlass:** Prüffrage „ist Kuwait wirklich nur 15 € / Klasse A?" im Rahmen der STP-Simulation
(siehe `STP_SIMULATION_2026-08-25.md`). Die Antwort ist ja — der Weg dorthin hat aber drei
Befunde ergeben, die über die Simulation hinausgehen.

---

## 1. Kuwait ist bestätigt

`records.knowyourcustomer.com/coverage`, wörtlich:
**„Kuwait / Kuwait Chamber of Commerce & Industry / US$19.00"** — 19 USD = Low = Klasse A =
15,00 € Verkauf. Deckungsgleich mit `curation/price_bands.json`, der Vertragstabelle im
Order Form und der Klassenliste im Deck.

Der naheliegende Einwand — Kuwait hat keine automatische Suche, kann das der Regelpreis sein? —
trägt nicht: **87 der 139 bepreisten Jurisdiktionen sind nicht automatisiert**, davon 65 im
Low-Band. Das Band bepreist den Vorgang, nicht den Beschaffungsweg. Manuelle Beschaffung steckt
im Bandpreis.

Der `Manual Case` im Order Form (3,50 € Einkauf, kein Verkaufspreis) ist etwas anderes: ein
manuell **erfasster** Fall, keine manuell **beschaffte** Jurisdiktion. Er ersetzt das Band nicht.

---

## 2. Die Preisseite ist umgezogen und hat sich geändert

Alte URLs (`knowyourcustomer.com/products/buy-kyc-report/…`) leiten per 301 auf
**`records.knowyourcustomer.com/pricing`** bzw. **`/coverage`**.

| Band | bisher (30.07.) | jetzt (26.08.) |
|---|---:|---:|
| Low | 18,00 | **19,00 USD** |
| Medium | 43,50 | **49,00 USD** |
| High | 88,00 | **89,00 USD** |
| Premium | 114,00 | **119,00 USD** |

Jurisdiktionen: Low 102 · Medium 34 · High 12 · Premium 1 — zusammen **149** statt 139.

**Für unseren Einkauf ändert das nichts.** Die Sätze stehen im Order Form vom 13.04.2026,
Laufzeit 12 Monate. Die öffentliche Seite ist nur für die **Zuordnung Land → Band** maßgeblich —
und genau die hat sich verschoben.

### Drei Bandwechsel unter den 15 Prioritätsmärkten

| Land | `price_bands.json` | Website 26.08. | Richtung |
|---|---|---|---|
| **Brasilien** | Low (A) | **US$49 = Medium (B)** | teurer |
| **Luxemburg** | High (C) | **US$49 = Medium (B)** | **günstiger** |
| **Israel** | Medium (B) | **US$19 = Low (A)** | **günstiger** |

Unverändert: Kuwait, Japan, Indien, Niederlande, Schweiz, Norwegen = Low (A) · Frankreich =
High (C) · Spanien = Medium (B).

> **Luxemburg von C auf B ist eine gute Nachricht**, die im Deck noch nicht steht: Folie 18
> führt LU als teuerstes Land neben Frankreich. Das stimmt nicht mehr.

**Zu tun:** `curation/price_bands.json` neu ziehen, Deck Folie 15/16/18 nachziehen,
`PRICE_BAND_BY_CODE` im `knowyourcustomer`-Skill mitkorrigieren.

---

## 3. Die USA sind kein Festband

Die Coverage-Seite führt die USA nicht mit einem Bandpreis, sondern mit
**„See USA tab for details. Per state / By state"**. Der USA-Reiter war über die naheliegende
URL nicht erreichbar (404) und ist **noch nicht ausgelesen**.

**Tragweite:** In der STP-Simulation sind **18 der 70 Zeilen US-Gesellschaften**, alle pauschal
mit Klasse B (35,00 €) gerechnet. Wenn die USA je Bundesstaat bepreist werden, ist diese Zahl
nicht belastbar. Vor der nächsten Preiszusage für US-Volumen klären.

---

## 4. Brasilien: „Jucesp Online" — womöglich nur São Paulo

Die Coverage-Seite nennt je Land das Register. Für Brasilien steht dort
**„Jucesp Online"** — das ist die **Junta Comercial do Estado de São Paulo**, eine von 27
Landesregistern.

Falls die Abdeckung tatsächlich auf São Paulo begrenzt ist, betrifft das in der Simulation
unmittelbar:

| Gesellschaft | Sitz | in São Paulo? |
|---|---|---|
| Cacau Show Comércio de Chocolates Ltda. | Itapevi (SP) | ja |
| **Petróleo Brasileiro S.A. (Petrobras)** | Rio de Janeiro | **nein** |
| **Gerdau & Cia** | Porto Alegre | **nein** |
| **BNDESPAR, BNDES, Ministério, Presidência** | Rio / Brasília | **nein** |

Das wäre gravierender als jede Preisfrage: Petrobras ist Basisfirma #15. **Offen, unbedingt
klären.** Unser eigener Eintrag in `curation/registry_intelligence.json` beschreibt Brasilien
korrekt als 27 Juntas Comerciais — die Frage ist, wie viele davon der Vorlieferant anbindet.

---

## 5. Fünf der 15 Prioritätsmärkte haben keine automatische Suche

`GET /v2/Jurisdictions` führt je Land `isautomated`; nur **53 von 253** sind `true`.

| Markt | Klasse | automatisiert |
|---|:--:|---|
| Spanien | B | **nein** |
| Luxemburg | B (neu) | **nein** |
| Israel | A (neu) | **nein** |
| Japan | A | **nein** |
| Kuwait | A | **nein** |

Die übrigen zehn sind automatisiert. In nicht automatisierten Ländern gibt es **keine
Vorabprüfung**: Wir können vor der Bestellung nicht sagen, ob eine Gesellschaft auffindbar ist,
und `search()` antwortet dort mit HTTP 500 statt einer sauberen Fehlermeldung — auch bei
Kontrollsuchen nach Großunternehmen. Siehe `STP_SIMULATION_2026-08-25.md` § 8.

---

## 6. Auswirkung auf die STP-Simulation

Die an STP gegangene Rechnung nennt **995,00 € für 42 Vorgänge**. Mit Brasilien in Klasse B
statt A wären es **1.135,00 €** (7 BR-Zeilen × 20,00 € Differenz).

**Die Mail ist mit 995,00 € herausgegangen** — bewusste Entscheidung („good enough for now",
26.08.). Nachzuziehen, sobald die USA-Frage und die São-Paulo-Frage geklärt sind; dann in einem
Aufwasch korrigieren statt zweimal nachzubessern.

---

## Offene Punkte

1. **USA-Reiter auslesen** — Bandpreis je Bundesstaat. Betrifft 18 der 70 Zeilen der Simulation.
2. **Brasilien-Abdeckung klären** — nur São Paulo (Jucesp) oder alle 27 Juntas? Betrifft
   Petrobras als Basisfirma.
3. **`curation/price_bands.json` neu ziehen** von `records.knowyourcustomer.com/coverage`,
   inklusive der Registernamen je Land — die Seite liefert sie mit.
4. **Deck korrigieren**: Luxemburg ist nicht mehr Klasse C.
5. **Registerart-Spalte im STP-Sheet korrigieren**: Kuwait ist die *Kuwait Chamber of Commerce
   & Industry*, nicht das Ministry of Commerce and Industry.
