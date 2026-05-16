#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script - Plan strategique Mad Makers
A presenter a Goudet Abale (co-fondateur, Strategie & Developpement).

Objectifs :
1. Valider la direction Carnet Plein(R) avant prospection
2. Permettre a Goudet de prendre une decision sur son engagement
3. Servir de support pour challenger le plan

Generates plan-strategique-mad-makers.html in this folder.
Open in Chrome -> File > Print > Save as PDF (A4 portrait).
"""
import os

# ===========================================================
# DATA
# ===========================================================

ROLES_PROPOSES = [
    {
        "personne": "Rayan Mpondo (Maïck)",
        "perimetre": "Opérateur Carnet Plein®",
        "responsabilites": [
            "Livraison des 6 composants pour chaque client (site, GBP, avis, reporting, photos, coaching)",
            "Animation des cohorts (kick-off groupé + visios mensuelles + WhatsApp)",
            "Prospection terrain et appels Calendly (audits gratuits 20 min)",
            "Relations clients : email, SMS, visios, reporting mensuel",
            "Direction créative et brand Mad Makers (site, identité visuelle, contenus)",
            "Maintenance technique : site, hébergement, monitoring",
        ],
        "charge_hebdo": "30 à 40 h/sem (saturée à 3 cohorts actives en parallèle)",
    },
    {
        "personne": "Goudet Abalé",
        "perimetre": "Stratégie & Développement (à valider)",
        "responsabilites": [
            "Direction stratégique de l'agence Mad Makers (parent mad-makers.fr)",
            "Pilotage financier : comptabilité, prévisionnel, optimisation fiscale",
            "Recherche d'investissement si nécessaire (capital, BPI, crédit pro)",
            "Support cohort : co-animation possible des visios mensuelles, backup en cas d'indisponibilité de Rayan",
            "Développement de nouvelles offres / nouvelles niches au-delà de Carnet Plein®",
            "Pilotage des KPI globaux Mad Makers (CA, marge, NPS, taux de renouvellement)",
            "Partenariats stratégiques (CAPEB, FFB, fournisseurs technologiques, freelances futurs)",
        ],
        "charge_hebdo": "À définir ensemble (5 à 15 h/sem selon engagement choisi)",
    },
    {
        "personne": "Sara Cankaya",
        "perimetre": "Structure juridique (passive)",
        "responsabilites": [
            "Représentation légale de Mad Makers EI",
            "Détentrice du SIRET 832 059 695 00029",
            "Signature des contrats officiels et documents juridiques externes",
            "Non opérationnelle au quotidien sur la livraison ni sur la stratégie",
        ],
        "charge_hebdo": "Quasi-nulle (signatures ponctuelles uniquement)",
    },
]

# ===========================================================
# DATA - PROJECTIONS CHIFFREES
# ===========================================================

# Hypothese tarif : 5000 EUR HT setup + 800 EUR HT/mois x 11 mois = 13800 EUR HT par contrat
# TVA 20 % B2B
# Année 1 mois par mois

def compute_projections(clients_per_month):
    """Calcule CA HT par mois pour année 1 selon nombre de signatures/mois."""
    setup = 5000
    retainer = 800
    months = []
    cumulative_active = 0
    for m in range(1, 13):
        new_signed = clients_per_month
        # nouveaux clients du mois apportent setup
        revenue_setup_month = new_signed * setup
        # MRR : tous les clients deja signes ET en periode retainer (mois 2 a 12 du contrat)
        # Approximation : au mois m, les clients signes au mois 1 sont au mois m de contrat
        # ils paient le retainer du mois 2 au mois 12 (11 mois)
        revenue_mrr_month = 0
        for prev_month in range(1, m):
            # clients signes au mois prev_month sont au mois (m - prev_month + 1) du contrat
            contract_month = m - prev_month + 1
            if 2 <= contract_month <= 12:
                revenue_mrr_month += new_signed * retainer
        cumulative_active += new_signed
        total_month = revenue_setup_month + revenue_mrr_month
        months.append({
            "mois": m,
            "actifs": cumulative_active,
            "setup": revenue_setup_month,
            "mrr": revenue_mrr_month,
            "total_ht": total_month,
        })
    return months


SCENARIO_CONSERVATIVE = compute_projections(2)
SCENARIO_REALISTE = compute_projections(3)

# Totaux annuels
TOTAL_CONS = sum(m["total_ht"] for m in SCENARIO_CONSERVATIVE)
TOTAL_REA = sum(m["total_ht"] for m in SCENARIO_REALISTE)
MRR_12_CONS = SCENARIO_CONSERVATIVE[-1]["mrr"]
MRR_12_REA = SCENARIO_REALISTE[-1]["mrr"]

# Charges externes annuelles estimees (HT)
CHARGES_EXTERNES = {
    "Stack outils SaaS": (60 + 120) // 2 * 12,  # ~ 1080 EUR
    "Compta Tiime ou comptable externe": 1800,
    "Frais bancaires + paiements Stripe": 1500,
    "Hosting Vercel + Cloudflare R2 + Render CRM": 600,
    "Yousign + Calendly + Notion": 480,
    "Avocat relecture contrat (one-time mais provisionne)": 600,
    "Communication / déplacements terrain": 1500,
    "Formations / outils ponctuels": 1000,
}
TOTAL_CHARGES_EXT = sum(CHARGES_EXTERNES.values())

# ===========================================================
# DATA - RISQUES TOP 5
# ===========================================================

RISQUES = [
    {
        "nom": "Saturation opérationnelle de Rayan",
        "proba": "ÉLEVÉE",
        "impact": "MAJEUR",
        "description": "Solo, Rayan ne peut pas livrer durablement plus de 5 à 8 clients en régime de croisière (5h/sem/client minimum). Au-delà : qualité dégradée, retards, garantie déclenchée, churn.",
        "mitigation": "Recrutement structuré dès 12-15 clients actifs : chargé(e) de projet à temps partiel (apprenti / freelance / alternant). Investissement à anticiper dans la roadmap.",
    },
    {
        "nom": "Dépendance Google (GBP)",
        "proba": "FAIBLE",
        "impact": "MAJEUR",
        "description": "Suspension d'une fiche GBP par Google = arrêt brutal d'un des 6 composants. Si plusieurs clients suspendus en même temps, dommage réputationnel agence.",
        "mitigation": "Diversification : référencement local sur PagesJaunes, Yelp, Habitatpresto en parallèle. Process de reinstatement documenté (procédure incident playbook). Conformité stricte aux règles Google (pas d'avis achetés, pas de zones desservies sur-déclarées).",
    },
    {
        "nom": "Concurrence agences spécialisées BTP",
        "proba": "MOYENNE",
        "impact": "MOYEN",
        "description": "Plusieurs agences (Habitatpresto, Partoo, SK Web, Phaos, Digibat) ciblent déjà les artisans avec des offres parfois plus abordables. Risque de pression sur les prix.",
        "mitigation": "Positionnement différencié : (1) niche serrée plombiers-chauffagistes vs généraliste, (2) Cohort + accompagnement humain vs SaaS impersonnel, (3) Bonus livrables qualifiants (PDFs, Devis Cialdini) que les concurrents ne fournissent pas, (4) Garantie Carnet Plein® unique sur le marché.",
    },
    {
        "nom": "Cadre juridique fragile (structure Sara EI)",
        "proba": "MOYENNE",
        "impact": "MAJEUR",
        "description": "Si Rayan opère sous SIRET Sara sans statut formalisé (salarié, sous-traitant déclaré, gérant), risque qualifié de travail dissimulé par l'URSSAF (article L8221-1 Code travail). Sanctions : amende + redressement + interdiction d'exercer pendant 3 ans.",
        "mitigation": "À résoudre AVANT le premier client signé. Trois options : (1) Création d'une SAS / SASU avec Rayan et Goudet associés, Sara reste EI séparée, (2) Rayan devient salarié de l'EI Mad Makers (CDI avec déclaration URSSAF), (3) Rayan crée sa propre EI / micro-entreprise et facture Mad Makers en sous-traitance. Décision à prendre avec un expert-comptable et le cas échéant un avocat en droit des sociétés.",
    },
    {
        "nom": "Sous-investissement marketing inbound",
        "proba": "MOYENNE",
        "impact": "MOYEN",
        "description": "Le site carnetplein.mad-makers.fr est lancé sans budget publicitaire ni stratégie SEO active. Si la prospection sortante (CRM + appels) ne porte pas, croissance trop lente pour atteindre le plafond opérationnel.",
        "mitigation": "Stratégie de visibilité organique low-cost : publier 1 article/mois sur le blog Mad Makers ciblant des requêtes longue traîne (« comment optimiser sa fiche Google artisan », « calculer son TVA réduite chaudière 2026 »), publier sur LinkedIn 2 fois par semaine, demander aux 1ers clients pilotes des recommandations explicites.",
    },
]

# ===========================================================
# DATA - DECISIONS A PRENDRE AVEC GOUDET
# ===========================================================

DECISIONS = [
    {
        "num": "01",
        "titre": "Engagement de Goudet : temps et capital",
        "options": [
            "(a) Engagement actif : 10 à 15 h/sem sur Mad Makers, co-animation cohort, pilotage compta+strategie, recherche investissement. Implique une rémunération (salaire, dividendes ou parts).",
            "(b) Engagement light : 5 h/sem en advisory, conseil stratégique mensuel, support ponctuel cohort. Pas de salaire mais participation aux bénéfices.",
            "(c) Engagement minimal : silent partner / advisor non rémunéré sur les premiers mois, ré-évaluation au mois 6.",
        ],
        "recommandation": "Option (a) si Goudet a la bande passante. Plus la barre est haute côté investissement, plus l'agence peut scaler vite (recrutement plus tôt, prospection plus large). Option (b) est un fallback acceptable.",
    },
    {
        "num": "02",
        "titre": "Structure juridique cible (court terme)",
        "options": [
            "(a) Statu quo : EI Sara Cankaya, Rayan en sous-traitance déclarée (Rayan crée micro-entreprise et facture Mad Makers). Simple, mais limité pour scaler.",
            "(b) Création d'une SAS / SASU : Rayan président, Goudet associé minoritaire ou égalitaire. Plus de crédibilité B2B, meilleure optimisation fiscale au-dessus de 50k€ de bénéfice.",
            "(c) SARL : Rayan + Goudet co-gérants. Moins de flexibilité que SAS mais charges sociales plus stables.",
        ],
        "recommandation": "Option (b) SASU ou SAS. Coût création ~300-500 € + comptable 80-120 €/mois. Rentabilisé dès 80k€ de CA annuel. Permet aussi de faire entrer Goudet au capital formellement.",
    },
    {
        "num": "03",
        "titre": "Répartition économique entre associés",
        "options": [
            "(a) 60% Rayan / 40% Goudet : reconnaît que Rayan est l'opérateur principal (livraison + brand + créa)",
            "(b) 50% / 50% : reconnaît un engagement équitable des deux côtés (Rayan ops, Goudet stratégie + capital + compta)",
            "(c) Vesting progressif : 70/30 à l'origine, transition vers 50/50 sur 4 ans si Goudet tient ses engagements opérationnels (avec triggers documentés)",
        ],
        "recommandation": "Option (c) Vesting progressif. Évite la rancœur si l'un des deux décroche. Standard dans la startup française. Documenter clairement les triggers.",
    },
    {
        "num": "04",
        "titre": "Scénario de croissance cible",
        "options": [
            "(a) Scénario conservateur : 2 signatures/mois, 24 contrats year 1, ~225k€ CA HT. Solo Rayan jusqu'à fin year 1, embauche year 2.",
            "(b) Scénario réaliste : 3 signatures/mois, 36 contrats year 1, ~330k€ CA HT. Embauche dès mois 8-10 (chargé de projet temps partiel).",
            "(c) Scénario ambitieux : 4-5 signatures/mois en s'appuyant fortement sur le CRM prospection + LinkedIn outreach. 48 à 60 contrats year 1, ~440-550k€ CA HT. Embauche plus rapide (2-3 personnes mid-year).",
        ],
        "recommandation": "Option (b) Scénario réaliste, qui s'aligne avec la cohort de 3/mois et permet d'embaucher sans précipitation. Option (c) viable seulement si on investit en marketing payant (à acter avec Goudet).",
    },
    {
        "num": "05",
        "titre": "Stratégie d'acquisition pour les 6 premiers mois",
        "options": [
            "(a) 100% prospection sortante via CRM : appel + email à 500 prospects. Effort cold call quotidien.",
            "(b) 100% réseau perso + parrainage : démarrer avec les contacts existants de Rayan et Goudet, demander des recommandations.",
            "(c) Mix sortant (CRM) + organique (LinkedIn, blog, SEO local) + réseau. Plus large mais demande des heures réparties.",
        ],
        "recommandation": "Option (b) puis (c). Les 3 premiers clients devraient venir du réseau (taux de conversion plus élevé, témoignages plus solides, marge de manœuvre sur le tarif pilote). À partir du mois 3, basculer en (c) avec le CRM en backbone.",
    },
    {
        "num": "06",
        "titre": "Réinvestissement vs distribution des bénéfices",
        "options": [
            "(a) Réinvestir 100% du bénéfice net year 1 dans l'agence (recrutement, outils, ads).",
            "(b) Distribuer 50% en salaires / dividendes year 1, réinvestir 50%.",
            "(c) Distribuer 80% year 1 (récompenser le démarrage), réinvestir 20%.",
        ],
        "recommandation": "Option (a) ou (b) selon les besoins de cash personnel de Rayan et Goudet. Si Rayan n'a pas besoin de salaire massif sur year 1 (autres revenus), option (a) maximise la croissance year 2.",
    },
    {
        "num": "07",
        "titre": "Roadmap Mad Makers parent vs Carnet Plein® enfant",
        "options": [
            "(a) Focus exclusif Carnet Plein® pendant 12 mois, mad-makers.fr en veille",
            "(b) Carnet Plein® 80% + mad-makers.fr maintenu actif (portfolio, blog SEO, leads d'autres niches)",
            "(c) Carnet Plein® en pilote year 1, mad-makers.fr montée en gamme year 2 avec d'autres offres B2B (artisans autres métiers, TPE locales)",
        ],
        "recommandation": "Option (c). Year 1 = preuve de concept Carnet Plein®. Year 2 = capitalisation sur les apprentissages pour ouvrir 1 ou 2 autres niches verticales sous la marque parent Mad Makers.",
    },
]

# ===========================================================
# CSS - same charter as previous docs (Carnet Plein/Mad Makers)
# ===========================================================

CSS = """
@page {
  size: A4 portrait;
  margin: 22mm 16mm 24mm 16mm;
  @bottom-left {
    content: "Plan stratégique Mad Makers · Confidentiel · à Goudet Abalé · 2026";
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

p { margin: 0 0 0.6em 0; text-align: justify; }
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
  padding: 32mm 22mm;
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
h1.page-h1 {
  font-size: 26pt;
  margin-bottom: 5mm;
  line-height: 1.1;
}
.lead {
  font-size: 11pt;
  line-height: 1.5;
  color: #3a3d36;
  max-width: 160mm;
  margin-bottom: 5mm;
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
.callout.green {
  background: rgba(45,154,95,0.06);
  border-left-color: #2d9a5f;
}
.callout.green h4 { color: #2d9a5f; }
.callout.red {
  background: rgba(196,60,42,0.04);
  border-left-color: #c43c2a;
}
.callout.red h4 { color: #c43c2a; }
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

/* ===== STAT BLOCKS ===== */
.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 5mm;
  margin: 6mm 0;
}
.stats-row.cols-4 { grid-template-columns: repeat(4, 1fr); }
.stat {
  background: #ebe7dc;
  padding: 5mm;
  border-radius: 3mm;
  border-top: 3px solid #e0541b;
  page-break-inside: avoid;
}
.stat-num {
  font-family: 'Inter', sans-serif;
  font-size: 22pt;
  font-weight: 700;
  color: #e0541b;
  letter-spacing: -0.025em;
  line-height: 1;
  margin-bottom: 2mm;
}
.stat-label {
  font-size: 9pt;
  color: #1a1c18;
  line-height: 1.4;
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
  font-size: 9pt;
}
table.ref-table td.label {
  font-weight: 600;
  color: #0a0a0a;
  width: 35%;
}
table.ref-table td.amount {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
  text-align: right;
}
table.ref-table td.highlight {
  background: rgba(224,84,27,0.08);
  color: #e0541b;
  font-weight: 700;
}
table.ref-table tr:nth-child(even) td:not(.highlight) {
  background: #ebe7dc;
}
table.ref-table tfoot td {
  background: #0a0a0a;
  color: #fff;
  font-weight: 700;
}

/* ===== ROLE CARD ===== */
.role-card {
  background: #fafaf7;
  border: 1px solid #d5d2c9;
  border-left: 3px solid #e0541b;
  padding: 5mm 6mm;
  margin-bottom: 5mm;
  border-radius: 0 2mm 2mm 0;
  page-break-inside: avoid;
}
.role-card h4 {
  font-size: 13pt;
  margin-bottom: 1mm;
  color: #0a0a0a;
}
.role-card .perimetre {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9pt;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #e0541b;
  margin-bottom: 4mm;
  font-weight: 600;
}
.role-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.role-card li {
  font-size: 9.5pt;
  line-height: 1.55;
  margin-bottom: 1.5mm;
  padding-left: 5mm;
  position: relative;
  color: #1a1c18;
  text-align: left;
}
.role-card li::before {
  content: "·";
  position: absolute;
  left: 0;
  top: -2mm;
  color: #e0541b;
  font-size: 16pt;
  font-weight: 700;
  line-height: 1;
}
.role-card .charge {
  margin-top: 4mm;
  font-size: 9pt;
  color: #5a5d56;
  font-style: italic;
  border-top: 1px dashed #d5d2c9;
  padding-top: 3mm;
}
.role-card .charge::before {
  content: "Charge hebdomadaire estimée : ";
  font-weight: 600;
  color: #0a0a0a;
  font-style: normal;
}

/* ===== RISQUE CARD ===== */
.risque-card {
  background: #fafaf7;
  border: 1px solid #d5d2c9;
  border-left: 3px solid #c43c2a;
  padding: 5mm 6mm;
  margin-bottom: 5mm;
  border-radius: 0 2mm 2mm 0;
  page-break-inside: avoid;
}
.risque-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3mm;
  border-bottom: 1px solid #ebe7dc;
  padding-bottom: 2mm;
}
.risque-card h4 {
  font-size: 12pt;
  color: #0a0a0a;
  line-height: 1.2;
  flex: 1;
}
.risque-meta {
  display: flex;
  gap: 4mm;
  font-family: 'JetBrains Mono', monospace;
  font-size: 8pt;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.risque-meta span {
  padding: 2px 7px;
  border-radius: 99px;
  font-weight: 600;
}
.risque-meta .proba-ELEVÉE,
.risque-meta .impact-MAJEUR { background: rgba(196,60,42,0.15); color: #c43c2a; }
.risque-meta .proba-MOYENNE,
.risque-meta .impact-MOYEN { background: rgba(224,84,27,0.15); color: #e0541b; }
.risque-meta .proba-FAIBLE,
.risque-meta .impact-MINEUR { background: rgba(45,154,95,0.15); color: #2d9a5f; }
.risque-card .desc {
  font-size: 9.5pt;
  line-height: 1.55;
  margin-bottom: 3mm;
  color: #1a1c18;
}
.risque-card .mitigation {
  font-size: 9.5pt;
  line-height: 1.55;
  background: rgba(45,154,95,0.06);
  padding: 3mm 4mm;
  border-left: 2px solid #2d9a5f;
  border-radius: 0 2mm 2mm 0;
  color: #1a1c18;
}
.risque-card .mitigation::before {
  content: "MITIGATION · ";
  font-family: 'JetBrains Mono', monospace;
  font-size: 8pt;
  letter-spacing: 0.08em;
  color: #2d9a5f;
  font-weight: 700;
}

/* ===== DECISION CARD ===== */
.decision-card {
  background: #fff;
  border: 1px solid #d5d2c9;
  padding: 5mm 6mm;
  margin-bottom: 6mm;
  border-radius: 3mm;
  position: relative;
  page-break-inside: avoid;
}
.decision-card::before {
  content: "";
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 4mm;
  background: #e0541b;
  border-radius: 3mm 0 0 3mm;
}
.decision-head {
  display: flex;
  align-items: baseline;
  gap: 4mm;
  margin-bottom: 4mm;
  padding-bottom: 3mm;
  border-bottom: 1px solid #ebe7dc;
}
.decision-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10pt;
  color: #e0541b;
  font-weight: 700;
  letter-spacing: 0.06em;
}
.decision-titre {
  font-size: 13pt;
  font-weight: 600;
  color: #0a0a0a;
  line-height: 1.2;
}
.decision-options {
  list-style: none;
  padding: 0;
  margin: 0 0 4mm 0;
}
.decision-options li {
  font-size: 9.5pt;
  line-height: 1.55;
  margin-bottom: 2.5mm;
  padding-left: 6mm;
  position: relative;
  color: #1a1c18;
  text-align: left;
}
.decision-options li::before {
  content: "☐";
  position: absolute;
  left: 0;
  top: 0;
  color: #e0541b;
  font-size: 11pt;
}
.decision-reco {
  background: rgba(45,154,95,0.06);
  border-left: 2px solid #2d9a5f;
  padding: 3mm 4mm;
  border-radius: 0 2mm 2mm 0;
  font-size: 9.5pt;
  line-height: 1.55;
}
.decision-reco::before {
  content: "Recommandation · ";
  font-family: 'JetBrains Mono', monospace;
  font-size: 8pt;
  letter-spacing: 0.08em;
  color: #2d9a5f;
  font-weight: 700;
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
"""

# ===========================================================
# RENDER FUNCTIONS
# ===========================================================

def render_cover():
    return """
<section class="bleed cover">
  <div class="cover-top">
    <span class="badge">Plan stratégique · Confidentiel · à Goudet</span>
    <h1>Mad Makers<br>2026.</h1>
    <p class="sub">Plan stratégique pour valider la direction Carnet Plein®, cadrer notre engagement mutuel, et challenger ensemble ce que nous pouvons construire à 2.</p>
  </div>
  <div class="cover-meta">
    <div>
      <div class="accent-line"></div>
      Document V1 - Rayan Mpondo (Maïck) à Goudet Abalé
    </div>
    <div>Mai 2026</div>
  </div>
</section>
"""


def render_avant_propos():
    return """
<section class="page">
  <div class="eyebrow">Avant-propos pour Goudet</div>
  <h1 class="page-h1">Pourquoi je t'envoie ce document.</h1>

  <p class="lead">Salut Goudet, on en parle depuis quelques mois mais sans jamais avoir mis les choses à plat. Voici ce que j'ai construit ces dernières semaines sur Carnet Plein®, où on en est, et surtout les questions sur lesquelles j'ai besoin de toi.</p>

  <p>Ce document a trois objectifs, dans cet ordre :</p>

  <div class="callout">
    <h4>Objectif 01 : valider la direction</h4>
    <p>Le système Carnet Plein® est techniquement prêt (site, contrat, playbook, Calendly, CRM, bonus livrables). Avant de commencer à prospecter pour de vrai, j'ai besoin que tu me dises si la direction te paraît saine, ou si tu vois des trous que je ne vois plus à force d'être dans le détail.</p>
  </div>

  <div class="callout">
    <h4>Objectif 02 : décider de ton engagement</h4>
    <p>Tu es co-fondateur Mad Makers, je sais que tu as ta vie à côté. Carnet Plein® va consommer du temps, des décisions, possiblement du capital. Avant que je signe le premier client, on doit poser ton niveau d'engagement (temps, responsabilités, rémunération, parts) en toute transparence. C'est le sujet de la section « Équipe » et des décisions à prendre.</p>
  </div>

  <div class="callout">
    <h4>Objectif 03 : challenger le plan</h4>
    <p>Je préfère me prendre une bonne soufflante de ta part maintenant qu'un retour client négatif dans 6 mois. Si quelque chose te semble fragile ou faux, dis-le. La section « Risques » est volontairement la plus longue : c'est là qu'on doit s'écouter le plus.</p>
  </div>

  <p style="margin-top:6mm">Le document fait une trentaine de pages. Tu peux le lire d'un trait (~45 min) ou par sections selon ce qui t'intéresse. À la fin, il y a sept décisions concrètes que je propose qu'on aborde ensemble en visio dédiée d'1h30.</p>

  <p>Merci d'avance pour ton temps.</p>
  <p>- Rayan</p>
</section>
"""


def render_vue_ensemble():
    return """
<section class="page">
  <div class="eyebrow">Vue d'ensemble</div>
  <h1 class="page-h1">L'architecture Mad Makers en 2026.</h1>

  <p class="lead">Mad Makers, c'est aujourd'hui trois activités liées par la même marque parente, avec des niveaux de maturité différents.</p>

  <div class="callout dark">
    <h4>1. Mad Makers (marque parent) - <code>mad-makers.fr</code></h4>
    <p>Agence web créative généraliste basée à Paris. Portfolio de projets passés (papiche, riot, sophie-marchand entre autres). C'est notre vitrine identitaire, mais ce n'est pas un moteur d'acquisition direct. À maintenir en veille active sur year 1, à monter en gamme year 2.</p>
  </div>

  <div class="callout">
    <h4>2. L'Accélérateur Carnet Plein® - <code>carnetplein.mad-makers.fr</code></h4>
    <p>Notre première offre verticale productisée. Cible : plombiers-chauffagistes en Île-de-France, Hauts-de-France et Grand Est. Tarif : 5 000 € HT setup + 800 €/mois sur 12 mois (~13 800 € HT par contrat). Format : cohort de 3 artisans / mois, livraison du bundle complet en 14 jours, garantie de continuité gratuite si objectif non atteint. <strong>C'est le focus principal des 12 prochains mois.</strong></p>
  </div>

  <div class="callout dark">
    <h4>3. Le CRM Mad Makers - infrastructure interne</h4>
    <p>Outil de prospection sortante développé en interne. Flask + SQLite/Postgres, multi-user, déployé sur Render. Base de 500 prospects déjà importés (RocketReach), briefing live cold call avec ROI calculator, campagnes email via Resend (RGPD compliant), pipeline kanban. <strong>C'est notre avantage compétitif sur l'acquisition pour Carnet Plein®.</strong> Détails en section dédiée.</p>
  </div>

  <h3 style="margin-top:8mm;font-size:14pt;">Pourquoi cette architecture en trois niveaux ?</h3>

  <p>Mad Makers en tant que marque-parent reste flexible : on garde la capacité d'ouvrir d'autres niches (Carnet Plein® version restaurants, version artisans autres métiers, etc.) sous la même bannière. Le CRM est mutualisé et peut servir toutes les futures verticales.</p>

  <p>Carnet Plein® est notre <strong>preuve de concept</strong> year 1 : si on tient nos engagements opérationnels, nos garanties, et nos KPI internes (NPS, rétention, marge), on a un produit reproductible que l'on peut soit scaler dans la niche, soit dupliquer dans une autre verticale en year 2-3.</p>
</section>
"""


def render_marche():
    return """
<section class="page">
  <div class="eyebrow">Le marché et le problème</div>
  <h1 class="page-h1">Pourquoi les plombiers-chauffagistes,<br>pourquoi maintenant.</h1>

  <p class="lead">Choix de la niche : il y a en France environ 50 000 entreprises de plomberie-chauffage (source : INSEE, code APE 4322A et 4322B). Marché stable, fragmenté, vieillissant.</p>

  <div class="stats-row">
    <div class="stat">
      <div class="stat-num">50 000</div>
      <div class="stat-label">entreprises de plomberie-chauffage en France (INSEE 2024)</div>
    </div>
    <div class="stat">
      <div class="stat-num">68%</div>
      <div class="stat-label">de ces entreprises ont moins de 5 salariés (TPE-cible)</div>
    </div>
    <div class="stat">
      <div class="stat-num">~12 000</div>
      <div class="stat-label">entreprises dans nos 3 régions cibles (IDF + HDF + GE)</div>
    </div>
  </div>

  <h3 style="margin-top:6mm;font-size:13pt;">Les 5 douleurs documentées du persona</h3>

  <p>Synthétisées depuis le rapport stratégique v2 inspiré de Hormozi, et corroborées par les études FFB, CAPEB et Effectif Marketing 2024-2025.</p>

  <table class="ref-table">
    <thead>
      <tr><th style="width:30%;">Douleur</th><th>Manifestation concrète</th></tr>
    </thead>
    <tbody>
      <tr>
        <td class="label">Carnet de commandes en dents de scie</td>
        <td>Périodes de sur-charge (urgences hiver) puis trous en intersaison. Pas de prévisibilité.</td>
      </tr>
      <tr>
        <td class="label">Visibilité Google quasi-nulle</td>
        <td>Fiche GBP médiane à 11 photos, peu d'avis, descriptions pauvres. Concurrence des grosses enseignes (Boulanger, Engie) qui captent le trafic local.</td>
      </tr>
      <tr>
        <td class="label">Time-poor sur la partie digitale</td>
        <td>L'artisan est sur chantier 8-10h/jour. Le soir, il fait les devis. Le digital passe en dernier, donc jamais.</td>
      </tr>
      <tr>
        <td class="label">Méfiance face aux agences web</td>
        <td>Promesses non tenues, contrats à rallonge, factures imprévues. Le mot « marketing » est péjoratif.</td>
      </tr>
      <tr>
        <td class="label">Plafond de croissance technique</td>
        <td>Pas le réflexe d'augmenter les prix ni de filtrer les clients. Donc travaillent beaucoup pour peu de marge.</td>
      </tr>
    </tbody>
  </table>

  <div class="callout">
    <h4>Pourquoi 3 régions et pas la France entière</h4>
    <p>Île-de-France, Hauts-de-France et Grand Est représentent ~24% des entreprises du secteur. Couvertes par une seule personne (Rayan) en délivrance, c'est tenable. Concentration géographique : on peut visiter physiquement les 3 premiers clients en 1 journée si besoin. La France entière, c'est pour year 2-3 et avec une équipe.</p>
  </div>
</section>
"""


def render_solution():
    return """
<section class="page">
  <div class="eyebrow">La solution Carnet Plein®</div>
  <h1 class="page-h1">Six composants, une cohort,<br>une garantie unique.</h1>

  <p class="lead">L'offre est conçue selon les principes Hormozi de Grand Slam Offer : valeur perçue maximale, friction d'achat minimale, garantie qui change la perception du risque.</p>

  <h3 style="font-size:13pt;margin-top:5mm;">Les 6 composants opérationnels</h3>

  <table class="ref-table">
    <thead><tr><th style="width:35%;">Composant</th><th>Description courte</th></tr></thead>
    <tbody>
      <tr><td class="label">01. Site web professionnel</td><td>Création, hébergement, maintenance. Stack Vercel + Cloudflare R2.</td></tr>
      <tr><td class="label">02. Google Business Profile</td><td>Audit 12 points, optimisation, Google Posts hebdo, suivi métriques.</td></tr>
      <tr><td class="label">03. Système d'avis automatisé</td><td>Lien personnalisé + SMS post-chantier + réponses templates 5★ à 1★.</td></tr>
      <tr><td class="label">04. Reporting mensuel</td><td>PDF 4-6 pages envoyé le 5 du mois, métriques GBP + GA4 + actions menées.</td></tr>
      <tr><td class="label">05. Gestion des photos chantiers</td><td>Récupération WhatsApp, retouche Snapseed, upload GBP + Google Posts.</td></tr>
      <tr><td class="label">06. Accompagnement (1:1 + cohort)</td><td>Visio mensuelle individuelle + kick-off groupé + visio cohort mensuelle + WhatsApp group privé.</td></tr>
    </tbody>
  </table>

  <h3 style="font-size:13pt;margin-top:6mm;">La cohort light (notre différenciation)</h3>

  <p>3 artisans démarrent le même 1er lundi du mois. Ils se rencontrent en kick-off groupé visio de 60 min, puis se retrouvent tous les 1ers mardis du mois en visio cohort de 45 min (animée par Rayan en facilitateur). Entre les visios, un WhatsApp group privé entre les 3 artisans et Rayan permet l'entraide rapide.</p>

  <p>Règle Chatham House : ce qui se dit dans la cohort reste dans la cohort. Documenté dans le contrat (art. 03).</p>

  <p><strong>Valeur pour le client :</strong> sortir de l'isolement de l'artisan solo, accountability mensuelle, possibilité de partage de leads entre métiers complémentaires, validation sociale de l'investissement.</p>

  <p><strong>Valeur pour Mad Makers :</strong> taux de rétention boosté (Hormozi : x2 à x3 vs 1:1 pur), pricing power justifié, réduction du temps répétitif (on explique 1 fois pour 3), bouche-à-oreille structuré entre artisans.</p>

  <h3 style="font-size:13pt;margin-top:6mm;">Les 4 bonus livrables (PDF remis à la signature)</h3>

  <ul>
    <li><strong>Bonus #1 - Fiche Google Parfaite :</strong> checklist 12 points pour optimiser une fiche GBP en autonomie</li>
    <li><strong>Bonus #2 - 30 Réponses Prêtes à l'Emploi :</strong> templates de réponses aux avis Google (5★ à 1★ + avis injustes)</li>
    <li><strong>Bonus #3 - Photos qui Vendent :</strong> 5 règles smartphone pour photographier les chantiers</li>
    <li><strong>Bonus #4 - Le Devis qui Close à 70% :</strong> template Cialdini + 8 objections + relances structurées, conforme légal 2026</li>
  </ul>

  <h3 style="font-size:13pt;margin-top:6mm;">Les 2 garanties (notre marqueur anti-bullshit)</h3>

  <div class="callout">
    <h4>Garantie Carnet Plein® - continuité gratuite</h4>
    <p>Si à 12 mois l'objectif KPI défini au brief n'est pas atteint à 80%, et sous réserve que le client ait respecté ses engagements de réactivité et de fourniture de photos, le Prestataire poursuit la prestation <strong>sans facturer de retainer supplémentaire</strong>, jusqu'à atteinte de l'objectif (max 6 mois supplémentaires).</p>
  </div>

  <div class="callout">
    <h4>Garantie qualité d'exécution à 90 jours</h4>
    <p>Si à 90 jours le client constate de manière motivée que la qualité d'exécution ou la communication n'est pas conforme, le Prestataire offre <strong>1 mois de retainer additionnel gratuit</strong> en fin de contrat. Sans question, sans condition.</p>
  </div>

  <p>Les deux garanties sont des <strong>obligations de moyens renforcées</strong> au sens de l'article 1231-1 du Code civil. Jamais d'obligation de résultats sur des indicateurs commerciaux dépendants de facteurs extérieurs. Conformité totale au droit français.</p>
</section>
"""


def render_modele_economique():
    rows_cons = "".join(
        f"<tr><td class='label'>Mois {m['mois']}</td><td class='amount'>{m['actifs']}</td><td class='amount'>{m['setup']:,} €</td><td class='amount'>{m['mrr']:,} €</td><td class='amount highlight'>{m['total_ht']:,} €</td></tr>".replace(",", " ")
        for m in SCENARIO_CONSERVATIVE
    )
    rows_rea = "".join(
        f"<tr><td class='label'>Mois {m['mois']}</td><td class='amount'>{m['actifs']}</td><td class='amount'>{m['setup']:,} €</td><td class='amount'>{m['mrr']:,} €</td><td class='amount highlight'>{m['total_ht']:,} €</td></tr>".replace(",", " ")
        for m in SCENARIO_REALISTE
    )

    charges_rows = "".join(
        f"<tr><td class='label'>{cat}</td><td class='amount'>{amt:,} €</td></tr>".replace(",", " ")
        for cat, amt in CHARGES_EXTERNES.items()
    )

    return f"""
<section class="page">
  <div class="eyebrow">Modèle économique</div>
  <h1 class="page-h1">Combien on facture,<br>combien on garde.</h1>

  <p class="lead">Tarif unitaire : <strong>5 000 € HT setup + 800 € HT/mois</strong> sur 12 mois fermes, soit <strong>13 800 € HT par contrat</strong>. TVA 20% B2B reversée à l'État. Paiement en 3× sans frais ou 6× avec 2% d'agios.</p>

  <h3 style="font-size:13pt;">Scénario conservateur - 2 signatures par mois</h3>

  <table class="ref-table">
    <thead>
      <tr><th>Mois</th><th>Clients actifs cumul.</th><th>Setup encaissé</th><th>MRR encaissé</th><th>Total HT mois</th></tr>
    </thead>
    <tbody>{rows_cons}</tbody>
    <tfoot>
      <tr><td class="label">TOTAL ANNÉE 1</td><td>{SCENARIO_CONSERVATIVE[-1]['actifs']}</td><td colspan="2"></td><td class="amount">{TOTAL_CONS:,} €</td></tr>
    </tfoot>
  </table>

  <p style="margin-top:3mm;font-size:9pt;color:#5a5d56;">MRR fin year 1 : {MRR_12_CONS:,} € HT/mois récurrent.</p>

  <h3 style="font-size:13pt;margin-top:6mm;">Scénario réaliste - 3 signatures par mois</h3>

  <table class="ref-table">
    <thead>
      <tr><th>Mois</th><th>Clients actifs cumul.</th><th>Setup encaissé</th><th>MRR encaissé</th><th>Total HT mois</th></tr>
    </thead>
    <tbody>{rows_rea}</tbody>
    <tfoot>
      <tr><td class="label">TOTAL ANNÉE 1</td><td>{SCENARIO_REALISTE[-1]['actifs']}</td><td colspan="2"></td><td class="amount">{TOTAL_REA:,} €</td></tr>
    </tfoot>
  </table>

  <p style="margin-top:3mm;font-size:9pt;color:#5a5d56;">MRR fin year 1 : {MRR_12_REA:,} € HT/mois récurrent.</p>
</section>

<section class="page">
  <div class="eyebrow">Charges et marge</div>
  <h1 class="page-h1">Combien il reste après<br>les dépenses externes.</h1>

  <h3 style="font-size:13pt;">Charges externes annuelles estimées (HT)</h3>

  <table class="ref-table">
    <thead><tr><th style="width:60%;">Poste</th><th>Montant HT/an</th></tr></thead>
    <tbody>{charges_rows}</tbody>
    <tfoot>
      <tr><td class="label">TOTAL CHARGES EXTERNES</td><td class="amount">{TOTAL_CHARGES_EXT:,} €</td></tr>
    </tfoot>
  </table>

  <h3 style="font-size:13pt;margin-top:6mm;">Marge brute year 1 (avant rémunérations associés)</h3>

  <table class="ref-table">
    <thead><tr><th style="width:50%;">Scénario</th><th>CA HT year 1</th><th>Marge brute après charges</th></tr></thead>
    <tbody>
      <tr><td class="label">Conservateur (2 sign./mois)</td><td class="amount">{TOTAL_CONS:,} €</td><td class="amount highlight">{TOTAL_CONS - TOTAL_CHARGES_EXT:,} €</td></tr>
      <tr><td class="label">Réaliste (3 sign./mois)</td><td class="amount">{TOTAL_REA:,} €</td><td class="amount highlight">{TOTAL_REA - TOTAL_CHARGES_EXT:,} €</td></tr>
    </tbody>
  </table>

  <div class="callout">
    <h4>Ce qui n'est PAS dans ces chiffres</h4>
    <p>(1) <strong>Charges sociales URSSAF</strong> : ~22% du résultat en EI Sara, ou différent en SAS/SARL. À discuter avec expert-comptable. (2) <strong>Impôts sur les bénéfices</strong> : IR si EI, IS si SAS/SARL (15% jusqu'à 42 500 €, puis 25%). (3) <strong>Salaire éventuel de Rayan et Goudet</strong> selon la structure choisie. (4) <strong>Coûts de recrutement</strong> si embauche en cours d'année (chargé de projet à temps partiel ~ 1 500-2 000 €/mois chargé).</p>
  </div>

  <div class="callout dark">
    <h4>Lecture de ces chiffres</h4>
    <p>Les marges affichées sont des <strong>marges brutes opérationnelles</strong>, pas des marges nettes après tout (salaires, charges sociales, impôts). En SAS avec deux associés rémunérés modestement (Rayan 2 000 €/mois brut, Goudet 1 000 €/mois brut) + charges sociales, on retire environ 60 000 €/an de coût salarial chargé. Reste à arbitrer entre dividendes year 1 ou réinvestissement intégral.</p>
  </div>

  <p style="margin-top:6mm">Au-delà de l'aspect chiffré pur, la vraie variable c'est la <strong>marge horaire effective</strong>. Cible : >= 80 € HT / heure travaillée. À 24 clients actifs avec 5h/sem chacun = 120h/sem = impossible en solo. C'est le déclic du recrutement.</p>
</section>
"""


def render_acquisition():
    return """
<section class="page">
  <div class="eyebrow">Stratégie d'acquisition</div>
  <h1 class="page-h1">Trois canaux, dans cet ordre.</h1>

  <p class="lead">Pour les 6 premiers mois, on combine trois canaux d'acquisition avec des intensités différentes selon les phases.</p>

  <h3 style="font-size:13pt;">Canal 01 - Réseau personnel et parrainage (mois 1-3)</h3>

  <p>Pour les 3 premiers clients pilotes, on s'appuie sur notre réseau direct : artisans connus, contacts CAPEB, anciens clients Mad Makers, recommandations d'amis. Conversion attendue ~30-50%, taux d'engagement plus élevé que cold, témoignages obtenus plus facilement, tolérance plus grande sur les ratés du démarrage.</p>

  <p><strong>Tactique :</strong> 1 message LinkedIn personnel à chacun de nos contacts pertinents (~50 personnes au total), proposition d'une « place pilote Carnet Plein® avec tarif préférentiel » (par exemple 3 500 € setup au lieu de 5 000 € pour les 3 premiers) en échange de témoignages publics et de cas d'études détaillés à publier.</p>

  <h3 style="font-size:13pt;margin-top:5mm;">Canal 02 - Prospection sortante via le CRM (mois 1-12)</h3>

  <p>Notre <strong>CRM Mad Makers</strong> est l'asset central de ce canal (détails section suivante). Base de 500 prospects déjà importés, segmentés par catégorie (sans-site / veillot / récent) et par région.</p>

  <p><strong>Tactique :</strong> 10 appels qualifiés par semaine, briefing live avec le CRM (audit + ROI calculator + objections Belfort), suivis par séquence de relance email (3-4 emails sur 30 jours via Resend), bookings via le Calendly /audit-carnet-plein.</p>

  <p>Taux de conversion attendu : 5-10% d'appels qualifiés vers booking Calendly, 40% des bookings vers FIT, 60% des FIT vers signature = environ 1,2-2,4% appels → contrat.</p>

  <h3 style="font-size:13pt;margin-top:5mm;">Canal 03 - Inbound organique (mois 3-12)</h3>

  <p>Mise en place progressive d'une stratégie de visibilité long terme :</p>

  <ul>
    <li><strong>Blog SEO local</strong> : 1 article par mois ciblant des requêtes longue traîne (« comment optimiser sa fiche Google plombier 2026 », « TVA chaudière gaz 20% conséquences », « MaPrimeRénov' artisan »). Hébergé sur mad-makers.fr/blog. Objectif : 30-50 visites organiques/mois year 1.</li>
    <li><strong>LinkedIn personnel Rayan + Goudet</strong> : 2 posts par semaine chacun, contenu valeur (insights métier, retours d'expérience clients, partage des bonus PDF). Construction d'audience à 12 mois.</li>
    <li><strong>Bouche-à-oreille clients</strong> : à partir du mois 4-5, les premiers clients renvoient des recommandations. Tactique : un programme de parrainage explicite (1 mois de retainer offert au filleul ET au parrain pour chaque signature).</li>
  </ul>

  <div class="callout">
    <h4>Pas de publicité payante year 1</h4>
    <p>Google Ads, Meta Ads, LinkedIn Ads : exclus année 1. Pourquoi : (1) marge sur le premier client moins claire qu'il n'y paraît, brûler du cash en ads = risque, (2) on n'a pas encore d'attribution ni de funnel optimisé, (3) Hormozi-Sabri : maîtriser l'organique d'abord, le payant ne fait qu'amplifier ce qui marche déjà. Year 2 : éventuellement Google Ads sur les requêtes commerciales (« agence web plombier »).</p>
  </div>
</section>
"""


def render_crm():
    return """
<section class="page">
  <div class="eyebrow">Le CRM Mad Makers</div>
  <h1 class="page-h1">L'asset qui change tout<br>côté prospection.</h1>

  <p class="lead">Le CRM Mad Makers (~/Desktop/MadMakers Prospection) est un outil interne développé en propre, déployé sur Render.com, qui couvre l'intégralité du cycle de prospection sortante. Sans cet outil, on prospectait à l'aveugle avec un tableur. Avec, on a un funnel structuré.</p>

  <h3 style="font-size:13pt;">Stack technique et infrastructure</h3>

  <ul>
    <li><strong>Backend :</strong> Python 3.12 + Flask 3, SQLite local pour dev + Postgres pour prod (script de migration prêt)</li>
    <li><strong>Frontend :</strong> Jinja2 templates + htmx (interactivité légère sans framework lourd) + CSS Mad Makers (noir + jaune chaud)</li>
    <li><strong>Hosting :</strong> Render.com free tier (sleeps après 15 min d'inactivité, 50s cold start, OK pour usage interne 1-2 utilisateurs)</li>
    <li><strong>Auth :</strong> Flask-Login avec session multi-user, whitelist par emails autorisés (Rayan + Goudet + futurs collaborateurs)</li>
    <li><strong>Email :</strong> intégration Resend pour envoi transactionnel et bulk (RGPD compliant, hébergement UE, unsubscribe automatique)</li>
    <li><strong>AI :</strong> intégration prête pour drafting d'emails personnalisés (variable selon prospect)</li>
  </ul>

  <h3 style="font-size:13pt;margin-top:5mm;">Les 8 fonctionnalités opérationnelles</h3>

  <table class="ref-table">
    <thead><tr><th style="width:30%;">Fonctionnalité</th><th>Description</th></tr></thead>
    <tbody>
      <tr><td class="label">01. Dashboard KPI</td><td>500 prospects par catégorie/stage, calls de la semaine, RDV 2 calés, payback moyen.</td></tr>
      <tr><td class="label">02. Prospects (table)</td><td>Table filtrable par catégorie / stage / ville, recherche en live, bouton « 📞 cold call » direct (téléphone cliquable tel:).</td></tr>
      <tr><td class="label">03. Prospect Detail</td><td>Identité éditable, audit site en live, timeline complète des interactions, notes.</td></tr>
      <tr><td class="label">04. Briefing live cold call</td><td>Audit factuel du site, arguments financiers, questions découverte (4 thèmes), pain points cochables, ROI calculator interactif (gain mensuel + payback + verdict couleur), future pacing, demande visuels, pitch RDV 2 (assumed close Belfort), objections (Loop : Agree → Bridge → Reinforce → Close), closing patterns, save direct DB.</td></tr>
      <tr><td class="label">05. Pipeline kanban</td><td>Drag & drop pour changer le stage : a_contacter → email_envoyé → en_relance → rdv_1_calé → rdv_1_fait → rdv_2_calé → rdv_2_fait → devis_envoyé → signé (ou perdu/dormant).</td></tr>
      <tr><td class="label">06. Activités</td><td>RDV à venir, relances dues, timeline complète des interactions par prospect.</td></tr>
      <tr><td class="label">07. Email templates</td><td>Création / édition / archivage de templates email avec variables. Render preview avant envoi. AI drafting en option.</td></tr>
      <tr><td class="label">08. Campagnes email</td><td>Séquences multi-étapes avec délais, assignation à prospects, suivi des ouvertures et désinscriptions. Conformité RGPD avec lien d'unsubscribe automatique.</td></tr>
    </tbody>
  </table>

  <h3 style="font-size:13pt;margin-top:5mm;">Coût du CRM</h3>

  <p>Hosting Render.com free tier : <strong>0 € / mois</strong> (limite : sleeps après 15 min, cold start 50s acceptable pour 1-2 users).</p>
  <p>Resend API : free jusqu'à 3 000 emails/mois, ensuite ~20 € / mois pour 50 000 emails.</p>
  <p>Base prospects RocketReach : déjà importée, coût zero à ce stade.</p>
  <p>Migration Postgres si scaling : 7 €/mois Render Postgres starter, ou 0 € Supabase free tier.</p>

  <div class="callout green">
    <h4>Pourquoi c'est un asset stratégique</h4>
    <p>Construit en interne, le CRM est <strong>notre propriété et notre différenciation</strong>. Les concurrents qui utilisent Pipedrive ou HubSpot à 50-100 €/mois ont moins de feature spécifiques (notre briefing live cold call est unique). Nous pouvons ajouter ou retirer des fonctionnalités au gré de nos apprentissages, sans dépendance fournisseur. À terme : possibilité de le revendre en SaaS aux autres agences si on en a envie (mais pas dans la roadmap year 1).</p>
  </div>

  <div class="callout">
    <h4>Améliorations à venir (next iterations)</h4>
    <p>(1) Intégration Calendly OAuth pour caler RDV depuis le CRM. (2) Auto-génération du mail récap post-call. (3) Multi-user complet avec rôles (owner / sales / admin). (4) Mode mobile responsive avancé. (5) Génération de campaigns AI à partir d'un brief court. Roadmap interne, pas bloquant pour démarrer la prospection.</p>
  </div>
</section>
"""


def render_operations():
    return """
<section class="page">
  <div class="eyebrow">Opérations</div>
  <h1 class="page-h1">Comment on livre concrètement.</h1>

  <p class="lead">Le playbook de livraison interne (<code>process-livraison/playbook-livraison-carnet-plein.html</code>) documente chaque étape, chaque outil, chaque template. Synthèse ici.</p>

  <h3 style="font-size:13pt;">Capacité opérationnelle (le vrai goulot)</h3>

  <p>Solo, Rayan peut livrer durablement <strong>5 à 8 clients actifs en régime de croisière</strong>, soit ~25-40h/sem sur la livraison (5h/sem/client). En période de delivery initiale (14 jours), il peut absorber jusqu'à <strong>3 clients en parallèle simultanément</strong> (= 1 cohort).</p>

  <p>Au-delà : retards, qualité dégradée, garantie de continuité déclenchée, churn. <strong>C'est la contrainte numéro 1 pour scaler.</strong> Cf. risques section 14.</p>

  <h3 style="font-size:13pt;margin-top:5mm;">Timeline type J0 à J+14</h3>

  <table class="ref-table">
    <thead><tr><th style="width:25%;">Jalon</th><th>Action</th></tr></thead>
    <tbody>
      <tr><td class="label">D-7</td><td>Audit gratuit Calendly 20 min (qualification)</td></tr>
      <tr><td class="label">D-3</td><td>Envoi devis + contrat + questionnaire pré-kick-off</td></tr>
      <tr><td class="label">D0</td><td>Signature contrat + paiement setup + email bienvenue</td></tr>
      <tr><td class="label">J+1 à J+5</td><td>Récupération accès comptes (GBP, hébergeur, registrar)</td></tr>
      <tr><td class="label">J+7 matin</td><td>Kick-off groupé cohort 60 min visio (3 artisans + Rayan)</td></tr>
      <tr><td class="label">J+7 après-midi</td><td>3 visios 1:1 de 30 min (KPI individuels, planning)</td></tr>
      <tr><td class="label">J+8 à J+11</td><td>Customisation site web + audit/optimisation GBP</td></tr>
      <tr><td class="label">J+10 à J+12</td><td>Système avis automatisé en place</td></tr>
      <tr><td class="label">J+11</td><td>Briefing client photos chantiers + setup WhatsApp</td></tr>
      <tr><td class="label">J+13</td><td>Validation site avec chaque client (visio 30 min)</td></tr>
      <tr><td class="label">J+14</td><td>GO LIVE - bundle complet en service pour les 3 artisans</td></tr>
    </tbody>
  </table>

  <h3 style="font-size:13pt;margin-top:5mm;">Charge mensuelle en régime de croisière (post J+14)</h3>

  <p>Une fois le bundle livré, la charge se stabilise par client :</p>

  <ul>
    <li><strong>~5h / semaine / client</strong> en moyenne (photos, GBP, Posts, avis, support)</li>
    <li><strong>45 min de visio 1:1 mensuelle</strong> avec chaque client (le 15 du mois)</li>
    <li><strong>45 min de visio cohort mensuelle</strong> avec chaque cohort active (1er mardi du mois)</li>
    <li><strong>60 min de kick-off groupé</strong> pour chaque nouvelle cohort qui démarre</li>
    <li><strong>Reporting mensuel</strong> 4-6 pages PDF par client (le 5 du mois)</li>
    <li><strong>Modération WhatsApp cohort</strong> : 5-10 min par jour</li>
  </ul>

  <p>À 3 cohorts actives = 9 clients = 45h/sem dédiées à la livraison. Plus la prospection (10h/sem) + le pilotage interne (5h/sem) = ~60h/sem. Insoutenable. <strong>Trigger d'embauche.</strong></p>
</section>
"""


def render_equipe():
    cards_html = ""
    for r in ROLES_PROPOSES:
        resps_html = "".join(f"<li>{x}</li>" for x in r['responsabilites'])
        cards_html += f"""
<div class="role-card">
  <h4>{r['personne']}</h4>
  <div class="perimetre">{r['perimetre']}</div>
  <ul>{resps_html}</ul>
  <div class="charge">{r['charge_hebdo']}</div>
</div>
"""

    return f"""
<section class="page">
  <div class="eyebrow">Équipe et rôles</div>
  <h1 class="page-h1">Qui fait quoi (proposition).</h1>

  <p class="lead">Voici comment je propose qu'on découpe les responsabilités. Sujet ouvert : c'est précisément la décision 01 et 03 à prendre ensemble. Cette section sert de base de discussion, pas de plan acté.</p>

  {cards_html}

  <div class="callout">
    <h4>Ce que cette répartition implique</h4>
    <p>Rayan reste l'opérateur principal Carnet Plein® (delivery, brand, créa). Goudet apporte la dimension stratégique, financière et entrepreneuriale qui manque quand on est seul à tout porter. Sara reste exclusivement le porte-drapeau juridique. Cette répartition est viable pour year 1 et permet de monter en charge à 2 sans recruter immédiatement.</p>
  </div>

  <div class="callout red">
    <h4>Point d'attention juridique</h4>
    <p>Aujourd'hui, Rayan opère sous SIRET Sara sans statut formalisé. Si Goudet rejoint officiellement, cela <strong>doit</strong> s'accompagner d'une structure adaptée (création SAS / SASU, ou ajustement du statut de Rayan en sous-traitance déclarée, ou autre). Sinon : risque travail dissimulé (article L8221-1 du Code du travail). À résoudre AVANT le premier client. Cf. décision 02.</p>
  </div>
</section>
"""


def render_risques():
    cards = "".join(f"""
<div class="risque-card">
  <div class="risque-head">
    <h4>{r['nom']}</h4>
    <div class="risque-meta">
      <span class="proba-{r['proba']}">Probabilité : {r['proba']}</span>
      <span class="impact-{r['impact']}">Impact : {r['impact']}</span>
    </div>
  </div>
  <div class="desc">{r['description']}</div>
  <div class="mitigation">{r['mitigation']}</div>
</div>
""" for r in RISQUES)

    return f"""
<section class="page">
  <div class="eyebrow">Risques et mitigations</div>
  <h1 class="page-h1">Les 5 risques sur lesquels<br>on doit s'écouter.</h1>

  <p class="lead">Honnêtement, c'est la section la plus importante pour la décision finale. Si l'un de ces risques te paraît mal calibré ou ignoré, dis-le-moi avant la prospection.</p>

  {cards}
</section>
"""


def render_roadmap():
    return """
<section class="page">
  <div class="eyebrow">Roadmap 24 mois</div>
  <h1 class="page-h1">De la prospection au scale.</h1>

  <p class="lead">Découpée par trimestre, avec les jalons critiques.</p>

  <h3 style="font-size:13pt;">Trimestre 1 (mois 1 à 3) - Pilotage et premiers clients</h3>
  <ul>
    <li>Validation avec Goudet + structure juridique acté (SAS / autre)</li>
    <li>Contrat avocat relu, Calendly configuré, Stripe en place</li>
    <li>3 clients pilotes signés via réseau perso (tarif préférentiel)</li>
    <li>Première cohort démarre (mois 2 idéalement)</li>
    <li>CRM activement utilisé pour la prospection sortante (10 appels/sem)</li>
  </ul>

  <h3 style="font-size:13pt;margin-top:5mm;">Trimestre 2 (mois 4 à 6) - Premiers retours et ajustements</h3>
  <ul>
    <li>2 cohorts actives en parallèle (= 6 clients)</li>
    <li>Premier reporting NPS 90 jours avec les pilotes</li>
    <li>Itération sur les bonus livrables et le contrat selon retours terrain</li>
    <li>Premiers témoignages clients réels (vidéo si possible)</li>
    <li>Lancement du blog SEO sur mad-makers.fr</li>
  </ul>

  <h3 style="font-size:13pt;margin-top:5mm;">Trimestre 3 (mois 7 à 9) - Décision recrutement</h3>
  <ul>
    <li>3 cohorts actives en parallèle (= 9 clients), Rayan sature à 35-40h/sem</li>
    <li><strong>Décision recrutement</strong> : alternant chargé de projet, freelance, ou attente</li>
    <li>1 article SEO publié / mois, contenu LinkedIn structuré</li>
    <li>Première levée de fonds éventuelle si croissance ambitieuse (à arbitrer avec Goudet)</li>
  </ul>

  <h3 style="font-size:13pt;margin-top:5mm;">Trimestre 4 (mois 10 à 12) - Premier bilan</h3>
  <ul>
    <li>Bilan year 1 : CA réel, marge nette, NPS moyen, taux renouvellement attendu</li>
    <li>Première cohort arrive en fin de contrat (mois 12) : discussion renouvellement</li>
    <li>Décision sur l'ouverture d'une seconde niche year 2 (autres métiers BTP ? restaurants ? autres TPE ?)</li>
    <li>Si recrutement effectué : intégration, formation, premières délégations</li>
  </ul>

  <h3 style="font-size:13pt;margin-top:5mm;">Year 2 (mois 13 à 24) - Scale et diversification</h3>
  <ul>
    <li>Effectif cible : 2 à 4 personnes (Rayan + Goudet + 1 à 2 chargés de projet)</li>
    <li>30 à 50 clients actifs en parallèle (selon retention)</li>
    <li>Lancement d'une seconde verticale (Carnet Plein® version restaurants OU artisans autres métiers)</li>
    <li>Optionnel : publicité payante Google Ads sur requêtes commerciales</li>
    <li>Mise en place possible d'un programme d'affiliation</li>
  </ul>

  <div class="callout dark">
    <h4>Ce qui se passe si on ne tient pas la roadmap</h4>
    <p>Pas grave. Cette roadmap est ambitieuse mais pas catastrophique si on glisse de 3-6 mois. Le vrai signal d'alarme : pas de client signé au mois 4-5 (réseau perso pas converti + prospection CRM peu efficace). Si on est dans ce cas, on stoppe la prospection, on retravaille l'offre ou le positionnement, et on relance au mois 6.</p>
  </div>
</section>
"""


def render_decisions():
    cards = "".join(f"""
<div class="decision-card">
  <div class="decision-head">
    <span class="decision-num">DÉCISION {d['num']} / 07</span>
    <span class="decision-titre">{d['titre']}</span>
  </div>
  <ul class="decision-options">
    {"".join(f"<li>{opt}</li>" for opt in d['options'])}
  </ul>
  <div class="decision-reco">{d['recommandation']}</div>
</div>
""" for d in DECISIONS)

    return f"""
<section class="page">
  <div class="eyebrow">Décisions à prendre ensemble</div>
  <h1 class="page-h1">Sept décisions pour la visio<br>de validation avec Goudet.</h1>

  <p class="lead">Je propose qu'on bloque une visio de 90 minutes pour aborder ces 7 décisions une par une. Ma recommandation pour chacune est indiquée en vert, mais c'est ouvert au débat.</p>

  {cards}
</section>
"""


def render_annexes():
    return """
<section class="page">
  <div class="eyebrow">Annexes - liens vers les documents</div>
  <h1 class="page-h1">Tous les artefacts du projet.</h1>

  <p class="lead">Pour aller plus loin, voici les documents et outils déjà produits, accessibles localement ou en ligne.</p>

  <h3 style="font-size:13pt;">Site et infrastructure</h3>
  <ul>
    <li><strong>Site public :</strong> <code>https://carnetplein.mad-makers.fr</code></li>
    <li><strong>Site Mad Makers parent :</strong> <code>https://mad-makers.fr</code></li>
    <li><strong>Repo GitHub madmakers-pro :</strong> <code>github.com/directedbymaick/madmakers-pro</code></li>
    <li><strong>Repo GitHub CRM :</strong> <code>github.com/darthmaick/mad-makers-prospection</code> et mirror <code>github.com/directedbymaick/madmakers-prospection</code></li>
    <li><strong>Calendly audit :</strong> <code>https://calendly.com/directedbymaick/audit-carnet-plein</code></li>
  </ul>

  <h3 style="font-size:13pt;margin-top:5mm;">Documents internes produits</h3>
  <table class="ref-table">
    <thead><tr><th>Document</th><th>Localisation</th></tr></thead>
    <tbody>
      <tr><td class="label">Convention de prestation V1</td><td><code>contrat/contrat-garantie-carnet-plein.html</code></td></tr>
      <tr><td class="label">Playbook livraison interne</td><td><code>process-livraison/playbook-livraison-carnet-plein.html</code></td></tr>
      <tr><td class="label">Setup Calendly audit (config + emails)</td><td><code>process-livraison/setup-calendly-audit.md</code></td></tr>
      <tr><td class="label">Bonus #1 - Fiche Google Parfaite</td><td><code>bonus-deliverables/01-fiche-google-parfaite.pptx</code></td></tr>
      <tr><td class="label">Bonus #2 - 30 Réponses Avis Google</td><td><code>bonus-deliverables/02-30-reponses-avis-google.html</code></td></tr>
      <tr><td class="label">Bonus #3 - Photos qui Vendent</td><td><code>bonus-deliverables/03-photos-qui-vendent.html</code></td></tr>
      <tr><td class="label">Bonus #4 - Devis qui Close à 70%</td><td><code>bonus-deliverables/04-devis-close-70.html</code></td></tr>
      <tr><td class="label">Présent plan stratégique</td><td><code>business-plan/plan-strategique-mad-makers.html</code></td></tr>
    </tbody>
  </table>

  <h3 style="font-size:13pt;margin-top:5mm;">CRM Mad Makers</h3>
  <ul>
    <li><strong>Local :</strong> <code>~/Desktop/MadMakers Prospection/</code></li>
    <li><strong>Lancement local :</strong> <code>python -X utf8 -m crm.run</code> → <code>http://127.0.0.1:8000</code></li>
    <li><strong>Hosting :</strong> Render.com (configuration dans <code>render.yaml</code>)</li>
    <li><strong>Base prospects :</strong> 500 prospects RocketReach déjà importés en SQLite</li>
  </ul>

  <h3 style="font-size:13pt;margin-top:5mm;">Références stratégiques</h3>
  <ul>
    <li>Rapport stratégique v2 inspiré de Hormozi ($100M Offers) - source de vérité pour les décisions produit</li>
    <li>Études FFB / CAPEB sur le marché artisanal français 2024-2025</li>
    <li>BrightLocal Google My Business Insights Study 2024-2025</li>
    <li>Cialdini, <em>Influence</em> + <em>Pre-Suasion</em> (intégré dans le Bonus #4)</li>
  </ul>

  <div class="final-disclaimer">
    Plan stratégique V1 - mai 2026 - confidentiel - usage interne Mad Makers (Rayan, Goudet, Sara). Document à mettre à jour à minima à mi-année 1 (mois 6) et à fin year 1 (mois 12) avec les chiffres réels constatés. Les projections financières sont des estimations basées sur des hypothèses raisonnables mais non garanties : marge réelle dépendra du taux de conversion, du taux de churn, du temps moyen de livraison effectif, et des charges réelles facturées par le futur expert-comptable. Toute décision stratégique majeure (création de société, levée de fonds, recrutement) devra être validée par un expert-comptable et le cas échéant un avocat en droit des sociétés.
  </div>
</section>
"""


def render_html():
    parts = [
        render_cover(),
        render_avant_propos(),
        render_vue_ensemble(),
    ]

    parts.append("""
<section class="bleed section-sep">
  <div class="label">- Le marché et la solution</div>
  <h2>Qui sont nos clients,<br>et ce qu'on leur vend.</h2>
  <div class="count">Sections 04 à 05</div>
  <p class="desc">Cible plombiers-chauffagistes en IDF / HDF / GE, douleurs documentées, 6 composants + cohort + bonus + garantie unique sur le marché. Conformité légale française stricte (obligation de moyens, jamais résultat).</p>
</section>
""")

    parts.append(render_marche())
    parts.append(render_solution())

    parts.append("""
<section class="bleed section-sep">
  <div class="label">- Le business</div>
  <h2>Combien on facture,<br>comment on acquiert.</h2>
  <div class="count">Sections 06 à 09</div>
  <p class="desc">Tarif 5 000 € + 800 €/mois, deux scénarios chiffrés mois par mois, charges externes, marge brute. Trois canaux d'acquisition dans l'ordre : réseau perso, CRM prospection sortante, organique long-terme.</p>
</section>
""")

    parts.append(render_modele_economique())
    parts.append(render_acquisition())
    parts.append(render_crm())
    parts.append(render_operations())

    parts.append("""
<section class="bleed section-sep">
  <div class="label">- Équipe, risques, roadmap</div>
  <h2>Qui fait quoi,<br>ce qui peut casser,<br>où on va.</h2>
  <div class="count">Sections 10 à 13</div>
  <p class="desc">Répartition proposée entre Rayan opérateur, Goudet stratégie, Sara structure juridique. 5 risques honnêtement adressés. Roadmap 24 mois trimestre par trimestre.</p>
</section>
""")

    parts.append(render_equipe())
    parts.append(render_risques())
    parts.append(render_roadmap())

    parts.append("""
<section class="bleed section-sep">
  <div class="label">- À toi de jouer</div>
  <h2>Sept décisions à prendre<br>en visio de 90 minutes.</h2>
  <div class="count">Section 14</div>
  <p class="desc">De ton engagement à la structure juridique, en passant par la répartition économique et le scénario de croissance. Ma recommandation est notée pour chacune, mais c'est ouvert.</p>
</section>
""")

    parts.append(render_decisions())
    parts.append(render_annexes())

    body = "\n".join(parts)

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Plan stratégique Mad Makers - Confidentiel - à Goudet</title>
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
        "plan-strategique-mad-makers.html"
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
    print(f"     Pages estimees : ~32-35")
    print()
    print("PROCHAINE ETAPE :")
    print("  1. Ouvrir le .html dans Chrome")
    print("  2. Ctrl+P (Imprimer)")
    print("  3. Destination : Enregistrer au format PDF")
    print("  4. Marges : Aucune (le CSS gere)")
    print("  5. Cocher Graphiques d'arriere-plan")
    print("  6. Enregistrer sous : Plan strategique Mad Makers - V1.pdf")
    print()
    print("PRESENTATION A GOUDET :")
    print("  -> Envoyer le PDF + bloquer une visio de 90 minutes")
    print("  -> Ordre du jour : 7 decisions a aborder (section 14)")
