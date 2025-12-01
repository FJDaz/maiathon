# 📁 Organisation Documentation - Référence pour Skills Cursor

## Structure des Dossiers (Mise à jour)

```
docs/
├── tutos/             # Tutoriels pas à pas
├── notes/             # Notes rapides, TODO, réflexions
├── references/        # Explications techniques, concepts, articulations, architectures
├── guides/            # Guides pratiques, procédures
├── resumes/           # Résumés et clarifications
├── analyses/          # Analyses détaillées, bilans
├── tests/             # Documentation des tests
│   └── archives/      # Archives automatiques
├── supports/         # Support technique (fixes, schémas)
└── logs/             # Logs et traces d'exécution
```

## 📋 Liste Explicite des Fichiers

⚠️ **IMPORTANT** : Utiliser la liste explicite dans `LISTE_EXPLICITE_FICHIERS.md`, pas de règles heuristiques.

Voir `docs/references/LISTE_EXPLICITE_FICHIERS.md` pour la liste complète et exacte de tous les fichiers par dossier.

## 🎯 Instructions pour Skills Cursor

### Workspaces concernés
- **bergsonAndFriends** : `/Users/francois-jeandazin/bergsonAndFriends`
- **I Amiens** : `/Users/francois-jeandazin/Documents/En Cours/Crea/NUX/I Amiens`
- **NUX_FT** : `/Users/francois-jeandazin/NUX_FT`

### ✅ Méthode Hybride : Liste Explicite + Inférences Génériques

**Étape 1 : Liste Explicite (PRIORITÉ)**
- Vérifier si le nom exact du fichier est dans `docs/references/LISTE_EXPLICITE_FICHIERS.md`
- Si oui → Placer dans le dossier indiqué (sans exception)

**Étape 2 : Inférences Génériques (si pas dans la liste)**
- Si le fichier commence par `FIX_` → `docs/supports/`
- Si le fichier commence par `ANALYSE_` ou `analyse-` → `docs/analyses/`
- Si le fichier commence par `GUIDE_` ou `OU_PLACER_` → `docs/guides/`
- Si le fichier commence par `RESUME_` ou `RECAP_` → `docs/resumes/`
- Si le fichier commence par `TEST_` ou `test-` → `docs/tests/`
- Si le fichier contient `CLARIFICATION` → `docs/supports/`
- Si le fichier contient `ADAPTATION` → `docs/supports/`
- Si le fichier contient `SCHEMA` ou `SCHÉMA` → `docs/supports/`
- Si le fichier contient `ARCHITECTURE` ou `ARTICULATION` → `docs/references/`
- Si le fichier contient `VOIR_REPONSE` ou `DEBUG` → `docs/supports/`

**Étape 3 : Demander à l'Utilisateur (si aucune règle ne s'applique)**
- Si le fichier n'est ni dans la liste explicite, ni couvert par les règles génériques → Demander à l'utilisateur

### Règles à appliquer

1. **Classement de nouveaux fichiers** :
   - Vérifier si le nom exact est dans `LISTE_EXPLICITE_FICHIERS.md`
   - Si oui → Utiliser le dossier indiqué
   - Si non → Utiliser les inférences génériques

2. **Vérification et renommage (LOGIQUE INVERSE)** :
   - Après avoir déterminé la destination, vérifier que le nom correspond au pattern de la section
   - Si incohérent → Proposer de renommer selon `REGLE_NOM_FICHIER.md`
   - Format standard : minuscules, tirets (`-`), extension `.md`

3. **Archivage automatique** :
   - Les documents de plus de 1 jour dans `docs/tests/` → `docs/tests/archives/`

4. **Conventions de nommage** :
   - Fichiers .md : Markdown
   - Noms en minuscules avec tirets (`-`) pour nouveaux fichiers
   - Patterns par section : voir `REGLE_NOM_FICHIER.md`
   - Dates : Format `YYYY-MM-DD` pour archives

## 📝 Mise à jour des Skills

Les skills Cursor doivent être mis à jour pour :
- Utiliser la liste explicite (pas de règles heuristiques)
- Refléter cette nouvelle organisation dans les trois workspaces

