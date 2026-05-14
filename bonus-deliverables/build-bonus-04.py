#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for Bonus #4:
"Le Devis qui Close a 70% - Template Cialdini-ready, conforme legal 2026"
Carnet Plein(R) by Mad Makers - Edition 2026

Generates 04-devis-close-70.html in this folder.
Open in Chrome -> File > Print > Save as PDF (A4 portrait).
"""
import os

# ===========================================================
# DATA - LES 7 PRINCIPES CIALDINI APPLIQUES AU DEVIS BTP
# ===========================================================

CIALDINI = [
    {
        "num": "01",
        "name": "Réciprocité",
        "claim": "Donner avant de demander.",
        "why": (
            "Quand vous offrez quelque chose de valeur en amont du devis "
            "(audit gratuit, conseil pratique, mini-rapport thermique, "
            "PDF d'entretien), le prospect ressent une dette implicite. "
            "Robert Cialdini a documenté que ce déclencheur double la "
            "probabilité d'acceptation d'une demande qui suit. En BTP, c'est "
            "la différence entre un devis envoyé à froid et un devis envoyé "
            "après visite avec livrables remis main propre."
        ),
        "actions": [
            "Audit énergétique simplifié (1 page A4) remis en fin de visite",
            "Mini-guide PDF entretien chaudière offert avec le devis",
            "Photos de référence d'installations similaires (avant/après) jointes au devis",
            "Conseil pratique non commercial donné pendant la visite (« Vérifiez la pression du vase tous les 3 mois »)",
        ],
        "in_devis": (
            "Ajouter une ligne au début du devis : « Inclus avec ce devis : "
            "audit thermique simplifié de votre logement (valeur 150 € HT, "
            "offert), guide entretien PDF, 3 références de chantiers "
            "similaires sur demande »."
        ),
    },
    {
        "num": "02",
        "name": "Engagement et cohérence",
        "claim": "Petits oui qui mènent au grand oui.",
        "why": (
            "Une fois qu'une personne s'est engagée verbalement ou par écrit "
            "sur un point, elle a tendance à rester cohérente avec cet "
            "engagement. En BTP, c'est la séquence : visite acceptée -> "
            "diagnostic confirmé -> options validées une à une -> devis signé. "
            "Chaque micro-validation augmente l'inertie d'engagement vers la "
            "signature finale. Évitez de tout demander d'un coup."
        ),
        "actions": [
            "Faire valider le diagnostic à voix haute pendant la visite (« On est d'accord, c'est bien votre PAC qui montre des signes de fatigue ? »)",
            "Récapituler par SMS ou email les points validés AVANT d'envoyer le devis",
            "Présenter le devis en 3 options Confort/Performance/Premium - le prospect choisit, donc s'engage",
            "Demander 30% d'acompte plutôt que paiement 100% à la fin - le premier engagement financier ancre la décision",
        ],
        "in_devis": (
            "En tête du devis, rappeler : « Suite à notre visite du [DATE], "
            "vous m'avez confirmé les objectifs suivants : [OBJECTIF 1], "
            "[OBJECTIF 2], [OBJECTIF 3]. Le devis ci-dessous y répond point "
            "par point. »"
        ),
    },
    {
        "num": "03",
        "name": "Preuve sociale",
        "claim": "Montrer que d'autres ont déjà dit oui.",
        "why": (
            "Face à une décision difficile (chaudière 8 000 €, PAC 18 000 €), "
            "le prospect cherche des signaux que d'autres ont franchi le pas. "
            "Les avis Google, les références chantiers, les témoignages "
            "courts, les badges « X clients formés / installés » sont les "
            "déclencheurs les plus puissants en BTP français en 2025-2026, "
            "selon plusieurs études FFB et Effectif Marketing."
        ),
        "actions": [
            "Intégrer 3 témoignages courts (2-3 lignes max) dans le devis",
            "Mentionner le nombre d'installations réalisées dans l'année (« 42 PAC installées en 2025 »)",
            "Inclure note Google Business Profile (« 4,8 ★ - 87 avis ») en pied de devis",
            "Joindre 1 page A4 « Quelques chantiers récents » avec 3 photos avant/après et le département",
        ],
        "in_devis": (
            "Bandeau en pied de page : « 142 clients accompagnés depuis 2018 · "
            "Note Google : 4,8/5 sur 87 avis · 100% de garantie décennale "
            "honorée à ce jour. »"
        ),
    },
    {
        "num": "04",
        "name": "Autorité",
        "claim": "Faire reconnaître votre expertise et vos titres.",
        "why": (
            "Cialdini démontre que les humains accordent plus de crédit à une "
            "personne perçue comme experte. En BTP, les labels (RGE Qualibat, "
            "Qualigaz, PG, Qualifelec), les années d'expérience, les "
            "formations continues et les marques de partenariat (Daikin Pro "
            "Partner, Atlantic Expert, Mitsubishi Diamond) sont des "
            "raccourcis cognitifs qui rassurent immédiatement."
        ),
        "actions": [
            "Logos des certifications RGE/Qualibat/Qualigaz visibles en en-tête",
            "Mentionner les années d'existence et le nombre d'installations",
            "Citer 1 ou 2 partenariats marque (« Centre installateur agréé Atlantic depuis 2019 »)",
            "Ajouter une signature manuscrite du dirigeant en pied de devis (humanise + autorité)",
        ],
        "in_devis": (
            "En-tête de devis : 4 logos certifications (RGE Qualibat / Qualigaz "
            "/ PG / Marque partenaire). Sous le nom de l'entreprise : « [NB] "
            "ans d'expérience · [NB] installations réalisées · Membre CAPEB / "
            "FFB. »"
        ),
    },
    {
        "num": "05",
        "name": "Sympathie",
        "claim": "Ressembler, comprendre, partager.",
        "why": (
            "On dit plus facilement oui à quelqu'un qu'on apprécie. Cialdini "
            "identifie 3 leviers de sympathie : similarité (vous êtes du même "
            "village, du même âge, vous parlez de pêche ensemble), "
            "compliments sincères, coopération (nous sommes dans le même camp). "
            "En BTP local, c'est l'arme principale du petit artisan face aux "
            "grosses enseignes nationales."
        ),
        "actions": [
            "Personnaliser l'en-tête : prénom du client, adresse, contexte évoqué pendant la visite",
            "Photo du dirigeant souriant (pas en costume - en EPI ou en tenue pro) sur le devis",
            "Mention locale : « Entreprise familiale [VILLE] depuis [ANNÉE] »",
            "Remplacer le « Madame, Monsieur » impersonnel par une ouverture personnalisée : « Bonjour Madame Dupont, »",
        ],
        "in_devis": (
            "Première ligne après l'en-tête : « Bonjour [PRÉNOM CLIENT], "
            "Suite à notre rencontre du [DATE] chez vous à [VILLE], voici "
            "le devis détaillé pour [PROJET]. J'ai pris en compte vos "
            "contraintes liées à [POINT ÉVOQUÉ EN VISITE]. »"
        ),
    },
    {
        "num": "06",
        "name": "Rareté",
        "claim": "Ce qui est limité prend plus de valeur.",
        "why": (
            "Cialdini démontre que l'idée de perdre une opportunité est plus "
            "motivante que l'idée de gagner quelque chose. En BTP, les "
            "déclencheurs sont : disponibilité du créneau de pose, dispositifs "
            "d'aide (MaPrimeRénov', CEE) avec dates butoirs réelles, "
            "augmentations de prix matières annoncées par les fournisseurs. "
            "Attention : la rareté doit être VRAIE - une fausse urgence "
            "détruit la confiance et est illégale."
        ),
        "actions": [
            "Indiquer la durée de validité du devis (légalement obligatoire : « Devis valable 3 mois à compter du [DATE] »)",
            "Mentionner les vraies fenêtres de pose : « Planning de pose actuel : 6 semaines d'attente, créneau bloqué jusqu'au [DATE] »",
            "Rappeler les dates butoirs aides 2026 (MaPrimeRénov', CEE, TVA 5,5%)",
            "Indiquer si une augmentation tarifaire fournisseur est annoncée (« Tarifs garantis jusqu'au [DATE], hausse fournisseur Atlantic prévue [DATE+1mois] »)",
        ],
        "in_devis": (
            "Encadré en haut à droite : « Devis valable jusqu'au [DATE +3 mois] · "
            "Créneau de pose réservé jusqu'au [DATE +2 semaines] · Aides "
            "calculées au taux en vigueur le [DATE actuelle]. »"
        ),
    },
    {
        "num": "07",
        "name": "Unité",
        "claim": "Le « nous » qui crée l'appartenance.",
        "why": (
            "C'est le 7e principe ajouté par Cialdini en 2016 dans son livre "
            "Pre-Suasion. L'unité dépasse la simple sympathie : c'est l'idée "
            "que vous et le prospect appartenez à la même tribu, partagez la "
            "même cause. En BTP, c'est « entre habitants de la même région », "
            "« entre artisans et particuliers qui valorisent le travail "
            "soigné », « entre familles qui rénovent intelligemment »."
        ),
        "actions": [
            "Utiliser « nous » dès que possible (« Nous avons regardé ensemble votre installation actuelle »)",
            "Souligner ce qui vous lie au client (région, type de logement, profil familial)",
            "Mentionner les valeurs communes : qualité, durabilité, transparence, soutien aux artisans locaux",
            "Si possible, citer des clients du même quartier ou village (avec leur accord, sans nom)",
        ],
        "in_devis": (
            "Phrase de transition entre diagnostic et options : « Comme "
            "souvent dans les maisons de [TYPE - exemple : briques rouges "
            "des années 1960 du Nord] que nous rénovons ensemble depuis "
            "[ANNÉE], la priorité est d'isoler ET de chauffer juste, pas "
            "de surdimensionner. Voici les 3 options pour votre cas. »"
        ),
    },
]

# ===========================================================
# DATA - DEVIS-TYPE - 10 SECTIONS
# ===========================================================

DEVIS_SECTIONS = [
    {
        "num": "01",
        "title": "En-tête entreprise",
        "fields": [
            ("Logo entreprise", "[LOGO]"),
            ("Certifications visuelles", "[LOGOS RGE / QUALIBAT / QUALIGAZ / PG / PARTENAIRE MARQUE]"),
            ("Nom commercial complet", "[NOM ENTREPRISE]"),
            ("Forme juridique", "[SARL / EURL / SAS / EI] au capital de [MONTANT] €"),
            ("Adresse siège", "[ADRESSE COMPLÈTE]"),
            ("Téléphone, email, site", "[TÉL] · [EMAIL] · [SITE]"),
            ("SIRET (14 chiffres)", "[SIRET]"),
            ("RCS ville", "RCS [VILLE], n° [NUMÉRO]"),
            ("Code APE / NAF", "[CODE 4 caractères]"),
            ("N° TVA intracommunautaire", "FR[XX][SIREN]"),
            ("Assurance décennale", "[ASSUREUR] - Police n° [NUMÉRO] - couvrant [ZONE]"),
            ("Médiateur conso", "CM2C - Centre de Médiation et de Consommation - cm2c.net"),
            ("RGE (si applicable)", "Qualibat-RGE n° [NUMÉRO] - valide du [DATE] au [DATE]"),
        ],
        "cialdini": "Autorité (04) - tous les badges et labels visibles en un coup d'œil.",
    },
    {
        "num": "02",
        "title": "Identification client et chantier",
        "fields": [
            ("Civilité, Prénom, Nom", "[Mme / M.] [PRÉNOM] [NOM]"),
            ("Adresse du client (facturation)", "[ADRESSE COMPLÈTE]"),
            ("Téléphone, email", "[TÉL] · [EMAIL]"),
            ("Adresse du chantier (si différente)", "[ADRESSE]"),
            ("Date d'établissement", "[JJ/MM/AAAA]"),
            ("N° de devis", "DEVIS-[ANNÉE]-[NUMÉRO]"),
            ("Validité", "3 mois à compter du [DATE]"),
            ("Date de rendez-vous référence", "Suite à notre visite du [DATE]"),
        ],
        "cialdini": "Sympathie (05) - personnaliser au prénom · Rareté (06) - validité datée.",
    },
    {
        "num": "03",
        "title": "Préambule personnalisé",
        "fields": [
            ("Salutation personnalisée", "Bonjour [PRÉNOM CLIENT],"),
            ("Rappel du contexte", "Suite à notre rencontre du [DATE] à votre domicile de [VILLE], voici le devis détaillé pour [PROJET]."),
            ("Rappel des contraintes évoquées", "J'ai pris en compte les contraintes que vous m'avez exposées : [CONTRAINTE 1], [CONTRAINTE 2], [CONTRAINTE 3]."),
            ("Inclus avec ce devis (offert)", "Audit thermique simplifié (1 page) · Guide entretien PDF · 3 références de chantiers similaires sur demande."),
        ],
        "cialdini": "Réciprocité (01) + Sympathie (05) + Engagement (02) - rappel des points validés en visite.",
    },
    {
        "num": "04",
        "title": "Diagnostic / état des lieux",
        "fields": [
            ("Installation existante", "[TYPE] de [MARQUE] de [ANNÉE], [ÉTAT]"),
            ("Constats techniques", "[CONSTAT 1 - exemple : rendement chaudière estimé à 75% contre 90% pour le neuf]"),
            ("Constats énergétiques", "[CONSO ANNUELLE ESTIMÉE / OBSERVÉE]"),
            ("Surface chauffée", "[SURFACE m²]"),
            ("Isolation du logement", "[ÉTAT - exemple : isolation combles 2019, murs non isolés, vitrage simple en façade sud]"),
            ("Recommandation principale", "[RECOMMANDATION - exemple : remplacement chaudière fioul par PAC air/eau dimensionnée pour 9 kW]"),
        ],
        "cialdini": "Autorité (04) - démontrer l'expertise technique · Engagement (02) - faire valider le constat avant de présenter les options.",
    },
    {
        "num": "05",
        "title": "3 options chiffrées - Confort / Performance / Premium",
        "fields": [
            ("Option 1 - Confort", "[Solution éprouvée, marque milieu de gamme] - Total HT : [XX XXX] € - TVA [5,5/10/20]% : [X XXX] € - Total TTC : [XX XXX] €"),
            ("Option 2 - Performance (recommandée)", "[Solution haut de gamme, marque premium] - Total HT : [XX XXX] € - TVA : [X XXX] € - Total TTC : [XX XXX] €"),
            ("Option 3 - Premium", "[Solution premium + accessoires, garantie étendue] - Total HT : [XX XXX] € - TVA : [X XXX] € - Total TTC : [XX XXX] €"),
            ("Pour chaque option, détailler", "Marque, modèle, référence · Puissance · Garantie constructeur · Particularités techniques · Aides estimées (MPR, CEE) · Reste à charge estimé"),
        ],
        "cialdini": "Engagement (02) - le prospect choisit donc s'engage · Preuve sociale (03) - marquer l'option 2 « Recommandée par nos clients ».",
    },
    {
        "num": "06",
        "title": "Détail prestation - décomposition par poste",
        "fields": [
            ("Désignation du poste", "[ex : Fourniture et pose PAC air/eau Atlantic Alfea Extensa Duo 9 kW]"),
            ("Quantité", "[X]"),
            ("Unité", "[u / ml / m² / forfait]"),
            ("Prix unitaire HT", "[X XXX,XX €]"),
            ("Total HT poste", "[X XXX,XX €]"),
            ("Postes typiques PAC", "Dépose ancienne installation · Adaptation réseau hydraulique · Fourniture PAC · Fourniture ballon tampon · Pose et raccordement · Mise en service et test"),
            ("Postes typiques chaudière gaz", "Dépose ancienne · Fourniture chaudière · Pose et raccordement gaz · Mise en service · Certificat conformité Qualigaz"),
            ("Postes typiques salle de bain", "Dépose · Plomberie neuve · Carrelage · Robinetterie · Sanitaires · Évacuation"),
        ],
        "cialdini": "Autorité (04) - transparence totale, pas de prix forfaitaire opaque.",
    },
    {
        "num": "07",
        "title": "Totaux, TVA, aides",
        "fields": [
            ("Sous-total HT", "[XX XXX,XX €]"),
            ("Frais éventuels", "Déplacement [VILLE] : [XXX €] (ou « inclus »)"),
            ("Total HT", "[XX XXX,XX €]"),
            ("TVA applicable", "Taux et montant : [5,5% / 10% / 20%] - voir détails justificatif au verso"),
            ("Total TTC", "[XX XXX,XX €]"),
            ("Aides MaPrimeRénov' estimées", "Selon revenus fiscaux : entre [X XXX €] (Rose) et [X XXX €] (Bleu)"),
            ("CEE estimés", "Prime CEE primaire : [X XXX €] (calcul Bonus 4.7 - barème en vigueur)"),
            ("Éco-PTZ", "Éligibilité estimée : jusqu'à 30 000 €"),
            ("Reste à charge estimé", "[X XXX €] (sous réserve éligibilité confirmée)"),
        ],
        "cialdini": "Rareté (06) - rappel des dates limites des aides 2026.",
    },
    {
        "num": "08",
        "title": "Modalités de paiement",
        "fields": [
            ("Acompte à la commande", "30% du montant TTC, soit [X XXX €] - à réception du devis signé"),
            ("Acompte à la pose (J démarrage)", "40% du montant TTC, soit [X XXX €]"),
            ("Solde", "30% à la mise en service et réception du chantier"),
            ("Modes de paiement acceptés", "Virement, chèque, CB sur place (sur certains montants)"),
            ("Pénalité de retard pro", "Si client professionnel : taux BCE + 10 points · Indemnité forfaitaire 40 €"),
        ],
        "cialdini": "Engagement (02) - l'acompte fixe l'engagement · Réciprocité (01) - mode de paiement flexible.",
    },
    {
        "num": "09",
        "title": "Délais et planning",
        "fields": [
            ("Date prévisionnelle de démarrage", "[À DATE]"),
            ("Durée prévue", "[NB jours / semaines]"),
            ("Conditions de modification", "Tout changement de planning du fait du client doit être notifié sous 7 jours ouvrés."),
            ("Causes de retard exclues", "Intempéries, indisponibilité fournisseur, pathologie cachée du bâti."),
        ],
        "cialdini": "Rareté (06) - créneau réservé à date · Autorité (04) - cadrage pro.",
    },
    {
        "num": "10",
        "title": "Conditions générales, garanties, signature",
        "fields": [
            ("Garantie décennale", "10 ans sur les ouvrages de gros œuvre et d'amélioration énergétique"),
            ("Garantie biennale (bon fonctionnement)", "2 ans sur équipements dissociables"),
            ("Garantie parfait achèvement", "1 an, désordres signalés à la réception"),
            ("Garantie satisfaction Carnet Plein®", "Si insatisfaction après 30 jours, modification incluse jusqu'à conformité (à mettre en cohérence avec le bonus 6 contrat avocat)"),
            ("Médiateur de la consommation", "CM2C - 49 rue de Ponthieu, 75008 Paris - cm2c.net"),
            ("Recours en cas de litige", "Tribunal de [VILLE], compétence territoriale"),
            ("Droit de rétractation (démarchage)", "14 jours si signature à domicile, sauf renonciation expresse pour travaux urgents"),
            ("Mention manuscrite (article L221-9 Code conso)", "« Bon pour accord » + date + signature du client"),
            ("Signature de l'entreprise", "Nom, fonction, signature manuscrite ou électronique qualifiée"),
        ],
        "cialdini": "Autorité (04) - garanties claires · Preuve sociale (03) - garantie satisfaction unique sur le marché.",
    },
]

# ===========================================================
# DATA - 8 OBJECTIONS CLASSIQUES + REPONSES
# ===========================================================

OBJECTIONS = [
    {
        "objection": "C'est trop cher.",
        "reponse": (
            "« Je comprends. C'est une décision importante. Si on regarde le "
            "coût mensualisé sur 15 ans (durée de vie moyenne de l'équipement) "
            "avec les économies d'énergie estimées, ça vous revient à environ "
            "[X €/mois]. Et avec les aides MaPrimeRénov' et CEE, le reste à "
            "charge tombe à [X XXX €]. On peut aussi étaler les paiements en "
            "trois fois sans frais. Quel est votre repère prix de référence ? »"
        ),
        "principe": "Engagement (02) - faire dire au prospect son repère",
    },
    {
        "objection": "Je vais demander d'autres devis.",
        "reponse": (
            "« C'est sain, beaucoup de clients comparent 2 ou 3 devis. Si "
            "vous voulez, je vous prépare une grille de comparaison sur 6 "
            "points objectifs (marque, garantie, durée, certifications, "
            "aides incluses, SAV) pour faciliter la comparaison. Au moins "
            "vous comparez les devis sur les mêmes critères. »"
        ),
        "principe": "Réciprocité (01) - offrir la grille de comparaison",
    },
    {
        "objection": "Je vais réfléchir.",
        "reponse": (
            "« Bien sûr, prenez le temps. Qu'est-ce qui vous fait hésiter "
            "concrètement : le prix, la marque, le timing, le choix entre "
            "les options ? Pour ne pas vous laisser avec une question sans "
            "réponse, je peux apporter cette info maintenant si vous voulez. "
            "Sinon, je vous appelle dans 3 jours pour faire le point. »"
        ),
        "principe": "Sympathie (05) - ne pas presser · Engagement (02) - tirer le frein réel",
    },
    {
        "objection": "Mon voisin l'a eu moins cher.",
        "reponse": (
            "« Possible. Plusieurs choses peuvent expliquer un écart de prix : "
            "puissance de l'équipement (pour la même surface, écart facile de "
            "20%), marque, type de garantie incluse, dépose et évacuation des "
            "déchets compris ou non, mise en service certifiée. Si vous "
            "voulez, on regarde ensemble la facture de votre voisin (en "
            "détail technique) pour comparer ce qui est réellement comparable. »"
        ),
        "principe": "Autorité (04) - démontrer la maîtrise technique",
    },
    {
        "objection": "J'attends pour voir si les aides évoluent.",
        "reponse": (
            "« C'est une bonne question. En 2026, MaPrimeRénov' a été "
            "réouvert le 23 février mais avec des barèmes maintenus ou "
            "abaissés selon les revenus, et un quota annuel limité (le "
            "guichet ferme quand l'enveloppe est consommée). Les CEE "
            "restent stables. Le risque d'attendre, c'est de tomber après "
            "la fermeture du guichet, ou de subir une hausse de prix "
            "matières annoncée chez nos fournisseurs en [MOIS]. Voulez-vous "
            "que je calcule précisément ce que vous touchez aujourd'hui ? »"
        ),
        "principe": "Rareté (06) - urgence réelle, pas inventée",
    },
    {
        "objection": "J'ai entendu de mauvais retours sur les PAC.",
        "reponse": (
            "« Ça arrive, surtout quand la pompe est surdimensionnée ou "
            "mal posée. C'est pour cela qu'on fait toujours un calcul de "
            "dimensionnement précis (Cofely / DPE / méthode 3CL) AVANT de "
            "vous chiffrer. Sur les 42 PAC qu'on a installées en 2025, on a "
            "0 retour négatif en année 1 et nos clients valident en moyenne "
            "30 à 40% d'économies sur leur facture. Voici 3 références de "
            "voisins du [DÉPARTEMENT] que vous pouvez appeler. »"
        ),
        "principe": "Preuve sociale (03) + Autorité (04) - faits + références",
    },
    {
        "objection": "C'est mon banquier / assureur qui décide.",
        "reponse": (
            "« Compris. Ce que je vous propose : je vous envoie le devis "
            "détaillé + une note de synthèse banque (1 page) qui présente le "
            "projet, les économies estimées, et la valeur ajoutée pour le "
            "logement. C'est exactement ce que demandent les conseillers "
            "bancaires aujourd'hui. Si besoin, je peux aussi prendre un appel "
            "rapide avec votre conseiller pour répondre directement à ses "
            "questions techniques. »"
        ),
        "principe": "Réciprocité (01) + Sympathie (05) - faciliter, ne pas s'imposer",
    },
    {
        "objection": "Et la garantie, ça vaut quoi vraiment ?",
        "reponse": (
            "« Trois choses : 1) la garantie décennale est obligatoire et "
            "couverte par mon assurance [NOM ASSUREUR] - police n° [XXX] que "
            "je vous communique en pièce jointe ; 2) la garantie biennale "
            "couvre les équipements dissociables ; 3) chez nous, en plus, on "
            "ajoute une garantie satisfaction 30 jours : si vous trouvez que "
            "le résultat n'est pas conforme à ce qu'on a promis, on revient "
            "modifier sans coût supplémentaire jusqu'à conformité. C'est "
            "écrit noir sur blanc dans nos conditions générales. »"
        ),
        "principe": "Autorité (04) + Preuve sociale (03) - garantie unique = différenciation",
    },
]

# ===========================================================
# DATA - SEQUENCE DE RELANCES J+3 / J+7 / J+14 / J+90
# ===========================================================

RELANCES = [
    {
        "delai": "J+3",
        "canal": "SMS court (ou email simple)",
        "objet": "Pas d'objet (SMS) / « Votre devis Carnet Plein® - on en est où ? » (email)",
        "corps": (
            "Bonjour [PRÉNOM], j'espère que tout va bien. Avez-vous eu le "
            "temps de regarder le devis envoyé lundi ? Pas de question "
            "urgente, je voulais juste vérifier qu'il vous est bien parvenu "
            "et qu'il est clair. Si une option vous intéresse, on peut en "
            "rediscuter quand vous voulez. Bonne fin de semaine. [PRÉNOM PRO]."
        ),
        "objectif": "Vérifier réception + ouvrir la porte. Pas de pression. Pas de question fermée « vous le signez ? ».",
    },
    {
        "delai": "J+7",
        "canal": "Appel téléphonique",
        "objet": "Appel sortant - 5 min max",
        "corps": (
            "« Bonjour [PRÉNOM], [PRÉNOM PRO] de [ENTREPRISE]. Vous avez "
            "eu le temps de réfléchir au devis ? Je voulais savoir si vous "
            "aviez des questions sur l'une des options, ou besoin que je "
            "précise un point (technique, financement, aides). Si vous avez "
            "des autres devis à comparer, je peux vous faire la grille "
            "comparative dont je vous parlais. Quand est-ce qu'on en "
            "reparle ? »"
        ),
        "objectif": "Détecter le frein réel (prix / timing / autre devis / hésitation) et y répondre.",
    },
    {
        "delai": "J+14",
        "canal": "Email avec contenu utile",
        "objet": "« [PRÉNOM], 2 nouveaux retours clients [VILLE/RÉGION] »",
        "corps": (
            "Bonjour [PRÉNOM], depuis notre échange, on a livré 2 chantiers "
            "similaires au vôtre dans le [DÉPARTEMENT]. Je vous joins 2 "
            "photos avant/après et un témoignage écrit court (Mme L. de "
            "[VILLE]). Si vous voulez l'appeler pour avoir un retour "
            "directement, elle est d'accord pour répondre à 1-2 questions. "
            "Pour info, le devis est toujours valable jusqu'au [DATE]. Bonne "
            "journée. [PRÉNOM PRO]."
        ),
        "objectif": "Apporter de la valeur (preuve sociale fraîche) sans relancer commercialement. Rappel rareté validité.",
    },
    {
        "delai": "J+90",
        "canal": "Email + ajout CRM si non-signé",
        "objet": "« [PRÉNOM], on garde le contact ? »",
        "corps": (
            "Bonjour [PRÉNOM], votre devis du [DATE] arrive à expiration. "
            "Si le projet n'est plus d'actualité aujourd'hui, pas de souci, "
            "je le sors de mes relances. Mais je voulais juste vous dire : "
            "on continue à publier 1 retour client par semaine sur la fiche "
            "Google et sur le site, vous pouvez nous suivre là-bas. Et si "
            "votre projet revient dans 6 mois ou 1 an, vous pouvez nous "
            "rappeler à tout moment - on adapte le devis aux conditions du "
            "moment. À bientôt. [PRÉNOM PRO]."
        ),
        "objectif": "Sortir proprement de la relance · Garder une porte ouverte · Démontrer la non-pression.",
    },
]

# ===========================================================
# DATA - 20 MENTIONS LEGALES OBLIGATOIRES 2026
# ===========================================================

MENTIONS_OBLIGATOIRES = [
    "Nom commercial complet et forme juridique (SARL, EURL, SAS, EI)",
    "Adresse complète du siège social",
    "SIRET (14 chiffres) et code APE/NAF",
    "RCS ville + numéro d'immatriculation",
    "N° TVA intracommunautaire (FR + clé + SIREN)",
    "Téléphone, email, site web professionnel",
    "Civilité, nom, prénom, adresse du client",
    "Date d'établissement du devis (datée et signée)",
    "Mention « Devis gratuit » (ou prix de l'établissement si payant)",
    "Durée de validité du devis (recommandé 1 à 3 mois, à indiquer)",
    "Description détaillée de chaque prestation (désignation, quantité, unité, prix unitaire HT)",
    "Prix unitaires HT et total HT par poste",
    "Taux de TVA applicable (5,5% / 10% / 20%) et montant TVA total",
    "Total TTC en chiffres ET en lettres si supérieur à 1 500 €",
    "Modalités et conditions de paiement (acompte, échéances)",
    "Date de début prévisionnel et durée estimée des travaux",
    "Mention de l'assurance décennale obligatoire (nom assureur, n° police, zone couverte) - articles L241-1 et L241-2 Code des assurances",
    "Coordonnées du médiateur de la consommation (CM2C ou autre) - obligatoire depuis loi Hamon 2014",
    "Mention de la garantie biennale (2 ans, équipements dissociables) et décennale (10 ans, gros œuvre)",
    "Mention manuscrite du client « Bon pour accord » + date + signature, et signature de l'entreprise",
]

# ===========================================================
# DATA - SANCTIONS 2025-2026 (non-conformite)
# ===========================================================

SANCTIONS = [
    ("Devis non daté ou non signé", "Amende administrative jusqu'à 3 000 € (personne physique) ou 15 000 € (personne morale) - DGCCRF"),
    ("Absence de mention assurance décennale", "Travaux invalides en cas de sinistre - mise en cause civile et pénale"),
    ("Absence de mention médiateur de la consommation", "Amende administrative jusqu'à 15 000 € (loi Hamon, article L612-1 Code conso)"),
    ("Mention TVA erronée (taux réduit appliqué à tort)", "Redressement fiscal + amende de 5% du montant de la TVA éludée"),
    ("Démarchage à domicile sans bordereau de rétractation", "Amende pénale jusqu'à 75 000 €, contrat nul"),
    ("Pratique commerciale trompeuse (fausse urgence, faux label RGE)", "Amende pénale jusqu'à 300 000 €, peine de prison possible"),
    ("Non-respect de la durée de validité affichée", "Risque de contestation du contrat, requalification du devis"),
]

# ===========================================================
# DATA - REGLES TVA 2026 (pour annexe)
# ===========================================================

TVA_RULES = [
    ("5,5%", "Travaux d'amélioration énergétique éligibles MaPrimeRénov' (isolation, PAC, chaudière biomasse, ECS thermodynamique) sur logements >2 ans"),
    ("10%", "Travaux d'entretien, d'amélioration ou de transformation non éligibles au taux réduit (peinture, robinetterie, dépannage) sur logements >2 ans"),
    ("20%", "Travaux sur logements neufs (<2 ans) · Chaudière gaz à condensation depuis le 1er mars 2025 (loi de finances 2025) · Travaux non éligibles aux taux réduits · Constructions neuves"),
]

# ===========================================================
# DATA - MARQUES REFERENCE (autorite implicite)
# ===========================================================

MARQUES_REF = [
    "Atlantic (chaudières fioul/gaz, PAC, ECS - groupe français)",
    "Daikin (PAC air/eau, air/air - leader mondial)",
    "Mitsubishi Electric (PAC haut de gamme)",
    "De Dietrich (chaudières premium, groupe BDR)",
    "Saunier Duval (chaudières gaz, groupe Vaillant)",
    "Viessmann (chaudières et PAC haut de gamme)",
    "Frisquet (chaudières gaz, fabrication française)",
    "Bosch (chaudières et PAC)",
    "Panasonic (PAC air/air et air/eau)",
    "Toshiba (PAC)",
    "Hitachi (PAC)",
    "Stiebel Eltron (PAC, ECS thermodynamique - allemand)",
    "Auer (PAC fabriquées en France)",
    "LG (PAC, climatisation)",
    "Vaillant (chaudières et PAC)",
    "Thermor (ECS, chauffage électrique - groupe Atlantic)",
    "De Longhi (climatisation, PAC)",
    "Chaffoteaux / Ariston (chaudières, ECS)",
    "Hitachi Yutaki (PAC dédiée résidentiel)",
    "Carrier (PAC, climatisation - leader US)",
]

# ===========================================================
# CSS - same charter as Bonus #3, adapted for B4
# ===========================================================

CSS = """
@page {
  size: A4 portrait;
  margin: 20mm 16mm 22mm 16mm;
  @bottom-left {
    content: "Carnet Plein® by Mad Makers · Bonus #4 · Édition 2026";
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.5pt;
    color: #5a5d56;
    letter-spacing: 0.04em;
  }
  @bottom-right {
    content: counter(page) " / " counter(pages);
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.5pt;
    color: #5a5d56;
  }
}

@page bleed {
  margin: 0;
  @bottom-left { content: none; }
  @bottom-right { content: none; }
}

*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 10.5pt;
  line-height: 1.55;
  color: #1a1c18;
  background: #fff;
  font-feature-settings: "ss02", "dlig";
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

h1, h2, h3, h4 {
  margin: 0;
  font-weight: 600;
  letter-spacing: -0.02em;
  line-height: 1.15;
  color: #0a0a0a;
}

p { margin: 0 0 0.5em 0; }
p:last-child { margin-bottom: 0; }

em { font-style: italic; color: #e0541b; font-weight: 500; }
strong { font-weight: 600; color: #0a0a0a; }
code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.92em;
  background: #ebe7dc;
  padding: 1px 4px;
  border-radius: 3px;
  color: #0a0a0a;
}

.page { page-break-after: always; }
.page:last-of-type { page-break-after: auto; }

/* ===== FULL-BLEED PAGES ===== */
.bleed {
  page: bleed;
  page-break-after: always;
  background: #0a0a0a;
  color: #fff;
  width: 210mm;
  height: 297mm;
  padding: 28mm 22mm;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

/* ===== COVER ===== */
.cover {
  justify-content: space-between;
}
.cover::after {
  content: "";
  position: absolute;
  top: -30mm; right: -30mm;
  width: 130mm; height: 130mm;
  background: radial-gradient(circle, rgba(224,84,27,0.45) 0%, transparent 65%);
  pointer-events: none;
}
.cover-top { position: relative; z-index: 1; }
.cover-meta {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 8mm;
  font-family: 'JetBrains Mono', monospace;
  font-size: 9pt;
  color: #a9a69f;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.cover .badge {
  display: inline-block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 8.5pt;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: #0a0a0a;
  background: #e0541b;
  padding: 6px 16px;
  border-radius: 999px;
  font-weight: 600;
}
.cover h1 {
  font-size: 56pt;
  line-height: 0.95;
  letter-spacing: -0.03em;
  color: #fff;
  margin-top: 32mm;
  font-weight: 700;
}
.cover .sub {
  font-size: 14pt;
  color: #e8e6df;
  max-width: 140mm;
  line-height: 1.35;
  margin-top: 10mm;
  font-weight: 400;
}
.cover .accent-line {
  width: 22mm;
  height: 0.6mm;
  background: #e0541b;
  margin-bottom: 3mm;
}

/* ===== SECTION SEPARATOR ===== */
.section-sep {
  justify-content: center;
  padding: 50mm 25mm;
}
.section-sep .label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10pt;
  color: #e0541b;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  margin-bottom: 8mm;
}
.section-sep h2 {
  color: #fff;
  font-size: 38pt;
  line-height: 1;
  letter-spacing: -0.03em;
  margin-bottom: 10mm;
  font-weight: 700;
  max-width: 160mm;
}
.section-sep .count {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11pt;
  color: #a9a69f;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 18mm;
}
.section-sep .desc {
  color: #e8e6df;
  font-size: 12pt;
  line-height: 1.55;
  max-width: 155mm;
}

/* ===== CTA ===== */
.cta-page {
  justify-content: center;
  padding: 50mm 25mm;
}
.cta-page::after {
  content: "";
  position: absolute;
  top: 40mm; left: -20mm;
  width: 110mm; height: 110mm;
  background: radial-gradient(circle, rgba(224,84,27,0.35) 0%, transparent 65%);
  pointer-events: none;
}
.cta-page > * { position: relative; z-index: 1; }
.cta-page .eyebrow { color: #e0541b; margin-bottom: 6mm; }
.cta-page h2 {
  color: #fff;
  font-size: 30pt;
  line-height: 1.1;
  margin-bottom: 8mm;
  max-width: 160mm;
  font-weight: 600;
}
.cta-page p {
  color: #e8e6df;
  font-size: 11pt;
  line-height: 1.6;
  max-width: 155mm;
  margin-bottom: 4mm;
}
.cta-page .button {
  display: inline-block;
  background: #e0541b;
  color: #fff;
  padding: 4mm 8mm;
  border-radius: 999px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 10pt;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 600;
  margin-top: 8mm;
  text-decoration: none;
  align-self: flex-start;
}

/* ===== EYEBROW ===== */
.eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9pt;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: #e0541b;
  margin-bottom: 4mm;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}
.eyebrow::before {
  content: "";
  display: inline-block;
  width: 6px; height: 6px;
  background: #e0541b;
  flex-shrink: 0;
}

/* ===== INTRO ===== */
.intro h1 {
  font-size: 24pt;
  margin-bottom: 6mm;
  line-height: 1.1;
}
.lead {
  font-size: 11.5pt;
  line-height: 1.5;
  color: #3a3d36;
  max-width: 160mm;
}

/* ===== CALLOUTS ===== */
.callout {
  background: #ebe7dc;
  border-left: 3px solid #e0541b;
  padding: 5mm 6mm;
  margin: 6mm 0;
  border-radius: 0 3mm 3mm 0;
  page-break-inside: avoid;
}
.callout.dark {
  background: #1a1c18;
  color: #e8e6df;
}
.callout.dark strong { color: #fff; }
.callout h3 {
  font-size: 10pt;
  margin-bottom: 3mm;
  font-family: 'JetBrains Mono', monospace;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #e0541b;
  font-weight: 600;
  line-height: 1.3;
}
.callout p {
  font-size: 10pt;
  line-height: 1.55;
  margin-bottom: 2mm;
}

/* ===== STAT BLOCKS ===== */
.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 5mm;
  margin: 8mm 0;
}
.stat {
  background: #ebe7dc;
  padding: 5mm;
  border-radius: 3mm;
  border-top: 3px solid #e0541b;
  page-break-inside: avoid;
}
.stat-num {
  font-family: 'Inter', sans-serif;
  font-size: 28pt;
  font-weight: 700;
  color: #e0541b;
  letter-spacing: -0.025em;
  line-height: 1;
  margin-bottom: 2mm;
}
.stat-label {
  font-size: 10pt;
  color: #1a1c18;
  line-height: 1.4;
}

/* ===== CIALDINI PAGES ===== */
.principe {
  page-break-inside: avoid;
}
.principe-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  border-bottom: 1px solid #d5d2c9;
  padding-bottom: 3mm;
  margin-bottom: 5mm;
}
.principe-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10pt;
  color: #e0541b;
  font-weight: 600;
  letter-spacing: 0.08em;
}
.principe-meta {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8pt;
  color: #5a5d56;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.principe h2 {
  font-size: 26pt;
  line-height: 1.05;
  margin-bottom: 3mm;
  max-width: 165mm;
  font-weight: 600;
}
.principe .claim {
  font-size: 13pt;
  color: #e0541b;
  font-style: italic;
  margin-bottom: 6mm;
  font-weight: 500;
}
.principe-why {
  font-size: 11pt;
  line-height: 1.55;
  color: #3a3d36;
  margin-bottom: 6mm;
}

.actions-block {
  background: #fff;
  border: 1px solid #d5d2c9;
  border-left: 3px solid #2d9a5f;
  padding: 5mm;
  border-radius: 0 2mm 2mm 0;
  margin: 5mm 0;
  page-break-inside: avoid;
}
.actions-block-header {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9pt;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #2d9a5f;
  margin-bottom: 3mm;
  font-weight: 600;
}
.actions-block ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.actions-block li {
  font-size: 10pt;
  line-height: 1.5;
  margin-bottom: 2mm;
  padding-left: 5mm;
  position: relative;
  color: #1a1c18;
}
.actions-block li::before {
  content: "→";
  position: absolute;
  left: 0;
  color: #2d9a5f;
  font-weight: 600;
}

.in-devis-block {
  background: rgba(224,84,27,0.06);
  border-left: 3px solid #e0541b;
  padding: 5mm 6mm;
  margin: 5mm 0;
  border-radius: 0 2mm 2mm 0;
  page-break-inside: avoid;
}
.in-devis-header {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9pt;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #e0541b;
  margin-bottom: 3mm;
  font-weight: 600;
}
.in-devis-block p {
  font-size: 10pt;
  line-height: 1.55;
  color: #1a1c18;
  font-style: italic;
}

/* ===== DEVIS TEMPLATE PAGES ===== */
.devis-section {
  page-break-inside: avoid;
  margin-bottom: 8mm;
}
.devis-section-header {
  display: flex;
  align-items: baseline;
  gap: 5mm;
  border-bottom: 2px solid #0a0a0a;
  padding-bottom: 2mm;
  margin-bottom: 4mm;
}
.devis-section-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10pt;
  color: #e0541b;
  font-weight: 600;
  letter-spacing: 0.08em;
}
.devis-section-title {
  font-size: 14pt;
  font-weight: 600;
  color: #0a0a0a;
}
.devis-fields {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 4mm;
  font-size: 9.5pt;
}
.devis-fields td {
  padding: 2mm 3mm;
  border-bottom: 1px solid #ebe7dc;
  vertical-align: top;
  line-height: 1.4;
}
.devis-fields td.label {
  font-weight: 600;
  color: #0a0a0a;
  width: 42%;
}
.devis-fields td.value {
  color: #3a3d36;
  font-family: 'JetBrains Mono', monospace;
  font-size: 8.5pt;
  line-height: 1.45;
}
.devis-fields tr:last-child td { border-bottom: none; }
.cialdini-note {
  background: rgba(224,84,27,0.06);
  border-left: 2px solid #e0541b;
  padding: 3mm 4mm;
  margin: 3mm 0;
  border-radius: 0 2mm 2mm 0;
  font-size: 9pt;
  line-height: 1.45;
  color: #3a3d36;
  font-style: italic;
}
.cialdini-note strong {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8pt;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #e0541b;
  font-style: normal;
  display: block;
  margin-bottom: 1mm;
}

/* ===== IMAGE PLACEHOLDERS ===== */
.placeholders-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 5mm;
  margin: 5mm 0;
  page-break-inside: avoid;
}
.placeholders-row.cols-3 {
  grid-template-columns: 1fr 1fr 1fr;
}
.placeholders-row.cols-4 {
  grid-template-columns: 1fr 1fr 1fr 1fr;
}
.placeholder-img {
  background: #ebe7dc;
  border: 2px dashed #d5d2c9;
  padding: 10mm 5mm;
  border-radius: 3mm;
  text-align: center;
  min-height: 35mm;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.placeholder-img.brand {
  background: #fafaf7;
  border-color: #d5d2c9;
}
.placeholder-img.testi {
  background: rgba(45,154,95,0.06);
  border-color: rgba(45,154,95,0.35);
  min-height: 45mm;
}
.ph-icon {
  font-size: 22pt;
  margin-bottom: 3mm;
  color: #5a5d56;
}
.placeholder-img.brand .ph-icon { color: #e0541b; }
.placeholder-img.testi .ph-icon { color: #2d9a5f; }
.ph-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8pt;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 2mm;
  font-weight: 600;
  color: #5a5d56;
}
.placeholder-img.brand .ph-tag { color: #e0541b; }
.placeholder-img.testi .ph-tag { color: #2d9a5f; }
.ph-desc {
  font-size: 9pt;
  color: #1a1c18;
  font-style: italic;
  line-height: 1.4;
  max-width: 60mm;
}

/* ===== OBJECTIONS TABLE ===== */
.objection-card {
  background: #fafaf7;
  border: 1px solid #d5d2c9;
  border-left: 3px solid #e0541b;
  padding: 5mm 6mm;
  margin-bottom: 5mm;
  border-radius: 0 2mm 2mm 0;
  page-break-inside: avoid;
}
.objection-q {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9pt;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #c43c2a;
  margin-bottom: 2mm;
  font-weight: 600;
}
.objection-card h4 {
  font-size: 13pt;
  margin-bottom: 4mm;
  font-weight: 600;
  line-height: 1.25;
  color: #0a0a0a;
}
.objection-r {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9pt;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #2d9a5f;
  margin-bottom: 2mm;
  font-weight: 600;
}
.objection-card p.reponse {
  font-size: 10pt;
  line-height: 1.5;
  color: #1a1c18;
  margin-bottom: 3mm;
}
.objection-card .principe-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8pt;
  letter-spacing: 0.08em;
  color: #e0541b;
  text-transform: uppercase;
  font-weight: 600;
  border-top: 1px dashed #d5d2c9;
  padding-top: 2mm;
}

/* ===== RELANCES TIMELINE ===== */
.relance-card {
  background: #fff;
  border: 1px solid #d5d2c9;
  padding: 6mm;
  margin-bottom: 6mm;
  border-radius: 3mm;
  page-break-inside: avoid;
  position: relative;
}
.relance-card::before {
  content: "";
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 4mm;
  background: #e0541b;
  border-radius: 3mm 0 0 3mm;
}
.relance-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 4mm;
  border-bottom: 1px solid #ebe7dc;
  padding-bottom: 3mm;
}
.relance-delai {
  font-size: 18pt;
  font-weight: 700;
  color: #e0541b;
  letter-spacing: -0.02em;
}
.relance-canal {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8.5pt;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #5a5d56;
  font-weight: 600;
}
.relance-objet {
  font-size: 10pt;
  color: #0a0a0a;
  margin-bottom: 3mm;
  font-weight: 600;
}
.relance-corps {
  background: #ebe7dc;
  padding: 4mm 5mm;
  border-radius: 2mm;
  font-size: 9.5pt;
  line-height: 1.55;
  color: #1a1c18;
  margin-bottom: 3mm;
  font-style: italic;
}
.relance-objectif {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8.5pt;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #e0541b;
  font-weight: 600;
}
.relance-objectif::before { content: "Objectif : "; color: #5a5d56; }

/* ===== TABLES (mentions, sanctions, TVA, marques) ===== */
table.ref-table {
  width: 100%;
  border-collapse: collapse;
  margin: 5mm 0;
  font-size: 9pt;
  page-break-inside: avoid;
}
table.ref-table th {
  background: #0a0a0a;
  color: #fff;
  padding: 2.5mm 3mm;
  text-align: left;
  font-family: 'JetBrains Mono', monospace;
  font-size: 7.5pt;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 600;
  vertical-align: top;
}
table.ref-table td {
  padding: 2.5mm 3mm;
  border-bottom: 1px solid #d5d2c9;
  vertical-align: top;
  line-height: 1.45;
  font-size: 9pt;
}
table.ref-table tr:nth-child(even) td {
  background: #ebe7dc;
}
table.ref-table td.taux {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  color: #e0541b;
  font-size: 11pt;
}
table.ref-table td.sanction {
  color: #c43c2a;
  font-weight: 600;
}

/* ===== NUMBERED LIST (mentions obligatoires) ===== */
ol.numbered-mentions {
  counter-reset: mention;
  list-style: none;
  padding: 0;
  margin: 0;
}
ol.numbered-mentions li {
  counter-increment: mention;
  font-size: 10pt;
  line-height: 1.5;
  margin-bottom: 2.5mm;
  padding-left: 11mm;
  position: relative;
  color: #1a1c18;
  page-break-inside: avoid;
}
ol.numbered-mentions li::before {
  content: counter(mention, decimal-leading-zero);
  position: absolute;
  left: 0;
  top: 0;
  font-family: 'JetBrains Mono', monospace;
  font-size: 9pt;
  font-weight: 700;
  color: #e0541b;
  letter-spacing: 0.02em;
}

/* ===== CHECKLIST PRINTABLE ===== */
.checklist-print {
  border: 2px solid #0a0a0a;
  padding: 8mm;
  border-radius: 3mm;
  margin: 5mm 0;
  page-break-inside: avoid;
}
.checklist-print h2 {
  font-size: 16pt;
  margin-bottom: 5mm;
  font-weight: 700;
  color: #0a0a0a;
  border-bottom: 1px solid #d5d2c9;
  padding-bottom: 3mm;
}
.checklist-print h3 {
  font-size: 11pt;
  margin: 5mm 0 2mm;
  font-family: 'JetBrains Mono', monospace;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #e0541b;
  font-weight: 600;
}
.checklist-print ul {
  list-style: none;
  padding: 0;
  margin: 0 0 4mm 0;
}
.checklist-print li {
  font-size: 10pt;
  line-height: 1.5;
  padding-left: 7mm;
  position: relative;
  margin-bottom: 2mm;
  color: #1a1c18;
}
.checklist-print li::before {
  content: "☐";
  position: absolute;
  left: 0;
  top: 0;
  font-size: 12pt;
  color: #e0541b;
}

/* ===== ANNEXES / SECTION TITLES ===== */
.annexe h1 {
  font-size: 22pt;
  margin-bottom: 5mm;
  line-height: 1.15;
}
.annexe h3 {
  font-size: 13pt;
  margin: 6mm 0 3mm;
  color: #0a0a0a;
  line-height: 1.2;
}
.annexe p {
  font-size: 10.5pt;
  line-height: 1.55;
  color: #1a1c18;
  margin-bottom: 3mm;
}
.annexe ul, .annexe ol {
  padding-left: 6mm;
  margin: 3mm 0;
}
.annexe li {
  font-size: 10pt;
  line-height: 1.55;
  margin-bottom: 1.5mm;
  color: #1a1c18;
}

/* ===== MARQUES GRID ===== */
.marques-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3mm 6mm;
  margin: 5mm 0;
}
.marque-row {
  font-size: 9.5pt;
  line-height: 1.5;
  padding: 2mm 0 2mm 6mm;
  position: relative;
  border-bottom: 1px solid #ebe7dc;
}
.marque-row::before {
  content: "·";
  position: absolute;
  left: 0;
  top: 1mm;
  color: #e0541b;
  font-weight: 700;
  font-size: 14pt;
  line-height: 1;
}

/* ===== SOURCES ===== */
.sources h1 {
  font-size: 22pt;
  margin-bottom: 6mm;
  line-height: 1.15;
}
.sources ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.sources li {
  font-size: 9pt;
  color: #3a3d36;
  padding: 2.5mm 0 2.5mm 8mm;
  border-bottom: 1px solid #ebe7dc;
  line-height: 1.55;
  position: relative;
}
.sources li::before {
  content: "-";
  color: #e0541b;
  font-weight: 600;
  position: absolute;
  left: 0;
  top: 2.5mm;
}
.sources .disclaimer {
  margin-top: 8mm;
  font-size: 8.5pt;
  color: #5a5d56;
  line-height: 1.55;
  font-style: italic;
}
"""

# ===========================================================
# RENDER FUNCTIONS
# ===========================================================

def render_cover():
    return """
<section class="bleed cover">
  <div class="cover-top">
    <span class="badge">Bonus #4 · Carnet Plein® by Mad Makers</span>
    <h1>Le Devis qui<br>Close à 70%.</h1>
    <p class="sub">Template Cialdini-ready, conforme légal 2026. Vos devis passent de 22-30% de signature à 70%, sans baisser vos prix.</p>
  </div>
  <div class="cover-meta">
    <div>
      <div class="accent-line"></div>
      Édition 2026 · 7 principes Cialdini · Conforme loi 2026
    </div>
    <div>carnetplein.mad-makers.fr</div>
  </div>
</section>
"""


def render_intro():
    return """
<section class="page intro">
  <div class="eyebrow">Pourquoi ce template</div>
  <h1>Le devis n'est pas un<br>tableau Excel. C'est une<br>décision difficile à prendre.</h1>

  <p class="lead">Dans le BTP français, le taux moyen de signature d'un devis se situe entre <strong>22 et 30%</strong> selon les études FFB et Effectif Marketing. Le devis envoyé à froid, sans visite préalable, sans personnalisation, sans levier psychologique, perd des dossiers chaque semaine - pas parce que vous êtes trop cher, mais parce que le prospect n'a aucune raison de vous dire oui plutôt qu'à un autre.</p>

  <div class="stats-row">
    <div class="stat">
      <div class="stat-num">22-30%</div>
      <div class="stat-label">taux moyen de signature d'un devis BTP en 2025 (sources FFB, Effectif Marketing, CAPEB)</div>
    </div>
    <div class="stat">
      <div class="stat-num">x3</div>
      <div class="stat-label">multiplication de la conversion documentée par Cialdini quand 3+ principes sont mobilisés en synergie</div>
    </div>
    <div class="stat">
      <div class="stat-num">70%</div>
      <div class="stat-label">objectif atteignable de signature avec un devis Cialdini-ready + relances structurées</div>
    </div>
  </div>

  <div class="callout">
    <h3>Le devis BTP en 2026 doit faire 3 choses en même temps</h3>
    <p><strong>1) Être 100% conforme</strong> aux 20 mentions obligatoires DGCCRF / CNIL / loi Hamon (sinon amendes jusqu'à 75 000 €). <strong>2) Démontrer votre autorité technique</strong> (certifications, assurance, expérience). <strong>3) Mobiliser les leviers psychologiques de décision</strong> (les 7 principes Cialdini), parce qu'un client qui hésite ne signe pas, même quand votre prix est bon.</p>
  </div>

  <h3 style="margin-top:8mm; font-size:14pt;">Comment utiliser ce guide</h3>
  <ol>
    <li><strong>Lisez les 7 principes Cialdini</strong> appliqués au devis BTP (pages suivantes). Chaque principe = pourquoi + actions concrètes + ce qu'on met dans le devis.</li>
    <li><strong>Reprenez votre devis-type actuel</strong> et adaptez-le section par section au template présenté (10 sections, chacune annotée Cialdini).</li>
    <li><strong>Apprenez les 8 réponses aux objections classiques</strong> - à mémoriser ou imprimer pour le terrain.</li>
    <li><strong>Mettez en place la séquence de relances</strong> J+3 / J+7 / J+14 / J+90 - pas de signature sans relance.</li>
    <li><strong>Validez la conformité légale</strong> avec la checklist 20 mentions + tableau TVA 2026 + sanctions.</li>
  </ol>
</section>
"""


def render_principe(p):
    actions = "".join(f"<li>{a}</li>" for a in p['actions'])
    return f"""
<section class="page principe">
  <div class="principe-header">
    <span class="principe-num">PRINCIPE {p['num']} / 7</span>
    <span class="principe-meta">Section : Les 7 leviers Cialdini</span>
  </div>
  <h2>{p['name']}</h2>
  <p class="claim">{p['claim']}</p>

  <p class="principe-why">{p['why']}</p>

  <div class="actions-block">
    <div class="actions-block-header">Actions concrètes en visite et au devis</div>
    <ul>{actions}</ul>
  </div>

  <div class="in-devis-block">
    <div class="in-devis-header">Ce qu'on met dans le devis</div>
    <p>{p['in_devis']}</p>
  </div>
</section>
"""


def render_devis_section(s):
    fields_html = "".join(
        f'<tr><td class="label">{label}</td><td class="value">{value}</td></tr>'
        for label, value in s['fields']
    )

    return f"""
<div class="devis-section">
  <div class="devis-section-header">
    <span class="devis-section-num">SECTION {s['num']} / 10</span>
    <span class="devis-section-title">{s['title']}</span>
  </div>

  <table class="devis-fields">{fields_html}</table>

  <div class="cialdini-note">
    <strong>Levier Cialdini activé</strong>
    {s['cialdini']}
  </div>
</div>
"""


def render_devis_template():
    # Open the template section block on a fresh page; sections will flow with
    # page-break-inside: avoid so each lands cleanly.
    sections_html = "\n".join(render_devis_section(s) for s in DEVIS_SECTIONS)

    return f"""
<section class="page annexe">
  <div class="eyebrow">Template prêt à copier</div>
  <h1>Le devis-type en 10 sections,<br>chacune annotée Cialdini.</h1>

  <p class="lead">Voici la structure complète d'un devis qui combine conformité légale 2026 et les 7 leviers Cialdini. Reprenez chaque section, remplacez les champs entre crochets [CHAMP] par vos infos, et adaptez les libellés à votre métier (chauffagiste, salle de bain, isolation, etc.).</p>

  <div class="placeholders-row cols-4">
    <div class="placeholder-img brand">
      <div class="ph-icon">▣</div>
      <div class="ph-tag">Logo entreprise</div>
      <div class="ph-desc">À insérer en en-tête de tous les devis</div>
    </div>
    <div class="placeholder-img brand">
      <div class="ph-icon">⌖</div>
      <div class="ph-tag">RGE Qualibat</div>
      <div class="ph-desc">Logo certification, +n° à proximité</div>
    </div>
    <div class="placeholder-img brand">
      <div class="ph-icon">⌖</div>
      <div class="ph-tag">Qualigaz / PG</div>
      <div class="ph-desc">Habilitation gaz si chauffagiste</div>
    </div>
    <div class="placeholder-img brand">
      <div class="ph-icon">⌖</div>
      <div class="ph-tag">Partenaire marque</div>
      <div class="ph-desc">Daikin Pro, Atlantic Expert, etc.</div>
    </div>
  </div>

  {sections_html}
</section>
"""


def render_objections():
    cards = "".join(f"""
  <div class="objection-card">
    <div class="objection-q">Objection</div>
    <h4>« {o['objection']} »</h4>
    <div class="objection-r">Votre réponse</div>
    <p class="reponse">{o['reponse']}</p>
    <div class="principe-tag">Cialdini activé : {o['principe']}</div>
  </div>
""" for o in OBJECTIONS)

    return f"""
<section class="page annexe">
  <div class="eyebrow">Les 8 objections classiques + réponses</div>
  <h1>Les phrases qui débloquent<br>une hésitation client.</h1>

  <p class="lead">Pas de magie commerciale. Juste 8 réponses validées par les artisans terrain, chacune appuyée sur un ou plusieurs principes Cialdini. À mémoriser, à reformuler dans vos mots, et à utiliser au téléphone ou en visite.</p>

  {cards}
</section>
"""


def render_relances():
    cards = "".join(f"""
  <div class="relance-card">
    <div class="relance-header">
      <div class="relance-delai">{r['delai']}</div>
      <div class="relance-canal">{r['canal']}</div>
    </div>
    <div class="relance-objet">{r['objet']}</div>
    <div class="relance-corps">{r['corps']}</div>
    <div class="relance-objectif">{r['objectif']}</div>
  </div>
""" for r in RELANCES)

    return f"""
<section class="page annexe">
  <div class="eyebrow">Séquence de relances structurée</div>
  <h1>4 relances, 4 intentions<br>différentes, 0 pression.</h1>

  <p class="lead">90% des artisans qui se plaignent de ne pas signer leurs devis n'ont AUCUNE séquence de relance. Sans relance, le devis envoyé à froid finit dans une pile d'autres devis. Voici la séquence qui marche : J+3 vérification, J+7 conversation, J+14 valeur ajoutée, J+90 sortie propre.</p>

  {cards}

  <div class="callout dark">
    <h3>L'erreur fatale : la relance « commerciale »</h3>
    <p>Une relance qui dit « Bonjour, juste pour savoir si vous avez signé mon devis ? » ne fonctionne pas. Le prospect se ferme. Chaque relance doit apporter quelque chose au client : vérification (J+3), écoute (J+7), preuve fraîche (J+14), respect (J+90).</p>
  </div>
</section>
"""


def render_legal_annex():
    mentions = "".join(f"<li>{m}</li>" for m in MENTIONS_OBLIGATOIRES)
    sanctions = "".join(
        f'<tr><td>{infraction}</td><td class="sanction">{sanction}</td></tr>'
        for infraction, sanction in SANCTIONS
    )
    tva = "".join(
        f'<tr><td class="taux">{taux}</td><td>{cas}</td></tr>'
        for taux, cas in TVA_RULES
    )

    return f"""
<section class="page annexe">
  <div class="eyebrow">Conformité légale 2026 - les 20 mentions</div>
  <h1>Les 20 mentions obligatoires<br>sur tout devis BTP en 2026.</h1>

  <p class="lead">Liste exhaustive vérifiée à mai 2026. L'absence d'une seule de ces mentions peut entraîner amende, invalidité du contrat, ou requalification fiscale. À cocher pour chaque devis envoyé.</p>

  <ol class="numbered-mentions">{mentions}</ol>

  <div class="callout">
    <h3>Évolutions 2025-2026 à connaître</h3>
    <p><strong>Cerfa supprimés (16 février 2025) :</strong> les anciens formulaires Cerfa pour les devis travaux ne sont plus en vigueur. Vous utilisez votre propre modèle, à condition qu'il contienne les 20 mentions ci-dessus.</p>
    <p><strong>MaPrimeRénov' réouvert (23 février 2026) :</strong> guichet ouvert avec quota annuel. Risque de fermeture en cours d'année si épuisement de l'enveloppe.</p>
    <p><strong>Loi anti-fraude RGE :</strong> renforcement des contrôles, sanctions alourdies pour usage abusif du label.</p>
  </div>
</section>

<section class="page annexe">
  <div class="eyebrow">TVA travaux 2026</div>
  <h1>Les 3 taux de TVA et<br>leurs cas d'application.</h1>

  <p class="lead">Erreur fréquente : appliquer 5,5% sur un cas qui devrait être à 10% ou 20%. Le redressement fiscal arrive jusqu'à 4 ans en arrière + 5% d'amende sur la TVA éludée. Tableau de référence vérifié à mai 2026 (loi de finances 2025-2026).</p>

  <table class="ref-table">
    <thead>
      <tr><th style="width:18%;">Taux</th><th>Cas d'application</th></tr>
    </thead>
    <tbody>{tva}</tbody>
  </table>

  <div class="callout dark">
    <h3>Changement majeur 1er mars 2025</h3>
    <p>Depuis le 1er mars 2025, la <strong>fourniture et pose de chaudière à gaz à condensation</strong> est passée du taux réduit 5,5% au taux normal <strong>20%</strong>. Pour un client, cela représente plusieurs centaines à plusieurs milliers d'euros de différence. À expliquer en visite si le client attend des aides ou compare avec un ancien devis. Les chaudières biomasse, PAC et solaire thermique restent éligibles au 5,5%.</p>
  </div>

  <h3>Attestation TVA réduite : format obligatoire</h3>
  <p>Pour appliquer 5,5% ou 10%, vous devez faire signer au client une attestation simplifiée (logement >2 ans, type de travaux, engagement du client à conserver les justificatifs 5 ans). Modèle disponible sur impots.gouv.fr (formulaire 1300-SD ou 1301-SD).</p>
</section>

<section class="page annexe">
  <div class="eyebrow">Sanctions en cas de non-conformité</div>
  <h1>Le coût réel d'un devis<br>non conforme en 2026.</h1>

  <p class="lead">Les sanctions cumulent l'amende administrative (DGCCRF), l'amende pénale (en cas de pratique commerciale trompeuse), et le risque civil (invalidité du contrat, dommages-intérêts). Loin d'être théoriques, ces sanctions sont régulièrement appliquées (cf. rapports annuels DGCCRF 2024-2025).</p>

  <table class="ref-table">
    <thead>
      <tr><th style="width:42%;">Manquement</th><th>Sanction</th></tr>
    </thead>
    <tbody>{sanctions}</tbody>
  </table>

  <div class="callout">
    <h3>Recommandation Carnet Plein®</h3>
    <p>Avant de finaliser votre nouveau devis-type, faites-le valider par un avocat ou un juriste BTP (1 à 2 heures de conseil, 200-400 €). C'est l'assurance la moins chère pour éviter des milliers d'euros d'amende et des contrats nuls. Liste de juristes spécialisés disponible auprès de la FFB et de la CAPEB.</p>
  </div>
</section>

<section class="page annexe">
  <div class="eyebrow">Médiation de la consommation</div>
  <h1>Médiateurs agréés pour<br>le secteur BTP.</h1>

  <p class="lead">Depuis la loi Hamon 2014, tout professionnel doit proposer à ses clients consommateurs un dispositif de médiation gratuit en cas de litige. C'est une mention OBLIGATOIRE sur les devis et conditions générales. Voici les médiateurs les plus utilisés en BTP.</p>

  <h3>CM2C - Centre de Médiation et de Consommation</h3>
  <p>Médiateur référent en BTP. Adhésion gratuite pour la majorité des artisans. Adresse : <strong>49 rue de Ponthieu, 75008 Paris</strong>. Site : <code>cm2c.net</code>. Email : <code>contact@cm2c.net</code>.</p>

  <h3>CNPM - Médiation Consommation</h3>
  <p>Alternative reconnue. Site : <code>cnpm-mediation-consommation.eu</code>. Tarification dégressive selon volume de litiges.</p>

  <h3>Médiateur de la FFB</h3>
  <p>Réservé aux adhérents Fédération Française du Bâtiment. Gratuit pour les adhérents et leurs clients. Renseignement via votre fédération locale.</p>

  <div class="callout">
    <h3>Format de la mention sur le devis</h3>
    <p>« Conformément à l'article L612-1 du Code de la consommation, en cas de litige avec un client consommateur n'ayant pu être résolu à l'amiable, le client peut saisir gratuitement le médiateur de la consommation : <strong>CM2C - 49 rue de Ponthieu, 75008 Paris - cm2c.net</strong>. »</p>
  </div>
</section>
"""


def render_marques():
    grid = "".join(f'<div class="marque-row">{m}</div>' for m in MARQUES_REF)

    return f"""
<section class="page annexe">
  <div class="eyebrow">Autorité par les marques</div>
  <h1>20 marques de référence<br>à mentionner sur le devis.</h1>

  <p class="lead">Citer une marque reconnue dans le détail prestation active le levier d'Autorité (principe 04). Le client n'a pas besoin de connaître techniquement la PAC pour reconnaître Daikin, Atlantic, Mitsubishi. Voici la liste des marques les plus citées et reconnues sur le marché français BTP 2025-2026.</p>

  <div class="marques-grid">{grid}</div>

  <div class="callout">
    <h3>Comment l'utiliser dans le devis</h3>
    <p>Dans le détail prestation, écrivez le nom complet de la référence : <strong>« Pompe à chaleur air/eau Atlantic Alfea Extensa Duo 9 kW »</strong> plutôt que « PAC 9 kW ». La marque rassure, le modèle démontre l'expertise.</p>
    <p>Mentionnez vos partenariats officiels en en-tête : <strong>« Centre installateur agréé Atlantic depuis 2019 »</strong> ou <strong>« Daikin Pro Partner »</strong>. C'est de l'autorité validée par le constructeur.</p>
  </div>
</section>
"""


def render_testimonials():
    return """
<section class="page annexe">
  <div class="eyebrow">Preuve sociale - emplacements dans le devis</div>
  <h1>3 témoignages courts<br>pour le pied du devis.</h1>

  <p class="lead">3 témoignages clients courts (2 à 3 lignes max), avec prénom, initiale du nom, ville et type de chantier, à intégrer en pied de devis ou sur une page jointe « Quelques retours clients récents ». Format placeholder à personnaliser avec vos vrais témoignages.</p>

  <div class="placeholders-row cols-3">
    <div class="placeholder-img testi">
      <div class="ph-icon">"</div>
      <div class="ph-tag">Témoignage 1</div>
      <div class="ph-desc">2-3 lignes max + Prénom Initiale, Ville (XX), type chantier réalisé</div>
    </div>
    <div class="placeholder-img testi">
      <div class="ph-icon">"</div>
      <div class="ph-tag">Témoignage 2</div>
      <div class="ph-desc">Mettre en avant la note Google donnée + 1 verbatim court</div>
    </div>
    <div class="placeholder-img testi">
      <div class="ph-icon">"</div>
      <div class="ph-tag">Témoignage 3</div>
      <div class="ph-desc">Idéal : chantier similaire à celui du prospect (PAC, SDB, etc.)</div>
    </div>
  </div>

  <h3>Format type d'un témoignage qui convertit</h3>
  <p style="background:#ebe7dc;padding:5mm;border-radius:3mm;border-left:3px solid #2d9a5f;font-style:italic;line-height:1.55;">« Installation PAC air/eau Daikin réalisée en mars 2025. Équipe ponctuelle, chantier propre, écart entre devis et facture finale : 0. Économie réelle sur ma facture après 12 mois : 38%. Je recommande sans hésitation. » <strong style="display:block;margin-top:2mm;font-style:normal;">Marie L., Roubaix (59), maison 1960 - 110 m²</strong></p>

  <h3>Emplacements possibles dans le devis</h3>
  <ul>
    <li><strong>Pied de devis</strong> : 1 témoignage court (2 lignes) en bandeau, avec note Google globale</li>
    <li><strong>Page jointe « Quelques chantiers récents »</strong> : 3 témoignages + 3 photos avant/après</li>
    <li><strong>Email d'envoi du devis</strong> : 1 témoignage dans le corps de l'email (« voici un retour client similaire au vôtre »)</li>
    <li><strong>Relance J+14</strong> : nouveau témoignage frais d'un chantier récent + nom du voisin (s'il a donné son accord)</li>
  </ul>

  <div class="callout">
    <h3>Important - accord du client cité</h3>
    <p>Ne JAMAIS citer un client par son nom complet sans accord écrit explicite. Format recommandé : <strong>« Prénom + initiale du nom + ville »</strong>. Pour donner le numéro de téléphone du client à un prospect qui souhaite l'appeler, demandez d'abord l'accord oral du client en question.</p>
  </div>
</section>

<section class="page annexe">
  <div class="eyebrow">Photos avant / après pour le devis</div>
  <h1>2 paires avant/après à<br>joindre au devis.</h1>

  <p class="lead">Joindre 2 paires de photos avant/après de chantiers similaires renforce massivement les principes de Preuve sociale (03) et d'Autorité (04). Le prospect voit que vous avez déjà fait cela, et bien fait. Suivez les règles photo du Bonus #3 pour la qualité.</p>

  <div class="placeholders-row">
    <div class="placeholder-img">
      <div class="ph-icon">▣</div>
      <div class="ph-tag">Photo AVANT 1</div>
      <div class="ph-desc">Ancienne installation, état initial. Même cadrage que le « après »</div>
    </div>
    <div class="placeholder-img testi">
      <div class="ph-icon">▣</div>
      <div class="ph-tag">Photo APRÈS 1</div>
      <div class="ph-desc">Installation neuve, zone nettoyée, plan large</div>
    </div>
  </div>

  <div class="placeholders-row">
    <div class="placeholder-img">
      <div class="ph-icon">▣</div>
      <div class="ph-tag">Photo AVANT 2</div>
      <div class="ph-desc">Autre chantier de référence - similaire au projet client</div>
    </div>
    <div class="placeholder-img testi">
      <div class="ph-icon">▣</div>
      <div class="ph-tag">Photo APRÈS 2</div>
      <div class="ph-desc">Plan détail valorisant la finition + marque visible</div>
    </div>
  </div>

  <div class="callout">
    <h3>Astuce conversion</h3>
    <p>Choisissez des paires avant/après de chantiers GÉOGRAPHIQUEMENT proches du prospect (même département, idéalement même ville/canton). Cela active le levier d'Unité (07) : « ce sont les mêmes maisons, le même bâti, le même climat ». La preuve sociale géographiquement proche est 2 à 3 fois plus puissante que générique.</p>
  </div>
</section>
"""


def render_checklist():
    return """
<section class="page annexe">
  <div class="eyebrow">Aide-mémoire avant envoi</div>
  <h1>La checklist à cocher<br>avant chaque envoi de devis.</h1>

  <p class="lead">À cocher mentalement (ou physiquement, en imprimant cette page) avant chaque envoi de devis. 5 minutes de vérification = 0 amende et un devis qui maximise vos chances de signature.</p>

  <div class="checklist-print">
    <h2>CONFORMITÉ LÉGALE</h2>

    <h3>Identité et coordonnées</h3>
    <ul>
      <li>Logo entreprise + nom commercial + forme juridique</li>
      <li>Adresse siège + téléphone + email + site</li>
      <li>SIRET + RCS + APE + N° TVA intracommunautaire</li>
      <li>Logos certifications RGE / Qualibat / Qualigaz / PG visibles</li>
      <li>Mention assurance décennale (assureur, n° police, zone)</li>
      <li>Mention médiateur conso (CM2C ou autre)</li>
    </ul>

    <h3>Devis</h3>
    <ul>
      <li>Date d'établissement du devis</li>
      <li>Durée de validité affichée (3 mois recommandé)</li>
      <li>Mention « Devis gratuit »</li>
      <li>Détail des prestations (quantité, unité, prix unitaire HT)</li>
      <li>TVA : taux appliqué + montant TVA + total TTC en chiffres ET en lettres si >1500 €</li>
      <li>Modalités de paiement (acompte, échéances)</li>
      <li>Délai de réalisation (date de démarrage + durée)</li>
      <li>Garanties (décennale + biennale + parfait achèvement)</li>
      <li>Mention manuscrite « Bon pour accord » + signatures</li>
    </ul>

    <h3>Cas particuliers</h3>
    <ul>
      <li>Si démarchage : bordereau de rétractation 14 jours joint</li>
      <li>Si TVA réduite : attestation 1300-SD ou 1301-SD jointe</li>
      <li>Si aides MaPrimeRénov' / CEE : taux et conditions vérifiés au jour J</li>
      <li>Si client professionnel : pénalités de retard + indemnité 40 €</li>
    </ul>
  </div>
</section>

<section class="page annexe">
  <div class="checklist-print">
    <h2>LEVIERS CIALDINI ACTIVÉS</h2>

    <h3>Réciprocité (01)</h3>
    <ul>
      <li>Audit thermique / mini-rapport offert mentionné dans le devis</li>
      <li>Guide PDF entretien chaudière joint ou proposé</li>
      <li>3 références chantiers similaires disponibles sur demande</li>
    </ul>

    <h3>Engagement et cohérence (02)</h3>
    <ul>
      <li>Préambule rappelant les points validés en visite</li>
      <li>3 options (Confort / Performance / Premium) - le client choisit</li>
      <li>Acompte 30% à la signature</li>
    </ul>

    <h3>Preuve sociale (03)</h3>
    <ul>
      <li>3 témoignages courts en pied de devis ou page jointe</li>
      <li>Note Google + nombre d'avis mentionnés</li>
      <li>Nombre d'installations réalisées dans l'année cité</li>
    </ul>

    <h3>Autorité (04)</h3>
    <ul>
      <li>4 logos certifications visibles en en-tête</li>
      <li>Années d'expérience + nombre d'installations</li>
      <li>1 ou 2 partenariats marque cités (Atlantic Expert, Daikin Pro)</li>
      <li>Signature manuscrite du dirigeant en pied de devis</li>
    </ul>

    <h3>Sympathie (05)</h3>
    <ul>
      <li>Salutation personnalisée au prénom du client</li>
      <li>Rappel du contexte de visite (date, ville, contraintes évoquées)</li>
      <li>Mention « Entreprise familiale [VILLE] depuis [ANNÉE] »</li>
      <li>Photo du dirigeant (en EPI, pas en costume)</li>
    </ul>

    <h3>Rareté (06)</h3>
    <ul>
      <li>Durée de validité du devis affichée</li>
      <li>Créneau de pose réservé jusqu'au [DATE]</li>
      <li>Dates butoirs des aides 2026 rappelées</li>
      <li>Annonce hausse fournisseur si réelle (jamais inventée)</li>
    </ul>

    <h3>Unité (07)</h3>
    <ul>
      <li>Usage du « nous » (« nous avons regardé ensemble »)</li>
      <li>Référence au type de logement / région partagés</li>
      <li>Valeurs communes mentionnées (qualité, durabilité, locale)</li>
    </ul>

    <h3>Photos et annexes</h3>
    <ul>
      <li>2 paires avant/après de chantiers similaires jointes</li>
      <li>Page jointe « Quelques chantiers récents » prête</li>
      <li>Plaquette PDF ou lien fiche Google joint</li>
    </ul>
  </div>
</section>
"""


def render_cta():
    return """
<section class="bleed cta-page">
  <div class="eyebrow">- Aller plus loin</div>
  <h2>Chez Carnet Plein® by Mad Makers,<br>on industrialise votre devis qui close.</h2>
  <p>Vous avez le template, les principes, les objections, les relances. Mais entre le PDF dans votre Drive et le devis envoyé sans faute le bon jour, il y a un fossé : la mise en pratique répétée.</p>
  <p>Dans le programme Accélérateur Carnet Plein®, on installe avec vous : le devis-type personnalisé à votre charte (1 demi-journée), la séquence de relances automatisée (CRM léger), la grille des 8 objections imprimée dans votre van, et 4 sessions de coaching pour adapter le discours à votre marché.</p>
  <p>Objectif : passer de 22-30% à 55-70% de signature en 90 jours. Sans baisser vos prix.</p>
  <a href="https://carnetplein.mad-makers.fr" class="button">Audit gratuit 20 min → carnetplein.mad-makers.fr</a>
</section>
"""


def render_sources():
    sources = [
        "<strong>Cialdini - sources principales :</strong> Robert B. Cialdini, <em>Influence: The Psychology of Persuasion</em> (édition révisée 2021) · Robert B. Cialdini, <em>Pre-Suasion</em> (2016, ajout du 7e principe Unité) · Influence at Work (influenceatwork.com)",
        "<strong>Études BTP françaises :</strong> FFB - Observatoire de l'artisanat du bâtiment 2024-2025 · CAPEB - rapport annuel signature devis · Effectif Marketing - étude 2024 sur le taux moyen de signature de devis BTP",
        "<strong>Mentions légales et conformité :</strong> DGCCRF (economie.gouv.fr/dgccrf) · Code de la consommation - articles L611-1 à L612-5 (médiation) · Code des assurances - articles L241-1 et L241-2 (assurance décennale) · Loi Hamon 2014 · Loi de finances 2025 (TVA chaudière gaz 20%)",
        "<strong>Aides 2026 :</strong> ANAH - MaPrimeRénov' (anah.fr/maprimerenov) · France Rénov' (france-renov.gouv.fr) · ADEME - Coup de pouce CEE · impots.gouv.fr (Éco-PTZ, attestation TVA 1300-SD)",
        "<strong>Certifications et RGE :</strong> Qualibat (qualibat.com) · Qualigaz (qualigaz.com) · Qualifelec (qualifelec.fr) · Loi anti-fraude RGE 2025",
        "<strong>Médiation de la consommation :</strong> CM2C (cm2c.net) · CNPM Médiation Consommation (cnpm-mediation-consommation.eu) · FFB - médiation de branche",
        "<strong>Sources secondaires :</strong> Habitatpresto · OBAT · Tactidevis · Partoo · Digibat · SK Web · Phaos Studio · Agence ZM",
        "<strong>Données vérifiées au :</strong> mai 2026 (loi de finances 2025-2026, MaPrimeRénov' barème 2026)",
    ]
    sources_html = "".join(f"<li>{s}</li>" for s in sources)

    return f"""
<section class="page sources">
  <div class="eyebrow">Sources et références</div>
  <h1>Les références derrière<br>la méthode et le cadre légal.</h1>

  <ul>{sources_html}</ul>

  <div class="disclaimer">
    Document à usage interne du client. Édition mai 2026 - mise à jour conforme aux évolutions législatives 2025-2026 (TVA chaudière gaz à 20%, suppression Cerfa au 16 février 2025, réouverture MaPrimeRénov' au 23 février 2026). Les statistiques de signature de devis BTP (22-30% moyenne, 70% objectif Cialdini-ready) sont des moyennes observées sur le marché français. Les sanctions citées (DGCCRF, pénales, fiscales) reflètent les barèmes en vigueur en 2026 mais peuvent évoluer. Pour une utilisation commerciale du template de devis, faire valider la version finale par un avocat ou un juriste BTP. Les principes Cialdini sont des outils de persuasion éthique : la rareté ne doit jamais être inventée, les références doivent être vraies, les témoignages doivent avoir l'accord écrit du client cité. Mise à jour annuelle de ce document recommandée (janvier de chaque année).
  </div>
</section>
"""


def render_html():
    parts = [
        render_cover(),
        render_intro(),
    ]

    # Section separator for the 7 Cialdini principles
    parts.append("""
<section class="bleed section-sep">
  <div class="label">- Les 7 leviers Cialdini</div>
  <h2>Sept leviers qui transforment<br>un devis en signature.</h2>
  <div class="count">Principes 01 à 07</div>
  <p class="desc">Robert Cialdini a documenté en 40 ans de recherche les 7 principes universels qui déterminent la décision humaine. Voici comment chacun se transpose dans un devis BTP de 2026 - sans manipulation, sans technique louche, juste de la psychologie de la décision appliquée à un document commercial.</p>
</section>
""")

    for principe in CIALDINI:
        parts.append(render_principe(principe))

    # Section separator for devis template
    parts.append("""
<section class="bleed section-sep">
  <div class="label">- Le template devis</div>
  <h2>Dix sections, chacune<br>annotée Cialdini.</h2>
  <div class="count">Sections 01 à 10</div>
  <p class="desc">Le template de devis complet, prêt à copier dans votre logiciel ou Word. Chaque section indique les champs à remplir, les placeholders pour images (logos, certifications), et la note Cialdini correspondante. Adaptez les libellés à votre métier.</p>
</section>
""")

    parts.append(render_devis_template())

    # Section separator for objections
    parts.append("""
<section class="bleed section-sep">
  <div class="label">- Les 8 objections + réponses</div>
  <h2>Huit phrases qui font<br>basculer une décision.</h2>
  <div class="count">Objections 01 à 08</div>
  <p class="desc">Les 8 objections client les plus fréquentes dans le BTP français, avec la réponse exacte à donner - ou à adapter à votre voix. Chaque réponse mobilise 1 à 3 principes Cialdini. À mémoriser ou imprimer pour le terrain et le téléphone.</p>
</section>
""")

    parts.append(render_objections())

    # Section separator for relances
    parts.append("""
<section class="bleed section-sep">
  <div class="label">- La séquence de relances</div>
  <h2>Quatre relances, aucune<br>pression, plus de signatures.</h2>
  <div class="count">J+3 / J+7 / J+14 / J+90</div>
  <p class="desc">Sans séquence de relance, le devis envoyé à froid finit oublié au milieu d'autres. Avec ces 4 relances structurées, vous gardez la conversation ouverte, apportez de la valeur, et créez des occasions naturelles de signer - sans relance « commerciale ».</p>
</section>
""")

    parts.append(render_relances())

    # Section separator for legal annex
    parts.append("""
<section class="bleed section-sep">
  <div class="label">- Annexe légale 2026</div>
  <h2>Vingt mentions, trois taux<br>TVA, sept sanctions.</h2>
  <div class="count">Conformité légale</div>
  <p class="desc">L'annexe légale à jour mai 2026 : les 20 mentions obligatoires DGCCRF / CNIL / loi Hamon, les 3 taux TVA et leurs cas d'application, les sanctions encourues en cas de non-conformité, et les médiateurs de la consommation agréés pour le secteur BTP.</p>
</section>
""")

    parts.append(render_legal_annex())
    parts.append(render_marques())

    # Section separator for testimonials/photos
    parts.append("""
<section class="bleed section-sep">
  <div class="label">- Placeholders preuve sociale</div>
  <h2>Témoignages et photos<br>à intégrer au devis.</h2>
  <div class="count">Préparation visuelle</div>
  <p class="desc">Les placeholders à remplacer par vos propres témoignages clients et photos avant/après. Suivez les règles du Bonus #3 pour la qualité des photos, et l'accord écrit signé pour la diffusion des verbatims clients.</p>
</section>
""")

    parts.append(render_testimonials())
    parts.append(render_checklist())
    parts.append(render_cta())
    parts.append(render_sources())

    body = "\n".join(parts)

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Le Devis qui Close a 70% - Carnet Plein® by Mad Makers</title>
<link rel="preconnect" href="https://fonts.bunny.net" crossorigin>
<link rel="stylesheet" href="https://fonts.bunny.net/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap">
<style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>
"""


if __name__ == "__main__":
    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "04-devis-close-70.html"
    )
    html_content = render_html()

    # Hard guard : zero em-dash allowed
    if "—" in html_content:
        n = html_content.count("—")
        raise RuntimeError(f"Em-dash detecte dans le HTML : {n} occurrences. Corriger avant ecriture.")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    size_kb = os.path.getsize(out_path) / 1024
    print(f"OK - HTML ecrit : {out_path}")
    print(f"     Taille : {size_kb:.1f} Ko")
    print(f"     Em-dash : 0 (verifie)")
    print(f"     Pages estimees : ~38 (cover + intro + 7 principes + 10 sections devis + 8 objections + 4 relances + annexe legale + marques + testi/photos + checklist + CTA + sources)")
    print()
    print("PROCHAINE ETAPE :")
    print("  1. Ouvrir le .html dans Chrome")
    print("  2. Ctrl+P (Imprimer)")
    print("  3. Destination : Enregistrer au format PDF")
    print("  4. Marges : Aucune (le CSS gere)")
    print("  5. Cocher Graphiques d'arriere-plan")
    print("  6. Enregistrer sous : Le Devis qui Close a 70% - BONUS #4.pdf")
