# 🏗️ Architecture Complète - Spinoza Secours HF & Maïeuthon

**Date :** Décembre 2024  
**Projet :** Assistant philosophique Spinoza avec système d'évaluation Maïeuthon  
**Version :** 1.0

---

## 📋 Table des Matières

1. [Vue d'Ensemble](#vue-densemble)
2. [Stack Technique](#stack-technique)
3. [Architecture Globale](#architecture-globale)
4. [Fonctionnement Spinoza Secours](#fonctionnement-spinoza-secours)
5. [Fonctionnement Maïeuthon](#fonctionnement-maïeuthon)
6. [Endpoints API](#endpoints-api)
7. [Flux de Données](#flux-de-données)
8. [Composants Principaux](#composants-principaux)

---

## 🎯 Vue d'Ensemble

**Spinoza Secours HF** est un assistant philosophique dialogique basé sur Mistral 7B fine-tuné, conçu pour guider des élèves de Terminale dans la compréhension de la philosophie de Spinoza.

**Maïeuthon** est un système d'évaluation hybride qui combine :
- **Score Frontend** : Évaluation en temps réel basée sur des critères lexicaux et comportementaux
- **Score Backend** : Évaluation par le modèle IA basée sur la compréhension, la coopération et la progression

### Objectifs

1. **Dialogue philosophique** : Guider l'élève vers la compréhension progressive des concepts spinoziens
2. **Évaluation formative** : Fournir un feedback en temps réel et une évaluation finale
3. **Pédagogie adaptative** : Adapter les réponses selon le niveau de compréhension de l'élève

---

## 🛠️ Stack Technique

### Backend

**Environnement :** Google Colab  
**Framework :** FastAPI  
**Serveur :** Uvicorn (ASGI)  
**Tunnel :** ngrok (exposition publique)

**Modèle IA :**
- **Base :** Mistral 7B (`mistralai/Mistral-7B-Instruct-v0.2`)
- **Fine-tuning :** LoRA adapter (`FJDaz/mistral-7b-philosophes-lora`)
- **Quantization :** 8-bit via `bitsandbytes`
- **Format :** ChatML (`<s>[INST] ... [/INST]`)

**Dépendances principales :**
```python
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
torch>=2.0.0
transformers>=4.35.0
bitsandbytes>=0.41.0
accelerate>=0.24.0
pydantic>=2.5.0
pyngrok>=5.0.0
```

### Frontend

**Technologies :**
- HTML5 vanilla
- JavaScript ES6+ (vanilla, pas de framework)
- CSS3 (responsive design)

**Fichiers principaux :**
- `Frontend/index_spinoza.html` : Interface utilisateur complète
- `Frontend/static/style.css` : Styles desktop
- `Frontend/static/responsive.css` : Styles mobile

**Fonts :**
- Serifa Std (titres, instructions)
- Letter Gothic Std (scores, résultats)
- Grotesque MT Std (interface générale)

### Infrastructure

**Hébergement Backend :** Google Colab (GPU T4/V100)  
**Hébergement Frontend :** Local ou serveur statique  
**Tunnel Public :** ngrok (URL publique temporaire)

---

## 🏗️ Architecture Globale

```
┌─────────────────────────────────────────────────────────────┐
│                    UTILISATEUR (Navigateur)                  │
└───────────────────────┬─────────────────────────────────────┘
                         │
                         │ HTTP/HTTPS
                         │
┌────────────────────────▼─────────────────────────────────────┐
│              FRONTEND (index_spinoza.html)                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • Interface utilisateur (desktop + mobile)         │   │
│  │  • Gestion dialogue (historique Q/A)                │   │
│  │  • Score Frontend (calcul temps réel)                │   │
│  │  • Appels API (fetch)                                │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         │ API REST (ngrok)
                         │
┌────────────────────────▼─────────────────────────────────────┐
│         BACKEND (RAG_Spinoza_secours.ipynb - Colab)          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  FastAPI Server (Uvicorn)                            │   │
│  │  ├── /health                                         │   │
│  │  ├── /init                                           │   │
│  │  ├── /chat                                           │   │
│  │  ├── /evaluate                                       │   │
│  │  └── /evaluate/incremental                           │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Modèle Mistral 7B + LoRA                           │   │
│  │  ├── Inference dialogue (température 0.7)           │   │
│  │  ├── Évaluation (température 0.3)                  │   │
│  │  └── Message final (température 1.1)                │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Système Maïeuthon                                   │   │
│  │  ├── Score Frontend (calculé côté frontend)         │   │
│  │  ├── Score Backend (évalué par modèle)               │   │
│  │  └── Score Final (somme des deux)                   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 💬 Fonctionnement Spinoza Secours

### Initialisation

1. **Frontend** : Appel `GET /init`
2. **Backend** : Sélection d'une question aléatoire depuis `QUESTIONS_BAC`
3. **Backend** : Génération du message de bienvenue avec la question
4. **Frontend** : Affichage du message et activation du formulaire

### Dialogue

**Prompt Système :** `SYSTEM_PROMPT_SPINOZA` (défini dans `Cellule_9.py`)

**Caractéristiques :**
- **Style** : Première personne ("je", "mon", "ma")
- **Ton** : Chaleureux, intime, encourageant
- **Méthode** : Maïeutique (questions ouvertes, reformulations)
- **Concepts** : conatus, affects, puissance d'agir, servitude vs liberté, Dieu = Nature

**Flux d'un échange :**
```
1. Utilisateur saisit question → Frontend
2. Frontend : POST /chat {message, history}
3. Backend : 
   - Formatage prompt (ChatML)
   - Inference modèle (température 0.7)
   - Décodage réponse
4. Backend : Retourne {response, ...}
5. Frontend : Affiche réponse dans historique
```

**Gestion du contexte :**
- Historique complet envoyé à chaque requête
- Format : `[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]`
- Limite : 5 échanges maximum (Maïeuthon)

---

## 🎮 Fonctionnement Maïeuthon

### Principe

Le **Maïeuthon** est un système d'évaluation hybride qui combine deux scores :

1. **Score Frontend** (`scoreFront`) : Calculé en temps réel côté client
2. **Score Backend** (`scoreBackend`) : Évalué par le modèle IA

**Score Final = Score Frontend + Score Backend**

### Score Frontend

**Base :** 50 points au démarrage

**Calcul en temps réel** (à chaque message utilisateur) :

1. **Lexical** (vocabulaire philosophique)
   - Mots de progression (`donc`, `je comprends`, `d'accord`) : **+3 points chacun**
   - Mots de résistance (`pas d'accord`, `faux`, `tu te trompes`) : **-2 points chacun**

2. **Longueur** (effort de réponse)
   - < 5 caractères : **-5 points**
   - > 100 caractères : **+3 points**
   - > 50 caractères : **+1 point**

3. **Cohérence** (qualité linguistique)
   - Mélange français/anglais excessif : **-3 points**
   - Répétitions de caractères : **-1 point par occurrence**
   - MAJUSCULES EXCESSIVES : **-1 point par occurrence**

4. **Répétition** (éviter les messages similaires)
   - Message trop similaire (>80%) : **-5 points**

5. **Fair-play** (respect du jeu)
   - Insultes : **-10 points**
   - Tentative de hack : **-10 à -15 points**

6. **Citations** (références à d'autres philosophes)
   - Détection de félicitations de Spinoza : **+5 points par philosophe cité**

**Fonction :** `calculateScore(message, previousMessages)` dans `index_spinoza.html`

### Score Backend

**Évaluation par le modèle IA** sur 3 critères (0-10 chacun) :

1. **Compréhension** (0-10)
   - Reformulation correcte des idées
   - Questions pertinentes
   - Liens entre concepts
   - **Bonus** : Distinction morale classique vs morale spinozienne → ≥ 9

2. **Coopération** (0-10)
   - Participation au dialogue
   - Réponses développées
   - Engagement

3. **Progression** (0-10)
   - Évolution de la compréhension
   - Amélioration entre début et fin
   - Synthèses partielles

**Total Backend = Compréhension + Coopération + Progression** (max 30)

**Prompt d'évaluation :** `PROMPT_EVALUATION` (défini dans cellule Maïeuthon)

### Système Hybride Optimisé

**Évaluation Incrémentale** (tous les 2 échanges) :
- Endpoint : `POST /evaluate/incremental`
- Évalue les 2 derniers échanges uniquement
- Stocke les scores dans `incremental_scores[dialogue_id]`
- Invisible à l'utilisateur (en arrière-plan)

**Évaluation Finale** (échange 5) :
- Endpoint : `POST /evaluate`
- Si scores incrémentaux disponibles → Agrège les scores
- Sinon → Évaluation complète du dialogue
- Génère le message final de Spinoza

**Gain de performance :** 25% (3 appels modèle au lieu de 4)

### Attribution de Titres

Basée sur le **Score Final** :

- **🌀 L'Égaré** : Score < 50
- **🔍 Le Sondeur** : Score ≥ 50 et < 80
- **🧭 L'Explorateur** : Score ≥ 80 et < 130
- **🌟 L'Illuminateur** : Score ≥ 130

---

## 🔌 Endpoints API

### `GET /health`

**Description :** Health check du serveur

**Réponse :**
```json
{
  "status": "ok",
  "model_loaded": true
}
```

### `GET /init`

**Description :** Initialise une nouvelle conversation

**Réponse :**
```json
{
  "message": "Bonjour, cher ami. [Question aléatoire]",
  "philosopher": "spinoza"
}
```

### `POST /chat`

**Description :** Envoie un message et reçoit la réponse de Spinoza

**Requête :**
```json
{
  "message": "Qu'est-ce que le conatus ?",
  "history": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

**Réponse :**
```json
{
  "response": "Le conatus est l'effort que chaque chose fait pour persévérer dans son être...",
  "thinking_time": 2.5
}
```

### `POST /evaluate/incremental`

**Description :** Évalue les 2 derniers échanges (évaluation incrémentale)

**Requête :**
```json
{
  "dialogue": "Spinoza: ...\nÉlève: ...\nSpinoza: ...\nÉlève: ...",
  "exchange_count": 2
}
```

**Réponse :**
```json
{
  "scores": {
    "comprehension": 7,
    "cooperation": 8,
    "progression": 6
  },
  "exchange_count": 2
}
```

### `POST /evaluate`

**Description :** Évalue le dialogue complet et génère le message final

**Requête :**
```json
{
  "dialogue": "Spinoza: ...\nÉlève: ...\n...",
  "score_front": 65
}
```

**Réponse :**
```json
{
  "score_final": 95,
  "message_final": "Ton effort pour comprendre tes propres affects est impressionnant...",
  "details_model": {
    "comprehension": 8,
    "cooperation": 9,
    "progression": 8,
    "total": 25
  }
}
```

---

## 🔄 Flux de Données

### Flux Dialogue Complet

```
1. INITIALISATION
   Frontend → GET /init
   Backend → {message, philosopher}
   Frontend → Affiche message + active formulaire

2. ÉCHANGE 1
   Utilisateur → Saisit question
   Frontend → Calcul score frontend (temps réel)
   Frontend → POST /chat {message, history: []}
   Backend → Inference modèle
   Backend → {response}
   Frontend → Affiche réponse + met à jour score

3. ÉCHANGE 2
   Utilisateur → Saisit réponse
   Frontend → Calcul score frontend
   Frontend → POST /chat {message, history: [échange1]}
   Backend → Inference modèle
   Backend → {response}
   Frontend → Affiche réponse
   Frontend → POST /evaluate/incremental (en arrière-plan)
   Backend → Évalue 2 derniers échanges
   Backend → Stocke scores incrémentaux

4. ÉCHANGES 3-4 (même pattern)

5. ÉCHANGE 5 (Dernier)
   Utilisateur → Saisit dernière réponse
   Frontend → Calcul score frontend final
   Frontend → POST /chat {message, history: [échanges1-4]}
   Backend → Inference modèle
   Backend → {response}
   Frontend → Affiche réponse
   Frontend → Affiche loader "Le jury délibère..."
   Frontend → POST /evaluate {dialogue, score_front}
   Backend → Agrège scores incrémentaux (si disponibles)
   Backend → Génère message final
   Backend → {score_final, message_final, details_model}
   Frontend → Affiche résultats (modal)
```

### Flux Score Frontend

```
Message utilisateur
    ↓
calculateScore(message, previousMessages)
    ↓
Calcul 5 critères :
  - Lexical
  - Longueur
  - Cohérence
  - Répétition
  - Fair-play
    ↓
Bonus citations (si détectées)
    ↓
scoreFront += delta
    ↓
Affichage en temps réel
```

### Flux Score Backend

```
Dialogue complet
    ↓
POST /evaluate {dialogue, score_front}
    ↓
Backend : PROMPT_EVALUATION.format(dialogue)
    ↓
Inference modèle (température 0.3)
    ↓
Parsing JSON {comprehension, cooperation, progression}
    ↓
total = comprehension + cooperation + progression
    ↓
PROMPT_MESSAGE_FINAL
    ↓
Inference modèle (température 1.1)
    ↓
message_final
    ↓
{score_final, message_final, details_model}
```

---

## 🧩 Composants Principaux

### Backend (Colab Notebook)

**Cellule 1-2 :** Installation dépendances  
**Cellule 3 :** Configuration secrets (ngrok, HuggingFace)  
**Cellule 4 :** Chargement modèle Mistral 7B + LoRA  
**Cellule 5 :** Configuration tokenizer  
**Cellule 6 :** Fonction inference  
**Cellule 7 :** Prompt système (`SYSTEM_PROMPT_SPINOZA`)  
**Cellule 8 :** Questions BAC (`QUESTIONS_BAC`)  
**Cellule 9-14 :** Endpoints FastAPI (`/health`, `/init`, `/chat`)  
**Cellule 15 :** Endpoint Maïeuthon (`/evaluate`)  
**Cellule 16 :** Endpoint évaluation incrémentale (`/evaluate/incremental`)  
**Cellule 17 :** Lancement serveur + ngrok

### Frontend (index_spinoza.html)

**Structure HTML :**
- Version desktop (`.desktop-version`)
- Version mobile (`.mobile-version`)
- Modal résultats (`#maieuthon-result-modal`)

**JavaScript principal :**
- `API_BASE_URL` : URL ngrok
- `scoreFront` : Score frontend (démarre à 50)
- `exchangeCount` : Compteur d'échanges (max 5)
- `dialogueHistory` : Historique complet

**Fonctions clés :**
- `submitQuestion()` : Envoie message, calcule score, affiche réponse
- `calculateScore()` : Calcule score frontend
- `handleIncrementalEvaluation()` : Appelle `/evaluate/incremental`
- `endGame()` : Appelle `/evaluate` et affiche résultats
- `startThinkingAnimation()` : Animation "thinking state"
- `detectCitationFromSpinozaReply()` : Détecte citations et ajoute bonus

### Fichiers de Configuration

**Backend/Cellule_9.py :**
- `SYSTEM_PROMPT_SPINOZA` : Prompt système principal
- `INSTRUCTIONS_CONTEXTUELLES` : Instructions selon contexte
- `construire_prompt_complet()` : Construction prompt final

**Backend/PROMPT_EVALUATION_FINAL.py :**
- `PROMPT_EVALUATION` : Prompt d'évaluation (3 critères)
- `PROMPT_MESSAGE_FINAL` : Prompt message final

**Backend/QUESTIONS_BAC_ETENDUES.py :**
- `QUESTIONS_BAC` : Liste des questions initiales (15 questions)

---

## 📊 Métriques et Performance

### Latence Typique

- **Inference dialogue** : 2-5 secondes
- **Évaluation incrémentale** : 3-6 secondes
- **Évaluation finale** : 5-10 secondes (optimisée : 3-6 secondes)

### Charge Modèle

**Système optimisé :**
- Échange 2 : `/evaluate/incremental` → 1 appel
- Échange 4 : `/evaluate/incremental` → 1 appel
- Échange 5 : `/evaluate` → 1 appel (message seulement)
- **Total : 3 appels modèle**

**Système non optimisé :**
- Échange 2 : `/evaluate/incremental` → 1 appel
- Échange 4 : `/evaluate/incremental` → 1 appel
- Échange 5 : `/evaluate` → 2 appels (scores + message)
- **Total : 4 appels modèle**

### Limites

- **Échanges maximum** : 5
- **Longueur historique** : ~2000 tokens (limite modèle)
- **Température dialogue** : 0.7 (cohérence)
- **Température évaluation** : 0.3 (précision)
- **Température message final** : 1.1 (créativité)

---

## 🔐 Sécurité et Configuration

### Secrets Colab

- `ngrok` : Token ngrok (tunnel public)
- `HuggingFaceToken` : Token Hugging Face (téléchargement modèle)
- `COLAB_GITHUB_TOKEN` : Token GitHub (clonage repo)

### Variables d'Environnement

Aucune variable d'environnement requise (tout dans Colab secrets)

### CORS

CORS activé pour toutes les origines (développement)

---

## 📚 Documentation Complémentaire

- **README.md** : Vue d'ensemble rapide
- **Backend/README.md** : Documentation backend
- **Backend/EXPLICATION_SCORE_MAIEUTHON.md** : Détails score Maïeuthon
- **docs/references/ARCHITECTURE_EVALUATION.md** : Architecture évaluation
- **docs/tutos/** : Guides pas à pas
- **docs/analyses/** : Analyses détaillées

---

**Dernière mise à jour :** Décembre 2024

