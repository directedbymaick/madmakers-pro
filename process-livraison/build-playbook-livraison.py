#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script - Playbook de livraison interne Mad Makers
"L'Accelerateur Carnet Plein(R)" - operations doc J0 a J+14 + rythme M+1 a M+12

Operateur : Rayan Mpondo (Maick). Structure legale : EI Sara Cankaya.
Solo. Max 3 clients en parallele (cohort).

Generates playbook-livraison-carnet-plein.html in this folder.
Open in Chrome -> File > Print > Save as PDF (A4 portrait).
"""
import os

# ===========================================================
# DATA - TIMELINE J0 a J+14
# ===========================================================

TIMELINE_PRE_SIGN = [
    ("D-7", "Appel découverte (Calendly)",
     "Audit gratuit 20 minutes en visio. Comprendre marché local, métier, objectifs. Pas de pitch, juste écoute + diagnostic rapide. Si fit : annoncer devis + contrat sous 72h."),
    ("D-3", "Envoi devis + contrat + questionnaire pré-kick-off",
     "Email : devis chiffré, convention de prestation (PDF), questionnaire pré-kick-off (Notion ou Tally), 3 références de chantiers similaires. Délai de signature : 7 jours max."),
    ("D0", "Signature contrat + paiement setup",
     "Signature électronique (Yousign). Paiement setup 5 000 € HT (ou 1ère échéance si 3×). Email automatique de bienvenue déclenché."),
]

TIMELINE_J0_J14 = [
    ("J+1", "Email bienvenue + accès partagé Notion",
     "Envoi email bienvenue (template 02). Création espace Notion partagé avec le client (brief, action items, photos). Renvoi du questionnaire pré-kick-off à remplir avant J+5."),
    ("J+1 à J+5", "Récupération accès comptes existants",
     "Demander accès admin secondaire : Google Business Profile, registrar nom de domaine, hébergeur (si site existant), compte WhatsApp Business (création si pas existant). Documenter dans Notion."),
    ("J+5", "Réception du questionnaire pré-kick-off complété",
     "Questionnaire client rempli : positionnement, marché local, concurrence vue, contenus disponibles (logos, photos, références chantiers, certifications)."),
    ("J+7 matin", "Kick-off groupé cohort visio 60 minutes",
     "Visio Zoom à 4 (les 3 nouveaux artisans + toi). Tour de table 15 min (chaque artisan se présente : métier, zone, objectif), présentation du programme et calendrier 20 min, calage du KPI commun de cohort 15 min, Q&A 10 min. Création du WhatsApp group de cohort à l'issue."),
    ("J+7 après-midi", "3 visios 1:1 individuelles de 30 min chacune",
     "Visios séparées avec chaque artisan : validation du KPI individuel détaillé (annexe 1 du contrat), planning détaillé J+8 à J+14, accès comptes finalisés."),
    ("J+7 soir", "Briefs écrits envoyés + annexes 1 signées",
     "Compte-rendu du kick-off groupé envoyé dans le WhatsApp group. Brief individuel + annexe 1 (KPI) signés électroniquement avec chaque artisan. Action items dans Notion partagé client."),
    ("J+8", "Démarrage site web",
     "Setup repo GitHub à partir du template Mad Makers Pro. Branche par client. Préparation des assets : logos, photos hero, palette si différente du défaut."),
    ("J+8 à J+10", "Audit + optimisation GBP",
     "Audit 12 points (cf Bonus #1). Correction catégories, attributs, zones desservies, horaires, photos. Upload des 10 premières photos catégorisées. Premier Google Post de bienvenue programmé."),
    ("J+9 à J+11", "Customisation site web",
     "Adaptation copy (sections : qui, services, zone, avis, contact). Intégration logos et photos. Tests responsive (mobile/tablette/desktop). Lighthouse mobile ≥ 90."),
    ("J+10 à J+12", "Mise en place système avis",
     "Récupération lien d'avis Google personnalisé (g.page/r/...). Création du flow SMS post-chantier (Twilio ou Brevo). Test sur 1 numéro réel. Réponses pré-rédigées 5★ à 1★ en place (cf Bonus #2)."),
    ("J+11", "Lancement collecte photos chantiers",
     "Setup WhatsApp Business avec numéro dédié. Briefing client sur les 5 règles photo (cf Bonus #3) : lumière naturelle, cadre serré, avant/après, plan large + détail, paysage. Premier envoi test."),
    ("J+13", "Validation site avec client (visio 30 min)",
     "Démo du site sur URL temporaire (preview Vercel). Récupération des corrections. Validation finale par email + dans Notion."),
    ("J+14", "GO LIVE - mise en service complète",
     "Déploiement sur le domaine final (DNS). Site en production. GBP opérationnel. Avis système actif. Photos chantiers en cours. Premier Google Post hebdo. Email client : bundle livré."),
]

# ===========================================================
# DATA - COMPOSANTS DEEP DIVE (6 composants)
# ===========================================================

COMPOSANTS_DETAIL = [
    {
        "num": "01",
        "nom": "Site web professionnel",
        "stack": [
            "Hébergement : Vercel (UE, RGPD-compliant)",
            "Médias lourds : Cloudflare R2 (vidéos hero, photos brutes)",
            "CDN : intégré Vercel + Cloudflare R2",
            "Fonts : Bunny Fonts (Geist) ou typo brand client",
            "Versioning : GitHub (1 repo par client, branche main = prod)",
            "DNS : cible cname.vercel-dns.com",
        ],
        "phases": [
            ("Phase 1 - Récup contenus (J+1 à J+5)", "Logos, photos initiales, copy validée client, références à mettre en avant, certifications, marques partenaires."),
            ("Phase 2 - Setup repo + template (J+8)", "Fork du template Mad Makers Pro vers repo dédié client. Adaptation palette, typo, sections. Branch main = prod."),
            ("Phase 3 - Customisation (J+9 à J+11)", "Sections : hero, services, zone géographique, expérience, photos chantiers, avis, contact, mentions légales. Inclusion schema.org local business."),
            ("Phase 4 - Quality gates (J+11)", "Lighthouse mobile ≥ 90 sur perf et accessibilité. Tests browser : Chrome / Safari iOS / Firefox / Edge. axe DevTools 0 erreur critique. Vérification mentions légales conformes (RGS, RGPD, médiateur conso)."),
            ("Phase 5 - Validation client (J+13)", "Démo URL preview Vercel. Récup corrections par email ou Notion. Itération si besoin sous 24h."),
            ("Phase 6 - Mise en live (J+14)", "Config DNS chez registrar du client. Propagation 24h max. Surveillance status.vercel.com pendant 48h."),
        ],
        "quality_gates": [
            "Lighthouse mobile : Performance ≥ 90, Accessibilité ≥ 95, SEO ≥ 95, Best Practices ≥ 95",
            "Aucune erreur dans la console navigateur",
            "Tests effectués sur iOS Safari + Android Chrome (devices réels ou BrowserStack)",
            "Mentions légales complètes : SIRET, RCS, TVA, assurance décennale, médiateur conso",
            "Schema.org LocalBusiness avec NAP (Name, Address, Phone) cohérent avec GBP",
            "Favicon, OG image, meta description renseignés",
            "Formulaire de contact testé : envoi reçu + accusé client",
        ],
        "tools": "Vercel CLI, GitHub Desktop, VS Code, Lighthouse, axe DevTools, BrowserStack (optionnel)",
        "erreurs": [
            "Oublier le NAP cohérent entre site et GBP : Google considère 2 entités différentes, dilue le ranking",
            "Pousser sans tester sur iOS Safari : 30% des artisans clients ouvrent depuis iPhone",
            "Ne pas activer le HTTPS forcé sur Vercel (auto désormais, mais à vérifier)",
        ],
    },
    {
        "num": "02",
        "nom": "Google Business Profile",
        "stack": [
            "Compte Google admin secondaire (jamais propriétaire principal)",
            "App mobile GBP iOS / Android pour réponses rapides",
            "Whitespark Local Citation Finder (audit annuaires - optionnel)",
            "Spreadsheet de suivi mensuel des métriques (Google Sheets)",
        ],
        "phases": [
            ("Phase 1 - Audit 12 points (J+8)", "Suivre la checklist du Bonus #1. Identifier ce qui manque ou est mal renseigné. Documenter dans Notion."),
            ("Phase 2 - Corrections (J+8 à J+10)", "Catégorie principale + secondaires, description longue (750 caractères max optimisés mots-clés métier+ville), attributs RGE et certifications, zones desservies (villes ou rayon)."),
            ("Phase 3 - Photos catégorisées (J+9)", "Upload minimum 10 photos à T0, catégorisées : équipe, identité, intérieur (atelier), à l'extérieur (chantiers), produits, vidéo véhicule. Suivre règles Bonus #3."),
            ("Phase 4 - Premier Google Post (J+10)", "Post de bienvenue avec photo véhicule logoté + brève présentation. Programme un Post hebdomadaire à partir de J+14."),
            ("Phase 5 - Messagerie GBP (J+11)", "Activation messagerie GBP si le client est OK pour recevoir des messages directs. Configurer auto-réponse hors horaires."),
        ],
        "quality_gates": [
            "100% des 12 points du Bonus #1 cochés",
            "Au moins 10 photos uploadées et catégorisées",
            "Description longue sans bourrage de mots-clés (lisible humain)",
            "Horaires d'ouverture renseignés + horaires spéciaux (jours fériés)",
            "Zones desservies cohérentes avec la zone réelle d'intervention",
            "NAP identique au site et aux annuaires existants",
            "Premier Google Post publié",
        ],
        "tools": "Google Business Profile web + mobile, Whitespark, Google Sheets pour suivi mensuel",
        "erreurs": [
            "Lister plus de zones desservies que la zone réelle : risque suspension Google",
            "Mettre une catégorie primaire trop générique (ex 'Entrepreneur') au lieu de précise (ex 'Plombier')",
            "Oublier de répondre aux avis dans les 48h : signal négatif pour le ranking local",
        ],
    },
    {
        "num": "03",
        "nom": "Système d'avis Google automatisé",
        "stack": [
            "Lien d'avis Google personnalisé (forme g.page/r/...)",
            "Envoi SMS : Twilio (international) ou Brevo (FR, plus simple)",
            "Envoi email : Resend ou Brevo",
            "Templates de réponses pré-rédigés (cf Bonus #2 : 30 réponses)",
            "Déclencheur : déclaratif client (formulaire interne) OU intégration CRM s'il en a",
        ],
        "phases": [
            ("Phase 1 - Récupération du lien d'avis (J+10)", "Sur GBP, section Avis → bouton Demander des avis → copier le lien court. Format : g.page/r/[ID]/review"),
            ("Phase 2 - Templates SMS et email (J+10)", "SMS court (160 caractères max) : 'Bonjour [PRENOM], merci de nous avoir confié votre chantier. Votre retour compte beaucoup : [LIEN_AVIS] - [NOM_ARTISAN]'. Email plus long avec photo avant/après."),
            ("Phase 3 - Process de déclenchement (J+11)", "Définir avec le client : il déclenche manuellement (form Tally / Notion) en fin de chantier, ou intégration CRM existant (Tactidevis, Obat). Si manuel : créer raccourci écran d'accueil iPhone."),
            ("Phase 4 - 5 réponses templates en place (J+12)", "Pré-rédiger dans un Google Docs partagé : réponse 5★ chaleureuse, 4★ remerciante, 3★ honnête, 2★ amende honorable, 1★ professionnelle. Personnaliser au métier."),
            ("Phase 5 - Test sur 1 envoi réel (J+13)", "Envoi test sur le numéro de l'artisan lui-même pour vérifier que le SMS arrive, le lien fonctionne, le formulaire Google s'ouvre proprement."),
        ],
        "quality_gates": [
            "Lien d'avis testé sur 3 navigateurs (Chrome, Safari, Firefox)",
            "SMS test reçu en moins de 30 secondes",
            "5 réponses templates rédigées (5★ à 1★)",
            "Process de déclenchement compris et acté par le client",
            "Backup : procédure manuelle écrite si automation tombe",
        ],
        "tools": "GBP, Brevo (FR), Twilio (alternatif), Google Docs pour templates",
        "erreurs": [
            "Acheter des avis ou inciter avec une contrepartie : sanction Google immédiate + risque pénal",
            "Envoyer le SMS trop tôt (chantier non fini) : réception négative client",
            "Ne pas répondre aux avis 1★ par réflexe : aggrave la perception. Toujours répondre, posément, sous 48h",
        ],
    },
    {
        "num": "04",
        "nom": "Reporting mensuel",
        "stack": [
            "Template PDF : Python + HTML/CSS (même framework que les bonus)",
            "Données : GBP Insights (manuel ou API), GA4 si présent, suivi Sheets avis",
            "Envoi : email à J+5 du mois pour le mois précédent",
            "Stockage : Notion partagé client + archive locale",
        ],
        "phases": [
            ("Phase 1 - Collecte des données (1er du mois)", "Aller chercher dans GBP Insights : impressions sur recherche, vues, appels, demandes d'itinéraire, photos vues, mots-clés de découverte. Idem GA4 si installé."),
            ("Phase 2 - Calcul des deltas (2-3 du mois)", "Comparer aux 3 derniers mois. Identifier tendances. Mettre en exergue 1 ou 2 chiffres saillants."),
            ("Phase 3 - Rédaction (3-4 du mois)", "Synthèse exécutive 1 page + métriques détaillées + actions menées (Google Posts, photos, avis traités) + recommandations mois en cours."),
            ("Phase 4 - Envoi (5 du mois)", "Email + PDF joint + lien Notion. Demander un retour rapide (5 min) en visio si points à creuser."),
        ],
        "quality_gates": [
            "Envoi avant le 5 du mois à minuit, sans exception (sauf force majeure documentée)",
            "Recoupement de 2 sources si possible (GBP + GA4) pour fiabiliser les chiffres",
            "Pas de chiffres inventés ou estimés sans le préciser explicitement",
            "Sections constantes mois après mois (le client doit pouvoir comparer M-1 / M-2)",
        ],
        "tools": "GBP Insights, GA4, Python script de génération PDF, Notion",
        "erreurs": [
            "Sauter un mois ou envoyer en retard : casse la confiance immédiatement",
            "Trop de chiffres sans interprétation : reporting illisible",
            "Ne pas mentionner les baisses ou les semaines creuses : suspect, perte de confiance",
        ],
    },
    {
        "num": "05",
        "nom": "Gestion des photos chantiers",
        "stack": [
            "WhatsApp Business avec numéro dédié (réception)",
            "Snapseed iOS/Android pour retouche légère 30s par photo",
            "Google Photos pour Gomme Magique (flouter visages, plaques)",
            "GBP web pour upload + catégorisation",
            "Notion partagé pour archivage par chantier",
        ],
        "phases": [
            ("Phase 1 - Briefing client (J+11)", "Expliquer les 5 règles photo (Bonus #3). Setup WhatsApp Business. Rythme attendu : 2-3 photos par chantier (avant/après) chaque semaine."),
            ("Phase 2 - Réception hebdo", "Tous les lundis : check WhatsApp Business. Trier les photos par chantier dans Notion. Identifier les meilleures."),
            ("Phase 3 - Retouche (lundi soir)", "Snapseed 4 étapes (recadrer, exposition, healing, exporter). 30 secondes par photo. Gomme Magique Google Photos pour visages/plaques."),
            ("Phase 4 - Upload GBP + site (mardi)", "Upload 2-3 photos sur GBP avec catégorisation. Upload aussi sur le site dans la galerie photo si présente."),
            ("Phase 5 - Google Post hebdo avant/après (mardi)", "Créer 1 Google Post avec 1 paire avant/après + 50 à 100 mots de légende."),
        ],
        "quality_gates": [
            "Au moins 2 nouvelles photos uploadées sur GBP par semaine",
            "Droit à l'image respecté : visages floutés, plaques masquées, courriers non visibles, autocollants concurrents masqués",
            "1 Google Post hebdo publié (vendredi max)",
            "Photos catégorisées correctement sur GBP (équipe, intérieur, extérieur, identité, produits)",
        ],
        "tools": "WhatsApp Business, Snapseed, Google Photos, GBP web",
        "erreurs": [
            "Publier une photo avec visage de tiers identifiable sans accord : article 226-1 Code pénal, jusqu'à 45 000 € d'amende",
            "Photos floues ou mal exposées passées en production : nuit à la crédibilité",
            "Trop de photos uploadées en une fois (50 d'un coup puis rien pendant 3 mois) : signal négatif Google",
        ],
    },
    {
        "num": "06",
        "nom": "Accompagnement et coaching (1:1 + cohort)",
        "stack": [
            "Zoom ou Google Meet pour visio mensuelle individuelle ET pour la visio cohort groupée",
            "Calendly avec créneau récurrent réservé par client (1:1) + créneau cohort fixe (1er mardi du mois 18h par exemple)",
            "WhatsApp group privé : 1 par cohort (3 artisans + Rayan)",
            "Notion pour ordre du jour, notes, action items individuels ET notes cohort",
            "Email pour synthèse écrite post-visio",
        ],
        "phases": [
            ("Phase 1 - Kick-off groupé (1er lundi du mois, 60 min)", "Visio Zoom avec les 3 nouveaux artisans de la cohort. Tour de table 15 min (chaque artisan présente métier/zone/objectif en 5 min), présentation du programme et calendrier collectif 20 min, calage du KPI commun de cohort 15 min, Q&A 10 min. Création du WhatsApp group à l'issue."),
            ("Phase 2 - Visio individuelle mensuelle (45 min, mid-month)", "Visio 1:1 avec chaque client : tour de table 10 min, revue KPI 10 min, sujets prioritaires 20 min, action items 5 min. Notes Notion en live."),
            ("Phase 3 - Visio cohort mensuelle (45 min, 1er mardi 18h par défaut)", "Visio à 4 (les 3 cohort members + Rayan). Tour de table wins du mois 15 min (5 min par artisan), tour de table blocages 15 min, conseil croisé entre pairs 10 min, annonces communes 5 min. Animation par Rayan, rôle de facilitateur."),
            ("Phase 4 - Animation WhatsApp group (continu, light)", "Modération légère : 1 check le matin, 1 check le soir. Animation par 1 message-clé par semaine (lundi : 'Wins de la semaine ?'). Pas de disponibilité 24/7 promise."),
            ("Phase 5 - Synthèse écrite (J+1 après chaque visio)", "Compte-rendu par email + Notion. Action items numérotés avec responsable et date. Pour la visio cohort : synthèse partagée dans le WhatsApp group."),
        ],
        "quality_gates": [
            "Kick-off groupé tenu le 1er lundi du mois du démarrage, sans exception",
            "Visio cohort mensuelle tenue chaque mois, jamais annulée même si 1 absent",
            "Visios 1:1 mensuelles tenues sans exception",
            "Compte-rendu envoyé sous 24h après chaque visio",
            "WhatsApp group cohort actif (au moins 1 message animation par semaine)",
            "Règle Chatham House rappelée verbalement au kick-off (ce qui se dit dans la cohort reste dans la cohort)",
        ],
        "tools": "Zoom ou Google Meet, Calendly, WhatsApp group, Notion, email",
        "erreurs": [
            "Annuler la visio cohort si 1 ou 2 absents : casse le rituel, garde-la même à 2 ou même à 1",
            "Laisser le WhatsApp group mourir : si pas de message en 7 jours, déclencher avec une question, un partage de win, ou une ressource",
            "Mélanger les sujets individuels et cohort dans la même visio : les garder bien séparés",
            "Permettre à un membre toxique de polluer la cohort : recadrer en 1:1 d'abord, exclure du dispositif cohort si récidive (cf article 03 du contrat)",
            "Mettre 3 plombiers de la même ville dans une cohort : risque concurrence directe, choisir mix métiers + mix régions",
        ],
    },
]

# ===========================================================
# DATA - RYTHME MENSUEL M+1 a M+12
# ===========================================================

RYTHME_HEBDO = [
    ("Lundi", "Photos chantiers : tri + retouche + upload GBP. Google Post hebdo programmé (mardi). Message WhatsApp cohort « wins de la semaine ? » par cohort active (1 par cohort)."),
    ("Mardi", "Publication Google Post. Check GBP Insights (vue rapide). Réponses aux avis reçus week-end."),
    ("Mercredi", "Créneau libre : modifications site mineures, urgences clients, tâches imprévues."),
    ("Jeudi", "Visio coaching mensuelle individuelle (si dans le mois). Prep reporting (si fin de mois)."),
    ("Vendredi", "Sync clients : email récap semaine (3 lignes max). Check facturation. Modération légère WhatsApp cohort."),
]

RYTHME_MENSUEL = [
    ("1er lundi du mois", "Kick-off groupé visio 60 min avec les 3 nouveaux artisans de la cohort (si nouvelle cohort démarre ce mois). Création WhatsApp group cohort."),
    ("1er mardi du mois 18h", "Visio cohort mensuelle 45 min : pour chaque cohort active, réunion des 3 artisans + toi. Animation par toi (rôle facilitateur)."),
    ("1er du mois", "Collecte métriques GBP + GA4 du mois précédent. Sauvegarde dans Sheets de suivi."),
    ("3-4 du mois", "Rédaction reporting mensuel par client. Charte Carnet Plein®. 4-6 pages PDF."),
    ("5 du mois", "Envoi des reporting mensuels (email + PDF). Avant minuit, sans exception."),
    ("15 du mois", "Visio mensuelle individuelle 1:1 avec chaque client (45 min). Compte-rendu sous 24h."),
    ("20 du mois", "Audit interne : KPI internes Mad Makers. Heures travaillées par client. Marge effective."),
    ("Dernier vendredi", "Anticipation mois suivant : check Stripe pour prélèvements, prévision charge, anticipation congés."),
]

RYTHME_TRIMESTRIEL = [
    ("Trimestre", "Revue stratégique étendue avec chaque client (1h30 visio). Bilan KPI cumulés. Ajustements priorités."),
    ("Trimestre", "Sondage NPS auprès de chaque client (3 questions max)."),
    ("Trimestre", "Bilan financier interne : CA, marges, dépenses, charge prévue."),
]

# ===========================================================
# DATA - PROCEDURES DE RECUPERATION
# ===========================================================

INCIDENTS = [
    {
        "nom": "Client ne fournit pas les photos sous 72h",
        "symptome": "WhatsApp Business vide en milieu de semaine. Le client n'a rien envoyé.",
        "procedure": [
            "J+1 : SMS de rappel léger 'Hello [PRENOM], pas de photo cette semaine ? Pas grave, mais le rituel marche mieux avec 2-3 par chantier. À ce soir si t'as quelque chose.'",
            "J+3 : email plus structuré rappelant le levier de visibilité et l'engagement contractuel article 07",
            "Si 3 occurrences dans le mois : sujet explicite à la visio mensuelle, documenté dans Notion, escalade verbale écrite",
            "Si 6 occurrences dans le trimestre : courrier RAR rappel article 07 + article 08 (la garantie de continuité gratuite peut être écartée si le Client ne tient pas ses engagements)",
        ],
    },
    {
        "nom": "Client ne répond pas aux demandes de devis sous 24h",
        "symptome": "Demandes de devis générées par le site sans réponse documentée du client.",
        "procedure": [
            "Sur le formulaire de contact, ajouter un accusé de réception automatique pour le prospect (geste de réciprocité)",
            "Setup un email de notification au client à chaque demande, avec mention 'Délai contractuel : 24h'",
            "Si 3 demandes non répondues dans le mois : alerte rouge dans le reporting + escalade visio mensuelle",
            "Documenter dans Notion. Cela peut affecter la garantie de continuité gratuite (article 08).",
        ],
    },
    {
        "nom": "Site Vercel down ou ralentissement majeur",
        "symptome": "Site inaccessible ou très lent. Alerte d'un monitoring tiers (Better Uptime) ou remontée client.",
        "procedure": [
            "Check immédiat status.vercel.com",
            "Si problème Vercel global : attendre, communiquer au client, mettre la page d'attente Vercel par défaut",
            "Si problème spécifique au repo client : redeploy depuis le local en backup",
            "Médias hébergés sur Cloudflare R2 : continuent à fonctionner indépendamment",
            "Communication client : SMS dans les 15 minutes 'Incident technique en cours, je gère, retour à la normale sous Xh'",
            "Post-mortem écrit sous 48h dans Notion partagé client",
        ],
    },
    {
        "nom": "GBP suspension ou contestation",
        "symptome": "Fiche désactivée par Google ou marquée comme suspendue.",
        "procedure": [
            "Email immédiat au client : explication factuelle, ne pas paniquer",
            "Soumettre une demande de reinstatement via le formulaire Google officiel",
            "Joindre les justificatifs : SIRET, justif domicile pro, photos locaux, factures fournisseurs, témoignages clients",
            "Délai de traitement Google : 5 à 15 jours ouvrés",
            "Pendant ce temps : focus sur le site web et les annuaires alternatifs (PagesJaunes, Yelp, Habitatpresto)",
            "Documentation complète dans Notion pour reproduire si récidive",
        ],
    },
    {
        "nom": "Avis Google diffamant ou abusif",
        "symptome": "Avis 1★ avec contenu insultant, mensonger, ou hors sujet (avis sur autre entreprise par exemple).",
        "procedure": [
            "Ne PAS répondre dans l'émotion",
            "Signaler l'avis à Google via 'Avis inapproprié' (raison : faux, conflit d'intérêts, insultes)",
            "En parallèle : préparer une réponse modérée respectant les règles : 'Bonjour [PRENOM], nous regrettons votre expérience. Pouvez-vous nous contacter à [EMAIL] pour qu'on regarde votre dossier en détail ? Cordialement, [NOM]'",
            "Publier la réponse après 24h (cool-down)",
            "Si réellement diffamatoire et non retiré par Google : mise en demeure de retrait via formulaire DDPP / Procureur République (extrême)",
            "Documenter dans Notion. Inclure dans reporting mensuel.",
        ],
    },
    {
        "nom": "Client demande hors périmètre (Google Ads, Insta, etc.)",
        "symptome": "Client demande une prestation qui n'est pas couverte par les 6 composants : SEA, prospection téléphonique, design imprimés, gestion réseaux sociaux non-GBP.",
        "procedure": [
            "Ne PAS céder à la pression sociale. La discipline du périmètre est ce qui permet de tenir la qualité.",
            "Reformuler : 'Bonne idée. Ce n'est pas dans le périmètre actuel, mais je peux te faire un devis séparé si tu veux qu'on l'attaque en parallèle.'",
            "Faire un devis spécifique avec un tarif réaliste (jamais cadeau pour ne pas créer de précédent)",
            "Si refus client : proposer un partenaire ou freelance de confiance qui peut gérer en complément",
            "Documenter la demande dans Notion (utile pour faire évoluer le produit si la demande revient souvent)",
        ],
    },
    {
        "nom": "Retard de paiement",
        "symptome": "Une mensualité de 800 € HT non prélevée ou non virée à l'échéance.",
        "procedure": [
            "J+5 : email courtois 'Pas vu le virement de ce mois, peux-tu vérifier ?'",
            "J+15 : email plus formel + relance par SMS",
            "J+30 : courrier RAR (envoi physique) rappelant article 05 (pénalités L441-10 du Code de commerce, 40 € indemnité de recouvrement)",
            "J+30 : suspension des prestations selon article 05 jusqu'à régularisation (notification écrite)",
            "J+60 : escalade vers conseil juridique CAPEB ou société de recouvrement",
        ],
    },
    {
        "nom": "Demande de résiliation anticipée par le client",
        "symptome": "Client demande à arrêter avant les 12 mois.",
        "procedure": [
            "Première étape : écouter et comprendre la raison (insatisfaction qualité ? problème métier indépendant ? besoin de cash ?)",
            "Si insatisfaction qualité : voir si la garantie qualité 90j s'applique (article 09)",
            "Si raison externe (cessation d'activité, divorce, accident) : ouvrir une négociation à l'amiable, possibilité de geler le contrat 3 mois max",
            "Si rien ne se débloque : appliquer article 13 du contrat. Si résiliation aux torts du Client : indemnité 3 mois retainer (2 400 € HT).",
            "Documenter écrit : courrier RAR avec proposition de sortie négociée",
            "Si médiation : proposer CM2C avant le contentieux",
        ],
    },
]

# ===========================================================
# DATA - KPI INTERNES MAD MAKERS
# ===========================================================

KPI_INTERNES = [
    ("Marge effective par client", "(CA encaissé - dépenses externes) / nombre d'heures travaillées. Cible : ≥ 80 € / heure"),
    ("Délai effectif kick-off à go live", "Jours calendaires du contrat signé à site en prod. Cible : ≤ 14j. Alerte : > 18j"),
    ("Délai de réponse client moyen", "Temps moyen de réponse aux sollicitations client. Cible : ≤ 24h ouvrées. Alerte : ≥ 48h"),
    ("NPS client à 90 jours", "Sondage NPS 3 questions à J+90. Cible : ≥ 50. Alerte : ≤ 30"),
    ("NPS client à 12 mois", "Sondage NPS à fin de contrat. Cible : ≥ 60 (clients matures)"),
    ("Taux de renouvellement post-12 mois", "% clients qui signent un nouvel accord après les 12 mois fermes. Cible : ≥ 50%"),
    ("Garanties Carnet Plein® déclenchées", "Nombre de clients en garantie de continuité gratuite. Alerte : ≥ 1 par cohort"),
    ("Heures hebdo par client (régime de croisière)", "Après le bundle initial. Cible : ≤ 5h/sem/client. Alerte : ≥ 7h/sem/client"),
    ("Saturation cohort", "Nombre de clients actifs en parallèle. Cible : ≤ 3 (qualité). Plafond : 4 (urgence)"),
    ("Taux de paiement à l'échéance", "% mensualités payées dans les 5 jours. Cible : 100%. Alerte : ≤ 95%"),
]

# ===========================================================
# CSS - same charter as bonus #4 / contrat
# ===========================================================

CSS = """
@page {
  size: A4 portrait;
  margin: 20mm 16mm 22mm 16mm;
  @bottom-left {
    content: "Playbook Livraison · Carnet Plein® by Mad Makers · Doc interne";
    font-family: 'JetBrains Mono', monospace;
    font-size: 7pt;
    color: #5a5d56;
    letter-spacing: 0.04em;
  }
  @bottom-right {
    content: counter(page) " / " counter(pages);
    font-family: 'JetBrains Mono', monospace;
    font-size: 7pt;
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
  font-size: 10pt;
  line-height: 1.6;
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
  line-height: 1.2;
  color: #0a0a0a;
}

p { margin: 0 0 0.6em 0; }
p:last-child { margin-bottom: 0; }

strong { font-weight: 600; color: #0a0a0a; }
em { font-style: italic; color: #e0541b; font-weight: 500; }
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
  padding: 30mm 22mm;
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
  font-size: 52pt;
  line-height: 0.95;
  letter-spacing: -0.03em;
  color: #fff;
  margin-top: 28mm;
  font-weight: 700;
}
.cover .sub {
  font-size: 13pt;
  color: #e8e6df;
  max-width: 140mm;
  line-height: 1.4;
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
  font-size: 36pt;
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
  margin: 5mm 0;
  border-radius: 0 3mm 3mm 0;
  page-break-inside: avoid;
}
.callout.dark {
  background: #1a1c18;
  color: #e8e6df;
}
.callout.dark strong { color: #fff; }
.callout h4 {
  font-size: 10pt;
  margin-bottom: 3mm;
  font-family: 'JetBrains Mono', monospace;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #e0541b;
  font-weight: 600;
}
.callout p {
  font-size: 10pt;
  line-height: 1.55;
  margin-bottom: 2mm;
}

/* ===== TIMELINE ===== */
.timeline-block {
  margin: 6mm 0;
}
.timeline-item {
  display: grid;
  grid-template-columns: 22mm 1fr;
  gap: 5mm;
  padding: 4mm 0;
  border-bottom: 1px solid #ebe7dc;
  page-break-inside: avoid;
}
.timeline-item:last-child { border-bottom: none; }
.timeline-day {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11pt;
  font-weight: 700;
  color: #e0541b;
  letter-spacing: 0.02em;
  line-height: 1.2;
}
.timeline-task h4 {
  font-size: 11.5pt;
  margin-bottom: 2mm;
  color: #0a0a0a;
  line-height: 1.25;
}
.timeline-task p {
  font-size: 9.5pt;
  line-height: 1.55;
  color: #3a3d36;
  margin: 0;
}

/* ===== COMPOSANT DEEP DIVE ===== */
.composant-block {
  page-break-inside: auto;
}
.composant-header {
  display: flex;
  align-items: baseline;
  gap: 5mm;
  border-bottom: 2px solid #0a0a0a;
  padding-bottom: 3mm;
  margin-bottom: 5mm;
}
.composant-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11pt;
  color: #e0541b;
  font-weight: 700;
  letter-spacing: 0.06em;
}
.composant-name {
  font-size: 16pt;
  font-weight: 600;
  color: #0a0a0a;
  line-height: 1.2;
}
.composant-section {
  margin: 5mm 0;
  page-break-inside: avoid;
}
.composant-section h4 {
  font-size: 10pt;
  font-family: 'JetBrains Mono', monospace;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #e0541b;
  margin-bottom: 3mm;
  font-weight: 600;
}
.stack-list, .gates-list, .errors-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.stack-list li, .gates-list li {
  font-size: 9.5pt;
  line-height: 1.55;
  margin-bottom: 1.5mm;
  padding-left: 5mm;
  position: relative;
  color: #1a1c18;
}
.stack-list li::before {
  content: "·";
  position: absolute;
  left: 0;
  top: -2mm;
  color: #e0541b;
  font-size: 16pt;
  font-weight: 700;
  line-height: 1;
}
.gates-list li::before {
  content: "☐";
  position: absolute;
  left: 0;
  top: 0;
  color: #e0541b;
  font-size: 12pt;
}
.errors-list li {
  font-size: 9.5pt;
  line-height: 1.55;
  margin-bottom: 1.5mm;
  padding-left: 5mm;
  position: relative;
  color: #1a1c18;
}
.errors-list li::before {
  content: "✕";
  position: absolute;
  left: 0;
  top: 0;
  color: #c43c2a;
  font-weight: 700;
}
.phase-block {
  padding: 3mm 4mm;
  background: #fafaf7;
  border-left: 2px solid #e0541b;
  margin-bottom: 3mm;
  border-radius: 0 2mm 2mm 0;
  page-break-inside: avoid;
}
.phase-block .phase-title {
  font-size: 10pt;
  font-weight: 600;
  margin-bottom: 2mm;
  color: #0a0a0a;
}
.phase-block .phase-desc {
  font-size: 9.5pt;
  line-height: 1.55;
  color: #3a3d36;
}
.tools-line {
  font-size: 9pt;
  color: #5a5d56;
  font-family: 'JetBrains Mono', monospace;
  background: #fafaf7;
  padding: 3mm 4mm;
  border-radius: 2mm;
  margin-top: 3mm;
}
.tools-line::before {
  content: "OUTILS · ";
  font-weight: 700;
  color: #e0541b;
}

/* ===== INCIDENT CARD ===== */
.incident-card {
  background: #fafaf7;
  border: 1px solid #d5d2c9;
  border-left: 3px solid #c43c2a;
  padding: 5mm 6mm;
  margin-bottom: 5mm;
  border-radius: 0 2mm 2mm 0;
  page-break-inside: avoid;
}
.incident-card h4 {
  font-size: 12pt;
  margin-bottom: 2mm;
  color: #c43c2a;
  line-height: 1.25;
}
.incident-symptom {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9pt;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #5a5d56;
  margin-bottom: 3mm;
}
.incident-symptom::before { content: "Symptôme : "; color: #c43c2a; font-weight: 700; }
.incident-proc {
  list-style: decimal;
  padding-left: 5mm;
  margin: 0;
}
.incident-proc li {
  font-size: 9.5pt;
  line-height: 1.55;
  margin-bottom: 2mm;
  color: #1a1c18;
}

/* ===== TABLES ===== */
table.ref-table {
  width: 100%;
  border-collapse: collapse;
  margin: 4mm 0;
  font-size: 9.5pt;
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
  font-size: 9.5pt;
}
table.ref-table td.label {
  font-weight: 600;
  color: #0a0a0a;
  width: 35%;
}
table.ref-table tr:nth-child(even) td {
  background: #ebe7dc;
}

/* ===== FINAL DISCLAIMER ===== */
.final-disclaimer {
  margin-top: 8mm;
  font-size: 8.5pt;
  color: #5a5d56;
  line-height: 1.55;
  font-style: italic;
  border-top: 1px solid #ebe7dc;
  padding-top: 4mm;
}

/* ===== ANNEXES TEMPLATES ===== */
.template-block {
  background: #fafaf7;
  border: 1px solid #d5d2c9;
  border-radius: 3mm;
  padding: 6mm 7mm;
  margin: 5mm 0;
  page-break-inside: avoid;
}
.template-block h4 {
  font-size: 12pt;
  margin-bottom: 4mm;
  color: #0a0a0a;
}
.template-block pre {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8.5pt;
  line-height: 1.55;
  color: #1a1c18;
  white-space: pre-wrap;
  margin: 0;
  background: #fff;
  padding: 4mm 5mm;
  border-radius: 2mm;
  border-left: 2px solid #e0541b;
}
"""

# ===========================================================
# RENDER FUNCTIONS
# ===========================================================

def render_cover():
    return """
<section class="bleed cover">
  <div class="cover-top">
    <span class="badge">Playbook interne · Mad Makers · Doc V1</span>
    <h1>Livraison<br>Carnet Plein<sup style="font-size:0.5em">®</sup>.</h1>
    <p class="sub">Process de livraison J0 à J+14, rythme mensuel M+1 à M+12, procédures de récupération. Pour 1 personne, 3 clients max en parallèle.</p>
  </div>
  <div class="cover-meta">
    <div>
      <div class="accent-line"></div>
      Document interne Rayan Mpondo (Maïck) - Mad Makers
    </div>
    <div>Édition 2026</div>
  </div>
</section>
"""


def render_intro():
    return """
<section class="page intro">
  <div class="eyebrow">À quoi sert ce playbook</div>
  <h1>Le système qui tient la qualité<br>quand tu es seule à livrer.</h1>

  <p class="lead">Ce document est ton manuel opérationnel interne. Il décrit étape par étape ce qui doit se passer entre la signature d'un contrat et la mise en service complète du bundle (J+14), puis le rythme à tenir chaque mois pendant les 12 mois suivants. Il documente aussi les procédures à appliquer quand quelque chose dévie : retard photos client, demande hors périmètre, suspension GBP, avis diffamatoire, etc.</p>

  <div class="callout">
    <h4>Hypothèses opérationnelles</h4>
    <p><strong>Opérateur</strong> : Rayan Mpondo (alias Maïck). Toutes les actions opérationnelles du playbook (livraison, communication client, animation des comptes, reporting) sont menées par Rayan.</p>
    <p><strong>Structure légale</strong> : Mad Makers est une EI au nom de Sara Cankaya, qui fournit le SIRET pour l'activité. Sara apparaît dans les documents juridiques externes (contrats, factures, mentions légales), mais ne participe pas à la livraison opérationnelle au quotidien.</p>
    <p><strong>3 clients en parallèle maximum</strong> : c'est le plafond qui permet de tenir la qualité du périmètre des 6 composants sans dégrader le service. Au-delà, il faut recruter ou refuser.</p>
    <p><strong>14 jours de bundle</strong> : entre kick-off et go-live. Délai contractuel pris dans l'article 06 du contrat. Alerte rouge si > 18 jours.</p>
  </div>

  <div class="callout dark">
    <h4>Comment utiliser ce playbook</h4>
    <p>Lis-le intégralement une fois avant ton premier client. Ensuite, garde-le ouvert sur ton second écran (ou imprimé) pendant les 2 premières livraisons. À partir du 3e client, les automatismes seront en place. Mise à jour annuelle recommandée.</p>
  </div>

  <h3 style="margin-top:8mm;font-size:14pt;">Structure du document</h3>
  <ol>
    <li>Timeline complète : pré-signature, J0 à J+14, rythme mensuel</li>
    <li>Deep dive composant par composant (6 composants, stack + phases + quality gates)</li>
    <li>Rythme mensuel M+1 à M+12 (hebdomadaire, mensuel, trimestriel)</li>
    <li>Procédures de récupération (8 incidents typiques)</li>
    <li>KPI internes Mad Makers</li>
    <li>Stack outils complète</li>
    <li>Annexes : templates emails et messages copy-paste</li>
  </ol>
</section>
"""


def render_timeline_global():
    pre_sign = "".join(
        f"""<div class="timeline-item">
  <div class="timeline-day">{day}</div>
  <div class="timeline-task">
    <h4>{title}</h4>
    <p>{desc}</p>
  </div>
</div>"""
        for day, title, desc in TIMELINE_PRE_SIGN
    )

    j0_j14 = "".join(
        f"""<div class="timeline-item">
  <div class="timeline-day">{day}</div>
  <div class="timeline-task">
    <h4>{title}</h4>
    <p>{desc}</p>
  </div>
</div>"""
        for day, title, desc in TIMELINE_J0_J14
    )

    return f"""
<section class="page">
  <div class="eyebrow">Timeline pré-signature</div>
  <h1>Avant le contrat :<br>3 étapes courtes.</h1>
  <p class="lead">Du premier contact à la signature, en 7 jours typiques.</p>

  <div class="timeline-block">{pre_sign}</div>
</section>

<section class="page">
  <div class="eyebrow">Timeline J0 à J+14</div>
  <h1>Après signature :<br>14 jours, 12 jalons.</h1>
  <p class="lead">Les 12 jalons opérationnels entre la signature et la mise en service complète du bundle. Sois prête : sur les 3 premiers clients, c'est intense. À partir du 4e, les automatismes Notion et les templates feront 60% du boulot.</p>

  <div class="timeline-block">{j0_j14}</div>

  <div class="callout">
    <h4>Le tampon de sécurité de 18 jours</h4>
    <p>Le contrat (article 06) fixe la livraison à 14 jours calendaires. En interne, donne-toi un objectif de 12 jours pour absorber les imprévus. Si tu dépasses 18 jours sans cas de force majeure ou défaillance documentée du client, c'est un signal de surcharge ou de dysfonctionnement à analyser dans le post-mortem mensuel.</p>
  </div>
</section>
"""


def render_composant(c):
    stack_html = "".join(f"<li>{s}</li>" for s in c['stack'])
    phases_html = "".join(
        f"""<div class="phase-block">
  <div class="phase-title">{title}</div>
  <div class="phase-desc">{desc}</div>
</div>"""
        for title, desc in c['phases']
    )
    gates_html = "".join(f"<li>{g}</li>" for g in c['quality_gates'])
    errors_html = "".join(f"<li>{e}</li>" for e in c['erreurs'])

    return f"""
<section class="page composant-block">
  <div class="composant-header">
    <span class="composant-num">COMPOSANT {c['num']} / 06</span>
    <span class="composant-name">{c['nom']}</span>
  </div>

  <div class="composant-section">
    <h4>Stack technique</h4>
    <ul class="stack-list">{stack_html}</ul>
  </div>

  <div class="composant-section">
    <h4>Phases opérationnelles</h4>
    {phases_html}
  </div>

  <div class="composant-section">
    <h4>Quality gates avant de déclarer livré</h4>
    <ul class="gates-list">{gates_html}</ul>
  </div>

  <div class="composant-section">
    <h4>Erreurs classiques à éviter</h4>
    <ul class="errors-list">{errors_html}</ul>
  </div>

  <div class="tools-line">{c['tools']}</div>
</section>
"""


def render_rythme():
    hebdo = "".join(
        f'<tr><td class="label">{jour}</td><td>{tache}</td></tr>'
        for jour, tache in RYTHME_HEBDO
    )
    mensuel = "".join(
        f'<tr><td class="label">{moment}</td><td>{tache}</td></tr>'
        for moment, tache in RYTHME_MENSUEL
    )
    trimestriel = "".join(
        f'<tr><td class="label">{moment}</td><td>{tache}</td></tr>'
        for moment, tache in RYTHME_TRIMESTRIEL
    )

    return f"""
<section class="page">
  <div class="eyebrow">Rythme hebdomadaire en régime de croisière</div>
  <h1>5 jours, 5 missions courtes,<br>jamais plus de 4h/jour par client.</h1>
  <p class="lead">À partir de M+1 (après la livraison initiale), la charge se stabilise. Avec 3 clients en parallèle, vise ≤ 5 heures par semaine par client en moyenne, hors visios mensuelles.</p>

  <table class="ref-table">
    <thead><tr><th style="width:18%;">Jour</th><th>Action</th></tr></thead>
    <tbody>{hebdo}</tbody>
  </table>

  <h3 style="margin-top:6mm;font-size:12pt;">Rythme mensuel par client</h3>
  <table class="ref-table">
    <thead><tr><th style="width:22%;">Moment</th><th>Action</th></tr></thead>
    <tbody>{mensuel}</tbody>
  </table>

  <h3 style="margin-top:6mm;font-size:12pt;">Rythme trimestriel</h3>
  <table class="ref-table">
    <thead><tr><th style="width:22%;">Moment</th><th>Action</th></tr></thead>
    <tbody>{trimestriel}</tbody>
  </table>

  <div class="callout">
    <h4>Le piège du multitasking inter-clients</h4>
    <p>Avec 3 clients, la tentation est de papillonner. Plus efficace : <strong>1 plage horaire = 1 client</strong>. Ex : lundi matin = client A, lundi après-midi = client B, mardi = client C. Sinon tu perds 30% de temps en context-switching.</p>
  </div>
</section>
"""


def render_incidents():
    cards = "".join(f"""
<div class="incident-card">
  <h4>{inc['nom']}</h4>
  <div class="incident-symptom">{inc['symptome']}</div>
  <ol class="incident-proc">
    {"".join(f"<li>{step}</li>" for step in inc['procedure'])}
  </ol>
</div>
""" for inc in INCIDENTS)

    return f"""
<section class="page">
  <div class="eyebrow">Procédures de récupération</div>
  <h1>Quand ça dévie, voilà<br>quoi faire (sans paniquer).</h1>
  <p class="lead">8 incidents typiques en B2B service local, avec la procédure exacte à appliquer. À mémoriser ou imprimer pour le terrain. La discipline procédurale en cas d'incident est ce qui sépare un opérateur de niveau pro d'un opérateur amateur.</p>

  {cards}
</section>
"""


def render_kpi():
    rows = "".join(
        f'<tr><td class="label">{nom}</td><td>{cible}</td></tr>'
        for nom, cible in KPI_INTERNES
    )

    return f"""
<section class="page">
  <div class="eyebrow">KPI internes Mad Makers</div>
  <h1>10 indicateurs à suivre<br>pour ton propre pilotage.</h1>
  <p class="lead">Ces KPI ne sont PAS ceux que tu reportes au client (ceux-là sont dans l'article 08 et l'annexe 1 du contrat). Ce sont les indicateurs de TON business à toi : marge, charge, qualité, rétention. À relever le 20 de chaque mois.</p>

  <table class="ref-table">
    <thead><tr><th style="width:40%;">Indicateur</th><th>Définition + cible</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>

  <div class="callout dark">
    <h4>Décisions déclenchées par les KPI</h4>
    <p><strong>Saturation cohort à 3</strong> : tu ouvres une cohort la suivante. Si la demande dépasse 3 récurrents, c'est le moment de recruter (apprentie, freelance) ou de monter les prix.</p>
    <p><strong>NPS 90j ≤ 30</strong> : tu réajustes immédiatement avec le client concerné. Discussion ouverte avant que ça dégénère en résiliation.</p>
    <p><strong>Garantie déclenchée ≥ 1 par cohort</strong> : le système ne marche pas pour le profil cible. Soit tu refines la sélection client (entretien commercial plus dur), soit tu améliores le produit, soit tu changes la promesse.</p>
  </div>
</section>
"""


def render_stack():
    stack_complete = [
        ("Site web", "Vercel (UE), Cloudflare R2 (médias), GitHub (versioning), Bunny Fonts, VS Code"),
        ("Google Business Profile", "GBP web + app mobile iOS/Android, Whitespark Local Citation Finder (optionnel)"),
        ("Avis automatisés", "Brevo (FR, SMS + email), Twilio (alternatif), GBP web pour réponses, Google Docs templates"),
        ("Reporting mensuel", "Python + HTML/CSS (template), GBP Insights, GA4 si présent, Google Sheets suivi"),
        ("Photos chantiers", "WhatsApp Business (numéro dédié), Snapseed iOS/Android, Google Photos (Gomme Magique)"),
        ("Coaching", "Zoom ou Google Meet, Calendly récurrent, Notion partagé client, email"),
        ("CRM léger interne", "Notion (template Mad Makers à dupliquer pour chaque client)"),
        ("Paiement", "Stripe (cartes + virements SEPA) ou GoCardless (SEPA exclusif, moins de frais)"),
        ("Contrat", "Yousign (signature électronique conforme eIDAS)"),
        ("Facturation", "Tiime ou Indy (compatible auto-entrepreneur / EI), connecté Stripe"),
        ("Comptabilité", "Tiime (1ère année) ou comptable externe (à partir de 50k€ CA)"),
        ("Email pro", "Google Workspace (sara@mad-makers.fr - 6€/mois)"),
        ("Stockage", "Google Drive Workspace inclus + Notion + GitHub privés"),
        ("Monitoring", "Better Uptime (free tier) pour 1 ping/min sur chaque site client"),
        ("Backup", "GitHub privé + export Notion mensuel + sauvegarde Drive"),
    ]

    rows = "".join(
        f'<tr><td class="label">{cat}</td><td>{outils}</td></tr>'
        for cat, outils in stack_complete
    )

    return f"""
<section class="page">
  <div class="eyebrow">Stack outils complète</div>
  <h1>15 outils, c'est tout.<br>Pas un de plus.</h1>
  <p class="lead">Le stack consolidé pour opérer 3 clients en parallèle sans saturation, sans abonnement inutile. Coût total approximatif : 60 à 120 € HT par mois selon les options et le nombre de clients.</p>

  <table class="ref-table">
    <thead><tr><th style="width:32%;">Catégorie</th><th>Outils</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>

  <div class="callout">
    <h4>Principe : un seul outil par fonction</h4>
    <p>La tentation est forte d'ajouter le dernier outil à la mode (Cal.com vs Calendly, Beehiiv vs Substack, etc.). Avec un solo et 3 clients max, la simplicité bat la flexibilité. <strong>Ne change un outil que si l'actuel te freine concrètement</strong>, pas par envie d'optimiser.</p>
  </div>
</section>
"""


def render_templates_annexe():
    return f"""
<section class="page">
  <div class="eyebrow">Annexe 1 - Templates copy-paste</div>
  <h1>Les messages que tu vas<br>envoyer 100 fois.</h1>
  <p class="lead">À copier-coller dans tes outils (email, SMS, WhatsApp). Personnalise les placeholders [PRENOM], [DATE], [VILLE], etc. à chaque envoi. Garde une version éditable dans Notion pour faire évoluer.</p>

  <div class="template-block">
    <h4>T01 - Email de bienvenue post-signature (J+1)</h4>
<pre>Objet : Bienvenue chez Carnet Plein® - on démarre cette semaine

Bonjour [PRENOM],

Merci pour ta confiance, signature reçue, paiement bien arrivé.

Concrètement, voici ce qui va se passer dans les 14 prochains jours :

- J+1 (aujourd'hui) : tu reçois ce message + un lien Notion partagé où tout sera centralisé (notre brief, les action items, les photos, les rapports). Tu reçois aussi un lien vers le questionnaire pré-kick-off, à remplir avant lundi prochain.

- J+1 à J+5 : tu me communiques les accès aux comptes existants (Google Business Profile, hébergeur si tu as un site, registrar du nom de domaine). Notion contient la liste exacte.

- J+7 : kick-off visio de 90 minutes. On valide le positionnement, on choisit ton KPI principal Carnet Plein® (annexe 1 du contrat), on cale le planning.

- J+8 à J+14 : je livre le bundle complet (site, GBP optimisé, système d'avis, photos, reporting M+1 calé).

Pour le rendez-vous kick-off, propose-moi 3 créneaux la semaine prochaine ici : [LIEN_CALENDLY]

À très vite,
Rayan (Maïck) - Mad Makers
contact@mad-makers.fr - 01 89 72 44 98
</pre>
  </div>

  <div class="template-block">
    <h4>T02 - SMS de rappel photos chantiers (J+1 si rien reçu)</h4>
<pre>Hello [PRENOM], pas de photo cette semaine ?
Pas grave, mais le rituel marche mieux avec
2-3 par chantier. À ce soir si t'as quelque
chose.
- Rayan (Mad Makers)
</pre>
  </div>

  <div class="template-block">
    <h4>T03 - SMS post-chantier client final (vers le client du client)</h4>
<pre>Bonjour [PRENOM_CLIENT_FINAL], merci de
nous avoir confié votre chantier. Votre
retour compte beaucoup pour notre équipe :
[LIEN_AVIS_GOOGLE]
Belle journée,
[NOM_ARTISAN]
</pre>
  </div>

  <div class="template-block">
    <h4>T04 - Email d'envoi du reporting mensuel (le 5 du mois)</h4>
<pre>Objet : [VILLE_CLIENT] - Reporting Carnet Plein® de [MOIS]

Bonjour [PRENOM],

Voici ton reporting du mois de [MOIS], 5 pages,
PDF en pièce jointe.

3 points saillants en synthèse :
- [POINT 1 - chiffre ou tendance majeure]
- [POINT 2 - succès ou alerte]
- [POINT 3 - recommandation pour le mois en cours]

Tu peux ouvrir le PDF complet quand tu as 5 minutes.
Si tu veux qu'on en discute en visio, voici mes créneaux
cette semaine : [LIEN_CALENDLY].

Sinon, on se voit comme d'habitude le [DATE_VISIO_MENSUELLE]
pour le point d'étape.

Bonne semaine,
Rayan
</pre>
  </div>

  <div class="template-block">
    <h4>T05 - Sondage NPS à J+90 (3 questions max)</h4>
<pre>Objet : 3 questions, 90 secondes - retour
honnête après 90 jours ?

Bonjour [PRENOM],

Ça fait 90 jours qu'on bosse ensemble.
Pour que je m'améliore, j'aimerais 3 retours
honnêtes :

1. De 0 à 10, à quel point tu recommanderais
   Carnet Plein® à un confrère artisan ?
   [REPONSE LIBRE]

2. Qu'est-ce qui a le mieux marché pour toi ?
   [REPONSE LIBRE]

3. Qu'est-ce que je devrais ajuster ou améliorer ?
   [REPONSE LIBRE]

Réponse par retour d'email, 2 minutes max.
Pas de Tally, pas de Typeform, pas de questionnaire
à rallonge. Juste tes mots à toi.

Merci d'avance,
Rayan
</pre>
  </div>

  <div class="template-block">
    <h4>T06 - Message de bienvenue WhatsApp group cohort (envoyé à l'issue du kick-off groupé)</h4>
<pre>Bienvenue dans le WhatsApp group de la cohort
[MOIS] !

Ici on partage entre nous trois (+ moi) :
- Les wins de la semaine (chantiers signés, bons
  retours clients, photos qui claquent)
- Les blocages où vous avez besoin d'un coup de
  main de pair
- Les questions rapides du quotidien

Une règle non négociable : tout ce qui se dit ici
reste ici. Si vous voulez en parler à votre
femme/comptable/confrère, allez-y. Mais pas de
copies d'écran, pas de captures partagées en dehors
du groupe.

Rythme léger : je passe matin et soir, pas de
réponse garantie 24/7. Pour les vraies urgences
techniques (site down, GBP suspendu), c'est mon
numéro direct, pas le groupe.

On se retrouve aussi tous les 1ers mardis du mois
à 18h en visio à 4 (45 min). Le prochain rendez-vous
est dans votre Calendly.

Bienvenue les trois !
- Rayan
</pre>
  </div>

  <div class="template-block">
    <h4>T07 - Ordre du jour visio cohort mensuelle (45 min, animation Rayan)</h4>
<pre>VISIO COHORT [MOIS] - 45 minutes - 4 personnes

00:00 - 00:05 Accueil + rappel règle Chatham House
              (« ce qu'on partage ici reste ici »)

00:05 - 00:20 Tour de table WINS du mois
              5 min par artisan max (chronométré)
              Un chiffre ou un fait concret, pas du
              ressenti

00:20 - 00:35 Tour de table BLOCAGES du mois
              5 min par artisan max
              Un blocage métier, business ou perso
              qui impacte le projet

00:35 - 00:42 CONSEIL CROISÉ entre pairs
              Les artisans se conseillent
              entre eux (pas moi). Mon rôle :
              facilitateur, pas expert.

00:42 - 00:45 ANNONCES + prochain RDV
              - 1 ou 2 annonces si actualité métier
                (changement légal, aide nouvelle)
              - Confirmation visio cohort mois suivant
              - Rappel des actions individuelles à
                checker en visio 1:1

Post-visio (sous 24h) :
- Synthèse 5 lignes max dans WhatsApp group
- Actions individuelles dans Notion par artisan
</pre>
  </div>

  <div class="template-block">
    <h4>T08 - Kick-off groupé cohort (60 min, 1er lundi du mois nouvelle cohort)</h4>
<pre>KICK-OFF GROUPÉ COHORT [MOIS] - 60 min - 4 personnes

00:00 - 00:15 Tour de table présentation
              5 min par artisan : prénom, métier,
              ville, années d'activité, objectif
              en 1 phrase

00:15 - 00:35 Présentation programme Carnet Plein®
              - Les 6 composants en 10 min
              - Le calendrier J+8 à J+14 en 5 min
              - La cohort : visio mensuelle, WhatsApp,
                règle Chatham House (5 min)

00:35 - 00:50 Calage du KPI commun de cohort
              - Pas obligatoire, mais utile
              - Ex : « cohort de mai vise +30% de
                demandes de devis cumulées sur 12 mois »
              - On regardera ensemble la progression
                en visio cohort mensuelle

00:50 - 01:00 Q&A + création du WhatsApp group cohort
              en direct pendant la visio
              Envoi du message de bienvenue T06

Post-kick-off (sous 4h) :
- Email récap à chaque artisan individuellement
- Message T06 envoyé dans le WhatsApp group
- Création des 3 espaces Notion clients
- Confirmation date de la 1ère visio cohort
  mensuelle (1er mardi du mois suivant)
</pre>
  </div>
</section>

<section class="page">
  <div class="eyebrow">Annexe 2 - Questionnaire pré-kick-off</div>
  <h1>Les 10 questions à poser avant<br>le kick-off pour gagner 1h.</h1>
  <p class="lead">À envoyer en lien Notion ou Tally avec un délai de 5 jours. Sans ces réponses, le kick-off de 90 minutes en perd 30 à 45 (à découvrir des évidences). Avec ces réponses, on attaque direct le sujet stratégique.</p>

  <div class="template-block">
    <h4>Questionnaire à envoyer</h4>
<pre>Pré-kick-off Carnet Plein® - 10 questions

1. Ton métier principal et tes services secondaires ?
   (ex: plombier-chauffagiste + dépannage urgence)

2. Ta zone géographique d'intervention ?
   (ville centre + rayon en km, ou liste de villes)

3. Combien de chantiers par semaine en ce moment ?
   (plus important pour calibrer le KPI)

4. Type de chantiers principaux ?
   (PAC, chaudière gaz, dépannage, salle de bain, etc.)

5. Tes certifications actuelles ?
   (RGE Qualibat, Qualigaz, PG, etc.)

6. Tes marques partenaires ou principales installées ?
   (Atlantic, Daikin, Mitsubishi, etc.)

7. As-tu déjà un site internet ?
   (URL si oui, sinon non)

8. As-tu une fiche Google Business Profile ?
   (URL ou nom de la fiche si oui)

9. Combien d'avis Google as-tu actuellement ?
   (estimation OK)

10. Ton objectif réel à 12 mois ?
    (en mots à toi, pas en KPI : ex « ne plus chercher
    de chantiers, choisir mes clients, embaucher
    un apprenti »)

Bonus : trois photos récentes que tu peux m'envoyer
        pour démarrer le portfolio.

À renvoyer avant lundi [DATE].
</pre>
  </div>
</section>

<section class="page">
  <div class="eyebrow">Annexe 3 - Checklist quality gates condensée</div>
  <h1>La checklist à cocher<br>avant de dire « livré ».</h1>
  <p class="lead">Version condensée pour avoir tout sous les yeux le jour du go-live (J+14). À imprimer ou afficher en wallpaper d'écran.</p>

  <div class="template-block">
    <h4>Quality Gates - Go-Live J+14</h4>
<pre>SITE WEB
☐ Lighthouse mobile : Performance ≥ 90
☐ Lighthouse mobile : Accessibilité ≥ 95
☐ Lighthouse mobile : SEO ≥ 95
☐ Tests iOS Safari + Android Chrome OK
☐ Mentions légales complètes (SIRET, RCS,
  TVA, décennale, médiateur conso)
☐ Schema.org LocalBusiness avec NAP cohérent
☐ Favicon, OG image, meta description
☐ Formulaire contact testé bout en bout
☐ HTTPS forcé actif
☐ Domaine final pointé sur Vercel

GOOGLE BUSINESS PROFILE
☐ 12 points du Bonus #1 cochés
☐ Minimum 10 photos catégorisées
☐ Description sans bourrage mots-clés
☐ Horaires + horaires spéciaux
☐ Zones desservies cohérentes
☐ NAP identique au site
☐ Premier Google Post publié

SYSTEME AVIS
☐ Lien d'avis testé sur 3 navigateurs
☐ SMS test reçu en 30 secondes
☐ 5 templates de réponses prêts
☐ Process de déclenchement validé client
☐ Backup procédure manuelle écrite

PHOTOS CHANTIERS
☐ WhatsApp Business setup numéro dédié
☐ Briefing client 5 règles fait
☐ Premier envoi test reçu et traité
☐ Droit à l'image vérifié (visages, plaques)

REPORTING
☐ Template de rapport mensuel calé
☐ Sources de données identifiées (GBP, GA4)
☐ Premier reporting M+1 programmé pour J+35

ACCOMPAGNEMENT
☐ Notion partagé créé et structuré
☐ Visio mensuelle calée dans Calendly récurrent
☐ Premier compte-rendu de kick-off envoyé

ADMIN
☐ Contrat signé bilatéralement
☐ Annexe 1 (KPI objectif) signée
☐ Paiement setup reçu
☐ Mandat SEPA en place pour mensualités
☐ Factures de setup envoyée et comptabilisée
</pre>
  </div>

  <div class="final-disclaimer">
    Doc V1 - mai 2026. Mise à jour annuelle recommandée. Ce playbook intègre les conventions issues des Bonus #1 à #4 (Fiche Google Parfaite, 30 Réponses Avis, Photos qui Vendent, Devis qui Close à 70%) et du contrat de prestation Carnet Plein® V1. Les outils mentionnés et leurs tarifs (Vercel, Brevo, Twilio, Stripe, Yousign, etc.) sont à jour de mai 2026 et peuvent évoluer. Les KPI cibles internes sont des points de référence, à ajuster selon ton expérience après 3 à 6 premiers clients.
  </div>
</section>
"""


def render_html():
    parts = [
        render_cover(),
        render_intro(),
        render_timeline_global(),
    ]

    parts.append("""
<section class="bleed section-sep">
  <div class="label">- Composants 1 à 6</div>
  <h2>Six composants, six<br>quality gates, zéro flou.</h2>
  <div class="count">Site · GBP · Avis · Reporting · Photos · Coaching</div>
  <p class="desc">Pour chacun des 6 composants : la stack technique à utiliser, les phases opérationnelles dans l'ordre, les quality gates à cocher avant de déclarer livré, les erreurs classiques à éviter. À lire intégralement avant le premier client.</p>
</section>
""")

    for c in COMPOSANTS_DETAIL:
        parts.append(render_composant(c))

    parts.append(render_rythme())
    parts.append(render_incidents())
    parts.append(render_kpi())
    parts.append(render_stack())
    parts.append(render_templates_annexe())

    body = "\n".join(parts)

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Playbook Livraison Carnet Plein® - Doc interne Mad Makers</title>
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
        "playbook-livraison-carnet-plein.html"
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
    print(f"     Pages estimees : ~28 (cover + intro + timelines + 6 composants + rythme + incidents + KPI + stack + 3 annexes)")
    print()
    print("PROCHAINE ETAPE :")
    print("  1. Ouvrir le .html dans Chrome")
    print("  2. Ctrl+P (Imprimer)")
    print("  3. Destination : Enregistrer au format PDF")
    print("  4. Marges : Aucune (le CSS gere)")
    print("  5. Cocher Graphiques d'arriere-plan")
    print("  6. Enregistrer sous : Playbook Livraison Carnet Plein - V1.pdf")
