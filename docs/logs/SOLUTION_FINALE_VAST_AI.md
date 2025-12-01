# 🎯 Solution Finale - Vast.ai Sans On-start Script

**Date :** 28 novembre 2025

---

## ❌ Problème Identifié

Le On-start Script **plante systématiquement** à cause de :
- `pip install --upgrade pip` qui échoue
- Installation trop longue qui timeout
- Container qui se destroy avant la fin

---

## ✅ SOLUTION : Démarrage Manuel

### Étape 1 : Template Minimal

**Dans votre template (HORTENSE ou GENEVIEVE) :**

**Section "Ports"** :
```
8000 (TCP)
```

**Section "Environment Variables"** :
```
HF_TOKEN=votre_token_huggingface
PORT=8000
```

**Section "On-start Script"** :
```bash
#!/bin/bash
echo "✅ Instance ready" > /tmp/onstart.log
```

**Section "Launch Mode"** :
```
Jupyter-python notebook + SSH
```

**SAUVEGARDEZ le template.**

---

### Étape 2 : Créer l'Instance

1. **Create New Instance**
2. **Choisir GPU** : RTX 4090
3. **Template** : HORTENSE (ou GENEVIEVE)
4. **Launch**

**Temps de démarrage : 2-3 minutes** (pas 3 heures !)

---

### Étape 3 : Vérifier que Jupyter Démarre

Une fois l'instance "Running" :
- **Cliquez sur le lien Jupyter** (ou l'URL du terminal)
- **Vérifiez que le terminal est accessible**

---

### Étape 4 : Lancer le Déploiement Manuellement

**Dans le terminal Jupyter, copiez-collez TOUT ce bloc :**

```bash
#!/bin/bash
set -e

echo "🚀 Démarrage Spinoza Secours..."

# Aller dans workspace
cd /workspace

# Supprimer ancien clone si existe
rm -rf spinoza-secours maiathon

# Cloner le repository
echo "📥 Clonage du repository..."
git clone https://github.com/FJDaz/maiathon.git

# Aller dans Backend
cd maiathon/Spinoza_Secours_HF/Backend

# Installer dépendances (SANS upgrade pip)
echo "📦 Installation des dépendances..."
pip install --no-cache-dir -r requirements.runpod.txt

# Lancer FastAPI en arrière-plan
echo "🚀 Lancement FastAPI..."
nohup python app_runpod.py > /tmp/spinoza.log 2>&1 &

echo "✅ Déploiement lancé!"
echo "📋 Surveillez les logs: tail -f /tmp/spinoza.log"
```

**Appuyez sur ENTRÉE.**

---

### Étape 5 : Surveiller les Logs

```bash
tail -f /tmp/spinoza.log
```

**Vous devriez voir :**
```
🖥️ GPU disponible: True
🔄 Chargement Mistral 7B (4-bit GPU)...
Loading checkpoint shards: 100%|████████| 3/3 [00:08<00:00]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Temps : 2-5 minutes**

---

### Étape 6 : Tester en Local

```bash
curl http://localhost:8000/health
```

**Attendu :**
```json
{"status":"ok","model":"Mistral 7B + LoRA","gpu_available":true}
```

---

### Étape 7 : Trouver l'URL Publique

Dans l'interface Vast.ai, sur votre instance :

**Cherchez** :
- Section "Network" ou "Ports"
- Un lien/URL pour le port 8000
- Format possible : `https://[instance-id]-8000.vast.ai` ou `http://[ip]:XXXX`

**OU** testez directement :
```
http://[IP_INSTANCE]:8000/health
```

(L'IP est affichée dans les détails de l'instance)

---

### Étape 8 : Mettre à Jour le Frontend

**Fichier :** `Frontend/index_spinoza.html`

**Modifiez la ligne ~127 :**
```javascript
const API_BASE_URL = "http://[URL_TROUVEE]:8000";
```

**Testez le frontend !**

---

## 📋 Checklist Complète

- [ ] Template configuré (Ports, Env Vars, On-start minimal)
- [ ] Instance créée et Running
- [ ] Jupyter accessible
- [ ] Script de déploiement lancé manuellement
- [ ] Logs montrent "Uvicorn running"
- [ ] `curl http://localhost:8000/health` fonctionne
- [ ] URL publique identifiée
- [ ] Frontend mis à jour
- [ ] Test dialogue complet

---

## ⚠️ Important

**Cette méthode est manuelle** mais :
- ✅ **Fonctionne à tous les coups**
- ✅ **Rapide** (5-10 min total)
- ✅ **Vous voyez ce qui se passe**
- ❌ **Il faudra relancer le script** si l'instance reboot

---

## 💰 Coûts

- **RTX 4090** : $0.348/hr
- **Pensez à Destroy** l'instance quand vous ne l'utilisez pas

---

## 🆘 En Cas de Problème

### Si git clone échoue :
```bash
apt-get update && apt-get install -y git
```

### Si pip échoue :
```bash
apt-get update && apt-get install -y python3-pip
```

### Si le modèle ne charge pas :
Vérifiez que HF_TOKEN est défini :
```bash
echo $HF_TOKEN
```

Si vide :
```bash
export HF_TOKEN="votre_token"
```

---

**Cette méthode est LA solution qui marche.**
