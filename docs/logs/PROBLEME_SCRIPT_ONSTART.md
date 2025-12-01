# ⚠️ Problème : Script On-start Non Exécuté

**Date :** 28 novembre 2025  
**Instance ID :** 28314448  
**Statut :** Instance Running mais script On-start non exécuté

---

## 🔍 Diagnostic

### Ce que les Logs Montrent

**✅ Ce qui fonctionne :**
- Instance démarrée (Running)
- Jupyter démarré sur port 8080
- SSH disponible
- Packages système installés (curl, git, etc.)

**❌ Ce qui manque :**
- ❌ Clone du repository GitHub (`maiathon`)
- ❌ Installation des dépendances Python (`requirements.runpod.txt`)
- ❌ Lancement de l'application FastAPI (`app_runpod.py`)
- ❌ Aucun log de notre script On-start

**Conclusion :** Le script On-start n'a **pas été exécuté** ou n'est **pas le bon script**.

---

## 🔧 Solutions

### Solution 1 : Vérifier le Script On-start (RECOMMANDÉ)

**Dans l'interface Vast.ai :**

1. **Aller dans la page de détails de l'instance**
2. **Onglet "Onstart"** ou **"Environment"**
3. **Vérifier le script** présent

**Le script devrait être :**

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

**Si le script est différent ou manquant :**
- Le modifier dans l'interface
- Redémarrer l'instance

---

### Solution 2 : Exécuter Manuellement via Terminal/SSH

**Si le script On-start ne peut pas être modifié :**

1. **Cliquer sur le bouton "Terminal"** ou **">_Connect"** dans l'interface
2. **Exécuter manuellement les commandes :**

```bash
# Créer répertoire
mkdir -p /workspace/spinoza-secours
cd /workspace/spinoza-secours

# Cloner le repository
git clone https://github.com/FJDaz/maiathon.git

# Aller dans le répertoire Backend
cd maiathon/Spinoza_Secours_HF/Backend

# Installer les dépendances
pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.runpod.txt

# Lancer l'application
python app_runpod.py
```

**⚠️ Note :** Cette solution est temporaire. L'application s'arrêtera si le terminal se ferme.

---

### Solution 3 : Utiliser Jupyter pour Exécuter

**Alternative via Jupyter :**

1. **Cliquer sur le bouton "Jupyter"** dans l'interface
2. **Créer un nouveau notebook**
3. **Exécuter les cellules :**

```python
# Cellule 1 : Clone
import os
os.chdir('/workspace')
!git clone https://github.com/FJDaz/maiathon.git

# Cellule 2 : Install
os.chdir('/workspace/maiathon/Spinoza_Secours_HF/Backend')
!pip install --no-cache-dir --upgrade pip
!pip install --no-cache-dir -r requirements.runpod.txt

# Cellule 3 : Run (en background)
import subprocess
subprocess.Popen(['python', 'app_runpod.py'])
```

---

## 🎯 Action Immédiate Recommandée

### Option A : Modifier le Script On-start (Permanent)

1. **Dans l'interface Vast.ai :**
   - Instance → **"Edit"** ou **"Settings"**
   - Onglet **"Onstart"**
   - **Remplacer** le script par celui ci-dessus
   - **Sauvegarder**
   - **Redémarrer** l'instance

### Option B : Exécuter Manuellement (Rapide)

1. **Cliquer sur "Terminal"** ou **">_Connect"**
2. **Exécuter** les commandes ci-dessus
3. **Vérifier** que FastAPI démarre

---

## 📋 Vérification

**Après exécution du script, vous devriez voir dans les logs :**

```
🚀 Démarrage Spinoza Secours sur Vast.ai...
📥 Clonage du repository GitHub...
Cloning into 'maiathon'...
📦 Installation des dépendances...
Collecting torch>=2.2.0
...
🖥️ GPU disponible: True
🔄 Chargement Mistral 7B (4-bit GPU)...
✅ Modèle Mistral 7B + LoRA chargé!
🚀 Démarrage du serveur FastAPI sur le port 8000...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## ⚠️ Problème Identifié

**Le script On-start actuel dans les logs est :**
```
env >> /etc/environment
mkdir -p ${DATA_DIRECTORY:-/workspace/}
```

**C'est le script par défaut du template PyTorch, pas notre script Spinoza Secours !**

**Solution :** Il faut modifier le script On-start dans la configuration de l'instance.

---

**Action immédiate :** Vérifier et modifier le script On-start dans l'interface Vast.ai, puis redémarrer l'instance.

