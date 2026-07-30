# Zugangs-Dossier Unternehmensregister: Belgien (BE) und Israel (IL)

**Stand:** 2026-07-30 · **Zweck:** Entscheidungsgrundlage für Direktanbindung statt Zwischenanbieter
**Dokumentenarten im Fokus:** Registerauszug · Gesellschaftsvertrag/Satzung · Gesellschafterliste

**Quellendisziplin:** Als Primärquelle gilt ausschließlich der Registerbetreiber, die zuständige Behörde, die amtliche Gebührenordnung oder der Gesetzestext. Aggregatoren, Anbieter-Blogs und Kanzlei-Marketingseiten sind als Beleg nicht zugelassen; wo eine Aussage nur dort belegbar war, ist sie als **unbelegt** gekennzeichnet.

---

## Executive Summary — die drei Entscheidungspunkte

1. **Belgien, Kernfrage „Zahlen wir für etwas Öffentliches?" — Antwort: teilweise ja.**
   Für eine BV/SRL wird im Belgischen Staatsblatt **nicht die vollständige Satzung** veröffentlicht, sondern nur ein **Auszug der Gründungsurkunde** (Art. 2:14 Nr. 1 i.V.m. Art. 2:8 § 1 Nr. 2 WVV/CSA); von der Volltextsatzung wird lediglich der **Gegenstand erwähnt** (Art. 2:14 Nr. 2). Dieser Auszug ist als PDF frei und ohne Anmeldung abrufbar.
   Die **vollständige (koordinierte) Satzung** liegt stattdessen in der **Statutendatenbank „Stapor" von Fednot** — ebenfalls **kostenlos, ohne Login**, mit Standardkopie *und* beglaubigter Abschrift, für notarielle Urkunden ab 01.05.2019. Empirisch verifiziert.
   → Ein Aufpreis für „belgische Gründungsurkunde/Satzung" ist bei einer notariell gegründeten BV/SRL ab 2019 sachlich nicht gerechtfertigt, **es sei denn**, der Anbieter liefert die notarielle Ausfertigung aus dem Gerichtsdossier (die ist online nicht öffentlich).
   **Aber:** Stapor ist **nicht lückenlos**. In einer Stichprobe von 6 Unternehmen fehlten 2 — beides kleine, nach 2019 notariell gegründete BV. Vor der Anbieterverhandlung ist die Trefferquote an unserem eigenen Auftragsbestand zu messen (Details in A.6.2).

2. **Belgien, Dokument-API existiert — aber nur bei der Nationalbank.**
   Das NBB-Webservice-Produkt „Authentic Data Query" ist **kostenlos** und liefert **Dokumente** (PDF ab 1999, XBRL ab 2007, JSON ab 2022). KBO liefert nur Daten. Staatsblatt hat keine dokumentierte API, aber stabile, unauthentifizierte GET-URLs.

3. **Gesellschafterliste ist in Belgien beim Register nicht zu bekommen.** Das Aktien-/Anteilsregister wird am Sitz der Gesellschaft geführt und ist nur für Titelinhaber einsehbar (Art. 5:24 WVV/CSA). Der Gründungsauszug nennt nur Gründer und nicht voll eingezahlte Gesellschafter (Art. 2:8 § 2 Nr. 4), nicht den aktuellen Gesellschafterkreis.

4. **Israel, drei Korrekturen an unserem Datenbestand.** Der amtliche Firmenauszug kostet **12 ₪ ohne MwSt.** (nicht „~10 ₪, unbestätigt"), erfordert **kein Konto und keine israelische ID** — und **enthält bereits die Gesellschafterliste**. Die **Satzung (תקנון) ist real bestellbar** (Firmenakte 39 ₪, Einzeldokument 30 ₪) als gescanntes, elektronisch signiertes, gerichtsfestes PDF. Die im Anbieterkatalog geführte *Certificate of Incorporation* ist nach § 10(e) Companies Law ausdrücklich **nicht** die Satzung. Der Begriff „nesach mahshevi" aus unserem Bestand ist **unbelegt** (korrekt: נסח חברה).

---

# TEIL A — BELGIEN

Belgien ist **drei getrennte Quellen**, nicht eine. Die Aufteilung ist der zentrale Befund:

| Quelle | Betreiber | Liefert | Kosten |
|---|---|---|---|
| **KBO/BCE** (Kruispuntbank van Ondernemingen / Banque-Carrefour des Entreprises) | FÖD Wirtschaft (FOD Economie / SPF Économie) | **nur Strukturdaten** (Identifikation, Adresse, Rechtsform, NACE, Status) | Open Data gratis; Public-Search-Webservice kostenpflichtig |
| **Belgisches Staatsblatt, Anlage „Personnes morales / Rechtspersonen"** | FÖD Justiz (SPF Justice / FOD Justitie) | **Auszüge** aus Gründungs- und Änderungsurkunden als PDF | Einsicht gratis |
| **Statutendatenbank „Stapor"** | Fednot — Königliche Föderation des belgischen Notariats (gesetzlich beauftragt, Art. 2:7 § 2 WVV/CSA) | **Volltext der (koordinierten) Satzung**, Standardkopie + beglaubigte Abschrift | gratis |
| **NBB Zentrale Bilanzstelle** (Balanscentrale / Centrale des bilans) | Belgische Nationalbank | Jahresabschlüsse (PDF/XBRL/JSON) | Consult gratis; API-Produkt „Authentic Data" gratis |

---

## A.1 Registerbetreiber und offizielle Portale

### A.1.1 KBO/BCE — Strukturdaten

- **Name:** Kruispuntbank van Ondernemingen / Banque-Carrefour des Entreprises (KBO/BCE)
- **Betreiber:** FÖD Wirtschaft, KMU, Mittelstand und Energie (FOD Economie, K.M.O., Middenstand en Energie / SPF Économie)
- **Portal (Einsicht, ohne Konto):** https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html
- **Open-Data-Portal:** https://kbopub.economie.fgov.be/kbo-open-data
- **Themenseite:** https://economie.fgov.be/en/themes/enterprises/crossroads-bank-enterprises

Die KBO-Detailseite verlinkt selbst auf die anderen drei Quellen — das ist der beste Beleg dafür, dass sie die Dokumente **nicht** selbst hält. Abgerufen am 2026-07-30 für Unternehmensnummer 0403.199.702:

> „Publicaties in het Belgisch Staatsblad" → `https://www.ejustice.just.fgov.be/cgi_tsv/list.pl?language=nl&btw=0403199702&page=1&view_numac=0403199702#SUM`
> „Publicaties van de jaarrekeningen bij de NBB" → `https://consult.cbso.nbb.be/consult-enterprise/0403199702`
> „Databank van statuten en vertegenwoordigingsbevoegdheden (notariële akten)" → `https://statuten.notaris.be/stapor_v1/enterprise/0403199702/statutes`
>
> *(dt.: „Veröffentlichungen im Belgischen Staatsblatt" / „Veröffentlichungen der Jahresabschlüsse bei der NBB" / „Datenbank der Satzungen und Vertretungsbefugnisse (notarielle Urkunden)")*

**Konfidenz: hoch** (eigener Abruf der amtlichen KBO-Public-Search-Seite).

### A.1.2 Belgisches Staatsblatt — Anlage „Personnes morales"

- **Name:** Moniteur belge / Belgisch Staatsblad, **Annexe Personnes morales / Bijlage Rechtspersonen**
- **Betreiber:** FÖD Justiz (Service public fédéral Justice)
- **Portal:** https://www.ejustice.just.fgov.be/cgi_tsv_pub/welcome.pl?language=fr
- **Suchformular:** https://www.ejustice.just.fgov.be/cgi_tsv/rech.pl?language=fr

Zitat der Portalseite (abgerufen 2026-07-30):

> „Les actes des personnes morales (associations, entreprises, formes juridiques spéciales, etc.) paraissent ensemble dans cette annexe du Moniteur belge depuis le 1er juillet 2003."
>
> *dt.: „Die Urkunden juristischer Personen (Vereine, Unternehmen, besondere Rechtsformen usw.) erscheinen seit dem 1. Juli 2003 gemeinsam in dieser Anlage des Belgischen Staatsblatts."*

**Konfidenz: hoch.**

### A.1.3 Statutendatenbank „Stapor" (Fednot)

- **Name:** Statuten en vertegenwoordigingsbevoegdheden / Statuts et pouvoirs de représentation („Stapor")
- **Betreiber:** **Fednot** — Fédération Royale du Notariat belge / Koninklijke Federatie van het Belgisch Notariaat
- **Portal (NL):** https://statuten.notaris.be/stapor_v1/search — **(FR):** https://statuts.notaire.be/stapor_v1/search
- **Gesetzliche Grundlage:** Art. 2:7 § 2 WVV/CSA

Gesetzeszitat (Justel, Code des sociétés et des associations, Art. 2:7 § 2, abgerufen 2026-07-30):

> „Les documents visés aux articles 2:8, 2:9, 2:10 et 2:11, qui sont déposés par voie électronique, sont conservés, ensemble avec des métadonnées, dans un système de base de données électronique qui fait partie du dossier de la personne morale et **qui est géré par la Fédération Royale du Notariat belge**. Sur la base d'un protocole avec FEDNOT, le Service public fédéral Justice cofinancera les coûts de gestion du système de base de données électronique susmentionné."
>
> *dt.: „Die in den Artikeln 2:8, 2:9, 2:10 und 2:11 genannten Dokumente, die elektronisch hinterlegt werden, werden zusammen mit Metadaten in einem elektronischen Datenbanksystem aufbewahrt, das Teil des Dossiers der juristischen Person ist und **von der Königlichen Föderation des belgischen Notariats verwaltet wird**. Auf Grundlage eines Protokolls mit FEDNOT beteiligt sich der Föderale Öffentliche Dienst Justiz an den Verwaltungskosten des genannten elektronischen Datenbanksystems."*

**Konfidenz: hoch** für Betreiber und gesetzliche Grundlage der Datenbank.
**Einschränkung (wichtig, Konfidenz mittel):** Die *aktuelle* Fassung von Art. 2:12 § 2 Abs. 2 beschränkt die **Online-Einsicht in dieses Dossier-Datenbanksystem** auf Richter/Greffiers, KBO-Beamte, Notare und die juristische Person selbst. Das öffentlich zugängliche Stapor-Portal (unten empirisch belegt) ist davon offenbar abzugrenzen — es zeigt nur das Satzungssegment. Die Rechtsgrundlage genau dieses öffentlichen Segments konnte im geltenden Gesetzestext nicht isoliert belegt werden; die tatsächliche freie Zugänglichkeit ist dagegen zweifelsfrei verifiziert.

### A.1.4 NBB Zentrale Bilanzstelle

- **Name:** Balanscentrale / Centrale des bilans / Central Balance Sheet Office
- **Betreiber:** Nationale Bank van België / Banque nationale de Belgique (NBB)
- **Einsichtsportal:** https://consult.cbso.nbb.be/
- **Entwicklerportal:** https://developer.cbso.nbb.be/
- **Info:** https://www.nbb.be/en/central-balance-sheet-office/consultation-data

---

## A.2 Zugang: Registrierung, Vertrag, Nachweise, Auslandsbeschränkungen

| Dienst | Registrierung? | Nachweise | Beschränkung für ausländische Unternehmen | Registrierungs-URL |
|---|---|---|---|---|
| KBO Public Search (Web) | **nein** | – | keine erkennbar | – |
| KBO **Open Data** (CSV) | **ja**, kostenlos | E-Mail-Verifikation, Angabe des Nutzungszwecks, Annahme der Lizenz | keine erkennbar | https://kbopub.economie.fgov.be/kbo-open-data/login |
| KBO **Public Search Web Service** | **ja**, kostenpflichtig | Online-Registrierung + Annahme der Nutzungsbedingungen | keine erkennbar | https://economie.fgov.be/en/themes/enterprises/crossroads-bank-enterprises/services-everyone/public-data-available-reuse/cbe-public-search-web-service |
| Staatsblatt Anlage (Einsicht + PDF) | **nein** | – | keine | – |
| **Stapor** Satzungen | **nein** | – | keine | – |
| NBB **Consult** | **nein** | – | keine | – |
| NBB **Webservices** | **ja** (Vertrag: unterschriebenes Bestellformular + AGB) | Konto + E-Mail-Bestätigung; Primary Key + Request-ID | keine erkennbar | https://developer.cbso.nbb.be/ |

**Belege:**

KBO-Open-Data-Loginseite (https://kbopub.economie.fgov.be/kbo-open-data/login?lang=nl, abgerufen 2026-07-30):

> „De opendatabestanden bevatten informatie over alle actieve geregistreerde entiteiten in KBO. **Deze bestanden zijn gratis te verkrijgen.**"
> „De **Public Search Web Services** bieden de mogelijkheid om informatie van de KBO-toepassing Public Search in uw toepassingen te integreren. **Deze dienst is betalend.**"
>
> *dt.: „Die Open-Data-Dateien enthalten Informationen über alle aktiven registrierten Entitäten in der KBO. **Diese Dateien sind kostenlos erhältlich.** … Die **Public Search Web Services** ermöglichen es, Informationen der KBO-Anwendung Public Search in Ihre Anwendungen einzubinden. **Dieser Dienst ist kostenpflichtig.**"*

KBO-Open-Data-Themenseite (https://economie.fgov.be/nl/themas/ondernemingen/kruispuntbank-van/diensten-voor-iedereen/hergebruik-van-publieke/kruispuntbank-van-0, abgerufen 2026-07-30):

> „Het volledige bestand en de updatebestanden worden dagelijks beschikbaar gesteld" — SFTP-Zugang auf vorherige Anfrage an `kbo-bce-webservice@economie.fgov.be`.
>
> *dt.: „Die Volldatei und die Update-Dateien werden täglich bereitgestellt."*

> **Korrektur gegenüber unserem Stand:** Die Aktualisierung ist **täglich**, nicht monatlich; die Dateien bleiben 31 Tage verfügbar.

NBB-Webservices, AGB Nr. 3.1 (https://www.nbb.be/doc/ba/cbso2022/cnd_n_abin_webservices_v2022_en_v7.pdf):

> „To access the web services, a primary key and a request ID (UUID generated by the customer) are required."
>
> *dt.: „Für den Zugriff auf die Webservices sind ein Primärschlüssel und eine Request-ID (vom Kunden erzeugte UUID) erforderlich."*

**Gesetzliche Einsichtsgarantie** (Art. 2:12 § 2 Abs. 1 WVV/CSA, Justel, abgerufen 2026-07-30):

> „**Toute personne peut prendre connaissance gratuitement des documents déposés** relatifs à une personne morale déterminée et en obtenir, sur demande écrite ou verbale, copie intégrale ou partielle, **sans autre paiement que celui des droits de greffe**. Ces copies sont certifiées conformes à l'original, à moins que le demandeur ne renonce à cette formalité."
>
> *dt.: „**Jede Person kann die hinterlegten Dokumente** zu einer bestimmten juristischen Person **kostenlos einsehen** und auf schriftlichen oder mündlichen Antrag eine vollständige oder teilweise Kopie erhalten, **ohne andere Zahlung als die Kanzleigebühren**. Diese Kopien werden als mit dem Original übereinstimmend beglaubigt, sofern der Antragsteller nicht auf diese Förmlichkeit verzichtet."*

Kein Erfordernis eines belgischen Wohnsitzes, einer belgischen Identifikation oder einer Berufsqualifikation ist in einer der geprüften Primärquellen genannt. **Konfidenz: hoch** für die Existenz des Einsichtsrechts; **mittel** für die Aussage „keine Auslandsbeschränkung", da eine ausdrückliche Negativaussage in keiner Quelle steht (Schluss aus dem Fehlen jeder Bedingung).

---

## A.3 Preise

### A.3.1 Was **nichts** kostet

| Leistung | Preis | Beleg |
|---|---|---|
| KBO Public Search (Web) | 0 € | keine Zahlungs-/Loginschranke beim Abruf 2026-07-30 |
| KBO Open Data (CSV, täglich, Download + SFTP) | **0 €** | Lizenz Art. 7 (Zitat unten) |
| Staatsblatt-Anlage: Publikationsliste + PDF-Abruf | 0 € | Direktabruf ohne Auth, 2026-07-30 |
| Stapor: Standardkopie **und** beglaubigte Abschrift der Satzung | 0 € | Operator-Seite (Zitat unten) + eigener Abruf |
| NBB Consult (Jahresabschlüsse ab 1999, PDF/XBRL/CSV) | 0 € | NBB-Consult-Seite |
| NBB Webservice „Authentic Data Query" / „Extracts" / „Authentic Archive Data" | **0 €** | AGB Nr. 2 (Zitat unten) |

KBO-Open-Data-Lizenz, Artikel 7 (https://economie.fgov.be/sites/default/files/Files/Entreprises/KBO/Licentie-KBO-Open-Data-gebruiksvoorwaarden.pdf):

> „**Artikel 7 – Prijs.** De in het „open data bestand" opgenomen gegevens worden **gratis** ter beschikking gesteld."
>
> *dt.: „**Artikel 7 – Preis.** Die in der Open-Data-Datei enthaltenen Daten werden **kostenlos** zur Verfügung gestellt."*

NBB-Webservices-AGB, Nr. 2 „Subscription price":

> „**„Authentic Data Query", „Authentic Data Extracts" and „Authentic Archive Data" are free of charge.** The price of a subscription to „Improved Data" is **€3,300/year**, even if the customer voluntarily waives the right to download all or part of the files made available by the National Bank pursuant to this Agreement. „Improved Archive Data" is a supplement made available free of charge to paying subscribers to „Improved Data"."
>
> *dt.: „**„Authentic Data Query", „Authentic Data Extracts" und „Authentic Archive Data" sind kostenlos.** Der Preis eines Abonnements für „Improved Data" beträgt **3.300 €/Jahr** … „Improved Archive Data" wird zahlenden „Improved Data"-Abonnenten kostenlos als Ergänzung bereitgestellt."*

MwSt.-Ausweis: in den AGB nicht angegeben. **Als netto zu behandeln** (die NBB stellt eine Rechnung, Art. 3.1). Konfidenz zum MwSt.-Status: **niedrig**.

### A.3.2 Was etwas kostet

| Leistung | Preis | netto/brutto | Beleg-URL |
|---|---|---|---|
| KBO **Public Search Web Service** | **50 €** je Paket à **2.000 Abfragen** | nicht ausgewiesen → als netto behandeln | https://economie.fgov.be/en/themes/enterprises/crossroads-bank-enterprises/services-everyone/public-data-available-reuse/cbe-public-search-web-service |
| NBB **„Improved Data"** | **3.300 €/Jahr** | nicht ausgewiesen → als netto behandeln | https://www.nbb.be/doc/ba/cbso2022/cnd_n_abin_webservices_v2022_en_v7.pdf |
| NBB Kopie eines Jahresabschlusses **1978–1999** per E-Mail | **5 € je Dokument** | nicht ausgewiesen | https://www.nbb.be/en/central-balance-sheet-office/consultation/consult/ordering-copies-annual-accounts |
| NBB Kopie per Post | **0,25 € je Seite**, zzgl. Porto | nicht ausgewiesen | ebd. |

Zitat CBE Public Search Web Service (abgerufen 2026-07-30):

> „Each package entitles you to 2,000 requests (i.e. searches or retrievals) and costs 50 euro."
>
> *dt.: „Jedes Paket berechtigt zu 2.000 Anfragen (Suchen oder Abrufe) und kostet 50 Euro."*

Zitat NBB-Kopienbestellung:

> „by e-mail, with PDF files as attachments, at a cost of **€5 per document**" / „by post, at a cost of **€0.25 per page**, excluding postage"

> **Wichtig:** Diese 5 €/0,25 € betreffen nur Altjahrgänge, die **nicht** in Consult liegen (Consult deckt ab 01.01.1999). Ab 1999 ist der PDF-Download kostenlos.

### A.3.3 Nicht verwechseln: „Frais de publication"

Die auf https://www.ejustice.just.fgov.be/cgi_tsv_pub/page.pl?language=fr&type=p ausgewiesenen Beträge sind **Veröffentlichungsgebühren, die das Unternehmen bei der Hinterlegung zahlt** — nicht Kosten der Einsicht. Ab Hinterlegungen vom 01.03.2026 (abgerufen 2026-07-30):

| Fall | netto | brutto (21 % MwSt.) |
|---|---|---|
| Unternehmen, Gründung, elektronisch | 236,50 € | 286,17 € |
| Unternehmen, Gründung, Papier | 292,90 € | 354,41 € |
| Unternehmen, Änderung | 171,70 € | 207,76 € |
| Vereine (ASBL), Gründung, elektronisch | 146,50 € | 177,27 € |
| Vereine (ASBL), Gründung, Papier | 202,80 € | 245,39 € |
| Vereine (ASBL), Änderung | 137,40 € | 166,25 € |

Für BetterCo als **Abrufer** sind diese Beträge irrelevant. **Konfidenz: hoch** (amtliche Seite des Staatsblatts). Der zugrunde liegende Königliche Erlass wird auf der Seite nicht zitiert — Konfidenz zur Rechtsgrundlage: **niedrig**.

---

## A.4 API — Daten oder Dokumente?

| Dienst | API? | Dokumentation | Auth | **Liefert Dokumente?** |
|---|---|---|---|---|
| KBO Open Data | Bulk-CSV, kein REST | https://economie.fgov.be/sites/default/files/Files/Entreprises/BCE/Cookbook-BCE-Open-Data.pdf | Konto (Download/SFTP) | **nein — nur Daten** |

| KBO Public Search Web Service | ja, SOAP | https://economie.fgov.be/sites/default/files/Files/Entreprises/CBE/Cookbook-CBE-Public-Search-Webservice.pdf | Konto + Abfragepakete | **nein — nur Daten** |
| Staatsblatt Anlage | **keine dokumentierte API** | – | keine | **ja, aber per HTML/PDF-Scraping** |
| Stapor | **keine dokumentierte öffentliche API**; die Web-App nutzt ein undokumentiertes internes REST-Backend unter `/stapor_v1/api/...` | – | keine | **ja (über die Web-App)** |
| **NBB Webservices** | **ja, REST** | https://www.nbb.be/doc/ba/cbso2022/cbso_webservices_technical%20guide_0.94.pdf · Portal https://developer.cbso.nbb.be/ | Primary Key + Request-ID (UUID); Vertrag | **JA — PDF, XBRL, JSON** |

### Feldumfang KBO Open Data — wichtige Lücke

Der amtliche Datenkatalog (https://economie.fgov.be/sites/default/files/Files/Entreprises/BCE/Catalogue-des-donnees-reutilisables-BCE-opendata.pdf, abgerufen 2026-07-30) listet abschließend:

> „**Seules les données actives des entités enregistrées actives sont fournies.**
> I) DONNEES ACCESSIBLES AU NIVEAU DE L'ENTITE ENREGISTREE — Numéro d'entreprise · Type d'entité enregistrée · Dénomination (type, langue, nom) · Siège (rue, numéro, boîte, code postal–commune, pays, complément d'adresse, radiation) · Données de contact · Informations générales (date de début) · **Forme légale** · **Situation juridique: situation juridique, statut** · Activités (catégorie, Nacebel, version, type)
> II) … AU NIVEAU DES SUCCURSALES … III) … AU NIVEAU DES UNITES D'ETABLISSEMENT …"
>
> *dt.: „**Es werden nur die aktiven Daten aktiver registrierter Entitäten bereitgestellt.** … Unternehmensnummer, Entitätstyp, Bezeichnung, Sitz, Kontaktdaten, Beginndatum, **Rechtsform**, **Rechtslage/Status**, Tätigkeiten (Nacebel) … sowie Zweigniederlassungen und Niederlassungseinheiten."*

> **Zwei harte Grenzen, die in unserem Datenbestand fehlen:**
> 1. **Keine Funktionen/Organe.** Geschäftsführer, Verwaltungsratsmitglieder und Vertretungsbefugte sind im Open-Data-Paket **nicht enthalten** — sie erscheinen nur in der Public Search (Web bzw. kostenpflichtiger Webservice) und in den Staatsblatt-Auszügen.
> 2. **Nur aktive Entitäten und nur aktive Daten.** Gelöschte/beendete Unternehmen und historische Werte fehlen.

**Konfidenz: hoch** (amtlicher Katalog, wörtlich ausgewertet).

### Staatsblatt: faktische Maschinenlesbarkeit

Es gibt keine amtlich dokumentierte API. Es gibt aber **stabile, parametrisierte, unauthentifizierte GET-URLs**, die 2026-07-30 verifiziert wurden:

- Publikationsliste je Unternehmen:
  `https://www.ejustice.just.fgov.be/cgi_tsv/list.pl?language=nl&btw=<Unternehmensnummer>&page=1&view_numac=<Unternehmensnummer>`
  Rückgabe für 0403199702: „Lijst (983)" — 983 Veröffentlichungen, HTML-Tabelle mit Datum, Aktentyp (z. B. „STATUTEN (VERTALING, COÖRDINATIE, OVERIGE WIJZIGINGEN)", „ONTSLAGEN - BENOEMINGEN") und direktem PDF-Link.
- PDF-Direktabruf: `https://www.ejustice.just.fgov.be/tsv_pdf/<JJJJ>/<MM>/<TT>/<ID>.pdf`
  Verifiziert: `…/tsv_pdf/2021/01/22/21305176.pdf` — 8 Seiten, **PDF mit Textebene** (kein reiner Scan), Kopf „Copie à publier aux annexes au Moniteur belge après dépôt de l'acte au greffe — Volet B". Kein Login, keine Zahlung.

→ **Direktanbindung ist technisch machbar**, aber als Scraping ohne API-Vertrag und ohne SLA.

### NBB: das einzige echte Dokument-API in Belgien

AGB Nr. 1.1 „Authentic Data Query":

> „This product allows retrieval of the references and **documents** for annual account filings accepted and published by the National Bank for a given legal entity. … • first, the user receives a (list of) reference(s) for a specific legal entity; • next, the **documents (PDF, XBRL, JSON)** linked to these reference(s) are retrieved."
> „**Images (PDFs) of filings** — All images (PDFs) of filings published since 1999."
> „**JSON documents in filings** — … The content of the JSON document is limited to the description of the legal entity, accounting data, and data on participations, **the shareholder structure** and powers of attorney („mandates")."
>
> *dt.: „Dieses Produkt erlaubt den Abruf der Referenzen und **Dokumente** zu Jahresabschluss-Hinterlegungen … • zunächst erhält der Nutzer eine Referenzliste zu einer bestimmten juristischen Person; • anschließend werden die mit diesen Referenzen verknüpften **Dokumente (PDF, XBRL, JSON)** abgerufen. … **Bilder (PDFs) der Hinterlegungen** — alle seit 1999 veröffentlichten. … Der JSON-Inhalt beschränkt sich auf die Beschreibung der juristischen Person, Rechnungslegungsdaten sowie Daten zu Beteiligungen, **der Aktionärsstruktur** und Vollmachten."*

**Technische Eckdaten** (NBB CBSO Webservices Technical Guide v0.94, https://www.nbb.be/doc/ba/cbso2022/cbso_webservices_technical%20guide_0.94.pdf, abgerufen 2026-07-30):

> „The CBSO webservices are exposed via a **REST** interface. … The API Key: Obtained via the Developer portal, **Set into „NBB-CBSO-Subscription-Key" (query parameter or HTTP header)**. The request ID: Client-side generated UUID … **Set into „X-Request-Id"**. The media-type for the returned object … **Set into „Accept"**. … Request timeout is set to 120 sec"

> Basis-URL und Operationen:
> „`https://ws.cbso.nbb.be/authentic/legalEntity/{legalEntityId}/references`" — erlaubte API-Namen „**authentic**", „**extracts**", „**improved**".
> API `authentic`: `/legalEntity/{legalEntityId}/references` · `/deposit/{referenceNumber}/reference` · `/deposit/{referenceNumber}/accountingData`
> API `extracts`: `/batch/{date}/references` · `/batch/{date}/accountingData`

> **PDF-Abruf, wörtliches Beispiel aus dem Leitfaden:**
> „`#-- Get image as PDF for reference 2021-00000148`
> `GET https://ws.cbso.nbb.be/authentic/deposit/2021-00000148/accountingData`
> `X-Request-Id: dc4e66d7-4fff-1223-dc37-1235c36e1e4c`
> `NBB-CBSO-Subscription-Key: 6df61219188728ebb78db5c0cc9aeb2f`
> `Accept: application/pdf`
> The response is **the PDF representation of the deposit**"
>
> *dt.: Das Antwortformat wird über den `Accept`-Header gesteuert; mit `application/pdf` liefert dieselbe Operation das PDF des Jahresabschlusses.*

**Konfidenz: hoch** (amtlicher technischer Leitfaden der NBB).

**Was „shareholder structure" konkret ist — nachgeprüft.** Im amtlichen NBB-Jahresabschlussmodell (Volledig model voor kapitaalvennootschappen, https://www.nbb.be/doc/ba/models/ent/release_2021_nl_model_vol_kapitaalvennootschappen.pdf, abgerufen 2026-07-30) findet sich:

> „Nr. **VOL-kap 6.7.1** — STAAT VAN HET KAPITAAL EN DE AANDEELHOUDERSSTRUCTUUR"
> „Nr. **VOL-kap 6.7.2** — **AANDEELHOUDERSSTRUCTUUR VAN DE VENNOOTSCHAP OP DE DATUM VAN JAARAFSLUITING** — **zoals die blijkt uit de kennisgevingen die de vennootschap heeft ontvangen** overeenkomstig **artikel 7:225 van het Wetboek van vennootschappen en verenigingen**, artikel 14, 4de lid van de wet van 2 mei 2007 op de openbaarmaking van belangrijke deelnemingen of artikel 5 van het koninklijk besluit van 21 augustus 2008 …
> NAAM van de personen die maatschappelijke rechten van de vennootschap in eigendom hebben, met vermelding van het ADRES … en van het ONDERNEMINGSNUMMER … Aangehouden maatschappelijke rechten: Aard, Aantal stemrechten, %"
>
> *dt.: „**AKTIONÄRSSTRUKTUR DER GESELLSCHAFT ZUM BILANZSTICHTAG** — **wie sie sich aus den Mitteilungen ergibt, die die Gesellschaft erhalten hat** gemäß Artikel 7:225 des Gesetzbuchs der Gesellschaften und Vereinigungen, Artikel 14 Abs. 4 des Gesetzes vom 2. Mai 2007 über die Offenlegung bedeutender Beteiligungen oder Artikel 5 des Königlichen Erlasses vom 21. August 2008 … NAME der Personen, die Gesellschaftsrechte halten, mit ADRESSE … und UNTERNEHMENSNUMMER … gehaltene Gesellschaftsrechte: Art, Anzahl Stimmrechte, %."*

> **Bewertung: kein Ersatz für eine Gesellschafterliste.** Die Angabe beruht auf **Mitteilungen** (Transparenzmeldungen), nicht auf dem Anteilsregister; sie erfasst also nur meldepflichtige Beteiligungen, nicht den vollständigen Gesellschafterkreis. Außerdem gehört Rubrik 6.7.2 zum **vollständigen Modell (VOL)** — Klein- und Kleinstunternehmen, die im verkürzten oder Mikromodell hinterlegen, liefern sie gar nicht.
> **Konfidenz: hoch** (amtliches NBB-Modell im Wortlaut).

---

## A.5 Weitergaberecht — geschäftskritisch

### A.5.1 Staatsblatt / Justel — freie kommerzielle Weiterverwendung

„Conditions d'utilisation", Abschnitt III (https://www.ejustice.just.fgov.be/img_2024/pdf/GebruiksvoorwaardenFR.pdf, abgerufen 2026-07-30):

> „**III. CONDITIONS DE REUTILISATION** — Les informations publiées sur ce site internet sont **libres de droits**, sauf mention contraire. Elles peuvent être **réutilisées sans condition à des fins privées, associatives, scientifiques et commerciales**. Toutefois, les autorités fédérales recommandent de mentionner la source et la date des informations réutilisées."
>
> *dt.: „**III. WIEDERVERWENDUNGSBEDINGUNGEN** — Die auf dieser Website veröffentlichten Informationen sind, soweit nicht anders angegeben, **rechtefrei**. Sie können **ohne Bedingungen zu privaten, vereinsbezogenen, wissenschaftlichen und kommerziellen Zwecken wiederverwendet** werden. Die Bundesbehörden empfehlen jedoch, Quelle und Datum der wiederverwendeten Informationen anzugeben."*

→ **Weitergabe eines aus dem Staatsblatt bezogenen PDF an einen Kunden ist zulässig**, inklusive kommerziell. Quellen- und Datumsangabe wird empfohlen, ist nicht zwingend.
**Konfidenz: hoch.**

### A.5.2 KBO Open Data — zulässig, aber mit vier harten Auflagen

Lizenz KBO Open Data (Zitate, abgerufen 2026-07-30):

> „2.2 De licentienemer **mag de persoonsgegevens niet gebruiken voor direct-marketing doeleinden** …"
> „2.3 De licentienemer **mag de gegevens niet hergebruiken voor een ander doeleinde dan hetgene vermeld werd tijdens zijn inschrijving** als gebruiker van de bestanden „opendata"."
> „2.7 De licentienemer verbindt zich ertoe dat **de gegevens ongewijzigd blijven en hun zin behouden**."
> „2.8 In het kader van het hergebruik verbindt de licentienemer zich ertoe **de bron en de datum van de update van de gegevens te vermelden** …"
> „2.9 De licentienemer neemt alle nodige technische, organisatorische en juridische maatregelen om de naleving van de overeenkomst te waarborgen of te doen waarborgen, **ook door zijn personeel en klanten**."
> „**Artikel 11 – Overdraagbaarheid en onderaanneming.** De rechten en verplichtingen die voortvloeien uit de overeenkomst **kunnen geheel noch gedeeltelijk aan een derde worden afgestaan of in onderaanneming worden gegeven**."
>
> *dt.: „2.2 Der Lizenznehmer **darf die personenbezogenen Daten nicht zu Direktmarketingzwecken verwenden**. — 2.3 Der Lizenznehmer **darf die Daten nicht zu einem anderen als dem bei der Registrierung angegebenen Zweck wiederverwenden**. — 2.7 Der Lizenznehmer verpflichtet sich, dass **die Daten unverändert bleiben und ihren Sinn behalten**. — 2.8 Im Rahmen der Wiederverwendung verpflichtet sich der Lizenznehmer, **Quelle und Aktualisierungsdatum der Daten anzugeben**. — 2.9 Der Lizenznehmer trifft alle erforderlichen technischen, organisatorischen und rechtlichen Maßnahmen, um die Einhaltung der Vereinbarung zu gewährleisten oder gewährleisten zu lassen, **auch durch sein Personal und seine Kunden**. — Art. 11: Die Rechte und Pflichten aus der Vereinbarung **können weder ganz noch teilweise an einen Dritten abgetreten oder unterbeauftragt werden**."*

**Lesart für BetterCo:**
- Art. 2.9 („ook door zijn personeel en klanten") setzt voraus, dass Daten an Kunden gelangen — die **Weitergabe von KBO-Daten an Kunden ist also zulässig**, BetterCo muss aber die Lizenzeinhaltung bis zum Kunden durchstellen (Direktmarketing-Verbot, Unveränderlichkeit, Quellenangabe).
- Art. 11 verbietet die Abtretung/Unterbeauftragung **des Lizenzverhältnisses**, nicht die Weitergabe der Daten.
- Art. 2.3 ist die schärfste Auflage: **Der bei der Registrierung angegebene Zweck bindet.** Bei der Registrierung muss der Zweck „Weitergabe an Kunden im Rahmen von KYC-/Onboarding-Dienstleistungen" ausdrücklich benannt werden, sonst ist die Weitergabe lizenzwidrig.

**Konfidenz: hoch** für die Zitate; **mittel** für die Auslegung (Art. 2.9 ist ein Indiz, keine ausdrückliche Weitergabeerlaubnis).

### A.5.3 NBB Webservices — ausdrücklich erlaubt

AGB Nr. 5 „Restrictions on use":

> „Customers **may not transfer their access rights** to the National Bank's server **to a third party**, whether in return for payment or free of charge, on a temporary or permanent basis. **Customers may use annual accounts data downloaded from the National Bank's server free of charge and without limitation, unless provided otherwise by law.**"
>
> *dt.: „Kunden **dürfen ihre Zugriffsrechte** auf den Server der Nationalbank **nicht an Dritte übertragen**, weder entgeltlich noch unentgeltlich, weder vorübergehend noch dauerhaft. **Kunden dürfen die vom Server der Nationalbank heruntergeladenen Jahresabschlussdaten kostenlos und ohne Einschränkung verwenden**, sofern gesetzlich nichts anderes bestimmt ist."*

→ **Die heruntergeladenen Dokumente dürfen ohne Einschränkung verwendet — also auch an Kunden weitergegeben — werden.** Verboten ist nur die Weitergabe des **Zugangs** (Schlüssel/Account).
**Konfidenz: hoch.**

### A.5.4 NBB Consult — Massenabruf untersagt

Nutzungsbedingungen Consult (https://www.nbb.be/en/central-balance-sheet-office/consultation/consult/terms-use):

> „**The application is not intended for the systematic - or mass - consultation or downloading of files.**" — „The National Bank reserves the right to block access to the application without prior notice to any user who compromises its proper functioning."
>
> *dt.: „**Die Anwendung ist nicht für die systematische oder massenhafte Einsicht oder das massenhafte Herunterladen von Dateien bestimmt.**"*

→ Für Volumen ist **nicht** Consult zu scrapen, sondern das (kostenlose) Webservice-Produkt zu abonnieren. **Konfidenz: hoch.**

### A.5.5 Stapor — Weitergaberecht **nicht belegt**

Auf dem Stapor-Portal war beim Abruf am 2026-07-30 **keine Nutzungs-/Lizenzbedingung** sichtbar (nur ein Cookie-Banner und eine Cookie-Richtlinie). Eine Regelung zur Weitergabe der abgerufenen Satzungs-PDFs an Dritte wurde **nicht gefunden**.
**Vergeblich gesucht:** `statuten.notaris.be` (Fußzeile, Cookie-Richtlinie), `statuts.notaire.be`, `notaire.be` Satzungsseite, WVV/CSA Art. 2:7 und 2:12 (regeln Einsicht, nicht Weiterverbreitung).
**Konfidenz: niedrig.** → **Offener Punkt, vor produktivem Einsatz bei Fednot schriftlich klären.** Argumentativ spricht Art. 2:12 § 2 WVV (jedermann darf einsehen und Kopien erhalten) dafür, dass die Dokumente öffentlich sind; eine ausdrückliche Weitergabeerlaubnis ist das nicht.

---

## A.6 Die drei Dokumentenarten — belgische Realität

### A.6.1 Registerauszug

Es gibt in Belgien **kein einheitliches „Registerauszugs"-Dokument** wie den deutschen Handelsregisterauszug. Was es gibt:

| Ersatz | Quelle | Kosten | Form |
|---|---|---|---|
| KBO-Public-Search-Detailseite (Identifikation, Adresse, Rechtsform, NACE, Status, Funktionen) | KBO | 0 € | HTML, druckbar |
| Auszug der Gründungsurkunde („extrait de l'acte constitutif") | Staatsblatt Anlage | 0 € | PDF mit Textebene |
| Chronologische Liste aller Veröffentlichungen | Staatsblatt Anlage (`list.pl`) | 0 € | HTML + PDF-Links |

Inhalt des Gründungsauszugs, Art. 2:8 § 2 WVV/CSA:

> „L'extrait de l'acte constitutif … contient: 1° **la forme légale de la société, sa dénomination** et l'indication de la région dans laquelle le siège de la société est établi; 2° la désignation précise de **l'adresse à laquelle le siège** de la société est établi …; 3° **la durée** de la société lorsqu'elle n'est pas illimitée; 4° les **nom, prénom et domicile des associés solidaires, des fondateurs et des associés ou actionnaires qui n'ont pas encore libéré leur apport** …; 5° le cas échéant, **le montant du capital** et le montant du capital autorisé; 6° **les apports des fondateurs et des souscripteurs** …"
>
> *dt.: „Der Auszug der Gründungsurkunde … enthält: 1° **die Rechtsform der Gesellschaft, ihre Bezeichnung** und die Angabe der Region des Sitzes; 2° die genaue Bezeichnung **der Anschrift des Sitzes**; 3° **die Dauer** der Gesellschaft, wenn sie nicht unbegrenzt ist; 4° **Name, Vorname und Wohnsitz der solidarisch haftenden Gesellschafter, der Gründer und der Gesellschafter oder Aktionäre, die ihre Einlage noch nicht eingezahlt haben**; 5° gegebenenfalls **die Höhe des Kapitals** und des genehmigten Kapitals; 6° **die Einlagen der Gründer und Zeichner** …"*

**Konfidenz: hoch.**

### A.6.2 Gesellschaftsvertrag / Satzung — **der entscheidende Befund**

**Für Gesellschaften (BV/SRL, NV/SA) wird die Volltextsatzung im Staatsblatt NICHT veröffentlicht.**

Art. 2:14 WVV/CSA (Justel, abgerufen 2026-07-30):

> „**Sont publiés pour les sociétés:** 1° les extraits, déclarations et documents visés à l'article 2:8, § 1er, **2°**, 5°, 6°, 7°, 8° et 10°, a), et § 3; 2° **la mention de l'objet des documents visés à l'article 2:8, § 1er, 4°** et 10°, b); 3° l'objet des documents modificatifs de l'acte constitutif qui ne doivent pas être publiés par extrait; …"
>
> *dt.: „**Für Gesellschaften werden veröffentlicht:** 1° die in Artikel 2:8 § 1 Nr. **2**, 5, 6, 7, 8 und 10 a) sowie § 3 genannten Auszüge, Erklärungen und Dokumente; 2° **die Erwähnung des Gegenstands der in Artikel 2:8 § 1 Nr. 4 genannten Dokumente** …"*

Und Art. 2:8 § 1 WVV/CSA definiert:

> „2° **l'extrait de l'acte constitutif** visé au paragraphe 2;
> 4° **la première version du texte des statuts** ainsi que l'acte constitutif, et **le texte coordonné de ces statuts mis à jour** ainsi que chaque modification des statuts …"
>
> *dt.: „2° **der Auszug der Gründungsurkunde** gemäß § 2; 4° **die erste Fassung des Satzungstextes** sowie die Gründungsurkunde und **der aktualisierte koordinierte Satzungstext** sowie jede Satzungsänderung …"*

**Lesart:** Nr. 2 (= Auszug) wird publiziert. Nr. 4 (= Volltext-/koordinierte Satzung) wird **nur hinterlegt**; im Staatsblatt erscheint dazu lediglich eine **Erwähnung**.

**Empirischer Beweis am realen BV-Gründungsdokument.** Abgerufen 2026-07-30, `https://www.ejustice.just.fgov.be/tsv_pdf/2022/12/23/22385985.pdf` — Gründung der BV „FLOORMASTERS", notarielle Urkunde vom 20.12.2022, 5 Seiten, PDF mit Textebene:

> „Rechtsvorm : Besloten Vennootschap … Onderwerp akte : OPRICHTING … Er blijkt uit een akte verleden op 20 december 2022 … voor Meester Bart van OPSTAL, notaris met standplaats te Oostende …
> **STATUTEN (uittreksel)**
> Artikel 1: Naam en rechtsvorm …"
>
> *dt.: „Rechtsform: Besloten Vennootschap … Gegenstand der Urkunde: GRÜNDUNG … Aus einer am 20. Dezember 2022 … vor Meister Bart van OPSTAL, Notar mit Amtssitz in Ostende, errichteten Urkunde geht hervor … **SATZUNG (Auszug)** — Artikel 1: Name und Rechtsform …"*

Die im Dokument enthaltenen Artikelüberschriften lauten in dieser Reihenfolge: **1, 2, 3, 4, 5, 12, 15, 19, 21, 21.1, 21.4, 22, 25, 26, 29**. Die Lücken (6–11, 13–14, 16–18, 20, 23–24, 27–28) sind der direkte Beleg: Das Staatsblatt enthält bei einer BV **einen Auszug, nicht die Satzung**. Die Überschrift „STATUTEN (**uittreksel**)" sagt es wörtlich.

**Konfidenz dieses Einzelbefunds: hoch** (eigener Abruf, Textebene ausgewertet).

**Wo die Volltextsatzung tatsächlich frei liegt: Stapor.** Empirisch verifiziert am 2026-07-30, Abruf `https://statuten.notaris.be/stapor_v1/enterprise/0403199702/statutes`, ohne Login, ohne Zahlung:

> Seitentitel „Statutenübersicht"; Spalten „Statut | Titel | Datum der Urkunde | Letzte Aktualisierung | Notariatsbüro | Documents | Aktien". Einträge u. a. „Statuts coordonnés au 22 avril 2021" (Urkundendatum 22.04.2021, Notar Bernard WILLOCX) und „BNP Paribas Fortis - COO - 23.04.2026 - NL + FR" (Berquin Notarissen). Ausgabe „1 - 5 von 8".
> Je Zeile **zwei** Download-Symbole; Tooltips wörtlich: **„Standardkopie der Statuten"** und **„Beglaubigte Abschrift der Statuten"**.

Fednot-Betreiberseite (https://www.notaire.be/entreprendre/demarrer-une-entreprise/les-statuts-dune-societe):

> Die Datenbank „**peut être consultée gratuitement**", umfasst „**depuis le 1ᵉʳ mai 2019**" die Fassungen „**depuis la constitution de la personne morale jusqu'à la dernière mise à jour des statuts**", und man kann „**télécharger une copie électronique certifiée**".
>
> *dt.: „… kann **kostenlos eingesehen werden**"; abgedeckt **seit dem 1. Mai 2019**, alle Fassungen „**von der Gründung der juristischen Person bis zur letzten Satzungsaktualisierung**"; man kann „**eine beglaubigte elektronische Kopie herunterladen**".*

**Abdeckungslücken von Stapor — der wichtigste Vorbehalt.**

Stapor gibt bei fehlenden Einträgen selbst folgende Meldung aus (wörtlich, deutsche Sprachversion, abgerufen 2026-07-30):

> „Für das gewählte Unternehmen ist in der Datenbank noch keine Übersicht über die koordinierten Statuten vorhanden. **Diese Datenbank enthält nur die Statuten, die von 01.05.2019 übermittelt wurden.** Eine ältere Version der Statuten erhalten Sie bei der **Kanzlei des zuständigen Unternehmensgerichts** (auf Grundlage der Adresse des Unternehmenssitzes)."

Beachte die Formulierung: „die **übermittelt** wurden" — maßgeblich ist die tatsächliche Übermittlung durch den Notar, nicht das Gründungsdatum.

**Stichprobe vom 2026-07-30 (6 Unternehmen, nicht repräsentativ):**

| Unternehmensnummer | Name | Rechtsform | Stapor-Treffer |
|---|---|---|---|
| 0403.199.702 | BNP Paribas Fortis | NV | **ja** — 8 Fassungen |
| 0400.378.485 | Etablissementen Franz Colruyt | NV | **ja** — 5 Fassungen (2020–2025) |
| 0402.206.045 | Delhaize Le Lion/De Leeuw | NV | **ja** — 5 Fassungen (2022–2026) |
| 0878.065.378 | Google Belgium | — | **ja** — 1 Fassung (2022) |
| **0795.175.316** | **FLOORMASTERS** | **BV** | **NEIN** — trotz notarieller Gründung am **20.12.2022** |
| **0778.878.326** | Vastgoedgroep Degroote | BV | **NEIN** |

→ **Die beiden Fehltreffer sind genau der Fall, der uns interessiert: kleine, nach dem 01.05.2019 notariell gegründete BV.** Die freie Satzungsquelle ist damit **vorhanden, aber nicht garantiert**. Vor einer Produktivumstellung ist die **Trefferquote an einer echten Stichprobe aus unserem Auftragsbestand zu messen**; nur so lässt sich beziffern, welcher Anteil weiterhin über einen Anbieter oder über die Gerichtskanzlei laufen muss.

**Weitere Grenzen:**
- Nur **notarielle** Urkunden, die in Belgien errichtet wurden. Rechtsformen, die durch **Privaturkunde** gegründet werden (VZW/ASBL, VOF/SNC, CommV/SComm), sind **nicht** enthalten.
  *Belege:* Die KBO-Detailseite bezeichnet den Link ausdrücklich als „Databank van statuten en vertegenwoordigingsbevoegdheden **(notariële akten)**". Empirisch bestätigt: ASBL „Felobel", Unternehmensnummer 0761.808.009, gegründet 19.01.2021 durch Privaturkunde — **kein Stapor-Eintrag**, obwohl die **vollständige Satzung** derselben ASBL im Staatsblatt frei als PDF liegt (BE-5). Das ist genau die beschriebene Komplementarität.
- Für nicht abgedeckte Fälle bleibt das Dossier bei der **Kanzlei des Unternehmensgerichts**: kostenlose Einsicht, Kopien gegen Kanzleigebühren (Art. 2:12 § 2) — **manueller, nicht automatisierbarer Kanal**.

**Konfidenz: hoch** für die Existenz der Lücke (eigene Abrufe, Betreibermeldung wörtlich); **niedrig** für deren quantitativen Umfang.

**Gegenstück für ASBL/VZW:** Für Vereine wird der Auszug nach Art. 2:9 § 2 publiziert, und dieser Auszug ist inhaltlich nahezu eine Volltextsatzung (Zweck, Tätigkeiten, Mitgliedschaftsbedingungen, Generalversammlung, Verwaltungsorgan usw.). Das deckt sich mit dem geprüften Beispiel-PDF `tsv_pdf/2021/01/22/21305176.pdf` (ASBL „Felobel"), das die Statuten Artikel für Artikel im Volltext enthält.

→ **Kombinierte Abdeckung: Kapitalgesellschaften über Stapor, Vereine über das Staatsblatt — beides kostenlos.**

**Konfidenz: hoch** für Rechtslage und für die tatsächliche kostenlose Verfügbarkeit bei Stapor.

### A.6.3 Gesellschafterliste — beim Register nicht erhältlich

Art. 5:24 WVV/CSA (BV/SRL):

> „**La société tient à son siège un registre pour chaque catégorie de titres nominatifs** que la société a émis. Nonobstant toute disposition contraire, **les titulaires de titres peuvent prendre connaissance de l'intégralité du registre concernant leur catégorie de titres**."
>
> *dt.: „**Die Gesellschaft führt an ihrem Sitz ein Register für jede Kategorie von Namenspapieren**, die sie ausgegeben hat. Ungeachtet anderslautender Bestimmungen **können die Titelinhaber das gesamte Register ihrer Titelkategorie einsehen**."*

→ Das Anteilsregister wird **von der Gesellschaft** geführt, ist **nicht** beim Register hinterlegt und ist **nicht öffentlich** — nur die Inhaber der jeweiligen Titelkategorie haben Einsicht.

**Teilweise Ersatzquellen:**
- Der Gründungsauszug nennt Gründer und noch nicht voll einzahlende Gesellschafter (Art. 2:8 § 2 Nr. 4) — eine **Momentaufnahme bei Gründung**, kein aktueller Gesellschafterkreis.
- Rubrik **VOL-kap 6.7.2** des Jahresabschlusses („Aandeelhoudersstructuur", über NBB-API kostenlos abrufbar) — beruht aber auf **Transparenzmeldungen**, nicht auf dem Anteilsregister, und existiert nur im **vollständigen Modell**. Siehe A.4. Für eine typische kleine BV ist sie **nicht vorhanden**.
- Das UBO-Register (Register der wirtschaftlichen Eigentümer, FÖD Finanzen) ist eine andere Kategorie und wurde in diesem Auftrag nicht geprüft.

**Konfidenz: hoch** für „Register liefert keine Gesellschafterliste".

---

## A.7 Quellentabelle Belgien

| Nr. | Quelle | Betreiber | URL | Abruf | Primärquelle |
|---|---|---|---|---|---|
| BE-1 | Code des sociétés et des associations, Art. 2:7, 2:8, 2:9, 2:12, 2:14, 5:24 (Justel) | FÖD Justiz | https://www.ejustice.just.fgov.be/eli/loi/2019/03/23/2019A40586/justel | 2026-07-30 | **ja** (Gesetzestext) |
| BE-2 | Annexe Personnes morales — Portalseite | FÖD Justiz | https://www.ejustice.just.fgov.be/cgi_tsv_pub/welcome.pl?language=fr | 2026-07-30 | **ja** |
| BE-3 | Annexe — Suchformular | FÖD Justiz | https://www.ejustice.just.fgov.be/cgi_tsv/rech.pl?language=fr | 2026-07-30 | **ja** |
| BE-4 | Annexe — Publikationsliste je Unternehmen (983 Treffer für 0403199702) | FÖD Justiz | https://www.ejustice.just.fgov.be/cgi_tsv/list.pl?language=nl&btw=0403199702&page=1&view_numac=0403199702 | 2026-07-30 | **ja** |
| BE-5 | Beispiel-Veröffentlichung (ASBL, Volltextsatzung), 8 S., Textebene | FÖD Justiz | https://www.ejustice.just.fgov.be/tsv_pdf/2021/01/22/21305176.pdf | 2026-07-30 | **ja** |
| BE-5b | **Beispiel-Veröffentlichung BV „FLOORMASTERS", Gründung 20.12.2022 — „STATUTEN (uittreksel)", Artikel 1–5, 12, 15, 19, 21, 22, 25, 26, 29** | FÖD Justiz | https://www.ejustice.just.fgov.be/tsv_pdf/2022/12/23/22385985.pdf | 2026-07-30 | **ja** |
| BE-6 | Conditions d'utilisation — Wiederverwendungsklausel | FÖD Justiz | https://www.ejustice.just.fgov.be/img_2024/pdf/GebruiksvoorwaardenFR.pdf | 2026-07-30 | **ja** |
| BE-7 | Frais de publication (Tarife ab 01.03.2026) | FÖD Justiz | https://www.ejustice.just.fgov.be/cgi_tsv_pub/page.pl?language=fr&type=p | 2026-07-30 | **ja** |
| BE-8 | KBO Public Search Detailseite mit Verlinkung Staatsblatt/NBB/Stapor | FÖD Wirtschaft | https://kbopub.economie.fgov.be/kbopub/toonondernemingps.html?lang=nl&ondernemingsnummer=0403199702 | 2026-07-30 | **ja** |
| BE-9 | KBO Open Data — Themenseite | FÖD Wirtschaft | https://economie.fgov.be/nl/themas/ondernemingen/kruispuntbank-van/diensten-voor-iedereen/hergebruik-van-publieke/kruispuntbank-van-0 | 2026-07-30 | **ja** |
| BE-10 | KBO Open Data — Login/Registrierung („gratis" / „betalend") | FÖD Wirtschaft | https://kbopub.economie.fgov.be/kbo-open-data/login?lang=nl | 2026-07-30 | **ja** |
| BE-11 | **Lizenz KBO Open Data — Nutzungsbedingungen (14 Artikel)** | FÖD Wirtschaft | https://economie.fgov.be/sites/default/files/Files/Entreprises/KBO/Licentie-KBO-Open-Data-gebruiksvoorwaarden.pdf | 2026-07-30 | **ja** |
| BE-12 | CBE Public Search Web Service — 50 € / 2.000 Abfragen | FÖD Wirtschaft | https://economie.fgov.be/en/themes/enterprises/crossroads-bank-enterprises/services-everyone/public-data-available-reuse/cbe-public-search-web-service | 2026-07-30 | **ja** |
| BE-13 | KBO Open Data — Cookbook (techn. Doku) | FÖD Wirtschaft | https://economie.fgov.be/sites/default/files/Files/Entreprises/BCE/Cookbook-BCE-Open-Data.pdf | 2026-07-30 | **ja** |
| BE-13b | **KBO Open Data — amtlicher Datenkatalog (Feldliste, keine Funktionen/Organe)** | FÖD Wirtschaft | https://economie.fgov.be/sites/default/files/Files/Entreprises/BCE/Catalogue-des-donnees-reutilisables-BCE-opendata.pdf | 2026-07-30 | **ja** |
| BE-14 | **Stapor — Statutenübersicht, Live-Abruf (Standardkopie + beglaubigte Abschrift)** | Fednot | https://statuten.notaris.be/stapor_v1/enterprise/0403199702/statutes | 2026-07-30 | **ja** (Betreiberportal) |
| BE-15 | Stapor — Suchseite | Fednot | https://statuten.notaris.be/stapor_v1/search | 2026-07-30 | **ja** |
| BE-15b | **Stapor — Abdeckungsstichprobe**: Treffer 0400378485 (Colruyt), 0402206045 (Delhaize), 0878065378 (Google Belgium); **kein Treffer** 0795175316 (FLOORMASTERS BV, gegr. 20.12.2022), 0778878326 | Fednot | `https://statuten.notaris.be/stapor_v1/enterprise/<Nr>/statutes` | 2026-07-30 | **ja** |
| BE-16 | Fednot — Beschreibung der Statutendatenbank (gratis, ab 01.05.2019, beglaubigte Kopie) | Fednot | https://www.notaire.be/entreprendre/demarrer-une-entreprise/les-statuts-dune-societe | 2026-07-30 | **ja** (Betreiber) |
| BE-17 | NBB — Konsultationsprodukte | NBB | https://www.nbb.be/en/central-balance-sheet-office/consultation-data | 2026-07-30 | **ja** |
| BE-18 | NBB Consult — Umfang ab 1999, PDF/XBRL/CSV | NBB | https://www.nbb.be/en/central-balance-sheet-office/consultation/consult | 2026-07-30 | **ja** |
| BE-19 | NBB Consult — Nutzungsbedingungen (kein Massenabruf) | NBB | https://www.nbb.be/en/central-balance-sheet-office/consultation/consult/terms-use | 2026-07-30 | **ja** |
| BE-20 | NBB — Kopienbestellung 5 € / 0,25 € pro Seite | NBB | https://www.nbb.be/en/central-balance-sheet-office/consultation/consult/ordering-copies-annual-accounts | 2026-07-30 | **ja** |
| BE-21 | **NBB Webservices — AGB (Preise, Produkte, Nutzungsbeschränkungen)** | NBB | https://www.nbb.be/doc/ba/cbso2022/cnd_n_abin_webservices_v2022_en_v7.pdf | 2026-07-30 | **ja** |
| BE-22 | NBB Webservices — technischer Leitfaden (Basis-URL, Endpunkte, Header, PDF-Beispiel) | NBB | https://www.nbb.be/doc/ba/cbso2022/cbso_webservices_technical%20guide_0.94.pdf | 2026-07-30 | **ja** |
| BE-22b | **NBB Jahresabschlussmodell VOL-kap 6.7.1/6.7.2 — „Aandeelhoudersstructuur", meldungsbasiert** | NBB | https://www.nbb.be/doc/ba/models/ent/release_2021_nl_model_vol_kapitaalvennootschappen.pdf | 2026-07-30 | **ja** |
| BE-23 | NBB Webservices — Übersichtsseite (kostenlos vs. kostenpflichtig) | NBB | https://www.nbb.be/en/central-balance-sheet-office/consultation/web-services | 2026-07-30 | **ja** |
| BE-24 | NBB Entwicklerportal | NBB | https://developer.cbso.nbb.be/ | 2026-07-30 | **ja** |

### Nicht erreichbar / vergeblich gesucht (Belgien)

| URL | Fehlerart |
|---|---|
| `https://www.ejustice.just.fgov.be/cgi_tsv/tsv_rech.pl?language=fr` | HTTP 500 |
| `https://www.ejustice.just.fgov.be/cgi_tsv/tsv_rech.pl?language=fr&btw=0403199702` | ECONNRESET |
| `https://www.ejustice.just.fgov.be/tsv/tsvf.htm` | Frameset ohne Inhalt |
| `https://www.ejustice.just.fgov.be/tsv_pdf/2017/07/26/17317413.pdf` | ECONNRESET (zweiter SRL-Beleg daher nicht geprüft) |
| `https://economie.fgov.be/fr/themes/entreprises/banque-carrefour-des/…/open-data-de-la-bce` | HTTP 404 (FR-Pfad; NL/EN-Pfad funktioniert) |
| `https://www.nbb.be/fr/centrale-des-bilans/consultation-de-donnees` und `…/services-web` | HTTP 404 (FR-Pfade; EN-Pfade funktionieren) |
| `https://developer.cbso.nbb.be/products` | Azure-APIM-SPA, Produktliste ohne Login nicht auslesbar |
| `https://consult.cbso.nbb.be/` | JS-Anwendung, Text nicht per Fetch auslesbar |
| Nutzungs-/Lizenzbedingungen von Stapor | **nicht auffindbar** (Portal-Fußzeile, Cookie-Richtlinie, Fednot-Seiten geprüft) |
| Königlicher Erlass als Rechtsgrundlage der „Frais de publication" | auf der amtlichen Tarifseite **nicht zitiert** |
| Rechtsgrundlage speziell des **öffentlichen** Stapor-Segments im geltenden WVV | **nicht gefunden**; Art. 2:12 § 2 Abs. 2 beschränkt die Online-Einsicht des Dossier-Datenbanksystems auf Richter, KBO-Beamte, Notare und die juristische Person selbst |

---

## A.8 Konfidenz je Punkt (Belgien)

| Punkt | Konfidenz | Begründung |
|---|---|---|
| Registerbetreiber und Portale (alle vier) | **hoch** | amtliche Portalseiten selbst abgerufen |
| KBO Open Data kostenlos, tägliche Aktualisierung, Registrierung nötig | **hoch** | Lizenz Art. 7 + Loginseite + Themenseite |
| KBO liefert nur Daten, keine Dokumente | **hoch** | KBO-Detailseite verlinkt für Dokumente auf Staatsblatt/NBB/Stapor |
| CBE Public Search Web Service kostenpflichtig, 50 €/2.000 Abfragen | **hoch** | amtliche Seite |
| Staatsblatt: Gründungs**auszug** frei als PDF mit Textebene | **hoch** | eigener Abruf + Art. 2:14/2:8 |
| Staatsblatt: **keine** Volltextsatzung für Gesellschaften | **hoch** | Art. 2:14 Nr. 1 vs. Nr. 2 i.V.m. Art. 2:8 § 1 Nr. 2 und 4 |
| Volltextsatzung frei bei Stapor, inkl. beglaubigter Abschrift | **hoch** | Live-Abruf mit Tooltips + Fednot-Betreiberseite |
| Stapor-Abdeckung nur notarielle Urkunden ab 01.05.2019 | **hoch** | Betreibermeldung im Portal wörtlich: „nur die Statuten, die von 01.05.2019 übermittelt wurden" |
| **Stapor-Abdeckung ist lückenhaft** (2 von 6 Stichproben ohne Treffer, beide kleine BV nach 2019) | **hoch** (Existenz der Lücke) / **niedrig** (Umfang) | eigene Abrufe 0795175316 und 0778878326 |
| Ausschluss von Privaturkunden (VZW, VOF, CommV) aus Stapor | **mittel** | KBO-Linktext „(notariële akten)" + empirischer Negativtest ASBL 0761808009; keine ausdrückliche Regelaussage des Betreibers gefunden |
| Stapor: kein dokumentiertes öffentliches API | **hoch** | keine Doku auffindbar; internes REST-Backend nur aus dem Netzwerkverkehr sichtbar |
| Staatsblatt: kein dokumentiertes API, aber stabile GET-URLs | **hoch** | eigener Abruf |
| NBB-Webservice liefert **Dokumente** und ist kostenlos | **hoch** | AGB Nr. 1.1 und Nr. 2 |
| Weitergaberecht Staatsblatt (kommerziell frei) | **hoch** | Conditions d'utilisation Abschnitt III |
| Weitergaberecht NBB-Dokumente | **hoch** | AGB Nr. 5 |
| Weitergaberecht KBO-Daten | **mittel** | Art. 2.9 impliziert Kunden; keine ausdrückliche Erlaubnis; Zweckbindung nach Art. 2.3 bindet |
| **Weitergaberecht Stapor-Satzungen** | **niedrig** | **keine Nutzungsbedingungen gefunden — offener Punkt** |
| Gesellschafterliste beim Register nicht erhältlich | **hoch** | Art. 5:24 |
| „Aandeelhoudersstructuur" (VOL-kap 6.7.2) ist meldungsbasiert und kein Gesellschafterlisten-Ersatz | **hoch** | amtliches NBB-Modell, Wortlaut der Rubriküberschrift |
| NBB-API: Basis-URL, Endpunkte, Header, PDF via `Accept: application/pdf` | **hoch** | NBB Technical Guide v0.94, wörtliches Codebeispiel |
| MwSt.-Status aller genannten Preise | **niedrig** | nirgends ausgewiesen; als netto behandelt |
| Keine Beschränkung für ausländische Unternehmen | **mittel** | Schluss aus dem Fehlen jeder Bedingung, keine ausdrückliche Negativaussage |

---

## A.9 Bewertung für die Direktanbindung (Belgien)

| Dokumentenart | Direkt beschaffbar? | Kanal | Kosten | Restrisiko |
|---|---|---|---|---|
| **Strukturdaten / „Registerauszug"-Ersatz** | **ja** | KBO Open Data (Bulk, täglich) + Staatsblatt-Auszug | 0 € | keine Funktionen/Organe im Open Data → für Organe zusätzlich Public Search Webservice (50 €/2.000) oder Staatsblatt-Auszüge parsen |
| **Gründungsurkunde (Auszug)** | **ja** | Staatsblatt `list.pl` + `tsv_pdf` | 0 € | kein API-Vertrag, kein SLA; Scraping-Risiko |
| **Satzung, Volltext / koordiniert** | **überwiegend** | Stapor | 0 € | **Abdeckungslücke** (Stichprobe 4/6); nur notarielle Urkunden ab 2019; **Weitergaberecht ungeklärt** |
| **Satzung, Volltext (Verein)** | **ja** | Staatsblatt-Auszug nach Art. 2:9 § 2 | 0 € | – |
| **Jahresabschluss** | **ja, inkl. API** | NBB Webservice „Authentic Data Query" | 0 € | Vertrag (unterschriebenes Bestellformular) nötig |
| **Gesellschafterliste** | **nein** | – | – | Beim Register schlicht nicht vorhanden (Art. 5:24) |

**Empfehlung:**
1. **Vor der Anbieterverhandlung**: Trefferquote von Stapor an 50–100 echten belgischen Aufträgen messen. Das ist der Hebel für den Preisnachlass.
2. **Sofort umsetzbar und risikoarm**: NBB-Webservice „Authentic Data Query" abonnieren (kostenlos, echtes Dokument-API, ausdrücklich weitergabefreies Nutzungsrecht nach AGB Nr. 5).
3. **Vor produktivem Einsatz von Stapor**: Weitergaberecht schriftlich bei Fednot klären — das ist derzeit der einzige rechtlich offene Punkt in Belgien.
4. **Bei KBO-Open-Data-Registrierung**: Zweck ausdrücklich als „Bereitstellung an Kunden im Rahmen von KYC-/Onboarding-Dienstleistungen" angeben (Lizenz Art. 2.3 bindet an den angegebenen Zweck).
5. **Nicht** NBB Consult scrapen (Nutzungsbedingungen untersagen Massenabruf) — stattdessen das kostenlose Webservice-Produkt.

---

# TEIL B — ISRAEL

Israel ist der **umgekehrte Fall zu Belgien**: eine einzige Behörde, ein einziges Portal, klare amtliche Gebührenordnung — und der Registerauszug enthält **bereits die Gesellschafterliste**, die es in Belgien überhaupt nicht gibt.

## B.1 Registerbetreiber und offizielles Portal

- **Behörde:** רשות התאגידים — **Israeli Corporations Authority**, im משרד המשפטים (Justizministerium)
- **Zuständige Einheit:** יחידת החברות (Companies Unit); Amtsträger: **רשם החברות** (Registrar of Companies)
- **Transaktionsportal:** https://ica.justice.gov.il — Markenname **תאגידים ברשת (תאגידים ONLINE)**
  Verifiziert 2026-07-30: HTTP 302 auf `https://ica.justice.gov.il/GenericCorporarionInfo/SearchCorporation?unit=8`
- **Informations-/Dienstseite (gov.il):** https://www.gov.il/he/service/company_extract (EN: `/en/service/company_extract`)
- **Bestellstrecke Firmenauszug:** `https://ica.justice.gov.il/Request/OpenRequest?rt=CompanyExtract` → `…/IcaSite/request/openRequest/6/0/0/8`, Titel **„בקשה לנסח חברה"**
- **Dienstübersicht Dokumente:** https://ica.justice.gov.il/IcaSite/request-type-menu/8/2

> **Korrektur zu unserem Datenbestand:** `ica.justice.gov.il` ist **nicht migriert** und weiterhin gültig. Die vermutete Nachfolgedomain `taagidim.justice.gov.il` **existiert nicht** (kein DNS-Eintrag, Verbindungsfehler).

**Korrekte Dokumentbezeichnung: נסח חברה** („company extract"), optional als **נסח מורחב** („erweiterter Auszug") **ohne Mehrkosten**:

> „בהפקת נסח חברה בתשלום, ניתן לסמן את אפשרות 'נסח מורחב' לקבלת מידע נוסף על החברה ללא עלות נוספת."
>
> *dt.: „Bei der kostenpflichtigen Erstellung eines Firmenauszugs kann die Option ‚erweiterter Auszug' angehakt werden, um ohne Zusatzkosten weitere Informationen über die Gesellschaft zu erhalten."*
> (https://www.gov.il/he/service/company_extract, abgerufen 2026-07-30)

> **Der Begriff „נסח מחשבי" (nesach mahshevi) aus unserem Datenbestand ließ sich in KEINER Primärquelle nachweisen.** Vergeblich gesucht in gov.il, ica.justice.gov.il, der Gebührentabelle und im Companies Law. → **unbelegt, zu streichen.**

**Konfidenz: hoch.**

## B.2 Zugang: Registrierung, Identifikation, Ausländer

**Für Firmenauszug und Firmenakte gilt: kein Konto, kein Vertrag, keine israelische ID — nur die Gebühr.**

Beleg: Die ICA-Dienstkacheln nennen unter „מה נדרש ממך" („was von Ihnen verlangt wird", https://ica.justice.gov.il/IcaSite/request-type-menu/8/2, abgerufen 2026-07-30):

| Dienst | „מה נדרש ממך" | dt. |
|---|---|---|
| הפקת נסח חברה (עברית ואנגלית) | **אגרת שירות** | nur Dienstgebühr |
| הזמנת תיק חברה/חל"צ | **אגרת שירות** | nur Dienstgebühr |
| חיפוש הפוך (Reverse Search) | **הזדהות** + אגרת שירות | **Identifikation** + Gebühr |
| עץ בעלויות (Ownership-Tree) | **הזדהות** | **Identifikation** |

Der Bestellassistent hat drei Schritte und **keinen Login-Schritt**:

> „בקשה לנסח חברה — 1 פרטי הפניה · 2 פרטי הפונה · 3 הגשת הבקשה"
>
> *dt.: „Antrag auf Firmenauszug — 1 Antragsdetails · 2 Antragstellerdaten · 3 Antragseinreichung"*
> (https://ica.justice.gov.il/IcaSite/request/openRequest/6/0/0/8, abgerufen 2026-07-30; nur gelesen, nichts abgeschickt)

**Identifikationspflichtig** sind dagegen Reverse Search und Ownership-Tree:

> „מעבר להזדהות במערכת ההזדהות לאומית או עם כרטיס חכם"
>
> *dt.: „Wechsel zur Identifikation im nationalen Identifikationssystem oder mit Smartcard"*
> (https://www.gov.il/he/service/reverse-search, abgerufen 2026-07-30)

→ Diese beiden Dienste sind für uns als ausländisches Unternehmen **praktisch gesperrt**.

**Ausländische Besteller:** funktional möglich — Auszug und Akte verlangen keine הזדהות, die Zustellung erfolgt per E-Mail, und gov.il nennt ausdrücklich eine Auslandsrufnummer `+972-8-6831680`.
**Offener Punkt:** Ob der Zahlungsserver (שרת התשלומים) **nicht-israelische Kreditkarten** akzeptiert, ist in keiner amtlichen Quelle geregelt. **Konfidenz: niedrig — unbelegt.** Das ist der einzige echte Blocker-Kandidat und vor einer Integration mit einem Testkauf oder telefonisch zu klären.

**Registrierungsseite:** entfällt — es gibt keine.

**Konfidenz:** Zugang ohne Konto/ID **hoch**; Auslandszahlung **niedrig**.

## B.3 Preise — amtliche Gebührentabelle 2026

**Primärquelle:** gov.il-Publikation **„תעריפי אגרות רשות התאגידים לשנת 2026"** („Gebührentarife der Corporations Authority für das Jahr 2026"),
https://www.gov.il/he/pages/companies-fee-rates-2020 · PDF: https://www.gov.il/BlobFolder/reports/companies-fee-rates-2020/he/companies-fee-rates-2025.pdf
Aktualisierungsdatum **01.01.2026**; ausgewertet wurde **Seite 1 = יחידת החברות**.

| שם אגרה (Original) | ₪ | Deutsch |
|---|---|---|
| **נסח חברה (מקוון / api)** | **12** | **Firmenauszug (online / API)** |
| **הזמנת תיק חברה** | **39** | **Bestellung der Firmenakte** (enthält u. a. die Satzung) |
| **קבלת מסמך אחר מתיק החברה הסרוק** | **30** | **Einzeldokument aus der gescannten Firmenakte** |
| קבלת העתק תעודת התאגדות מקורית / תעודת שינוי שם / תעודה משוחזרת | 12 | Kopie Gründungsurkunde / Namensänderungsurkunde / rekonstruierte Urkunde |
| חיפוש הפוך | 12 | Reverse Search |
| אגרה שנתית מופחתת (עד 31.3) | 1.338 | ermäßigte Jahresgebühr (Pflicht der Gesellschaft, für uns irrelevant) |
| אגרה שנתית (מ-1.4) | 1.777 | Jahresgebühr |
| רישום חברה מקוון (אגרה מופחתת) | 2.559 | Online-Firmengründung (ermäßigt) |
| רישום חברה (למעט חל"צ) | 3.123 | Firmengründung |

**MwSt.: keine.** gov.il wörtlich (Dienstseite Firmenakte, Rubrik „אפשרויות תשלום"):

> „לתשומת לבכם, על תשלומים המשולמים למדינה לא מתווספת לרוב חובת תשלום מע"מ, ולכן, המדינה לא נדרשת להפיק בגינם חשבונית מס (לא קיים רכיב מע"מ)."
>
> *dt.: „Bitte beachten Sie: Zahlungen an den Staat unterliegen in der Regel keiner Mehrwertsteuerpflicht; der Staat ist daher nicht verpflichtet, dafür eine Steuerrechnung auszustellen (es gibt keine MwSt.-Komponente)."*
> (https://www.gov.il/he/service/company_online_portfolio, abgerufen 2026-07-30)

→ **Die Beträge sind Endbeträge in NIS. Netto = brutto.**

**Kostenlos:** Basisinformation zu einer Gesellschaft und der Bulk-Datensatz:

> „אפשרויות תשלום — השירות ניתן ללא עלות."
>
> *dt.: „Zahlungsoptionen — der Dienst wird kostenlos erbracht."*
> (https://www.gov.il/he/service/database-companies-partnership, abgerufen 2026-07-30)

> **Korrektur zu unserem Datenbestand:** Die Angabe „~NIS 10, exact amount not confirmed" ist zu ersetzen. Der Auszug kostet **12 ₪**, die Akte **39 ₪**, das Einzeldokument **30 ₪** — alles amtlich belegt.

**Konfidenz: hoch.**

**Vergeblich gesucht:** Die zugrunde liegende Verordnung **תקנות החברות (אגרות), תשס"א-2001** ist als amtlicher Volltext auf gov.il **nicht auffindbar**; sie liegt nur auf kommerziellen Portalen (nevo.co.il, psakdin, takdin). Ersatzbeleg ist die von der Behörde selbst publizierte Gebührentabelle. **Konfidenz zur Verordnungsfundstelle: niedrig.**

## B.4 API — Daten oder Dokumente?

### B.4.1 data.gov.il CKAN — live getestet, funktioniert

- **Dataset:** `ica_companies`, Titel **„מאגר חברות - רשם החברות"** („Firmendatenbank — Registerführer der Gesellschaften")
- **Organisation:** `ministry_of_justice` (משרד המשפטים), Kontakt `datagov_support@justice.gov.il`
- **Kanonische URL:** https://data.gov.il/datasets/ministry_of_justice/ica_companies (die bisher hinterlegte `…/dataset/ica_companies` liefert weiterhin HTTP 200)
- **resource_id:** `f004176c-b85f-4542-8901-7b3176f9a054` · CSV · 253.568.608 Bytes · `datastore_active: true`
- **Aktualisierung:** `Frequency: "Day"` — **täglich**; `metadata_modified: 2026-07-30T01:15:39`
- **Lizenz:** `license_id: "other-open"`, `license_title: "אחר (פתוח)"` („Sonstige (offen)"), `isopen: true`
- **Authentifizierung: keine.** **Rate-Limit:** in 5 schnellen Aufrufen keines beobachtet (5× HTTP 200, 0,35–3,2 s); ein dokumentiertes Limit wurde nicht gefunden.

**Echter Testaufruf** (2026-07-30):
`GET https://data.gov.il/api/3/action/datastore_search?resource_id=f004176c-b85f-4542-8901-7b3176f9a054&limit=1` → HTTP 200

```json
{"help":"https://data.gov.il/api/3/action/help_show?name=datastore_search","success":true,
 "result":{"limit":1,"resource_id":"f004176c-b85f-4542-8901-7b3176f9a054",
 "records":[{"_id":1,"מספר חברה":510000045,"שם חברה":"פלנת טרוסט אנד אגנסו בעמ","שם באנגלית":"",
   "סוג תאגיד":"ישראלית חברה פרטית","סטטוס חברה":"מחוקה","מטרת החברה":"לעסוק בסוגי עיסוק שפורטו בתקנון",
   "תאריך התאגדות":"01/05/1935","חברה ממשלתית":"לא","מגבלות":"מוגבלת", ...}],
 "total":728738,"total_was_estimated":false}}
```

**Datensatzzahl: 728.738** (bisher hinterlegt: ~728.150 — zu aktualisieren). Volltextsuche funktioniert: `&q=טבע` → `total: 477`, erster Treffer `TEVA TECH CHEMICALS LTD.`, ח.פ 510178676.

**Feldliste (29 Felder):** `_id` · מספר חברה · שם חברה · שם באנגלית · סוג תאגיד · סטטוס חברה · תאור חברה · מטרת החברה · תאריך התאגדות · חברה ממשלתית · מגבלות · מפרה · שנה אחרונה של דוח שנתי (שהוגש) · שם עיר · שם רחוב · מספר בית · מיקוד · ת.ד. · מדינה · אצל · תת סטטוס · zuzüglich 8 Code-Felder (קוד סטטוס חברה, קוד סוג חברה, קוד סיווג חברה, קוד מטרת החברה, קוד מגבלה, קוד חברה מפרה, קוד ישוב, קוד רחוב, קוד מדינה).

> **Kein Gesellschafter-, kein Direktoren-, kein Dokumentenfeld.** Die offene API liefert **ausschließlich Stammdaten**.

**Konfidenz: hoch** (live getestet, JSON zitiert).

### B.4.2 Der kostenpflichtige API-Kanal — belegt, aber undokumentiert

Die amtliche Gebührentabelle führt die Position wörtlich als:

> „**נסח חברה (מקוון / api) — 12**"
>
> *dt.: „Firmenauszug (online / API) — 12"*

→ Ein **kostenpflichtiger API-Kanal für den Firmenauszug existiert amtlich belegt**. **Öffentliche Entwicklerdokumentation wurde nicht gefunden.** Vergeblich gesucht: gov.il (Suche + Publikationen der רשות התאגידים), ica.justice.gov.il (alle Menüs unter `/IcaSite/`), data.gov.il/docs, sowie vier Websuchen HE/EN. Die einzigen Fundstellen sind Nicht-Primärquellen → **unbelegt**.

**Konfidenz:** „API existiert" **mittel-hoch** (amtliche Gebührenposition); „nutzbar/dokumentiert" **niedrig**.
**Nächster Schritt:** direkte Anfrage bei `*5601` bzw. `+972-8-6831680`. **Das ist der wichtigste offene Punkt für Israel** — er entscheidet, ob wir für 12 ₪ je Auszug vollautomatisch anbinden können.

### B.4.3 Zusammenfassung

| Kanal | Auth | Kosten | **Dokumente?** |
|---|---|---|---|
| data.gov.il CKAN `datastore_search` | **keine** | 0 ₪ | **nein — nur Daten** |
| ICA-Webbestellung (נסח חברה) | keine | 12 ₪ | **ja** (PDF per E-Mail) |
| ICA-Webbestellung (תיק חברה) | keine | 39 ₪ | **ja** (gescanntes, signiertes PDF) |
| „api"-Kanal laut Gebührentabelle | unbekannt | 12 ₪ | vermutlich ja — **Doku fehlt** |

## B.5 Die drei Dokumentenarten — israelische Realität

### B.5.1 Registerauszug (נסח חברה) — **enthält die Gesellschafterliste**

ICA-Dienstseite, wörtlich (https://ica.justice.gov.il/IcaSite/request-type-menu/8/2, abgerufen 2026-07-30):

> „נסח החברה כולל מידע מורחב כגון: שם החברה ומספרה, כתובת חברה, סטאטוס החברה, תאריך הגשת דוח שנתי אחרון, פירוט הרכב הון, **רשימת בעלי המניות**, רשימת הדירקטורים, רשימת השעבודים של החברה כולל סוג השעבוד, תאריכי רישום ויצירת השעבוד ותיאור הנכסים המשועבדים."
>
> *dt.: „Der Firmenauszug enthält erweiterte Informationen wie: Firmenname und -nummer, Firmenanschrift, Firmenstatus, Datum der letzten Jahresberichtseinreichung, Aufgliederung der Kapitalzusammensetzung, **Liste der Anteilseigner**, Liste der Direktoren, Liste der Sicherungsrechte der Gesellschaft einschließlich Art des Sicherungsrechts, Eintragungs- und Entstehungsdaten sowie Beschreibung der belasteten Vermögenswerte."*

→ **Ein einziges Dokument für 12 ₪ deckt Registerauszug UND Gesellschafterliste ab.** Das ist der wirtschaftlich attraktivste Einzelposten der beiden hier untersuchten Jurisdiktionen.

**Konfidenz: hoch.**

### B.5.2 Satzung (תקנון) — ja, erhältlich

**Einreichungspflicht bei Gründung**, חוק החברות, תשנ"ט-1999, § 8:

> „המבקש לרשום חברה יגיש לרשם בקשה לפי טופס שקבע השר ולה יצורפו: (1) **עותק של התקנון**; (2) הצהרה של הדירקטורים הראשונים על נכונותם לכהן כדירקטורים, כפי שקבע השר."
>
> *dt.: „Wer eine Gesellschaft eintragen lassen will, reicht beim Registerführer einen Antrag nach dem vom Minister bestimmten Formular ein, dem beizufügen sind: (1) **eine Abschrift der Satzung**; (2) eine Erklärung der ersten Direktoren über ihre Bereitschaft, als Direktoren zu amtieren."*

**Öffentlich bestellbar**, ICA-Dienstseite „הזמנת תיק חברה/חל"צ":

> „שירות זה מאפשר **לכל אדם** לעיין במסמכים המצויים בתיק חברה או חברה לתועלת הציבור. התיק כולל את המסמכים שהוגשו ליחידת רשם החברות על ידי התאגיד מיום רישומו … כגון: תעודת התאגדות, תעודת שינוי שם, **תקנון** ועוד. המסמכים בתיק **סרוקים וחתומים בחתימה אלקטרונית מאובטחת** והם **קבילים להגשה בבית משפט ובכל היחידות הממשלתיות** לאחר הדפסתם."
>
> *dt.: „Dieser Dienst ermöglicht es **jeder Person**, die in der Akte einer Gesellschaft … befindlichen Dokumente einzusehen. Die Akte umfasst die Dokumente, die die Körperschaft seit dem Tag ihrer Eintragung bei der Einheit des Registerführers eingereicht hat, wie etwa: Gründungsurkunde, Namensänderungsurkunde, **Satzung** und weitere. Die Dokumente in der Akte sind **gescannt und mit einer gesicherten elektronischen Signatur versehen** und nach dem Ausdruck **vor Gericht und bei allen Regierungsstellen zulässig**."*

**Ablauf** (https://www.gov.il/he/service/company_online_portfolio): Firmenname bzw. ח.פ eingeben → Warenkorb → Bestellung bestätigen → Kontaktdaten + Online-Zahlung → **innerhalb ca. einer Stunde** E-Mail mit Link zur gescannten Akte; Download nach Eingabe von Bestellnummer + Bestell-E-Mail; Entpacken aus dem Ordner `Catalog`.
**Zwei Varianten:** „כל מסמכי התיק" (gesamte Akte, **39 ₪**) und „מסמכים מאומתים מהתיק" (beglaubigte Einzeldokumente, **30 ₪** je Dokument).

**Konfidenz: hoch.**

### B.5.3 Certificate of Incorporation ≠ Satzung — bestätigt

Unser Anbieterkatalog führt für Israel nur eine *Certificate of Incorporation*. Das ist **nicht** die Satzung, und das israelische Recht sagt das ausdrücklich.

ICA-Dienstseite:

> „בהתאם לסעיף 10(ד) לחוק החברות, התשנ"ט - 1999, רשות התאגידים מנפיקה לחברות **תעודת התאגדות** המשמשת **ראיה חלוטה** לכך שהחברה נרשמה כדין במרשם החברות של מדינת ישראל."
>
> *dt.: „Gemäß § 10(d) des Companies Law 5759-1999 stellt die Corporations Authority den Gesellschaften eine **Gründungsurkunde** aus, die als **schlüssiger Beweis** dafür dient, dass die Gesellschaft ordnungsgemäß im Gesellschaftsregister des Staates Israel eingetragen wurde."*

Gesetzestext § 10:

> „(ג) משנרשמה חברה, ימסור לה הרשם תעודת התאגדות. (ד) תעודת התאגדות שנמסרה לחברה תשמש ראיה חלוטה לכך כי נתמלאו כל הדרישות לפי חוק זה לעניין הרישום … **(ה) אין בהוראת סעיף קטן (ד) כדי לרפא פגם בתקנון, או למנוע את הצורך בתיקונו.**"
>
> *dt.: „(c) Nach Eintragung der Gesellschaft übergibt der Registerführer ihr eine Gründungsurkunde. (d) Die Gründungsurkunde dient als schlüssiger Beweis dafür, dass alle Eintragungsanforderungen erfüllt wurden … **(e) Absatz (d) heilt keinen Mangel der Satzung und macht deren Berichtigung nicht entbehrlich.**"*

→ § 10(e) trennt beide Dokumente ausdrücklich: Die תעודת התאגדות ist eine reine **Eintragungsbescheinigung**, nicht die Satzung. Kopie: **12 ₪**.

> **Konsequenz für die Anbieterverhandlung:** Wenn ein Anbieter für Israel nur eine *Certificate of Incorporation* liefert, deckt er die Dokumentenart „Gesellschaftsvertrag/Satzung" **nicht** ab — obwohl die Satzung beim Register für **39 ₪** ohne Konto und ohne israelische ID bestellbar ist.

**Konfidenz: hoch.**

## B.6 Weitergaberecht — geschäftskritisch

### B.6.1 Registerdokumente — gesetzlich öffentlich

חוק החברות, תשנ"ט-1999, § 43 („עיון"):

> „המרשמים שמנהל הרשם בלשכת הרישום **יהיו פתוחים לעיון הציבור וכל אדם רשאי לעיין בהם ולקבל העתקים מאושרים** מן הרשום בהם, בין באמצעות הרשם ובין באמצעות אחרים שהרשם הסמיך אותם לכך, הכל כפי שקבע השר."
>
> *dt.: „Die Register, die der Registerführer im Registerbüro führt, **sind für die Einsichtnahme durch die Öffentlichkeit offen, und jede Person ist berechtigt, sie einzusehen und beglaubigte Abschriften des dort Eingetragenen zu erhalten**, sei es über den Registerführer oder über andere, die der Registerführer hierzu ermächtigt hat, alles wie vom Minister bestimmt."*

Ergänzend § 42 (zur Einordnung, keine Weitergabefrage): „רישומו או קיומו של מסמך בחברה או אצל הרשם, אין בו כשלעצמו משום ראיה לידיעת תוכנו." — *„Eintragung oder Vorhandensein eines Dokuments begründet für sich genommen keine Kenntnisvermutung."*

§ 43 sieht **keine Zweckbindung und keine Weitergabebeschränkung** vor. Die ICA bestätigt zusätzlich die Verwendbarkeit gegenüber Dritten („קבילים להגשה בבית משפט ובכל היחידות הממשלתיות לאחר הדפסתם").

> **Ausdrücklich unbelegt:** Ein Weiterverkaufs- bzw. Weitergabeverbot für bezogene Dokumente wurde in **keiner** Primärquelle gefunden. Die verbreitete Aussage „systematisches Bulk-Downloading zum Aufbau einer konkurrierenden Datenbank ist untersagt" stammt aus einem Aggregator-Blog und ist **unbelegt**.

**Konfidenz: hoch** für die Öffentlichkeit des Registers; **mittel** für „Weitergabe uneingeschränkt zulässig" (Schluss aus dem Fehlen einer Beschränkung).

### B.6.2 data.gov.il — kommerzielle Nutzung ausdrücklich erlaubt

Nutzungsbedingungen (תנאי שימוש), https://data.gov.il/he/terms-of-use, veröffentlicht 01.01.2018, aktualisiert 30.08.2025, Abschnitt „שימושים מותרים" (erlaubte Nutzungen):

> „אתה רשאי **להעתיק את המידע, להפיץ אותו, להעמיד אותו לרשות לציבור, לשדר אותו**, לבצע שינויים טכניים במידע וליצור ממנו יצירות נגזרות בכל מדיום או פורמט. **אתה רשאי לעשות שימוש במידע באופן מסחרי ובאופן שאינו מסחרי.**"
>
> *dt.: „Sie dürfen **die Informationen kopieren, verbreiten, der Öffentlichkeit zugänglich machen, senden**, technisch verändern und daraus abgeleitete Werke in jedem Medium oder Format erstellen. **Sie dürfen die Informationen kommerziell und nichtkommerziell nutzen.**"*

Namensnennungspflicht: „בשימוש במידע, עליך לציין את מקור המידע." — *„Bei Nutzung der Informationen müssen Sie die Quelle angeben."*

Abschnitt „שימושים אסורים" (verbotene Nutzungen), einschlägig für unser Aggregations-Setup:

> „לעשות שימוש שיביא לפגיעה בפרטיותו של אדם, **לרבות על ידי הצלבת המידע עם מקורות מידע אחרים**."
>
> *dt.: „Eine Nutzung vorzunehmen, die die Privatsphäre einer Person verletzt, **einschließlich durch Abgleich der Informationen mit anderen Informationsquellen**."*

> **Achtung, direkt relevant:** Das Verbot des **Cross-Matchings mit anderen Quellen bei Personenbezug** ist eine reale Nebenbedingung für eine Aggregationsarchitektur. Bei natürlichen Personen (der Datensatz enthält „ישראלית חברה פרטית" ebenso wie Einzelkaufleute) ist der Abgleich des CKAN-Datensatzes mit weiteren Quellen einzuschränken oder zu dokumentieren.

**Konfidenz: hoch.**

### B.6.3 gov.il-Urheberrecht

https://www.gov.il/he/pages/gov_terms_of_use:

> „זכויות היוצרים בפרסומי משרדי הממשלה … שייכות למדינת ישראל … המשתמש רשאי לעשות 'שימוש הוגן' בחומר המוגן"
>
> *dt.: „Das Urheberrecht an Publikationen der Regierungsministerien … steht dem Staat Israel zu … Der Nutzer darf ‚fair use' am geschützten Material vornehmen."*

Betrifft Website-Inhalte, **nicht** die nach § 43 Companies Law bezogenen Registerauszüge. **Konfidenz: hoch** für die Abgrenzung.

## B.7 Quellentabelle Israel

| Nr. | Quelle / Betreiber | URL | Abruf | Primärquelle |
|---|---|---|---|---|
| IL-1 | רשות התאגידים / gov.il — Dienstseite Firmenauszug | https://www.gov.il/he/service/company_extract | 2026-07-30 | **ja** |
| IL-2 | gov.il (EN) — Dienstseite Firmenauszug | https://www.gov.il/en/service/company_extract | 2026-07-30 | **ja** |
| IL-3 | ICA — Dienstübersicht „מידע, נסחים ומסמכים" (Auszugsinhalt inkl. Gesellschafterliste; Akteninhalt inkl. תקנון; Certificate of Incorporation) | https://ica.justice.gov.il/IcaSite/request-type-menu/8/2 | 2026-07-30 | **ja** |
| IL-4 | ICA — Bestellstrecke „בקשה לנסח חברה" | https://ica.justice.gov.il/IcaSite/request/openRequest/6/0/0/8 | 2026-07-30 | **ja** |
| IL-5 | ICA — Portalwurzel (HTTP 302 verifiziert) | https://ica.justice.gov.il | 2026-07-30 | **ja** |
| IL-6 | **gov.il — Gebührentabelle 2026 (Übersichtsseite)** | https://www.gov.il/he/pages/companies-fee-rates-2020 | 2026-07-30 | **ja** |
| IL-7 | **gov.il — Gebührentabelle 2026 (PDF, S. 1 יחידת החברות)** | https://www.gov.il/BlobFolder/reports/companies-fee-rates-2020/he/companies-fee-rates-2025.pdf | 2026-07-30 | **ja** |
| IL-8 | gov.il — Dienstseite Firmenakte (Ablauf, MwSt.-Hinweis) | https://www.gov.il/he/service/company_online_portfolio | 2026-07-30 | **ja** |
| IL-9 | gov.il — Dienstseite Bulk-Datensatz („ללא עלות") | https://www.gov.il/he/service/database-companies-partnership | 2026-07-30 | **ja** |
| IL-10 | gov.il — Reverse Search (Identifikationspflicht) | https://www.gov.il/he/service/reverse-search | 2026-07-30 | **ja** |
| IL-11 | **חוק החברות, תשנ"ט-1999 §§ 8, 10, 42, 43** (vom Justizministerium bereitgestellte konsolidierte Fassung) | https://www.gov.il/BlobFolder/legalinfo/info-and-regulation-15/he/files_InformationAndRegulation_15-law_companieslaw.pdf | 2026-07-30 | **ja, mit Vorbehalt*** |
| IL-12 | **data.gov.il — תנאי שימוש (Weitergaberecht)** | https://data.gov.il/he/terms-of-use | 2026-07-30 | **ja** |
| IL-13 | **data.gov.il CKAN — Live-Testaufruf `datastore_search`** | https://data.gov.il/api/3/action/datastore_search?resource_id=f004176c-b85f-4542-8901-7b3176f9a054&limit=1 | 2026-07-30 | **ja** |
| IL-14 | data.gov.il CKAN — `package_show` (Lizenz, Frequenz, Kontakt) | https://data.gov.il/api/3/action/package_show?id=ica_companies | 2026-07-30 | **ja** |
| IL-15 | data.gov.il — Datensatzseite (kanonisch) | https://data.gov.il/datasets/ministry_of_justice/ica_companies | 2026-07-30 | **ja** |
| IL-16 | gov.il — Nutzungsbedingungen / Urheberrecht | https://www.gov.il/he/pages/gov_terms_of_use | 2026-07-30 | **ja** |

\* **Vorbehalt zu IL-11:** Die PDF wird vom Justizministerium unter `/legalinfo/` bereitgestellt, trägt aber die Fußzeile „נבו הוצאה לאור בע"מ nevo.co.il" — es handelt sich um eine von Nevo erstellte **konsolidierte Fassung, die das Ministerium veröffentlicht**. Die Originalveröffentlichung in Reshumot (ספר החוקים) wurde **nicht** zusätzlich verifiziert. Für die zitierten §§ 8, 10, 42, 43 ist das unkritisch, sollte aber bekannt sein.

### Nicht erreichbar / vergeblich gesucht (Israel)

| URL / Gegenstand | Fehlerart |
|---|---|
| `https://www.gov.il/...` — alle Pfade per WebFetch und curl, inkl. Gebühren-PDF | **HTTP 403** (Antwortkörper: 5.946 B HTML-Blockseite). gov.il blockt automatisierte Abrufe generell; Inhalte wurden über den Chrome-Browser gelesen |
| `https://www.gov.il/he/api/PublicApi/GetDataByPath?path=...` | **HTTP 403** |
| `https://ica.justice.gov.il/IcaSite/request-type-menu/8/3` (WebFetch) | **ECONNRESET** |
| `https://ica.justice.gov.il/IcaSite/...` (curl) | HTTP 200, aber **JS-Wall** (Angular-SPA): extrahierter Text nur „תאגידים ברשת (תאגידים ONLINE)" |
| `https://www.gov.il/he/pages/company-fees` | **HTTP 404** — von Suchmaschinen noch indexierter toter Link |
| `https://data.gov.il/terms` | **HTTP 404** (korrekt: `/terms-of-use`) |
| `https://taagidim.justice.gov.il/` | **kein DNS-Eintrag, Verbindungsfehler** — Domain existiert nicht |
| `https://www.gov.il/he/search?q=...` (Browser) | Ergebnisse **rendern nicht** |
| gov.il-Such-API per JS-Fetch | von der Browser-Erweiterung blockiert |
| Gebühren-PDF S. 2–7 (andere Einheiten der רשות התאגידים) | **nicht ausgewertet** — nur S. 1 (יחידת החברות) |
| **Entwicklerdokumentation zum kostenpflichtigen „api"-Kanal** | **nicht gefunden.** Vergeblich: gov.il (Suche + Publikationen), ica.justice.gov.il (alle `/IcaSite/`-Menüs), data.gov.il/docs, 4 Websuchen HE/EN → **unbelegt** |
| Amtliche Aussage zu **ausländischen Zahlungsmitteln** | **nicht gefunden** → **unbelegt** |
| **„נסח מחשבי" / „nesach mahshevi"** | **nicht gefunden** in gov.il, ica.justice.gov.il, Gebührentabelle, Companies Law → **unbelegt** |
| „Bulk-Download zum Aufbau einer Konkurrenzdatenbank verboten" | nur Aggregator-Blog, kein Primärbeleg → **unbelegt** |
| **תקנות החברות (אגרות), תשס"א-2001** als amtlicher Volltext | auf gov.il **nicht auffindbar**; nur nevo.co.il / psakdin / takdin (kommerziell). Ersatzbeleg: IL-7 |

## B.8 Konfidenz je Punkt (Israel)

| Punkt | Konfidenz | Begründung |
|---|---|---|
| Betreiber, Portal-URL, Dienstseiten | **hoch** | gov.il + ica.justice.gov.il, wörtlich; `taagidim`-Domain aktiv widerlegt |
| Bezeichnung „נסח מחשבי" | **niedrig — unbelegt** | in keiner Primärquelle auffindbar; korrekt ist נסח חברה |
| Kein Konto / keine israelische ID für Auszug und Akte | **hoch** | ICA „מה נדרש ממך: אגרת שירות"; Bestellassistent ohne Login-Schritt |
| Identifikationspflicht bei Reverse Search / Ownership-Tree | **hoch** | gov.il wörtlich |
| Zahlung mit ausländischer Kreditkarte | **niedrig — unbelegt** | keine amtliche Aussage auffindbar |
| Gebühren 12 / 30 / 39 ₪, ohne MwSt. | **hoch** | amtliche Gebührentabelle 2026 + gov.il-MwSt.-Hinweis |
| Rechtsgrundlage der Gebühren (תקנות החברות (אגרות)) | **niedrig** | amtlicher Volltext nicht auf gov.il auffindbar |
| data.gov.il CKAN: 728.738 Sätze, keine Auth, täglich | **hoch** | live getestet, JSON zitiert |
| Offene API liefert nur **Daten**, keine Dokumente | **hoch** | Feldliste ohne Gesellschafter-, Direktoren- oder Dokumentenfeld |
| Kostenpflichtiger „api"-Kanal für den Auszug existiert | **mittel** | amtliche Gebührenposition „(מקוון / api)"; keine Doku gefunden |
| Auszug enthält **Gesellschafterliste** und Direktorenliste | **hoch** | ICA-Dienstseite wörtlich |
| Satzung (תקנון) über die Firmenakte bestellbar, 39 ₪ | **hoch** | ICA + gov.il wörtlich; § 8 Companies Law |
| Certificate of Incorporation ≠ Satzung | **hoch** | § 10(c)–(e) Companies Law wörtlich |
| Register öffentlich, Kopienanspruch für jedermann | **hoch** | § 43 Companies Law wörtlich |
| Weitergabe bezogener **Dokumente** an Kunden zulässig | **mittel** | § 43 kennt keine Beschränkung; ausdrückliche Erlaubnis fehlt |
| Weitergabe der **data.gov.il-Daten** zulässig, auch kommerziell | **hoch** | ToU wörtlich |
| Cross-Matching-Verbot bei Personenbezug | **hoch** | ToU wörtlich |
| Rechtstext-Fundstelle (konsolidierte Nevo-Fassung auf gov.il) | **mittel** | vom Ministerium publiziert, aber nicht Reshumot-Original |

## B.9 Bewertung für die Direktanbindung (Israel)

| Dokumentenart | Direkt beschaffbar? | Kanal | Kosten | Restrisiko |
|---|---|---|---|---|
| **Strukturdaten (Bulk)** | **ja** | data.gov.il CKAN, keine Auth | **0 ₪** | Cross-Matching-Verbot bei Personenbezug |
| **Registerauszug** | **ja** | ICA-Webbestellung | **12 ₪** | Bestellstrecke ist eine Angular-SPA → Automatisierung nur per Browser-Automation, sofern der „api"-Kanal nicht nutzbar ist; Auslandszahlung ungeklärt |
| **Satzung (תקנון)** | **ja** | ICA „הזמנת תיק חברה" (39 ₪) oder Einzeldokument (30 ₪) | **30–39 ₪** | Lieferung als ZIP mit gescannten PDFs → Zuordnung des richtigen Dokuments erfordert Verarbeitung |
| **Gesellschafterliste** | **ja — im Auszug enthalten** | ICA-Webbestellung | **im 12 ₪-Auszug enthalten** | – |

**Empfehlung:**
1. **Höchste Priorität:** Klärung des kostenpflichtigen „api"-Kanals (`נסח חברה (מקוון / api) — 12 ₪`) bei der Behörde (`*5601` / `+972-8-6831680`). Existiert er nutzbar, ist Israel für 12 ₪ je Auszug **vollautomatisch und ohne Anbieter** anzubinden — inklusive Gesellschafterliste.
2. **Parallel:** Testkauf eines Auszugs mit einer europäischen Firmenkreditkarte, um die einzige verbleibende Zugangsfrage zu beantworten. *(Erfordert eine ausdrückliche Freigabe — im Rahmen dieser Recherche wurde nichts bestellt und nichts bezahlt.)*
3. **Anbietergespräch Israel:** Der Katalogeintrag „Certificate of Incorporation" deckt die Satzung **nicht** ab. Entweder Nachlieferung des תקנון verlangen oder diese Dokumentenart selbst beschaffen — die Behördengebühr beträgt 30–39 ₪.
4. **data.gov.il** sofort als kostenlose Stammdatenquelle einbinden (Quellenangabe pflicht, Cross-Matching-Grenze dokumentieren).

---

# TEIL C — Vergleich und Gesamtbild

| Kriterium | **Belgien** | **Israel** |
|---|---|---|
| Zahl der Quellen | **4** (KBO, Staatsblatt, Stapor, NBB) | **2** (ICA, data.gov.il) |
| Stammdaten kostenlos | ja (KBO Open Data, Registrierung nötig) | ja (CKAN, **ohne** Registrierung) |
| Registerauszug | kein einheitliches Dokument; Ersatz aus mehreren Quellen, 0 € | **ein Dokument, 12 ₪** |
| Satzung Volltext | Stapor, 0 €, **aber lückenhaft** | Firmenakte, 30–39 ₪, vollständig |
| **Gesellschafterliste** | **existiert nicht** (Art. 5:24 WVV) | **im Auszug enthalten** |
| Dokument-API | **ja**, aber nur für Jahresabschlüsse (NBB, kostenlos) | Gebührenposition belegt einen API-Kanal, **Doku fehlt** |
| Weitergaberecht Dokumente | **ausdrücklich frei** (Staatsblatt), **ausdrücklich frei** (NBB) | § 43 kennt keine Beschränkung; keine ausdrückliche Erlaubnis |
| Zugangshürde für uns als Ausländer | keine erkennbar | keine für Auszug/Akte; **Zahlungsmittel ungeklärt** |
| Größter offener Punkt | **Weitergaberecht Stapor** + Abdeckungslücke | **API-Doku** + Auslandszahlung |

**Gemeinsamer Befund:** In **beiden** Jurisdiktionen sind alle beim Register überhaupt existierenden Dokumentenarten **direkt und zu Beträgen unter 10 €** beschaffbar. Ein Anbieteraufschlag lässt sich in keinem der beiden Fälle mit der Beschaffungsschwierigkeit begründen — nur mit Automatisierungsaufwand (Belgien: Scraping ohne SLA; Israel: SPA-Bestellstrecke) und mit der Abdeckungslücke bei Stapor.
