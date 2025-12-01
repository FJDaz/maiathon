# 🔄 Synchronisation GitHub pour Vast.ai

**Date :** Janvier 2025  
**Repo GitHub :** https://github.com/FJDaz/Spinoza_secours  
**Objectif :** Vérifier et synchroniser les fichiers nécessaires pour déploiement Vast.ai

---

## ✅ État Actuel

### Fichiers Locaux Présents

✅ **Fichiers nécessaires pour Vast.ai :**
- `Backend/Dockerfile.runpod` ✅ Existe localement
- `Backend/app_runpod.py` ✅ Existe localement
- `Backend/requirements.runpod.txt` ✅ Existe localement
- `Backend/Notebooks/Spinoza_Secours_DER` ✅ Existe localement (nouveau fichier)

### État Git Local

⚠️ **Problème détecté :** Les fichiers ne sont **pas trackés par git**

```bash
# Vérification
git status Backend/Dockerfile.runpod Backend/app_runpod.py Backend/requirements.runpod.txt
# Résultat : ?? (non trackés)
```

### État GitHub

**Vérification en cours...** (voir section Vérification Finale)

---

## 📋 Actions à Effectuer

### 1. Vérifier Structure Repo GitHub

**Vérifier si le dossier `Backend/` existe sur GitHub :**
- Aller sur : https://github.com/FJDaz/Spinoza_secours
- Vérifier si le dossier `Backend/` existe
- Vérifier si les fichiers sont présents :
  - `Backend/Dockerfile.runpod`
  - `Backend/app_runpod.py`
  - `Backend/requirements.runpod.txt`

### 2. Ajouter les Fichiers au Repo (Si Absents)

**⚠️ Résultat vérification :** Les fichiers retournent **404** → **Ils ne sont pas sur GitHub**

**Option A : Script Automatique (Recommandé)**

```bash
cd /Users/francois-jeandazin/bergsonAndFriends/Spinoza_Secours_HF
./push_to_github.sh
```

**Option B : Commandes Manuelles**

```bash
cd /Users/francois-jeandazin/bergsonAndFriends/Spinoza_Secours_HF

# Ajouter les fichiers nécessaires
git add Backend/Dockerfile.runpod
git add Backend/app_runpod.py
git add Backend/requirements.runpod.txt

# Ajouter aussi le nouveau fichier si nécessaire
git add Backend/Notebooks/Spinoza_Secours_DER

# Vérifier ce qui sera commité
git status

# Commit
git commit -m "Add Vast.ai deployment files (Dockerfile, app_runpod, requirements)"

# Push vers GitHub
git push github main
# ou
git push spinoza-secours main
```

### 3. Vérifier Structure Attendue sur GitHub

**Structure attendue pour Vast.ai :**

```
Spinoza_secours/
├── Backend/
│   ├── Dockerfile.runpod          ✅ Nécessaire
│   ├── app_runpod.py              ✅ Nécessaire
│   ├── requirements.runpod.txt     ✅ Nécessaire
│   └── Notebooks/
│       └── Spinoza_Secours_DER    ✅ Nouveau fichier
└── ...
```

### 4. Configuration Vast.ai

**Une fois les fichiers sur GitHub, utiliser :**

- **Repository** : `FJDaz/Spinoza_secours`
- **Branch** : `main`
- **Dockerfile Path** : `Backend/Dockerfile.runpod`
- **Dockerfile Context** : `/` (racine du repo)

---

## 🔍 Vérification Finale

**Checklist avant déploiement Vast.ai :**

- [ ] Fichiers présents sur GitHub : https://github.com/FJDaz/Spinoza_secours/tree/main/Backend
- [ ] `Dockerfile.runpod` accessible
- [ ] `app_runpod.py` accessible
- [ ] `requirements.runpod.txt` accessible
- [ ] Structure correcte (dossier `Backend/` à la racine)

**Test d'accès GitHub (après push) :**
```bash
# Vérifier que les fichiers sont accessibles
curl -s https://raw.githubusercontent.com/FJDaz/Spinoza_secours/main/Backend/Dockerfile.runpod | head -5

# Devrait retourner le contenu du Dockerfile (pas 404)
```

**État actuel :** ❌ Fichiers retournent 404 → **Action requise : Push vers GitHub**

---

## 📝 Notes

- **Remote GitHub configuré :** `github` et `spinoza-secours` pointent vers https://github.com/FJDaz/Spinoza_secours.git
- **Fichiers locaux :** Tous présents et prêts
- **Action requise :** Ajouter et pousser vers GitHub si absents

---

**Prochaine étape :** Une fois les fichiers sur GitHub, suivre l'Option B du plan de migration pour créer le template personnalisé sur Vast.ai.

