# Setup Calendly - "Audit Carnet Plein®"

> URL : https://calendly.com/directedbymaick/audit-carnet-plein
> Durée : 20 minutes (aligné avec promesse site)
> Opérateur : Rayan Mpondo (Maïck)
> Doc V1 - À configurer une seule fois dans Calendly

Ce document contient tout ce qu'il faut copier-coller dans Calendly pour transformer un event-type générique en funnel d'audit qualifié. Compte 30 minutes de setup une fois pour toutes.

---

## 1. Paramètres de l'événement (Event Type Settings)

Dans Calendly → Event Types → "Audit Carnet Plein®" → Edit

### Nom et description visibles sur la page de booking

**Nom de l'événement :**
```
Audit Carnet Plein® - 20 minutes
```

**Description (visible sur la page de booking) :**
```
Vingt minutes pour comprendre votre marché local, votre fiche Google
actuelle, et vous dire honnêtement si Carnet Plein® est fait pour vous.

Pas de pitch commercial déguisé. Si ce n'est pas le bon moment ou le
bon programme pour vous, je vous le dis directement et je vous oriente
vers la ressource gratuite la plus utile.

Avant le rendez-vous, vous recevrez un email de confirmation avec une
courte liste de questions à préparer (lien fiche Google, ville, métier
principal). Cinq minutes max pour gagner du temps le jour J.

À très bientôt.
```

### Durée et configuration

| Paramètre | Valeur | Note |
|---|---|---|
| **Duration** | 20 minutes | Aligné avec promesse site |
| **Location** | Google Meet (auto) ou Zoom | Google Meet préféré (zéro friction) |
| **Time zone** | Europe/Paris | Auto-detect côté visiteur |
| **Availability** | Lundi-vendredi, 10h-12h et 14h-17h | Pas de soir, pas de week-end : préserve ta vie + crédibilité B2B |
| **Buffer before** | 5 minutes | Temps de préparer le contexte du prospect |
| **Buffer after** | 15 minutes | Pour prendre des notes + envoyer email post-call |
| **Minimum scheduling notice** | 24 heures | Évite les bookings de dernière minute |
| **Maximum days in future** | 30 jours | Pas plus d'1 mois à l'avance (rareté) |
| **Date range** | Rolling 30 days | Glissant |
| **Daily limit** | 4 audits / jour max | Sinon tu vides ta journée |
| **Event color** | Orange `#e0541b` | Brand Carnet Plein® |

---

## 2. Booking form - 6 questions de qualification

Dans Calendly → Event Type → "Audit Carnet Plein®" → Invitee Questions

Calendly demande automatiquement le nom et l'email. À ajouter en custom questions :

### Q1 - Nom de l'entreprise et SIRET

**Type :** Text (single line)
**Label :**
```
Nom de votre entreprise (raison sociale)
```
**Description (sous le label) :**
```
Tel qu'il apparaît sur vos devis. Si vous êtes auto-entrepreneur, votre nom suffit.
```
**Required :** Oui

---

### Q2 - Métier principal

**Type :** Dropdown / Select
**Label :**
```
Votre métier principal
```
**Options :**
- Plombier-chauffagiste
- Chauffagiste (PAC, chaudière)
- Plombier (sanitaire, salle de bain)
- Électricien
- Maçon / Maçon-rénovateur
- Carreleur
- Couvreur
- Menuisier
- Étancheur
- Autre artisan du bâtiment

**Required :** Oui

---

### Q3 - Zone géographique d'intervention

**Type :** Text (single line)
**Label :**
```
Votre ville principale + rayon d'intervention en km
```
**Description :**
```
Exemple : "Lille + 30 km" ou "Romainville 93 + toute l'Île-de-France"
```
**Required :** Oui

---

### Q4 - Taille de l'entreprise

**Type :** Dropdown / Select
**Label :**
```
Vous êtes
```
**Options :**
- Seul (sans salarié, sans apprenti)
- 1 salarié ou 1 apprenti
- 2 à 5 salariés
- 6 à 10 salariés
- Plus de 10 salariés

**Required :** Oui

---

### Q5 - État actuel de votre visibilité Google

**Type :** Multi-select (checkboxes)
**Label :**
```
Aujourd'hui, vous avez (cochez tout ce qui s'applique)
```
**Options :**
- Un site internet professionnel
- Une fiche Google Business Profile active
- Au moins 10 avis Google
- Un système pour demander les avis automatiquement
- Aucun de ces éléments / je démarre de zéro

**Required :** Non (pour ne pas bloquer si flou)

---

### Q6 - Votre objectif principal pour les 12 prochains mois

**Type :** Long text (paragraph)
**Label :**
```
En une phrase, qu'est-ce qui vous amène à m'écrire ?
```
**Description :**
```
Pas besoin de jargon marketing. Mettez vos mots à vous : ce qui ne va pas
aujourd'hui, ou ce que vous voudriez changer dans les 12 prochains mois.
```
**Required :** Oui

---

## 3. Emails automatiques Calendly

Dans Calendly → Workflows (Free plan inclut les workflows basiques)

### Email A - Confirmation de réservation (envoyé immédiatement après booking)

**Trigger :** When invitee schedules
**Sent :** Immediately
**Recipient :** Invitee (le prospect)

**Subject :**
```
RDV confirmé : Audit Carnet Plein® le {{Event Date}} à {{Event Time}}
```

**Body (HTML simple, texte brut OK) :**
```
Bonjour {{Invitee First Name}},

Merci pour votre demande d'audit, c'est noté pour le {{Event Date}}
à {{Event Time}}.

Comment ça va se passer :

1. Je vais d'abord regarder votre fiche Google, votre site (si vous
   en avez un) et le marché local de votre zone. 5 minutes de
   préparation côté Mad Makers.

2. Le jour J, 20 minutes en visio sur le lien Google Meet ci-joint
   (qui apparaît aussi dans l'invitation calendrier que vous venez
   de recevoir).

3. Au cours du rendez-vous : pas de pitch commercial. Je vous
   présente ce que j'ai vu, les 2-3 leviers prioritaires pour
   votre situation, et je vous dis honnêtement si Carnet Plein®
   est fait pour vous ou pas.

4. Si oui, je vous envoie le devis détaillé et le contrat dans
   les 48 heures. Vous démarrez avec la cohort suivante (3 artisans
   max, 1er lundi du mois) qui inclut un kick-off groupé + une
   visio cohort mensuelle + un WhatsApp group entre vous trois et
   moi. Si non, je vous oriente vers la ressource gratuite la plus
   utile.

Pour gagner du temps le jour J, deux choses à préparer si possible
(5 minutes max, pas besoin de vous prendre la tête) :

- Le lien direct de votre fiche Google Business Profile (si vous
  en avez une). Sinon "non" suffit.
- Le lien de votre site internet professionnel (si vous en avez un).

Si vous devez décaler, voici le lien pour reprogrammer ou annuler :
{{Cancel Link}} | {{Reschedule Link}}

À très bientôt,
Rayan Mpondo (Maïck)
Mad Makers - Carnet Plein®
https://carnetplein.mad-makers.fr
```

---

### Email B - Rappel 24 heures avant le rendez-vous

**Trigger :** Before event starts
**Sent :** 24 hours before event start
**Recipient :** Invitee

**Subject :**
```
Demain {{Event Time}} : audit Carnet Plein®
```

**Body :**
```
Bonjour {{Invitee First Name}},

Petit rappel pour notre rendez-vous demain {{Event Date}} à
{{Event Time}}.

Lien de la visio : {{Location}}

Si vous n'avez pas encore préparé les 2 infos demandées dans la
confirmation (lien fiche Google + lien site), pas grave. On les
regardera ensemble.

À demain,
Rayan
```

---

### Email C - Rappel 1 heure avant le rendez-vous

**Trigger :** Before event starts
**Sent :** 1 hour before event start
**Recipient :** Invitee

**Subject :**
```
Dans 1 heure : notre point de 20 minutes
```

**Body :**
```
Bonjour {{Invitee First Name}},

On se retrouve dans 1 heure pour notre audit Carnet Plein®.

Visio : {{Location}}

Si imprévu : {{Cancel Link}}

À tout de suite,
Rayan
```

---

### Email D - Post no-show (si le prospect ne vient pas)

**Trigger :** Manual or after no-show flag
**Sent :** Same day after the missed slot
**Recipient :** Invitee

**Subject :**
```
Désolé de vous avoir manqué aujourd'hui
```

**Body :**
```
Bonjour {{Invitee First Name}},

Je viens de tenir le créneau pendant 10 minutes mais sans nouvelle de
votre part. Pas de souci, ça arrive.

Si l'audit Carnet Plein® vous intéresse toujours, voici le lien pour
reprogrammer quand ça vous arrange :
https://calendly.com/directedbymaick/audit-carnet-plein

Sinon, aucun souci, je vous souhaite une bonne suite.

Cordialement,
Rayan Mpondo (Maïck)
Mad Makers
```

---

### Email E - Post-call si "FIT" (envoi manuel après le RDV - template à coller dans ton client mail)

**Subject :**
```
Suite à notre échange - devis et contrat Carnet Plein® sous 48h
```

**Body :**
```
Bonjour {{PRENOM}},

Merci pour notre point de tout à l'heure. Comme convenu, voici la
suite.

Synthèse rapide de ce qu'on a vu ensemble :

- {{POINT 1 - constat principal observé sur la fiche Google ou le site}}
- {{POINT 2 - levier prioritaire pour les 90 prochains jours}}
- {{POINT 3 - estimation d'impact 12 mois}}

Comme dit, je vous envoie sous 48 heures :

1. Le devis détaillé Carnet Plein® personnalisé à votre situation
   (5 000 € HT setup + 800 €/mois sur 12 mois, options de
   paiement 3× ou 6× détaillées).

2. La convention de prestation V1 (modèle relu par avocat), 22 pages,
   avec en particulier la garantie de continuité gratuite et la
   garantie qualité 90 jours.

3. Les 4 bonus livrables Carnet Plein® en avant-première PDF :
   - Fiche Google Parfaite (checklist 12 points)
   - 30 Réponses prêtes à l'emploi aux avis Google
   - Photos qui Vendent (guide smartphone)
   - Le Devis qui Close à 70% (template Cialdini)

Si vous signez, vous rejoignez la cohort de {{MOIS_PROCHAIN}} qui
démarre le {{1ER_LUNDI}}. Concrètement : un kick-off groupé visio
de 60 min avec les 2 autres artisans de la cohort le 1er lundi du
mois, une visio cohort mensuelle de 45 min à 3 + moi, et un WhatsApp
group privé pour l'entraide entre vous. Il reste {{NB}} places sur
les 3 de la cohort. Signature avant le {{DATE_LIMITE}}.

Aucune pression, prenez le temps qu'il faut. Si questions entre
temps, mon numéro direct : 01 89 72 44 98.

À très bientôt,
Rayan Mpondo (Maïck)
Mad Makers - Carnet Plein®
contact@mad-makers.fr
```

---

### Email F - Post-call si "NOT FIT" (template - envoi manuel)

**Subject :**
```
Suite à notre échange - 2 ressources utiles + qui contacter
```

**Body :**
```
Bonjour {{PRENOM}},

Merci pour notre point de tout à l'heure. Comme convenu, voici les
ressources gratuites que je vous ai mentionnées et que vous pouvez
utiliser dès demain sans avoir besoin de moi.

1. {{RESSOURCE 1 - exemple : "Le guide PDF Fiche Google Parfaite,
   12 points à vérifier sur votre fiche actuelle. C'est l'audit
   gratuit que je viens de vous faire, en version texte que vous
   pouvez relire à tête reposée."}}

2. {{RESSOURCE 2 - exemple : "Le guide PDF Photos qui Vendent,
   5 règles smartphone pour publier des photos de chantiers qui
   valorisent votre travail sur Google."}}

3. {{ORIENTATION éventuelle vers confrère ou autre prestataire
   plus adapté à votre situation}}

Je vous souhaite sincèrement une belle suite. Si dans 6 ou 12 mois
vos besoins évoluent et que Carnet Plein® devient pertinent pour
vous, je serai toujours là.

Cordialement,
Rayan Mpondo (Maïck)
Mad Makers
```

---

## 4. Configuration Calendly - checklist de setup

À cocher une fois pour toutes dans l'interface Calendly :

### Event Type Settings
- [ ] Nom : "Audit Carnet Plein® - 20 minutes"
- [ ] Durée : 20 minutes
- [ ] Description copiée depuis section 1 ci-dessus
- [ ] Couleur événement : orange `#e0541b`
- [ ] Location : Google Meet (auto-link) ou Zoom
- [ ] Time zone visiteur : auto
- [ ] Disponibilités : Lun-Ven 10h-12h et 14h-17h
- [ ] Buffer before : 5 min
- [ ] Buffer after : 15 min
- [ ] Minimum scheduling notice : 24h
- [ ] Maximum days in advance : 30
- [ ] Daily event limit : 4
- [ ] Slug URL : audit-carnet-plein

### Booking form questions (en plus de Name + Email auto)
- [ ] Q1 - Nom entreprise (text, required)
- [ ] Q2 - Métier principal (dropdown, required)
- [ ] Q3 - Zone d'intervention (text, required)
- [ ] Q4 - Taille entreprise (dropdown, required)
- [ ] Q5 - État visibilité Google (multi-select, optional)
- [ ] Q6 - Objectif 12 mois (paragraph, required)

### Workflows (emails auto)
- [ ] Workflow A - Confirmation de booking (subject + body)
- [ ] Workflow B - Rappel J-1 (subject + body)
- [ ] Workflow C - Rappel H-1 (subject + body)
- [ ] Workflow D - Post no-show (subject + body)

### Templates manuels (à garder dans Notion ou Google Docs)
- [ ] Email E - Post-call si FIT (template prêt)
- [ ] Email F - Post-call si NOT FIT (template prêt)

### Branding Calendly (si plan Premium)
- [ ] Logo Mad Makers uploadé
- [ ] Couleur primaire : `#e0541b`
- [ ] URL personnalisée : carnetplein.mad-makers.fr (si CNAME possible)

---

## 5. Process de qualification mentale avant chaque appel

5 minutes de prep à faire AVANT chaque audit Calendly :

1. Ouvrir la fiche GBP du prospect (rechercher son nom + ville sur Google)
2. Compter ses avis, vérifier la note moyenne, regarder ses photos
3. Ouvrir son site s'il en a un (PageSpeed Insights mobile : 30 secondes)
4. Rechercher 1 à 2 concurrents directs sur la même requête (ex "plombier Romainville")
5. Noter 2-3 points concrets à présenter pendant l'audit

Output mental : "Voilà ce que j'ai vu, voilà les 2-3 leviers prioritaires, voilà si Carnet Plein® est fait pour vous ou pas."

---

## 6. Critères de qualification "FIT" vs "NOT FIT"

Après les 20 minutes, tu décides "FIT" ou "NOT FIT" selon ces critères. C'est binaire, pas de "peut-être" qui pourrit le funnel.

### FIT - On envoie le devis et le contrat
- Métier dans la cible : plombier, chauffagiste, électricien, maçon, etc.
- Zone géographique dans les 3 régions cibles (IDF, HDF, Grand Est)
- Taille : 1 à 5 salariés (cible parfaite) ; jusqu'à 10 acceptable
- Posture : ouverture, écoute, pas dans le défi systématique du prix
- Capacité de payer 5 000 € setup en 1 à 6 fois (signal pendant l'appel)
- Pas en surcharge actuelle d'autres prestataires concurrents
- Compatibilité humaine : tu sens que tu vas pouvoir bosser ensemble 12 mois

### NOT FIT - On envoie les 2 ressources gratuites et on remercie
- Hors métier (pourra demander ressources Mad Makers générales)
- Hors zone géographique (recommander confrère local si possible)
- Plus de 15 salariés (besoins différents, prestataires différents)
- Cherche un "lead gen pas cher" : tu vends de la valeur, pas du low-cost
- Refus de l'obligation de moyens (veut une garantie de résultats)
- Mauvais feeling humain : trust your gut, 12 mois c'est long

---

## 7. KPI à suivre sur le funnel Calendly

À reporter dans ta feuille de suivi mensuelle (Notion ou Google Sheets) :

- **Bookings entrants par mois** (volume top de funnel)
- **Show-up rate** (% qui viennent vraiment au RDV) - cible ≥ 70%
- **FIT rate** (% des shows qui sortent FIT) - cible ≥ 40%
- **Signature rate** (% des FIT qui signent dans les 14 jours) - cible ≥ 60%
- **Conversion globale** (booking → signature) - cible ≥ 17% (= 0.7 × 0.4 × 0.6)

Si tu bookes 10 appels par mois et que la conversion globale tient sa cible, tu signes ~1.7 client/mois. Avec un plafond de 3 clients en parallèle livrés sur 12 mois, tu satures rapidement. C'est ton signal pour ouvrir une seconde cohort ou recruter.

---

## 8. Évolutions à prévoir (V2)

À reconsidérer après les 3 premiers clients réels :

- Intégrer Zapier pour push automatique des bookings dans Notion CRM
- Ajouter une étape "pré-qualification" via Tally avant l'accès au Calendly (si trop de bookings non qualifiés)
- Activer le rappel SMS via Brevo en plus des emails Calendly (ouverture +30%)
- Diversifier les créneaux : ajouter 1 créneau "soir" 19h30 pour les artisans en chantier toute la journée
- Mettre en place un "buffer cohort" : si toutes les places de la cohort en cours sont prises, désactiver l'audit Calendly et afficher la page d'attente
