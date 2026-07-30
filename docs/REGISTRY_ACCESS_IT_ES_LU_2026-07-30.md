# Zugangs-Dossier Handelsregister: Italien, Spanien, Luxemburg

**Stand: 2026-07-30** · Grundlage für die Entscheidung „Direktanbindung vs. Zwischenanbieter"
**Ziel:** Konfidenz von mittel/niedrig auf hoch heben — belegt ausschließlich über Primärquellen.

---

## 0. Quellendisziplin dieses Dossiers

**Als Primärquelle gilt hier nur:** der Registerbetreiber selbst, die zuständige Behörde,
amtliche Gebührenverordnungen, Gesetzestexte in amtlicher oder vom Betreiber selbst
publizierter koordinierter Fassung.

**Nicht als Beleg verwendet:** Aggregatoren, Anbieter-Blogs, Kanzlei-Marketingseiten,
Wikipedia. Wo eine Aussage nur dort auffindbar war, ist sie als **UNBELEGT** markiert,
mit Angabe der vergeblich geprüften Stellen.

Jeder Beleg besteht aus **wörtlichem Zitat in Originalsprache + URL + Abrufdatum**.
Ein Beleg ohne Zitat zählt in diesem Dossier nicht.

**Bewusst nicht getan:** kein Konto angelegt, keine Registrierung eingereicht, nichts
bestellt, nichts bezahlt, keine Nutzungsbedingungen akzeptiert, kein CAPTCHA gelöst,
keine Repo-Datei geändert. Wo der Weg an einer solchen Schranke endete, ist das als
Schranke dokumentiert und nicht überschritten worden.

---

## 1. Executive Summary — was sich gegenüber unserem bisherigen Stand ändert

| Jurisdiktion | Bisherige Annahme | Befund | Richtung |
|---|---|---|---|
| **LU** | „Download hinterlegter Dokumente kostenlos mit Konto" | **BESTÄTIGT**, doppelt belegt (AGB + Gebührenanhang). Kein Konto nötig — anonyme Verbindung genügt | ✅ bestätigt |
| **LU** | „API liefert Daten, aber keine Dokumente" | **WIDERLEGT.** Art. 22 (2) RGD i.d.F. 17.02.2025: „données publiques inscrites **et des documents publics déposés**" | ❌ korrigieren |
| **LU** | „API-Behauptungen stammen von Aggregatoren" | **WIDERLEGT.** LBR bestätigt die API in den eigenen AGB; Zugangsgebühr steht im Gebührenanhang: **5.000 €/Jahr** | ❌ korrigieren |
| **LU** | „Konfidenz mittel" | Alles aus Primärquellen belegbar | → **hoch** |
| **IT** | „ABDO/Telemaco liefert Daten und Dokumente" | **BESTÄTIGT.** Atti nur als PDF, Prospetti HTML/PDF/TXT, Dati XML/XBRL/CSV | ✅ bestätigt |
| **IT** | „optionales Web-Telemaco-Abo ~250 € + MwSt" | **WIDERLEGT.** Kein amtlicher Beleg; nur bei Wiederverkäufern. Telemaco ist Prepaid, Registrierung gratis | ❌ korrigieren |
| **IT** | Weitergabe an Kunden implizit unterstellt | **KRITISCH:** Mit Standard-Telemaco **ausdrücklich verboten**. Nur der Operator-Vertrag erlaubt Distribution | ⚠️ neu |
| **ES** | „apificado-Systeme liefern Dokumente per API" | **Teilweise widerlegt.** CORPME bestätigt die Systeme wörtlich, nennt als Ausgabe aber nur *„nota simple o certificación"* — Urkunden (estatutos, cuentas anuales) sind **nicht** belegt | ⚠️ einschränken |
| **ES** | „kein öffentliches Entwicklerportal" | **BESTÄTIGT.** Einziger veröffentlichter Zugangsweg: `api@corpme.es` | ✅ bestätigt |
| **ES** | „nota simple ~6–9 € + MwSt" | **Nicht als Festpreis belegt.** Arancel kennt nur **0,601012 € je *asiento*** — der Endpreis skaliert mit der Zahl der Eintragungen | ⚠️ präzisieren |
| **ES** | Zugang implizit als machbar unterstellt | **NEU und kritisch:** Für die „alta de abonado" ist *certificado electrónico* oder *Cl@ve* **zwingend** — faktische Hürde für ein deutsches Unternehmen | ⚠️ neu |
| **ES** | Weitergaberecht nicht bewertet | **NEU:** Aviso legal begrenzt die Nutzung auf *ámbito doméstico* und verbietet kommerzielle Verbreitung ohne vorherige schriftliche CORPME-Genehmigung | ⚠️ neu |
| **ES** | „Konfidenz mittel" | Zugang, Weitergaberecht, API-Existenz jetzt primärbelegt; Urkundenpreise und Auslandstauglichkeit weiter offen | → **mittel** (unverändert, aber anders begründet) |

**Die teuerste Fehlannahme wäre gewesen**, Italien über das bequeme englischsprachige
Auslandsportal anzubinden: dessen AGB verbieten die Weitergabe wörtlich. Der Kanal, der
unser Geschäftsmodell trägt, ist ein anderer und deutlich teurer.

**Das übergreifende Muster:** In **allen drei** Ländern ist die Weitergabe eines bezogenen
Dokuments an einen eigenen Kunden auf dem günstigen Selbstbedienungsweg **untersagt oder
auf nicht-kommerzielle Zwecke beschränkt**. Der Vertrags-/API-Weg ist damit nirgends eine
Optimierung, sondern die Voraussetzung des Geschäftsmodells.

---
---

# LUXEMBURG — RCS / Luxembourg Business Registers

**Priorität dieses Auftrags. Die Gratis-Download-Aussage wurde vorrangig geprüft und
ist bestätigt — mit einer wichtigen Präzisierung.**

## LU.1 Registerbetreiber und offizielles Portal

| | |
|---|---|
| Register | Registre de commerce et des sociétés (RCS) |
| Betreiber | **Luxembourg Business Registers** — ein *groupement d'intérêt économique* (g.i.e.) |
| Portal | `https://www.lbr.lu` (neue Oberfläche unter `/mjrcs-web-front/`) |
| Weitere Register desselben Betreibers | RBE (wirtschaftliche Eigentümer), RESA (Amtsblatt), REGINSOL (Insolvenz) |
| Sitz | 31, Avenue de la Gare, L-1611 Luxembourg |

**Beleg (Gesetzesrang):**
> „*La gestion du registre de commerce et des sociétés est confiée au groupement d'intérêt
> économique Luxembourg Business Registers, appelé ci-après le « gestionnaire du Registre
> de commerce et des sociétés ».*"
> — Art. 1er, Règlement grand-ducal du 23 janvier 2003, i.d.F. Règl. gd. 13 mars 2025,
> koordinierte Fassung publiziert von LBR selbst:
> `https://lbrcontent.public.lu/dam-assets/code-legal/legislation/rcs/fr/rgd-2003-2025.pdf`
> (Abruf 2026-07-30)

**Beleg (Selbstbeschreibung des Betreibers):**
> „*Le groupement d'intérêt économique (gie) LUXEMBOURG BUSINESS REGISTERS (ci-après « LBR »)
> alimente ce serveur en vue de promouvoir l'accès public aux informations concernant les
> personnes physiques et entités sujettes à immatriculation de par la législation concernant
> le registre de commerce et des sociétés (RCS) …*"
> — `https://www.lbr.lu/mjrcs-web-front/legal` (Abruf 2026-07-30)

**Konfidenz: hoch.** Betreiber aus dem Gesetzestext, Portal aus dem Betreiberimpressum.

> **Wichtig für die Aktualität:** Die koordinierte Fassung trägt den Warnhinweis
> „*Ce texte coordonné a été élaboré à des fins d'information ; seuls les textes publiés au
> Journal Officiel du Grand-Duché de Luxembourg font foi.*" Letzte eingearbeitete Änderung:
> règl. gd. 10 avril 2025 (Mem A 2025, n°140). Für rechtsverbindliche Zitate ist der
> Journal-officiel-Text maßgeblich.

## LU.2 Zugang

Es gibt **vier** Authentifizierungswege, und der entscheidende Punkt für uns:
**eine deutsche Gesellschaft braucht keine luxemburgische Identität.**

**Beleg (alle vier Modi, inkl. anonym ohne Kontoerstellung):**
> „*l'accès en ligne à certains services proposés par le gestionnaire sur son site internet
> se fait soit par une authentification via un produit délivré par LuxTrust S.A. ou une carte
> eID luxembourgeoise ou un certificat électronique eIDAS, offrant au minimum un niveau de
> garantie substantiel, soit par une connexion anonyme, qui n'implique pas de création de
> compte utilisateur.*"
> — Conditions Générales LBR, Ziff. 2 „Mise en garde",
> `https://www.lbr.lu/mjrcs-web-front/legal` → „Aspects légaux" → „conditions générales"
> (Abruf 2026-07-30)

**Der Weg für eine deutsche GmbH — eIDAS, Kontoanlage automatisch:**
> „*La création d'un nouveau compte utilisateur via une authentification par certificat eIDAS
> s'effectue automatiquement lors de la première connexion, si le certificat choisi n'a pas
> encore été utilisé sur le site LBR.*" … „*l'utilisateur est invité à : Saisir ses informations
> personnelles ; Saisir son adresse e-mail ; Répondre à une question de sécurité pour prouver
> qu'il ne s'agit pas d'un robot*"
> — `https://lbrcontent.public.lu/fr/help/help-account/help-account-authentication/help-account-authentication-eidas.html`
> (Abruf 2026-07-30)

**Der anonyme Weg (keine Registrierung, aber zwei Zustimmungsschranken):**
> „*Après avoir sélectionner le mode d'authentification par Connexion anonyme (Utilisateur
> anonyme), l'utilisateur est invité à répondre à une question de sécurité, prouvant qu'il ne
> s'agit pas d'un robot, et d'accepter les conditions d'utilisation des sites du CTIE en cochant
> la case correspondante. … l'utilisateur est redirigé vers l'écran suivant où il est invité à
> accepter les Conditions générales LBR.*"
> — `https://lbrcontent.public.lu/fr/help/help-account/help-account-authentication/help-account-authentication-anonymous.html`

**Selbst geprüft am 2026-07-30** (Browser, Suche nach RCS-Nr. B82454 / ArcelorMittal):
Die Stammdaten (Name, Sitz, Eintragungsdatum, Rechtsform) sind **ohne** Anmeldung sichtbar.
Beim Reiter „Liste der Einreichungen" erscheint:
> „*Um die Liste der Einreichungen zu sehen, ist eine Authentifizierung erforderlich*"
> — `https://www.lbr.lu/mjrcs-web-front/consult-company/B82454`

Der Klick führt auf die staatliche eAccess-Anmeldemaske
(`https://www.lbr.lu/login/TAMLoginServlet…`) mit den vier o.g. Modi. Bei „anonymer Benutzer"
folgt eine Sicherheitsfrage („Wie lautet die Summe von 2 und 7?") plus Zustimmung zu den
CTIE-Nutzungsbedingungen. **Hier wurde abgebrochen** — Bot-Prüfung und Zustimmung zu
Nutzungsbedingungen sind nicht Teil dieses Rechercheauftrags.

| Punkt | Antwort | Beleg |
|---|---|---|
| Reicht Registrierung? | Ja — bzw. gar keine nötig (anonyme Verbindung) | CG Ziff. 2 |
| Vertrag nötig? | Nein für das Portal. **Ja** für die API (siehe LU.4) | CG Ziff. 12 |
| Welche Nachweise? | Portal: keine. Bei eIDAS-Konto: Name, E-Mail | Hilfeseite eIDAS |
| Handelsregisterauszug/USt-ID? | Für den Portalzugang **nicht** verlangt | — |
| Beschränkung für Ausländer? | **Keine** — eIDAS ist ausdrücklich vorgesehen | CG Ziff. 2 |
| Registrierungsseite | `https://www.lbr.lu/mjrcs-web-front/` → „Se connecter"; Kontoanlage erfolgt implizit über eAccess/eIDAS beim Erstlogin. **Eine separate Registrierungs-URL existiert nicht.** | selbst geprüft |

**Konfidenz: hoch.**

## LU.3 Preise

**Maßgeblich ist Annexe J – Tarifs** des Règlement grand-ducal vom 23.01.2003. Quelle ist die
von LBR selbst publizierte koordinierte Fassung:
`https://lbrcontent.public.lu/dam-assets/code-legal/legislation/rcs/fr/rgd-2003-2025.pdf`
(Abruf 2026-07-30), erreichbar über `https://www.lbr.lu/mjrcs-web-front/legislative-documents`.

**Rechtsgrundlage der Gebührenerhebung:**
> „*… donnent lieu au paiement des frais tels que détaillés à l'annexe J auprès du gestionnaire
> du Registre de commerce et des sociétés.*" — Art. 25

**Netto/Brutto — eindeutig:**
> „*montants en EUR hors TVA (tarifs soumis à TVA au taux de 17%)*"
> — Kopfzeile Annexe J

Alle folgenden Beträge sind also **netto, zzgl. 17 % luxemburgischer MwSt.**

### Abrufkosten (Abschnitt „Autres frais administratifs")

| Position (verbatim) | Betrag netto |
|---|---|
| *demande de consultation* | **(kein Betrag ausgewiesen → gebührenfrei)** |
| *demande de consultation par voie électronique certifié conforme* | € 5,00 |
| *demande de consultation par voie électronique d'un lot d'archive certifié conforme* | € 7,50 |
| **frais d'accès à la plateforme électronique** | **Annuellement : € 5.000** |
| *extrait sous format papier (pour le 1er extrait …) avec signature* | € 21,43 |
| *pour chaque extrait sous format papier supplémentaire … avec signature* | € 7,70 |
| **extrait sous format électronique** | **€ 10,43** |
| *extrait sous format électronique avec signature qualifiée* | € 15,43 |
| *mise à disposition d'informations publiques inscrites au RCS … sous forme de données électroniques avec signature qualifiée automatique* | € 10,43 |
| *copie d'un document sous format papier certifiée conforme, par page* | € 1,50 |
| *copie d'un document sous format papier, par page* | € 0,50 |
| *certificat sous format papier avec signature* | € 10,00 |
| *certificat sous format électronique* | € 4,75 |
| *certificat sous format électronique avec signature qualifiée* | € 9,75 |
| *supplément pour traitement urgent d'une demande* | € 100,00 |
| *notification et suivi des dépôts (par numéro RCS)* — Überwachungsabo | € 1,00 |

Zum Vergleich Hinterlegungsgebühren (für uns nur Kontext): SA/SARL Ersteintragung
€ 105,91, Satzungsänderung € 54,78, *comptes annuels … déposés dans les délais légaux* € 19.

### **Die zentrale Aussage: hinterlegte Dokumente herunterladen ist gebührenfrei**

Zwei voneinander unabhängige Primärquellen sagen dasselbe.

**(a) Die AGB des Betreibers, wörtlich:**
> „*3.1.2. La consultation en ligne des dossiers tenus au RCS*
> *Pour pouvoir consulter les documents accessibles au public, contenus dans les dossiers tenus
> au RCS, l'utilisateur doit se connecter au site internet du gestionnaire soit par une
> authentification via un produit délivré par Luxtrust S.A. ou une carte eID luxembourgeoise ou
> un certificat électronique eIDAS, offrant au minimum un niveau de garantie substantiel, soit
> par une connexion anonyme.*
> *La recherche s'opère par numéro d'immatriculation ou par la dénomination / nom de l'entité
> immatriculée.*
> **Cette consultation est gratuite.**
> *Il est à noter que lorsque l'utilisateur demande à ce que le document consulté électroniquement
> soit certifié conforme par le gestionnaire, ces demandes font l'objet d'une prestation tarifaire.*"
> — Conditions Générales LBR, Ziff. 3.1.2, `https://www.lbr.lu/mjrcs-web-front/legal`
> (Abruf 2026-07-30)

**(b) Die Gebührenverordnung, im Umkehrschluss:** In Annexe J trägt die Rubrik
*„demande de consultation"* **selbst keinen Betrag**; bepreist sind ausschließlich die
*beglaubigte* elektronische Konsultation (€ 5,00) und der beglaubigte Archivsatz (€ 7,50).

**Was das für die drei STP-Dokumentarten heißt:**

| Dokumentart | LU-Entsprechung | Kosten netto |
|---|---|---|
| **Gesellschaftsvertrag / Satzung** | *statuts / statuts coordonnés*, im Dossier hinterlegt | **€ 0,00** (Download), € 5,00 falls beglaubigt |
| **Jahresabschluss, Beschlüsse** | *comptes annuels*, *actes*, im Dossier hinterlegt | **€ 0,00** (Download) |
| **Registerauszug** | *Extrait RCS* — vom Betreiber ausgestellt, **nicht** hinterlegt | € 10,43 elektronisch (€ 15,43 mit qualifizierter Signatur) |
| **Gesellschafterliste** | **im Register selbst geführt** — siehe LU.6 | im Extrait enthalten |

**Präzisierung gegenüber unserer Notiz:** Es ist **nicht** „kostenlos mit Konto", sondern
**kostenlos mit Authentifizierung** — und die anonyme Verbindung zählt als Authentifizierung
und erfordert ausdrücklich *keine* Kontoerstellung. Die Notiz war in der Sache richtig,
in der Bedingung zu streng.

**Konfidenz: hoch** (zwei unabhängige Primärquellen, wörtlich).

## LU.4 API

**Es gibt eine API. Sie ist vertraglich gegated. Und sie liefert Dokumente.**
Das ist die substanziellste Korrektur an unserem Datenbestand.

**(a) Der Betreiber bestätigt die API in den eigenen AGB:**
> „*Une interface de programmation d'application (API) est disponible pour permettre un accès
> automatisé aux données, dans le respect des conditions prévues notamment l'article 22 (2) du
> règlement grand-ducal modifié du 23 janvier 2003 précité et de l'article 7(3) du règlement
> grand-ducal du 15 février 2019 relatif aux modalités d'inscription, de paiement des frais
> administratifs ainsi qu'à l'accès aux informations inscrites au Registre des bénéficiaires
> effectifs. **L'accès à cette API suppose une demande dûment motivée et documentée et peut être
> accordé sous réserve de la conclusion d'une convention spécifique avec le gestionnaire du
> registre de commerce et des sociétés et du registre des bénéficiaires effectifs.***"
> — Conditions Générales LBR, Ziff. 12 „Sécurisation du site – Protection contre les accès
> automatisés", `https://www.lbr.lu/mjrcs-web-front/legal` (Abruf 2026-07-30)

**(b) Die Rechtsgrundlage sagt ausdrücklich: Daten UND Dokumente.**
> „*Art. 22. (Règl. gd. 17 février 2025) … (2) Après avoir été saisi d'une demande d'accès à un
> grand volume d'informations détenues au registre de commerce et des sociétés, le gestionnaire
> du registre de commerce et des sociétés peut mettre à disposition du demandeur, par le biais de
> sa plateforme électronique, tout ou partie des **données publiques inscrites et des documents
> publics déposés** au registre de commerce et des sociétés.*
> *La demande doit être motivée et préciser les finalités de la réutilisation desdites informations.*"
> — RGD 23.01.2003 i.d.F. 17.02.2025, koordinierte Fassung (URL wie LU.1)

**(c) Der Preis steht im Gebührenanhang:**
> „*frais d'accès à la plateforme électronique — Annuellement : € 5.000*"
> — Annexe J, Rubrik „Autres frais administratifs"

Dazu je Abruf strukturierter Daten mit automatischer qualifizierter Signatur:
> „*mise à disposition d'informations publiques inscrites au RCS pour une personne ou entité
> immatriculée sous forme de données électroniques avec signature qualifiée automatique — € 10,43*"

**(d) Kontext aus den Gesetzesmaterialien** (Projet de règlement grand-ducal, Februar 2022,
`https://gouvernement.lu/dam-assets/documents/actualites/2022/02-fevrier/21-tanson-lbr/PRGD-LBR.pdf`,
Abruf 2026-07-30) — nützlich, weil es Zweck und Volumen benennt:
> „*La plateforme dont il est question est mise à disposition par le Centre des technologies de
> l'information de l'Etat (CTIE), l'« API Gateway », ouvrant la voie aux communications
> électroniques de masse, de « machine à machine », sans intervention humaine.*"
> „*Durant l'année 2020, presque 15 millions de documents ont été consultés et téléchargés sur le
> site internent de LBR.*"
> „*Ce nouvel accès a pour objectif de répondre à la forte demande du marché d'obtenir des données
> réutilisables, à jour et actuelles, notamment à des fins de contrôle de la clientèle et de mise
> en conformité par rapport aux règles de la législation ayant trait à la lutte contre le
> blanchiment d'argent et le financement du terrorisme (LABFT).*"

Das ist exakt unser Anwendungsfall — der Gesetzgeber hat diese Schnittstelle für KYC/AML gebaut.

**(e) Technische Dokumentation: nicht öffentlich.** Es gibt kein Entwicklerportal, keine
Swagger-/OpenAPI-Datei, keine öffentliche Endpunktbeschreibung. Geprüft: `lbr.lu` (gesamtes
SPA-Bundle nach `api`/`tarif`-Strings durchsucht), `lbr.lu/sitemap.xml`, `lbrcontent.public.lu`
(vollständiger Hilfebaum), `legislative-documents`. **UNBELEGT bleibt jede Aussage über
Authentifizierungsverfahren (OAuth? mTLS? API-Key?), Endpunkte, Rate Limits und
Antwortformate** — die AGB nennen nur das Verfahren zur Zugangserlangung, nicht die Technik.

**(f) Scraping ist ausdrücklich untersagt** — relevant, weil „Portal abgreifen" damit als
Fallback ausscheidet:
> „*… l'accès au site internet est strictement limité à une utilisation manuelle et individuelle.
> **L'accès robotisé y est donc interdit**, les connexions en masse et automatisées sur le site
> internet pouvant entraîner un ralentissement de ce dernier, voire son blocage.*"
> „*Dans le cadre de la sécurisation du site et afin de prévenir les connexions automatisées
> abusives (par des robots ou scripts), LBR utilise un système de vérification automatique de type
> CAPTCHA. … **Toute tentative de contournement de ce système de protection pourra entraîner la
> suspension ou la suppression de l'accès aux services du site du LBR www.lbr.lu.***"
> — Conditions Générales LBR, Ziff. 12

Das CAPTCHA ist real: es erschien bei der Suche am 2026-07-30 auf
`https://www.lbr.lu/mjrcs-web-front/consult-company/B82454`.

**Konfidenz:**
- API existiert und ist vertragsgebunden: **hoch**
- API liefert Dokumente: **hoch** (Wortlaut der Rechtsgrundlage)
- Jahresgebühr 5.000 €: **hoch**
- Technische Ausgestaltung: **keine Aussage möglich — unbelegt**

## LU.5 Weitergaberecht

**Hier ist die Lage nicht eindeutig, und das ist ein Risiko, kein Detail.**

**Was der Betreiber auf seiner Website sagt — restriktiv:**
> „*Copyright — En l'absence d'indication contraire, la reproduction des informations contenues
> sur ce site est **réservée à des fins non commerciales** à condition que la source soit
> expressément mentionnée.*"
> — `https://www.lbr.lu/mjrcs-web-front/legal`, Abschnitt „Copyright" (Abruf 2026-07-30)

**Was die AGB sagen — Eigentumsanspruch, aber ohne Weitergabeverbot:**
> „*7. Droit de la propriété intellectuelle — La loi modifiée du 18 avril 2001 sur les droits
> d'auteur, les droits voisins et les bases de données est applicable au site internet du
> gestionnaire. Tous les éléments du site « www.lbr.lu » sont la propriété intellectuelle et
> exclusive du gestionnaire.*"
> — Conditions Générales LBR, Ziff. 7 (vollständiger Wortlaut der Ziffer)

**Was die Rechtsgrundlage der API sagt — Weiterverwendung ist ausdrücklich vorgesehen:**
> „*La demande doit être motivée et préciser les finalités de la **réutilisation** desdites
> informations.*" — Art. 22 (2) RGD

und in den Materialien:
> „*Rappelons que la réutilisation, par les professionnels bénéficiant de cet accès, des documents
> et données transmis doit s'effectuer en conformité avec les dispositions légales applicables,
> notamment celles relatives à la protection des données personnelles.*"
> — PRGD 2022, Kommentar zu Art. 22

**Bewertung:**

1. Die Copyright-Klausel ist als **Website-Klausel** formuliert („les informations contenues
   sur ce site", „tous les éléments du site"). Sie deckt Layout, Aufbereitung und Datenbank
   des Portals. Sie ist **nicht** ohne Weiteres auf die von Dritten hinterlegten Urkunden
   (Satzungen, Jahresabschlüsse) zu übertragen, an denen LBR kein Urheberrecht hat.
2. Art. 22 (2) RGD setzt Weiterverwendung ausdrücklich voraus und macht die Zweckangabe zur
   Zulassungsbedingung. Der Verordnungsgeber geht also davon aus, dass API-Nehmer die Inhalte
   weiterverwenden.
3. **Kein einziger gefundener Text enthält ein ausdrückliches Verbot, ein bezogenes Dokument
   an einen eigenen Kunden weiterzugeben.** Das ist der Unterschied zu Italien (dort steht
   das Verbot wörtlich in den AGB, siehe IT.5).

**Konsequenz:** Über das kostenlose Portal ist die kommerzielle Weitergabe durch die
Copyright-Klausel **nicht gedeckt**. Der saubere Weg ist die *convention spécifique* nach
Ziff. 12 CG / Art. 22 (2) RGD, in der die *finalités de la réutilisation* — nämlich
Weitergabe an KYC-pflichtige Kunden — genehmigt werden. **Das ist zugleich der einzige
legale Weg zur Automatisierung**, da Roboterzugriff aufs Portal verboten ist.

**Konfidenz: mittel.** Die Klauseln sind belegt und wörtlich zitiert; ihre Reichweite auf
hinterlegte Drittdokumente ist Auslegung. **Empfehlung: im Antrag nach Art. 22 (2) die
Weitergabe an Endkunden ausdrücklich als *finalité* deklarieren und sich schriftlich
bestätigen lassen.** Kontakt: `https://www.lbr.lu/mjrcs-web-front/contact`,
LUXEMBOURG BUSINESS REGISTERS g.i.e., 31 Avenue de la Gare, L-1611 Luxembourg,
Tel. +352 264 28-1.

## LU.6 Sonderbefund: Luxemburg hat eine echte Gesellschafterliste im Register

Für die S.à r.l. sind die Gesellschafter **eintragungspflichtige Registerdaten** — anders
als in den meisten Nachbarjurisdiktionen.

> „*6° (L. 23 janvier 2025) dans le cas des sociétés à responsabilité limitée, les associés,
> leur adresse privée ou professionnelle précise, ainsi que le nombre et le cas échéant, le
> type de parts sociales détenues par chacun*"
> — Loi modifiée du 19 décembre 2002, koordinierte Fassung publiziert von LBR:
> `https://lbrcontent.public.lu/dam-assets/code-legal/legislation/rcs/fr/rcs-loi-19-12-2002-2025.pdf`
> (Abruf 2026-07-30)

Analog für die SARL-S (Ziff. 6bis°), SNC/SCS (Ziff. 7°, *associés solidaires*) und die
*société civile* (Art. 8 Ziff. 4°). Für die SA gilt das **nicht** — dort greift stattdessen
das RBE (wirtschaftliche Eigentümer) mit eigenem Zugangsregime.

Da der *Extrait RCS* laut Art. 21 (2) RGD „*les données publiques inscrites dans le dossier*"
wiedergibt, ist die Gesellschafterliste einer S.à r.l. **im Registerauszug für € 10,43
enthalten** — kein separates Dokument nötig.

**Konfidenz: hoch** für die Eintragungspflicht; **mittel** für die Annahme, dass die
Gesellschafter tatsächlich auf dem Extrait abgedruckt werden (aus Art. 21 (2) gefolgert,
nicht an einem Musterauszug verifiziert — dafür hätte ein Auszug bestellt werden müssen).

## LU.7 Quellentabelle Luxemburg

| # | Quelle | Art | URL | Abruf |
|---|---|---|---|---|
| LU-1 | Conditions Générales LBR | Betreiber, AGB | `https://www.lbr.lu/mjrcs-web-front/legal` → „Aspects légaux" → „conditions générales" | 2026-07-30 |
| LU-2 | Aspects légaux / Copyright | Betreiber | `https://www.lbr.lu/mjrcs-web-front/legal` | 2026-07-30 |
| LU-3 | RGD 23.01.2003, koord. Fassung inkl. **Annexe J – Tarifs** | Verordnung | `https://lbrcontent.public.lu/dam-assets/code-legal/legislation/rcs/fr/rgd-2003-2025.pdf` | 2026-07-30 |
| LU-4 | Loi 19.12.2002 RCS, koord. Fassung | Gesetz | `https://lbrcontent.public.lu/dam-assets/code-legal/legislation/rcs/fr/rcs-loi-19-12-2002-2025.pdf` | 2026-07-30 |
| LU-5 | Index der Rechtstexte beim Betreiber | Betreiber | `https://www.lbr.lu/mjrcs-web-front/legislative-documents` | 2026-07-30 |
| LU-6 | Hilfe: Konsultation | Betreiber | `https://lbrcontent.public.lu/fr/help/help-consult.html` | 2026-07-30 |
| LU-7 | Hilfe: Authentifizierung eIDAS | Betreiber | `…/help-account/help-account-authentication/help-account-authentication-eidas.html` | 2026-07-30 |
| LU-8 | Hilfe: anonyme Verbindung | Betreiber | `…/help-account/help-account-authentication/help-account-authentication-anonymous.html` | 2026-07-30 |
| LU-9 | Projet de RGD 2022 (Materialien zur API) | Regierung | `https://gouvernement.lu/dam-assets/documents/actualites/2022/02-fevrier/21-tanson-lbr/PRGD-LBR.pdf` | 2026-07-30 |
| LU-10 | Live-Test Dossierkonsultation B82454 | eigene Beobachtung | `https://www.lbr.lu/mjrcs-web-front/consult-company/B82454` | 2026-07-30 |
| LU-11 | Kontakt LBR | Betreiber | `https://www.lbr.lu/mjrcs-web-front/contact` | 2026-07-30 |

## LU.8 Dead Ends Luxemburg

- `https://www.lbr.lu/mjrcs/jsp/…DisplayConsultDocumentsActionNotSecured.action` — **HTTP 429**,
  danach: Altsystem, ersetzt durch das neue SPA.
- `https://www.lbr.lu/mjrcs/jsp/secured/DisplayTarifsActionNotSecured.action` — leitet auf die
  eAccess-Anmeldemaske um, kein Tarifinhalt.
- `https://lbrcontent.public.lu/…` — **HTTP 403** über das Standard-Fetch-Tool; mit
  Browser-User-Agent per `curl` erreichbar. Alle Zitate stammen aus dem so geholten Volltext.
- `https://legilux.public.lu/eli/etat/leg/rgd/2003/01/23/n1/jo` — **JS-Wall**, Inhalt nur über
  `data.legilux.public.lu/filestore/...` erreichbar. Die konsolidierte Fassung ist dort unter
  keinem der geprüften ELI-Datumsmuster abrufbar (7 Varianten, alle 404) — deshalb wurde die
  vom Betreiber selbst publizierte koordinierte Fassung verwendet.
- `https://data.public.lu/en/organizations/luxembourg-business-registers/` — **HTTP 404**.
  **Die frühere Annahme „einige Datensätze auf data.public.lu sind frei" ist damit UNBELEGT.**
- **Kein API-Entwicklerportal auffindbar.** Geprüft: SPA-Bundle, sitemap.xml, gesamter
  Hilfebaum, Rechtsdokumentenseite. Die frühere Quelle „i-hub Pressemitteilung" wurde für
  dieses Dossier **nicht** herangezogen (kein Registerbetreiber).
- **Abgebrochen (bewusst):** die anonyme Anmeldung, weil sie Bot-Prüfung und Zustimmung zu
  Nutzungsbedingungen erfordert. Deshalb wurde **nicht** empirisch verifiziert, dass ein
  hinterlegtes PDF tatsächlich ohne Zahlungsaufforderung herunterlädt — die Aussage stützt
  sich auf die AGB und den Gebührenanhang.

---
---

# ITALIEN — Registro delle Imprese

## IT.1 Registerbetreiber und offizielles Portal

| | |
|---|---|
| Register | Registro delle Imprese, Rechtsgrundlage Art. 8 L. 580/1993 |
| Träger | die **Camere di Commercio** (öffentliche Körperschaften) |
| Technischer Betreiber | **InfoCamere S.C.p.A.**, Konsortialgesellschaft der Kammern |
| Dachverband | Unioncamere — *nicht* Betreiber |

**Beleg (aktueller Telemaco-Vertragstext, Art. 1):**
> „*Camere di Commercio Industria Artigianato ed Agricoltura o Camere di Commercio: gli enti che
> svolgono i compiti e le funzioni di cui alla legge 29 dicembre 1993, n. 580 e s.m.i. e, in
> particolare, assicurano – attraverso InfoCamere - la tenuta del registro delle imprese, del
> repertorio economico amministrativo, del registro dei protesti e degli altri albi e registri
> ad esse attribuiti dalla legge.*"
> — `https://registroimprese.infocamere.it/` (Vertragstext im Registrierungsfluss), Abruf 2026-07-30

**Beleg (Rolle von InfoCamere, Vertrag Art. 1.2):**
> „*InfoCamere: la società consortile di informatica per azioni delle Camere di Commercio … che,
> nell'interesse e per conto delle Camere di Commercio, assicura e gestisce i servizi di accesso
> on-line ai registri camerali garantendo la consultazione e l'esecuzione degli adempimenti
> telematici ai sensi della normativa vigente e provvedendo all'applicazione e all'incasso degli
> oneri connessi.*"
> — `https://www.registroimprese.it/dama/comc/comc/IT/registraServizi/CONTRATTO_TELEMACO_LIGHT_pc.pdf`

**Portallandschaft (alle geprüft):**

| Portal | URL | Funktion | Zugang |
|---|---|---|---|
| registroimprese.it | `https://www.registroimprese.it` | Publikums-/Bestellportal (IT) | SPID / CIE / CNS |
| Telemaco | `https://registroimprese.infocamere.it` | Sportello telematico | SPID / CIE / CNS |
| **ABDO** | `https://accessoallebanchedati.registroimprese.it/abdo/` | Operator-/Distributorkanal, API | **Vertrag** |
| **italianbusinessregister.it** | `https://italianbusinessregister.it` | EN/DE/FR/ES-Portal für Ausländer | **E-Mail-Konto** |
| impresa.italia.it | `https://impresa.italia.it` | **nur eigenes Unternehmen** — für uns irrelevant | SPID / CNS |

> „*Il servizio offerto dalle Camere di Commercio ai titolari e legali rappresentanti per accedere
> ai dati certificati della propria impresa*"
> — `https://www.infocamere.it/tutte-le-soluzioni/impresa-italia.html`

**Konfidenz: hoch.**

## IT.2 Zugang — zwei Türen, und die bequeme ist die falsche

### (a) Telemaco / registroimprese.it — italienische digitale Identität zwingend

> „*dal 28/02/2021 per la registrazione a Telemaco devi avere uno dei seguenti dispositivi di
> autenticazione: SPID liv.2, CIE 3.0, CNS*" · „*dal 30/09/2021 l'accesso al Servizio Telemaco,
> per i privati cittadini, è consentito esclusivamente tramite SPID, CIE o CNS*" ·
> „*la registrazione è gratuita*"
> — `https://www.registroimprese.it/area-utente`, Abruf 2026-07-30

Und technisch bindend an einen **codice fiscale**:
> „*in fase di accesso al Servizio da parte dell'Utente, verifica in automatico … della
> corrispondenza tra il codice fiscale contenuto nel sistema di identità digitale utilizzato …
> con il codice fiscale abilitato ad accedere alle banche dati e all'invio delle pratiche
> telematiche*" — Telemaco-AGB, Datenschutzabschnitt

Zudem definitorisch territorial gebunden:
> „*Servizio Telemaco e/o Servizio: il servizio di sportello telematico reso disponibile,
> attraverso InfoCamere, dalla Camera di Commercio ove ha sede o residenza l'Utente*" — AGB Art. 1

*Nebenbefund:* Die Fassung von 2012 enthielt zusätzlich
„*L'Utente si obbliga altresì ad utilizzare il Servizio … esclusivamente nello Stato ove ha
residenza o sede.*" (Art. 10.3) — diese Klausel ist in der aktuellen Fassung **nicht mehr
enthalten** (geprüft: String nicht vorhanden).

### (b) italianbusinessregister.it — Zugang ohne SPID, ohne codice fiscale

Der Login läuft über InfoCameres eigenes SSO (`sso.infocamere.it`, Keycloak-Realm `PIFE`)
und bietet **E-Mail/Passwort-Selbstregistrierung sowie Google** — **kein** SPID/CIE/CNS,
**kein** eIDAS.

> „*After login - if you have already registered - or after registration and subsequent login,
> your request will be added into a cart*" · „*you can pay the amount indicated by credit card
> (VISA, MASTERCARD are all accepted)*" · „*The registration will be deactivated automatically
> after 180 days if the user does not access the portal at least once*"
> — `https://italianbusinessregister.it/en/home`, Abruf 2026-07-30

> „*Access to the Italian Business Register is subject to registration in the manner indicated
> on the portal.*" — `https://italianbusinessregister.it/term-and-conditions-use`

Bonus: englischsprachige Auszüge ohne Aufpreis —
> „*The service is particularly economical, as there are no translation costs: Company
> Registration Reports in English actually cost the same as the reports in Italian.*"
> — `https://italianbusinessregister.it/en/company-report`

**Konfidenz: hoch** für die Existenz des Wegs; **die exakte Feldliste der Registrierung ist
unbelegt** (Keycloak-Registrierungsformular lieferte HTTP 400, abgelaufener `tab_id`).

### (c) Operator-/Distributorvertrag (ABDO) — der einzige tragfähige Weg

Voraussetzungen laut Allegato 2 zum *Contratto di accesso alle banche dati*:
> „*Requisiti dell'operatore ai sensi dell'articolo 12 del Contratto di accesso alle banche dati —
> **Iscrizione al Registro delle Imprese**; assenza di procedure concorsuali pendenti alla data di
> sottoscrizione delle Contratto di Accesso; assenza delle cause ostative di cui al Decreto
> Legislativo n. 159/2011 e s.m.i. (c.d. "Codice Antimafia"); … possesso di tutte le autorizzazioni
> ed i requisiti richiesti dalla normativa vigente per il legittimo espletamento delle proprie
> attività.*"
> — `https://intranet.infocamere.it/documents/10193/72493596/3+Contratto+di+accesso+-+Allegato+2.pdf`

Plus SEPA-Mandat und Sicherheit:
> „*l'Operatore presterà, contestualmente alla sottoscrizione del contratto e per tutta la sua
> durata, un deposito cauzionale o in alternativa una fideiussione bancaria o assicurativa per un
> importo di Euro 10.000,00 (diecimila) resa da primario istituto di credito o primaria compagnia
> di assicurazione.*" — Hauptvertrag Art. 15.1

Bei Jahresumsatz > 50.000 € Aufstockung auf 15 %, max. 1.000.000 €.

> **Offene Kernfrage:** „*Iscrizione al Registro delle Imprese*" meint im italienischen
> Rechtskontext das *italienische* Register. Ob eine deutsche Handelsregistereintragung genügt
> oder eine italienische *sede secondaria* nötig ist, sagt der Text **nicht**.
> **Konfidenz für die Auslegung: mittel — muss bei InfoCamere erfragt werden.**

**eIDAS am Kammerportal: UNBELEGT.** `https://www.eid.gov.it/en` lieferte **HTTP 403**.
Entsprechende Behauptungen fanden sich nur in Suchergebnis-Zusammenfassungen.

## IT.3 Preise

Rechtsgrundlage: interministerielles Dekret MIMIT/MEF vom 20.04.2023, veröffentlicht in
GU Nr. 149 vom 28.06.2023.
> Kopfzeile: „*TABELLA A — IMPORTI DIRITTI DI SEGRETERIA PER IL REGISTRO DELLE IMPRESE*",
> Blattkopf „*28-6-2023 GAZZETTA UFFICIALE DELLA REPUBBLICA ITALIANA Serie generale - n. 149*"
> — `https://www.mimit.gov.it/images/stories/normativa/TABELLA_A.pdf`, Abruf 2026-07-30
> (Dekretseite: `https://www.mimit.gov.it/it/normativa/decreti-interministeriali/decreto-interministeriale-mimit-e-mef-20-aprile-2023`)

### (a) Endkundentarif „allo sportello telematico"

| Position (verbatim aus Tabella A) | Betrag |
|---|---|
| *16.1 Visura ordinaria* (Kapitalges.) = **Registerauszug** | **€ 5,00** |
| *16.13 Visura soci e titolari di diritti su quote e azioni* | € 2,00 |
| *16.14 Fascicolo* | € 10,00 |
| *16.15 Copia atti* = **Urkundenkopie** | **€ 3,50** |
| *16.16 Visura informazioni da statuto, ultimo statuto depositato* = **Satzung** | **€ 3,50** |
| *17.1 Visura ordinaria* (Personenges.) | € 3,50 |
| *18.1 Visura ordinaria* (Einzelunternehmen) | € 3,00 |
| *Visura storica società di capitali* | € 6,00 |

Identisch im **Listino Telemaco** („*Aggiornamento del 30/04/2020*"),
`https://registroimprese.infocamere.it/documents/20182/3303865/listino+telemaco/731e68a1-2e69-4ecc-a8d8-82e75deb5597`.
Bei der reinen Konsultation fällt **keine** *tariffa* an (nur beim Praktikenversand:
„*Pratica telematica Registro Imprese 2,00*").

Dieselben Beträge auf dem Auslandsportal:
> „*Company Registration Report: €5.00/3.50/3.00 … Annual Account: €2.50 … Administration fees
> provided by decree by the Ministry for Economic Development of 17 July 2012.*"
> — `https://italianbusinessregister.it/term-and-conditions-use`

### (b) Operatortarif „da terminale remoto" — rund 70 % günstiger

| Position (verbatim) | *diritto* | + InfoCamere-*tariffa* | gesamt |
|---|---|---|---|
| *28.1 Visura ordinaria* | € 1,40 | € 1,85 | **€ 3,25** |
| *28.16 Visura informazioni da statuto …* | € 0,85 | € 1,45 | € 2,30 |
| *28.15 Copia atti* | € 0,85 | € 1,45 | € 2,30 |
| *28.13 Visura soci e titolari di diritti su quote e azioni* | € 0,45 | € 0,85 | € 1,30 |
| *28.14 Fascicolo* | € 2,60 | — | — |
| *Visura inglese società di capitale* | € 1,40 | € 1,85 | € 3,25 |
| *Copia Bilancio* | € 0,60 | € 0,85 | € 1,45 |

Tariffe aus `https://intranet.infocamere.it/documents/10193/72493596/2%20Contratto%20di%20accesso%20-%20Allegato%201.pdf`,
Spalten „*Tariffe (€)*" / „*Diritti di Segreteria (€)*".
**Konfidenz: hoch** für die *diritti* (Deckung mit dem Dekret 2023); **mittel** für die
*tariffe* — das Allegato verweist noch auf die Dekrete „*2 dicembre 2009 e del 17 luglio 2012*"
und auf D.Lgs. 196/2003, ist also vor-DSGVO und möglicherweise überholt.

### (c) Netto/Brutto — wichtig für unsere Weiterberechnung

> „*gli importi delle tariffe sono indicate con Iva al 20 per cento, mentre i diritti di segreteria
> sono qualificati come "operazioni fuori campo Iva ai sensi dell'articolo 15 del d.P.R. 26 ottobre
> 1972, n. 633".*"
> — Agenzia delle Entrate, Risoluzione 203/E vom 05.08.2009,
> `https://www.agenziaentrate.gov.it/portale/documents/20143/305631/Ris+203+del+5+08+2009_...pdf`

Beim **Weiterberechnen an unsere Kunden** bleibt es ohne IVA, aber mit anderer Begründung:
> „*Non di meno, la riconosciuta natura tributaria dei diritti di segreteria - che non viene meno
> qualora siano riaddebitati dalla società al cliente - ne esclude il carattere di corrispettivo e,
> pertanto, tali diritti non rilevano agli effetti dell'Iva ex articolo 3 del d.P.R. n. 633 del 1972
> per carenza del presupposto oggettivo*"

**Warnung, direkt produktrelevant:**
> „*qualora il cliente richieda alla società una particolare **rielaborazione** dell'informazione
> acquisita dal sistema telematico, l'attività svolta dalla società rappresenta un'operazione unica
> e complessa, nella quale i diritti di segreteria costituiscono parte integrante del corrispettivo
> … e, pertanto, come tali soggiacciono all'obbligo impositivo.*"

Sobald wir aufbereiten statt durchreichen, wird **der Gesamtbetrag IVA-pflichtig**.

### (d) „Web Telemaco ~250 € + MwSt" — **WIDERLEGT**

Kein amtlicher Beleg. Der Betrag erscheint ausschließlich bei Wiederverkäufern
(`visurenetwork.it`, `praevio.it`) — nach unserer Quellendisziplin unzulässig.
Amtlich gilt: „*la registrazione è gratuita*" und Prepaid statt Abo:
> „*un importo destinato alla fruizione del Servizio, non produttivo di interessi*" — AGB Art. 6.1

**Die echten Fixkosten liegen im Operatorvertrag** (Allegato 1, „*2 Canoni e accessi*"):
> „*UNA TANTUM DI ATTIVAZIONE 13.000,00*" · „*Collegamento al sistema InfoCamere automatizzato in
> forma massiva (AICA-ASSI-ASSI PLUS- AIWS) 6.000,00*" · „*Collegamento al sistema InfoCamere web
> internet (TELEMACO) 1.000,00*" · „*CANONE ANNUO 12.000,00*" / „*6.000,00*"

**Konfidenz: mittel-hoch** — Wortlaut sicher, Spaltenzuordnung der beiden CANONE-Zahlen im
PDF-Layout unsauber gesetzt. Größenordnung (fünfstellige Aktivierung + fünfstelliger
Jahreskanon) ist eindeutig. **Vor Budgetierung bei InfoCamere bestätigen lassen.**

## IT.4 API

**Existenz und Leistungsumfang:**
> „*Documenti e dati ufficiali su aziende e persone sempre disponibili con il nostro Web Service.*"
> — `https://accessoallebanchedati.registroimprese.it/abdo/api`, Abruf 2026-07-30
> Gelistete Dienste: *Ricerca Anagrafica*, *Protesti*, *Visura Amministratori*, *Visure*, *Bilancio XBRL*

**Liefert sie Dokumente? Ja — und das ist die klarste Formulierung im ganzen Vertragswerk:**
> „*I contenuti informativi presenti nelle banche dati (ad esclusione degli **Atti forniti soltanto
> in formato PDF**), saranno erogati nei seguenti formati tecnici: Prospetti, nei seguenti formati
> non modificabili: HTML, PDF e TXT; Dati, nei seguenti formati elaborabili: XML, XBRL e CSV.*"
> — Allegato 1, Abschnitt 1.3 „Formati disponibili e modalità di erogazione"

Zugriffsarten: „*Automatizzata massiva; Web internet; Massiva batch.*"

**Technik:**
> „*utilizzano il formato per richieste e risposte di tipo XML; consentono lo scambio dei messaggi
> fra i sistemi dell'Operatore e il sistema informatico nazionale tramite code MQ (AICA),
> collegamento socket (ASSI e ASSIPlus) o **web services REST (AIWS)***"
> — Allegato 3 „Specifiche Tecniche", Abschnitt 1.2,
> `https://intranet.infocamere.it/documents/10193/72493596/4+Contratto+di+accesso+-+Allegato+3.pdf`

**Authentifizierung — kein OAuth, kein API-Key:**
> „*utilizzano un collegamento su linea dedicata a garanzia di una maggiore sicurezza per
> l'interscambio dei dati; **l'utente viene riconosciuto in funzione della rete di provenienza e
> degli indirizzi IP di collegamento**, indirizzi che sono definiti ed accettati dai firewall
> InfoCamere; nel solo caso di AICA consentono il riconoscimento dell'utente anche in base alle
> coppie di code MQ definite*"

Testumgebung ist vorgesehen: „*prevedono l'assegnazione a ciascun Operatore di una coppia di
utenze, una riservata agli accessi in ambiente di test ed una in ambiente di produzione*".

> **Dedizierte Leitung plus IP-Whitelisting ist für einen deutschen Anbieter nicht-trivialer
> Infrastrukturaufwand — das gehört in jede Aufwandsschätzung.**

**Dokumentation: nicht öffentlich.**
> „*Le specifiche di collegamento ed accesso ai dati e prospetti sono illustrate nei manuali
> specifici pubblicati da InfoCamere sul sito internet www.infocamere.it /Area Riservata all'interno
> della sezione "Contratti".*"

Also: **ohne Vertrag keine API-Doku.** Kein Swagger/OpenAPI auffindbar. Die ABDO-Seite ist
reines Marketing; die Buttons „*Scarica un esempio*" liefern keine auffindbaren Datei-URLs.

Abgrenzung: „*non consentono l'invio delle pratiche di iscrizione, modifica, cancellazione e
deposito nelle Banche Dati*" — Eintragungen gehen nicht über die API (für uns irrelevant).
Zusätzlich existiert ein Massenabzug: „*un servizio di estrazione massiva batch dei contenuti
informativi presenti nelle Banche Dati … erogati su sito web protetto da userid e password*".

## IT.5 Weitergaberecht — der geschäftskritischste Befund des Dossiers

### (a) Mit Standard-Telemaco: **ausdrücklich VERBOTEN**

> „*12.2 L'Utente prende atto che è **espressamente vietata la rivendita, la distribuzione
> informatica e/o la riproduzione e/o la diffusione per copie in qualunque forma (cartacea,
> informatica etc.) dei Documenti estratti**.*"
> — Telemaco-AGB, Art. 12.2, `https://registroimprese.infocamere.it/` (Abruf 2026-07-30)

Sanktion: „*InfoCamere avrà facoltà di procedere all'immediata sospensione e/o disattivazione
del Servizio*" (Art. 13.1).

Wortgleich in der Fassung 2012 (Art. 10.1) — **und wortgleich auf dem englischsprachigen
Auslandsportal**, das wir sonst als bequemen Einstieg erwogen hätten:
> „*The user acknowledges that the resale, computer distribution and/or reproduction and/or
> dissemination of copies in any form (mechanical, printed, IT, etc.) of the extracted schedules
> is expressly prohibited.*"
> — `https://italianbusinessregister.it/term-and-conditions-use` (Originalsprache dieser Seite
> ist Englisch), Abruf 2026-07-30

**Konsequenz: Der bequeme Ausländerweg ist für unser Geschäftsmodell rechtlich NICHT nutzbar.**

### (b) Mit Operatorvertrag: **ausdrücklich ERLAUBT**

Präambel des *Contratto di Accesso alle Banche Dati*
(`https://intranet.infocamere.it/documents/10193/72493596/1+Contratto+di+accesso.pdf`):
> „*InfoCamere riconoscendo agli operatori un ruolo strategico nella diffusione del patrimonio
> informativo delle Camere di Commercio … intende con il presente contratto disciplinare la
> possibilità di **distribuire i documenti e riutilizzare i dati** tramite i servizi di accesso
> resi disponibili dal sistema informatico nazionale*"

**Art. 5 – Distribuzione dei Prospetti:**
> „*1. L'Operatore acquisisce il **diritto alla distribuzione a terzi dei Prospetti** mediante
> interfacciamento con il sistema informatico nazionale dei propri servizi telematici resi
> disponibili agli utenti finali o ad altri operatori terzi.*"
> „*2. I Prospetti dovranno essere distribuiti **esclusivamente nel medesimo formato elettronico
> non modificabile** estratto mediante collegamento al sistema informatico nazionale.*"
> „*3. … per ogni richiesta di Prospetto, dovrà essere effettuata una **nuova specifica estrazione**
> dalle Banche Dati con conseguente obbligo di versare la tariffa ed il corrispondente diritto di
> segreteria.*"
> „*4. L'Operatore che si avvale del diritto di distribuire a terzi i Prospetti è tenuto a
> qualificarsi e dare evidenza di essere "distributore ufficiale di InfoCamere" ed ha facoltà di
> utilizzare il marchio di InfoCamere stessa.*"
> „*5. Nel caso la distribuzione avvenga per il tramite di un operatore terzo è obbligo del
> "distributore ufficiale di InfoCamere" comunicare preventivamente ad InfoCamere i dati
> identificativi di tale operatore e i siti web attraverso cui opera a sua volta la distribuzione*"

**Drei harte Nebenbedingungen für unsere Architektur:**
1. **Kein Umformatieren, kein Rebranding** des PDF (Art. 5.2).
2. **Kein Caching, kein Wiederverkauf desselben Abzugs** — jede Kundenanfrage = neuer
   kostenpflichtiger Abruf (Art. 5.3).
3. **Kennzeichnungspflicht** als „distributore ufficiale di InfoCamere" (Art. 5.4).

**Art. 6 – Riutilizzo dei Dati:**
> „*1. L'Operatore … ha il diritto di estrarre i contenuti informativi in formato Dati … anche al
> fine di realizzare propri prodotti commerciali distinguibili in modo immediato ed inequivocabile
> dai prospetti.*"
> „*2. … i propri prodotti commerciali **non potranno limitarsi ad una mera riproduzione o mera
> aggregazione dei Dati**, ma dovranno necessariamente contenere adeguate informazioni integrative
> o approfondite analisi degli stessi Dati.*"
> „*3. L'Operatore non potrà in alcun modo associare ai propri prodotti commerciali l'utilizzo di
> alcuna qualifica, denominazione, marchio o altro segno distintivo riconducibile ad InfoCamere,
> alle Camere di Commercio…*"

→ **Eine reine Datendurchreiche ist vertragswidrig; Anreicherung ist Pflicht.** Dazu Art. 13.3:
> „*non è concesso alcuno dei diritti esclusivi di cui all'art. 64 quinquies della legge 22 dicembre
> 1941, n. 633*" — keine Datenbankschutzrechte an uns. Art. 14: Vertrag nicht ohne Zustimmung
> übertragbar.

**Unabhängige Bestätigung durch die Finanzverwaltung**, dass dieses Modell gelebte Praxis ist:
> „*InfoCamere stipula con primari operatori del mercato (c.d. distributori) contratti di
> divulgazione a terzi delle informazioni contenute nella banca dati delle Camere di commercio.*"
> — Risoluzione 203/E/2009

**Konfidenz: hoch** für beide Regime.

### (c) Open Data / PSI-Weiterverwendung: **UNBELEGT**

Keine Primärquelle gefunden, die Registro-Imprese-Inhalte unter eine offene Lizenz nach
D.Lgs. 36/2006 stellt; im Gegenteil behandeln alle gefundenen Vertragswerke die Inhalte als
entgeltpflichtig und weitergabebeschränkt. Vergeblich gesucht: `docs.italia.it` (Schede basi
di dati di interesse nazionale), AgID Linee Guida Open Data, `registroimprese.it`.
**Offene Flanke:** Die AgID-Leitlinien wurden nicht im Volltext geöffnet.

## IT.6 Gesellschafterliste — Italien liefert sie im Auszug mit

Das *libro soci* und die jährliche *elenco soci*-Hinterlegung wurden 2009 für die S.r.l.
abgeschafft; die Publizität wanderte ins Register.

> „*la soppressione dell'obbligo della tenuta del libro soci per le Srl*" (Art. 16 c. 12-septies) ·
> „*la soppressione dell'obbligo di deposito (o di conferma) dell'elenco dei soci presso il Registro
> delle imprese*" (Art. 16 c. 12-octies) · „*trasferisce al Registro Imprese la competenza in materia
> di pubblicità della compagine sociale*"
> — Camera di Commercio di Pisa (amtlich),
> `https://www.pi.camcom.it/camera/862/SRL-abolizione-libro-soci-e-nuovi-adempimenti.html`,
> Abruf 2026-07-30

Normattiva bestätigt den Änderungsbefehl zu Art. 2478-bis c.c.:
„*le parole: 'libro dei soci' sono sostituite dalle seguenti: 'registro delle imprese'*"
(`https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2008-11-29;185~art16`) —
**Konfidenz mittel**, die Seite lieferte nur ein Fragment.

**Der schlagende Beleg dafür, dass die Gesellschafter im Standardauszug stehen**, ist die
Preisliste selbst: sie führt eine eigene Variante **ohne** Gesellschafterliste.
> „*Visura ordinaria società di capitali 1,85 / 1,40*" vs.
> „*Visura ordinaria società di capitali **senza elenco soci** 1,30 / 1,40*" ·
> „*Visura storica società di capitali senza elenco soci 1,73 / 1,70*"
> — Allegato 1

Zusätzlich einzeln abrufbar als „*Visura soci e titolari di diritti su quote e azioni*"
(€ 2,00 sportello / € 0,45 remoto).

Ein *elenco soci*-Hinterlegungstatbestand besteht fort (S.p.A. mit dem Jahresabschluss):
> „*2 Deposito bilancio ed elenco soci — 2.1 su supporto informatico digitale € 90,00 —
> 2.2 modalità telematica € 60,00*" — Tabella A.
**Konfidenz: hoch** für den Fortbestand, **niedrig** für die genaue Rechtsformabgrenzung
(nicht aus dem Gesetzestext verifiziert).

**Ergebnis für die drei STP-Dokumentarten:**
Registerauszug ✅ € 5,00 / € 1,40 · Gesellschaftsvertrag ✅ als *statuto* / *copia atti* PDF
€ 3,50 / € 0,85 · Gesellschafterliste ✅ **im Auszug enthalten**.
**Italien ist damit die vollständigste der drei Jurisdiktionen.**

## IT.7 Quellentabelle Italien

| # | Quelle | Art | URL | Abruf |
|---|---|---|---|---|
| IT-1 | Telemaco-AGB (aktuell) | Betreiber, Vertrag | `https://registroimprese.infocamere.it/` (Registrierungsfluss) | 2026-07-30 |
| IT-2 | Telemaco-Vertrag 2012 | Betreiber, Vertrag | `https://www.registroimprese.it/dama/comc/comc/IT/registraServizi/CONTRATTO_TELEMACO_LIGHT_pc.pdf` | 2026-07-30 |
| IT-3 | Area utente (SPID-Pflicht, Gratisregistrierung) | Betreiber | `https://www.registroimprese.it/area-utente` | 2026-07-30 |
| IT-4 | **Tabella A — diritti di segreteria** (GU 149/2023) | amtl. Gebührenordnung | `https://www.mimit.gov.it/images/stories/normativa/TABELLA_A.pdf` | 2026-07-30 |
| IT-5 | Dekret MIMIT/MEF 20.04.2023 | Ministerium | `https://www.mimit.gov.it/it/normativa/decreti-interministeriali/decreto-interministeriale-mimit-e-mef-20-aprile-2023` | 2026-07-30 |
| IT-6 | Listino Telemaco | Betreiber | `https://registroimprese.infocamere.it/documents/20182/3303865/listino+telemaco/731e68a1-2e69-4ecc-a8d8-82e75deb5597` | 2026-07-30 |
| IT-7 | ABDO API-Seite | Betreiber | `https://accessoallebanchedati.registroimprese.it/abdo/api` | 2026-07-30 |
| IT-8 | **Contratto di accesso alle banche dati** (Art. 5, 6, 13, 14, 15) | Betreiber, Vertrag | `https://intranet.infocamere.it/documents/10193/72493596/1+Contratto+di+accesso.pdf` | 2026-07-30 |
| IT-9 | Allegato 1 — Tarife, Kanoni, Formate | Betreiber, Vertrag | `…/2%20Contratto%20di%20accesso%20-%20Allegato%201.pdf` | 2026-07-30 |
| IT-10 | Allegato 2 — Requisiti dell'operatore | Betreiber, Vertrag | `…/3+Contratto+di+accesso+-+Allegato+2.pdf` | 2026-07-30 |
| IT-11 | Allegato 3 — Specifiche Tecniche (AIWS/REST, IP-Whitelist) | Betreiber, Vertrag | `…/4+Contratto+di+accesso+-+Allegato+3.pdf` | 2026-07-30 |
| IT-12 | Auslandsportal AGB (**Weitergabeverbot**) | Betreiber | `https://italianbusinessregister.it/term-and-conditions-use` | 2026-07-30 |
| IT-13 | Auslandsportal Ablauf & Preise | Betreiber | `https://italianbusinessregister.it/en/home`, `/en/company-report` | 2026-07-30 |
| IT-14 | Agenzia delle Entrate, Risoluzione 203/E/2009 (IVA) | Behörde | `https://www.agenziaentrate.gov.it/portale/documents/20143/305631/Ris+203+del+5+08+2009_...pdf` | 2026-07-30 |
| IT-15 | CCIAA Pisa — Abschaffung libro soci / elenco soci | Kammer (amtlich) | `https://www.pi.camcom.it/camera/862/SRL-abolizione-libro-soci-e-nuovi-adempimenti.html` | 2026-07-30 |
| IT-16 | Normattiva D.L. 185/2008 Art. 16 | Gesetzestext | `https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2008-11-29;185~art16` | 2026-07-30 |
| IT-17 | InfoCamere — impresa.italia.it (nur eigene Firma) | Betreiber | `https://www.infocamere.it/tutte-le-soluzioni/impresa-italia.html` | 2026-07-30 |

## IT.8 Dead Ends Italien

**HTTP-Fehler / nicht erreichbar:**
- `https://www.eid.gov.it/en` — **403** → eIDAS-Frage bleibt unbelegt
- `https://italianbusinessregister.it/en/registrazione`, `/en/faq`, `/en/terms-of-use` — **404**
- `https://sso.infocamere.it/auth/realms/PIFE/login-actions/registration?...` — **400**
  (Keycloak-`tab_id` abgelaufen) → **Feldliste der Auslandsregistrierung unbelegt**
- `https://cciaato.infocamere.it/registrazione-telemaco` — **DNS-Fehler**
- `https://www.gazzettaufficiale.it/atto/…009G0008` — **falscher Rechtsakt** geliefert
  (L. 220/2008 statt L. 2/2009) → Volltext Art. 16 L. 2/2009 nicht direkt aus der GU belegt
- `https://www.registroimprese.it/chi-siamo` — nur Navigationsgerüst
- `https://impresa.italia.it/` — leere Antwort (JS-Wall)

**Technischer Hinweis zur Belastbarkeit der Zahlen:** Sechs PDFs (Telemaco-AGB, Listino,
Tabella A, Operatorvertrag + Allegati 1/2/3, Risoluzione 203/E) waren über das Fetch-Tool
nicht lesbar und wurden lokal extrahiert. Der *Listino Telemaco* hat in naiver
Textextraktion einen **systematischen Spaltenversatz um eine Zeile**; alle Preise wurden
koordinatenbasiert neu extrahiert und gegen die amtliche Tabella A gegengeprüft.

**Nicht belegbar:**
1. eIDAS-Login am Kammerportal — **UNBELEGT**
2. „Web Telemaco 250 € + IVA" — **WIDERLEGT** als offizieller Preis
3. Pflichtfelder der Auslandsregistrierung — **unbelegt**
4. Ob eine deutsche GmbH ohne italienische Eintragung Operatore werden kann — **offen,
   muss bei InfoCamere erfragt werden**
5. Aktualität des Operatorvertrags (vor-DSGVO-Verweise) — **unbelegt**; aktuelle Fassung
   nicht öffentlich
6. ABDO-API-Referenzdoku — nur in der *Area Riservata* nach Vertragsschluss
7. S.p.A.-*elenco soci*-Pflicht heute — nur indirekt über die Gebührentabelle
8. Open-Data-Lizenz — keine gefunden

---
---

# SPANIEN — Registro Mercantil / CORPME

## ES.1 Registerbetreiber und offizielles Portal

| | |
|---|---|
| Register | Registro Mercantil — geführt von den **provinzialen Registros Mercantiles** (Registradores) |
| Zentralregister | Registro Mercantil Central (RMC) — Firmennamen, zentrale Indizes |
| Standesorganisation / Portalbetreiber | **Colegio de Registradores de la Propiedad, Mercantiles y de Bienes Muebles de España (CORPME)**, NIF Q-2863012-G |
| Sede electrónica | `https://sede.registradores.org` |
| Sitz | Príncipe de Vergara 70, 28006 Madrid · Tel. 912701796 · soporte.usuarios@corpme.es |

**Wesentlicher Strukturunterschied zu IT und LU:** Es gibt keinen einzelnen Registerbetreiber.
Die Urkunde erstellt jeweils der **örtlich zuständige Registrador** als Amtsträger; CORPME
betreibt lediglich das gemeinsame elektronische Zugangsportal. Das ist der Grund, warum
Spanien weder eine zentrale Gebührenseite noch ein zentrales Entwicklerportal hat.

**Beleg (gesetzliche Grundlage der Sede, von CORPME selbst zitiert):**
> „*Artículo 240 párrafo primero de la Ley Hipotecaria: Los registradores dispondrán de una sede
> electrónica general y única a nivel nacional cuya titularidad, desarrollo, gestión y
> administración corresponderá al Colegio de Registradores de la Propiedad Mercantiles y de
> Bienes Muebles de España, disponible para las personas a través de redes de comunicación y por
> medio de la cual puedan, en sus relaciones con los Registros, presentar, tramitar y acceder a
> toda la información y a los servicios registrales disponibles.*"
> — `https://sede.registradores.org/sede/sede-corpme-web/la-sede/info/normativa-reguladora`,
> Abruf 2026-07-30

**Beleg (Inhaberschaft der Sede):**
> „*Titular: COLEGIO DE REGISTRADORES DE LA PROPIEDAD Y MERCANTILES DE ESPAÑA (en adelante,
> „CORPME"). NIF: Q-2863012-G*"
> — `https://sede.registradores.org/sede/sede-corpme-web/information/aviso-legal`, Abruf 2026-07-30

**Welches Portal liefert was** (selbst am 2026-07-30 auf der Startseite verifiziert). Der
Bereich „Mercantil" führt genau diese Dienste:
> „*Nota informativa mercantil · Depósito de cuentas · Informe sobre la posición de riesgo ·
> Informe de pronóstico de viabilidad · Certificaciones · Sociedad con Cuentas depositadas ·
> Consulta de Titularidades Reales · Presentación telemática · Estadísticas a medida*"
> — `https://sede.registradores.org/sede/sede-corpme-web/home`, Fußbereich, Abruf 2026-07-30

Daneben verlinkt die Sede ein **offenes Datenportal**: `https://opendata.registradores.org/`.

> **Nicht geprüft:** die Abgrenzung zwischen `rmc.es` (Registro Mercantil Central) und den
> provinzialen Registern wurde in diesem Durchgang **nicht** an einer Primärquelle verifiziert.
> Die Aussage „RMC liefert Firmennamen/Denominaciones, die Provinzregister die
> Publicidad formal" ist damit **UNBELEGT**.

**Konfidenz: hoch** für CORPME/Sede und die Dienstliste; **niedrig** für die RMC-Abgrenzung.

## ES.2 Zugang — die härteste Zugangshürde der drei Länder

Die Sede akzeptiert genau drei Identifikationssysteme:
> „*Sistemas de identificación y firma aceptados*
> *Certificado Electrónico — Los certificados electrónicos, son de uso general y por lo tanto
> universales, es decir, cada ciudadano puede comunicarse con las diferentes administraciones con
> un único certificado.*
> *Cl@ve — Cl@ve es un sistema para identificarte electrónicamente en las relaciones con las
> Administraciones Públicas.*
> *Usuario abonado — Si usted es usuario abonado, acceda con su usuario y contraseña. Le sugerimos
> que si cuenta con un certificado electrónico, acceda con él para realizar sus trámites.*"
> — `https://sede.registradores.org/sede/sede-corpme-web/login`, Abruf 2026-07-30

Auf derselben Seite steht der Registrierungseinstieg: „*¿Eres nuevo? registrate aquí*".

**Und hier liegt das Problem. Der Link führt auf:**
`https://sede.registradores.org/site/alta/alta-abonado/noidt` (Titel: „Alta de nuevo cliente" /
„Abonarse"). Dort steht:

> „***Es imprescindible la identificación con certificado electrónico o Cl@ve para realizar este
> trámite.***"
> — `https://sede.registradores.org/site/alta/alta-abonado/noidt`, Abruf 2026-07-30

**Das heißt:** Der Nutzer/Passwort-Zugang („usuario abonado") ist zwar der Dauerzugang —
**aber um ihn überhaupt zu beantragen, braucht man vorher ein spanisches
certificado electrónico oder Cl@ve.** Es gibt keine Selbstregistrierung per E-Mail und
keinen erkennbaren Gelegenheitsnutzer-Weg mit bloßer Kreditkarte.

| Punkt | Antwort | Beleg |
|---|---|---|
| Reicht eine Registrierung? | Ja im Prinzip („alta de abonado"), aber nur mit vorheriger elektronischer Identifikation | Alta-Seite |
| Vertrag nötig? | Für das Portal: nein. Für die API: ja, mit technischer Entwicklung (ES.4) | API-Seite |
| Welche Nachweise? | certificado electrónico **oder** Cl@ve | Alta-Seite |
| Beschränkung für Ausländer? | **Faktisch ja.** Cl@ve setzt spanische Identität voraus; ein Zertifikat einer spanischen Zertifizierungsstelle (z. B. FNMT) setzt regelmäßig NIF/NIE voraus | siehe Vorbehalt |
| Registrierungs-URL | `https://sede.registradores.org/site/alta/alta-abonado/noidt` | selbst geprüft |

> **Ausdrücklicher Vorbehalt:** Ob ein **eIDAS**-Zertifikat aus Deutschland an der Sede
> akzeptiert wird, ist **UNBELEGT**. Die Seite „Sistemas de identificación y firma aceptados"
> spricht allgemein von „*certificados electrónicos … de uso general y por lo tanto universales*",
> nennt aber keine ausländischen Aussteller und keine eIDAS-Norm. Die Detailseiten
> („Más información", „¿Qué certificado utilizar?") wurden **nicht** geöffnet.
> **Das ist die wichtigste offene Frage für Spanien** und sollte vor jeder Aufwandsschätzung
> geklärt werden — notfalls direkt bei `soporte.usuarios@corpme.es`.

**Konfidenz:** hoch für die drei Systeme und die Zertifikatspflicht bei der Alta;
**niedrig** für die Frage, ob eine deutsche GmbH diese Hürde ohne NIF nehmen kann.

## ES.3 Preise

**Maßgeblich ist der Arancel**, nicht eine Preisseite: Eine offizielle Preisliste für die
Publicidad formal existiert auf der Sede **nicht** (Startseite und Mercantil-Bereich am
2026-07-30 durchsucht: kein Treffer für „arancel", „tarifa", „precio", „IVA").

**Rechtsquelle:**
> „*Decreto 757/1973, de 29 de marzo, por el que se aprueba el adjunto Arancel de los
> Registradores Mercantiles.* … *«BOE» núm. 93, de 18 de abril de 1973* … *TEXTO CONSOLIDADO —
> Última modificación: 17 de noviembre de 2011*"
> — `https://www.boe.es/buscar/act.php?id=BOE-A-1973-561` (konsolidiertes PDF:
> `https://www.boe.es/buscar/pdf/1973/BOE-A-1973-561-consolidado.pdf`), Abruf 2026-07-30

### Die für uns relevanten Positionen — wörtlich

> „***Número 22*** *— Por la manifestación de cada asiento se devengarán 0,150253 euros.
> Por la expedición de nota simple informativa se devengarán **0,601012 euros por asiento**.*"

> „***Número 23*** *— Por la certificación de cualquier asiento del Registro, **1,502530 euros**,
> y sí la certificación comprende más de dos páginas, se cobrarán, además, por cada página que
> exceda 0,150253 euros.*"

> „***Número 24*** *— Por la certificación de no constar en el Registro determinado asiento o
> circunstancia, se devengarán 0,601012 euros.*
> *Por la busca para manifestaciones, notas simples o certificaciones, cuando no se determinen los
> datos registrales o se expresen con error, se devengará el 10 por 100 de los derechos que
> correspondan con arreglo al número 5 con un mínimo de 0,300506 euros y un máximo de
> 1,502530 euros.*"

> „***Disposición adicional tercera*** *— Cuando a solicitud del presentante o interesado … se
> expida una certificación en plazo inferior a dos días, se devengará por concepto de urgencia el
> 20 por 100 de los derechos que correspondan con un tope máximo de 12,020242 euros.*"

Generelle Ermäßigung (gilt für die Skala nach Número 5, also **nicht** direkt für die
Publicidad formal):
> „*se aplicará una rebaja del 5 por 100 del importe del arancel a percibir por el registrador
> mercantil. Esta rebaja también se llevará a cabo, en todo caso, en los supuestos previstos en
> los números siguientes en los que el arancel resulte de la aplicación de la escala prevista en
> este número 5 y con carácter adicional a los demás descuentos y rebajas previstos en la
> normativa vigente.*"

### Was das für unsere bisherige Annahme „nota simple ~6–9 € + MwSt" bedeutet

**Die Zahl steht so nirgends im Arancel.** Der Arancel kennt keinen Stückpreis für eine
Nota simple, sondern **0,601012 € je *asiento*** (je Registereintragung). Der Endbetrag
hängt also davon ab, wie viele Eintragungen eine Gesellschaft hat. Bei 10–15 Eintragungen
landet man rechnerisch bei 6–9 € — die Größenordnung unserer Notiz ist damit **plausibel,
aber nicht als Festpreis belegt**. Für die Kalkulation heißt das: **Spanien hat als
einziges der drei Länder keinen kalkulierbaren Stückpreis** — die Kosten skalieren mit dem
Alter und der Änderungshistorie der Zielgesellschaft.

**Zuordnung zu den STP-Dokumentarten:**

| Dokumentart | ES-Entsprechung | Preis laut Arancel |
|---|---|---|
| **Registerauszug** | *nota simple informativa mercantil* | 0,601012 €/asiento (netto) |
| **beglaubigter Auszug** | *certificación* | 1,502530 € + 0,150253 €/Seite ab Seite 3 |
| **Gesellschaftsvertrag** | *estatutos* — Teil der hinterlegten Urkunde | **kein eigener Arancel-Posten gefunden** |
| **Jahresabschluss** | *cuentas anuales depositadas* | **kein eigener Arancel-Posten gefunden** |

> **UNBELEGT:** Für die Kopie hinterlegter Urkunden (*estatutos*, *cuentas anuales*) wurde
> **kein** Arancel-Posten identifiziert. Die Positionen 22–24 betreffen *asientos*
> (Registereintragungen), nicht die im Register archivierten Dokumente. Vergeblich gesucht:
> gesamter konsolidierter Arancel-Text (Stichworte „telem", „cuentas anuales", „depósito de las
> cuentas", „internet"), Sede-Startseite, Mercantil-Bereich. **Diese Lücke ist erheblich, weil
> der Gesellschaftsvertrag eine unserer drei Kerndokumentarten ist.**

### Netto/Brutto

Der Arancel nennt **keine** Umsatzsteuer (Volltextsuche „IVA", „Impuesto": kein Treffer im
materiellen Teil). Die Beträge sind damit **netto**; die spanische IVA von 21 % kommt nach
allgemeinem Recht hinzu.
**Konfidenz: mittel** — die Netto-Eigenschaft folgt aus dem Schweigen des Arancel, nicht aus
einer ausdrücklichen Aussage. Ein Beleg wie die italienische *Risoluzione 203/E* fehlt für
Spanien.

## ES.4 API

**Es gibt sie, sie ist bestätigt, und sie ist ausdrücklich für Hochvolumen-Abnehmer gedacht —
aber sie liefert etwas anderes, als wir angenommen haben.**

**Der Betreiber bestätigt die „sistemas apificados" wörtlich:**
> „*¿Existe algún servicio que permita la petición automatizada de información registral?*
> *Sí, el Colegio de Registradores ha desarrollado, tanto para los Registros de la Propiedad como
> para los Mercantiles, **sistemas apificados** que facilitan el proceso de petición automatizada
> de información a los Registros competentes, siendo los registradores quienes, conforme a la
> legislación aplicable, emiten dicha información **en forma de nota simple o certificación**.*
> *Se trata de un mecanismo que se pone a disposición de cualquier entidad que lo desee y tenga
> previsto realizar **un volumen muy alto de peticiones diarias**. Para garantizar los niveles de
> seguridad precisos para el desarrollo de la función registral, este servicio requiere la
> implementación de **desarrollos técnicos específicos**.*
> *Si cree que le puede interesar el servicio, o tiene dudas sobre las especificaciones técnicas
> requeridas o cualquier otra cuestión, por favor póngase en contacto con nosotros en la siguiente
> dirección de correo: **api@corpme.es***"
> — `https://sede.registradores.org/sede/sede-corpme-web/la-sede/info/peticion-automatizada-ambito-registral`,
> Abruf 2026-07-30

**Die entscheidende Präzisierung:** Der Text sagt „*en forma de nota simple o certificación*" —
also **Registerauskünfte**, die der Registrador ausstellt. Er sagt **nicht**, dass hinterlegte
Urkunden (*estatutos*, *cuentas anuales*) über diesen Kanal ausgeliefert werden.
**Unsere bisherige Eintragung `documentsViaApi: true` mit „notas simples, certificaciones,
cuentas anuales, estatutos" ist damit in der zweiten Hälfte nicht belegt.**

**Zweiter Kanal — Punkt-zu-Punkt-Anbindung, aber nur für die Einreichung:**
> „*Presentacion telemática integrada — Las redes telemáticas corporativas del Colegio de
> Registradores permiten a aquellos usuarios que hagan un uso intensivo de las mismas para la
> presentación telemática de documentos a los Registros … establecer Punto a Punto conexiones
> telemáticas que aumenten la eficiencia de dichos procesos.*
> *Se trata de una vía de acceso telemática abierta a cualquier usuario que pueda afrontar los
> desarrollos técnicos necesarios para el establecimiento de dicha conexión.*"
> — dieselbe Seite

Das ist der **Einreichungs**-Kanal (Dokumente ins Register), nicht der Abrufkanal — für uns
irrelevant.

**Dokumentation: existiert nicht öffentlich.** Es gibt kein Entwicklerportal, keine
OpenAPI-Spezifikation, keine öffentlichen Endpunkte. Der einzige veröffentlichte Zugangsweg
ist die **E-Mail-Adresse `api@corpme.es`**. Geprüft: `sede.registradores.org` (Startseite,
Login, La-Sede-Bereich, Fußnavigation vollständig), die Seite „Peticiones automatizadas"
selbst, „Normativa reguladora". **Authentifizierungsverfahren, Protokoll, Formate, Rate
Limits und Preise der API sind UNBELEGT.**

**Nicht geprüft (Restrisiko):** `https://opendata.registradores.org/` — das offene Datenportal
wurde nur als Link gesehen, nicht geöffnet. Ebenso wenig der **BRIS/e-Justice**-Weg über das
europäische Registerverbundsystem. Beides kann für uns relevant sein und ist hier
**ausdrücklich offen**.

**Konfidenz:** hoch für Existenz, Zielgruppe, Kontaktweg und Ausgabeformat
(*nota simple / certificación*); **keine Aussage möglich** zur Technik; **niedrig** für die
Frage, ob hinterlegte Urkunden über die API erhältlich sind.

## ES.5 Weitergaberecht — restriktivste Klausel der drei Länder

Der Aviso legal der Sede ist eindeutig und für unser Geschäftsmodell ungünstig.

**Bindungswirkung — schon durch bloßes Aufrufen:**
> „*El acceso, navegación y utilización de la Sede Electrónica atribuye al visitante la condición
> de usuario …, implicando la aceptación expresa y sin reservas de todos los términos del presente
> Aviso Legal, teniendo la misma validez y eficacia que cualquier contrato celebrado por escrito
> y firmado.*"

**Nutzungsrecht nur im häuslichen Bereich:**
> „*Al acceder a la Sede Electrónica, el Usuario adquiere un derecho de uso de los contenidos y/o
> servicios de la Sede Electrónica **dentro de un ámbito doméstico** y únicamente con la finalidad
> de disfrutar de las prestaciones del servicio de acuerdo con el presente Aviso Legal.*"

**Das ausdrückliche Verbot:**
> „*Quedan reservados todos los derechos de propiedad intelectual e industrial sobre los Contenidos
> del Sitio Web y, en particular, **queda prohibido modificar, copiar, reproducir, comunicar
> públicamente, poner a disposición, transformar o distribuir, por cualquier medio y bajo cualquier
> forma, la totalidad o parte de los contenidos incluidos en el mismo, para propósitos públicos o
> comerciales, si no se cuenta con autorización previa, expresa y por escrito de CORPME** o, en su
> caso, del titular de los derechos correspondientes.*"

> „*Asimismo, queda prohibido suprimir o manipular las indicaciones de copyright u otros créditos
> que identifiquen a los titulares de derechos de los contenidos de la Sede Electrónica, así como
> los dispositivos técnicos de protección, las huellas digitales, o cualquier mecanismo de
> protección o información incorporada a los mismos.*"

> Alle drei Zitate: `https://sede.registradores.org/sede/sede-corpme-web/information/aviso-legal`,
> Abschnitt „Derechos de propiedad intelectual e industrial", Ziff. 4.1, Abruf 2026-07-30

**Bewertung:** Anders als in Luxemburg ist das **kein** bloßer Website-Copyright-Hinweis,
sondern eine als Vertrag ausgestaltete Nutzungsbeschränkung, die (a) den Zweck auf
*ámbito doméstico* begrenzt und (b) kommerzielle Weitergabe **ausdrücklich** von einer
vorherigen schriftlichen Genehmigung von CORPME abhängig macht. Das ist von der Struktur
her wie Italien: **Portalzugang = keine Weitergabe; Weitergabe nur mit gesondertem
Vertrag.** Praktisch bedeutet das: **Der API-/Vertragsweg über `api@corpme.es` ist für
Spanien nicht optional, sondern die Voraussetzung des Geschäftsmodells.**

**Nicht belegt:** Ob die Klausel auf die vom Registrador ausgestellte *nota simple* selbst
durchschlägt (die als amtliche Urkunde dem Antragsteller ausgehändigt wird) oder nur auf die
Portalinhalte, ist Auslegung. Ebenfalls **nicht geprüft**: das Erfordernis eines
*interés legítimo* für die Publicidad formal (Art. 12 RRM) und die datenschutzrechtlichen
Weitergabegrenzen. **Beides sollte vor einer Spanien-Entscheidung juristisch geklärt werden.**

**Konfidenz: hoch** für den Wortlaut; **mittel** für die Reichweite.

## ES.6 Gesellschafterliste — in diesem Durchgang nicht belegt

Unsere Arbeitshypothese lautet, dass das *Libro Registro de Socios* bei der Gesellschaft
geführt wird (LSC Art. 104/105) und deshalb **nicht** aus dem Registro Mercantil erhältlich
ist, während der *socio único* (LSC Art. 13/14) eintragungspflichtig ist.

**Diese Hypothese wurde hier NICHT verifiziert.** Der Gesetzestext der Ley de Sociedades de
Capital wurde in diesem Durchgang nicht geöffnet. Die Aussage ist damit **UNBELEGT** und
darf nicht in `registry_intelligence.json` übernommen werden, bevor der BOE-Text
(RDL 1/2010) zitiert vorliegt.

Immerhin bietet die Sede im Bereich Mercantil den Dienst „*Consulta de Titularidades
Reales*" an (wirtschaftlich Berechtigte) — das ist ein **anderes** Produkt als eine
Gesellschafterliste und ersetzt sie nicht.
**Konfidenz: niedrig, bewusst offen gelassen.**

## ES.7 Quellentabelle Spanien

| # | Quelle | Art | URL | Abruf |
|---|---|---|---|---|
| ES-1 | Sede electrónica, Startseite + Dienstliste Mercantil | Betreiber | `https://sede.registradores.org/sede/sede-corpme-web/home` | 2026-07-30 |
| ES-2 | **Aviso legal** (Weitergabeverbot, Ziff. 4.1) | Betreiber | `https://sede.registradores.org/sede/sede-corpme-web/information/aviso-legal` | 2026-07-30 |
| ES-3 | **Peticiones automatizadas en el ámbito registral** (API) | Betreiber | `https://sede.registradores.org/sede/sede-corpme-web/la-sede/info/peticion-automatizada-ambito-registral` | 2026-07-30 |
| ES-4 | Normativa reguladora (Art. 240 LH) | Betreiber / Gesetz | `https://sede.registradores.org/sede/sede-corpme-web/la-sede/info/normativa-reguladora` | 2026-07-30 |
| ES-5 | Login / Sistemas de identificación y firma aceptados | Betreiber | `https://sede.registradores.org/sede/sede-corpme-web/login` | 2026-07-30 |
| ES-6 | **Alta de nuevo cliente / Abonarse** (Zertifikatspflicht) | Betreiber | `https://sede.registradores.org/site/alta/alta-abonado/noidt` | 2026-07-30 |
| ES-7 | **Arancel de los Registradores Mercantiles**, konsolidiert | amtl. Gebührenordnung | `https://www.boe.es/buscar/act.php?id=BOE-A-1973-561` · PDF: `https://www.boe.es/buscar/pdf/1973/BOE-A-1973-561-consolidado.pdf` | 2026-07-30 |

## ES.8 Dead Ends und offene Punkte Spanien

**Technische Hürden:**
- `sede.registradores.org` ist eine **Angular-SPA**; einfaches Abrufen liefert nur das
  Grundgerüst. Alle Zitate stammen aus einer Browser-Sitzung mit DOM-Auslesung.
- Ein **Cookie-Banner** überlagert die Seite. Es wurde **nicht** akzeptiert; das Overlay wurde
  lediglich lokal ausgeblendet, um den darunterliegenden Text zu lesen. Es wurden keine
  Cookies bestätigt und keine Einwilligung erteilt.
- `https://www.boe.es/buscar/act.php?id=BOE-A-1973-540` — **falscher Rechtsakt** (Feiertagskalender
  1973). Die korrekte Kennung ist BOE-A-1973-**561**.
- Direkte URL-Raterei für Unterseiten (`…/informacion-y-ayuda/info/sistemas-identificacion-firma-aceptados`,
  `…/site/mercantil`) führt zu **stillen Weiterleitungen auf die Startseite**; die Navigation
  funktioniert nur über die SPA-Links.

**Abgebrochen (bewusst):** Auf der Alta-Seite wurde **nicht** auf „Acceder" geklickt — das
wäre eine Registrierung gewesen. Es wurde keine Bestellung ausgelöst, weshalb auch **kein
Live-Preis** für eine konkrete Nota simple beobachtet werden konnte.

**Nicht belegt / offen:**
1. **eIDAS-Akzeptanz** für deutsche Zertifikate an der Sede — **die wichtigste offene Frage**
2. Ob ein deutsches Unternehmen ohne NIF/NIE überhaupt „abonado" werden kann
3. **Arancel-Posten für Kopien hinterlegter Urkunden** (*estatutos*, *cuentas anuales*) —
   nicht auffindbar
4. Ob die API hinterlegte Urkunden liefert (Wortlaut spricht nur von *nota simple / certificación*)
5. Technische Spezifikation, Auth-Verfahren und Preise der API
6. Abgrenzung RMC (`rmc.es`) ↔ Provinzregister
7. `opendata.registradores.org` — nicht geöffnet
8. **BRIS / e-Justice**-Weg — nicht geprüft
9. *Interés legítimo* nach Art. 12 RRM als Voraussetzung der Publicidad formal — nicht geprüft
10. Gesellschafterliste / LSC Art. 104-105, 13-14 — nicht geprüft
11. IVA-Behandlung — nur aus dem Schweigen des Arancel gefolgert

> **Spanien ist damit das am schlechtesten belegte der drei Länder.** Die Konfidenz steigt
> gegenüber dem Ausgangsstand bei **Zugang, Weitergaberecht und API-Existenz** deutlich
> (jeweils mit wörtlichem Primärbeleg), bleibt aber bei **Preisen für Urkunden** und
> **Auslandstauglichkeit** niedrig. Diese beiden Lücken sind vor einer Investitionsentscheidung
> zu schließen — am schnellsten durch eine Anfrage an `api@corpme.es` und
> `soporte.usuarios@corpme.es`.

---
---

# GESAMTBEWERTUNG UND EMPFEHLUNG

## Vergleich der drei Jurisdiktionen

| Kriterium | 🇮🇹 Italien | 🇪🇸 Spanien | 🇱🇺 Luxemburg |
|---|---|---|---|
| Betreiber | Camere di Commercio / InfoCamere | CORPME + Provinzregistratoren | LBR g.i.e. |
| Portalzugang für dt. Firma | ✅ ohne SPID über `italianbusinessregister.it` | ⚠️ nur mit span. Zertifikat/Cl@ve | ✅ eIDAS ausdrücklich vorgesehen |
| API existiert | ✅ ABDO | ✅ „sistemas apificados" | ✅ plataforma électronique |
| API-Doku öffentlich | ❌ nur nach Vertrag | ❌ nur `api@corpme.es` | ❌ keine |
| API liefert Dokumente | ✅ (Atti als PDF) | ❓ nur *nota simple/certificación* belegt | ✅ (Art. 22 (2): *documents publics déposés*) |
| Registerauszug | € 5,00 / € 1,40 (Operator) | 0,601012 €/asiento | € 10,43 |
| Satzung | € 3,50 / € 0,85 | ❓ kein Arancel-Posten gefunden | **€ 0,00** |
| Gesellschafterliste | ✅ im Auszug enthalten | ❓ vermutlich nicht im Register | ✅ im Auszug (S.à r.l.) |
| Weitergabe ohne Vertrag | ❌ ausdrücklich verboten | ❌ ausdrücklich verboten | ⚠️ „nur nicht-kommerziell" |
| Weitergabe mit Vertrag | ✅ ausdrücklich geregelt (Art. 5) | ❓ „autorización previa" nötig | ⚠️ über *finalités* zu regeln |
| Fixkosten p. a. | ~12.000 € + 13.000 € einmalig | unbekannt | **5.000 €** |
| Konfidenz gesamt | **hoch** | **mittel** | **hoch** |

## Die drei Erkenntnisse, die die Strategie ändern

**1. „Kostenlos" gibt es nur in Luxemburg — und nur für hinterlegte Dokumente.**
LU liefert Satzung und Jahresabschluss zum Nulltarif; nur der amtliche Auszug kostet.
Das macht Luxemburg **pro Dokument** zum günstigsten der drei Märkte — aber nur über den
Portalweg, der maschinell verboten ist. Wer automatisieren will, zahlt 5.000 €/Jahr.
Das ist immer noch der **mit Abstand günstigste API-Einstieg** der drei Länder.

**2. Alle drei Länder verbieten die Weitergabe auf dem billigen Weg.**
Das ist das eigentliche Ergebnis dieses Dossiers. IT und ES verbieten sie wörtlich,
LU beschränkt sie auf nicht-kommerzielle Zwecke. **Der Vertragsweg ist in keinem der drei
Länder optional** — er ist die Geschäftsgrundlage. Jede Kalkulation, die mit Portalpreisen
ohne Vertragskosten rechnet, ist falsch.

**3. Italien ist inhaltlich der stärkste Markt, Spanien der schwächste.**
Italien liefert alle drei Dokumentarten, hat einen ausdrücklich geregelten
Distributionsvertrag und amtlich belegte Preise. Spanien hat als einziges Land **keinen
kalkulierbaren Stückpreis** (Preis skaliert mit der Zahl der *asientos*), keine belegte
Urkundengebühr und eine faktische Zugangshürde für ausländische Antragsteller.

## Empfohlene Reihenfolge

1. **Luxemburg zuerst.** Beste Konfidenz, klarster Rechtsrahmen, niedrigste Fixkosten
   (5.000 €/Jahr), Dokumentenlieferung per API gesetzlich zugesichert, Gesellschafterliste
   für S.à r.l. inklusive. Nächster Schritt: Antrag nach Art. 22 (2) RGD mit ausdrücklicher
   Angabe der *finalités de la réutilisation* (Weitergabe an KYC-pflichtige Kunden).
2. **Italien parallel.** Höchster inhaltlicher Wert, aber fünfstellige Einstiegskosten,
   dedizierte Leitung und die ungeklärte Frage der *iscrizione al Registro delle Imprese*
   für einen ausländischen Operator. Vor Budgetierung: InfoCamere kontaktieren.
3. **Spanien zuletzt.** Erst die vier offenen Fragen klären (eIDAS-Akzeptanz,
   Urkundengebühren, API-Leistungsumfang, Weitergabegenehmigung), bevor Aufwand geschätzt
   wird. Einstiegskontakt: `api@corpme.es`.

## Was dieses Dossier NICHT leistet

- Keine Preise wurden durch eine echte Bestellung verifiziert — es wurde nichts bestellt.
- Kein Konto wurde angelegt, keine AGB akzeptiert, kein CAPTCHA gelöst. Wo der Weg dort
  endete, ist das dokumentiert.
- Die technischen API-Spezifikationen aller drei Länder liegen hinter Verträgen und sind
  **in keinem** der drei Fälle belegt.
- Sämtliche Aussagen zu Rechtsfolgen sind Auslegung von zitiertem Text, keine Rechtsberatung.
