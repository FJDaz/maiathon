# Plan de Migration Complet - Spinoza Secours vers Vast.ai

**Date :** Janvier 2025  
**Projet :** Spinoza Secours HF  
**Source :** Colab + ngrok  
**Destination :** Vast.ai (RTX 3090 ou RTX 4090)  
**Budget :** 
- RTX 3090 : ~$0.20-0.40/h (vérifier tarifs actuels)
- **RTX 4090 : $0.29/h** ✅ (tarif vérifié Janvier 2025)

---

## 📋 Table des Matières

1. [Vue d'Ensemble](#vue-densemble)
2. [Prérequis](#prérequis)
3. [Étape 1 : Préparation](#étape-1--préparation)
4. [Étape 2 : Création Compte Vast.ai](#étape-2--création-compte-vastai)
5. [Étape 3 : Configuration Instance](#étape-3--configuration-instance)
6. [Étape 4 : Déploiement](#étape-4--déploiement)
7. [Étape 5 : Tests](#étape-5--tests)
8. [Étape 6 : Mise à Jour Frontend](#étape-6--mise-à-jour-frontend)
9. [Étape 7 : Validation Complète](#étape-7--validation-complète)
10. [Sécurité et Bonnes Pratiques](#sécurité-et-bonnes-pratiques)
11. [Maintenance et Monitoring](#maintenance-et-monitoring)
12. [Troubleshooting](#troubleshooting)
13. [Procédures Post-Déploiement](#procédures-post-déploiement)
14. [Checklist Complète](#checklist-complète)

---

## 📍 Quick Reference - Lignes Critiques

| Fichier | Ligne | Contenu | Action |
|---------|-------|---------|--------|
| `Backend/app_runpod.py` | 543 | CORS `allow_origins=["*"]` | ⚠️ **RESTREINDRE** en production |
| `Backend/app_runpod.py` | 619-624 | `uvicorn.run()` avec `log_level="info"` | ✅ OK |
| `Frontend/index_spinoza.html` | 127 | `API_BASE_URL` | ⚠️ **METTRE À JOUR** avec URL Vast.ai |
| `Backend/app_runpod.py` | 401, 449, 489 | `max_new_tokens` (optimisation latence) | ⚠️ Peut être réduit si besoin |
| `Backend/requirements.runpod.txt` | 7 | `pydantic>=2.5.0` | ✅ V2 (utiliser `field_validator`) |

---

## 🎯 Vue d'Ensemble

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
- Pas de contrôle sur l'infrastructure

### Architecture Cible (Vast.ai)

```
Frontend (fjdaz.com)
    ↓
Vast.ai (URL fixe)
    ↓
Docker Container (FastAPI + Mistral 7B + LoRA)
```

**Avantages :**
- URL fixe et stable
- Contrôle total sur l'infrastructure
- Pay-per-use (économique pour usage ponctuel)
- Performance supérieure (RTX 3090 vs T4)

### Coûts Comparés

| Plateforme | GPU | Coût/heure | Coût 3h démo | Dépôt |
|------------|-----|------------|--------------|-------|
| **Colab** | T4 | Gratuit* | $0 | $0 |
| **Vast.ai** | RTX 3090 | $0.20-0.40 | $0.60-1.20 | $0 ✅ |
| **Vast.ai** | **RTX 4090** | **$0.29** ✅ | **$0.87** | **$0** ✅ |

*Colab : Gratuit mais instable, limitations, timeout

---

## 📋 Prérequis

### 1. Compte Vast.ai

**Lien :** https://vast.ai/

**Étapes :**
1. Aller sur https://vast.ai/
2. Cliquer sur **"Sign Up"** ou **"Create Account"**
3. Remplir le formulaire (email, mot de passe)
4. Vérifier l'email
5. Se connecter

**Note :** Généralement pas de dépôt minimum requis ✅

### 2. Token Hugging Face

**Lien :** https://huggingface.co/settings/tokens

**Étapes :**
1. Aller sur https://huggingface.co/
2. Se connecter ou créer un compte
3. Aller dans **Settings** → **Access Tokens** : https://huggingface.co/settings/tokens
4. Cliquer sur **"New token"**
5. Nom : `spinoza-secours-vast-ai`
6. Type : **Read** (suffisant pour télécharger les modèles)
7. Cliquer sur **"Generate token"**
8. **Copier le token** (il ne sera plus visible après)

**Modèles nécessaires :**
- Base : `mistralai/Mistral-7B-Instruct-v0.2` (public)
- LoRA : `FJDaz/mistral-7b-philosophes-lora` (peut nécessiter le token)

### 3. GitHub (Optionnel mais Recommandé)

**Lien :** https://github.com/

**Si déploiement depuis GitHub :**
1. Créer un dépôt GitHub (ou utiliser existant)
2. Pousser les fichiers suivants :
   - `Backend/Dockerfile.runpod`
   - `Backend/app_runpod.py`
   - `Backend/requirements.runpod.txt`

**Lien dépôt actuel :** https://github.com/FJDaz/Spinoza_secours (à vérifier)

### 4. Fichiers Locaux

Vérifier que vous avez accès aux fichiers suivants :
- `Backend/Dockerfile.runpod`
- `Backend/app_runpod.py`
- `Backend/requirements.runpod.txt`
- `Frontend/index_spinoza.html`

---

## 🚀 Étape 1 : Préparation

### 1.1 Vérifier les Fichiers

**Localisation :** `/Users/francois-jeandazin/bergsonAndFriends/Spinoza_Secours_HF/Backend/`

**Fichiers requis :**
- ✅ `Dockerfile.runpod` - Dockerfile pour Vast.ai
- ✅ `app_runpod.py` - Application FastAPI complète
- ✅ `requirements.runpod.txt` - Dépendances Python

**Vérification :**
```bash
cd /Users/francois-jeandazin/bergsonAndFriends/Spinoza_Secours_HF/Backend/
ls -la Dockerfile.runpod app_runpod.py requirements.runpod.txt
```

### 1.2 Préparer le Token Hugging Face

**Action :** Copier le token Hugging Face obtenu à l'étape Prérequis #2

**Format :** `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Stockage temporaire :** Noter dans un endroit sûr (vous en aurez besoin pour la configuration)

### 1.3 (Optionnel) Préparer GitHub

Si vous déployez depuis GitHub :

1. **Créer un dépôt** (ou utiliser existant) : https://github.com/new
2. **Cloner localement** (si pas déjà fait)
3. **Copier les fichiers** :
   ```bash
   cp Backend/Dockerfile.runpod /chemin/vers/repo/
   cp Backend/app_runpod.py /chemin/vers/repo/
   cp Backend/requirements.runpod.txt /chemin/vers/repo/
   ```
4. **Commit et push** :
   ```bash
   git add Dockerfile.runpod app_runpod.py requirements.runpod.txt
   git commit -m "Add Vast.ai deployment files"
   git push origin main
   ```

---

## 🔐 Étape 2 : Création Compte Vast.ai

### 2.1 Créer le Compte

**Lien :** https://vast.ai/

**Étapes :**
1. Aller sur https://vast.ai/
2. Cliquer sur **"Sign Up"** (en haut à droite)
3. Remplir :
   - **Email** : votre email
   - **Password** : mot de passe sécurisé
   - **Confirm Password** : confirmation
4. Accepter les conditions
5. Cliquer sur **"Sign Up"**
6. Vérifier l'email (lien de confirmation)
7. Se connecter : https://vast.ai/ (cliquer sur **"Sign In"**)

### 2.2 Vérifier le Compte

**Dashboard :** https://vast.ai/console/instances

**Vérifications :**
- ✅ Compte créé et vérifié
- ✅ Email confirmé
- ✅ Peut accéder au dashboard

**Note :** Pas de dépôt minimum généralement requis ✅

---

## ⚙️ Étape 3 : Configuration Instance

### 3.1 Accéder à la Création d'Instance

**Lien direct :** https://vast.ai/console/create

**Ou depuis le dashboard :**
1. Aller sur https://vast.ai/console/instances
2. Cliquer sur **"Create"** (bouton vert en haut)

### 3.2 Choisir le Type d'Instance

**⚠️ Important :** Vast.ai propose plusieurs types d'instances. Pour Spinoza Secours, nous avons besoin d'une **instance Docker**, pas d'une VM.

**Options que vous pouvez voir :**

| Option | Type | Pour Spinoza Secours |
|--------|------|----------------------|
| **Ubuntu 22.04 VM** | Machine virtuelle complète | ❌ **NE PAS CHOISIR** |
| **Ubuntu Desktop (VM)** | VM avec interface graphique | ❌ **NE PAS CHOISIR** |
| **SSH** | Accès SSH direct | ❌ **NE PAS CHOISIR** |
| **Docker** / **Container** | Container Docker | ✅ **À CHOISIR** |
| **Custom Dockerfile** | Dockerfile personnalisé | ✅ **À CHOISIR** |

**⚠️ Si vous voyez "Ubuntu 22.04 VM" ou "Ubuntu Desktop (VM)" :**
- Ces options sont des **machines virtuelles complètes**
- Elles ne sont **pas adaptées** pour notre cas (FastAPI avec Dockerfile)
- **Ne pas les sélectionner**

**✅ Ce qu'il faut chercher :**
1. **Option "Docker"** ou **"Container"**
2. **Option "Custom Dockerfile"** ou **"Dockerfile"**
3. **Option "From GitHub"** (qui permet de spécifier un Dockerfile)

**Si vous ne trouvez pas ces options :**
- Regarder dans les **onglets** ou **options avancées**
- Chercher un champ **"Source"** ou **"Repository"** où vous pouvez entrer un Dockerfile
- Vérifier s'il y a un onglet **"Docker"** ou **"Container"**
- Consulter la documentation Vast.ai : https://docs.vast.ai/

**Note :** L'interface Vast.ai peut varier selon les versions. L'important est de trouver une option qui permet d'utiliser un **Dockerfile** (comme `Backend/Dockerfile.runpod`), pas une VM complète.

### 3.3 Sélectionner le GPU

**Section :** "Choose GPU"

**Recommandation :** **RTX 4090** ⭐⭐ (ou **RTX 3090** ⭐ si indisponible ou budget serré)

**Pourquoi RTX 4090 (RECOMMANDÉ) :**
- **Coût : $0.29/h** ✅ (tarif vérifié Janvier 2025)
- Performance : 3-4x plus rapide que T4
- VRAM : 24GB (suffisant pour Mistral 7B en 4-bit)
- **Meilleur rapport performance/prix** : Plus rapide que RTX 3090 pour prix similaire

**Pourquoi RTX 3090 (EXCELLENTE ALTERNATIVE) :**
- **Coût : $0.20-0.40/h** (peut être moins cher que RTX 4090 selon offre)
- **Performance : 2-3x plus rapide que T4** (largement suffisant)
- **VRAM : 24GB** (identique à RTX 4090, suffisant pour Mistral 7B)
- **Disponibilité :** Généralement disponible
- **Rapport qualité/prix :** Excellent si trouvé à $0.20-0.25/h
- **Économie :** Jusqu'à 31% moins cher que RTX 4090 si à $0.20/h

**Sélection :**
1. **Option A (Performance) :** Chercher **"RTX 4090"** à **$0.29/h** ⭐⭐
2. **Option B (Budget) :** Chercher **"RTX 3090"** à **$0.20-0.25/h** ⭐ (excellent rapport qualité/prix)
3. Filtrer par :
   - **VRAM** : 24GB (minimum)
   - **Prix** : 
     - RTX 4090 : $0.29/h (optimal)
     - RTX 3090 : $0.20-0.25/h (recommandé) ou $0.26-0.40/h (acceptable)
4. **Recommandation :** Si RTX 3090 < $0.25/h → choisir RTX 3090 (économies 14-31%)
5. Sélectionner une offre disponible

**Autres options :**
- **RTX 3060 12GB** : $0.15-0.25/h (moins cher mais moins performant, VRAM limite)

### 3.4 Configurer l'Instance

**Interface Vast.ai :** Lors de la création d'instance, vous verrez plusieurs sections :

#### Template (Sélection ou Création)

**Qu'est-ce qu'un Template ?**
- Configuration réutilisable pour créer plusieurs instances identiques
- Vast.ai propose 38+ templates pré-configurés
- Vous pouvez aussi créer votre propre template personnalisé

**⚠️ Important :** Aucun template pré-configuré ne correspond exactement à Spinoza Secours. Il faut utiliser un **Dockerfile personnalisé**.

**Options disponibles :**

**Option A : Utiliser un Template de Base (Recommandé pour débuter)**

Parmi les templates disponibles, les plus proches sont :
- **"NVIDIA CUDA"** : Base image avec CUDA (peut servir de point de départ)
- **"PyTorch (Vast)"** : PyTorch pré-installé (peut servir de point de départ)

**⚠️ Mais attention :** Ces templates ne contiennent pas notre application. Il faut quand même configurer un **Dockerfile personnalisé** pour utiliser `Backend/Dockerfile.runpod`.

**Option B : Créer un Template Personnalisé (Recommandé pour réutilisation)**

1. Lors de la création d'instance, **ne pas sélectionner de template pré-configuré**
2. Configurer manuellement :
   - Dockerfile : Utiliser `Backend/Dockerfile.runpod` (voir section Configuration Docker)
   - Variables d'environnement : `HF_TOKEN`, `PORT`
   - Storage : 50GB minimum
   - Port : 8000
3. Après configuration, chercher **"Save as Template"** ou **"Create Template"**
4. **Nom** : `spinoza-secours-mistral7b`
5. **Description** : "Spinoza Secours API - Mistral 7B + LoRA"
6. Sauvegarder

**Utiliser un Template Personnalisé :**
1. Lors de la création d'instance, sélectionner **"From Template"** ou chercher dans vos templates
2. Choisir le template `spinoza-secours-mistral7b`
3. Les configurations sont pré-remplies ✅
4. Ajuster si nécessaire (GPU, variables d'environnement)

**Option C : Pas de Template (Configuration Manuelle à Chaque Fois)**

1. **Ne pas sélectionner de template** dans la liste
2. Configurer manuellement toutes les options (voir sections suivantes)
3. Plus long mais plus flexible

---

#### Configuration Docker

**⚠️ Important :** Il n'y a **pas de section "Docker Image"** dédiée sur l'interface Vast.ai. La configuration Docker se fait dans les sections **Template**, **Instances** ou dans les paramètres de configuration.

**Où configurer Docker :**

1. **Si vous avez sélectionné un template** : Chercher une option **"Custom Dockerfile"**, **"Dockerfile"** ou **"Override Image"** dans les paramètres du template
2. **Si vous créez une instance manuelle** : Chercher un champ **"Dockerfile"**, **"Custom Dockerfile"** ou **"Source"** dans les paramètres d'instance
3. **Dans les options avancées** : Regarder dans les onglets ou paramètres avancés

**Où trouver la configuration Docker :**

1. **Dans la section Template** (si vous créez/sélectionnez un template)
2. **Dans les paramètres d'instance** (champs de configuration)
3. **Dans les options avancées** (selon la version de l'interface)

**Option A : Depuis GitHub (Recommandé)**

1. Chercher un champ **"Source"**, **"Repository"**, **"GitHub"** ou **"From GitHub"** dans les sections Template/Instances
2. Entrer le repository : `FJDaz/Spinoza_secours` (ou votre repo)
3. **Branch** : `main` (ou la branche appropriée)
4. **Dockerfile Path** : `Backend/Dockerfile.runpod`
5. **Dockerfile Context** : `/` (racine du repo) - si champ disponible

**Option B : Dockerfile Direct**

1. Chercher un champ **"Dockerfile"**, **"Custom Dockerfile"** ou zone de texte pour Dockerfile
2. Copier le contenu de `Backend/Dockerfile.runpod`
3. Coller dans le champ

**Option C : Image Docker Hub (Si publiée)**

1. Chercher un champ **"Image"** ou **"Docker Hub"**
2. Entrer : `votre-username/spinoza-secours:latest`

**Si vous ne trouvez pas ces champs :**
- Regarder dans les **options avancées** ou **paramètres avancés**
- Vérifier s'il y a un onglet **"Docker"** ou **"Container"**
- Consulter la documentation Vast.ai : https://docs.vast.ai/
- Les champs peuvent être dans la section **Template** ou **Instances**

---

#### Instances (Configuration Instance)

**Section :** "Instance Settings" ou "Configuration"

**Paramètres à vérifier :**
- **Instance Name** : `spinoza-secours-001` (optionnel, pour identification)
- **Auto-start** : Désactivé par défaut (démarrage manuel recommandé)
- **Auto-stop** : Optionnel (voir section Auto-Sleep)
- **Restart Policy** : `on-failure` (redémarrage si crash)

**Recommandations :**
- **Instance Name** : Utiliser un nom descriptif pour faciliter l'identification
- **Auto-start** : Laisser désactivé pour contrôler les coûts
- **Restart Policy** : `on-failure` pour éviter les redémarrages inutiles

---

#### Storage (Stockage)

**Section :** "Storage" ou "Disk" (déjà détaillée en section 3.5, rappel ici)

**Container Disk (Gratuit) :**
- **Taille** : **50GB minimum**
- **Type** : Stockage éphémère (effacé à l'arrêt)
- **Coût** : Inclus dans le prix GPU
- **Avantage** : Gratuit
- **Inconvénient** : Modèle retéléchargé à chaque démarrage (10-15 min)

**Volume Disk (Persistant) :**
- **Taille** : 50GB minimum (recommandé : 100GB pour marge)
- **Type** : Stockage persistant (conservé entre redémarrages)
- **Coût** : +$0.10-0.20/h supplémentaire
- **Avantage** : Modèle conservé, démarrage rapide (6-12 min vs 16-27 min)
- **Rentabilité** : Si usage > 4h/jour avec redémarrages fréquents

**Configuration Storage :**
1. **Container Disk** : Sélectionner **50GB** (ou plus)
2. **Volume Disk** (optionnel) : Cocher si besoin de persistance
   - Sélectionner taille : 50-100GB
   - Vérifier le coût supplémentaire affiché
3. **Mount Point** : `/workspace` ou `/data` (par défaut)

**⚠️ Important :**
- **Container Disk** : Suffisant pour usage ponctuel
- **Volume Disk** : Recommandé pour usage fréquent (voir section Cold Start)

### 3.5 Configurer les Variables d'Environnement

**Section :** "Environment Variables" ou "Env"

**Ajouter :**

| Variable | Valeur | Description |
|----------|--------|-------------|
| `HF_TOKEN` | `votre_token_hf` | Token Hugging Face (obtenu à l'étape Prérequis #2) |
| `PORT` | `8000` | Port FastAPI |

**Format :**
```
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PORT=8000
```

**⚠️ Important :** Remplacer `votre_token_hf` par le vrai token Hugging Face

### 3.6 Configurer le Stockage

**Section :** "Storage" ou "Disk"

**Container Disk :** **50GB minimum**

**Pourquoi :**
- Modèle Mistral 7B : ~14GB
- LoRA adapter : ~100MB
- Système + dépendances : ~5GB
- Marge : ~30GB

**Configuration :**
- **Container Disk** : 50GB (ou plus si disponible)
  - **Type :** Stockage éphémère (perdu à l'arrêt de l'instance)
  - **Coût :** Inclus dans le prix de l'instance
  - **Inconvénient :** Modèle retéléchargé à chaque démarrage (~10-15 min)

**Option : Volume Disk Persistant**
- **Type :** Stockage persistant (conservé entre redémarrages)
- **Coût :** +$0.10-0.20/h supplémentaire
- **Avantage :** Modèle conservé, démarrage rapide (~2-3 min)
- **Rentabilité :** Voir calcul ci-dessous

**Calcul Rentabilité Volume Disk :**
- **Seuil :** Si instance utilisée > 4h/jour avec redémarrages fréquents
- **Gain temps :** 10-15 min économisées par redémarrage
- **Exemple :** Usage 8h/jour avec 2 redémarrages = 20-30 min économisées
  - Volume Disk : $0.80-1.60/jour
  - Si valeur temps > coût → Volume Disk rentable

### 3.7 Configurer le Port

**Section :** "Ports" ou "Network"

**Port :** **8000**

**Configuration :**
- **Internal Port** : 8000
- **External Port** : Vast.ai mappe automatiquement (généralement même port 8000)
- **Protocol** : HTTP (ou TCP)

**⚠️ Important :** 
- Vast.ai mappe automatiquement les ports
- L'URL publique sera de type `http://votre-instance.vast.ai:8000`
- **Vérification :** Après création de l'instance, aller dans Dashboard → Instance → Connect/Public URL pour récupérer l'URL exacte
- Le port externe est généralement le même que le port interne (8000), mais peut varier selon la configuration Vast.ai


### 3.8 Réviser la Configuration

**Vérifications avant création :**

- [ ] GPU : RTX 3090 sélectionné
- [ ] Docker : Dockerfile configuré (GitHub ou direct)
- [ ] Variables d'environnement : `HF_TOKEN` et `PORT` définis
- [ ] Container Disk : 50GB minimum
- [ ] Port : 8000 exposé

**Coût estimé :** 
- **RTX 4090 : $0.29/h** ✅ (recommandé)
- RTX 3090 : $0.20-0.40/h (alternative)

---

## 🚀 Étape 4 : Déploiement

### 4.1 Lancer l'Instance

**Action :** Cliquer sur **"Create"** ou **"Deploy"**

**Lien dashboard :** https://vast.ai/console/instances

**Étapes :**
1. Vérifier toutes les configurations (étape 3)
2. Cliquer sur **"Create Instance"** ou **"Deploy"**
3. Attendre la confirmation

### 4.2 Suivre le Build Docker

**Temps estimé :** 5-10 minutes

**Où voir les logs :**
- Dashboard → Votre instance → **"Logs"** ou **"Console"**

**Ce qui se passe :**
1. Build de l'image Docker
2. Installation des dépendances Python
3. Téléchargement des packages (torch, transformers, etc.)

**Logs attendus :**
```
Building Docker image...
Installing dependencies...
Collecting torch>=2.0.0
Collecting transformers>=4.35.0
...
Successfully built image
```

### 4.3 Attendre le Chargement du Modèle (Cold Start)

**Temps estimé :** 
- **Container Disk** : 10-15 minutes (téléchargement modèle)
- **Volume Disk** : 1-2 minutes (modèle déjà présent)

**Voir section détaillée :** [Cold Start](#-cold-start-démarrage-à-froid)

**Où voir les logs :**
- Dashboard → Votre instance → **"Logs"**

**Ce qui se passe :**
1. Téléchargement Mistral 7B depuis Hugging Face (~14GB)
2. Téléchargement LoRA adapter (~100MB)
3. Chargement du modèle en mémoire GPU
4. Application de la quantization 4-bit

**Logs attendus :**
```
🖥️ GPU disponible: True
🔄 Chargement Mistral 7B (4-bit GPU)...
Downloading model.safetensors: 100%|████████| 14.2G/14.2G
🔄 Application LoRA Spinoza_Secours...
✅ Modèle Mistral 7B + LoRA chargé!
🚀 Démarrage du serveur FastAPI sur le port 8000...
```

**⚠️ Important :** Ne pas arrêter l'instance pendant le téléchargement

### 4.4 Vérifier le Démarrage du Serveur

**Logs attendus :**
```
🚀 Démarrage du serveur FastAPI sur le port 8000...
📡 Endpoints disponibles:
   - GET  /health
   - GET  /init
   - POST /chat
   - POST /evaluate
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Si vous voyez ces logs :** ✅ Le serveur est démarré et prêt

### 4.5 Récupérer l'URL Publique

**Où trouver :**
- Dashboard → Votre instance → **"Connect"** ou **"Public URL"**

**Format d'URL :**
- `http://votre-instance.vast.ai:8000`
- ou `https://votre-instance.vast.ai:8000` (si HTTPS activé)

**Exemple :**
```
http://abc123def456.vast.ai:8000
```

**⚠️ Important :** Noter cette URL, vous en aurez besoin pour le frontend

---

## 🧪 Étape 5 : Tests

### 5.1 Test Health Check

**Commande :**
```bash
curl http://votre-instance.vast.ai:8000/health
```

**Réponse attendue :**
```json
{
  "status": "ok",
  "model": "Mistral 7B + LoRA",
  "gpu_available": true
}
```

**Si `gpu_available: false` :** ⚠️ Problème de configuration GPU

### 5.2 Test Initialisation

**Commande :**
```bash
curl http://votre-instance.vast.ai:8000/init
```

**Réponse attendue :**
```json
{
  "greeting": "Bonjour ! Je suis Spinoza. Discutons :\n\n**La liberté est-elle une illusion ?**\n\nQu'en penses-tu ?",
  "history": [[null, "Bonjour ! Je suis Spinoza..."]]
}
```

### 5.3 Test Chat

**Commande :**
```bash
curl -X POST http://votre-instance.vast.ai:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Bonjour Spinoza, qu'\''est-ce que le conatus ?",
    "history": []
  }'
```

**Réponse attendue :**
```json
{
  "reply": "Le conatus est l'\''effort que chaque chose fait pour persévérer dans son être...",
  "history": [["Bonjour Spinoza...", "Le conatus est..."]]
}
```

**Temps de réponse :** 2-5 secondes (RTX 3090)

### 5.4 Test Évaluation (Maïathon)

**Commande :**
```bash
curl -X POST http://votre-instance.vast.ai:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "dialogue": "Spinoza: Bonjour ! Je suis Spinoza. Discutons : La liberté est-elle une illusion ?\nÉlève: Je pense que oui, tout est déterminé.\nSpinoza: Tu dis que tout est déterminé... qu'\''est-ce que ça veut dire pour toi ?",
    "score_front": 55
  }'
```

**Réponse attendue :**
```json
{
  "score_final": 85,
  "message_final": "Ton effort pour comprendre tes propres affects est impressionnant...",
  "details_model": {
    "comprehension": 8,
    "cooperation": 9,
    "progression": 8,
    "total": 25
  }
}
```

**Temps de réponse :** 5-10 secondes (RTX 3090)

### 5.5 Test Automatique (Script)

**Script :** `Backend/test_runpod_deployment.sh`

**Commande :**
```bash
cd /Users/francois-jeandazin/bergsonAndFriends/Spinoza_Secours_HF/Backend/
chmod +x test_runpod_deployment.sh
./test_runpod_deployment.sh http://votre-instance.vast.ai:8000
```

**Résultat attendu :** Tous les tests passent ✅

---

## 🎨 Étape 6 : Mise à Jour Frontend

### 6.1 Localiser le Fichier

**Fichier :** `Frontend/index_spinoza.html`

**Chemin complet :** `/Users/francois-jeandazin/bergsonAndFriends/Spinoza_Secours_HF/Frontend/index_spinoza.html`

### 6.2 Modifier l'URL Backend

**Ligne à modifier :** Ligne 127 (vérifiée)

**Ancien code :**
```javascript
const API_BASE_URL = 'https://nonremunerative-rory-unbreakably.ngrok-free.dev';
```

**Nouveau code :**
```javascript
const API_BASE_URL = 'http://votre-instance.vast.ai:8000';
```

**⚠️ Important :** Remplacer `votre-instance.vast.ai:8000` par votre vraie URL Vast.ai

### 6.3 Vérifier la Modification

**Vérification :**
1. Ouvrir `Frontend/index_spinoza.html`
2. Chercher `API_BASE_URL` (ligne ~120)
3. Vérifier que l'URL correspond à votre instance Vast.ai

### 6.4 Tester Localement

**Étapes :**
1. Ouvrir `Frontend/index_spinoza.html` dans un navigateur
2. Ouvrir la console développeur (F12)
3. Vérifier qu'il n'y a pas d'erreurs CORS
4. Cliquer sur "Commencer"
5. Vérifier que la question initiale de Spinoza s'affiche
6. Envoyer une réponse
7. Vérifier que Spinoza répond

**Si erreur CORS :** Vérifier que le backend autorise votre origine (voir Troubleshooting)

### 6.5 Mettre à Jour sur le Serveur

**Si le frontend est hébergé sur fjdaz.com :**

**Méthode 1 : FTP/SFTP**
1. Se connecter au serveur
2. Uploader `index_spinoza.html` mis à jour
3. Remplacer l'ancien fichier

**Méthode 2 : Git**
1. Committer les changements :
   ```bash
   git add Frontend/index_spinoza.html
   git commit -m "Update backend URL to Vast.ai"
   git push origin main
   ```
2. Si déploiement automatique, attendre le déploiement

**Méthode 3 : Interface d'hébergement**
1. Utiliser l'interface de votre hébergeur
2. Uploader le fichier mis à jour

---

## ✅ Étape 7 : Validation Complète

### 7.1 Test Complet Frontend + Backend

**Étapes :**
1. Ouvrir `Frontend/index_spinoza.html` (local ou sur serveur)
2. Cliquer sur "Commencer"
3. Vérifier que la question initiale s'affiche
4. Compléter les 5 échanges avec Spinoza
5. Vérifier que le score s'affiche en temps réel
6. Vérifier que l'évaluation finale fonctionne
7. Vérifier que le message final de Spinoza s'affiche
8. Vérifier que le titre "Maïathon" et "Réfléchis. Reformule. Questionne." s'affichent

### 7.2 Vérifier les Performances

**Latences attendues :**

| GPU | Inférence dialogue | Évaluation finale | Latence totale |
|-----|-------------------|-------------------|----------------|
| **T4 (Colab)** | 2-5s | 5-10s | 8-16s |
| **RTX 3090** | 1-3s | 3-6s | 4-9s |
| **RTX 4090** | **0.7-1.5s** | **2-4s** | **2.7-5.5s** |

**Gain RTX 4090 vs RTX 3090 :** ~1.3-3.5 secondes par requête complète

**Si latence trop élevée :** Vérifier que le GPU est bien utilisé (`gpu_available: true`)

### 7.3 Vérifier la Stabilité

**Tests de stabilité :**
1. Faire plusieurs dialogues complets
2. Vérifier que l'instance ne crash pas
3. Vérifier que les réponses sont cohérentes
4. Vérifier que le score fonctionne correctement

### 7.4 Documenter l'URL

**Action :** Noter l'URL Vast.ai dans un endroit sûr

**Format :**
```
URL Backend Vast.ai : http://votre-instance.vast.ai:8000
Date de déploiement : [date]
GPU : RTX 3090
Coût : $0.20-0.40/h
```

---

## 🔒 Sécurité et Bonnes Pratiques

### ⚠️ Points Critiques de Sécurité

#### 1. Configuration CORS (CRITIQUE)

**Problème actuel :** Le code autorise toutes les origines (`allow_origins=["*"]`)

**Fichier :** `Backend/app_runpod.py` ligne 543

**Action REQUISE avant production :**

```python
# ❌ ACTUEL (INSÉCURISÉ)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ DANGEREUX
    ...
)

# ✅ CORRIGER EN (PRODUCTION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://fjdaz.com",
        "https://www.fjdaz.com",
        # "http://localhost:8000",  # ⚠️ RETIRER en production, garder seulement pour dev local
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# Pour développement local, utiliser une configuration séparée :
# allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"]  # Dev uniquement
```

**Étapes :**
1. Modifier `Backend/app_runpod.py` ligne 543
2. Remplacer `allow_origins=["*"]` par la liste de vos domaines
3. Commit et push sur GitHub
4. Redémarrer l'instance Vast.ai

**Vérification :**
```bash
# Tester depuis un domaine non autorisé (doit échouer)
curl -H "Origin: https://evil.com" http://votre-instance.vast.ai:8000/health
```

#### 2. Gestion des Tokens (CRITIQUE)

**Règles de sécurité :**

✅ **À FAIRE :**
- Token Hugging Face stocké uniquement dans variables d'environnement Vast.ai
- Token avec permissions minimales (Read uniquement)
- Token régénéré tous les 90 jours minimum
- Token jamais commité dans Git
- Token jamais affiché dans les logs

❌ **À NE JAMAIS FAIRE :**
- Hardcoder le token dans le code
- Commit le token dans Git
- Partager le token par email/chat non chiffré
- Utiliser le même token pour plusieurs projets
- Token avec permissions Write si non nécessaire

**Vérification :**
```bash
# Vérifier qu'aucun token n'est dans le code (version améliorée)
grep -r "hf_\|HUGGINGFACE_TOKEN\|HF_TOKEN" \
  Backend/ \
  --exclude-dir=.git \
  --exclude-dir=venv \
  --exclude-dir=__pycache__ \
  --exclude-dir=.venv \
  --exclude="*.pyc"
# Résultat attendu : Aucun résultat (ou seulement les commentaires/documentation)
```

#### 3. Rate Limiting (RECOMMANDÉ)

**Problème :** Aucune protection contre l'abus (spam, DoS)

**Solution :** Ajouter rate limiting sur les endpoints

**Fichier à modifier :** `Backend/app_runpod.py`

**Ajout après les imports :**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

**Ajout sur les endpoints :**
```python
@app.post("/chat")
@limiter.limit("10/minute")  # 10 requêtes par minute par IP
def chat(req: ChatRequest):
    ...

@app.post("/evaluate")
@limiter.limit("5/minute")  # 5 requêtes par minute par IP
def evaluate(req: EvaluateRequest):
    ...
```

**Dépendance à ajouter :** `slowapi>=0.1.9` dans `requirements.runpod.txt`

**⚠️ Important :** Après ajout de `slowapi`, redéployer complètement l'instance (rebuild Docker requis)

#### 4. Validation des Inputs (CRITIQUE)

**Vérification actuelle :** Pydantic valide les types mais pas le contenu

**Améliorations nécessaires :**

```python
from pydantic import BaseModel, field_validator
import html

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[List[str]]] = None
    
    @field_validator('message')  # Pydantic v2 (requirements.runpod.txt spécifie >=2.5.0)
    @classmethod
    def validate_message(cls, v: str) -> str:
        # Limiter la longueur
        if len(v) > 2000:
            raise ValueError('Message trop long (max 2000 caractères)')
        
        # Rejeter les tentatives d'injection XSS
        xss_patterns = ['<script', 'javascript:', 'onerror=', 'onload=', '<iframe']
        if any(pattern in v.lower() for pattern in xss_patterns):
            raise ValueError('Contenu non autorisé')
        
        # Échapper les entités HTML
        v = html.escape(v)
        
        return v
```

#### 5. HTTPS (RECOMMANDÉ)

**Problème :** Vast.ai peut exposer en HTTP par défaut

**Solutions :**

**Option A : Cloudflare Tunnel (RECOMMANDÉ - Gratuit)**

**Étapes détaillées :**

1. **Créer compte Cloudflare** : https://dash.cloudflare.com/sign-up
2. **Installer cloudflared** sur votre machine locale :
   ```bash
   # macOS
   brew install cloudflare/cloudflare/cloudflared
   
   # Linux
   wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
   chmod +x cloudflared-linux-amd64
   sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
   ```
3. **Authentifier** :
   ```bash
   cloudflared tunnel login
   ```
4. **Créer un tunnel** :
   ```bash
   cloudflared tunnel create spinoza-secours
   ```
5. **Configurer le tunnel** (créer `config.yml`) :
   ```yaml
   tunnel: [tunnel-id]
   credentials-file: /path/to/credentials.json
   
   ingress:
     - hostname: spinoza-secours.votre-domaine.com
       service: http://votre-instance.vast.ai:8000
     - service: http_status:404
   ```
6. **Démarrer le tunnel** :
   ```bash
   cloudflared tunnel run spinoza-secours
   ```
7. **Configurer DNS** dans Cloudflare :
   - Type : CNAME
   - Nom : spinoza-secours (ou @ pour racine)
   - Cible : [tunnel-id].cfargotunnel.com
8. **URL finale** : `https://spinoza-secours.votre-domaine.com`

**Avantages :** Gratuit, HTTPS automatique, pas d'exposition directe de l'IP Vast.ai

**Option B : Vast.ai avec HTTPS natif**

**Vérifier dans le dashboard Vast.ai** si HTTPS est disponible :
- Dashboard → Instance → Network → HTTPS
- Si disponible, suivre les instructions Vast.ai

**Option C : ngrok avec HTTPS (Alternative)**

**Étapes :**
1. Créer compte ngrok : https://dashboard.ngrok.com/signup
2. Installer ngrok
3. Authentifier : `ngrok config add-authtoken [token]`
4. Créer tunnel : `ngrok http http://votre-instance.vast.ai:8000`
5. URL HTTPS fournie automatiquement

**Inconvénient :** URL change à chaque démarrage (comme Colab)

**Vérification :**
```bash
# Tester que HTTPS fonctionne
curl https://votre-url-cloudflare.com/health
# ou
curl https://votre-instance.vast.ai:8000/health  # Si HTTPS natif
```

#### 6. Monitoring des Coûts (CRITIQUE)

**Risque :** Facture explosive si instance laissée tourner

**Solutions :**

1. **Alertes Vast.ai** (si disponible dans le dashboard)
   - Dashboard → Settings → Alerts
   - Configurer une alerte à $X dépensés
   - Configurer une alerte si instance tourne > X heures
   - **Note :** Vérifier si cette fonctionnalité existe dans votre compte

2. **Monitoring manuel quotidien**
   - Vérifier le dashboard Vast.ai : https://vast.ai/console/instances
   - Noter les coûts dans un fichier (ex: `docs/logs/couts_vast_ai.md`)
   - **Fréquence recommandée :** Quotidien si instance active

3. **Script de monitoring des coûts** (voir section Maintenance → Monitoring)

4. **Bonnes pratiques :**
   - **Toujours arrêter l'instance** après usage
   - **Ne pas laisser tourner** en veille "au cas où"
   - **Configurer un rappel** (calendrier, alarme) pour vérifier l'instance
   - **Noter dans un calendrier** les dates de démarrage/arrêt

**Dashboard Vast.ai :** https://vast.ai/console/instances

#### 7. Protection Prompt Injection (SPÉCIFIQUE LLM)

**Risque :** Utilisateur peut injecter des prompts malveillants

**Protection actuelle :** Partielle (validation basique)

**Améliorations :**

```python
def sanitize_user_input(text: str) -> str:
    """Nettoie l'input utilisateur pour éviter prompt injection"""
    # Supprimer les tentatives de formatage spécial
    text = text.replace('[INST]', '').replace('[/INST]', '')
    text = text.replace('<s>', '').replace('</s>', '')
    # Limiter la longueur
    return text[:2000]

# Utiliser dans les endpoints
@app.post("/chat")
def chat(req: ChatRequest):
    sanitized_message = sanitize_user_input(req.message)
    ...
```

#### 8. Logs et Données Sensibles

**Règles :**

✅ **À FAIRE :**
- Ne pas logger les tokens/secrets
- Anonymiser les données utilisateur dans les logs
- Limiter les logs en production (INFO uniquement)

❌ **À NE JAMAIS FAIRE :**
- Logger les tokens Hugging Face
- Logger les messages utilisateurs complets
- Exposer les logs publiquement

**Vérification :**
```bash
# Vérifier les logs ne contiennent pas de tokens
grep -i "hf_\|token\|secret" logs/*.log
# Résultat attendu : Aucun résultat
```

### Checklist Sécurité Avant Production

- [ ] CORS restreint aux domaines autorisés uniquement
- [ ] Token Hugging Face en variable d'environnement (pas hardcodé)
- [ ] Rate limiting activé sur endpoints critiques
- [ ] Validation stricte des inputs utilisateur
- [ ] HTTPS configuré (ou reverse proxy avec HTTPS)
- [ ] Monitoring des coûts configuré
- [ ] Protection prompt injection implémentée
- [ ] Logs ne contiennent pas de données sensibles
- [ ] `.env` dans `.gitignore` (si utilisé)
- [ ] Scan sécurité effectué (`grep -r "hf_\|password\|secret"` = vide)

---

## 🔧 Maintenance et Monitoring

### 1. Monitoring de Base

#### Métriques à Surveiller

**Disponibilité :**
- Uptime de l'instance Vast.ai
- Temps de réponse des endpoints
- Taux d'erreur (5xx)

**Performance :**
- Latence moyenne des requêtes
- Utilisation GPU (VRAM, compute)
- Temps de génération du modèle

**Coûts :**
- Coût par heure
- Coût total depuis démarrage
- Estimation coût mensuel si 24/7

**Où surveiller :**
- **Dashboard Vast.ai :** https://vast.ai/console/instances
- **Logs instance :** Dashboard → Instance → Logs
- **Health check :** `curl http://votre-instance.vast.ai:8000/health`

#### Health Check Automatisé

**Script de monitoring (à créer) :**

```bash
#!/bin/bash
# monitor_vast_ai.sh
# Usage: Ajouter dans cron pour vérifier toutes les heures

INSTANCE_URL="http://votre-instance.vast.ai:8000"
ALERT_EMAIL="votre-email@example.com"

# Test health check
response=$(curl -s -o /dev/null -w "%{http_code}" "$INSTANCE_URL/health")

if [ "$response" != "200" ]; then
    echo "ALERT: Instance Vast.ai down (HTTP $response)" | mail -s "Vast.ai Alert" "$ALERT_EMAIL"
fi
```

**Cron :**
```bash
# Vérifier toutes les heures
0 * * * * /chemin/vers/monitor_vast_ai.sh
```

### 2. Logs et Debugging

#### Configuration des Logs

**Niveaux de log :**
- **Production :** INFO (pas de DEBUG)
- **Développement :** DEBUG

**Fichier :** `Backend/app_runpod.py` lignes 619-624

```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=PORT,
    log_level="info"  # "info" en prod, "debug" en dev
)
```

#### Rotation des Logs

**Si logs volumineux :**
- Configurer logrotate ou équivalent
- Conserver 7 jours de logs maximum
- Archivage au-delà

#### Accès aux Logs Vast.ai

**Dashboard :** https://vast.ai/console/instances → Votre instance → **Logs**

**Commandes utiles :**
```bash
# Voir les dernières erreurs
# (via dashboard Vast.ai ou SSH si disponible)

# Filtrer les erreurs
grep -i "error\|exception\|traceback" logs.txt

# Voir les requêtes
grep "POST /chat" logs.txt
```

### 3. Backups et Récupération

#### Configuration à Sauvegarder

**Fichiers critiques :**
- `Backend/app_runpod.py` (code principal)
- `Backend/Dockerfile.runpod` (configuration Docker)
- `Backend/requirements.runpod.txt` (dépendances)
- Variables d'environnement Vast.ai (notées dans un endroit sûr)

**Où sauvegarder :**
- ✅ GitHub (déjà fait si vous poussez le code)
- ✅ Backup local (copie des fichiers)
- ✅ Documentation (noter la configuration)

#### Plan de Reprise Après Sinistre

**Scénario : Instance crash ou perdue**

**Temps de récupération estimé :** 20-30 minutes

**Étapes :**
1. Créer nouvelle instance Vast.ai (5 min)
2. Configurer identique à l'ancienne (5 min)
3. Déployer depuis GitHub (10-15 min)
4. Tester les endpoints (2 min)
5. Mettre à jour le frontend si URL change (2 min)

**Documentation :**
- Noter l'URL de backup si vous créez une instance de secours
- Garder une copie de la configuration Vast.ai

### 4. Mises à Jour de Sécurité

#### Dépendances Python

**Vérification régulière :**
```bash
# Vérifier les vulnérabilités
pip-audit -r requirements.runpod.txt

# Mettre à jour les dépendances
pip list --outdated
```

**Fréquence :** Mensuelle minimum

**Outils :**
- `pip-audit` : Scan des CVE
- `safety` : Alternative à pip-audit
- GitHub Dependabot : Alertes automatiques (si repo GitHub)

#### Mises à Jour du Modèle

**Quand mettre à jour :**
- Nouvelle version du LoRA adapter
- Amélioration du prompt système
- Correction de bugs

**Procédure :**
1. Tester localement d'abord
2. Commit et push sur GitHub
3. Redémarrer l'instance Vast.ai
4. Vérifier que tout fonctionne

### 5. Rotation des Secrets

#### Token Hugging Face

**Fréquence :** Tous les 90 jours minimum

**Procédure :**
1. Créer nouveau token sur https://huggingface.co/settings/tokens
2. Mettre à jour variable d'environnement Vast.ai
3. Redémarrer l'instance
4. Vérifier que tout fonctionne
5. Révoquer l'ancien token (après vérification)

### 6. Documentation des Incidents

#### Template d'Incident

**Créer un fichier :** `docs/logs/incidents.md`

**Format :**
```markdown
## Incident [DATE]

**Type :** [Downtime / Erreur / Sécurité]
**Durée :** [X minutes/heures]
**Cause :** [Description]
**Impact :** [Utilisateurs affectés, fonctionnalités]
**Résolution :** [Actions prises]
**Prévention :** [Mesures pour éviter récurrence]
```

### 7. Maintenance Préventive

#### Tâches Régulières

**Quotidien :**
- [ ] Vérifier que l'instance tourne (health check)
- [ ] Vérifier les coûts dans le dashboard

**Hebdomadaire :**
- [ ] Vérifier les logs pour erreurs
- [ ] Tester un dialogue complet
- [ ] Vérifier les performances (latence)

**Mensuel :**
- [ ] Audit sécurité (scan dépendances)
- [ ] Vérifier rotation des secrets
- [ ] Mettre à jour documentation si changements
- [ ] Backup de la configuration

**Trimestriel :**
- [ ] Review complet sécurité
- [ ] Optimisation des coûts
- [ ] Mise à jour des dépendances majeures

### 8. Alertes et Notifications

#### Alertes Recommandées

**À configurer si possible :**
- Instance down (health check échoue)
- Coût dépassant un seuil ($X/heure ou $Y/jour)
- Erreurs répétées dans les logs
- Latence anormalement élevée

**Moyens :**
- Email (si Vast.ai le permet)
- Webhook (Slack, Discord, etc.)
- Script de monitoring (voir section Monitoring)

---

## 🐛 Troubleshooting

### Problème : Le modèle ne charge pas

**Symptômes :**
- Erreur `ValueError: HF_TOKEN ou HUGGINGFACE_TOKEN doit être défini`
- Erreur `401 Unauthorized` lors du téléchargement

**Solutions :**
1. Vérifier que `HF_TOKEN` est bien configuré dans les variables d'environnement Vast.ai
2. Vérifier que le token a les permissions de lecture sur Hugging Face
3. Vérifier que le token n'a pas expiré
4. Vérifier les logs pour voir l'erreur exacte

**Lien vérification token :** https://huggingface.co/settings/tokens

### Problème : L'API ne répond pas

**Symptômes :**
- Timeout lors des requêtes
- Erreur de connexion
- 502 Bad Gateway

**Solutions :**
1. Vérifier que l'instance est bien démarrée (status "Running")
2. Vérifier que le port 8000 est bien exposé
3. Vérifier les logs pour voir si le serveur FastAPI a démarré
4. Tester avec `curl` directement depuis votre machine
5. Vérifier l'URL publique dans le dashboard Vast.ai

**Lien dashboard :** https://vast.ai/console/instances

### Problème : Erreur CORS

**Symptômes :**
- `Access to fetch at '...' from origin '...' has been blocked by CORS policy`
- Erreur dans la console du navigateur

**Solutions :**
1. Vérifier que `allow_origins` dans `app_runpod.py` inclut votre domaine
2. Modifier `app_runpod.py` ligne 543 (voir section Sécurité pour détails complets) :
   ```python
   allow_origins=[
       "https://fjdaz.com",
       "https://www.fjdaz.com",
       # "http://localhost:8000",  # Retirer en production
   ]
   ```
3. Commit et push sur GitHub
4. Redémarrer l'instance Vast.ai
5. Vérifier que l'URL backend est correcte (http vs https)
6. **Vérifier que fjdaz.com est en HTTPS** (mixed content si HTTP frontend + HTTPS backend)

### Problème : GPU non détecté

**Symptômes :**
- `gpu_available: false` dans `/health`
- Latence très élevée
- Erreur `CUDA not available`

**Solutions :**
1. Vérifier que l'instance a bien un GPU (RTX 3090) dans le dashboard Vast.ai
2. Vérifier les logs pour voir les erreurs CUDA
3. Vérifier que PyTorch détecte le GPU : Chercher `torch.cuda.is_available()` dans les logs
4. **Vérifier la version CUDA** dans les logs :
   ```bash
   # Dans les logs Vast.ai, chercher :
   nvidia-smi
   # ou
   CUDA Version: X.X
   ```
5. Si problème persiste, utiliser une image Docker avec CUDA explicite (voir ci-dessous)

**Note :** T4 et RTX 3090 sont tous deux supportés par PyTorch 2.0+ et bitsandbytes 0.41.0+

**Dockerfile avec CUDA Explicite (Alternative) :**

Si le Dockerfile actuel ne fonctionne pas, créer `Backend/Dockerfile.vast.cuda` :

```dockerfile
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Installer Python 3.10
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Créer lien symbolique python
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# Définir le répertoire de travail
WORKDIR /app

# Copier requirements.txt
COPY requirements.runpod.txt /app/requirements.txt

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier les fichiers de l'application
COPY app_runpod.py /app/app.py

# Exposer le port FastAPI
EXPOSE 8000

# Commande de démarrage
CMD ["python", "/app/app.py"]
```

**Utilisation :** Remplacer `Dockerfile.runpod` par `Dockerfile.vast.cuda` dans la configuration Vast.ai

### Problème : Erreur de mémoire (OOM)

**Symptômes :**
- `CUDA out of memory` dans les logs
- Crash de l'instance

**Solutions :**
1. Vérifier que le GPU a assez de VRAM (RTX 4090 ou RTX 3090 24GB suffit)
2. Réduire `max_new_tokens` dans `app_runpod.py` (lignes 401, 449, 489)
3. Vérifier que la quantization 4-bit est bien activée (déjà fait dans le code)

### Problème : Le Maïathon ne fonctionne pas

**Symptômes :**
- Le score ne s'affiche pas
- L'évaluation finale échoue

**Solutions :**
1. Vérifier les logs du backend (dashboard Vast.ai)
2. Vérifier que l'endpoint `/evaluate` répond correctement
3. Ouvrir la console développeur pour voir les erreurs JavaScript
4. Vérifier que le format des données correspond à ce que le frontend attend
5. Tester l'endpoint `/evaluate` directement avec curl

---

## 📋 Checklist Complète

### Préparation
- [ ] Compte Vast.ai créé : https://vast.ai/
- [ ] Token Hugging Face obtenu : https://huggingface.co/settings/tokens
- [ ] Token noté dans un endroit sûr
- [ ] Fichiers vérifiés (`Dockerfile.runpod`, `app_runpod.py`, `requirements.runpod.txt`)
- [ ] (Optionnel) Dépôt GitHub préparé

### Configuration Instance
- [ ] Instance Vast.ai créée : https://vast.ai/console/create
- [ ] GPU sélectionné : **RTX 4090 ($0.29/h)** ⭐⭐ ou **RTX 3090 ($0.20-0.40/h)** ⭐ (excellent si < $0.25/h)
- [ ] Dockerfile configuré (GitHub ou direct)
- [ ] Variables d'environnement configurées (`HF_TOKEN`, `PORT`)
- [ ] Container Disk : 50GB minimum
- [ ] Port 8000 exposé

### Déploiement
- [ ] Instance lancée
- [ ] Build Docker réussi (5-10 min)
- [ ] Modèle chargé (10-15 min)
- [ ] Serveur FastAPI démarré
- [ ] URL publique récupérée

### Tests
- [ ] Test `/health` réussi
- [ ] Test `/init` réussi
- [ ] Test `/chat` réussi
- [ ] Test `/evaluate` réussi
- [ ] Script de test automatique réussi

### Frontend
- [ ] `index_spinoza.html` modifié (ligne 127)
- [ ] URL backend mise à jour
- [ ] Test local réussi (console sans erreurs)
- [ ] Frontend mis à jour sur serveur (si hébergé)
- [ ] Test en production réussi

### Validation
- [ ] Test complet frontend + backend réussi
- [ ] 5 échanges complets fonctionnent
- [ ] Score s'affiche en temps réel
- [ ] Évaluation finale fonctionne
- [ ] Message final de Spinoza s'affiche
- [ ] Titre "Maïathon" et "Réfléchis. Reformule. Questionne." s'affichent
- [ ] Performances vérifiées (latence acceptable)
- [ ] Stabilité vérifiée (plusieurs dialogues)

### Documentation
- [ ] URL Vast.ai notée
- [ ] Date de déploiement notée
- [ ] Configuration documentée

### Sécurité (CRITIQUE)
- [ ] CORS restreint aux domaines autorisés uniquement (`allow_origins` modifié)
- [ ] Token Hugging Face en variable d'environnement (pas hardcodé dans le code)
- [ ] Aucun token/secret dans le code (vérifié avec `grep -r "hf_"`)
- [ ] Rate limiting activé sur endpoints critiques (si implémenté)
- [ ] Validation stricte des inputs utilisateur (longueur, contenu malveillant)
- [ ] HTTPS configuré (ou reverse proxy avec HTTPS)
- [ ] Monitoring des coûts configuré (alertes si disponible)
- [ ] Protection prompt injection implémentée (si applicable)
- [ ] Logs ne contiennent pas de données sensibles (tokens, secrets)
- [ ] `.env` dans `.gitignore` (si utilisé)

### Maintenance
- [ ] Monitoring de base configuré (health check automatique)
- [ ] Accès aux logs Vast.ai documenté et testé
- [ ] Backup de la configuration effectué (code + config Vast.ai)
- [ ] Plan de reprise après sinistre documenté
- [ ] Rotation des secrets planifiée (token HF tous les 90 jours)
- [ ] Tâches de maintenance définies (quotidien, hebdo, mensuel)
- [ ] Script de monitoring créé (si applicable)
- [ ] Documentation des incidents préparée (template)

---

## 📚 Ressources et Liens

### Plateformes
- **Vast.ai** : https://vast.ai/
- **Dashboard Vast.ai** : https://vast.ai/console/instances
- **Créer Instance** : https://vast.ai/console/create
- **Hugging Face** : https://huggingface.co/
- **Tokens HF** : https://huggingface.co/settings/tokens
- **GitHub** : https://github.com/

### Documentation
- **Guide Vast.ai détaillé** : `docs/references/vast-ai/README_VAST_AI.md`
- **Quick Start** : `docs/references/vast-ai/QUICKSTART_VAST_AI.md`
- **Guide Vast.ai** : `docs/references/vast-ai/README_VAST_AI.md`
- **Guide RunPod** : `docs/references/vast-ai/README_RUNPOD.md`
- **Guide Frontend** : `Frontend/GUIDE_UPDATE_VAST_AI.md`
- **Architecture complète** : `docs/references/ARCHITECTURE_COMPLETE.md`

### Modèles Hugging Face
- **Mistral 7B Base** : https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2
- **LoRA Spinoza** : https://huggingface.co/FJDaz/mistral-7b-philosophes-lora

### Support
- **Documentation Vast.ai** : https://docs.vast.ai/
- **Support Vast.ai** : Via dashboard ou email
- **Documentation Hugging Face** : https://huggingface.co/docs

---

## 💰 Coûts et Optimisation

### Coûts Estimés

**RTX 4090 sur Vast.ai (RECOMMANDÉ) :**
- **Par heure** : **$0.29** (~0.26€/h) ✅ (tarif vérifié Janvier 2025)
- **3h de démo** : **$0.87** (0.78€)
- **8h/jour, 22j/mois** : **$51.04** (45.94€)
- **~60€/mois** : **~230h/mois** (~7.7h/jour)
- **24/7** : **$208.80/mois** (187.92€)

**RTX 3090 sur Vast.ai (Alternative) :**
- **Par heure** : $0.20-0.40 (~0.18-0.36€/h)
- **3h de démo** : $0.60-1.20 (0.54-1.08€)
- **8h/jour, 22j/mois** : $35.20-70.40 (31.68-63.36€)
- **~50€/mois** : **~220-280h/mois** (~7-9h/jour) selon tarif
- **24/7** : $144-288/mois (129.60-259.20€)

**Comparaison RTX 4090 vs RTX 3090 :**

**Différence de Performance (Inférence LLM) :**
- **RTX 4090** : ~50-70% plus rapide que RTX 3090 pour l'inférence
- **RTX 3090** : Performance déjà excellente (2-3x plus rapide que T4)

**Exemples Concrets de Latence (Mistral 7B 4-bit) :**
| Opération | T4 (Colab) | RTX 3090 | RTX 4090 |
|-----------|------------|----------|----------|
| **Inférence dialogue** | 2-5s | 1-3s | **0.7-1.5s** |
| **Évaluation finale** | 5-10s | 3-6s | **2-4s** |
| **Latence totale** | 8-16s | 4-9s | **2.7-5.5s** |

**Différence RTX 4090 vs RTX 3090 :**
- **Gain de temps** : ~1.3-3.5 secondes par requête complète
- **Pour 100 requêtes** : ~2-6 minutes économisées
- **Impact utilisateur** : Perceptible mais RTX 3090 reste très fluide

**Recommandation :**
- **RTX 4090** si priorité performance maximale ou si RTX 3090 > $0.25/h
- **RTX 3090** si budget serré ou si trouvé à $0.20-0.25/h (économies 14-31%)
- **Les deux sont d'excellentes solutions** pour Mistral 7B + LoRA

### Optimisation des Coûts

1. **Arrêter l'instance** immédiatement après usage
2. **Ne pas laisser tourner** en veille
3. **Utiliser un Volume Disk persistant** seulement si usage fréquent (coût supplémentaire)
4. **Monitorer les coûts** dans le dashboard Vast.ai
5. **Auto-sleep automatique** : Voir section ci-dessous

---

## ⏰ Auto-Sleep (Arrêt Automatique)

### Principe

L'auto-sleep permet d'arrêter automatiquement l'instance Vast.ai après une période d'inactivité, évitant les coûts inutiles.

### Implémentation

**Fichier :** `Backend/auto_sleep.py`

**Fonctionnement :**
1. Le script surveille l'activité de l'API (requêtes `/chat`, `/evaluate`, `/init`)
2. Chaque requête met à jour un timestamp de dernière activité
3. Si aucune activité pendant X minutes (défaut: 30 min), arrêt de l'instance

**Configuration :**

```bash
# Lancer l'auto-sleep en arrière-plan
python3 Backend/auto_sleep.py --timeout 1800 --check-interval 60 &

# Options :
# --timeout : Temps d'inactivité avant arrêt (défaut: 1800s = 30min)
# --check-interval : Fréquence de vérification (défaut: 60s)
```

**Exemples de timeout :**
- **15 minutes** : `--timeout 900` (usage ponctuel)
- **30 minutes** : `--timeout 1800` (défaut, usage normal)
- **1 heure** : `--timeout 3600` (usage prolongé)

### Intégration dans Dockerfile

**Option 1 : Lancer auto-sleep au démarrage**

Ajouter dans `Dockerfile.runpod` :

```dockerfile
# Copier le script auto-sleep
COPY auto_sleep.py /app/auto_sleep.py

# Lancer auto-sleep en arrière-plan au démarrage
CMD python3 /app/auto_sleep.py --timeout 1800 & python3 /app/app.py
```

**Option 2 : Utiliser un script de démarrage**

Créer `start.sh` :

```bash
#!/bin/bash
# Lancer auto-sleep en arrière-plan
python3 /app/auto_sleep.py --timeout 1800 &
# Lancer FastAPI
python3 /app/app.py
```

### Limitations

⚠️ **Important :** Vast.ai n'a pas d'API publique pour arrêter automatiquement l'instance depuis le container.

**Solutions :**
1. **Arrêt manuel** : Le script log un message, vous devez arrêter depuis le dashboard
2. **Webhook** : Si Vast.ai ajoute une API, utiliser un webhook pour arrêter l'instance
3. **Monitoring externe** : Script externe qui surveille et arrête via dashboard (nécessite authentification)

### Alternative : Monitoring Externe

Créer un script externe qui :
1. Vérifie l'activité via `/health` toutes les X minutes
2. Si inactif, arrête l'instance via l'API Vast.ai (si disponible) ou envoie une alerte

**Fichier :** `Backend/monitor_and_sleep.sh` (à créer si besoin)

---

## 🚀 Cold Start (Démarrage à Froid)

### Qu'est-ce que le Cold Start ?

**Cold Start = Temps d'attente avant que l'API soit prête à répondre**

Quand tu démarres une instance Vast.ai, elle est vide. Il faut :
1. Installer les logiciels (Docker, Python, etc.)
2. Télécharger le modèle Mistral 7B (14GB)
3. Charger le modèle dans la mémoire GPU
4. Démarrer le serveur FastAPI

**Pendant ce temps, l'API ne répond pas encore !** ⏳

---

### Exemple Concret

**Scénario :** Tu démarres ton instance à 10h00 pour une démo à 10h30

**Avec Container Disk (gratuit) :**
```
10h00 → Tu démarres l'instance
10h00-10h10 → Build Docker (installation logiciels)
10h10-10h25 → Téléchargement Mistral 7B (14GB depuis internet)
10h25-10h27 → Chargement dans GPU
10h27 → ✅ API prête !
```
**Total : 27 minutes d'attente** ⏱️

**Avec Volume Disk (+$0.10-0.20/h) :**
```
10h00 → Tu démarres l'instance
10h00-10h10 → Build Docker (installation logiciels)
10h10 → Modèle déjà présent (pas de téléchargement) ✅
10h10-10h12 → Chargement dans GPU
10h12 → ✅ API prête !
```
**Total : 12 minutes d'attente** ⏱️

**Gain : 15 minutes économisées !**

---

### Comparaison Simple

| Type Stockage | Coût | Temps Cold Start | Quand utiliser ? |
|---------------|------|------------------|-----------------|
| **Container Disk** | Gratuit | **16-27 min** | Usage ponctuel (1-2h puis arrêt) |
| **Volume Disk** | +$0.10-0.20/h | **6-12 min** | Usage fréquent (plusieurs fois/jour) |

---

### Pourquoi cette Différence ?

**Container Disk (gratuit) :**
- Stockage temporaire, effacé à l'arrêt
- À chaque démarrage → **retélécharger le modèle** (14GB)
- Comme si tu réinstallais Windows à chaque fois que tu allumes ton PC

**Volume Disk (payant) :**
- Stockage permanent, conservé entre redémarrages
- Le modèle reste sur le disque
- Comme un disque dur externe : les fichiers restent même si tu éteins

---

### Quand Choisir Volume Disk ?

**Volume Disk est rentable si :**
- Tu redémarres l'instance **plusieurs fois par jour**
- Tu utilises l'instance **> 4h/jour**
- Le gain de temps (15 min × nombre de redémarrages) vaut le coût supplémentaire

**Exemple de calcul :**
- 2 redémarrages/jour × 15 min économisées = **30 min/jour**
- Volume Disk : +$0.15/h × 8h = **$1.20/jour**
- Si tu gagnes 30 min/jour, ça vaut ~$0.50-1.00 selon ta valeur du temps
- **→ Volume Disk rentable si tu redémarres souvent**

**Container Disk est suffisant si :**
- Tu démarres l'instance **1 fois par jour** (ou moins)
- Tu l'utilises **quelques heures puis tu l'arrêtes**
- Tu préfères économiser $0.10-0.20/h

---

### Résumé Ultra-Simple

**Cold Start = Temps d'attente au démarrage**

- **Container Disk** : 16-27 min (gratuit, mais lent)
- **Volume Disk** : 6-12 min (payant, mais rapide)

**Recommandation :**
- **Démo ponctuelle** → Container Disk OK (attendre 20-30 min une fois)
- **Usage quotidien** → Volume Disk (gagner 15 min à chaque démarrage)

### Comparaison avec Colab

| Critère | Colab | Vast.ai RTX 4090 | Vast.ai RTX 3090 |
|---------|-------|------------------|------------------|
| **Coût** | Gratuit* | **$0.29/h** ✅ | **$0.20-0.40/h** ✅ |
| **Stabilité** | ⚠️ Instable | ✅ Stable | ✅ Stable |
| **Performance** | T4 (baseline) | **3-4x plus rapide** | **2-3x plus rapide** ✅ |
| **VRAM** | 16GB | 24GB | 24GB ✅ |
| **URL** | Change à chaque session | ✅ Fixe | ✅ Fixe |
| **Contrôle** | Limité | ✅ Total | ✅ Total |
| **Recommandation** | - | ⭐⭐ Meilleure perf | ⭐ Excellent si < $0.25/h |

*Colab : Gratuit mais avec limitations, timeout, instabilité

---

## 🎯 Prochaines Étapes

### Après Migration Réussie

1. **Monitorer les performances** pendant quelques jours
2. **Optimiser la latence** si nécessaire (voir optimisations possibles)
3. **Documenter les coûts réels** vs estimés
4. **Mettre à jour la documentation** avec l'URL finale
5. **Informer les utilisateurs** du changement (si nécessaire)

### Améliorations Futures

1. **Volume Disk persistant** : Éviter de retélécharger le modèle (voir calcul rentabilité section 3.5)
2. **Optimisations de latence** : Réduire `max_new_tokens`, greedy decoding
3. **Monitoring** : Ajouter des métriques de performance
4. **Backup** : Configurer un backup de la configuration

---

## 🔄 Procédures Post-Déploiement

### Procédure de Rollback

**Scénario :** Le déploiement Vast.ai échoue ou cause des problèmes

**Temps estimé :** 5-10 minutes

**Étapes :**

1. **Arrêter l'instance Vast.ai**
   - Dashboard → Instance → Stop
   - Confirmer l'arrêt

2. **Rétablir l'ancien backend (Colab + ngrok)**
   - Ouvrir le notebook Colab
   - Exécuter les cellules dans l'ordre
   - Récupérer la nouvelle URL ngrok

3. **Mettre à jour le frontend**
   - Modifier `Frontend/index_spinoza.html` ligne 127
   - Remplacer URL Vast.ai par URL ngrok
   - Tester la connexion

4. **Documenter le rollback**
   - Noter dans `docs/logs/incidents.md`
   - Identifier la cause du problème
   - Planifier correction avant nouveau déploiement

**Note :** Garder l'instance Vast.ai arrêtée (pas supprimée) pour investigation

### Procédure de Migration GPU

**Scénario :** Passer de RTX 3090 à RTX 4090 (ou autre GPU)

**Temps estimé :** 20-30 minutes

**Étapes :**

1. **Créer nouvelle instance avec nouveau GPU**
   - Dashboard → Create
   - Sélectionner RTX 4090 (ou autre)
   - **Copier la configuration** de l'ancienne instance :
     - Même Dockerfile
     - Mêmes variables d'environnement
     - Même Container Disk (ou Volume Disk si utilisé)

2. **Déployer et tester**
   - Suivre étapes 4-5 du plan principal
   - Vérifier que tout fonctionne

3. **Mettre à jour le frontend** (si URL change)
   - Modifier `Frontend/index_spinoza.html` ligne 127
   - Nouvelle URL Vast.ai

4. **Arrêter l'ancienne instance**
   - Dashboard → Ancienne instance → Stop
   - Vérifier les coûts finaux

5. **Comparer les performances**
   - Latence avant/après
   - Coûts avant/après
   - Documenter les gains

**Note :** Garder l'ancienne instance arrêtée 24h avant suppression (au cas où)

### Procédure de Mise à Jour du Code

**Scénario :** Modifier le code sans tout redéployer

**Temps estimé :** 10-15 minutes

**Étapes :**

1. **Modifier le code localement**
   - Faire les changements dans `Backend/app_runpod.py` (ou autres fichiers)

2. **Tester localement** (si possible)
   - Tester les modifications
   - Vérifier qu'il n'y a pas d'erreurs

3. **Commit et push sur GitHub**
   ```bash
   git add Backend/app_runpod.py
   git commit -m "Description des changements"
   git push origin main
   ```

4. **Redémarrer l'instance Vast.ai**
   - Dashboard → Instance → Restart
   - **OU** si déploiement depuis GitHub :
     - Dashboard → Instance → Rebuild
     - L'instance va rebuild depuis le dernier commit

5. **Attendre le redémarrage**
   - Build : 5-10 min (si rebuild complet)
   - Chargement modèle : 10-15 min (si Container Disk)
   - Chargement modèle : 2-3 min (si Volume Disk persistant)

6. **Tester les changements**
   - Health check
   - Test d'un dialogue complet
   - Vérifier que les modifications fonctionnent

**Note :** Si Volume Disk persistant, le modèle n'est pas retéléchargé → Gain de temps

### Procédure de Test A/B (Colab vs Vast.ai)

**Scénario :** Tester Vast.ai en parallèle de Colab avant migration complète

**Temps estimé :** 30 minutes setup + tests

**Étapes :**

1. **Déployer Vast.ai** (suivre plan principal)
   - Créer instance Vast.ai
   - Déployer et tester
   - Noter l'URL Vast.ai

2. **Garder Colab actif**
   - Ne pas arrêter le notebook Colab
   - Garder l'URL ngrok active

3. **Modifier le frontend pour test A/B**
   - Créer une version de test : `Frontend/index_spinoza_test.html`
   - Modifier ligne 127 pour pointer vers Vast.ai
   - Garder `index_spinoza.html` avec Colab

4. **Tester en parallèle**
   - Ouvrir `index_spinoza.html` (Colab) dans un onglet
   - Ouvrir `index_spinoza_test.html` (Vast.ai) dans un autre onglet
   - Faire le même dialogue sur les deux
   - Comparer :
     - Latence
     - Qualité des réponses
     - Stabilité

5. **Documenter les résultats**
   - Créer `docs/tests/test_ab_colab_vs_vast.md`
   - Noter les différences
   - Décider de la migration complète

6. **Après décision**
   - Si Vast.ai meilleur : Migrer complètement (étapes 6-7 du plan)
   - Si Colab meilleur : Arrêter instance Vast.ai, garder Colab
   - Si équivalent : Choisir selon coûts/stabilité

**Durée recommandée du test :** 1-2 jours pour avoir assez de données

**Coût test :** ~$5-10 (instance Vast.ai 1-2 jours)

---

## ✅ Conclusion

Ce plan de migration vous guide étape par étape pour déployer Spinoza Secours sur Vast.ai. 

**Temps total estimé :** ~30-45 minutes (dont 15-20 min d'attente pour le modèle)

**Coût estimé :** 
- **RTX 4090 : $0.87** pour une démo de 3h ✅ (recommandé)
- RTX 3090 : $0.60-1.20 pour une démo de 3h

**Avantages :**
- ✅ URL fixe et stable
- ✅ Performance supérieure (RTX 4090 : 3-4x plus rapide que T4)
- ✅ Contrôle total
- ✅ Coûts maîtrisés (RTX 4090 : $0.29/h vérifié)

**En cas de problème :** Consulter la section Troubleshooting ou la documentation complète.

---

**Dernière mise à jour :** Janvier 2025  
**Version :** 1.2 (Finalisé - Vérifications complètes)

**Documents complémentaires :**
- `PLAN_MIGRATION_VAST_AI_CORRECTIONS.md` - Détails des corrections appliquées
- `VERIFICATION_PLAN_MIGRATION.md` - Rapport de vérification technique complète

