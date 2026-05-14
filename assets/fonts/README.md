# Fonts - carnetplein.mad-makers.fr

Le site attend les fichiers suivants pour charger AeonikPro et DotConnect.
**Tant qu'ils ne sont pas présents, le navigateur tombe sur Geist (Bunny Fonts) puis system-ui.**

## Fichiers attendus

| Fichier | Famille | Poids | Notes |
|---------|---------|-------|-------|
| `AeonikPro-Regular.woff2` | AeonikPro | 400 | Body, paragraphes, lead |
| `AeonikPro-Medium.woff2` | AeonikPro | 500 | Headings, CTA, labels |
| `DotConnect-Medium.woff2` | DotConnect | 500 | Accents italiques (`<em>` dans les titres) |

## Où les obtenir

AeonikPro et DotConnect sont des fontes commerciales (CoType Foundry pour Aeonik). License à acheter :
- AeonikPro : https://www.cotypefoundry.com/fonts/aeonik
- DotConnect : font custom du brand "(dot)connect" - pas disponible publiquement.

## Si tu n'as pas la license

Le fallback automatique est **Geist** (Vercel, gratuit via Bunny Fonts) + Geist Mono pour les labels.
Visuellement très proche d'AeonikPro - la majorité des visiteurs n'auront jamais l'occasion de comparer.

## Hot-swap

Une fois les .woff2 déposés dans ce dossier, recharge la page - aucun build, aucun cache à purger.
Les `@font-face` sont déclarés en `font-display: swap` donc le passage est invisible.
