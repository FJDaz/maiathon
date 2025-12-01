# 🚀 Quick Start - Déploiement Vast.ai

Guide rapide pour déployer Spinoza Secours sur Vast.ai en 5 minutes.

---

## ⚡ Déploiement Express

### 1. Prérequis (2 min)
- [ ] Compte Vast.ai créé : [vast.ai](https://vast.ai/)
- [ ] Token Hugging Face : [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

### 2. Créer l'Instance (2 min)

1. **Dashboard Vast.ai** → **Create**
2. **GPU** : Sélectionner **RTX 3090** (recommandé, $0.20-0.40/h)
3. **Docker** : 
   - Source : GitHub ou Dockerfile direct
   - Dockerfile : `Backend/Dockerfile.runpod`
4. **Variables d'environnement** :
   ```
   HF_TOKEN=votre_token_huggingface
   PORT=8000
   ```
5. **Container Disk** : 50GB minimum
6. **Port** : 8000

### 3. Déployer (10-15 min)

1. Cliquer **"Deploy"** ou **"Start"**
2. Attendre le build Docker (~5-10 min)
3. Attendre le chargement du modèle (~10-15 min)
4. Récupérer l'URL publique dans **"Connect"**

### 4. Tester (1 min)

```bash
# Test rapide
curl http://votre-instance.vast.ai:8000/health
```

**Réponse attendue :**
```json
{"status": "ok", "model": "Mistral 7B + LoRA", "gpu_available": true}
```

### 5. Mettre à Jour le Frontend (1 min)

1. Ouvrir `Frontend/index_spinoza.html`
2. Ligne 120 : Remplacer l'URL par votre URL Vast.ai
   ```javascript
   const API_BASE_URL = 'http://votre-instance.vast.ai:8000';
   ```
3. Tester dans le navigateur

---

## 📚 Documentation Complète

- **Guide détaillé** : `Backend/README_VAST_AI.md`
- **Guide frontend** : `Frontend/GUIDE_UPDATE_VAST_AI.md`
- **Tests** : `Backend/test_runpod_deployment.sh`

---

## 💰 Coûts

- **RTX 3090** : $0.20-0.40/h (~0.18-0.36€/h)
- **3h de démo** : ~$0.60-1.20 (0.54-1.08€)
- **Dépôt minimum** : Généralement $0 ✅

---

## ✅ Checklist

- [ ] Instance Vast.ai créée
- [ ] Variables d'environnement configurées
- [ ] Instance démarrée et modèle chargé
- [ ] URL publique récupérée
- [ ] Test `/health` réussi
- [ ] Frontend mis à jour
- [ ] Test complet réussi

---

**Temps total estimé :** ~20 minutes (dont 15 min d'attente pour le modèle)

**Dernière mise à jour :** Décembre 2024

