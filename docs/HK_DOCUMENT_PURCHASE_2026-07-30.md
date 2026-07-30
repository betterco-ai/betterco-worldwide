# Memo — Hongkong: der erste dokument-genaue Bestellweg

*Intern. Stand 2026-07-30, Contract verifiziert 2026-07-29 gegen das Prod-Swagger. **Es wurde nichts
gekauft.** Companion: `ARCHITECTURE_AGGREGATION_2026-07-28.md` (Design), `BACKEND_DEV_MEMO.md`
(Gateway-Aufgabe), `STATUS_TODO_2026-07-29.md` N7 (offene Punkte).*

---

## 1. Der Fund in einem Satz

Der Vendor, den wir bisher durchgängig als **case-level** modelliert haben — Case bestellen, nehmen was
im Bündel liegt, kein Dokument-SKU — hat für **Hongkong genau ein Dokument-SKU**: die Einreichungen
eines Falls lassen sich auflisten und **einzeln kaufen**.

## 2. Contract

Verbatim aus dem Prod-Swagger (`/swagger/v2/swagger.json`), Summary des GET:
*„Retrieves the available filings for case with the document statuses, **Works only for HKCR cases**"*
— andere Jurisdiktionen antworten **400**.

| | Aufruf | Kosten |
|---|---|---|
| Auflisten | `GET /v2/DocumentPurchase/{caseCommonId}?refreshList=false` | frei |
| Kaufen | `POST /v2/DocumentPurchase {caseCommonId, registryDocumentId}` → `{message}` | **kostenpflichtig, pro Einreichung** |

Antwort: `{caseDetail:{company:{caseCompanyId, lastRefreshedDate, registryDocuments:{documents:[…]}}}}`,
je Einreichung `{caseDocumentId?, registrydocumentId, name, filingDate, status, category, updateDatetime}`.

## 3. Warum das architektonisch zählt

Unsere Aggregationsschicht stellt nach außen eine **dokument-genaue Anfrage** und bildet sie nach unten
auf das ab, was der jeweilige Kanal kann. Bisher war das für alles außer DE/FR/GB eine Übersetzung
nach unten: „ein Dokument bestellen" wurde zu „einen Case bestellen und hoffen, dass es drin liegt".
Hongkong ist der erste Kanal außerhalb der Direktanbindungen, der **1:1** passt — es gibt eine echte
Dokument-ID, und der Bestellvorgang meint genau ein Dokument.

Konkret schließt das für HK den Punkt, der im STP-Update vom 2026-07-22 offen blieb: *zusätzliche
Dokumente haben weder Preis noch automatischen Bestellweg*. **Der Bestellweg existiert jetzt** — für
eine Jurisdiktion, ohne hinterlegten Preis.

## 4. Was es ausdrücklich **nicht** heißt

- **Nicht verallgemeinerbar.** HKCR-only, sonst 400. Es ist kein verstecktes Feature, das anderswo
  auch ginge — der Vendor bleibt überall sonst case-level.
- **Die HK-Standarddokumente kommen ohnehin mit.** HK CR führt *Memorandum & Articles of Association*
  und *Annual Return (FNAR1)* als **mandatory**; im Sandbox-Bündel (Fall 1000003840, Ubizense Ltd)
  lagen beide bereits drin. Der Kaufweg trägt also für das, was das Bündel **nicht** hat: ältere
  NAR1-Jahrgänge, geänderte Satzungen, Sonderbeschlüsse. Wer ihn für die aktuelle Satzung benutzt,
  zahlt für etwas, das er schon hat.
- **Noch nie mit echtem Inhalt gesehen.** Die v2-Sandbox **stubbt** die Route: 200 für *jeden* Fall
  (auch GB/DK) mit `documents: null`. Die Liste ist nur auf Prod gegen einen echten HKCR-Fall zu
  sehen. Der Payload-Shape stammt aus dem Swagger, nicht aus einer Messung.
- **Preis unbekannt.** Dass pro Einreichung abgerechnet wird, steht fest; die Höhe nicht.

## 5. Zwei Fallen, die still zuschlagen

1. **Schreibweise der ID.** Die **GET-Antwort** nennt sie `registrydocumentId` (**kleines d**), der
   **POST-Body** `registryDocumentId` (**großes D**). Beides ist laut Swagger korrekt — an seiner
   jeweiligen Stelle. Wer die ID mit der POST-Schreibweise ausliest, bekommt stillschweigend `null`.
2. **Doppelkauf.** Eine Einreichung mit gesetzter `caseDocumentId` liegt bereits am Fall — gekauft
   oder mitgeliefert. Sie ist über den normalen Download zu holen und darf **nicht erneut gekauft**
   werden. Ein Retry auf den POST kauft eine zweite Kopie; der Endpunkt ist nicht idempotent.

## 6. Was verdrahtet ist

| Ort | Was |
|---|---|
| `betterco_claude_api/kyc_com_client.py` | `list_document_filings()` (frei, normalisiert, Flag `purchased`), `find_document_filings(kind=…)` (Articles → Gesellschaftsvertrag, NAR1 → Gesellschafterliste, Particulars/CoI → Registerauszug; neueste Einreichung zuerst), `purchase_document(…, confirm=False)` → wirft ohne explizites `confirm=True` |
| `betterco_claude_api/api/routers/kyccom.py` | `GET /kyccom/cases/{id}/filings[?kind=&refresh_list=]`, `POST /kyccom/cases/{id}/filings/{registryDocumentId}/purchase?confirm=true` — `PaidGate` **und** confirm |
| `scripts/build_routing.py` → `curation/document_kinds_routing.json` | HK-Zeilen für Gesellschafterliste/Gesellschaftsvertrag: `order.howToObtain = "document_purchase"` + `order.channel` mit den exakten Aufrufen. Andere Jurisdiktionen unverändert (0 Zeilen betroffen) |
| `docs/BACKEND_DEV_MEMO.md` | Gateway-Aufgabe, vendor-neutral als `orderable-documents` formuliert |
| Skill `knowyourcustomer` | eigener DocumentPurchase-Abschnitt; die alte Einzeile „ist HKCR-only" war korrekt, aber nutzlos knapp |

Zwei Schutzschichten gegen ungewollten Kauf: der Client wirft ohne `confirm=True`, die Route
antwortet ohne `?confirm=true` mit 400 — beides ohne einen einzigen Upstream-Call.

## 7. Offen

1. **Eine Prod-Liste ziehen** — ein echter HK-Fall, nur `GET`, nichts kaufen. Erst danach lohnt UI
   auf dem Payload. (Ein HK-Fall anzulegen kostet; falls schon einer im Prod-Tenant liegt, den nehmen.)
2. **Preis pro Einreichung** beim Vendor erfragen — ohne ihn ist der Bestellweg für STP nicht
   anbietbar, nur ankündbar.
3. **Base vs. additional für HK klären.** Die Evidence-Datei stuft HK-Satzung und NAR1 als
   `additional` ein (Registersicht: neben dem Auszug gesondert zu beschaffen), die Vendor-Matrix
   führt beide als mandatory (Bündelsicht: kommen mit). Beides ist in seiner Sicht richtig, aber die
   Zusammenführung ist noch nicht entschieden. Solange gilt: das `purchased`-Flag ist die Wahrheit
   für den Einzelfall, die Klassifikation bleibt unverändert.
4. **Übertragbarkeit prüfen:** gibt es weitere Register, die pro Einreichung verkaufen und die wir
   bisher als case-level abgebildet haben? HK war es zufällig — gesucht hat danach niemand.
