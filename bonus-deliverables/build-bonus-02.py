#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for Bonus #2:
"30 Réponses Prêtes à l'Emploi - Le pack de modèles pour répondre
à chaque avis Google en 2 minutes"
Carnet Plein(R) by Mad Makers - Édition 2026

Generates 02-30-reponses-avis-google.html in this folder.
Open in Chrome -> File > Print > Save as PDF (A4 portrait).
"""
import os

# ===========================================================
# DATA - 30 TEMPLATES
# ===========================================================

POSITIFS = [
    {
        "num": "01",
        "title": "Avis 5★ enthousiaste générique",
        "when": "Avis 5 étoiles court ou général, sans détail spécifique sur la prestation.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour ces mots. Ravi que vous soyez satisfait. À votre service quand vous voudrez.\n\n"
            "[PRENOM PATRON] · [NOM ENTREPRISE]"
        ),
        "tip": "Si une prestation est mentionnée dans l'avis (dépannage, pose, devis), reprenez-la dans la réponse pour montrer que vous avez lu.",
        "antipattern": "Pas de « Votre satisfaction est notre priorité ». Trop corporate, sonne faux.",
        "delay": "Sous 7 jours",
        "seo": "Si possible mentionnez le métier (ex. plombier-chauffagiste).",
    },
    {
        "num": "02",
        "title": "Avis 5★ - Dépannage urgent réussi",
        "when": "L'avis mentionne une intervention urgente (panne, fuite, week-end).",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour ces mots. Une [TYPE PANNE] qui lâche un dimanche, ça n'arrange personne. Content qu'on ait pu intervenir vite.\n\n"
            "À votre service.\n\n"
            "[PRENOM PATRON] · [NOM ENTREPRISE]"
        ),
        "tip": "Adaptez [TYPE PANNE] au contexte (chaudière, fuite, ballon, WC).",
        "antipattern": "Ne promettez pas « disponibles 24/7 » si ce n'est pas vrai - vous vous engagez.",
        "delay": "Sous 7 jours",
        "seo": "« dépannage urgent », « intervention rapide » + ville.",
    },
    {
        "num": "03",
        "title": "Avis 5★ - Installation chaudière",
        "when": "Post-installation chaudière gaz, condensation ou fioul.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour votre confiance. Heureux que la chaudière vous donne satisfaction. "
            "Un rappel utile : l'entretien annuel est obligatoire (décret du 9 juin 2009). On vous recontactera dans l'année.\n\n"
            "À bientôt.\n\n"
            "[PRENOM PATRON] · [NOM ENTREPRISE], artisan QualiGaz"
        ),
        "tip": "Mention QualiGaz en signature = SEO local + confiance.",
        "antipattern": "Pas de promesse de prix sur le futur entretien. Engagement commercial.",
        "delay": "Sous 7 jours",
        "seo": "« installation chaudière » + ville + « QualiGaz ».",
    },
    {
        "num": "04",
        "title": "Avis 5★ - Installation pompe à chaleur",
        "when": "Post-installation PAC air-eau ou air-air.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour ces mots. Heureux que votre pompe à chaleur vous donne satisfaction. "
            "N'hésitez pas à nous solliciter pour l'entretien annuel - c'est ce qui garde la machine au mieux dans la durée.\n\n"
            "[PRENOM PATRON] · [NOM ENTREPRISE], artisan RGE QualiPAC"
        ),
        "tip": "Mention « RGE QualiPAC » en signature = signal MaPrimeRénov'.",
        "antipattern": "Pas de chiffre de performance (COP, économies). Engagement de résultat (art. 1231-1).",
        "delay": "Sous 7 jours",
        "seo": "« pompe à chaleur » + ville + « RGE QualiPAC ».",
    },
    {
        "num": "05",
        "title": "Avis 5★ - Entretien annuel",
        "when": "Client récurrent en contrat d'entretien ou habitué.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour votre fidélité. À l'année prochaine.\n\n"
            "[PRENOM PATRON]"
        ),
        "tip": "Ultra-courte volontairement. La fidélité parle d'elle-même.",
        "antipattern": "Trop long sonne forcé. La brièveté EST le compliment.",
        "delay": "Sous 7 jours",
        "seo": "« entretien annuel » subtil.",
    },
    {
        "num": "06",
        "title": "Avis 5★ - Rénovation salle de bain complète",
        "when": "Avis sur gros chantier : SDB complète, plomberie globale.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour ces mots. Une rénovation complète, c'est toujours un projet exigeant - pour vous comme pour nous. "
            "Heureux qu'elle vous plaise et tienne ses promesses dans la durée.\n\n"
            "[PRENOM PATRON] · [NOM ENTREPRISE]"
        ),
        "tip": "Reconnaissez l'ampleur du projet - ça valorise le travail accompli.",
        "antipattern": "Pas de mention du tarif ou de la durée. Pas pertinent en public.",
        "delay": "Sous 7 jours",
        "seo": "« rénovation salle de bain » + ville.",
    },
    {
        "num": "07",
        "title": "Avis 5★ - Mentionnant un collaborateur par son prénom",
        "when": "L'avis cite un employé (ex. : « Marc a été super »).",
        "reply": (
            "Bonjour [PRENOM CLIENT],\n\n"
            "Merci pour ces mots. Je transmets votre message à [PRENOM EMPLOYE] - ça lui fera vraiment plaisir.\n\n"
            "Toute l'équipe vous remercie.\n\n"
            "[PRENOM PATRON]"
        ),
        "tip": "Reprenez UNIQUEMENT le prénom de l'employé tel qu'il apparaît dans l'avis. Jamais son nom complet (RGPD).",
        "antipattern": "Pas de blague interne (« Marc va être surpris de cet avis »). Manque de pro.",
        "delay": "Sous 7 jours",
        "seo": "-",
    },
    {
        "num": "08",
        "title": "Avis 4★ avec petite réserve constructive",
        "when": "Avis globalement positif (4★) avec une critique mineure.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour ce retour, le détail compte. Je note votre remarque sur [POINT MENTIONNE] - c'est utile pour progresser.\n\n"
            "À votre service en cas de besoin.\n\n"
            "[PRENOM PATRON] · [NOM ENTREPRISE]"
        ),
        "tip": "Acknowledge le point précis sans excuse formelle ni défense.",
        "antipattern": "Pas de défense (« en fait c'était parce que... »). Accueillir la critique fait gagner du capital confiance.",
        "delay": "48-72h (action plus rapide)",
        "seo": "-",
    },
    {
        "num": "09",
        "title": "Avis positif sur respect du devis / transparence",
        "when": "Le client salue le respect du devis, pas de surprise sur la facture.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour ces mots. La transparence sur le devis, c'est la base - on essaie de la tenir sur chaque chantier.\n\n"
            "À votre service.\n\n"
            "[PRENOM PATRON] · [NOM ENTREPRISE]"
        ),
        "tip": "Confirmez la valeur (transparence) sans en faire trop. C'est un signal SEO ET commercial fort.",
        "antipattern": "Pas de « contrairement à nos concurrents ». Dénigrement (art. 1240 Code civil).",
        "delay": "Sous 7 jours",
        "seo": "« devis transparent », « devis détaillé ».",
    },
    {
        "num": "10",
        "title": "Avis 5★ - Client récurrent / fidèle",
        "when": "Vous reconnaissez le nom : c'est un habitué.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci. Toujours un plaisir d'intervenir chez vous. À très bientôt.\n\n"
            "[PRENOM PATRON]"
        ),
        "tip": "Ultra-courte, ton chaleureux. La récurrence parle d'elle-même.",
        "antipattern": "Pas de « comme d'habitude » - sonne automatique et brise l'instant.",
        "delay": "Sous 7 jours",
        "seo": "-",
    },
]

NEGATIFS = [
    {
        "num": "11",
        "title": "Retard d'intervention",
        "when": "Le client se plaint d'un créneau non tenu ou d'un retard significatif.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour votre retour. Je comprends que le décalage d'horaire a posé problème - on essaie de tenir les créneaux mais certains chantiers se compliquent et impactent ceux qui suivent. Pas une excuse, juste une explication.\n\n"
            "Pour qu'on en parle de vive voix et trouver une suite, vous pouvez me joindre au [NUMERO DIRECT].\n\n"
            "[PRENOM PATRON]"
        ),
        "tip": "S'excuser du RESSENTI, pas de la faute (« je comprends que ça a posé problème »). Engage moins.",
        "antipattern": "Pas « les aléas font partie du métier ». Trop défensif, balaie la plainte.",
        "delay": "48-72h impérativement",
        "seo": "-",
    },
    {
        "num": "12",
        "title": "Surcoût « découverte chantier »",
        "when": "Plainte sur facture > devis initial, surcoût non anticipé.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour ce retour. Un surcoût en cours de chantier, c'est toujours désagréable - surtout quand on s'attend à autre chose au départ.\n\n"
            "Pour qu'on revoie ensemble le détail de la facture et l'écart par rapport au devis initial, n'hésitez pas à m'appeler au [NUMERO].\n\n"
            "[PRENOM PATRON]"
        ),
        "tip": "« Examiner ensemble » est la formule magique - propose, n'accuse pas.",
        "antipattern": "JAMAIS de mention du montant en public (RGPD). JAMAIS de « comme stipulé dans le devis » (sec, défensif).",
        "delay": "48-72h",
        "seo": "-",
    },
    {
        "num": "13",
        "title": "Devis MaPrimeRénov' contesté",
        "when": "Plainte : dossier mal monté, non transmis, gonflé, refusé par l'Anah.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour votre retour. La constitution d'un dossier MaPrimeRénov' a beaucoup de paramètres (catégorie de revenus, type d'équipement, attestations, validation Anah). "
            "Pour qu'on regarde ensemble où votre dossier en est exactement, contactez-nous au [NUMERO]. Notre équipe administrative connaît bien le sujet.\n\n"
            "[PRENOM PATRON]"
        ),
        "tip": "Mentionnez « équipe administrative » - rassure les futurs prospects sur votre sérieux.",
        "antipattern": "Pas de « c'est la faute de l'Anah ». Pas de défausse.",
        "delay": "48-72h",
        "seo": "« MaPrimeRénov' » subtile.",
    },
    {
        "num": "14",
        "title": "Fuite ou défaut post-intervention (garantie biennale)",
        "when": "Un défaut technique signalé peu après l'intervention.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci de nous signaler ce point. Une fuite peu après une intervention, c'est toujours préoccupant - et précisément ce que couvre la garantie biennale (art. 1792-3 Code civil) qui s'applique sur nos prestations.\n\n"
            "Appelez-nous au [NUMERO], on programme une visite SAV cette semaine.\n\n"
            "[PRENOM PATRON]"
        ),
        "tip": "Mention de la garantie biennale = rassurance prospect + cadre légal sans aveu.",
        "antipattern": "JAMAIS « nous avons mal posé » = aveu opposable. JAMAIS « nous remboursons » = engagement irrévocable.",
        "delay": "24-48h (urgent)",
        "seo": "-",
    },
    {
        "num": "15",
        "title": "PAC qui ne chauffe pas suffisamment",
        "when": "PAC sous-dimensionnée ou mal réglée, plainte sur performance.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour ce retour. Une pompe à chaleur peut nécessiter un ajustement de dimensionnement ou de réglage selon la maison et la saison.\n\n"
            "Pour qu'on regarde précisément ce qui se passe chez vous, contactez-nous au [NUMERO] - on programme un passage technique.\n\n"
            "[PRENOM PATRON] · artisan RGE QualiPAC"
        ),
        "tip": "« Dimensionnement » = explication factuelle, pas une excuse. Mention RGE QualiPAC rassure.",
        "antipattern": "JAMAIS « votre maison est mal isolée » = blâme client, contre-productif.",
        "delay": "48-72h",
        "seo": "-",
    },
    {
        "num": "16",
        "title": "PAC bruyante / claquements",
        "when": "Plainte sur bruit, vibrations, claquements d'une PAC.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour ce retour. Un bruit anormal sur une PAC peut venir de plusieurs choses - fixation, réglage, ou pièce qui demande à être revue.\n\n"
            "Appelez-nous au [NUMERO] cette semaine, on vient diagnostiquer sur place.\n\n"
            "[PRENOM PATRON]"
        ),
        "tip": "Ouvrir plusieurs causes possibles, sans s'engager sur l'origine en public.",
        "antipattern": "JAMAIS « c'est normal ». Minimisation = effet inverse.",
        "delay": "48-72h",
        "seo": "-",
    },
    {
        "num": "17",
        "title": "Communication SAV insuffisante",
        "when": "Plainte « personne ne répond, pas de retour, je dois relancer ».",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour ce retour, je le prends au sérieux. La communication SAV est un point sur lequel on travaille - vous m'aidez à identifier où ça coince.\n\n"
            "Pouvez-vous me joindre directement au [NUMERO DIRECT] cette semaine ? Je m'occupe personnellement de votre dossier.\n\n"
            "[PRENOM PATRON]"
        ),
        "tip": "« Numéro direct » + « personnellement » = engagement palpable, perçu sincère.",
        "antipattern": "Pas de « notre standard est débordé ». Excuse externe qui irrite.",
        "delay": "24-48h",
        "seo": "-",
    },
    {
        "num": "18",
        "title": "Propreté du chantier",
        "when": "Plainte sur poussière, traces, déchets laissés, bâche oubliée.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour ce retour. La propreté en fin de chantier, c'est un point qu'on doit toujours rendre impeccable - visiblement pas le cas chez vous.\n\n"
            "Appelez-nous au [NUMERO], on s'organise pour repasser.\n\n"
            "[PRENOM PATRON]"
        ),
        "tip": "Reconnaître le ressenti + offrir un retour sur place. Geste fort, peu coûteux.",
        "antipattern": "JAMAIS « le client doit finir le nettoyage ». Argument faible et faux.",
        "delay": "48-72h",
        "seo": "-",
    },
    {
        "num": "19",
        "title": "Comportement d'un technicien",
        "when": "Plainte sur ton, attitude, manque de respect d'un employé.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour ce retour, c'est important pour nous. Le comportement de nos équipes face aux clients est un sujet sur lequel nous sommes exigeants.\n\n"
            "Appelez-moi au [NUMERO], j'aimerais comprendre précisément ce qui s'est passé pour qu'on en tire les leçons.\n\n"
            "[PRENOM PATRON]"
        ),
        "tip": "Ne pas défendre l'employé en public, même si vous estimez la critique injuste. Inviter en privé.",
        "antipattern": "JAMAIS « nos techniciens sont toujours irréprochables ». Faux et défensif.",
        "delay": "24-48h",
        "seo": "-",
    },
    {
        "num": "20",
        "title": "Délai pièces détachées",
        "when": "Plainte sur délai d'approvisionnement d'une pièce.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour ce retour. Les délais de certaines pièces se sont allongés cette année - ça nous embête autant que vous.\n\n"
            "Pour qu'on vous fasse un point précis sur où en est votre commande, contactez-nous au [NUMERO].\n\n"
            "[PRENOM PATRON]"
        ),
        "tip": "Reconnaître le problème filière sans s'en servir comme excuse complète.",
        "antipattern": "Pas de « la pénurie n'est pas de notre faute ». Trop défensif, ferme le dialogue.",
        "delay": "48-72h",
        "seo": "-",
    },
    {
        "num": "21",
        "title": "Devis jugé trop cher (sans intervention)",
        "when": "Plainte sur prix d'un devis non signé. Le client n'est pas client, mais l'avis pèse.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour votre retour. Le prix d'un devis dépend de beaucoup d'éléments : matériel, durée, garanties incluses, certifications. Difficile à comparer point par point sans le contexte complet.\n\n"
            "Si vous souhaitez qu'on revoie ensemble la composition du devis ou qu'on regarde des alternatives, contactez-moi au [NUMERO].\n\n"
            "[PRENOM PATRON]"
        ),
        "tip": "Ne pas justifier le prix en public. Inviter à discuter, le prospect lecteur appréciera la posture ouverte.",
        "antipattern": "JAMAIS « nos concurrents sont moins chers parce qu'ils [...] ». Dénigrement (art. 1240).",
        "delay": "Sous 7 jours",
        "seo": "-",
    },
    {
        "num": "22",
        "title": "Insatisfaction finition",
        "when": "Plainte sur joints, alignement, esthétique du rendu final.",
        "reply": (
            "Bonjour [PRENOM],\n\n"
            "Merci pour ce retour. La finition fait toute la différence - sans elle, le travail n'est pas complet.\n\n"
            "Appelez-nous au [NUMERO], on programme un passage cette semaine pour reprendre les points qui ne vont pas.\n\n"
            "[PRENOM PATRON]"
        ),
        "tip": "Acknowledge l'importance de la finition. Offre un retour sur site - ça coûte peu et ça vaut beaucoup.",
        "antipattern": "JAMAIS « ce sont des défauts de moins de 1 mm ». Minimisation technique.",
        "delay": "48-72h",
        "seo": "-",
    },
]

DIFFAMATOIRES = [
    {
        "num": "23",
        "title": "Avis manifestement faux (jamais client)",
        "when": "Après vérification de vos archives, aucune intervention sous ce nom.",
        "reply": (
            "Bonjour,\n\n"
            "Après vérification de nos dossiers, nous ne trouvons aucune trace d'intervention sous ce nom. Peut-être une confusion d'entreprise ou un dépôt erroné.\n\n"
            "Si vous estimez avoir été en relation avec nous, contactez-nous au [NUMERO] pour clarifier.\n\n"
            "[NOM ENTREPRISE]"
        ),
        "tip": "Ton neutre, factuel, sans accusation. Signaler à Google (motif « hors-sujet » ou « spam »). Faire constat d'huissier dans les 3 mois.",
        "antipattern": "JAMAIS « cet avis est faux » publiquement. Constater factuellement suffit, l'accusation peut se retourner.",
        "delay": "24-48h + signalement immédiat",
        "seo": "-",
    },
    {
        "num": "24",
        "title": "Avis concurrent identifié",
        "when": "Profil sans avis ailleurs, timing suspect, langage métier inversé.",
        "reply": (
            "Bonjour,\n\n"
            "Après vérification, nous ne retrouvons pas d'intervention correspondant à ce profil. Si une erreur d'entreprise s'est glissée, n'hésitez pas à nous contacter directement au [NUMERO].\n\n"
            "[NOM ENTREPRISE]"
        ),
        "tip": "Signalement Google immédiat (motif « conflit d'intérêts »). Constat d'huissier si récurrent. Avocat si pattern établi.",
        "antipattern": "JAMAIS nommer le concurrent en public. Diffamation immédiate.",
        "delay": "24h",
        "seo": "-",
    },
    {
        "num": "25",
        "title": "Avis d'ancien salarié",
        "when": "Profil que vous reconnaissez comme ancien collaborateur.",
        "reply": (
            "Bonjour,\n\n"
            "Nous n'identifions pas cette personne dans notre fichier client. Si une erreur s'est glissée, vous pouvez nous joindre au [NUMERO].\n\n"
            "[NOM ENTREPRISE]"
        ),
        "tip": "Signaler Google « conflit d'intérêts ». Si récurrent, mise en demeure par avocat (~500€).",
        "antipattern": "JAMAIS mentionner la relation de travail antérieure en public. Diffamation et violation RGPD du salarié.",
        "delay": "24h",
        "seo": "-",
    },
    {
        "num": "26",
        "title": "Insulte ou injure caractérisée",
        "when": "Termes injurieux sans fait précis (escroc, voleur, malhonnête).",
        "reply": (
            "Bonjour,\n\n"
            "Nous prenons note de votre retour, mais le ton employé ne nous permet pas d'y donner suite ici.\n\n"
            "Pour échanger sur le fond, vous pouvez nous joindre au [NUMERO].\n\n"
            "[PRENOM PATRON]"
        ),
        "tip": "Très court. Signalement Google (motif « langage offensant »). L'injure publique = jusqu'à 12 000€ d'amende (loi 1881, art. 33).",
        "antipattern": "JAMAIS répondre sur le même ton. Effet boomerang sur votre image.",
        "delay": "24h + signalement",
        "seo": "-",
    },
    {
        "num": "27",
        "title": "Allégation de surfacturation type « arnaque »",
        "when": "Le mot « arnaque » est utilisé, sans détail factuel.",
        "reply": (
            "Bonjour,\n\n"
            "Merci pour ce retour. La transparence du devis est un point sur lequel nous sommes très attentifs.\n\n"
            "Pour qu'on revoie ensemble la facture point par point, n'hésitez pas à me joindre au [NUMERO].\n\n"
            "[PRENOM PATRON]"
        ),
        "tip": "Ne PAS reprendre le mot « arnaque ». Reformuler en termes neutres. Si récurrent, action en dénigrement (art. 1240).",
        "antipattern": "JAMAIS « ce mot est diffamatoire » ou « nous nous réservons des poursuites ». Effet Streisand garanti.",
        "delay": "24-48h",
        "seo": "-",
    },
    {
        "num": "28",
        "title": "Allégation d'incompétence sans fondement",
        "when": "« Travail bâclé », « ne savent pas faire », sans détail technique.",
        "reply": (
            "Bonjour,\n\n"
            "Merci pour votre retour. Pour qu'on regarde ensemble précisément ce qui n'a pas convenu, contactez-nous au [NUMERO].\n\n"
            "[PRENOM PATRON]"
        ),
        "tip": "Court et factuel. Invitation au privé. Constat d'huissier si récurrent.",
        "antipattern": "Pas de défense de compétence (« nos techniciens ont 20 ans d'expérience »). Sonne défensif.",
        "delay": "48-72h",
        "seo": "-",
    },
    {
        "num": "29",
        "title": "Confusion avec entreprise homonyme",
        "when": "Le client cite un détail qui ne correspond pas (ville inconnue, équipe différente).",
        "reply": (
            "Bonjour,\n\n"
            "Après vérification, votre avis semble concerner une autre entreprise de plomberie portant un nom similaire. Pouvez-vous vérifier auprès de votre artisan d'intervention ?\n\n"
            "Vous pouvez aussi nous joindre au [NUMERO] pour clarifier.\n\n"
            "[NOM ENTREPRISE]"
        ),
        "tip": "Inviter à vérifier le bon prestataire. Constat d'huissier + signalement Google si retrait demandé.",
        "antipattern": "Pas de ton sec ni accusateur. La confusion est probablement de bonne foi.",
        "delay": "48-72h",
        "seo": "-",
    },
    {
        "num": "30",
        "title": "Avis sur faits anciens (potentiellement prescrits)",
        "when": "Un avis qui revient sur un chantier vieux de plusieurs années.",
        "reply": (
            "Bonjour,\n\n"
            "Merci pour votre retour. L'intervention que vous évoquez remonte à plus de [X années]. Nous avons depuis fait évoluer nos pratiques et nos process.\n\n"
            "Pour qu'on regarde si nous pouvons encore vous aider, contactez-nous au [NUMERO].\n\n"
            "[PRENOM PATRON]"
        ),
        "tip": "Reconnaître l'évolution = signal aux prospects que vous écoutez. Ne pas évoquer la prescription en public.",
        "antipattern": "JAMAIS « c'est prescrit ». Mauvais signal commercial même si juridiquement correct.",
        "delay": "Sous 7 jours",
        "seo": "-",
    },
]

ALL_TEMPLATES = POSITIFS + NEGATIFS + DIFFAMATOIRES

# ===========================================================
# HTML GENERATION
# ===========================================================

CSS = """
/* ============================================
   CARNET PLEIN(R) BONUS #2 - PRINT STYLESHEET
   Designed for Chrome > Print > Save as PDF
   ============================================ */

@page {
  size: A4 portrait;
  margin: 20mm 16mm 22mm 16mm;
  @bottom-left {
    content: "Carnet Plein® by Mad Makers · Bonus #2 · Édition 2026";
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

/* ===== RESET & BASE ===== */
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

/* ===== PAGE FLOW ===== */
.page {
  page-break-after: always;
  break-after: page;
}
.page:last-of-type {
  page-break-after: auto;
}

/* ===== FULL-BLEED PAGES (cover, section-sep, cta-page) ===== */
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
  z-index: 0;
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
  font-size: 52pt;
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
  max-width: 155mm;
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

/* ===== CTA FINAL ===== */
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
  z-index: 0;
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
  width: 6px;
  height: 6px;
  background: #e0541b;
  flex-shrink: 0;
}

/* ===== INTRO PAGE ===== */
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
  border-left-color: #e0541b;
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
.callout p:last-child { margin-bottom: 0; }

/* ===== R.A.R.E. FRAMEWORK ===== */
.framework { margin-top: 6mm; }
.framework-row {
  display: grid;
  grid-template-columns: 28mm 1fr;
  gap: 6mm;
  padding: 5mm 0;
  border-bottom: 1px solid #d5d2c9;
  align-items: start;
  page-break-inside: avoid;
}
.framework-row:last-child { border-bottom: none; }
.framework-letter {
  font-family: 'Inter', sans-serif;
  font-size: 38pt;
  font-weight: 700;
  color: #e0541b;
  line-height: 0.85;
  letter-spacing: -0.04em;
}
.framework-step h4 {
  font-size: 12pt;
  margin-bottom: 2mm;
  line-height: 1.2;
}
.framework-step p {
  font-size: 10pt;
  color: #3a3d36;
  line-height: 1.55;
}

/* ===== MODEL PAGES (flow naturel, footer en bas du contenu) ===== */
.model {
  page-break-inside: avoid;
  page-break-after: always;
}

.model-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  border-bottom: 1px solid #d5d2c9;
  padding-bottom: 3mm;
  margin-bottom: 5mm;
  gap: 4mm;
}
.model-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10pt;
  color: #e0541b;
  font-weight: 600;
  letter-spacing: 0.08em;
  flex-shrink: 0;
}
.model-meta {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8pt;
  color: #5a5d56;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  text-align: right;
}
.model h2 {
  font-size: 20pt;
  line-height: 1.15;
  margin-bottom: 6mm;
  max-width: 165mm;
  font-weight: 600;
}

.model-block { margin-bottom: 5mm; }
.model-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8.5pt;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #e0541b;
  margin-bottom: 2mm;
  font-weight: 600;
}
.model-when {
  font-size: 10.5pt;
  color: #3a3d36;
  line-height: 1.5;
  font-style: italic;
}

.model-reply {
  background: #fafaf7;
  border: 1px solid #d5d2c9;
  border-left: 3px solid #e0541b;
  padding: 5mm 6mm;
  border-radius: 0 2mm 2mm 0;
  font-size: 10.5pt;
  line-height: 1.55;
  white-space: pre-wrap;
  color: #1a1c18;
}

.model-tip, .model-anti {
  display: grid;
  grid-template-columns: 6mm 1fr;
  gap: 3mm;
  padding: 3mm 0;
  border-top: 1px solid #ebe7dc;
}
.model-tip:first-of-type {
  border-top: none;
  padding-top: 4mm;
}
.icon {
  font-family: 'Inter', sans-serif;
  font-size: 13pt;
  font-weight: 700;
  line-height: 1.1;
  text-align: center;
}
.model-tip .icon { color: #2d9a5f; }
.model-anti .icon { color: #c43c2a; }

.tip-content .label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8pt;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #5a5d56;
  margin-bottom: 1mm;
  font-weight: 600;
}
.tip-content p {
  font-size: 10pt;
  line-height: 1.5;
  color: #1a1c18;
  margin: 0;
}

.model-footer {
  border-top: 1px solid #d5d2c9;
  padding-top: 3mm;
  margin-top: 5mm;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 4mm;
  font-family: 'JetBrains Mono', monospace;
  font-size: 7.5pt;
  color: #5a5d56;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
.model-footer .delay { color: #e0541b; font-weight: 600; }

/* ===== ANNEXES ===== */
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

/* ===== RECOURS TABLE ===== */
table.recours {
  width: 100%;
  border-collapse: collapse;
  margin: 5mm 0;
  font-size: 9pt;
  page-break-inside: avoid;
}
table.recours th {
  background: #0a0a0a;
  color: #fff;
  padding: 3mm;
  text-align: left;
  font-family: 'JetBrains Mono', monospace;
  font-size: 8pt;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 600;
}
table.recours td {
  padding: 3mm;
  border-bottom: 1px solid #d5d2c9;
  vertical-align: top;
  line-height: 1.4;
  font-size: 9pt;
}
table.recours tr:nth-child(even) td { background: #ebe7dc; }

/* ===== TEMPLATE LETTER (DSA / mise en demeure) ===== */
.template-letter {
  background: #fafaf7;
  border: 1px solid #d5d2c9;
  padding: 6mm;
  border-radius: 2mm;
  font-size: 8.5pt;
  line-height: 1.55;
  white-space: pre-wrap;
  margin: 4mm 0;
  font-family: 'Inter', sans-serif;
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

def render_template_page(t, section_label):
    """Render one model template as a full A4 page."""
    return f"""
<section class="page model">
  <div class="model-header">
    <span class="model-num">M{t['num']} / 30</span>
    <span class="model-meta">{section_label} · DÉLAI : {t['delay']}</span>
  </div>
  <h2>{t['title']}</h2>

  <div class="model-block">
    <div class="model-label">Quand l'utiliser</div>
    <p class="model-when">{t['when']}</p>
  </div>

  <div class="model-block">
    <div class="model-label">La réponse type</div>
    <div class="model-reply">{t['reply']}</div>
  </div>

  <div class="model-tip">
    <div class="icon">✓</div>
    <div class="tip-content">
      <div class="label">Conseil de personnalisation</div>
      <p>{t['tip']}</p>
    </div>
  </div>

  <div class="model-anti">
    <div class="icon">✕</div>
    <div class="tip-content">
      <div class="label">Anti-pattern</div>
      <p>{t['antipattern']}</p>
    </div>
  </div>

  <div class="model-footer">
    <span>Délai conseillé : <span class="delay">{t['delay']}</span></span>
    <span>RGPD : pas de nom complet, adresse, montant, téléphone du client</span>
  </div>
</section>
"""


def render_html():
    cover = """
<section class="bleed cover">
  <div class="cover-top">
    <span class="badge">Bonus #2 · Carnet Plein® by Mad Makers</span>
    <h1>30 Réponses<br>Prêtes à l'Emploi.</h1>
    <p class="sub">Le pack de modèles pour répondre à chaque avis Google en 2 minutes, sans piège juridique et sans langue de bois.</p>
  </div>
  <div class="cover-meta">
    <div>
      <div class="accent-line"></div>
      Édition 2026 · Mise à jour conforme DSA &amp; loi SREN
    </div>
    <div>pro.mad-makers.fr</div>
  </div>
</section>
"""

    intro = """
<section class="page intro">
  <div class="eyebrow">Pourquoi ce pack</div>
  <h1>97% des prospects lisent vos avis<br>avant de vous appeler.</h1>

  <p class="lead">Et 41% d'entre eux préfèrent une entreprise qui répond à <em>tous</em> ses avis - positifs comme négatifs - à une entreprise qui n'en répond à aucun (BrightLocal Local Consumer Review Survey, 2024-2026). Répondre n'est plus optionnel. C'est devenu le 2e facteur de classement dans le bloc local Google Maps après votre fiche elle-même.</p>

  <div class="callout">
    <h3>Les 4 règles d'or de la réponse aux avis</h3>
    <p><strong>1. Répondre à 100% des avis</strong> - positifs ET négatifs. Sélectionner est lu comme manipulation.</p>
    <p><strong>2. Délai : 48-72h, 7 jours grand maximum</strong> - 63% des consommateurs attendent une réponse dans cette fenêtre.</p>
    <p><strong>3. Longueur calibrée</strong> - 40-80 mots pour un positif, 70-150 pour un négatif. Au-delà : effet défensif.</p>
    <p><strong>4. Signer du prénom du dirigeant + nom entreprise</strong> - humanise, ancre la confiance dans l'artisanat local.</p>
  </div>

  <div class="callout dark">
    <h3>RGPD - Règle absolue, non négociable</h3>
    <p>Dans une réponse publique : <strong>aucun nom de famille du client, aucune adresse, aucun numéro de téléphone, aucun email, aucun montant facturé associé à son identité, aucune donnée de santé ou familiale.</strong> Risque : plainte CNIL, atteinte à la vie privée (art. 9 Code civil). Vous pouvez mentionner UNIQUEMENT le prénom (et seulement si le client a signé son avis avec).</p>
  </div>

  <h3 style="margin-top:8mm; font-size:14pt;">Comment utiliser ce pack</h3>
  <ol>
    <li>Repérez le type d'avis reçu (5★ enthousiaste, 4★ avec réserve, négatif justifié, faux/diffamatoire...)</li>
    <li>Trouvez le modèle correspondant dans le bon section (positifs M01-M10, négatifs M11-M22, faux M23-M30)</li>
    <li>Copiez la réponse, remplacez les [CHAMPS ENTRE CROCHETS] par vos infos réelles</li>
    <li>Relisez 10 secondes : aucune donnée perso du client ? Pas de promesse irréversible ? Publiez</li>
    <li>Pour les négatifs ou faux : conservez une trace écrite (capture) - délai prescription diffamation = 3 mois (loi 1881)</li>
  </ol>
</section>
"""

    framework = """
<section class="page">
  <div class="eyebrow">Le framework R.A.R.E.</div>
  <h1>Pour chaque avis négatif,<br>passez en mode R.A.R.E.</h1>

  <p class="lead">Quatre étapes simples qui transforment un avis négatif en signal de professionnalisme pour les futurs prospects qui le liront. C'est l'adaptation française du framework anglo-saxon LARC, validée par les cabinets d'e-réputation spécialisés.</p>

  <div class="framework">
    <div class="framework-row">
      <div class="framework-letter">R</div>
      <div class="framework-step">
        <h4>Remercier</h4>
        <p>« Merci pour ce retour. » Sec et brutal seul, mais c'est la base obligatoire. Vous reconnaissez que la personne s'est donnée la peine d'écrire. Sans remerciement, le ton est défensif d'emblée.</p>
      </div>
    </div>
    <div class="framework-row">
      <div class="framework-letter">A</div>
      <div class="framework-step">
        <h4>Assumer le RESSENTI, jamais la faute</h4>
        <p>« Je comprends que [le délai / le surcoût / la propreté] a posé problème. » Vous reconnaissez l'émotion du client SANS reconnaître une faute technique. La nuance est juridique : « Nous reconnaissons notre erreur » est un aveu opposable, « Je comprends votre déception » non.</p>
      </div>
    </div>
    <div class="framework-row">
      <div class="framework-letter">R</div>
      <div class="framework-step">
        <h4>Recadrer ou Proposer</h4>
        <p>Apportez le contexte factuel (« Les chantiers parfois se compliquent »), rappelez la garantie applicable, et surtout PROPOSEZ un échange privé : « Appelez-nous au [NUMERO] pour qu'on regarde ensemble. » Vous sortez du jugement public, vous entrez dans la résolution privée.</p>
      </div>
    </div>
    <div class="framework-row">
      <div class="framework-letter">E</div>
      <div class="framework-step">
        <h4>Échec → opportunité</h4>
        <p>Concluez sur une note constructive. Études BrightLocal : 33% des clients mécontents modifient leur avis ou en laissent un positif après une résolution empathique sous 7 jours. L'avis négatif d'aujourd'hui peut devenir le 5★ de demain.</p>
      </div>
    </div>
  </div>
</section>
"""

    section_a = """
<section class="bleed section-sep">
  <div class="label">- Section A · 10 modèles</div>
  <h2>Les avis positifs.</h2>
  <div class="count">M01 → M10</div>
  <p class="desc">Le piège classique sur les positifs : la réponse copier-coller détectable. Personnalisez systématiquement avec un détail repris de l'avis. Visez 2 à 4 phrases, 40-80 mots. Signez du prénom du dirigeant.</p>
</section>
"""

    section_b = """
<section class="bleed section-sep">
  <div class="label">- Section B · 12 modèles</div>
  <h2>Les avis mitigés<br>et négatifs légitimes.</h2>
  <div class="count">M11 → M22</div>
  <p class="desc">Appliquez R.A.R.E. systématiquement. Excuses du RESSENTI jamais de la faute. Basculez en privé dès la 2e ligne pour protéger juridiquement (aveu opposable) et émotionnellement le client.</p>
</section>
"""

    section_c = """
<section class="bleed section-sep">
  <div class="label">- Section C · 8 modèles</div>
  <h2>Les avis diffamatoires,<br>faux ou injurieux.</h2>
  <div class="count">M23 → M30</div>
  <p class="desc">Ici, votre réponse publique ne sert pas à convaincre l'auteur - elle sert à montrer aux <em>futurs prospects</em> qui liront que vous êtes professionnel, calme et factuel. Aucune contre-attaque. En parallèle : signalement Google + constat d'huissier dans les 3 mois (prescription loi 1881).</p>
</section>
"""

    annexe_garanties = """
<section class="page annexe">
  <div class="eyebrow">Annexe A · Garanties légales</div>
  <h1>Les 3 garanties qui<br>pèsent sur vos prestations.</h1>

  <p class="lead">À connaître pour répondre intelligemment à un avis sur un défaut post-intervention. Mentionner la garantie applicable rassure les futurs prospects ET donne un cadre clair au client mécontent.</p>

  <h3>1. Garantie de parfait achèvement (art. 1792-6 C. civ.)</h3>
  <p><strong>Durée : 1 an</strong> à compter de la réception des travaux. Couvre tous les désordres signalés par écrit, quelle que soit leur gravité.</p>

  <h3>2. Garantie biennale (art. 1792-3 C. civ.)</h3>
  <p><strong>Durée : 2 ans</strong>. Couvre les éléments d'équipement dissociables : radiateurs, robinetterie, ballon d'eau chaude, soudures, chauffe-eau, sanitaires.</p>

  <h3>3. Garantie décennale (art. 1792, loi Spinetta du 4 janvier 1978)</h3>
  <p><strong>Durée : 10 ans</strong>. Couvre les dommages affectant la solidité de l'ouvrage ou le rendant impropre à sa destination : canalisations encastrées, planchers chauffants, raccordement chaudière, PAC indissociable, climatisation gainée.</p>

  <div class="callout">
    <h3>Ce qu'il ne faut JAMAIS écrire en réponse publique</h3>
    <p>- « Nous reconnaissons que notre intervention a été mal effectuée »</p>
    <p>- « Notre technicien a commis une erreur »</p>
    <p>- « Nous prenons à notre charge les réparations »</p>
    <p>- « Vous avez raison, la pose n'était pas conforme »</p>
    <p><em>Toutes ces formulations sont des aveux opposables (art. 1383 C. civ.) qui peuvent entraîner la déchéance de votre garantie RC Pro et être utilisés contre vous en justice.</em></p>
  </div>

  <div class="callout dark">
    <h3>Formulations sécurisées</h3>
    <p>✓ « Nous prenons votre retour au sérieux et souhaitons en faire le point avec vous. »</p>
    <p>✓ « Sans préjuger des causes, nous mandatons un technicien pour expertiser. »</p>
    <p>✓ « Notre équipe SAV vous contacte sous 48h pour examiner le dossier. »</p>
    <p>✓ « Nous vous proposons un rendez-vous d'expertise gratuit. »</p>
  </div>
</section>
"""

    annexe_google = """
<section class="page annexe">
  <div class="eyebrow">Annexe B · Signalement Google</div>
  <h1>Comment signaler un avis<br>à Google en 7 étapes.</h1>

  <p class="lead">Quand un avis est manifestement faux, hors-sujet, injurieux ou émane d'un concurrent identifié, le signalement Google est la première démarche - gratuite, traitée en 3 à 10 jours. Voici la procédure officielle (Google Business Profile Help, 2026).</p>

  <ol>
    <li>Connectez-vous à votre compte Google professionnel propriétaire de la fiche.</li>
    <li>Tapez le nom de votre entreprise dans Google Search (ou ouvrez Google Maps).</li>
    <li>Le panneau de gestion s'affiche - allez dans l'onglet <strong>Avis</strong>.</li>
    <li>Cliquez sur les 3 points verticaux à droite de l'avis litigieux.</li>
    <li>Sélectionnez <strong>Signaler l'avis</strong>.</li>
    <li>Choisissez un motif valide parmi les 7 motifs acceptés par Google (voir ci-dessous).</li>
    <li>Envoyez et patientez 3-10 jours ouvrés. L'état s'affiche dans l'outil de gestion des avis.</li>
  </ol>

  <h3>Les 7 motifs acceptés par Google</h3>
  <ul>
    <li>Hors sujet (l'avis ne concerne pas votre entreprise réelle)</li>
    <li>Spam (avis dupliqué, généré automatiquement)</li>
    <li>Conflit d'intérêts (concurrent, ancien salarié, faux client)</li>
    <li>Langage offensant / contenu inapproprié</li>
    <li>Harcèlement / incitation à la haine</li>
    <li>Informations personnelles (le client a divulgué les siennes ou les vôtres)</li>
    <li>Contenu illégal</li>
  </ul>

  <div class="callout">
    <h3>Motifs systématiquement REFUSÉS par Google</h3>
    <p>Ne signalez pas un avis simplement parce qu'il est négatif ou que vous n'êtes pas d'accord. Google le rappelle : « Nous ne prenons pas parti en cas de conflit entre un établissement et un client. » Une notification abusive expose à 1 an d'emprisonnement et 15 000€ d'amende (LCEN art. 6-I-4).</p>
  </div>

  <h3>En cas de refus de Google</h3>
  <ol>
    <li>Recours interne (appel via l'outil de gestion des avis).</li>
    <li>Mise en demeure adressée à Google Ireland Limited (Google France n'est pas compétente, jurisprudence constante).</li>
    <li>Saisine du Tribunal judiciaire de Paris en procédure accélérée au fond (art. 6-3 LCEN) ou en référé.</li>
  </ol>
</section>
"""

    annexe_surveillance = """
<section class="page annexe">
  <div class="eyebrow">Annexe C · Surveillance hebdomadaire</div>
  <h1>Pourquoi vous DEVEZ vérifier<br>vos avis chaque lundi.</h1>

  <p class="lead">La diffamation et l'injure (loi du 29 juillet 1881) se prescrivent en <strong>3 mois</strong> à compter de la publication de l'avis - pas de sa découverte. Si vous découvrez un avis diffamatoire 4 mois après sa publication, vous avez perdu vos recours pénaux. Le screening hebdomadaire est non négociable.</p>

  <div class="callout dark">
    <h3>Le piège des 3 mois - confirmé par la jurisprudence</h3>
    <p>Cass. crim. 10 janvier 2023, n° 22-82.838 : le délai court à partir de la première publication, indépendamment de la date où le professionnel en prend connaissance. Pour interrompre la prescription, seuls les actes formels (citation directe, plainte avec constitution de partie civile) sont valables - et ils doivent qualifier précisément les faits sous peine de nullité.</p>
  </div>

  <h3>Check-list de surveillance hebdomadaire (15 min chaque lundi matin)</h3>
  <ol>
    <li>Ouvrez votre fiche Google Business Profile, onglet <strong>Avis</strong>.</li>
    <li>Filtrez par <strong>Plus récents</strong>. Repérez les nouveaux depuis la semaine dernière.</li>
    <li>Pour chaque nouvel avis : décidez du type (5★, 4★, 3★, 2★, 1★, faux/injuste).</li>
    <li>Sélectionnez le modèle correspondant dans ce pack. Personnalisez. Publiez sous 48-72h.</li>
    <li><strong>Pour tout avis suspect</strong> (faux, diffamatoire, injurieux) : <strong>capture d'écran datée immédiate</strong> avec URL visible. Stockez dans un dossier dédié.</li>
    <li>Si plusieurs avis suspects en cascade ou un seul gravement préjudiciable : prenez rendez-vous avec un avocat spécialisé sous <strong>30 jours</strong> grand maximum pour préserver le délai de 3 mois.</li>
  </ol>

  <h3>Le constat d'huissier - quand et combien</h3>
  <p>Si vous envisagez une procédure judiciaire (diffamation, dénigrement), un constat d'huissier sur l'avis litigieux est <strong>indispensable</strong> comme preuve. Coût : <strong>250 à 600€</strong>. Délai : immédiat (l'huissier intervient sous 48h). Validité juridique : opposable à Google et à l'auteur de l'avis.</p>
</section>
"""

    annexe_recours = """
<section class="page annexe">
  <div class="eyebrow">Annexe D · Recours juridiques</div>
  <h1>Coûts, délais et résultats<br>des procédures (2026).</h1>

  <p class="lead">Tableau de référence pour décider entre signalement Google gratuit, mise en demeure, procédure accélérée ou action au fond. Vérifié au regard du DSA (entrée en vigueur 17 février 2024) et de la loi SREN du 21 mai 2024 (nouvelle numérotation art. 6-3 LCEN).</p>

  <table class="recours">
    <thead>
      <tr>
        <th>Procédure</th>
        <th>Coût indicatif</th>
        <th>Délai</th>
        <th>Résultat possible</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Signalement Google direct</td>
        <td>Gratuit</td>
        <td>3-10 jours</td>
        <td>Retrait si motif valable</td>
      </tr>
      <tr>
        <td>Mise en demeure par avocat à l'auteur</td>
        <td>300-800€</td>
        <td>8-15 jours</td>
        <td>Retrait volontaire ~30% des cas</td>
      </tr>
      <tr>
        <td>Constat d'huissier internet</td>
        <td>250-600€</td>
        <td>Immédiat</td>
        <td>Preuve indispensable avant procédure</td>
      </tr>
      <tr>
        <td>Procédure accélérée au fond contre Google (art. 6-3 LCEN)</td>
        <td>1 500-5 000€</td>
        <td>1-3 mois</td>
        <td>Retrait sous astreinte si illicéité manifeste</td>
      </tr>
      <tr>
        <td>Levée d'anonymat (art. 145 CPC)</td>
        <td>1 500-3 000€</td>
        <td>1-2 mois</td>
        <td>Communication des données par Google</td>
      </tr>
      <tr>
        <td>Plainte diffamation (loi 1881)</td>
        <td>1 500-4 000€ ou aide juridictionnelle</td>
        <td>12-24 mois</td>
        <td>Amende ≤ 12 000€ + dommages-intérêts</td>
      </tr>
      <tr>
        <td>Action au fond dénigrement (art. 1240)</td>
        <td>3 000-15 000€</td>
        <td>12-24 mois</td>
        <td>Dommages-intérêts (3 000-20 000€)</td>
      </tr>
    </tbody>
  </table>

  <div class="callout">
    <h3>À retenir</h3>
    <p>La procédure accélérée au fond (art. 6-3 LCEN) ne permet PAS d'obtenir des dommages-intérêts - uniquement le retrait du contenu (rép. ministérielle JO 26 août 2025 + TJ Paris 10 oct. 2025). Pour l'indemnisation, action séparée nécessaire au fond sur fondement art. 1240 C. civ. ou loi 1881.</p>
  </div>
</section>
"""

    annexe_dsa = """
<section class="page annexe">
  <div class="eyebrow">Annexe E · Modèle de notification DSA</div>
  <h1>À adresser à Google Ireland<br>pour faire retirer un avis illicite.</h1>

  <p class="lead">À utiliser quand le signalement Google direct a échoué et avant d'engager une procédure judiciaire. Adresse : Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irlande. À envoyer par lettre recommandée avec accusé de réception.</p>

  <div class="template-letter">[Vos coordonnées complètes]
[Nom entreprise, SIRET, adresse, téléphone, email]

Le [date], à [ville]

Google Ireland Limited
Gordon House, Barrow Street
Dublin 4, Irlande

Objet : Notification de contenu illicite au sens du Règlement (UE) 2022/2065 (DSA) - Demande de retrait

Madame, Monsieur,

Je soussigné(e) [Prénom NOM], agissant en qualité de [gérant / dirigeant] de la société [NOM ENTREPRISE] (SIRET [numéro]), vous notifie par la présente, conformément à l'article 16 du Règlement européen sur les services numériques (DSA), un contenu manifestement illicite publié sur la fiche Google Business Profile de mon entreprise.

URL EXACTE DE L'AVIS LITIGIEUX :
[copier-coller URL complète, vérifiable par constat d'huissier joint]

TENEUR DU CONTENU :
[Retranscrire mot pour mot l'avis litigieux]

MOTIFS D'ILLICÉITÉ :
[Au choix : diffamation publique - loi 29 juillet 1881, art. 29 / Injure publique - art. 33 / Dénigrement - art. 1240 C. civ. / Atteinte à la vie privée - art. 9 C. civ. / Faux avis - art. L. 121-1 Code de la consommation]

JUSTIFICATIONS FACTUELLES :
[Démontrer en 5-10 lignes pourquoi le contenu est illicite : fait imputé faux et vérifiable, absence de bonne foi, intention de nuire, etc.]

PIÈCES JOINTES :
- Constat d'huissier du [date] établi par Maître [Nom], huissier de justice à [ville]
- Copie de la mise en demeure préalable adressée à l'auteur le [date] (si identifié)
- [Autres pièces probantes]

DÉCLARATION DE BONNE FOI :
Je certifie sur l'honneur que les informations fournies dans la présente notification sont exactes et complètes, et qu'elles sont communiquées de bonne foi conformément à l'article 16 §2 d) du DSA. Je suis informé(e) qu'une notification abusive m'expose aux sanctions prévues à l'article 6-I-4 de la LCEN (1 an d'emprisonnement, 15 000€ d'amende).

Je vous demande de procéder au retrait du contenu litigieux dans le délai prévu par l'article 16 §6 du DSA et de m'en accuser réception.

Je me réserve le droit, à défaut de retrait dans un délai de [10 jours], de saisir le Tribunal judiciaire de Paris en procédure accélérée au fond (art. 6-3 LCEN) à vos frais exclusifs.

Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

[Signature manuscrite]
[Prénom NOM]
[Qualité]</div>
</section>
"""

    annexe_mise_en_demeure = """
<section class="page annexe">
  <div class="eyebrow">Annexe F · Mise en demeure à l'auteur</div>
  <h1>À adresser à l'auteur identifié<br>d'un avis diffamatoire.</h1>

  <p class="lead">À utiliser quand vous connaissez l'identité de l'auteur (avis signé, levée d'anonymat préalable, ou auteur évident par le contenu). Effet psychologique fort - dans 30% des cas, l'avis est retiré volontairement. À envoyer par lettre recommandée AR.</p>

  <div class="template-letter">[Vos coordonnées complètes]

Lettre recommandée avec accusé de réception

[Date]
[Prénom NOM auteur]
[Adresse complète]

Objet : Mise en demeure de retrait d'un avis Google publié à mon encontre

Madame, Monsieur,

Le [date de publication], vous avez publié sur la fiche Google Business Profile de mon entreprise [NOM ENTREPRISE] (URL : [copier-coller]) un avis comportant les propos suivants :

[Citer mot pour mot l'avis, entre guillemets]

Ces propos sont manifestement [au choix : diffamatoires au sens de l'article 29 de la loi du 29 juillet 1881 / injurieux au sens de l'article 29 al. 2 de la même loi / constitutifs d'un dénigrement au sens de l'article 1240 du Code civil] dans la mesure où :

[Démontrer factuellement en 3-5 points :
- les faits imputés sont faux (preuves à l'appui)
- l'absence de toute base factuelle
- l'intention manifeste de nuire (le cas échéant)]

Je vous mets donc en demeure, par la présente, de :

1. Procéder au retrait immédiat de l'avis litigieux dans un délai maximal de SEPT (7) jours à compter de la réception de la présente.

2. À défaut, j'engagerai à votre encontre, sans nouvelle mise en demeure, toute action utile devant les juridictions compétentes, qui pourra notamment aboutir à :

- une condamnation pénale au titre de l'article [29 ou 33] de la loi du 29 juillet 1881 (amende jusqu'à 12 000 €) ;
- une condamnation civile au titre de l'article 1240 du Code civil (dommages-intérêts).

3. Je conserve par-devers moi le constat d'huissier établi par Maître [Nom] le [date] qui constitue une preuve irréfutable de votre publication, opposable en justice.

Le délai de prescription de trois mois prévu par l'article 65 de la loi de 1881 sera, le cas échéant, interrompu par les actes appropriés.

Je vous saurais gré de bien vouloir prendre les mesures qui s'imposent dans le délai imparti, et reste à votre disposition pour tout échange constructif avant cette échéance.

Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

[Signature]
[Prénom NOM]
[Qualité - dirigeant de NOM ENTREPRISE]

Pièces jointes :
- Constat d'huissier daté du [date]
- Copie de la fiche Google Business Profile</div>
</section>
"""

    cta = """
<section class="bleed cta-page">
  <div class="eyebrow">- Aller plus loin</div>
  <h2>Ces 30 modèles, on les applique chez chaque artisan signé.</h2>
  <p>Plus le système d'avis automatisé qui demande l'avis au bon moment après chaque chantier (SMS personnalisé + QR code sur facture), le monitoring hebdomadaire de votre fiche Google et le reporting mensuel.</p>
  <p>Vous gardez le savoir-faire métier. On gère le digital.</p>
  <a href="https://pro.mad-makers.fr" class="button">Audit gratuit 20 min → pro.mad-makers.fr</a>
</section>
"""

    sources = """
<section class="page sources">
  <div class="eyebrow">Sources principales</div>
  <h1>Les références derrière<br>les chiffres et le cadre.</h1>

  <ul>
    <li><strong>Législation et jurisprudence française :</strong> Code civil (art. 1240, 1792, 1792-3, 1792-6, 9, 12, 1383) · Loi du 29 juillet 1881 (art. 29, 32, 33, 65) · LCEN (art. 6-3, 6-4, 6-I-4) · Loi SREN n° 2024-449 du 21 mai 2024 · Décret n° 2007-1527 du 24 octobre 2007 (droit de réponse)</li>
    <li><strong>Droit européen :</strong> Règlement (UE) 2016/679 (RGPD) · Règlement (UE) 2022/2065 (DSA) - entré en vigueur 17 février 2024</li>
    <li><strong>Jurisprudence récente :</strong> Cass. crim. 10 janvier 2023, n° 22-82.838 · TJ Paris 22 juin 2022 (Raimondi) · TJ Paris 10 octobre 2025 · CA Chambéry 22 mai 2025 · Réponse ministérielle JO 26 août 2025</li>
    <li><strong>Position CNIL :</strong> « Avis et notations en ligne : quels sont les droits des professionnels ? » (cnil.fr)</li>
    <li><strong>Études consommateurs :</strong> BrightLocal Local Consumer Review Survey 2024, 2025, 2026 · Whitespark Local Search Ranking Factors 2024, 2026 · ReviewTrackers · GatherUp · Bazaarvoice · Sitejabber</li>
    <li><strong>Google Business Profile :</strong> Documentation officielle support.google.com/business · Politique des avis Google</li>
    <li><strong>Cabinets juridiques spécialisés :</strong> Haas Avocats · Bem Avocats · Cahen Avocats · Pechenard Avocats · ACI Avocats · Solvoxia Avocats · Bauer Avocats · ACD Avocats · Village-Justice · Dalloz Étudiant</li>
    <li><strong>Secteur artisanal :</strong> CAPEB · FFB · DGCCRF · SignalConso · 60 Millions de consommateurs · UFC-Que Choisir · Qualit'EnR · Anah (MaPrimeRénov') · economie.gouv.fr</li>
  </ul>

  <div class="disclaimer">
    Document à usage interne du client. Édition 2026. Mise à jour conforme DSA et loi SREN. Les statistiques BrightLocal portent essentiellement sur un panel américain (transposition à la France légitime mais à préciser). Aucun document de ce type ne dispense d'une lecture humaine attentive de chaque avis avant publication d'une réponse. En cas de doute juridique sur un cas particulier, consulter un avocat spécialisé en e-réputation. Pour toute mise à jour annuelle de ce pack, contactez Mad Makers.
  </div>
</section>
"""

    template_pages = ""
    for t in POSITIFS:
        template_pages += render_template_page(t, "Avis positifs")
    template_pages += section_b
    for t in NEGATIFS:
        template_pages += render_template_page(t, "Négatifs légitimes")
    template_pages += section_c
    for t in DIFFAMATOIRES:
        template_pages += render_template_page(t, "Faux / diffamatoires")

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>30 Réponses Prêtes à l'Emploi - Carnet Plein® by Mad Makers</title>
<link rel="preconnect" href="https://fonts.bunny.net" crossorigin>
<link rel="stylesheet" href="https://fonts.bunny.net/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap">
<style>{CSS}</style>
</head>
<body>

{cover}

{intro}

{framework}

{section_a}

{template_pages}

{annexe_garanties}

{annexe_google}

{annexe_surveillance}

{annexe_recours}

{annexe_dsa}

{annexe_mise_en_demeure}

{cta}

{sources}

</body>
</html>
"""
    return html


if __name__ == "__main__":
    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "02-30-reponses-avis-google.html"
    )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(render_html())
    size_kb = os.path.getsize(out_path) / 1024
    print(f"OK - HTML écrit : {out_path}")
    print(f"     Taille : {size_kb:.1f} Ko")
    print(f"     Pages estimées : ~45 (30 templates + 7 sections + 6 annexes + cover + sources)")
    print()
    print("PROCHAINE ETAPE :")
    print("  1. Ouvrir le .html dans Chrome")
    print("  2. Ctrl+P (Imprimer)")
    print("  3. Destination : 'Enregistrer en PDF'")
    print("  4. Plus de parametres -> Marges : Aucune")
    print("  5. Cocher 'Graphiques d'arriere-plan'")
    print("  6. Enregistrer")
