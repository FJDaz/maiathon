# 📊 Topo Complet - Déploiement Spinoza Secours sur Vast.ai

**Date :** 28 novembre 2025  
**Statut :** Instance créée mais application non déployée  
**Instance ID :** 28314448

---

## ✅ Ce Qui a Été Fait

### 1. Préparation GitHub ✅

- ✅ **Repository créé :** https://github.com/FJDaz/maiathon
- ✅ **Fichiers poussés :**
  - `Backend/Dockerfile.runpod`
  - `Backend/app_runpod.py` (18KB, application FastAPI complète)
  - `Backend/requirements.runpod.txt`
  - Structure complète du projet (142 fichiers)

### 2. Configuration Instance Vast.ai ✅

- ✅ **Instance créée :** ID 28314448
- ✅ **GPU :** 1x RTX 4090 (24GB VRAM)
- ✅ **Localisation :** IP 195.139.22.91
- ✅ **Template :** NVIDIA CUDA (obligatoire, pas de bypass)
- ✅ **Ports configurés :** 8000
- ✅ **Variables d'environnement :**
  - `HF_TOKEN` = [votre token]
  - `PORT` = 8000
- ✅ **Disk Space :** 50GB (Container Disk)
- ✅ **Docker Options :** `-p 8000:8000 -e HF_TOKEN=$HF_TOKEN -e PORT=8000`
- ✅ **Status :** Running (4 minutes d'uptime)

---

## ❌ Problèmes Identifiés

### Problème 1 : Script On-start Incorrect ⚠️ CRITIQUE

**Situation actuelle :**
- Le script On-start dans l'instance est celui du template PyTorch par défaut :
  ```
  env >> /etc/environment
  mkdir -p ${DATA_DIRECTORY:-/workspace/}
  ```

**Notre script requis :**
```bash
#!/bin/bash
set -e

echo "🚀 Démarrage Spinoza Secours sur Vast.ai..."

mkdir -p /workspace/spinoza-secours
cd /workspace/spinoza-secours

echo "📥 Clonage du repository GitHub..."
if [ ! -d "maiathon" ]; then
    git clone https://github.com/FJDaz/maiathon.git
fi

cd maiathon/Spinoza_Secours_HF/Backend

echo "📦 Installation des dépendances..."
pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.runpod.txt

echo "🚀 Lancement de l'application FastAPI..."
python app_runpod.py
```

**Impact :**
- ❌ Repository GitHub non cloné
- ❌ Dépendances Python non installées
- ❌ Application FastAPI non lancée
- ❌ Modèle Mistral 7B non chargé
- ❌ Port 8000 non utilisé (FastAPI ne tourne pas)

### Problème 2 : URL Publique Non Trouvée ⚠️

**Situation :**
- Le bouton "Connect" ouvre le terminal SSH, pas l'URL publique
- L'URL publique n'est pas visible directement

**Solution :**
- L'URL devrait être : `http://195.139.22.91:8000` (IP + port)
- Mais FastAPI ne tourne pas encore (voir Problème 1)

---

## 📋 État Actuel de l'Instance

### Configuration Matérielle ✅

- **GPU :** RTX 4090 (24GB VRAM) - 0.3GB utilisés (vide)
- **CPU :** AMD EPYC 7763 64-Core (21.3/256 CPU utilisés)
- **RAM :** 0/43.0 GB utilisés
- **Disk :** 0.1/50.0 GB utilisés
- **Network :** 16 ports disponibles
- **Status :** Running (mais application non lancée)

### Services Actifs

- ✅ **Jupyter :** Démarré sur port 8080
- ✅ **SSH :** Disponible
- ❌ **FastAPI :** Non démarré (script On-start incorrect)

### Logs Actuels

**Ce qu'on voit :**
- Installation packages système (curl, git, etc.)
- Démarrage Jupyter
- Erreurs SSH port forwarding (non critiques)

**Ce qu'on ne voit PAS :**
- Clone du repository GitHub
- Installation dépendances Python (torch, transformers, etc.)
- Chargement modèle Mistral 7B
- Démarrage FastAPI

---

## 🎯 Ce Qu'il Faut Faire MAINTENANT

### Action 1 : Modifier le Script On-start (CRITIQUE)

**Dans l'interface Vast.ai :**

1. **Sur la page de votre instance** (Instance ID: 28314448)
2. **Chercher un bouton "Edit"** ou **"Settings"** ou **"Configure"**
3. **Onglet "Onstart"** ou **"On-start Script"**
4. **Remplacer le script actuel** par notre script complet (voir ci-dessus)
5. **Sauvegarder**
6. **Redémarrer l'instance** (bouton "Restart")

**OU** si pas d'option Edit :

1. **Arrêter l'instance** (bouton "Stop")
2. **Créer une nouvelle instance** avec le bon script On-start dès le départ
3. **OU** utiliser la solution manuelle ci-dessous

---

### Action 2 : Solution Manuelle (Alternative Rapide)

**Si vous ne pouvez pas modifier le script On-start :**

1. **Cliquer sur "Open Jupyter terminal"** dans la boîte de dialogue
2. **OU** utiliser SSH (si configuré)
3. **Exécuter manuellement :**

```bash
# Créer répertoire
mkdir -p /workspace/spinoza-secours
cd /workspace/spinoza-secours

# Cloner le repository
git clone https://github.com/FJDaz/maiathon.git

# Aller dans Backend
cd maiathon/Spinoza_Secours_HF/Backend

# Installer dépendances
pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.runpod.txt

# Lancer FastAPI (en background pour que ça continue)
nohup python app_runpod.py > /tmp/spinoza.log 2>&1 &
```

4. **Vérifier les logs :**
```bash
tail -f /tmp/spinoza.log
```

**⚠️ Note :** Cette solution est temporaire. Si l'instance redémarre, il faudra réexécuter.

---

### Action 3 : Trouver l'URL Publique

**Méthode 1 : IP Directe**

L'URL devrait être :
```
http://195.139.22.91:8000
```

**Méthode 2 : Dans l'Interface**

1. **Page de l'instance** → Chercher section **"Network"** ou **"Ports"**
2. **Chercher** l'URL publique mappée au port 8000
3. **Format possible :** `http://[instance-id].vast.ai:8000` ou `http://[ip]:8000`

**Méthode 3 : Via Jupyter Terminal**

```bash
# Voir les ports exposés
netstat -tlnp | grep 8000

# Voir l'IP publique
curl ifconfig.me
```

---

## 📊 Checklist Complète

### Configuration ✅
- [x] Instance créée (ID: 28314448)
- [x] GPU RTX 4090 sélectionné
- [x] Port 8000 configuré
- [x] Variables d'environnement (HF_TOKEN, PORT)
- [x] Disk Space 50GB
- [x] Docker Options configurés

### Déploiement ❌
- [ ] Script On-start corrigé
- [ ] Repository GitHub cloné
- [ ] Dépendances Python installées
- [ ] Modèle Mistral 7B chargé
- [ ] FastAPI démarré sur port 8000

### Tests ⏳
- [ ] URL publique identifiée
- [ ] Test `/health` réussi
- [ ] Test `/init` réussi
- [ ] Test `/chat` réussi
- [ ] Test `/evaluate` réussi

### Frontend ⏳
- [ ] `index_spinoza.html` modifié avec URL Vast.ai
- [ ] Frontend testé
- [ ] Dialogue complet fonctionne

---

## 🔧 Fichiers Disponibles

### Localement ✅

- `Backend/Dockerfile.runpod` - Dockerfile pour Vast.ai
- `Backend/app_runpod.py` - Application FastAPI complète
- `Backend/requirements.runpod.txt` - Dépendances Python
- `Backend/onstart_vast_ai.sh` - Script On-start complet
- `Backend/test_runpod_deployment.sh` - Script de test

### Sur GitHub ✅

- Repository : https://github.com/FJDaz/maiathon
- Branch : `main`
- Tous les fichiers de déploiement présents

---

## 🎯 Prochaines Étapes (Ordre de Priorité)

### 1. IMMÉDIAT : Corriger le Script On-start

**Option A : Modifier dans l'interface**
- Instance → Edit/Settings → Onstart
- Remplacer le script
- Redémarrer

**Option B : Exécution manuelle**
- Terminal Jupyter
- Exécuter les commandes manuellement
- Lancer FastAPI en background

### 2. Vérifier le Déploiement

**Dans les logs, chercher :**
```
🚀 Démarrage Spinoza Secours sur Vast.ai...
📥 Clonage du repository GitHub...
📦 Installation des dépendances...
🖥️ GPU disponible: True
🔄 Chargement Mistral 7B (4-bit GPU)...
✅ Modèle Mistral 7B + LoRA chargé!
🚀 Démarrage du serveur FastAPI sur le port 8000...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 3. Tester l'URL Publique

**Une fois FastAPI démarré :**
```bash
# Health check
curl http://195.139.22.91:8000/health

# OU si URL différente
curl http://[votre-url-vast-ai]:8000/health
```

### 4. Mettre à Jour le Frontend

**Fichier :** `Frontend/index_spinoza.html` ligne 127

**Modifier :**
```javascript
const API_BASE_URL = "http://195.139.22.91:8000";
// OU
const API_BASE_URL = "http://[votre-url-vast-ai]:8000";
```

---

## 💰 Coûts Actuels

- **Instance :** $0.348/hr (RTX 4090)
- **Uptime actuel :** ~4 minutes
- **Coût actuel :** ~$0.02
- **Si 24/7 :** ~$250/mois

**⚠️ Important :** Arrêter l'instance si vous ne l'utilisez pas pour éviter les coûts inutiles.

---

## 🔗 Références Utiles

### Documentation
- **Plan migration :** `docs/references/PLAN_MIGRATION_VAST_AI.md`
- **Guide post-création :** `docs/tutos/ETAPES_POST_CREATION_VAST_AI.md`
- **Problème script :** `docs/logs/PROBLEME_SCRIPT_ONSTART.md`

### Fichiers
- **Script On-start :** `Backend/onstart_vast_ai.sh`
- **Application :** `Backend/app_runpod.py`
- **Dockerfile :** `Backend/Dockerfile.runpod`

### URLs
- **Repository GitHub :** https://github.com/FJDaz/maiathon
- **Instance Vast.ai :** https://cloud.vast.ai/instances
- **Instance ID :** 28314448
- **IP Publique :** 195.139.22.91

---

## ⚠️ Points d'Attention

### 1. Script On-start

**Le problème principal :** Le script On-start n'est pas le bon. Il faut le corriger pour que l'application se déploie automatiquement.

### 2. URL Publique

**Format attendu :** `http://195.139.22.91:8000` ou `http://[instance-id].vast.ai:8000`

**Mais :** FastAPI doit être lancé pour que l'URL fonctionne.

### 3. Coûts

**L'instance tourne et coûte $0.348/hr même si l'application n'est pas lancée.**

**Recommandation :** Corriger le script rapidement ou arrêter l'instance en attendant.

---

## 🎯 Action Immédiate Recommandée

### Option 1 : Modifier le Script (Permanent) ⭐⭐⭐

1. **Instance → Edit/Settings**
2. **Onglet Onstart**
3. **Remplacer le script**
4. **Sauvegarder et Redémarrer**

### Option 2 : Exécution Manuelle (Rapide) ⭐⭐

1. **Jupyter Terminal**
2. **Exécuter les commandes**
3. **Lancer FastAPI en background**

### Option 3 : Recréer l'Instance (Si Edit Impossible) ⭐

1. **Arrêter instance actuelle**
2. **Créer nouvelle instance**
3. **Configurer le bon script On-start dès le départ**

---

## 📝 Résumé Exécutif

**✅ Fait :**
- Instance créée et running
- Configuration matérielle OK
- Fichiers sur GitHub

**❌ Problème :**
- Script On-start incorrect
- Application non déployée
- FastAPI non lancé

**🎯 Solution :**
- Modifier le script On-start
- OU exécuter manuellement
- Redémarrer/relancer

**⏭️ Après :**
- Vérifier logs
- Tester URL publique
- Mettre à jour frontend

---

**Action immédiate :** Corriger le script On-start dans l'interface Vast.ai ou exécuter manuellement via Jupyter Terminal.

