# Métiers - portraits artisans

La section `#metiers` de la landing attend les portraits AI-générés dans ce dossier.

## Fichiers attendus (13 portraits)

| # | Fichier | Profil |
|---|---------|--------|
| 01 | `portrait-01-marc.jpg` | Marc D. - Plombier-chauffagiste · Reims |
| 02 | `portrait-02-sophie.jpg` | Sophie L. - Électricienne · Lille |
| 03 | `portrait-03-karim.jpg` | Karim B. - Maçon · Romainville |
| 04 | `portrait-04-helene.jpg` | Hélène R. - Plâtrière-peintre · Strasbourg |
| 05 | `portrait-05-patrick.jpg` | Patrick V. - Plombier · Paris 18e |
| 06 | `portrait-06-mehdi.jpg` | Mehdi K. - Électricien · Roubaix |
| 07 | `portrait-07-olivier.jpg` | Olivier N. - Maçon-rénovateur · Charleville-Mézières |
| 08 | `portrait-08-aicha.jpg` | Aïcha T. - Carreleuse · Saint-Denis |
| 09 | `portrait-09-david.jpg` | David S. - Chauffagiste RGE · Metz |
| 10 | `portrait-10-thomas.jpg` | Thomas G. - Électricien IRVE · Versailles |
| 11 | `portrait-11-julien.jpg` | Julien M. - Couvreur-zingueur · Amiens |
| 12 | `portrait-12-lea.jpg` | Léa P. - Menuisière · Pontoise |
| 13 | `portrait-13-bruno.jpg` | Bruno L. - Étancheur-couvreur · Arras |

## Spec d'image

- **Format** : JPG, 1200×1020 px (ratio 4:3.4, comme les tuiles de la grille)
- **Style** : portrait pro contemporain, fond contextuel discret (atelier, chantier flou en arrière-plan), lumière naturelle, pas de pose marketing exagérée
- **Cadrage** : tête + buste, sujet centré, regard direct ou légèrement décalé
- **Diversité** : âges 28-58, mix hommes/femmes équilibré, origines variées (cohérent avec les prénoms)
- **Tenue** : vêtements de travail crédibles (pas de costumes), accessoires métier OK (mètre, lunettes, casque enlevé)
- **Pas de** : sourires figés "stock photo", logo Mad Makers, bras croisés caricaturaux

## Hot-swap

Une fois les .jpg déposés, recharge la page : les `<img>` chargent et masquent le gradient placeholder.
Si un fichier manque, `onerror="this.style.display='none'"` cache l'image cassée et laisse le gradient + initiales visible - la grille reste fonctionnelle.

## Photos de scènes (déjà présentes)

Les fichiers `cutting-wood.png`, `electrician-*.png`, `renovation-mur-*.png`, etc. sont des photos de chantier/atelier non utilisées dans la grille actuelle.
Réservées pour : section "Preuves" enrichie, futurs case studies, OG image dédiée.
