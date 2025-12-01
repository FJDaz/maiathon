# 🚀 Étapes Post-Création Instance Vast.ai

**Date :** 28 novembre 2025  
**Objectif :** Vérifier le déploiement et tester l'instance

---

## 📋 Checklist Post-Création

### Phase 1 : Vérification Démarrage (15-25 min)

- [ ] Instance créée et en cours de démarrage
- [ ] Accéder aux logs de l'instance
- [ ] Vérifier que le script On-start s'exécute
- [ ] Vérifier le clone du repository GitHub
- [ ] Vérifier l'installation des dépendances
- [ ] Vérifier le téléchargement du modèle Mistral 7B
- [ ] Vérifier le chargement du modèle en GPU
- [ ] Vérifier le démarrage du serveur FastAPI

---

## 🔍 Étape 1 : Accéder aux Logs

### Dans le Dashboard Vast.ai

1. **Aller sur :** https://vast.ai/console/instances
2. **Cliquer** sur votre instance
3. **Section "Logs"** ou **"Console"**

### Ce que vous devriez voir

**Séquence normale des logs :**

```
🚀 Démarrage Spinoza Secours sur Vast.ai...
📥 Clonage du repository GitHub...
Cloning into 'maiathon'...
📦 Installation des dépendances...
Collecting torch>=2.2.0
Collecting transformers>=4.40.0
...
Successfully installed torch transformers peft bitsandbytes...
🖥️ GPU disponible: True
🔄 Chargement Mistral 7B (4-bit GPU)...
Downloading model.safetensors: 100%|████████| 14.2G/14.2G
🔄 Application LoRA Spinoza_Secours...
✅ Modèle Mistral 7B + LoRA chargé!
🚀 Démarrage du serveur FastAPI sur le port 8000...
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## ⏱️ Temps Estimés

| Étape | Temps | Description |
|-------|-------|-------------|
| **Build container** | 5-10 min | Démarrage du container Docker |
| **Clone repo** | 1-2 min | Téléchargement depuis GitHub |
| **Install dépendances** | 3-5 min | Installation pip (torch, transformers, etc.) |
| **Téléchargement modèle** | 10-15 min | Mistral 7B (~14GB) |
| **Chargement GPU** | 1-2 min | Chargement en mémoire GPU |
| **Démarrage FastAPI** | <1 min | Serveur démarre |
| **TOTAL** | **20-35 min** | Premier démarrage |

**⚠️ Note :** Les redémarrages suivants seront plus rapides si vous utilisez Volume Disk (modèle conservé).

---

## 🔍 Étape 2 : Vérifier les Logs Critiques

### Logs à Chercher

#### ✅ Clone Repository Réussi
```
Cloning into 'maiathon'...
```

#### ✅ Dépendances Installées
```
Successfully installed torch transformers peft bitsandbytes accelerate fastapi uvicorn pydantic slowapi
```

#### ✅ GPU Détecté
```
🖥️ GPU disponible: True
```

#### ✅ Modèle Téléchargé
```
Downloading model.safetensors: 100%|████████| 14.2G/14.2G
```

#### ✅ LoRA Appliqué
```
🔄 Application LoRA Spinoza_Secours...
✅ Modèle Mistral 7B + LoRA chargé!
```

#### ✅ Serveur Démarré
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## ⚠️ Problèmes Possibles

### Problème 1 : Clone Échoue

**Symptômes :**
```
fatal: could not read Username for 'https://github.com'
```

**Solution :**
- Vérifier que le repository `FJDaz/maiathon` est public
- Vérifier l'URL GitHub dans le script

### Problème 2 : Dépendances Échouent

**Symptômes :**
```
ERROR: Could not find a version that satisfies the requirement torch>=2.2.0
```

**Solution :**
- Vérifier la connexion internet
- Vérifier que `requirements.runpod.txt` est correct

### Problème 3 : GPU Non Détecté

**Symptômes :**
```
🖥️ GPU disponible: False
```

**Solution :**
- Vérifier que l'instance a bien un GPU (RTX 4090)
- Vérifier les drivers CUDA dans les logs

### Problème 4 : Modèle Ne Télécharge Pas

**Symptômes :**
```
Error: HF_TOKEN not found
```

**Solution :**
- Vérifier que `HF_TOKEN` est bien configuré dans Environment Variables
- Vérifier que le token est valide

### Problème 5 : Port Non Accessible

**Symptômes :**
```
Connection refused
```

**Solution :**
- Vérifier que le port 8000 est bien exposé
- Vérifier que FastAPI démarre (logs)
- Vérifier l'URL publique dans le dashboard

---

## 🌐 Étape 3 : Récupérer l'URL Publique

### Dans le Dashboard Vast.ai

1. **Instance** → **"Connect"** ou **"Public URL"**
2. **Noter l'URL** : `http://votre-instance.vast.ai:8000`

**Format d'URL typique :**
- `http://[instance-id].vast.ai:8000`
- `http://[ip-address]:8000`

---

## 🧪 Étape 4 : Tester les Endpoints

### Test 1 : Health Check

```bash
curl http://votre-instance.vast.ai:8000/health
```

**Réponse attendue :**
```json
{
  "status": "ok",
  "model": "Mistral 7B + LoRA",
  "gpu_available": true
}
```

### Test 2 : Init

```bash
curl http://votre-instance.vast.ai:8000/init
```

**Réponse attendue :**
```json
{
  "greeting": "Bonjour ! Je suis Spinoza. Discutons :\n\n**La liberté est-elle une illusion ?**\n\nQu'en penses-tu ?",
  "history": [[null, "Bonjour ! Je suis Spinoza..."]]
}
```

### Test 3 : Chat

```bash
curl -X POST http://votre-instance.vast.ai:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Bonjour Spinoza, quest-ce que le conatus ?",
    "history": []
  }'
```

**Réponse attendue :**
```json
{
  "reply": "Le conatus, c'est l'effort par lequel chaque chose s'efforce de persévérer dans son être...",
  "history": [
    ["Bonjour Spinoza, quest-ce que le conatus ?", "Le conatus, c'est..."]
  ]
}
```

### Test 4 : Evaluate

```bash
curl -X POST http://votre-instance.vast.ai:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "dialogue": "Spinoza: Bonjour !\nÉlève: Bonjour",
    "score_front": 50
  }'
```

**Réponse attendue :**
```json
{
  "score_final": 65,
  "message_final": "Tu progresses, continue...",
  "details_model": {
    "comprehension": 5,
    "cooperation": 5,
    "progression": 5,
    "total": 15
  }
}
```

---

## 📝 Étape 5 : Script de Test Automatique

**Utiliser le script existant :**

```bash
cd /Users/francois-jeandazin/bergsonAndFriends/Spinoza_Secours_HF/Backend
./test_runpod_deployment.sh http://votre-instance.vast.ai:8000
```

**Ou créer un script de test rapide :**

```bash
#!/bin/bash
API_URL="http://votre-instance.vast.ai:8000"

echo "🧪 Test Health Check..."
curl -s "$API_URL/health" | python3 -m json.tool

echo ""
echo "🧪 Test Init..."
curl -s "$API_URL/init" | python3 -m json.tool

echo ""
echo "🧪 Test Chat..."
curl -s -X POST "$API_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Bonjour", "history": []}' | python3 -m json.tool
```

---

## 🎨 Étape 6 : Mettre à Jour le Frontend

### Fichier à Modifier

**`Frontend/index_spinoza.html`** ligne 127

### Modification

**Avant :**
```javascript
const API_BASE_URL = "https://votre-ngrok-url.ngrok.io";
```

**Après :**
```javascript
const API_BASE_URL = "http://votre-instance.vast.ai:8000";
```

**⚠️ Important :** Remplacer `votre-instance.vast.ai` par votre vraie URL Vast.ai

### Tester le Frontend

1. Ouvrir `Frontend/index_spinoza.html` dans un navigateur
2. Vérifier la console (F12) pour les erreurs
3. Tester un dialogue complet
4. Vérifier que le score s'affiche

---

## 📊 Étape 7 : Monitoring

### Vérifier les Performances

**Dans le dashboard Vast.ai :**
- **GPU Usage** : Devrait être > 0% pendant l'inférence
- **VRAM Usage** : Devrait être ~6-8GB (Mistral 7B 4-bit)
- **Network** : Trafic entrant/sortant

### Vérifier les Coûts

**Dans le dashboard :**
- **Coût actuel** : $0.27-0.29/h (RTX 4090)
- **Temps d'exécution** : Noter les heures
- **Coût total** : Calculer selon usage

---

## ✅ Checklist Complète

### Déploiement
- [ ] Instance créée
- [ ] Logs vérifiés (clone, install, modèle)
- [ ] Serveur FastAPI démarré
- [ ] URL publique récupérée

### Tests
- [ ] Test `/health` réussi
- [ ] Test `/init` réussi
- [ ] Test `/chat` réussi
- [ ] Test `/evaluate` réussi

### Frontend
- [ ] `index_spinoza.html` modifié avec URL Vast.ai
- [ ] Frontend testé dans navigateur
- [ ] Dialogue complet fonctionne
- [ ] Score s'affiche

### Documentation
- [ ] URL Vast.ai notée
- [ ] Date de déploiement notée
- [ ] Configuration documentée

---

## 🔗 Références

- **Script de test :** `Backend/test_runpod_deployment.sh`
- **Frontend guide :** `Frontend/GUIDE_UPDATE_VAST_AI.md`
- **Plan migration :** `docs/references/PLAN_MIGRATION_VAST_AI.md`

---

**✅ Une fois tous les tests réussis, le déploiement est terminé !**

