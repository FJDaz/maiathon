# 📚 Documentation Spinoza Secours HF

## Structure des Dossiers

```
docs/
├── tutos/             # Guides pas à pas, tutoriels
├── notes/             # Notes rapides, TODO, réflexions
├── references/        # Explications techniques, concepts
├── guides/            # Guides pratiques, procédures
├── analyses/          # Analyses détaillées, bilans
├── tests/             # Documentation des tests
│   └── archives/      # Archives automatiques
├── supports/         # Support technique
└── logs/             # Logs et traces d'exécution
```

## 📁 Contenu par Catégorie

### `docs/tutos/`
Guides pas à pas :
- **ordre-execution-colab.md** : Ordre d'exécution des cellules dans Colab
- **commandes-colab-git.md** : Commandes Git pour Colab
- **cellule-maieuthon-backend.md** : Ajouter la cellule Maïeuthon au notebook

### `docs/notes/`
Notes rapides et réflexions :
- **mapping-bergson-hf-vs-racine.md** : Mapping entre fichiers HF et racine
- **proposition-code-colab.md** : Proposition de code pour Colab

### `docs/references/`
Explications techniques et concepts :
- **arborescence-repo.md** : Structure du repository
- **calibration-evaluation.md** : Méthode de calibration de l'évaluateur
- **prompt-systeme-hybride.md** : Documentation du prompt système hybride

### `docs/analyses/`
Analyses détaillées et bilans :
- **analyse-whoosh-rag-client.md** : Analyse Whoosh RAG côté client
- **rapport-prompt-sys-rag.md** : Rapport sur les prompts système et RAG
- **audit-bordel-local.md** : Audit de l'organisation locale

### `docs/tests/`
Documentation des tests :
- **resultats-test-prompt.md** : Résultats des tests de prompts

### `docs/supports/`
Support technique :
- (À compléter selon besoins)

### `docs/logs/`
Logs et traces d'exécution :
- Dialogues réels pour calibration
- Logs d'exécution Colab

## 📝 Conventions

- **Fichiers .md** : Documentation Markdown
- **Noms de fichiers** : En minuscules avec tirets (`-`)
- **Dates** : Format `YYYY-MM-DD` dans les noms de fichiers archivés

## 🔄 Archivage Automatique

Les documents de plus de 1 jour dans `docs/tests/` sont automatiquement déplacés vers `docs/tests/archives/` par les skills Cursor.

