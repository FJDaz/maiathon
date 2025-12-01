# ⚠️ Problème : Connection Refused - Instance Inaccessible

**Date :** 28 novembre 2025  
**Erreur :** `ERR_CONNECTION_REFUSED` sur `http://195.139.22.91:8000`  
**Cause probable :** FastAPI n'est plus en cours d'exécution

---

## 🔍 Diagnostic

### Causes Possibles

1. **FastAPI arrêté** (le plus probable)
   - Le processus a été tué
   - L'instance a redémarré
   - Le terminal a été fermé et le processus s'est arrêté

2. **Instance arrêtée**
   - L'instance Vast.ai s'est arrêtée
   - Redémarrage de l'instance

3. **Port non exposé**
   - Le port 8000 n'est plus mappé
   - Problème de configuration réseau

---

## ✅ Solutions

### Solution 1 : Vérifier l'État de l'Instance (PRIORITÉ)

**Dans l'interface Vast.ai :**

1. **Aller sur :** https://cloud.vast.ai/instances
2. **Vérifier le statut** de l'instance ID 28314448 :
   - **"Running"** → L'instance tourne, mais FastAPI est arrêté
   - **"Stopped"** → L'instance est arrêtée, il faut la redémarrer
   - **"Starting"** → L'instance redémarre

**Action selon le statut :**
- **Running** → Voir Solution 2 (relancer FastAPI)
- **Stopped** → Cliquer "Start" pour redémarrer l'instance
- **Starting** → Attendre que l'instance démarre

---

### Solution 2 : Relancer FastAPI (Si Instance Running)

**Si l'instance est "Running" mais FastAPI ne répond pas :**

1. **Ouvrir un nouveau terminal Jupyter** dans l'instance
2. **Vérifier si FastAPI tourne :**
   ```bash
   ps aux | grep app_runpod
   lsof -i :8000
   ```

3. **Si rien ne tourne, relancer :**
   ```bash
   cd /workspace/spinoza-secours/maiathon/Spinoza_Secours_HF/Backend
   
   # OU si le repo n'existe pas encore :
   cd /workspace
   git clone https://github.com/FJDaz/maiathon.git
   cd maiathon/Spinoza_Secours_HF/Backend
   
   # Installer dépendances (si pas déjà fait)
   pip install --no-cache-dir -r requirements.runpod.txt
   
   # Lancer en background
   nohup python app_runpod.py > /tmp/spinoza.log 2>&1 &
   ```

4. **Vérifier que ça tourne :**
   ```bash
   ps aux | grep app_runpod
   tail -f /tmp/spinoza.log
   ```

5. **Tester l'URL :**
   ```bash
   curl http://localhost:8000/health
   # OU
   curl http://195.139.22.91:8000/health
   ```

---

### Solution 3 : Vérifier les Logs de l'Instance

**Dans l'interface Vast.ai :**

1. **Instance → "Logs"**
2. **Chercher** les dernières lignes
3. **Vérifier** si FastAPI était en cours d'exécution
4. **Chercher** des erreurs ou crashs

---

### Solution 4 : Redémarrer l'Instance (Si Nécessaire)

**Si l'instance est "Stopped" :**

1. **Dans l'interface Vast.ai :**
   - Instance → Bouton **"Start"** ou **"Restart"**
2. **Attendre** que l'instance démarre (1-2 minutes)
3. **Relancer FastAPI** (voir Solution 2)

---

## 🔧 Script Complet de Relance

**Dans un nouveau terminal Jupyter, exécuter :**

```bash
#!/bin/bash
set -e

echo "🔍 Vérification état..."

# Vérifier si le processus tourne
if ps aux | grep -q "[p]ython app_runpod.py"; then
    echo "✅ FastAPI est déjà en cours d'exécution"
    ps aux | grep "[p]ython app_runpod.py"
else
    echo "⚠️ FastAPI n'est pas en cours d'exécution"
    echo "🚀 Relance de l'application..."
    
    # Aller dans workspace
    cd /workspace
    
    # Cloner repo si nécessaire
    if [ ! -d "maiathon" ]; then
        echo "📥 Clonage du repository..."
        git clone https://github.com/FJDaz/maiathon.git
    fi
    
    # Aller dans Backend
    cd maiathon/Spinoza_Secours_HF/Backend
    
    # Installer dépendances si nécessaire
    if [ ! -f ".deps_installed" ]; then
        echo "📦 Installation des dépendances..."
        pip install --no-cache-dir --upgrade pip
        pip install --no-cache-dir -r requirements.runpod.txt
        touch .deps_installed
    fi
    
    # Lancer FastAPI en background
    echo "🚀 Lancement de FastAPI..."
    nohup python app_runpod.py > /tmp/spinoza.log 2>&1 &
    
    # Attendre un peu
    sleep 3
    
    # Vérifier
    if ps aux | grep -q "[p]ython app_runpod.py"; then
        echo "✅ FastAPI lancé avec succès!"
        echo "📋 PID: $(ps aux | grep '[p]ython app_runpod.py' | awk '{print $2}')"
        echo "📋 Logs: tail -f /tmp/spinoza.log"
    else
        echo "❌ Échec du lancement. Voir logs:"
        tail -20 /tmp/spinoza.log
    fi
fi
```

---

## 📋 Checklist de Diagnostic

- [ ] Vérifier statut instance dans Vast.ai (Running/Stopped)
- [ ] Si Running : Vérifier si FastAPI tourne (`ps aux | grep app_runpod`)
- [ ] Si FastAPI ne tourne pas : Relancer (script ci-dessus)
- [ ] Vérifier les logs (`tail -f /tmp/spinoza.log`)
- [ ] Tester localement (`curl http://localhost:8000/health`)
- [ ] Tester depuis l'extérieur (`curl http://195.139.22.91:8000/health`)

---

## ⚠️ Points d'Attention

### 1. Processus en Background

**Si vous avez lancé FastAPI sans `nohup` :**
- Le processus s'arrête quand le terminal se ferme
- **Solution :** Toujours utiliser `nohup` ou `&`

### 2. Instance qui Redémarre

**Si l'instance redémarre :**
- Le script On-start devrait relancer FastAPI
- **Mais** le script On-start est incorrect actuellement
- **Solution :** Exécuter manuellement ou corriger le script On-start

### 3. Port Non Exposé

**Si le port 8000 n'est pas accessible :**
- Vérifier la configuration des ports dans Vast.ai
- Vérifier que le port 8000 est bien dans la liste des ports exposés

---

## 🎯 Action Immédiate

1. **Vérifier le statut de l'instance** dans Vast.ai
2. **Si Running :** Ouvrir un terminal et relancer FastAPI
3. **Si Stopped :** Redémarrer l'instance puis relancer FastAPI
4. **Vérifier les logs** pour voir ce qui s'est passé

---

**Dites-moi le statut de l'instance dans Vast.ai (Running/Stopped) et je vous guiderai pour la relancer !**

