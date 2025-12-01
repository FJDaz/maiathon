# 🔧 Template Obligatoire - Solution de Contournement

**Date :** 28 novembre 2025  
**Problème :** Impossible de bypasser la sélection de template  
**Solution :** Choisir un template de base, puis override avec notre Dockerfile

---

## ✅ Template à Choisir

### Option 1 : "NVIDIA CUDA" (RECOMMANDÉ) ⭐⭐⭐

**Pourquoi :**
- ✅ Base Docker avec CUDA (nécessaire pour GPU)
- ✅ Image légère (on va la remplacer)
- ✅ Compatible avec notre Dockerfile

**Tags visibles :** ARM, SSH, Jupyter

**Action :** Sélectionner "NVIDIA CUDA" et continuer

---

### Option 2 : "PyTorch (Vast)" (ALTERNATIVE) ⭐⭐

**Pourquoi :**
- ✅ PyTorch pré-installé (utile pour notre modèle)
- ✅ Base Docker
- ⚠️ Peut avoir des dépendances inutiles

**Tags visibles :** ARM, SSH, Jupyter

**Action :** Si "NVIDIA CUDA" n'est pas disponible, choisir "PyTorch (Vast)"

---

## ❌ Templates à ÉVITER

- ❌ **"Ubuntu 22.04 VM"** - VM complète, pas Docker
- ❌ **"Ubuntu Desktop (VM)"** - VM complète, pas Docker
- ❌ **"Hashcat CUDA"** - Application spécifique
- ❌ **"NVIDIA RAPIDS"** - Application spécifique
- ❌ **"Jupyter"** seul - Notebook, pas FastAPI

---

## 🔧 Étapes Après Sélection du Template

### Étape 1 : Sélectionner le Template

1. **Choisir :** "NVIDIA CUDA" (ou "PyTorch (Vast)")
2. **Cliquer** sur le template
3. **Continuer** vers la configuration

### Étape 2 : Override avec Notre Dockerfile

**Dans la page de configuration suivante, cherchez :**

#### Option A : Champ "Dockerfile" ou "Custom Dockerfile"

**Si vous trouvez un champ "Dockerfile" :**
1. Chercher un champ **"Dockerfile"**, **"Custom Dockerfile"** ou **"Override Image"**
2. **Remplacer** le contenu par notre Dockerfile :
   - Copier le contenu de `Backend/Dockerfile.runpod`
   - Coller dans le champ

#### Option B : Option "From GitHub"

**Si vous trouvez une option "From GitHub" ou "Repository" :**
1. Chercher un champ **"Source"**, **"Repository"**, **"GitHub"**
2. **Remplacer** la configuration :
   ```
   Repository: FJDaz/maiathon
   Branch: main
   Dockerfile Path: Spinoza_Secours_HF/Backend/Dockerfile.runpod
   ```

#### Option C : Section "Advanced" ou "Settings"

**Si les options ci-dessus ne sont pas visibles :**
1. Chercher un onglet **"Advanced"**, **"Settings"**, **"Docker"**
2. Chercher une option **"Override Image"** ou **"Custom Dockerfile"**
3. Configurer notre Dockerfile

---

## 📋 Configuration Complète Après Template

### 1. Dockerfile (Override)

**Remplacer le template par :**
```
Repository: FJDaz/maiathon
Branch: main
Dockerfile Path: Spinoza_Secours_HF/Backend/Dockerfile.runpod
```

**OU copier le contenu de `Backend/Dockerfile.runpod`**

### 2. Variables d'Environnement

**Ajouter :**
```
HF_TOKEN=votre_token_hf
PORT=8000
```

### 3. Storage

**Container Disk :** 50-100GB  
**Volume Disk :** Optionnel

### 4. Port

**Port :** 8000 (Internal et External)

---

## ⚠️ Important

**Le template choisi n'est qu'une base :**
- ✅ On va le remplacer par notre Dockerfile
- ✅ Le template sert juste à "débloquer" l'interface
- ✅ Notre Dockerfile (`Dockerfile.runpod`) sera utilisé à la place

**Notre Dockerfile contient :**
- ✅ Python 3.10
- ✅ Toutes les dépendances (`requirements.runpod.txt`)
- ✅ Notre application (`app_runpod.py`)
- ✅ Configuration complète

---

## 🎯 Résumé Action Immédiate

1. **Sélectionner :** "NVIDIA CUDA" (ou "PyTorch (Vast)")
2. **Continuer** vers la configuration
3. **Chercher** un champ "Dockerfile" ou "Repository"
4. **Remplacer** par notre Dockerfile depuis GitHub :
   ```
   Repository: FJDaz/maiathon
   Branch: main
   Dockerfile Path: Spinoza_Secours_HF/Backend/Dockerfile.runpod
   ```
5. **Configurer** variables d'environnement, storage, port

---

## 🔗 Références

- **Dockerfile :** `Backend/Dockerfile.runpod`
- **Repository :** https://github.com/FJDaz/maiathon
- **Plan migration :** `docs/references/PLAN_MIGRATION_VAST_AI.md`

---

**Note :** Même si vous choisissez un template, notre Dockerfile sera utilisé lors du build. Le template sert juste de "porte d'entrée" dans l'interface Vast.ai.

