# 📊 État du Déploiement Spinoza Secours sur Vast.ai

**Date :** 28 novembre 2025  
**Statut :** ✅ **Fichiers de déploiement créés et poussés**

---

## ✅ Accompli

### 1. Fichiers de Déploiement Créés

- ✅ **`Backend/Dockerfile.runpod`** - Dockerfile pour Vast.ai/RunPod
- ✅ **`Backend/app_runpod.py`** - Application FastAPI complète (18KB)
- ✅ **`Backend/requirements.runpod.txt`** - Dépendances Python

### 2. Repository GitHub

- ✅ **Repository :** https://github.com/FJDaz/maiathon
- ✅ **Branche :** `main`
- ✅ **Fichiers poussés :** Tous les fichiers de déploiement sont sur GitHub

### 3. Documentation

- ✅ Plan de migration complet : `docs/references/PLAN_MIGRATION_VAST_AI.md`
- ✅ TODO list : `TODO_VAST_AI_OPTION_B.md`
- ✅ Scripts de test : `Backend/test_runpod_deployment.sh`

---

## ⏳ À Faire (Prochaines Étapes)

### Phase 1 : Configuration Vast.ai

1. **Créer instance Vast.ai**
   - Aller sur : https://vast.ai/console/create
   - **Ne PAS sélectionner de template pré-configuré** (Option B)

2. **Sélectionner GPU**
   - Option A : RTX 4090 à $0.29/h ⭐⭐ (recommandé)
   - Option B : RTX 3090 à $0.20-0.25/h ⭐ (budget)
   - Filtrer : VRAM 24GB minimum

3. **Configurer Docker**
   - Source : GitHub
   - Repository : `FJDaz/maiathon`
   - Branch : `main`
   - Dockerfile Path : `Spinoza_Secours_HF/Backend/Dockerfile.runpod`
   - Dockerfile Context : `/` (racine)

4. **Configurer Variables d'Environnement**
   - `HF_TOKEN` : [Votre token Hugging Face]
   - `PORT` : `8000`

5. **Configurer Storage**
   - Container Disk : 50GB minimum
   - (Optionnel) Volume Disk : Si usage fréquent

6. **Configurer Port**
   - Internal Port : `8000`
   - External Port : `8000` (ou auto-mappé)

### Phase 2 : Déploiement

7. **Déployer l'instance**
   - Cliquer "Create" ou "Deploy"
   - Attendre build Docker (5-10 min)
   - Attendre chargement modèle (10-15 min Container Disk, 1-2 min Volume Disk)
   - Vérifier logs : Chercher "✅ Modèle Mistral 7B + LoRA chargé!"

8. **Récupérer URL publique**
   - Dashboard → Instance → "Connect" ou "Public URL"
   - Noter l'URL : `http://votre-instance.vast.ai:8000`

### Phase 3 : Tests

9. **Tester endpoints**
   ```bash
   # Health check
   curl http://votre-instance.vast.ai:8000/health
   
   # Init
   curl http://votre-instance.vast.ai:8000/init
   
   # Chat (exemple)
   curl -X POST http://votre-instance.vast.ai:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Bonjour", "history": []}'
   ```

10. **Mettre à jour frontend**
    - Ouvrir `Frontend/index_spinoza.html`
    - Ligne 127 : Modifier `API_BASE_URL` avec URL Vast.ai
    - Tester dans navigateur

---

## 📋 Checklist Complète

### Préparation ✅
- [x] Fichiers de déploiement créés
- [x] Repository GitHub créé (maiathon)
- [x] Fichiers poussés vers GitHub
- [x] Token Hugging Face obtenu
- [x] Compte Vast.ai créé

### Configuration Instance ⏳
- [ ] Instance Vast.ai créée
- [ ] GPU sélectionné (RTX 4090 ou RTX 3090)
- [ ] Docker configuré (GitHub repo)
- [ ] Variables d'environnement configurées
- [ ] Storage configuré (50GB minimum)
- [ ] Port 8000 exposé

### Déploiement ⏳
- [ ] Instance lancée
- [ ] Build Docker réussi
- [ ] Modèle chargé
- [ ] Serveur FastAPI démarré
- [ ] URL publique récupérée

### Tests ⏳
- [ ] Test `/health` réussi
- [ ] Test `/init` réussi
- [ ] Test `/chat` réussi
- [ ] Test `/evaluate` réussi
- [ ] Frontend mis à jour
- [ ] Test complet frontend + backend réussi

---

## 🔗 Références

- **Plan complet :** `docs/references/PLAN_MIGRATION_VAST_AI.md`
- **TODO list :** `TODO_VAST_AI_OPTION_B.md`
- **Repository GitHub :** https://github.com/FJDaz/maiathon
- **Dashboard Vast.ai :** https://vast.ai/console/instances

---

## 💰 Coûts Estimés

- **RTX 4090 :** $0.29/h (~$60/mois si 24/7)
- **RTX 3090 :** $0.20-0.40/h (~$50/mois si 24/7)
- **Usage ponctuel :** ~$0.87 pour 3h de démo (RTX 4090)

---

**Prochaine étape :** Aller sur https://vast.ai/console/create et créer l'instance ! 🚀

