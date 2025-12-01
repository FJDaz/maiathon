# 🚀 Préparation Repository Maiathon

**Date :** 27 novembre 2025  
**Repository :** https://github.com/FJDaz/maiathon  
**Type :** Public  
**Statut :** Repository vide, prêt pour initialisation

---

## 📋 Checklist Pré-Push

### ✅ Vérifications Effectuées

- [x] Remote `maiathon` configuré
- [x] Recherche de secrets (aucun codé en dur)
- [x] Structure du projet vérifiée
- [x] .gitignore présent

### 📁 Contenu à Pousser

**Structure complète :**
```
maiathon/
├── Backend/          (25 fichiers)
│   ├── Notebooks/    (notebooks Colab)
│   ├── auto_sleep.py
│   └── monitor_vast_ai.sh
├── Frontend/         (40 fichiers)
│   └── index_spinoza.html
├── ML/               (8 fichiers)
├── docs/             (62 fichiers)
│   ├── references/
│   ├── logs/
│   └── tutos/
└── README.md
```

### ⚠️ Fichiers à Exclure

- `.env` (variables d'environnement)
- `*.pyc`, `__pycache__/`
- `.DS_Store`
- Fichiers avec secrets (vérifiés)

---

## 🎯 Étapes de Push

### 1. Créer Branche Propre

```bash
git checkout -b main-clean
```

### 2. Vérifier Contenu

```bash
git status
git log --oneline -5
```

### 3. Commit Initial (Si Nécessaire)

```bash
# Si des fichiers non trackés
git add .
git commit -m "Initial commit: Maïathon - Spinoza Secours"
```

### 4. Push vers Maiathon

```bash
git push maiathon main-clean:main --force
```

---

## 📝 Notes

- **Repository public** : Assurez-vous qu'aucun secret n'est inclus
- **Premier push** : Utiliser `--force` car le repo est vide
- **Branche** : Pousser `main-clean` vers `main` sur GitHub

---

## 🔗 Références

- Repository : https://github.com/FJDaz/maiathon
- Documentation : `docs/references/PLAN_MIGRATION_VAST_AI.md`


