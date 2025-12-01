# 🔄 Redémarrer l'Instance Vast.ai - Guide Simple

**Date :** 28 novembre 2025  
**Situation :** Terminal inaccessible, FastAPI arrêté  
**Solution :** Redémarrer l'instance

---

## ✅ Solution : Redémarrer l'Instance

### Pourquoi Redémarrer ?

1. ✅ **Accès au terminal** : Un nouveau terminal sera accessible
2. ✅ **État propre** : Instance dans un état propre
3. ⚠️ **Mais** : Le script On-start incorrect sera toujours là

---

## 🎯 Étapes

### Étape 1 : Redémarrer l'Instance

**Dans l'interface Vast.ai :**

1. **Aller sur :** https://cloud.vast.ai/instances
2. **Trouver votre instance** (ID: 28314448)
3. **Cliquer sur le bouton "Restart"** ou **"Stop" puis "Start"**
4. **Attendre** 1-2 minutes que l'instance redémarre

### Étape 2 : Accéder au Nouveau Terminal

**Une fois l'instance redémarrée :**

1. **Cliquer sur "Jupyter"** ou **"Terminal"** ou **">_Connect"**
2. **Un nouveau terminal sera accessible** ✅

### Étape 3 : Exécuter le Script

**Dans le nouveau terminal, copier-coller :**

```bash
cd /workspace
git clone https://github.com/FJDaz/maiathon.git
cd maiathon/Spinoza_Secours_HF/Backend
pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.runpod.txt
nohup python app_runpod.py > /tmp/spinoza.log 2>&1 &
tail -f /tmp/spinoza.log
```

---

## ⚠️ Important : Le Problème Persistera

**Si vous redémarrez sans corriger le script On-start :**
- ✅ L'instance redémarrera
- ✅ Vous aurez accès au terminal
- ❌ Mais FastAPI ne se lancera pas automatiquement
- ⚠️ Il faudra relancer manuellement à chaque redémarrage

---

## 🎯 Solution Permanente (Recommandée)

### Option A : Corriger le Script On-start AVANT de Redémarrer

**Si vous pouvez accéder aux paramètres de l'instance :**

1. **Instance → "Edit"** ou **"Settings"**
2. **Onglet "Onstart"**
3. **Remplacer le script** par notre script complet
4. **Sauvegarder**
5. **Redémarrer** l'instance

**Résultat :** FastAPI se lancera automatiquement à chaque redémarrage ✅

### Option B : Redémarrer Maintenant, Corriger Plus Tard

**Si vous ne pouvez pas accéder aux paramètres maintenant :**

1. **Redémarrer** l'instance (pour avoir accès au terminal)
2. **Lancer FastAPI manuellement** (script ci-dessus)
3. **Plus tard** : Corriger le script On-start pour automatiser

---

## 📋 Checklist

- [ ] Redémarrer l'instance dans Vast.ai
- [ ] Attendre 1-2 minutes
- [ ] Accéder au nouveau terminal (Jupyter/Terminal)
- [ ] Exécuter le script de déploiement
- [ ] Vérifier les logs
- [ ] Tester l'URL `http://195.139.22.91:8000/health`
- [ ] (Optionnel) Corriger le script On-start pour automatiser

---

## 🚀 Action Immédiate

1. **Dans Vast.ai :** Instance → **"Restart"**
2. **Attendre** 1-2 minutes
3. **Ouvrir un nouveau terminal**
4. **Exécuter le script** ci-dessus

---

**✅ Redémarrer est effectivement la solution la plus simple pour récupérer l'accès au terminal !**

