# 🎯 Marche à Suivre SIMPLE - Vast.ai Instance 28314448

**Date :** 28 novembre 2025
**Instance ID :** 28314448
**IP :** 195.139.22.91
**Port :** 8000

---

## 📌 SITUATION ACTUELLE

Votre instance Vast.ai tourne mais **l'application FastAPI n'est pas déployée** car le script On-start est incorrect.

**L'instance coûte $0.348/heure même si l'application ne tourne pas.**

---

## ✅ SOLUTION IMMÉDIATE : Exécution Manuelle

### Étape 1 : Ouvrir le Terminal

Dans l'interface Vast.ai de votre instance :

1. **Cherchez** un bouton ou lien qui dit :
   - "Console" ou
   - "Jupyter" ou
   - "Terminal" ou
   - "Connect"

2. **Cliquez dessus** pour ouvrir un terminal

### Étape 2 : Copier-Coller le Script Complet

**Dans le terminal ouvert, copiez-collez TOUT ce bloc d'un coup :**

```bash
#!/bin/bash
set -e

echo "🚀 Démarrage Spinoza Secours..."

# Aller dans workspace
cd /workspace

# Supprimer ancien clone si existe
rm -rf maiathon

# Cloner le repository
echo "📥 Clonage du repository..."
git clone https://github.com/FJDaz/maiathon.git

# Aller dans le dossier Backend
cd maiathon/Spinoza_Secours_HF/Backend

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.runpod.txt

# Lancer FastAPI en background
echo "🚀 Lancement de l'application..."
nohup python app_runpod.py > /tmp/spinoza.log 2>&1 &

echo "✅ Application lancée en arrière-plan!"
echo "📋 Pour voir les logs: tail -f /tmp/spinoza.log"
```

**Appuyez sur ENTRÉE**

### Étape 3 : Surveiller les Logs

Dans le même terminal, tapez :

```bash
tail -f /tmp/spinoza.log
```

**Vous devriez voir apparaître :**

```
🖥️ GPU disponible: True
🔄 Chargement Mistral 7B (4-bit GPU)...
✅ Modèle Mistral 7B + LoRA chargé!
🚀 Démarrage du serveur FastAPI sur le port 8000...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**⏱️ Le chargement du modèle prend environ 2-5 minutes.**

### Étape 4 : Tester l'URL

Une fois que vous voyez "Uvicorn running on http://0.0.0.0:8000", testez :

**Dans votre navigateur :**
```
http://195.139.22.91:8000/health
```

**Vous devriez voir :**
```json
{
  "status": "healthy",
  "model": "Mistral 7B + LoRA",
  "device": "cuda"
}
```

---

## 🔧 Si Ça Ne Marche Pas

### Problème 1 : "git: command not found"

Dans le terminal :
```bash
apt-get update && apt-get install -y git
```

Puis recommencez l'Étape 2.

### Problème 2 : "pip: command not found"

Dans le terminal :
```bash
apt-get update && apt-get install -y python3-pip
```

Puis recommencez l'Étape 2.

### Problème 3 : L'URL ne répond pas

Vérifiez que l'application tourne :
```bash
ps aux | grep app_runpod
```

Si rien n'apparaît, relancez :
```bash
cd /workspace/maiathon/Spinoza_Secours_HF/Backend
python app_runpod.py
```

Regardez les erreurs qui s'affichent.

---

## 🎯 APRÈS QUE ÇA MARCHE

### Mettre à Jour le Frontend

**Fichier :** `Frontend/index_spinoza.html`

**Ligne 127, changez :**
```javascript
const API_BASE_URL = "http://195.139.22.91:8000";
```

**Testez le frontend** en ouvrant `index_spinoza.html` dans votre navigateur.

---

## ⚠️ IMPORTANT

### Cette Solution Est Temporaire

Si l'instance redémarre (crash, reboot, etc.), **vous devrez réexécuter le script**.

### Pour Une Solution Permanente

Il faudrait **modifier le script On-start** de l'instance, mais l'interface Vast.ai ne permet pas toujours cela facilement.

**Options :**
1. **Arrêter cette instance** et **créer une nouvelle** avec le bon script On-start dès le départ
2. **Garder cette solution manuelle** et ne pas redémarrer l'instance

### Coûts

- **Actuel :** $0.348/heure = ~$250/mois si 24/7
- **Pensez à arrêter l'instance** quand vous ne l'utilisez pas

---

## 📋 Checklist Rapide

- [ ] Ouvrir le terminal Vast.ai
- [ ] Copier-coller le script complet
- [ ] Attendre 2-5 minutes (chargement modèle)
- [ ] Vérifier logs avec `tail -f /tmp/spinoza.log`
- [ ] Tester `http://195.139.22.91:8000/health`
- [ ] Mettre à jour `Frontend/index_spinoza.html` ligne 127
- [ ] Tester le frontend

---

## 🆘 Si Vous Êtes Bloqué

1. **Copiez-moi les logs** que vous voyez dans `/tmp/spinoza.log`
2. **Dites-moi exactement** quel bouton/lien vous voyez dans l'interface Vast.ai
3. **Faites une capture d'écran** de l'interface si possible

---

**Action immédiate :** Ouvrez le terminal de votre instance Vast.ai et exécutez le script de l'Étape 2.
