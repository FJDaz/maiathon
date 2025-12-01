# ✅ Configuration Finale Vast.ai - Spinoza Secours

**Date :** 28 novembre 2025  
**Template :** NVIDIA CUDA  
**Méthode :** On-start Script

---

## 📋 Configuration à Appliquer

### 1. Image Path:Tag

**Laisser tel quel :**
```
vastai/base-image:@vastai-automatic-tag
```

---

### 2. Ports

**Supprimer tous les ports existants et ajouter :**
```
8000
```

**Action :**
- Supprimer : `1111`, `6006`, `8080`, `8384`, `72299`
- Ajouter : `8000`

---

### 3. Environment Variables

**Supprimer toutes les variables existantes et ajouter :**

| Key | Value |
|-----|-------|
| `HF_TOKEN` | `votre_token_hf` ⚠️ **REMPLACER par votre vrai token** |
| `PORT` | `8000` |

**Variables à supprimer :**
- `OPEN_BUTTON_PORT`
- `OPEN_BUTTON_TOKEN`
- `JUPYTER_DIR`
- `DATA_DIRECTORY`
- `PORTAL_CONFIG`

---

### 4. Docker Options

**Remplacer par :**
```
-p 8000:8000 -e HF_TOKEN=$HF_TOKEN -e PORT=8000
```

**Ou laisser vide si les variables d'environnement sont configurées séparément.**

---

### 5. On-start Script

**Remplacer `entrypoint.sh` par :**

```bash
#!/bin/bash
set -e

echo "🚀 Démarrage Spinoza Secours sur Vast.ai..."

# Créer répertoire de travail
mkdir -p /workspace/spinoza-secours
cd /workspace/spinoza-secours

# Cloner le repository GitHub
echo "📥 Clonage du repository GitHub..."
if [ ! -d "maiathon" ]; then
    git clone https://github.com/FJDaz/maiathon.git
fi

cd maiathon/Spinoza_Secours_HF/Backend

# Installer les dépendances Python
echo "📦 Installation des dépendances..."
pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.runpod.txt

# Lancer l'application FastAPI
echo "🚀 Lancement de l'application FastAPI..."
python app_runpod.py
```

**⚠️ Important :** Copier-coller ce script dans le champ "On-start Script"

---

### 6. Disk Space

**Modifier de 32 GB à :**
```
50 GB minimum (100 GB recommandé pour Qwen 14B futur)
```

**Action :**
- Changer `32` → `50` ou `100`

---

### 7. Launch Mode

**Choisir :**
```
Interactive shell server, SSH
```

**OU** laisser "Jupyter" si vous voulez garder Jupyter pour debug.

---

## ✅ Checklist Avant "Create"

- [ ] **Ports :** 8000 uniquement (autres supprimés)
- [ ] **Environment Variables :**
  - [ ] `HF_TOKEN` = `votre_token_hf` ⚠️ **REMPLACER**
  - [ ] `PORT` = `8000`
  - [ ] Autres variables supprimées
- [ ] **Docker Options :** `-p 8000:8000 -e HF_TOKEN=$HF_TOKEN -e PORT=8000`
- [ ] **On-start Script :** Script ci-dessus copié
- [ ] **Disk Space :** 50-100 GB
- [ ] **Launch Mode :** Interactive shell (ou Jupyter si debug)

---

## 🚀 Après "Create"

### 1. Attendre le Build

**Temps estimé :** 5-10 minutes

**Ce qui se passe :**
- Container démarre
- On-start Script s'exécute
- Clone du repository GitHub
- Installation des dépendances Python
- Chargement du modèle Mistral 7B + LoRA (~10-15 min)

### 2. Vérifier les Logs

**Dans le dashboard Vast.ai :**
- Aller dans votre instance
- Section "Logs" ou "Console"
- Chercher : `✅ Modèle Mistral 7B + LoRA chargé!`
- Chercher : `🚀 Démarrage du serveur FastAPI sur le port 8000...`

### 3. Récupérer l'URL Publique

**Dans le dashboard :**
- Instance → "Connect" ou "Public URL"
- URL type : `http://votre-instance.vast.ai:8000`

### 4. Tester les Endpoints

```bash
# Health check
curl http://votre-instance.vast.ai:8000/health

# Init
curl http://votre-instance.vast.ai:8000/init

# Chat
curl -X POST http://votre-instance.vast.ai:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Bonjour", "history": []}'
```

---

## ⚠️ Points d'Attention

### 1. Token HF_TOKEN

**⚠️ CRITIQUE :** Remplacer `votre_token_hf` par votre vrai token Hugging Face.

**Format :** `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Où l'obtenir :** https://huggingface.co/settings/tokens

### 2. Port 8000

**Vérifier que :**
- Le port 8000 est bien exposé
- Aucun autre service n'utilise le port 8000
- L'URL publique utilise le port 8000

### 3. Disk Space

**50 GB minimum nécessaire pour :**
- Modèle Mistral 7B : ~14GB
- LoRA adapter : ~100MB
- Système + dépendances : ~5GB
- Marge : ~30GB

**100 GB recommandé pour :**
- Migration future vers Qwen 14B (~28GB)

### 4. On-start Script

**Le script s'exécute à chaque démarrage :**
- ✅ Clone le repo (si pas déjà présent)
- ✅ Installe les dépendances
- ✅ Lance l'application

**Temps d'exécution :**
- Première fois : ~15-20 min (clone + install + modèle)
- Redémarrages suivants : ~10-15 min (modèle retéléchargé si Container Disk)

---

## 🔧 Troubleshooting

### Problème : Script ne s'exécute pas

**Vérifier :**
- Les logs de l'instance
- Que le script est bien copié dans "On-start Script"
- Que les permissions sont correctes

### Problème : Port 8000 non accessible

**Vérifier :**
- Que le port 8000 est bien dans la liste des ports
- Que l'application FastAPI démarre (logs)
- Que l'URL publique est correcte

### Problème : Modèle ne charge pas

**Vérifier :**
- Que `HF_TOKEN` est correct
- Que le token a les permissions "read"
- Les logs pour voir les erreurs

---

## 📝 Résumé Configuration

```
Template: NVIDIA CUDA
Image: vastai/base-image:@vastai-automatic-tag
Ports: 8000
Environment Variables:
  - HF_TOKEN=votre_token_hf
  - PORT=8000
Docker Options: -p 8000:8000 -e HF_TOKEN=$HF_TOKEN -e PORT=8000
On-start Script: [Script ci-dessus]
Disk Space: 50-100 GB
Launch Mode: Interactive shell, SSH
```

---

## 🔗 Références

- **On-start Script :** `Backend/onstart_vast_ai.sh`
- **Dockerfile :** `Backend/Dockerfile.runpod`
- **Repository :** https://github.com/FJDaz/maiathon
- **Plan migration :** `docs/references/PLAN_MIGRATION_VAST_AI.md`

---

**✅ Une fois la configuration terminée, cliquer "Create" et attendre le déploiement !**

