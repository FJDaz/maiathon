# ✅ Corrections Finales - Configuration Vast.ai

**Date :** 28 novembre 2025  
**Statut :** Configuration partiellement complétée

---

## ✅ Déjà Fait

- ✅ **Launch Mode** : "Docker ENTRYPOINT" sélectionné
- ✅ **Docker Options** : `-p 8000:8000 -e HF_TOKEN=$HF_TOKEN -e PORT=8000`
- ✅ **On-start Script** : Partiellement modifié (contient `python app_runpod.py`)

---

## ⚠️ À Corriger

### 1. Ports (CRITIQUE)

**Problème :** Les anciens ports sont toujours présents
```
1111, 6006, 8080, 8384, 72299
```

**Action :**
1. **Supprimer** tous ces ports (cliquer sur le X ou supprimer)
2. **Ajouter** uniquement le port **8000** dans le champ "Port"
3. **Vérifier** que seul `8000` apparaît dans la liste

---

### 2. Environment Variables (CRITIQUE)

**Problème :** Les anciennes variables sont toujours présentes
```
OPEN_BUTTON_PORT=1111
OPEN_BUTTON_TOKEN=1
JUPYTER_DIR=/
DATA_DIRECTORY=/workspace/
PORTAL_CONFIG=...
```

**Action :**
1. **Supprimer** toutes ces variables (cliquer sur le X ou supprimer)
2. **Ajouter** deux nouvelles variables :

| Key | Value |
|-----|-------|
| `HF_TOKEN` | `votre_token_hf` ⚠️ **REMPLACER par votre vrai token** |
| `PORT` | `8000` |

**⚠️ Important :** Remplacer `votre_token_hf` par votre vrai token Hugging Face !

---

### 3. On-start Script (VÉRIFIER)

**Vérifier que le script complet est présent :**

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

**Action :**
- Vérifier que tout le script est présent (pas seulement la dernière ligne)
- Si manquant, copier-coller le script complet ci-dessus

---

### 4. Disk Space (MODIFIER)

**Problème :** Toujours à 32 GB

**Action :**
- **Changer** de `32 GB` à **`50 GB`** minimum (ou `100 GB` pour Qwen 14B futur)
- Utiliser le slider ou le champ numérique

---

## 📋 Checklist Finale

Avant de cliquer "Create", vérifier :

- [ ] **Ports :** Seul `8000` est présent (autres supprimés)
- [ ] **Environment Variables :**
  - [ ] `HF_TOKEN` = `votre_token_hf` ⚠️ **REMPLACER**
  - [ ] `PORT` = `8000`
  - [ ] Toutes les anciennes variables supprimées
- [ ] **On-start Script :** Script complet présent (pas seulement la dernière ligne)
- [ ] **Disk Space :** 50-100 GB (pas 32 GB)
- [ ] **Docker Options :** `-p 8000:8000 -e HF_TOKEN=$HF_TOKEN -e PORT=8000` ✅ (déjà fait)
- [ ] **Launch Mode :** "Docker ENTRYPOINT" ✅ (déjà fait)

---

## 🚀 Après "Create"

### 1. Attendre le Déploiement

**Temps estimé :** 15-25 minutes
- Build container : 5-10 min
- Clone repo + install dépendances : 2-3 min
- Téléchargement modèle Mistral 7B : 10-15 min
- Chargement GPU : 1-2 min

### 2. Vérifier les Logs

**Dans le dashboard Vast.ai :**
- Instance → "Logs" ou "Console"
- Chercher : `✅ Modèle Mistral 7B + LoRA chargé!`
- Chercher : `🚀 Démarrage du serveur FastAPI sur le port 8000...`
- Chercher : `INFO:     Uvicorn running on http://0.0.0.0:8000`

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

**⚠️ CRITIQUE :** Ne pas oublier de remplacer `votre_token_hf` par votre vrai token !

**Format :** `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Où l'obtenir :** https://huggingface.co/settings/tokens

### 2. Ports

**Vérifier que :**
- Seul le port 8000 est présent
- Les anciens ports (1111, 6006, etc.) sont supprimés
- Le port 8000 est bien exposé dans Docker Options

### 3. On-start Script

**Vérifier que le script complet est présent :**
- Clone du repository
- Installation des dépendances
- Lancement de l'application

---

## 🔧 Si Problème

### Problème : Ports en conflit

**Solution :** Supprimer tous les anciens ports, garder uniquement 8000

### Problème : Variables d'environnement en conflit

**Solution :** Supprimer toutes les anciennes variables, ajouter uniquement HF_TOKEN et PORT

### Problème : Script ne s'exécute pas

**Solution :** Vérifier que le script complet est présent (pas seulement la dernière ligne)

---

## 📝 Résumé Actions Restantes

1. **Supprimer** tous les anciens ports (1111, 6006, 8080, 8384, 72299)
2. **Ajouter** uniquement le port 8000
3. **Supprimer** toutes les anciennes variables d'environnement
4. **Ajouter** HF_TOKEN (avec votre vrai token) et PORT=8000
5. **Vérifier** que le script On-start est complet
6. **Changer** Disk Space de 32 GB à 50-100 GB
7. **Cliquer** "Create"

---

**✅ Une fois ces corrections faites, vous pouvez créer l'instance !**

