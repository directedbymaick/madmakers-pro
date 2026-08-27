# Mad Makers Pro

Workspace principal des projets Mad Makers.

## Dossiers

- `carnet-plein/` : site, documents internes et outils du projet Carnet Plein®.
- `projects/` : autres sites et expérimentations, notamment les différentes versions d’ARMD.
- `workspace/` : audits, entretiens, imports et cahiers des charges.
- `tools/` : ressources de développement partagées.

Les fichiers cachés et les fichiers de configuration présents à la racine servent au dépôt Git et au déploiement Vercel. Aucun contenu de projet ne doit être ajouté directement à la racine.

## Structure

```text
Mad Makers Pro/
├── carnet-plein/
│   ├── site/
│   ├── internal/
│   └── tools/
├── projects/
│   ├── armd/
│   └── experiments/
├── workspace/
└── tools/
```

## Carnet Plein® en local

```powershell
python carnet-plein/tools/dev/serve.py
```

Le routage défini dans `vercel.json` conserve les URLs publiques historiques de Carnet Plein® malgré son rangement dans un dossier dédié.
