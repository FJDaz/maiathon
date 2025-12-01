# ✅ Todo List - Option B : Template Personnalisé Vast.ai

**Date :** Janvier 2025  
**Objectif :** Créer un template personnalisé sur Vast.ai pour Spinoza Secours

---

## 📋 Checklist Complète

### Phase 1 : Préparation GitHub ✅

- [x] **Vérifier fichiers locaux**
  - ✅ `Backend/Dockerfile.runpod` présent
  - ✅ `Backend/app_runpod.py` présent
  - ✅ `Backend/requirements.runpod.txt` présent
  - ✅ `Backend/Notebooks/Spinoza_Secours_DER` présent

- [ ] **Synchroniser vers GitHub** ⏳ EN COURS
  - [ ] Résoudre conflits Git (index.html)
  - [ ] Push vers https://github.com/FJDaz/Spinoza_secours
  - [ ] Vérifier fichiers accessibles sur GitHub

### Phase 2 : Configuration Vast.ai

- [ ] **Créer instance Vast.ai**
  - [ ] Aller sur : https://vast.ai/console/create
  - [ ] **Ne PAS sélectionner de template pré-configuré** (Option B)

- [ ] **Sélectionner GPU**
  - [ ] Option A : RTX 4090 à $0.29/h ⭐⭐ (recommandé)
  - [ ] Option B : RTX 3090 à $0.20-0.25/h ⭐ (budget)
  - [ ] Filtrer : VRAM 24GB minimum

- [ ] **Configurer Docker**
  - [ ] Source : GitHub
  - [ ] Repository : `FJDaz/Spinoza_secours`
  - [ ] Branch : `main`
  - [ ] Dockerfile Path : `Spinoza_Secours_HF/Backend/Dockerfile.runpod`
  - [ ] Dockerfile Context : `/` (racine)

- [ ] **Configurer Variables d'Environnement**
  - [ ] `HF_TOKEN` : [Votre token Hugging Face]
  - [ ] `PORT` : `8000`

- [ ] **Configurer Storage**
  - [ ] Container Disk : 50GB minimum
  - [ ] (Optionnel) Volume Disk : Si usage fréquent

- [ ] **Configurer Port**
  - [ ] Internal Port : `8000`
  - [ ] External Port : `8000` (ou auto-mappé)

### Phase 3 : Sauvegarde Template

- [ ] **Sauvegarder comme Template**
  - [ ] Chercher option "Save as Template" ou "Create Template"
  - [ ] Nom : `spinoza-secours-mistral7b`
  - [ ] Description : "Spinoza Secours API - Mistral 7B + LoRA"
  - [ ] Sauvegarder

### Phase 4 : Déploiement

- [ ] **Déployer l'instance**
  - [ ] Cliquer "Create" ou "Deploy"
  - [ ] Attendre build Docker (5-10 min)
  - [ ] Attendre chargement modèle (10-15 min Container Disk, 1-2 min Volume Disk)
  - [ ] Vérifier logs : Chercher "✅ Modèle Mistral 7B + LoRA chargé!"

- [ ] **Récupérer URL publique**
  - [ ] Dashboard → Instance → "Connect" ou "Public URL"
  - [ ] Noter l'URL : `http://votre-instance.vast.ai:8000`

### Phase 5 : Tests

- [ ] **Tester endpoints**
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

- [ ] **Mettre à jour frontend**
  - [ ] Ouvrir `Frontend/index_spinoza.html`
  - [ ] Ligne 127 : Modifier `API_BASE_URL` avec URL Vast.ai
  - [ ] Tester dans navigateur

---

## 📝 Notes

**Token HF :** ✅ Déjà obtenu  
**Compte Vast.ai :** ✅ Déjà créé  
**Repo GitHub :** https://github.com/FJDaz/Spinoza_secours

**Problème Git actuel :** Conflit sur `index.html` à résoudre avant push

**Temps estimé total :** ~30-45 minutes (dont 15-25 min d'attente pour build + modèle)

---

## 🔗 Références

- **Plan complet :** `docs/references/PLAN_MIGRATION_VAST_AI.md`
- **Guide sync GitHub :** `SYNC_GITHUB_VAST_AI.md`
- **Script push :** `push_to_github.sh`


