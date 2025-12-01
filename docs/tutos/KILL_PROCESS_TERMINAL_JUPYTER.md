# 🔧 Comment Arrêter un Processus dans Terminal Jupyter Vast.ai

**Date :** 28 novembre 2025  
**Problème :** Ctrl+C ne fonctionne pas, affiche juste "^C"

---

## 🎯 Solutions

### Solution 1 : Ouvrir un Nouveau Terminal (RECOMMANDÉ) ⭐⭐⭐

**Dans Jupyter :**
1. **Fermer** le terminal actuel (bouton X ou fermer l'onglet)
2. **Ouvrir un nouveau terminal** :
   - Menu Jupyter → **"New"** → **"Terminal"**
   - OU cliquer sur l'icône **"+"** → **"Terminal"**

**Avantage :** Nouveau terminal propre, pas de processus bloqué

---

### Solution 2 : Tuer le Processus par PID

**Dans le terminal actuel (même si Ctrl+C ne marche pas) :**

1. **Trouver le PID du processus :**
   ```bash
   ps aux | grep python
   # OU
   ps aux | grep app_runpod
   ```

2. **Tuer le processus :**
   ```bash
   kill <PID>
   # OU si ça ne marche pas :
   kill -9 <PID>
   ```

**Exemple :**
```bash
# Voir les processus Python
ps aux | grep python

# Résultat :
# root 12345 ... python app_runpod.py

# Tuer le processus
kill 12345
# OU
kill -9 12345
```

---

### Solution 3 : Tuer Tous les Processus Python

**Si vous ne trouvez pas le PID exact :**

```bash
# Tuer tous les processus python
pkill python
# OU plus agressif :
pkill -9 python
```

**⚠️ Attention :** Cela tuera TOUS les processus Python, y compris Jupyter si nécessaire.

---

### Solution 4 : Utiliser `killall`

```bash
# Tuer tous les processus app_runpod
killall python app_runpod.py
# OU
killall -9 python
```

---

### Solution 5 : Redémarrer le Kernel Jupyter

**Si le terminal est complètement bloqué :**

1. **Dans Jupyter :** Menu → **"Kernel"** → **"Restart Kernel"**
2. **OU** Cliquer sur l'icône **"Restart"** (flèche circulaire)
3. **OU** Utiliser le raccourci : **"0, 0"** (zéro deux fois)

**Cela redémarrera le kernel et libérera le terminal.**

---

### Solution 6 : Fermer et Rouvrir Jupyter

**Si rien ne fonctionne :**

1. **Fermer** complètement l'onglet Jupyter
2. **Dans l'interface Vast.ai :** Cliquer sur **"Jupyter"** à nouveau
3. **Ouvrir un nouveau terminal**

---

## 🔍 Vérifier si le Processus est Arrêté

**Après avoir tué le processus :**

```bash
# Vérifier que FastAPI n'est plus en cours
ps aux | grep app_runpod

# Vérifier que le port 8000 est libre
netstat -tlnp | grep 8000
# OU
lsof -i :8000
```

**Si rien n'apparaît :** Le processus est arrêté ✅

---

## 🚀 Relancer FastAPI Correctement

**Une fois le processus arrêté, relancer en background :**

```bash
cd /workspace/spinoza-secours/maiathon/Spinoza_Secours_HF/Backend

# Lancer en background avec nohup
nohup python app_runpod.py > /tmp/spinoza.log 2>&1 &

# Vérifier que ça tourne
ps aux | grep app_runpod

# Voir les logs en temps réel
tail -f /tmp/spinoza.log
```

**Avantages :**
- ✅ Processus en background (ne bloque pas le terminal)
- ✅ Logs dans `/tmp/spinoza.log`
- ✅ Peut fermer le terminal sans arrêter FastAPI

---

## ⚠️ Si le Terminal est Complètement Bloqué

**Si le terminal ne répond plus du tout :**

1. **Fermer l'onglet** du terminal
2. **Ouvrir un nouveau terminal** dans Jupyter
3. **OU** Utiliser SSH directement (si configuré)

---

## 📋 Commandes Utiles

### Voir les Processus en Cours

```bash
# Tous les processus Python
ps aux | grep python

# Processus sur le port 8000
lsof -i :8000

# Tous les processus
ps aux
```

### Tuer un Processus

```bash
# Méthode douce
kill <PID>

# Méthode forcée
kill -9 <PID>

# Tuer par nom
pkill python
killall python
```

### Vérifier le Port

```bash
# Voir qui utilise le port 8000
netstat -tlnp | grep 8000
lsof -i :8000

# Tuer le processus sur le port 8000
fuser -k 8000/tcp
```

---

## 🎯 Solution Rapide (Recommandée)

**Si Ctrl+C ne fonctionne pas :**

1. **Ouvrir un nouveau terminal** dans Jupyter
2. **Dans le nouveau terminal :**
   ```bash
   # Trouver le PID
   ps aux | grep app_runpod
   
   # Tuer (remplacer 12345 par le vrai PID)
   kill -9 12345
   ```
3. **Relancer en background :**
   ```bash
   cd /workspace/spinoza-secours/maiathon/Spinoza_Secours_HF/Backend
   nohup python app_runpod.py > /tmp/spinoza.log 2>&1 &
   ```

---

## 🔗 Références

- **Script On-start :** `Backend/onstart_vast_ai.sh`
- **Application :** `Backend/app_runpod.py`

---

**Action immédiate :** Ouvrir un nouveau terminal Jupyter et utiliser `kill -9 <PID>` pour arrêter le processus bloqué.

