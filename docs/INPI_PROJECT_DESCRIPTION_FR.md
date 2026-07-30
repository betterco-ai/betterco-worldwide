# INPI RNE — description du projet de réutilisation (demande d'accès API)

*Rédigé sous les termes de la « Licence de réutilisation des informations du RNE » (INPI, 2024),
homologuée aux articles L.323-2 / D.323-2-2 CRPA. Le texte ci-dessous reprend explicitement les
obligations des articles 2.4, 2.5, 3 et 4.4.*
*Deux versions : courte (champ de formulaire) et longue (annexe / demande détaillée).*
*⚠️ `[À COMPLÉTER]` = chiffres que je ne peux pas inventer — à remplir avant envoi.*

---

## Version courte — pour un champ de formulaire

> **Objet de la réutilisation.** BetterCo édite une solution logicielle de conformité (KYC / LCB-FT)
> destinée aux entités assujetties allemandes et européennes. Nous souhaitons accéder aux API du
> Registre National des Entreprises afin de mettre à la disposition de nos clients, de manière
> automatisée et fiable, les informations légales et les documents déposés relatifs à leurs
> contreparties françaises : données d'identité de l'entreprise (Base RNE), statuts et actes, et
> comptes annuels non confidentiels.
>
> **Usage.** Les appels sont effectués à la demande, entreprise par entreprise, à partir d'un
> numéro SIREN, dans le cadre d'un dossier de vigilance ouvert par un client. Il ne s'agit ni d'une
> collecte massive, ni de la constitution d'une base concurrente : les informations sont restituées
> au client à l'appui de son obligation légale de vigilance.
>
> **Modalités techniques.** Intégration serveur à serveur en REST/JSON, authentification par les
> identifiants techniques délivrés par l'INPI, exécution mono-thread avec temporisation entre les
> appels et gestion des codes 429/5xx. Volume estimé : [À COMPLÉTER] appels par an.
>
> **Respect de la licence.** Nous mentionnons systématiquement la source et la date de dernière
> mise à jour de l'information réutilisée (art. 2.4), sans suggérer une quelconque reconnaissance
> par l'INPI. Nous respectons les restrictions de critères de recherche de l'article A.123-69 du
> code de commerce (art. 2.5) : les recherches s'effectuent par SIREN ou par dénomination, jamais
> sur des critères relatifs aux personnes physiques. Les données à caractère personnel sont
> traitées conformément au RGPD et au livre III du CRPA (art. 3). Les documents sont restitués tels
> que délivrés par l'INPI, sans modification, avec leur date, afin de ne pas induire en erreur sur
> leur contenu, leur source ou leur date (art. 4.4).

---

## Short version, English — for a form field

> **Purpose of the reuse.** BetterCo provides compliance software (KYC / AML) for obliged entities in
> Germany and across Europe. We are requesting access to the Registre National des Entreprises APIs
> in order to supply our clients, automatically and reliably, with the legal information and filed
> documents concerning their French counterparties: company identity data (Base RNE), articles of
> association and filed deeds (actes), and non-confidential annual accounts.
>
> **Use.** Calls are made on demand, one company at a time, from a SIREN number, in the context of a
> due-diligence file opened by a client. This is neither bulk collection nor the building of a
> competing database: the information is passed to the client in support of their statutory
> due-diligence obligation.
>
> **Technical setup.** Server-to-server REST/JSON integration, authenticated with the technical
> identifiers issued by INPI, running single-threaded with throttling between calls and handling of
> 429/5xx responses. Estimated volume: [TO COMPLETE] calls per year.
>
> **Compliance with the licence.** We systematically state the source and the date of last update of
> the reused information (art. 2.4), without suggesting any endorsement by INPI. We respect the
> search-criteria restrictions of art. A.123-69 of the code de commerce (art. 2.5): searches are
> performed by SIREN or by company name, never on criteria relating to natural persons. Personal
> data is processed in accordance with the GDPR and livre III of the CRPA (art. 3). Documents are
> passed on exactly as delivered by INPI, unmodified and with their date, so as not to mislead as to
> their content, source or date (art. 4.4).

---

## Version longue — annexe / demande détaillée

### 1. Le réutilisateur

**[À COMPLÉTER : raison sociale exacte, forme juridique, siège, numéro d'immatriculation,
représentant légal, contact technique]**

BetterCo édite une solution logicielle de conformité destinée aux entités assujetties aux
obligations de lutte contre le blanchiment et le financement du terrorisme (LCB-FT) — notamment
établissements financiers, professions du chiffre et du droit, et autres professions réglementées.

### 2. Finalité de la réutilisation

Nos clients doivent, au titre de leur obligation légale de vigilance, identifier leurs contreparties
et en conserver la preuve documentaire. Lorsque la contrepartie est une société française, ils
doivent réunir l'équivalent des trois pièces qu'ils connaissent en droit allemand :

| Pièce attendue (droit allemand) | Équivalent français | Source |
|---|---|---|
| *Registerauszug* — extrait du registre | Extrait Kbis | **Infogreffe (payant) — pas l'INPI** |
| *Gesellschaftsvertrag* — statuts | Statuts (déposés parmi les actes) | **RNE / INPI** |
| *Gesellschafterliste* — liste des associés | Selon la forme sociale | RNE pour les SARL/SNC ; non probant pour les SAS/SA |

La difficulté que nous résolvons est une difficulté de correspondance : chaque pays nomme, tient et
publie ces pièces différemment. Notre réutilisation consiste à établir, par forme juridique, la
correspondance entre le document français réellement disponible et la pièce attendue par
l'assujetti, puis à lui restituer ce document.

Nous relevons expressément que **l'extrait Kbis n'est pas délivré par l'INPI** : il est obtenu
séparément auprès d'Infogreffe, à titre onéreux. Aucune information issue du RNE ne sera présentée
comme un extrait Kbis ni comme un document à valeur certifiée.

### 3. Accès demandés

- **Base RNE** — données d'identité et de situation de l'entreprise (JSON)
- **Actes** — documents déposés, en particulier les statuts (PDF)
- **Comptes annuels** — comptes non confidentiels (JSON et PDF)
- *le cas échéant* **SFTP** — pour des mises à jour incrémentales, en alternative à des appels
  unitaires répétés

### 4. Modalités techniques et volumétrie

- Intégration serveur à serveur, REST/JSON, authentification par identifiants techniques INPI
  (jeton de session, renouvelé en cas d'expiration)
- Appels **unitaires et à la demande**, déclenchés par l'ouverture d'un dossier client, à partir
  d'un SIREN
- Exécution **mono-thread**, temporisation entre appels, gestion des codes 429 et 5xx avec
  temporisation exponentielle — conformément aux recommandations d'usage de l'INPI
- Volume estimé : **[À COMPLÉTER]** appels/an, soit environ **[À COMPLÉTER]** par jour ouvré
- Pas d'aspiration systématique du registre, pas de reconstitution d'une base miroir destinée à
  concurrencer la mise à disposition publique

### 5. Engagements au titre de la licence

**Article 2.4 — paternité.** Chaque information et chaque document réutilisés sont restitués avec la
mention de leur source (« Registre National des Entreprises — INPI ») **et la date de dernière mise
à jour** de l'information réutilisée. Cette date est enregistrée au moment de l'appel et conservée
avec l'enregistrement, précisément pour pouvoir être affichée. Aucune mention ne suggère une
reconnaissance, une caution ou un caractère officiel conféré par l'INPI.

**Article 2.5 — critères de recherche.** Les restrictions de l'article A.123-69 du code de commerce
sont respectées : les recherches sont effectuées par numéro SIREN ou par dénomination sociale. Notre
interface **n'offre pas** de recherche par critères relatifs aux personnes physiques.

**Article 3 — données à caractère personnel.** Les données à caractère personnel contenues dans
l'information sont traitées conformément au RGPD et au livre III du CRPA. Leur traitement repose sur
l'obligation légale de vigilance pesant sur nos clients assujettis. Aucun usage contraire à ces
dispositions n'est effectué, et notamment aucun enrichissement à des fins de prospection.

**Article 4.4 — absence d'induction en erreur.** Les documents sont restitués **tels que délivrés
par l'INPI, sans modification**, accompagnés de leur date. Lorsqu'un document n'est pas disponible —
compte déclaré confidentiel, dépôt non numérisé, pièce non probante pour la forme sociale
considérée — cette indisponibilité est signalée comme telle, et non comblée par un document
approchant.

**Article 2.2 — communication aux clients.** Les documents obtenus sont transmis à nos clients
assujettis dans le cadre de leur dossier de vigilance. Nous relevons que l'article 2.2 de la licence
autorise expressément de « communiquer, diffuser, redistribuer, publier et transmettre »
l'information, et que l'article 1er inclut dans l'« Information » les documents communiqués ou reçus
par l'INPI.

### 6. Contact

**[À COMPLÉTER : contact technique — nom, e-mail, téléphone ; et contact administratif si
différent]**
