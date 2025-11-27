# 🔧 Backend - Spinoza Secours

**Dossier :** `Backend/`  
**Contenu :** Fichiers qui font tourner le serveur API

---

## 📁 Fichiers

### Notebooks et Extraits

**Dossier :** `Backend/Notebooks/`

Tous les notebooks Colab et extraits de cellules sont regroupés dans le dossier `Notebooks/` :

- **Notebooks Colab :**
  - `RAG_Spinoza_secours.ipynb` - Notebook Colab principal
  - `RAG_Spinoza_secours_23_11_25_STRUCTURE.ipynb` - Version structurée
  - `colab_spinoza_secours.ipynb` - Version alternative

- **Extraits de cellules :**
  - `CELLULE_EVALUATION_INCREMENTALE.py` - Évaluation incrémentale
  - `Cellule_9.py` - Cellule de référence
  - `PROMPT_EVALUATION_*.py` - Différentes versions de prompts d'évaluation
  - `FONCTION_EVALUER_DIALOGUE_ADAPTEE.py` - Fonction d'évaluation
  - `ENDPOINT_EVALUATE_OPTIMISE.py` - Endpoint optimisé
  - `QUESTIONS_BAC_ETENDUES.py` - Questions étendues

### Frontend

- **`index_spinoza.html`** - Interface utilisateur
  - Frontend HTML/JS vanilla
  - Appelle l'API backend via ngrok
  - Système de scoring Maïeuthon
  - Responsive (desktop + mobile)

### Tests

- **`test_evaluation_incremental.py`** - Tests unitaires de logique
  - Validation des modèles Pydantic
  - Structure des données
  - Parsing JSON avec regex
  - Extraction des échanges récents

- **`test_http_incremental.py`** - Test HTTP de l'endpoint
  - Teste l'endpoint `/evaluate/incremental` en conditions réelles
  - Usage: `python3 test_http_incremental.py <URL_NGROK>`
  - Vérifie la structure de la réponse

---

## 🚀 Architecture

```
Frontend (index_spinoza.html)
    ↓
Backend (RAG_Spinoza_secours.ipynb)
    ├── FastAPI serveur
    ├── Modèle Mistral 7B + LoRA
    ├── Tunnel ngrok
    └── Endpoints API
```

---

## 📝 Usage

1. **Ouvrir le notebook** dans Google Colab
2. **Configurer les secrets** :
   - `ngrok` : Token ngrok
   - `HuggingFaceToken` : Token Hugging Face
   - `COLAB_GITHUB_TOKEN` : Token GitHub
3. **Exécuter les cellules** dans l'ordre
4. **Récupérer l'URL ngrok** générée
5. **Mettre à jour** l'URL dans `index_spinoza.html`
6. **Ouvrir** `index_spinoza.html` dans un navigateur

---

## 🔗 Liens

- **Documentation :** `../docs/`
- **Guides Vast.ai :** `../docs/references/vast-ai/`
- **ML (Modèles) :** `../ML/`
- **Tutos :** `../docs/tutos/`

---

**Note :** La documentation détaillée a été déplacée dans `docs/` pour une meilleure organisation.

