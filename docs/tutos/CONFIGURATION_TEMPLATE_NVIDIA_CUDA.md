# 🔧 Configuration Template NVIDIA CUDA - Spinoza Secours

**Date :** 28 novembre 2025  
**Template :** NVIDIA CUDA  
**Objectif :** Override avec notre Dockerfile depuis GitHub

---

## 📋 Modifications à Apporter

### 1. Image Path:Tag (CRITIQUE)

**Champ actuel :**
```
Image Path:Tag: vastai/base-image:@vastai-automatic-tag
```

**⚠️ Problème :** Ce champ pointe vers une image Docker Hub, pas vers notre GitHub.

**Solutions possibles :**

#### Option A : Chercher "From GitHub" ou "Dockerfile"

**Cherchez dans la page :**
- Un bouton **"From GitHub"**
- Un onglet **"Dockerfile"**
- Une section **"Source"** ou **"Repository"**
- Un lien **"Use Dockerfile"** ou **"Custom Dockerfile"**

**Si vous trouvez cette option :**
```
Repository: FJDaz/maiathon
Branch: main
Dockerfile Path: Spinoza_Secours_HF/Backend/Dockerfile.runpod
```

#### Option B : Utiliser On-start Script (CONTournement)

**Si pas d'option GitHub directe :**

1. **Laisser l'Image Path tel quel** (pour l'instant)
2. **Modifier l'On-start Script** pour cloner et build notre Dockerfile
3. Voir section "On-start Script" ci-dessous

---

### 2. Ports (MODIFIER)

**Ports actuels :**
```
1111, 6006, 8080, 8384, 72299
```

**À modifier pour :**
```
8000
```

**Action :**
- **Supprimer** tous les ports existants
- **Ajouter** le port **8000**

---

### 3. Environment Variables (MODIFIER)

**Variables actuelles :**
```
OPEN_BUTTON_PORT=1111
OPEN_BUTTON_TOKEN=1
JUPYTER_DIR=/
DATA_DIRECTORY=/workspace/
PORTAL_CONFIG=...
```

**À remplacer par :**
```
HF_TOKEN=votre_token_hf
PORT=8000
```

**Action :**
- **Supprimer** toutes les variables existantes
- **Ajouter** :
  - `HF_TOKEN` = `votre_token_hf` (remplacer par votre vrai token)
  - `PORT` = `8000`

---

### 4. Disk Space (MODIFIER)

**Container disk actuel :**
```
32 GB
```

**À modifier pour :**
```
50 GB minimum (100 GB recommandé pour Qwen 14B futur)
```

**Action :**
- **Changer** de 32 GB à **50-100 GB**

---

### 5. On-start Script (MODIFIER si Option B)

**Script actuel :**
```
entrypoint.sh
```

**Si pas d'option GitHub directe, remplacer par :**

```bash
#!/bin/bash
# Clone repository GitHub
cd /workspace
git clone https://github.com/FJDaz/maiathon.git
cd maiathon/Spinoza_Secours_HF/Backend

# Build Docker image from Dockerfile
docker build -f Dockerfile.runpod -t spinoza-secours .

# Run container
docker run -d \
  -p 8000:8000 \
  -e HF_TOKEN=$HF_TOKEN \
  -e PORT=8000 \
  spinoza-secours
```

**⚠️ Note :** Cette option est un contournement. L'option GitHub directe est préférable.

---

### 6. Launch Mode (MODIFIER)

**Mode actuel :**
```
Jupyter-python notebook + SSH
```

**À modifier pour :**
```
Interactive shell server, SSH
```

**OU** laisser tel quel si vous voulez garder Jupyter pour debug.

---

## ✅ Configuration Recommandée (Résumé)

### Si Option GitHub Disponible :

1. **Image Path:Tag :** Laisser tel quel (sera override par GitHub)
2. **From GitHub :**
   - Repository: `FJDaz/maiathon`
   - Branch: `main`
   - Dockerfile Path: `Spinoza_Secours_HF/Backend/Dockerfile.runpod`
3. **Ports :** `8000` uniquement
4. **Environment Variables :**
   - `HF_TOKEN` = `votre_token_hf`
   - `PORT` = `8000`
5. **Disk Space :** `50-100 GB`
6. **On-start Script :** Laisser vide ou supprimer

### Si Pas d'Option GitHub (Contournement) :

1. **Image Path:Tag :** Laisser `vastai/base-image:@vastai-automatic-tag`
2. **Ports :** `8000` uniquement
3. **Environment Variables :**
   - `HF_TOKEN` = `votre_token_hf`
   - `PORT` = `8000`
4. **Disk Space :** `50-100 GB`
5. **On-start Script :** Utiliser le script ci-dessus

---

## 🔍 Où Chercher l'Option GitHub

**Dans cette page de configuration, cherchez :**

1. **Un bouton** "From GitHub" ou "Use Dockerfile"
2. **Un onglet** "Dockerfile" ou "Source"
3. **Un lien** "Custom Dockerfile" ou "Build from GitHub"
4. **Une section** "Source" ou "Repository" en haut de la page
5. **Un champ** "Dockerfile" séparé de "Image Path"

**Si vous ne trouvez pas :**
- Faire défiler toute la page
- Chercher dans les onglets en haut
- Vérifier s'il y a un bouton "Advanced" ou "More Options"

---

## 📝 Checklist Avant de Créer l'Instance

- [ ] Option GitHub trouvée OU On-start Script modifié
- [ ] Ports : 8000 uniquement
- [ ] Environment Variables : HF_TOKEN et PORT configurés
- [ ] Disk Space : 50-100 GB
- [ ] Launch Mode : Interactive shell (ou Jupyter si debug)
- [ ] Token HF_TOKEN remplié par votre vrai token

---

## 🚀 Après Configuration

1. **Cliquer** "Create" ou "Deploy"
2. **Attendre** le build (5-10 min)
3. **Attendre** le chargement du modèle (10-15 min)
4. **Récupérer** l'URL publique
5. **Tester** les endpoints

---

## 🔗 Références

- **Dockerfile :** `Backend/Dockerfile.runpod`
- **Repository :** https://github.com/FJDaz/maiathon
- **Plan migration :** `docs/references/PLAN_MIGRATION_VAST_AI.md`

---

**Important :** Cherchez d'abord l'option "From GitHub" ou "Dockerfile" dans la page. Si vous ne la trouvez pas, utilisez le contournement avec On-start Script.

