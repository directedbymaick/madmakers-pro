#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script - Convention de prestation
"L'Accelerateur Carnet Plein(R) by Mad Makers"
Modele V1 - A faire valider par avocat avant utilisation client.

Generates contrat-garantie-carnet-plein.html in this folder.
Open in Chrome -> File > Print > Save as PDF (A4 portrait).
"""
import os

# ===========================================================
# DATA - PARTIES (fixe pour le prestataire, placeholders client)
# ===========================================================

PRESTATAIRE = {
    "nom": "Sara Cankaya",
    "denomination": "Mad Makers",
    "forme": "Entreprise individuelle (EI)",
    "adresse": "6 rue Youri Gagarine, 93230 Romainville, France",
    "siret": "832 059 695 00029",
    "tva": "FR12 832 059 695",
    "ape": "7022Z",
    "email": "contact@mad-makers.fr",
    "telephone": "+33 1 89 72 44 98",
    "site": "https://www.mad-makers.fr",
    "service": "https://carnetplein.mad-makers.fr",
}

# ===========================================================
# DATA - 6 COMPOSANTS DU PERIMETRE
# ===========================================================

COMPOSANTS = [
    {
        "num": "01",
        "nom": "Site web professionnel",
        "details": [
            "Conception, design et developpement d'un site web vitrine optimise pour la conversion en demandes de devis qualifiees",
            "Hebergement sur infrastructure Vercel (UE, conforme RGPD), nom de domaine inclus pour la duree du contrat",
            "Maintenance technique : mises a jour de securite, monitoring uptime, sauvegardes automatiques quotidiennes",
            "Modifications mineures incluses (mise a jour de coordonnees, horaires, photos chantiers, prix indicatifs)",
        ],
    },
    {
        "num": "02",
        "nom": "Google Business Profile (fiche Google)",
        "details": [
            "Audit initial des 12 points cles de la fiche existante (ou creation complete si inexistante)",
            "Optimisation des categories, descriptions, attributs, zones desservies",
            "Mise en place des Google Posts hebdomadaires (1 a 2 publications par semaine, themes adaptes a la saison metier)",
            "Suivi mensuel des metriques GBP : impressions, recherches, appels, demandes d'itineraire",
        ],
    },
    {
        "num": "03",
        "nom": "Systeme d'avis Google automatise",
        "details": [
            "Mise en place d'un lien d'avis personnalise envoye au client final apres chaque chantier termine (SMS ou email)",
            "Mode de declenchement : declaratif par le client (formulaire interne) ou integration CRM si systeme tiers existant",
            "Reponses aux avis (positifs et negatifs) sous 48h ouvrees, avec validation prealable par le Client pour les avis sensibles",
        ],
    },
    {
        "num": "04",
        "nom": "Reporting mensuel",
        "details": [
            "Rapport mensuel transmis le 5 du mois pour le mois precedent, format PDF 4 a 6 pages",
            "Indicateurs suivis : trafic site web, conversions devis, metriques GBP, nouveaux avis recus, classement de la fiche sur les requetes cibles",
            "Synthese qualitative : actions menees, decisions prises, recommandations pour le mois en cours",
        ],
    },
    {
        "num": "05",
        "nom": "Gestion des photos chantiers",
        "details": [
            "Recuperation des photos brutes envoyees par le Client via WhatsApp ou email (2 a 3 chantiers par semaine recommandes)",
            "Retouche legere (recadrage, exposition, suppression d'elements parasites avec accord du Client)",
            "Upload sur la fiche GBP et le site web, categorisation et indexation",
            "Respect strict du droit a l'image : flouter systematiquement les visages, plaques d'immatriculation, courriers, donnees personnelles",
        ],
    },
    {
        "num": "06",
        "nom": "Accompagnement et coaching (incluant dimension cohort)",
        "details": [
            "1 point d'etape individuel mensuel en visioconference (45 minutes) entre le Prestataire et le Client",
            "Kick-off groupe le 1er lundi du mois de demarrage : visioconference de 60 minutes reunissant les 3 artisans de la cohort et le Prestataire (presentation mutuelle, presentation du programme, calage du KPI commun)",
            "1 visio cohort mensuelle de 45 minutes reunissant les 3 artisans de la cohort en cours et le Prestataire (partage des wins du mois, blocages, conseils croises entre pairs)",
            "Groupe WhatsApp prive entre les 3 artisans de la cohort et le Prestataire pour l'entraide rapide et l'animation legere (modere par le Prestataire, sans engagement de disponibilite 24/7)",
            "Acces a un canal de communication direct individuel (email, WhatsApp avec le Prestataire) pour les questions courantes, reponse sous 48h ouvrees",
            "Conseils strategiques sur les actions metier qui ne sont pas du ressort du Prestataire (devis, relances clients, RGE, etc.)",
            "4 bonus livrables remis a la signature : Fiche Google Parfaite (PDF), 30 Reponses Pretes a l'Emploi (PDF), Photos qui Vendent (PDF), Devis qui Close a 70% (PDF)",
        ],
    },
]

# ===========================================================
# CSS - reuse same charter as bonus #4
# ===========================================================

CSS = """
@page {
  size: A4 portrait;
  margin: 22mm 18mm 24mm 18mm;
  @bottom-left {
    content: "Convention Carnet Plein® by Mad Makers · Modèle V1 - à valider par avocat";
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

/* ===== WARNING PAGE ===== */
.warning-page {
  border: 2px solid #c43c2a;
  background: rgba(196,60,42,0.04);
  padding: 12mm 14mm;
  margin: 8mm 0;
  border-radius: 4mm;
  page-break-inside: avoid;
}
.warning-page h2 {
  font-size: 18pt;
  margin-bottom: 5mm;
  color: #c43c2a;
}
.warning-page p {
  font-size: 11pt;
  line-height: 1.6;
  color: #1a1c18;
  margin-bottom: 4mm;
}
.warning-page p:last-child { margin-bottom: 0; }

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

/* ===== TOC ===== */
.toc h1 {
  font-size: 26pt;
  margin-bottom: 8mm;
  line-height: 1.1;
}
.toc-list {
  list-style: none;
  padding: 0;
  margin: 0;
  counter-reset: toc-counter;
}
.toc-list li {
  counter-increment: toc-counter;
  font-size: 11pt;
  line-height: 1.5;
  padding: 3mm 0 3mm 14mm;
  border-bottom: 1px solid #ebe7dc;
  position: relative;
  color: #1a1c18;
}
.toc-list li::before {
  content: "Art. " counter(toc-counter, decimal-leading-zero);
  position: absolute;
  left: 0;
  top: 3mm;
  font-family: 'JetBrains Mono', monospace;
  font-size: 9pt;
  font-weight: 700;
  color: #e0541b;
  letter-spacing: 0.02em;
}

/* ===== PARTIES TABLE ===== */
.parties {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6mm;
  margin: 6mm 0;
}
.partie-card {
  background: #fafaf7;
  border: 1px solid #d5d2c9;
  border-left: 3px solid #e0541b;
  padding: 6mm 7mm;
  border-radius: 0 3mm 3mm 0;
}
.partie-card h3 {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9pt;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #e0541b;
  margin-bottom: 3mm;
  font-weight: 600;
}
.partie-card .nom {
  font-size: 13pt;
  font-weight: 600;
  color: #0a0a0a;
  margin-bottom: 2mm;
  line-height: 1.2;
}
.partie-card p {
  font-size: 9pt;
  line-height: 1.5;
  color: #3a3d36;
  margin-bottom: 1.5mm;
  text-align: left;
}
.partie-card p strong { color: #0a0a0a; }

/* ===== ARTICLE ===== */
.article {
  page-break-inside: avoid;
  margin-bottom: 8mm;
}
.article-header {
  display: flex;
  align-items: baseline;
  gap: 5mm;
  border-bottom: 2px solid #0a0a0a;
  padding-bottom: 3mm;
  margin-bottom: 5mm;
}
.article-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11pt;
  color: #e0541b;
  font-weight: 700;
  letter-spacing: 0.06em;
  flex-shrink: 0;
}
.article-title {
  font-size: 15pt;
  font-weight: 600;
  color: #0a0a0a;
  line-height: 1.2;
}
.article-body p {
  font-size: 10pt;
  line-height: 1.6;
  margin-bottom: 4mm;
}
.article-body ul, .article-body ol {
  padding-left: 6mm;
  margin: 3mm 0 4mm;
}
.article-body li {
  font-size: 10pt;
  line-height: 1.55;
  margin-bottom: 2mm;
  text-align: justify;
}
.article-body h4 {
  font-size: 11pt;
  margin: 5mm 0 2mm;
  color: #0a0a0a;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
}

/* ===== COMPOSANT (perimetre) ===== */
.composant {
  background: #fafaf7;
  border: 1px solid #d5d2c9;
  border-left: 3px solid #e0541b;
  padding: 4mm 5mm;
  margin-bottom: 4mm;
  border-radius: 0 2mm 2mm 0;
  page-break-inside: avoid;
}
.composant-head {
  display: flex;
  align-items: baseline;
  gap: 4mm;
  margin-bottom: 3mm;
}
.composant-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9pt;
  color: #e0541b;
  font-weight: 700;
  letter-spacing: 0.08em;
}
.composant-nom {
  font-size: 12pt;
  font-weight: 600;
  color: #0a0a0a;
  line-height: 1.2;
}
.composant ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.composant li {
  font-size: 9.5pt;
  line-height: 1.55;
  margin-bottom: 1.5mm;
  padding-left: 5mm;
  position: relative;
  color: #1a1c18;
  text-align: justify;
}
.composant li::before {
  content: "·";
  position: absolute;
  left: 0;
  top: -2mm;
  color: #e0541b;
  font-size: 16pt;
  font-weight: 700;
  line-height: 1;
}

/* ===== CALLOUTS ===== */
.callout {
  background: #ebe7dc;
  border-left: 3px solid #e0541b;
  padding: 4mm 5mm;
  margin: 4mm 0;
  border-radius: 0 3mm 3mm 0;
  page-break-inside: avoid;
}
.callout.legal {
  background: rgba(45,154,95,0.06);
  border-left-color: #2d9a5f;
}
.callout h4 {
  font-size: 9.5pt;
  margin-bottom: 2mm;
  font-family: 'JetBrains Mono', monospace;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #e0541b;
  font-weight: 600;
}
.callout.legal h4 { color: #2d9a5f; }
.callout p {
  font-size: 9.5pt;
  line-height: 1.55;
  margin-bottom: 2mm;
}
.callout p:last-child { margin-bottom: 0; }

/* ===== SIGNATURE BLOCK ===== */
.signature-block {
  border: 2px solid #0a0a0a;
  padding: 10mm;
  border-radius: 4mm;
  margin: 6mm 0;
  page-break-inside: avoid;
}
.signature-block h3 {
  font-size: 15pt;
  margin-bottom: 5mm;
  font-weight: 700;
}
.signature-block p {
  font-size: 10pt;
  line-height: 1.5;
  margin-bottom: 3mm;
}
.signature-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8mm;
  margin-top: 8mm;
}
.signature-col {
  border: 1px dashed #d5d2c9;
  padding: 6mm;
  border-radius: 2mm;
  background: #fafaf7;
}
.signature-col .role {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9pt;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #e0541b;
  font-weight: 600;
  margin-bottom: 3mm;
}
.signature-col .ident {
  font-size: 10pt;
  font-weight: 600;
  margin-bottom: 4mm;
  color: #0a0a0a;
  line-height: 1.3;
}
.signature-col .blanks {
  font-size: 9pt;
  color: #5a5d56;
  line-height: 1.7;
}
.signature-col .blanks .row {
  display: block;
  margin-bottom: 3mm;
}
.signature-col .blanks .line {
  display: inline-block;
  min-width: 50mm;
  border-bottom: 1px solid #5a5d56;
  margin-left: 2mm;
}
.signature-col .blanks .sign-area {
  display: block;
  min-height: 28mm;
  border: 1px dashed #d5d2c9;
  border-radius: 2mm;
  margin-top: 4mm;
  padding: 2mm;
  font-size: 8pt;
  color: #a9a69f;
}

/* ===== FIELD TABLE (RIB, KPI, etc.) ===== */
table.field-table {
  width: 100%;
  border-collapse: collapse;
  margin: 4mm 0;
  font-size: 9.5pt;
}
table.field-table td {
  padding: 2.5mm 3mm;
  border-bottom: 1px solid #ebe7dc;
  vertical-align: top;
  line-height: 1.4;
}
table.field-table td.label {
  font-weight: 600;
  color: #0a0a0a;
  width: 40%;
}
table.field-table td.value {
  color: #3a3d36;
  font-family: 'JetBrains Mono', monospace;
  font-size: 9pt;
}

/* ===== PLACEHOLDER STYLE ===== */
.placeholder {
  background: rgba(224,84,27,0.08);
  padding: 1px 5px;
  border-radius: 3px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.92em;
  color: #c43c2a;
  font-weight: 600;
  border: 1px dashed rgba(196,60,42,0.4);
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

def ph(label):
    """Inline placeholder for client-specific values."""
    return f'<span class="placeholder">[{label}]</span>'


def render_cover():
    return """
<section class="bleed cover">
  <div class="cover-top">
    <span class="badge">Convention de prestation · Modèle V1</span>
    <h1>L'Accélérateur<br>Carnet Plein<sup style="font-size:0.5em">®</sup>.</h1>
    <p class="sub">Convention de prestation de services entre Mad Makers et l'artisan Client - durée 12 mois ferme, garanties de moyens renforcées.</p>
  </div>
  <div class="cover-meta">
    <div>
      <div class="accent-line"></div>
      Modèle juridique - à faire valider par avocat
    </div>
    <div>carnetplein.mad-makers.fr</div>
  </div>
</section>
"""


def render_warning():
    return """
<section class="page">
  <div class="eyebrow">Avertissement</div>
  <div class="warning-page">
    <h2>Modèle V1 - à faire valider par un avocat.</h2>
    <p>Ce document est un <strong>modèle de convention de prestation rédigé en interne par Mad Makers</strong>. Il a vocation à structurer la relation contractuelle avec un artisan Client souscrivant à L'Accélérateur Carnet Plein®, mais il n'a pas encore été relu ni validé par un avocat ou un juriste spécialisé en droit commercial / droit du numérique / droit de la consommation.</p>
    <p><strong>Avant toute utilisation client</strong>, ce document doit être transmis à un professionnel du droit (avocat ou juriste BTP, conseil de la FFB/CAPEB, juriste spécialisé en e-commerce et prestations de services numériques) pour validation finale, ajustement des clauses, et adaptation à votre contexte spécifique.</p>
    <p>Coût indicatif d'une relecture par avocat : 200 à 600 € selon la complexité et la rapidité de retour. À considérer comme un investissement non négociable avant le premier client.</p>
    <p>Points de vigilance pour la relecture : (1) qualification B2B vs B2C selon la forme juridique du Client, (2) opposabilité de la clause de continuité gratuite (article 08), (3) clause RGPD si traitement de données personnelles de tiers, (4) clause de cession de droits sur les contenus créés, (5) répartition de la propriété intellectuelle au terme du contrat.</p>
  </div>
</section>
"""


def render_toc():
    articles = [
        "Préambule et identification des parties",
        "Objet du contrat",
        "Périmètre des prestations",
        "Durée du contrat",
        "Tarifs et modalités de paiement",
        "Engagements du Prestataire",
        "Engagements du Client",
        "Garantie Carnet Plein® - continuité gratuite",
        "Garantie qualité d'exécution à 90 jours",
        "Propriété intellectuelle et restitution des actifs",
        "Confidentialité et RGPD",
        "Médiation, litige et juridiction compétente",
        "Résiliation",
        "Force majeure",
        "Signature et exécution",
    ]
    items_html = "".join(f"<li>{a}</li>" for a in articles)

    return f"""
<section class="page toc">
  <div class="eyebrow">Table des articles</div>
  <h1>Quinze articles pour cadrer<br>une relation claire.</h1>
  <ol class="toc-list">{items_html}</ol>
</section>
"""


def render_art_01():
    return f"""
<section class="page">
  <div class="article">
    <div class="article-header">
      <span class="article-num">ARTICLE 01</span>
      <span class="article-title">Préambule et identification des parties</span>
    </div>
    <div class="article-body">
      <p>La présente Convention de prestation de services (ci-après « la Convention ») est conclue entre les deux parties désignées ci-dessous (ci-après ensemble « les Parties »), aux conditions stipulées dans les articles qui suivent.</p>

      <div class="parties">
        <div class="partie-card">
          <h3>Le Prestataire</h3>
          <div class="nom">{PRESTATAIRE['denomination']}</div>
          <p><strong>Représentant :</strong> {PRESTATAIRE['nom']}</p>
          <p><strong>Forme :</strong> {PRESTATAIRE['forme']}</p>
          <p><strong>Adresse :</strong> {PRESTATAIRE['adresse']}</p>
          <p><strong>SIRET :</strong> {PRESTATAIRE['siret']}</p>
          <p><strong>TVA intra :</strong> {PRESTATAIRE['tva']}</p>
          <p><strong>Code APE :</strong> {PRESTATAIRE['ape']}</p>
          <p><strong>Email :</strong> {PRESTATAIRE['email']}</p>
          <p><strong>Téléphone :</strong> {PRESTATAIRE['telephone']}</p>
        </div>
        <div class="partie-card">
          <h3>Le Client</h3>
          <div class="nom">{ph('NOM ENTREPRISE CLIENT')}</div>
          <p><strong>Représentant :</strong> {ph('PRÉNOM NOM DIRIGEANT')}</p>
          <p><strong>Forme :</strong> {ph('SARL / EURL / SAS / EI')}</p>
          <p><strong>Adresse :</strong> {ph('ADRESSE COMPLÈTE SIÈGE')}</p>
          <p><strong>SIRET :</strong> {ph('14 CHIFFRES')}</p>
          <p><strong>TVA intra :</strong> {ph('FR + CLÉ + SIREN')}</p>
          <p><strong>Code APE :</strong> {ph('4322A / 4322B / etc.')}</p>
          <p><strong>Email :</strong> {ph('EMAIL DIRIGEANT')}</p>
          <p><strong>Téléphone :</strong> {ph('NUMÉRO DIRECT')}</p>
        </div>
      </div>

      <div class="callout legal">
        <h4>Cadre juridique applicable</h4>
        <p>La présente Convention est régie par le droit français, et notamment les articles 1101 et suivants du Code civil (contrats), les articles 1231-1 et suivants du Code civil (responsabilité contractuelle), ainsi que par les dispositions du Code de la consommation lorsque le Client peut y être assimilé.</p>
      </div>
    </div>
  </div>
</section>
"""


def render_art_02():
    return f"""
<section class="page">
  <div class="article">
    <div class="article-header">
      <span class="article-num">ARTICLE 02</span>
      <span class="article-title">Objet du contrat</span>
    </div>
    <div class="article-body">
      <p>Le Prestataire s'engage à fournir au Client la prestation de services dénommée <strong>« L'Accélérateur Carnet Plein® »</strong> (ci-après « la Prestation »), consistant en la mise en œuvre d'un système complet de visibilité numérique locale destiné à augmenter, en quantité et en qualité, les demandes de devis entrantes du Client.</p>

      <p>La Prestation se compose de six (6) composants opérationnels décrits à l'article 03, livrés selon le calendrier convenu au brief de démarrage, et accompagnés de quatre (4) livrables annexes (bonus) remis à la signature.</p>

      <p>L'objectif partagé entre les Parties est de positionner le Client sur les premières positions de recherche locales Google pour son activité d'artisan du bâtiment, et d'automatiser autant que possible la captation et le traitement des demandes de devis qualifiées sur la zone géographique convenue.</p>

      <p>La Convention couvre une durée totale de douze (12) mois calendaires fermes à compter de la date de signature, conformément à l'article 04. Aucune reconduction tacite n'est prévue : à l'issue de cette période, les Parties devront, le cas échéant, négocier et signer un avenant explicite pour prolonger leur collaboration.</p>
    </div>
  </div>
</section>
"""


def render_art_03():
    composants_html = ""
    for c in COMPOSANTS:
        details_html = "".join(f"<li>{d}</li>" for d in c['details'])
        composants_html += f"""
  <div class="composant">
    <div class="composant-head">
      <span class="composant-num">COMPOSANT {c['num']} / 06</span>
      <span class="composant-nom">{c['nom']}</span>
    </div>
    <ul>{details_html}</ul>
  </div>
"""

    return f"""
<section class="page">
  <div class="article">
    <div class="article-header">
      <span class="article-num">ARTICLE 03</span>
      <span class="article-title">Périmètre des prestations</span>
    </div>
    <div class="article-body">
      <p>La Prestation se décompose en six (6) composants opérationnels distincts mais complémentaires, dont la liste détaillée et limitative est exposée ci-dessous. Toute prestation hors périmètre fera l'objet d'un avenant écrit chiffré.</p>

      {composants_html}

      <div class="callout">
        <h4>Hors périmètre</h4>
        <p>Sont expressément exclus du présent contrat : la création ou la gestion de comptes publicitaires (Google Ads, Meta Ads, autres), la prospection téléphonique ou par email pour le compte du Client, la rédaction de devis ou de factures commerciales, la gestion comptable, la création de supports imprimés (cartes de visite, flyers), et toute prestation de community management sur des réseaux sociaux autres que Google Business Profile.</p>
      </div>

      <div class="callout legal">
        <h4>Confidentialité du dispositif cohort</h4>
        <p>Les échanges effectués dans le cadre du kick-off groupé, de la visio cohort mensuelle et du groupe WhatsApp privé entre les membres de la cohort sont régis par une <strong>règle de discrétion implicite (type Chatham House)</strong> : ce qui est partagé dans ces espaces ne doit pas sortir du groupe. Toute divulgation à l'extérieur d'informations confidentielles concernant un autre membre de la cohort (chiffres, stratégies, références clients, situation personnelle), ou utilisation commerciale des données partagées par un autre membre, pourra entraîner l'exclusion immédiate du membre fautif du dispositif cohort, sans préjudice de la poursuite des autres prestations du contrat.</p>
      </div>
    </div>
  </div>
</section>
"""


def render_art_04():
    return f"""
<section class="page">
  <div class="article">
    <div class="article-header">
      <span class="article-num">ARTICLE 04</span>
      <span class="article-title">Durée du contrat</span>
    </div>
    <div class="article-body">
      <p>La présente Convention est conclue pour une durée déterminée de <strong>douze (12) mois calendaires fermes</strong>, à compter de la date de signature mentionnée à l'article 15.</p>

      <p>La période contractuelle débute à la date de signature et s'achève automatiquement, sans formalité, douze mois plus tard, à la même date.</p>

      <h4>Absence de tacite reconduction</h4>
      <p>Conformément à l'engagement public du Prestataire sur le site carnetplein.mad-makers.fr et à l'esprit anti-bullshit de la prestation, <strong>aucune clause de tacite reconduction n'est prévue</strong>. À l'issue de la période de douze mois, le Client n'est tenu à aucun engagement supplémentaire et peut librement :</p>
      <ul>
        <li>Récupérer la pleine propriété de son site web, de ses comptes Google Business Profile et de toutes les données associées, dans les conditions prévues à l'article 10</li>
        <li>Cesser purement et simplement la relation contractuelle</li>
        <li>Négocier avec le Prestataire un nouvel accord par avenant écrit, avec un périmètre et un tarif éventuellement renégociés</li>
      </ul>

      <p>La date prévisionnelle de démarrage opérationnel (« kick-off »), correspondant au premier rendez-vous de brief, est fixée à {ph('JJ/MM/AAAA')}. La livraison du « bundle initial » (mise en service des six composants) intervient dans un délai cible de quatorze (14) jours calendaires à compter du kick-off, sauf cas de retard imputable au Client ou de force majeure (article 14).</p>
    </div>
  </div>
</section>
"""


def render_art_05():
    return f"""
<section class="page">
  <div class="article">
    <div class="article-header">
      <span class="article-num">ARTICLE 05</span>
      <span class="article-title">Tarifs et modalités de paiement</span>
    </div>
    <div class="article-body">
      <p>En contrepartie de la Prestation décrite à l'article 03, le Client s'engage à régler au Prestataire les sommes ci-après détaillées.</p>

      <h4>Tarification</h4>
      <table class="field-table">
        <tr><td class="label">Forfait de setup (à la signature)</td><td class="value">5 000 € HT</td></tr>
        <tr><td class="label">Retainer mensuel (à partir du 2e mois)</td><td class="value">800 € HT / mois</td></tr>
        <tr><td class="label">Durée du retainer</td><td class="value">11 mois (mois 2 à mois 12)</td></tr>
        <tr><td class="label">Total HT sur 12 mois</td><td class="value">13 800 € HT</td></tr>
        <tr><td class="label">TVA applicable</td><td class="value">20% (prestation de services B2B)</td></tr>
        <tr><td class="label">Total TTC sur 12 mois</td><td class="value">16 560 € TTC</td></tr>
      </table>

      <h4>Modalités de paiement</h4>
      <p>Le Client peut opter, à sa convenance et au moment de la signature, pour l'une des trois modalités suivantes :</p>
      <ol>
        <li><strong>Paiement comptant intégral</strong> du forfait setup à la signature (5 000 € HT), puis prélèvement / virement mensuel récurrent de 800 € HT chaque 1er du mois à partir du mois 2.</li>
        <li><strong>Paiement en 3 fois sans frais</strong> du forfait setup : 3 × 1 666,67 € HT prélevés à J0, J+30, J+60.</li>
        <li><strong>Paiement en 6 fois avec 2% d'agios</strong> du forfait setup : 6 × 850 € HT prélevés mensuellement à partir de la signature.</li>
      </ol>

      <h4>Moyens de paiement acceptés</h4>
      <p>Virement bancaire SEPA, prélèvement SEPA (mandat à signer à la signature de la Convention), ou paiement par carte bancaire via une plateforme tierce sécurisée (Stripe, GoCardless).</p>

      <h4>Pénalités de retard</h4>
      <p>Conformément à l'article L441-10 du Code de commerce, tout retard de paiement entraîne de plein droit l'application d'une pénalité calculée au taux d'intérêt appliqué par la Banque Centrale Européenne à son opération de refinancement la plus récente majoré de 10 points, ainsi qu'une indemnité forfaitaire pour frais de recouvrement de 40 € par facture en retard.</p>

      <h4>Suspension des prestations</h4>
      <p>En cas de non-paiement d'une mensualité après deux relances espacées d'au moins quinze (15) jours calendaires, le Prestataire pourra suspendre la fourniture des prestations jusqu'à régularisation, sans que cette suspension ne dispense le Client du paiement des mois suspendus ni des intérêts de retard.</p>
    </div>
  </div>
</section>
"""


def render_art_06():
    return f"""
<section class="page">
  <div class="article">
    <div class="article-header">
      <span class="article-num">ARTICLE 06</span>
      <span class="article-title">Engagements du Prestataire</span>
    </div>
    <div class="article-body">
      <p>Le Prestataire s'engage, dans le cadre de la présente Convention, à exécuter la Prestation selon une <strong>obligation de moyens renforcée</strong> au sens de l'article 1231-1 du Code civil, à l'exclusion expresse de toute obligation de résultat sur des indicateurs commerciaux dépendants de facteurs extérieurs (qualité du marché local, prix pratiqués par le Client, qualité de la relation client par le Client, conditions économiques générales).</p>

      <h4>Délais de livraison</h4>
      <ul>
        <li>Kick-off (premier rendez-vous brief) : sous 7 jours calendaires à compter de la signature</li>
        <li>Livraison du bundle initial (six composants opérationnels) : sous 14 jours calendaires à compter du kick-off, soit 21 jours calendaires maximum à compter de la signature</li>
        <li>Premier reporting mensuel : le 5 du mois suivant la mise en service complète</li>
        <li>Points d'étape mensuels : un par mois calendaire jusqu'à la fin de la Convention</li>
      </ul>

      <h4>Qualité d'exécution</h4>
      <p>Le Prestataire s'engage à livrer chaque composant conformément à la description technique de l'article 03, en respectant les standards professionnels en vigueur (performances web, accessibilité WCAG 2.1 niveau AA pour le site, conformité RGPD pour la collecte de données, respect des chartes Google Business Profile).</p>

      <h4>Disponibilité et délais de réponse</h4>
      <p>Le Prestataire s'engage à répondre aux sollicitations courantes du Client (email, WhatsApp Business professionnel) sous quarante-huit (48) heures ouvrées, et à traiter toute alerte technique critique (site inaccessible, problème GBP majeur) sous huit (8) heures ouvrées.</p>

      <h4>Transparence</h4>
      <p>Le Prestataire s'engage à fournir au Client un accès en lecture seule à l'ensemble des comptes et outils utilisés pour la Prestation (compte GBP, hébergeur, plateforme de mailing, etc.). Aucune information ne doit rester opaque pour le Client tout au long du contrat.</p>

      <h4>Confidentialité</h4>
      <p>Le Prestataire s'engage à respecter la confidentialité de toutes les informations recueillies dans le cadre de la Prestation, conformément à l'article 11 ci-après.</p>
    </div>
  </div>
</section>
"""


def render_art_07():
    return f"""
<section class="page">
  <div class="article">
    <div class="article-header">
      <span class="article-num">ARTICLE 07</span>
      <span class="article-title">Engagements du Client</span>
    </div>
    <div class="article-body">
      <p>La bonne exécution de la Prestation suppose une collaboration active du Client. Le Client s'engage en conséquence à respecter les engagements suivants, qui sont indissociables des garanties prévues aux articles 08 et 09.</p>

      <h4>Mise à disposition d'informations et de contenus</h4>
      <ul>
        <li>Communiquer dans les sept (7) jours suivant le kick-off l'ensemble des informations nécessaires à la création ou à la reprise du site web et de la fiche Google Business Profile (raison sociale, adresse, horaires, photos initiales, certifications RGE, marques partenaires, références clients utilisables)</li>
        <li>Donner accès au Prestataire à tous les comptes existants (Google Business Profile, hébergeur, registrar du nom de domaine, plateforme d'emailing) sous forme d'accès délégué ou d'administrateur secondaire</li>
        <li>Fournir chaque semaine au moins deux à trois (2-3) photos de chantiers récents, dans un délai de soixante-douze (72) heures après la fin du chantier concerné, accompagnées d'une légende brève et de l'accord du client final lorsque cela est requis (article 11)</li>
      </ul>

      <h4>Réactivité aux demandes de devis entrantes</h4>
      <p>Le Client s'engage à répondre à toute demande de devis générée par le système Carnet Plein® dans un délai maximum de <strong>vingt-quatre (24) heures ouvrées</strong>. Le non-respect répété de ce délai constitue un défaut de coopération du Client de nature à exonérer le Prestataire de ses obligations au titre de l'article 08 (garantie de continuité gratuite).</p>

      <h4>Validation des contenus produits</h4>
      <p>Le Client s'engage à valider ou commenter, dans un délai maximum de cinq (5) jours ouvrés, tout contenu produit par le Prestataire et soumis à validation (texte du site, publication Google Post, réponse à un avis, photo retouchée). À défaut de retour dans ce délai, le contenu sera considéré comme validé par défaut.</p>

      <h4>Honnêteté de la collaboration</h4>
      <p>Le Client s'engage à ne pas demander au Prestataire la production de contenus mensongers ou trompeurs (faux avis clients, fausses références chantiers, faux témoignages, usage abusif de labels RGE ou certifications dont il ne serait pas titulaire). Toute demande de cette nature pourra entraîner la résiliation immédiate du contrat aux torts du Client (article 13).</p>

      <h4>Paiement aux échéances</h4>
      <p>Le Client s'engage au respect strict des échéances de paiement définies à l'article 05.</p>
    </div>
  </div>
</section>
"""


def render_art_08():
    return f"""
<section class="page">
  <div class="article">
    <div class="article-header">
      <span class="article-num">ARTICLE 08</span>
      <span class="article-title">Garantie Carnet Plein® - continuité gratuite</span>
    </div>
    <div class="article-body">
      <p>Le Prestataire consent au Client la garantie spécifique dite « Garantie Carnet Plein® », dans les conditions définies ci-après. Cette garantie constitue un renforcement contractuel de l'obligation de moyens prévue à l'article 06 et <strong>ne saurait être interprétée comme une obligation de résultat</strong>.</p>

      <h4>Objectif contractuel défini au brief</h4>
      <p>Au cours du rendez-vous de kick-off mentionné à l'article 04, les Parties définissent ensemble, par écrit, un <strong>objectif principal mesurable</strong> à douze mois (ci-après « l'Objectif »). Cet Objectif est consigné dans une annexe signée des deux Parties qui fait partie intégrante de la présente Convention.</p>

      <p>L'Objectif doit être <strong>spécifique, mesurable, atteignable, réaliste et temporellement défini</strong>. Il porte typiquement, à titre d'exemple non exhaustif, sur l'un des indicateurs suivants : nombre de demandes de devis qualifiées générées par mois en année 2, position moyenne de la fiche GBP sur les requêtes locales clés, nombre d'avis Google de quatre étoiles ou plus accumulés sur douze mois, ou taux de conversion site web.</p>

      <p>L'Objectif est défini dans l'annexe sous la forme : {ph('OBJECTIF MESURABLE PRÉCIS, valeur cible chiffrée, méthode de mesure')}</p>

      <h4>Déclenchement de la garantie</h4>
      <p>Si à l'issue de la période de douze mois, l'Objectif est atteint <strong>à moins de 80%</strong> de la valeur cible inscrite dans l'annexe, et sous réserve que le Client ait respecté l'intégralité de ses engagements définis à l'article 07, le Prestataire s'engage à <strong>poursuivre sans facturer de retainer supplémentaire</strong> la fourniture des Prestations pendant la durée nécessaire à l'atteinte de cet Objectif.</p>

      <h4>Limites et exclusions de la garantie</h4>
      <ul>
        <li>La garantie de continuité gratuite est limitée au périmètre des prestations défini à l'article 03 et ne peut donner lieu à aucune indemnité financière ou compensation monétaire d'aucune sorte.</li>
        <li>La garantie est exclue si le Client n'a pas respecté ses engagements de l'article 07, notamment en matière de réactivité aux demandes de devis (24h), de fourniture de photos, et de validation des contenus.</li>
        <li>La garantie est exclue en cas de modification substantielle de l'activité du Client en cours de contrat (changement de métier principal, déménagement hors de la zone initiale, cessation d'activité partielle).</li>
        <li>La garantie est exclue en cas de pratique anormale du Client (avis Google négatifs liés à la qualité des prestations métier du Client, contentieux clients impactant la réputation locale).</li>
        <li>La garantie ne saurait excéder une durée de six (6) mois supplémentaires au-delà des 12 mois contractuels initiaux. Au-delà, les Parties devront convenir d'un nouvel accord.</li>
      </ul>

      <div class="callout legal">
        <h4>Cadre légal - obligation de moyens renforcée</h4>
        <p>La présente garantie constitue une obligation de moyens renforcée au sens de l'article 1231-1 du Code civil. Elle ne crée aucune obligation de résultat à la charge du Prestataire, le résultat commercial du Client dépendant nécessairement de facteurs extérieurs au périmètre d'intervention du Prestataire.</p>
      </div>
    </div>
  </div>
</section>
"""


def render_art_09():
    return f"""
<section class="page">
  <div class="article">
    <div class="article-header">
      <span class="article-num">ARTICLE 09</span>
      <span class="article-title">Garantie qualité d'exécution à 90 jours</span>
    </div>
    <div class="article-body">
      <p>Indépendamment de la garantie de continuité prévue à l'article 08, le Prestataire consent au Client une garantie spécifique portant sur la qualité d'exécution de la Prestation au cours des premiers mois.</p>

      <h4>Périmètre de la garantie</h4>
      <p>Si, à quatre-vingt-dix (90) jours calendaires après la livraison du bundle initial (article 06), le Client constate de manière motivée et documentée que :</p>
      <ul>
        <li>La qualité d'exécution des Prestations livrées n'est pas conforme aux standards professionnels attendus (défauts manifestes du site web, erreurs significatives sur la fiche GBP, retards systématiques sur les publications)</li>
        <li>La communication entre les Parties est insatisfaisante (délais de réponse non respectés, absence de transparence)</li>
        <li>Les engagements du Prestataire au titre de l'article 06 n'ont pas été tenus</li>
      </ul>

      <p>... le Client peut faire valoir la présente garantie par lettre recommandée avec accusé de réception, dans un délai maximum de quatre-vingt-quatorze (94) jours après la livraison du bundle initial.</p>

      <h4>Effet de la garantie</h4>
      <p>En cas d'application de la garantie qualité, le Prestataire s'engage à octroyer au Client <strong>un (1) mois de retainer additionnel offert</strong> en fin de période contractuelle (mois 13), sans conditions ni questions, ce qui équivaut à 800 € HT de prestations supplémentaires offertes.</p>

      <p>Cette garantie est subsidiaire et indépendante de la garantie de continuité gratuite prévue à l'article 08. Les deux garanties peuvent se cumuler dans le cas où les conditions des deux articles sont remplies.</p>

      <div class="callout">
        <h4>Engagement de bonne foi</h4>
        <p>La présente garantie traduit l'engagement de bonne foi du Prestataire envers la qualité d'exécution de la Prestation. Elle vise à offrir au Client un recours simple et rapide en cas d'insatisfaction sur les premiers mois, sans avoir à engager une procédure formelle de résiliation.</p>
      </div>
    </div>
  </div>
</section>
"""


def render_art_10():
    return f"""
<section class="page">
  <div class="article">
    <div class="article-header">
      <span class="article-num">ARTICLE 10</span>
      <span class="article-title">Propriété intellectuelle et restitution des actifs</span>
    </div>
    <div class="article-body">
      <p>Le présent article définit le régime de la propriété intellectuelle des créations réalisées par le Prestataire au profit du Client, ainsi que les modalités de restitution des actifs numériques au terme de la Convention.</p>

      <h4>Cession des droits patrimoniaux</h4>
      <p>Le Prestataire cède au Client, à compter du paiement intégral de la première année de prestation, l'ensemble des <strong>droits patrimoniaux d'auteur</strong> portant sur les créations spécifiquement réalisées pour le Client dans le cadre de la Convention, à savoir : textes du site web, design et code source du site, photographies retouchées, contenus des Google Posts, contenus des bonus livrés.</p>

      <p>La cession comprend les droits de reproduction, de représentation, d'adaptation et de traduction, pour toute la durée légale de protection des droits d'auteur, sur tous supports connus ou inconnus à ce jour, dans le monde entier, à des fins commerciales ou non.</p>

      <p>Demeurent la propriété exclusive du Prestataire : la méthodologie générale de l'Accélérateur Carnet Plein®, la marque « Carnet Plein® », les templates et frameworks internes utilisés (CSS, scripts Python, scripts JavaScript du framework de site), et tous les bonus livrables sous leur forme générique (les versions personnalisées au Client sont, elles, propriété du Client).</p>

      <h4>Restitution des comptes et des données</h4>
      <p>À l'issue de la Convention (mois 12), ou en cas de résiliation anticipée (article 13), le Prestataire s'engage à restituer au Client, dans un délai maximum de trente (30) jours calendaires :</p>
      <ul>
        <li>Le transfert intégral des accès au compte Google Business Profile (le Client en redevient seul administrateur)</li>
        <li>Le transfert du nom de domaine et de l'hébergement vers un compte propriétaire du Client, ou export complet du site sous forme de fichiers statiques (HTML, CSS, JS, images)</li>
        <li>Une copie de l'ensemble des contenus textuels et visuels créés (export ZIP)</li>
        <li>Une copie de l'ensemble des rapports mensuels et des données analytiques accumulées sur la période</li>
        <li>Une liste exhaustive des outils et services tiers utilisés (avec identifiants de référence, sans mots de passe pour des raisons de sécurité)</li>
      </ul>

      <h4>Coût de la restitution</h4>
      <p>La restitution des actifs définis ci-dessus est <strong>incluse dans le tarif</strong> de la Convention. Aucun frais supplémentaire ne pourra être facturé au Client à ce titre, sauf pour des prestations de migration techniques exceptionnelles dont le Client serait à l'initiative et qui feraient l'objet d'un devis séparé.</p>
    </div>
  </div>
</section>
"""


def render_art_11():
    return f"""
<section class="page">
  <div class="article">
    <div class="article-header">
      <span class="article-num">ARTICLE 11</span>
      <span class="article-title">Confidentialité et RGPD</span>
    </div>
    <div class="article-body">

      <h4>Obligation générale de confidentialité</h4>
      <p>Chacune des Parties s'engage à conserver strictement confidentielles l'ensemble des informations communiquées par l'autre Partie dans le cadre de la Convention, et notamment : informations commerciales, données financières, listes de clients finaux, retours d'expérience, méthodologies internes, accès aux comptes numériques.</p>

      <p>Cette obligation perdure pendant toute la durée de la Convention et pendant les trois (3) années suivant son terme, quelle qu'en soit la cause.</p>

      <h4>Traitement des données personnelles</h4>
      <p>Dans le cadre de la Prestation, le Prestataire peut être amené à traiter des données personnelles relatives :</p>
      <ul>
        <li>Aux clients finaux du Client (nom, prénom, email, téléphone, adresse) lorsque ces données transitent par les formulaires de devis du site web ou les avis Google</li>
        <li>Aux salariés ou collaborateurs du Client (nom, prénom, photo, fonction) lorsque ces données apparaissent sur le site ou la fiche GBP</li>
        <li>Au dirigeant du Client lui-même</li>
      </ul>

      <h4>Qualification au sens du RGPD</h4>
      <p>Pour les données personnelles des clients finaux et des collaborateurs du Client, le Prestataire agit en qualité de <strong>sous-traitant</strong> du Client au sens de l'article 28 du RGPD. Le Client demeure <strong>responsable de traitement</strong> de ces données.</p>

      <h4>Engagements du Prestataire en tant que sous-traitant</h4>
      <ul>
        <li>Ne traiter les données que sur instruction documentée du Client</li>
        <li>Garantir la confidentialité des personnes habilitées à traiter les données</li>
        <li>Prendre toutes les mesures de sécurité requises (chiffrement, accès restreint, sauvegardes)</li>
        <li>N'utiliser aucun sous-sous-traitant sans autorisation préalable écrite du Client</li>
        <li>Notifier au Client toute violation de données dans les 48 heures de sa découverte</li>
        <li>Restituer ou supprimer toutes les données à l'issue du contrat, au choix du Client</li>
      </ul>

      <h4>Sous-traitants et services tiers utilisés</h4>
      <p>Le Prestataire informe le Client qu'il utilise les services tiers suivants pour l'exécution de la Prestation : Vercel (hébergement, États-Unis avec serveurs UE et SCC), Cloudflare (CDN, monde), Google Business Profile (Google, États-Unis), Bunny Fonts (typographies, UE), Stripe (paiements, si choisi). Le Client autorise expressément l'utilisation de ces sous-traitants.</p>

      <h4>Droits des personnes concernées</h4>
      <p>Le Client s'engage à informer ses clients finaux et collaborateurs des traitements opérés, et à garantir l'exercice de leurs droits RGPD (accès, rectification, effacement, opposition) en relayant les demandes au Prestataire dans les meilleurs délais.</p>
    </div>
  </div>
</section>
"""


def render_art_12():
    return f"""
<section class="page">
  <div class="article">
    <div class="article-header">
      <span class="article-num">ARTICLE 12</span>
      <span class="article-title">Médiation, litige et juridiction compétente</span>
    </div>
    <div class="article-body">

      <h4>Tentative de règlement amiable</h4>
      <p>En cas de désaccord ou de litige entre les Parties dans l'exécution de la présente Convention, les Parties s'engagent à se rencontrer (par visioconférence si nécessaire) dans un délai de quinze (15) jours calendaires à compter de la notification écrite du désaccord par l'une des Parties, afin de tenter d'aboutir à un règlement amiable.</p>

      <h4>Médiation de la consommation</h4>
      <p>Si le Client est un consommateur au sens du Code de la consommation, ou peut y être assimilé (artisan exerçant en nom personnel), et si la tentative de règlement amiable échoue, le Client peut saisir gratuitement le médiateur de la consommation suivant :</p>
      <table class="field-table">
        <tr><td class="label">Médiateur</td><td class="value">CM2C - Centre de Médiation et de Consommation</td></tr>
        <tr><td class="label">Adresse</td><td class="value">49 rue de Ponthieu, 75008 Paris</td></tr>
        <tr><td class="label">Site internet</td><td class="value">cm2c.net</td></tr>
        <tr><td class="label">Email</td><td class="value">contact@cm2c.net</td></tr>
      </table>

      <p>Cette saisine doit intervenir dans un délai d'un an à compter de la réclamation écrite adressée au Prestataire.</p>

      <h4>Juridiction compétente</h4>
      <p>À défaut de résolution amiable ou par médiation, tout litige sera soumis aux tribunaux compétents du <strong>ressort de la Cour d'appel de Paris</strong>, conformément aux règles de droit commun applicables.</p>

      <p>Si le Client est un consommateur au sens du Code de la consommation, le tribunal compétent peut, selon le choix du Client, être celui du lieu où il demeurait au moment de la conclusion du contrat ou de la survenance du fait dommageable, conformément à l'article R631-3 du Code de la consommation.</p>
    </div>
  </div>
</section>
"""


def render_art_13():
    return f"""
<section class="page">
  <div class="article">
    <div class="article-header">
      <span class="article-num">ARTICLE 13</span>
      <span class="article-title">Résiliation</span>
    </div>
    <div class="article-body">

      <h4>Résiliation à l'issue de la durée contractuelle</h4>
      <p>La Convention prend fin de plein droit, sans formalité, à l'issue de la période de douze (12) mois prévue à l'article 04. Aucun préavis n'est requis. Aucune indemnité n'est due par l'une ou l'autre des Parties au titre de cette fin de contrat.</p>

      <h4>Résiliation anticipée pour manquement</h4>
      <p>Chacune des Parties pourra résilier la Convention de manière anticipée, par lettre recommandée avec accusé de réception, en cas de manquement grave de l'autre Partie à ses obligations contractuelles, et après mise en demeure restée sans effet pendant trente (30) jours calendaires.</p>

      <p>Sont notamment considérés comme manquements graves :</p>
      <ul>
        <li>Pour le Client : le défaut de paiement répété de plus de deux mensualités consécutives malgré relances ; la demande de production de contenus mensongers, trompeurs ou contraires à l'éthique professionnelle (article 07) ; le non-respect répété des engagements de coopération (réactivité aux demandes de devis, validation des contenus)</li>
        <li>Pour le Prestataire : le non-respect répété des délais de réponse contractuels ; la suspension non motivée et non communiquée des prestations ; l'utilisation des données du Client à des fins autres que la Prestation</li>
      </ul>

      <h4>Effets de la résiliation anticipée</h4>
      <ul>
        <li>Si la résiliation est aux torts du Client : le Client demeure redevable des sommes facturées et impayées au titre des mois écoulés, ainsi que d'une indemnité forfaitaire de résiliation égale à trois (3) mois de retainer, soit 2 400 € HT, en compensation de l'investissement initial non amorti par le Prestataire.</li>
        <li>Si la résiliation est aux torts du Prestataire : le Prestataire rembourse au Client, au prorata temporis, le forfait setup payé à la signature, et procède à la restitution immédiate des actifs prévus à l'article 10, sans frais.</li>
      </ul>

      <h4>Résiliation pour cas de force majeure prolongé</h4>
      <p>Si un cas de force majeure (article 14) se prolonge au-delà de soixante (60) jours calendaires, chacune des Parties peut résilier la Convention sans indemnité, sur simple notification écrite à l'autre Partie.</p>
    </div>
  </div>
</section>
"""


def render_art_14():
    return f"""
<section class="page">
  <div class="article">
    <div class="article-header">
      <span class="article-num">ARTICLE 14</span>
      <span class="article-title">Force majeure</span>
    </div>
    <div class="article-body">
      <p>Aucune des Parties ne sera tenue pour responsable de l'inexécution totale ou partielle de ses obligations contractuelles si cette inexécution résulte d'un cas de force majeure au sens de l'article 1218 du Code civil, c'est-à-dire d'un événement échappant à son contrôle, qu'elle ne pouvait raisonnablement prévoir et dont elle ne pouvait éviter les effets par des mesures appropriées.</p>

      <p>Sont notamment considérés comme cas de force majeure : les catastrophes naturelles, les guerres et conflits armés, les troubles civils, les grèves générales, les épidémies entraînant des mesures gouvernementales restrictives (à l'instar de la crise sanitaire COVID-19), les pannes majeures et prolongées des infrastructures de télécommunication ou d'hébergement non remplaçables, les cyberattaques généralisées affectant les principaux fournisseurs de services cloud utilisés.</p>

      <p>La Partie invoquant la force majeure devra en informer l'autre Partie par écrit dans les meilleurs délais, en précisant la nature de l'événement, sa date prévisible de cessation, et les conséquences attendues sur l'exécution de ses obligations.</p>

      <p>Durant la période de force majeure, l'exécution des obligations contractuelles est suspendue. Si l'événement perdure au-delà de soixante (60) jours, l'article 13 (résiliation) trouvera à s'appliquer.</p>
    </div>
  </div>
</section>
"""


def render_art_15_signature():
    return f"""
<section class="page">
  <div class="article">
    <div class="article-header">
      <span class="article-num">ARTICLE 15</span>
      <span class="article-title">Signature et exécution</span>
    </div>
    <div class="article-body">
      <p>La présente Convention est établie en deux exemplaires originaux, un pour chaque Partie. Elle entre en vigueur à la date de signature par les deux Parties.</p>

      <p>Toute modification ultérieure de la Convention devra faire l'objet d'un avenant écrit signé par les deux Parties pour produire effet.</p>

      <p>Conformément à l'article 1366 du Code civil, la Convention peut être signée par voie électronique au moyen d'une plateforme de signature électronique reconnue (Yousign, DocuSign, ou équivalent), avec la même valeur probante qu'une signature manuscrite.</p>

      <p>En signant ci-dessous, chacune des Parties reconnaît : avoir lu l'intégralité de la présente Convention et de ses annexes, en avoir compris la portée juridique, et accepter expressément l'ensemble de ses stipulations.</p>

      <div class="signature-block">
        <h3>Signatures</h3>
        <p>Fait à {ph('VILLE')}, le {ph('JJ/MM/AAAA')}.</p>
        <p>Mention manuscrite obligatoire à porter par chacune des Parties au-dessus de sa signature : <strong>« Lu et approuvé - Bon pour accord »</strong>.</p>

        <div class="signature-grid">
          <div class="signature-col">
            <div class="role">Pour le Prestataire</div>
            <div class="ident">{PRESTATAIRE['nom']}<br>{PRESTATAIRE['denomination']}</div>
            <div class="blanks">
              <span class="row">Fait à <span class="line"></span></span>
              <span class="row">Le <span class="line"></span></span>
              <span class="row">Signature précédée de la mention « Lu et approuvé » :</span>
              <span class="sign-area">Signature</span>
            </div>
          </div>
          <div class="signature-col">
            <div class="role">Pour le Client</div>
            <div class="ident">{ph('PRÉNOM NOM DIRIGEANT')}<br>{ph('NOM ENTREPRISE CLIENT')}</div>
            <div class="blanks">
              <span class="row">Fait à <span class="line"></span></span>
              <span class="row">Le <span class="line"></span></span>
              <span class="row">Signature précédée de la mention « Lu et approuvé » :</span>
              <span class="sign-area">Signature</span>
            </div>
          </div>
        </div>
      </div>

      <div class="final-disclaimer">
        Document V1 - Modèle interne Mad Makers - À faire valider par un avocat ou un juriste BTP avant utilisation client. Édition 2026. Les références légales citées (articles du Code civil, Code de commerce, Code de la consommation, RGPD) sont à jour de la législation française au mois de mai 2026. Les Parties sont invitées à vérifier l'actualité de ces références au moment de la signature. La présente Convention vaut entre les Parties à compter de la signature et pendant la durée définie à l'article 04.
      </div>
    </div>
  </div>
</section>
"""


def render_annexe_objectif():
    return f"""
<section class="page">
  <div class="eyebrow">Annexe 1 - Objectif contractuel</div>
  <div class="article">
    <div class="article-header">
      <span class="article-num">ANNEXE 1</span>
      <span class="article-title">Objectif Carnet Plein® défini au brief</span>
    </div>
    <div class="article-body">
      <p>La présente annexe précise l'Objectif principal mesurable mentionné à l'article 08 de la Convention. Elle est signée par les deux Parties à l'issue du rendez-vous de kick-off et fait partie intégrante de la Convention.</p>

      <table class="field-table">
        <tr><td class="label">Date du kick-off</td><td class="value">{ph('JJ/MM/AAAA')}</td></tr>
        <tr><td class="label">Lieu du kick-off</td><td class="value">{ph('VISIO / VILLE')}</td></tr>
        <tr><td class="label">Zone géographique cible</td><td class="value">{ph('VILLE + RAYON KM, OU CANTON, OU DÉPARTEMENT')}</td></tr>
        <tr><td class="label">Métiers et services prioritaires</td><td class="value">{ph('CHAUFFAGE / PAC / SDB / ECS / etc.')}</td></tr>
        <tr><td class="label">Indicateur principal retenu (KPI)</td><td class="value">{ph('NOMBRE DE DEMANDES DE DEVIS QUALIFIÉES / MOIS')}</td></tr>
        <tr><td class="label">Valeur de référence à T0</td><td class="value">{ph('VALEUR INITIALE MESURÉE OU ESTIMÉE')}</td></tr>
        <tr><td class="label">Valeur cible à T+12 mois</td><td class="value">{ph('VALEUR CIBLE CHIFFRÉE')}</td></tr>
        <tr><td class="label">Méthode de mesure</td><td class="value">{ph('GBP Insights / GA4 / CRM client / autre')}</td></tr>
        <tr><td class="label">Fréquence de relevé</td><td class="value">{ph('Mensuelle / Trimestrielle')}</td></tr>
        <tr><td class="label">Seuil de déclenchement de la garantie</td><td class="value">80% de la valeur cible</td></tr>
      </table>

      <div class="callout">
        <h4>Méthode de définition de l'Objectif</h4>
        <p>L'Objectif est défini conjointement par les Parties selon la méthode SMART : Spécifique, Mesurable, Atteignable, Réaliste, Temporellement défini. Le Prestataire s'engage à proposer un Objectif réaliste compte tenu du marché local, du positionnement initial du Client, et de la concurrence observée. Le Client s'engage à accepter cet Objectif en toute connaissance de cause et à coopérer pleinement à son atteinte.</p>
      </div>

      <h4>Signatures de l'annexe</h4>
      <div class="signature-grid">
        <div class="signature-col">
          <div class="role">Pour le Prestataire</div>
          <div class="ident">{PRESTATAIRE['nom']}<br>{PRESTATAIRE['denomination']}</div>
          <div class="blanks">
            <span class="row">Le <span class="line"></span></span>
            <span class="sign-area">Signature</span>
          </div>
        </div>
        <div class="signature-col">
          <div class="role">Pour le Client</div>
          <div class="ident">{ph('PRÉNOM NOM DIRIGEANT')}<br>{ph('NOM ENTREPRISE CLIENT')}</div>
          <div class="blanks">
            <span class="row">Le <span class="line"></span></span>
            <span class="sign-area">Signature</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
"""


def render_html():
    parts = [
        render_cover(),
        render_warning(),
        render_toc(),
        render_art_01(),
        render_art_02(),
        render_art_03(),
        render_art_04(),
        render_art_05(),
        render_art_06(),
        render_art_07(),
        render_art_08(),
        render_art_09(),
        render_art_10(),
        render_art_11(),
        render_art_12(),
        render_art_13(),
        render_art_14(),
        render_art_15_signature(),
        render_annexe_objectif(),
    ]

    body = "\n".join(parts)

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Convention Carnet Plein® by Mad Makers - Modèle V1</title>
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
        "contrat-garantie-carnet-plein.html"
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
    print(f"     Pages estimees : ~22 (cover + warning + TOC + 15 articles + annexe objectif)")
    print()
    print("PROCHAINE ETAPE :")
    print("  1. Ouvrir le .html dans Chrome")
    print("  2. Ctrl+P (Imprimer)")
    print("  3. Destination : Enregistrer au format PDF")
    print("  4. Marges : Aucune (le CSS gere)")
    print("  5. Cocher Graphiques d'arriere-plan")
    print("  6. Enregistrer sous : Convention Carnet Plein - V1 modele.pdf")
    print()
    print("APRES :")
    print("  -> Envoyer le PDF a un avocat ou juriste BTP pour relecture")
    print("  -> Budget indicatif : 200 a 600 EUR")
