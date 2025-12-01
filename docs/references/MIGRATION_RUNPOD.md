# Migration Colab → RunPod/Vast.ai - Guide Complet

**Date :** Décembre 2024  
**Modèle :** Mistral 7B + LoRA (Spinoza Secours)  
**Budget :** 20€ maximum  
**Usage :** Ponctuel (démos/sessions)

---

## Table des Matières

1. [Vue d'Ensemble](#vue-densemble)
2. [Vérification des Dépôts](#vérification-des-dépôts)
3. [Préparation](#préparation)
4. [Déploiement RunPod](#déploiement-runpod)
5. [Déploiement Vast.ai](#déploiement-vastai)
6. [Mise à Jour Frontend](#mise-à-jour-frontend)
7. [Coûts et Optimisation](#coûts-et-optimisation)
8. [Troubleshooting](#troubleshooting)

---

## Vue d'Ensemble

### Architecture Actuelle (Colab)

```
Frontend (fjdaz.com)
    ↓
Colab + ngrok (URL temporaire)
    ↓
FastAPI + Mistral 7B + LoRA
```

**Problèmes :**
- URL ngrok change à chaque session
- Instabilité Colab (timeout, limitations)
- Nécessite redémarrage manuel

### Architecture Cible (RunPod/Vast.ai)

```
Frontend (fjdaz.com)
    ↓
RunPod/Vast.ai (URL fixe)
    ↓
Docker Container (FastAPI + Mistral 7B + LoRA)
```

**Avantages :**
- URL fixe et stable
- Contrôle total sur l'infrastructure
- Pay-per-use (économique pour usage ponctuel)

---

## Vérification des Dépôts

### RunPod

**Statut :** ⚠️ Dépôt minimum généralement $100 (~92€)

**Action requise :**
- Contacter support RunPod : support@runpod.io
- Vérifier si dépôt flexible disponible
- Si dépôt > 20€ → Utiliser Vast.ai à la place

**Documentation :** Voir `docs/references/VERIFICATION_DEPOTS.md`

### Vast.ai

**Statut :** ✅ Généralement pas de dépôt minimum

**Avantages :**
- Pas de dépôt requis
- Coûts similaires à RunPod
- Interface similaire

**Recommandation :** Commencer avec Vast.ai si budget limité

---

## Préparation

### Fichiers Créés

1. **`Backend/Dockerfile.runpod`**
   - Configuration Docker complète
   - Basé sur Python 3.10-slim
   - Installe toutes les dépendances

2. **`Backend/app_runpod.py`**
   - Application FastAPI complète
   - Tous les endpoints : `/health`, `/init`, `/chat`, `/evaluate`
   - Prompts intégrés directement

3. **`Backend/requirements.runpod.txt`**
   - Dépendances Python nécessaires
   - Versions compatibles avec le notebook Colab

4. **`Backend/test_runpod_deployment.sh`**
   - Script de test des endpoints
   - Usage : `./test_runpod_deployment.sh <URL_BACKEND>`

### Prérequis

1. **Token Hugging Face**
   - Créer sur https://huggingface.co/settings/tokens
   - Permissions : `read` (pour télécharger le modèle)

2. **Compte RunPod ou Vast.ai**
   - RunPod : https://www.runpod.io/
   - Vast.ai : https://vast.ai/

3. **Méthode de paiement**
   - Carte bancaire
   - Pour Vast.ai : Généralement pas de dépôt requis

---

## Déploiement RunPod

### Étape 1 : Créer un Template (15 min)

1. **Dashboard RunPod** → **Templates** → **Create Template**

2. **Configuration :**
   ```
   Name: spinoza-secours-mistral7b
   Container Image: python:3.10-slim
   ```

3. **Source :**
   - Option A : GitHub repo (recommandé)
     - Repository : `FJDaz/bergsonAndFriends`
     - Path : `Spinoza_Secours_HF/Backend/`
     - Dockerfile : `Dockerfile.runpod`
   
   - Option B : Dockerfile direct
     - Copier le contenu de `Dockerfile.runpod`

4. **Docker Command :**
   ```bash
   git clone https://github.com/FJDaz/bergsonAndFriends.git /app && \
   cd /app/Spinoza_Secours_HF/Backend && \
   docker build -f Dockerfile.runpod -t spinoza-secours . && \
   docker run -p 8000:8000 -e HF_TOKEN=$HF_TOKEN spinoza-secours
   ```

### Étape 2 : Créer un Pod (5 min)

1. **Dashboard** → **Pods** → **Create Pod**

2. **Configuration :**
   - **Template :** `spinoza-secours-mistral7b`
   - **GPU :** 
     - T4 (16GB VRAM) - ~$0.30/h ✅ Recommandé pour budget limité
     - RTX 3090 (24GB VRAM) - ~$0.50/h (si T4 indisponible)
   - **Container Disk :** 50GB (pour le modèle)
   - **Volume Disk :** 0GB (pas nécessaire pour débuter)

3. **Network :**
   - **Port Mapping :**
     - Container Port: `8000`
     - Public Port: `Auto` (RunPod génère une URL)

4. **Environment Variables :**
   ```
   HF_TOKEN=hf_votre_token_ici
   PORT=8000
   ```

5. **Cliquer "Create Pod"**

### Étape 3 : Attendre le Démarrage (15-20 min)

1. **Build** : 5-10 minutes
   - Installation dépendances
   - Build Docker image

2. **Chargement modèle** : 5-10 minutes
   - Téléchargement Mistral 7B (~14GB)
   - Téléchargement LoRA adapter
   - Chargement en mémoire GPU

3. **Vérifier les logs** :
   - Dashboard → Pods → Votre pod → Logs
   - Attendre : `✅ Modèle Mistral 7B + LoRA chargé!`
   - Attendre : `🚀 Démarrage du serveur FastAPI sur le port 8000...`

### Étape 4 : Récupérer l'URL Publique (1 min)

1. **Dashboard** → **Pods** → Votre pod → **Connect**
2. **URL générée** : `https://abc123xyz-8000.proxy.runpod.net`
3. **Copier cette URL** pour mettre à jour le frontend

### Étape 5 : Tester l'API (5 min)

```bash
# Utiliser le script de test
cd Spinoza_Secours_HF/Backend
./test_runpod_deployment.sh https://abc123xyz-8000.proxy.runpod.net
```

Ou tester manuellement :

```bash
# Health check
curl https://abc123xyz-8000.proxy.runpod.net/health

# Init
curl https://abc123xyz-8000.proxy.runpod.net/init

# Chat
curl -X POST https://abc123xyz-8000.proxy.runpod.net/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Bonjour Spinoza", "history": []}'
```

---

## Déploiement Vast.ai

### Étape 1 : Créer une Instance (10 min)

1. **Dashboard Vast.ai** → **Create**

2. **Configuration :**
   - **GPU :** RTX 3090 ou équivalent
   - **Image :** Docker custom
   - **Dockerfile :** Utiliser `Dockerfile.runpod`

3. **Environment Variables :**
   ```
   HF_TOKEN=votre_token
   PORT=8000
   ```

4. **Port :** 8000 (mappé automatiquement)

### Étape 2 : Attendre le Démarrage (15-20 min)

Même processus que RunPod

### Étape 3 : Récupérer l'URL

URL générée par Vast.ai (format variable)

---

## Mise à Jour Frontend

### Étape 1 : Modifier index_spinoza.html

1. Ouvrir `Frontend/index_spinoza.html`
2. Ligne 120, remplacer :
   ```javascript
   const API_BASE_URL = 'https://nonremunerative-rory-unbreakably.ngrok-free.dev';
   ```
   Par :
   ```javascript
   const API_BASE_URL = 'https://abc123xyz-8000.proxy.runpod.net';
   ```

### Étape 2 : Mettre à Jour sur fjdaz.com

Si le frontend est hébergé sur `fjdaz.com`, mettre à jour le fichier sur le serveur également.

### Étape 3 : Tester

1. Ouvrir `index_spinoza.html` dans un navigateur
2. Vérifier que la connexion fonctionne
3. Tester un échange complet
4. Vérifier que le Maïeuthon fonctionne

**Guide détaillé :** Voir `Frontend/GUIDE_UPDATE_BACKEND_URL.md`

---

## Coûts et Optimisation

### Coûts RunPod

| GPU | Coût/heure | 3h démo | Dépôt |
|-----|------------|---------|-------|
| T4 | $0.30 | $0.90 | $100 ? |
| RTX 3090 | $0.50 | $1.50 | $100 ? |
| A10G | $1.00 | $3.00 | $100 ? |

**Avec budget 20€ :**
- Si dépôt requis > 20€ → ❌ Non viable
- Si dépôt flexible < 20€ → ✅ Viable (20€ + 1-2€ usage)

### Coûts Vast.ai

| GPU | Coût/heure | 3h démo | Dépôt |
|-----|------------|---------|-------|
| RTX 3090 | $0.20-0.40 | $0.60-1.20 | $0 ✅ |

**Avec budget 20€ :**
- ✅ **Très viable** (0€ dépôt + 1-2€ usage)

### Optimisation

1. **Arrêter le pod après usage**
   - RunPod/Vast.ai : Arrêter immédiatement après démo
   - Économie : Pas de coût continu

2. **Volume Disk persistant** (optionnel)
   - Évite retéléchargement du modèle
   - Coût : ~$0.05/GB/mois
   - Pour usage ponctuel : Pas nécessaire

3. **GPU adapté**
   - T4 suffit pour Mistral 7B + LoRA (4-bit)
   - RTX 3090 pour plus de marge
   - A10G : Overkill pour ce modèle

---

## Troubleshooting

### Le modèle ne charge pas

**Symptômes :**
- Logs montrent erreur de mémoire
- Pod crash au démarrage

**Solutions :**
1. Vérifier que `HF_TOKEN` est bien configuré
2. Vérifier la VRAM disponible (logs)
3. Essayer un GPU avec plus de VRAM (RTX 3090 au lieu de T4)
4. Vérifier que le modèle peut être téléchargé depuis Hugging Face

### L'API ne répond pas

**Symptômes :**
- `curl` retourne timeout ou erreur
- Frontend ne peut pas se connecter

**Solutions :**
1. Vérifier que le port 8000 est bien mappé
2. Vérifier les logs du pod (erreurs FastAPI ?)
3. Tester directement l'URL dans un navigateur : `https://votre-url/health`
4. Vérifier les règles de firewall (RunPod/Vast.ai)

### Erreur de mémoire GPU

**Symptômes :**
- Erreur `CUDA out of memory`
- Modèle ne charge pas complètement

**Solutions :**
1. Utiliser un GPU avec plus de VRAM
2. Réduire `max_new_tokens` dans `app_runpod.py` (ligne ~200)
3. Vérifier que la quantification 4-bit est activée

### Le frontend ne se connecte pas

**Symptômes :**
- Erreur CORS dans la console
- Timeout sur les requêtes

**Solutions :**
1. Vérifier que l'URL backend est correcte
2. Vérifier que CORS est activé dans `app_runpod.py` (ligne ~350)
3. Vérifier que le pod est bien démarré et accessible

---

## Checklist de Migration

### Préparation
- [ ] Token Hugging Face créé et testé
- [ ] Compte RunPod ou Vast.ai créé
- [ ] Dépôt vérifié (si RunPod)
- [ ] Fichiers Docker créés et testés localement (optionnel)

### Déploiement
- [ ] Template créé (RunPod) ou instance configurée (Vast.ai)
- [ ] Pod/Instance démarré
- [ ] Modèle chargé (vérifier logs)
- [ ] URL publique récupérée
- [ ] Endpoints testés (script de test)

### Migration Frontend
- [ ] `API_BASE_URL` mis à jour dans `index_spinoza.html`
- [ ] Fichier mis à jour sur `fjdaz.com` (si hébergé)
- [ ] Connexion testée
- [ ] Échange complet testé
- [ ] Maïeuthon testé

### Validation
- [ ] Tous les endpoints fonctionnent
- [ ] Le dialogue fonctionne correctement
- [ ] L'évaluation Maïeuthon fonctionne
- [ ] Les coûts sont dans le budget

---

## Fichiers de Référence

- **Dockerfile :** `Backend/Dockerfile.runpod`
- **Application :** `Backend/app_runpod.py`
- **Requirements :** `Backend/requirements.runpod.txt`
- **Script de test :** `Backend/test_runpod_deployment.sh`
- **Guide RunPod :** `Backend/README_RUNPOD.md`
- **Guide Frontend :** `Frontend/GUIDE_UPDATE_BACKEND_URL.md`
- **Vérification dépôts :** `docs/references/VERIFICATION_DEPOTS.md`

---

## Prochaines Étapes

1. **Vérifier dépôt RunPod** (si souhaité)
2. **Choisir plateforme** (Vast.ai recommandé avec budget 20€)
3. **Déployer** selon guide ci-dessus
4. **Tester** avec script de test
5. **Mettre à jour frontend** avec nouvelle URL
6. **Valider** fonctionnement complet

---

## Support

- **RunPod :** support@runpod.io
- **Vast.ai :** Support via dashboard
- **Documentation :** Voir fichiers de référence ci-dessus

---

**Dernière mise à jour :** Décembre 2024


