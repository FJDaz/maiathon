# Rapport : Issues Git Commit et Push - Déploiement Vast.ai

**Date :** 27 novembre 2025  
**Contexte :** Synchronisation des fichiers de déploiement Vast.ai vers GitHub  
**Repository :** `https://github.com/FJDaz/Spinoza_secours`

---

## 📋 Résumé Exécutif

**Statut :** ❌ **ÉCHEC** - Push bloqué par GitHub Push Protection  
**Cause principale :** Détection de secrets (tokens) dans les fichiers et l'historique Git  
**Fichiers ciblés :** `Backend/Dockerfile.runpod`, `Backend/app_runpod.py`, `Backend/requirements.runpod.txt`

---

## 🔴 Problèmes Identifiés

### 1. **GitHub Push Protection - Secrets Détectés**

#### 1.1 Token Ngrok dans `Spinoza_Secours_DER`
- **Fichier :** `Backend/Notebooks/Spinoza_Secours_DER`
- **Ligne :** 27
- **Type :** `NGROK_TOKEN`
- **Action :** ✅ Retiré du commit (mais fichier toujours présent localement)

#### 1.2 Token GitHub dans l'historique Git
- **Fichier :** `RAG_Spinoza_secours.ipynb`
- **Ligne :** 1383
- **Type :** GitHub Personal Access Token (`ghp_*`)
- **Commit :** `d90601c060f9a566bf52848021612b64a8436b67`
- **Action :** ❌ Présent dans l'historique, non résolu

**Message d'erreur GitHub :**
```
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote: - GITHUB PUSH PROTECTION
remote:   - Push cannot contain secrets
remote:     —— GitHub Personal Access Token ——————————————————————
remote:      locations:
remote:        - commit: d90601c060f9a566bf52848021612b64a8436b67
remote:          path: Spinoza_Secours_HF/RAG_Spinoza_secours.ipynb:1383
```

---

### 2. **Problèmes de Structure de Répertoires**

#### 2.1 Divergence Local vs GitHub
- **Local :** Fichiers dans `/Backend/` (racine du repo local)
- **GitHub :** Structure attendue `/Spinoza_Secours_HF/Backend/`
- **Impact :** Fichiers non trouvés lors des tentatives de copie

#### 2.2 Fichiers absents dans `github/main`
- Les fichiers `Backend/Dockerfile.runpod`, `app_runpod.py`, `requirements.runpod.txt` n'existent pas dans la branche `github/main`
- Tentatives de création d'une nouvelle branche `vast-ai-deployment` échouées

---

### 3. **Problèmes de Branches Git**

#### 3.1 Branches divergentes
- **Branche locale `clean-main` :** 143 commits d'avance
- **Branche distante `origin/clean-main` :** 36 commits différents
- **Statut :** Divergence non résolue

#### 3.2 Tentatives de push
- Push vers `github/main` : ❌ Bloqué par Push Protection
- Push vers `github/clean-main` : ❌ Branches divergentes
- Push vers nouvelle branche `vast-ai-deployment` : ❌ Fichiers non trouvés

---

## 🔍 Détails Techniques

### Tentatives de Résolution Effectuées

1. **Retrait du token Ngrok**
   - ✅ `Spinoza_Secours_DER` retiré du staging
   - ⚠️ Fichier toujours présent localement (ligne 27)

2. **Nettoyage des commits**
   - Tentative de `git reset HEAD~1 --soft`
   - Tentative de commit avec seulement 3 fichiers Backend
   - ❌ Échec : commit inclut toujours 60+ fichiers

3. **Création de nouvelle branche**
   - Création de `vast-ai-deployment` basée sur `github/main`
   - ❌ Fichiers Backend non trouvés dans cette branche

4. **Vérification des fichiers**
   - ✅ Fichiers existent localement dans `/Backend/`
   - ❌ Structure GitHub différente (`/Spinoza_Secours_HF/Backend/`)

---

## 📊 État Actuel

### Fichiers Locaux
```
⚠️ Backend/Dockerfile.runpod : NON TROUVÉ (peut-être supprimé ou déplacé)
⚠️ Backend/app_runpod.py : NON TROUVÉ (peut-être supprimé ou déplacé)
⚠️ Backend/requirements.runpod.txt : NON TROUVÉ (peut-être supprimé ou déplacé)
✅ Backend/Dockerfile.vast.cuda : Présent
✅ Backend/auto_sleep.py : Présent
✅ Backend/monitor_vast_ai.sh : Présent
⚠️ Backend/Notebooks/Spinoza_Secours_DER : Contient NGROK_TOKEN ligne 27 (fichier supprimé du staging)
```

**Note :** Les fichiers de déploiement Vast.ai (`Dockerfile.runpod`, `app_runpod.py`, `requirements.runpod.txt`) ne sont plus présents dans le répertoire Backend. Ils ont peut-être été supprimés ou déplacés.

### Fichiers sur GitHub
```
❌ Spinoza_Secours_HF/Backend/Dockerfile.runpod (404)
❌ Spinoza_Secours_HF/Backend/app_runpod.py (404)
❌ Spinoza_Secours_HF/Backend/requirements.runpod.txt (404)
```

### Branches Git
- `clean-main` : Branche locale avec fichiers Backend
- `vast-ai-deployment` : Nouvelle branche basée sur `github/main` (sans fichiers Backend)
- `github/main` : Branche distante (contient token dans historique)

---

## 🛠️ Solutions Recommandées

### Solution 1 : Nettoyer l'historique Git (Recommandé)
```bash
# Option A : Utiliser git filter-branch ou BFG Repo-Cleaner
# Pour retirer le token GitHub de l'historique
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch Spinoza_Secours_HF/RAG_Spinoza_secours.ipynb" \
  --prune-empty --tag-name-filter cat -- --all

# Option B : Utiliser GitHub's secret scanning unblock URL
# https://github.com/FJDaz/Spinoza_secours/security/secret-scanning/unblock-secret/364eOrgypCLFzo1HHosOFUljHi3
```

### Solution 2 : Créer un nouveau commit propre
```bash
# 1. Trouver les fichiers Backend
find . -name "Dockerfile.runpod" -o -name "app_runpod.py" -o -name "requirements.runpod.txt" | grep -v ".git"

# 2. Vérifier absence de secrets dans les fichiers cibles
grep -r -E "(HF_TOKEN|NGROK_TOKEN|GITHUB_TOKEN|ghp_[0-9a-zA-Z]{36})" \
  [chemin_vers_fichiers] --exclude-dir=.git --exclude-dir=venv

# 3. Créer structure GitHub (selon structure réelle trouvée)
mkdir -p Spinoza_Secours_HF/Backend
cp [chemin_local]/Dockerfile.runpod Spinoza_Secours_HF/Backend/
cp [chemin_local]/app_runpod.py Spinoza_Secours_HF/Backend/
cp [chemin_local]/requirements.runpod.txt Spinoza_Secours_HF/Backend/

# 4. Commit et push
git add Spinoza_Secours_HF/Backend/
git commit -m "Add Vast.ai deployment files"
git push github vast-ai-deployment:main
```

### Solution 3 : Utiliser GitHub Secret Scanning Unblock
Si le token dans l'historique est un faux positif ou déjà révoqué :
1. Aller sur : https://github.com/FJDaz/Spinoza_secours/security/secret-scanning/unblock-secret/364eOrgypCLFzo1HHosOFUljHi3
2. Autoriser le push une fois
3. Pousser les fichiers

---

## ⚠️ Actions Immédiates Requises

1. **Localiser les fichiers de déploiement**
   - Rechercher `Dockerfile.runpod`, `app_runpod.py`, `requirements.runpod.txt`
   - Vérifier s'ils existent dans une autre branche ou ont été supprimés

2. **Nettoyer `Spinoza_Secours_DER`**
   - Retirer ou commenter la ligne 27 contenant `NGROK_TOKEN`
   - Ajouter à `.gitignore` si nécessaire

3. **Résoudre le token dans l'historique**
   - Utiliser `git filter-branch` ou BFG Repo-Cleaner
   - OU utiliser l'URL GitHub pour autoriser le push : https://github.com/FJDaz/Spinoza_secours/security/secret-scanning/unblock-secret/364eOrgypCLFzo1HHosOFUljHi3

4. **Créer la structure GitHub correcte**
   - Copier les fichiers dans `Spinoza_Secours_HF/Backend/`
   - Vérifier l'absence de secrets avant commit

5. **Vérifier les fichiers avant push**
   ```bash
   # Script de vérification
   grep -r -E "(HF_TOKEN|NGROK_TOKEN|GITHUB_TOKEN|ghp_)" \
     Spinoza_Secours_HF/Backend/ --exclude-dir=.git --exclude-dir=venv --exclude-dir=__pycache__
   ```

---

## 📝 Notes

- **GitHub Push Protection** est activé et fonctionne correctement
- Les tokens détectés doivent être révoqués si exposés
- La structure de répertoires GitHub diffère du local
- **Fichiers Backend manquants :** `Dockerfile.runpod`, `app_runpod.py`, `requirements.runpod.txt` ne sont plus présents localement
- **Branche actuelle :** `vast-ai-deployment` (basée sur `github/main`)
- **Remotes configurés :** 
  - `github` : https://github.com/FJDaz/Spinoza_secours.git
  - `origin` : https://github.com/FJDaz/bergson-and-friends.git
  - `hf`, `hf-secours`, `3phi` : HuggingFace Spaces
  - `spinoza-secours` : https://github.com/FJDaz/Spinoza_secours.git
- **Commit problématique :** `d90601c` contient token GitHub dans `RAG_Spinoza_secours.ipynb:1383`
- **Commits récents :** Aucun commit Vast.ai réussi depuis le 27/11/2025

---

## 🔗 Références

- [GitHub Push Protection Documentation](https://docs.github.com/code-security/secret-scanning/working-with-secret-scanning-and-push-protection)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [Git Filter-Branch](https://git-scm.com/docs/git-filter-branch)

---

**Prochaines étapes :** Nettoyer les secrets, créer la structure GitHub correcte, et pousser les fichiers de déploiement Vast.ai.

