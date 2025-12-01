# 🎯 Choisir le Template Vast.ai - Spinoza Secours

**Date :** 28 novembre 2025  
**Situation :** Vous voyez une liste de templates et vous devez choisir

---

## ❌ Ne PAS Choisir un Template Pré-configuré

### Pourquoi ?

**Aucun template pré-configuré ne correspond à Spinoza Secours :**

| Template | Pourquoi ❌ |
|----------|-------------|
| **Cuda 12.8** | Base CUDA seulement, pas d'application |
| **Hashcat CUDA** | Spécifique hashcat, pas adapté |
| **Jupyter** | Notebook, pas FastAPI |
| **NVIDIA RAPIDS** | Spécifique RAPIDS, pas adapté |
| **Ubuntu 22.04 VM** | VM complète, pas Docker container |
| **Ubuntu Desktop (VM)** | VM complète, pas Docker container |

**Tous ces templates ne contiennent pas :**
- ❌ Notre application FastAPI (`app_runpod.py`)
- ❌ Notre Dockerfile (`Dockerfile.runpod`)
- ❌ Les dépendances spécifiques (`requirements.runpod.txt`)
- ❌ La configuration Mistral 7B + LoRA

---

## ✅ Solution : Option B - Dockerfile Personnalisé

### Ce qu'il faut chercher

**Cherchez une option qui permet d'utiliser un Dockerfile personnalisé :**

1. **Option "Custom Dockerfile"** ou **"Dockerfile"**
2. **Option "From GitHub"** ou **"GitHub Repository"**
3. **Option "Docker"** (pas VM)
4. **Option "Container"** (pas VM)

**⚠️ Important :** Ne pas choisir de template de la liste. Chercher une option pour configurer manuellement.

---

## 🔍 Où Trouver l'Option Dockerfile Personnalisé

### Option 1 : Bouton "Skip" ou "Configure Manually"

**Si vous voyez un bouton :**
- **"Skip"** (ignorer les templates)
- **"Configure Manually"** (configurer manuellement)
- **"Custom"** (personnalisé)
- **"Advanced"** (avancé)

**→ Cliquez dessus pour accéder à la configuration Docker personnalisée**

### Option 2 : Onglet "Docker" ou "Container"

**Cherchez un onglet :**
- **"Docker"**
- **"Container"**
- **"Custom"**
- **"Advanced"**

**→ Cliquez pour voir les options Docker**

### Option 3 : Champ "Source" ou "Repository"

**Dans la page de configuration, cherchez un champ :**
- **"Source"**
- **"Repository"**
- **"GitHub"**
- **"Dockerfile"**
- **"Custom Dockerfile"**

**→ Entrez les informations GitHub**

---

## 📋 Configuration Recommandée

### Si vous trouvez l'option "From GitHub" :

**Remplir :**
```
Repository: FJDaz/maiathon
Branch: main
Dockerfile Path: Spinoza_Secours_HF/Backend/Dockerfile.runpod
Dockerfile Context: / (racine)
```

### Si vous trouvez un champ "Dockerfile" :

**Option A :** Copier le contenu de `Backend/Dockerfile.runpod` et coller

**Option B :** Utiliser une image Docker Hub (si vous l'avez publiée)

---

## 🎯 Étapes à Suivre

### 1. Ignorer les Templates

**Ne pas sélectionner :**
- ❌ Cuda 12.8
- ❌ Hashcat CUDA
- ❌ Jupyter
- ❌ NVIDIA RAPIDS
- ❌ Ubuntu 22.04 VM
- ❌ Ubuntu Desktop (VM)

### 2. Chercher l'Option Docker Personnalisé

**Chercher :**
- ✅ Bouton "Skip" ou "Configure Manually"
- ✅ Onglet "Docker" ou "Container"
- ✅ Champ "Source" / "Repository" / "Dockerfile"

### 3. Configurer le Dockerfile

**Si option GitHub :**
```
Repository: FJDaz/maiathon
Branch: main
Dockerfile Path: Spinoza_Secours_HF/Backend/Dockerfile.runpod
```

**Si champ Dockerfile direct :**
- Copier le contenu de `Backend/Dockerfile.runpod`

### 4. Continuer la Configuration

**Ensuite configurer :**
- Variables d'environnement (`HF_TOKEN`, `PORT`)
- Storage (Container Disk 50-100GB)
- Port (8000)

---

## ⚠️ Si Vous Ne Trouvez Pas l'Option

### Cas 1 : Interface Différente

**L'interface Vast.ai peut varier. Essayez :**
1. Faire défiler toute la page
2. Chercher dans tous les onglets
3. Chercher "Advanced" ou "Settings"
4. Vérifier s'il y a un bouton "Skip Templates"

### Cas 2 : Template de Base Acceptable

**Si vous devez absolument choisir un template :**
- **"Cuda 12.8"** pourrait servir de base
- **MAIS** il faudra quand même configurer un Dockerfile personnalisé par-dessus

**⚠️ Ce n'est pas recommandé** - mieux vaut trouver l'option Dockerfile personnalisé.

### Cas 3 : Documentation Vast.ai

**Consulter :**
- https://docs.vast.ai/
- Section "Creating Instances"
- Section "Custom Dockerfile"

---

## ✅ Résumé

**Question :** "Il faut du Docker, on est d'accord ?"

**Réponse :** ✅ **OUI, il faut Docker, MAIS :**
- ❌ **Ne PAS choisir un template pré-configuré** de la liste
- ✅ **Chercher l'option "Custom Dockerfile" ou "From GitHub"**
- ✅ **Utiliser notre Dockerfile :** `Spinoza_Secours_HF/Backend/Dockerfile.runpod`
- ✅ **Depuis GitHub :** `FJDaz/maiathon` branch `main`

**Action immédiate :**
1. **Ignorer tous les templates** de la liste
2. **Chercher un bouton "Skip"** ou **"Configure Manually"**
3. **Chercher un champ "Dockerfile"** ou **"GitHub Repository"**
4. **Configurer avec notre Dockerfile**

---

## 🔗 Références

- **Plan migration :** `docs/references/PLAN_MIGRATION_VAST_AI.md`
- **Section Template :** Lignes 240-390
- **Dockerfile :** `Backend/Dockerfile.runpod`
- **Repository :** https://github.com/FJDaz/maiathon

---

**Astuce :** Si vous ne trouvez pas l'option, faites une capture d'écran de la page de configuration et je pourrai vous guider plus précisément !

