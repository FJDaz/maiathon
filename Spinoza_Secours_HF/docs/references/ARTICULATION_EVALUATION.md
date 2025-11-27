# 🔗 Articulation des Deux Systèmes d'Évaluation

## ❌ On ne merge PAS les deux endpoints

Les deux endpoints restent **séparés** mais **collaborent** :

1. **`/evaluate/incremental`** → Évalue au fil de l'eau (échanges 2, 4)
2. **`/evaluate`** → Évaluation finale qui **utilise** les résultats de l'incrémentale

---

## 📋 Architecture : Deux Endpoints Séparés

### Endpoint 1 : `/evaluate/incremental`
```python
@app.post("/evaluate/incremental")
def evaluate_incremental(req: EvaluateRequest):
    """
    Prompt : PROMPT_EVALUATION_INCREMENTAL (court, 2 derniers échanges)
    - Évalue rapidement les 2 derniers échanges
    - Stocke dans incremental_scores[dialogue_id]
    - Retourne seulement les scores (pas de message final)
    """
    details_model = evaluer_incremental(req.dialogue)
    
    # Stocker pour l'évaluation finale
    dialogue_id = hash(req.dialogue)
    incremental_scores[dialogue_id].append({"scores": details_model, ...})
    
    return {"scores": details_model, ...}
```

**Prompt utilisé** : `PROMPT_EVALUATION_INCREMENTAL` (court, 2 derniers échanges)

---

### Endpoint 2 : `/evaluate` (Optimisé)
```python
@app.post("/evaluate")
def evaluate_endpoint(req: EvaluateRequest):
    """
    Vérifie si scores incrémentaux existent :
    
    CAS 1 : Scores incrémentaux disponibles
    ├─ Agrège les scores (moyenne pondérée)
    ├─ Génère SEULEMENT le message final (PROMPT_MESSAGE_FINAL)
    └─ PAS besoin de PROMPT_EVALUATION (scores déjà calculés)
    
    CAS 2 : Pas de scores incrémentaux (fallback)
    ├─ Utilise PROMPT_EVALUATION (évaluation complète)
    ├─ Génère les scores
    └─ Génère le message final
    """
    dialogue_id = hash(req.dialogue)
    
    if dialogue_id in incremental_scores and len(incremental_scores[dialogue_id]) > 0:
        # CAS 1 : Utiliser scores incrémentaux
        scores_inc = incremental_scores[dialogue_id]
        details_model = agreger_scores(scores_inc)  # Pas d'appel modèle pour les scores
        message_final = generer_message_final()     # 1 seul appel modèle (PROMPT_MESSAGE_FINAL)
        
    else:
        # CAS 2 : Évaluation complète (fallback)
        result = evaluer_dialogue(req.dialogue, req.score_front)  # Utilise PROMPT_EVALUATION
        return result
```

---

## 🎯 Répartition des Prompts

### `/evaluate/incremental` utilise :
- **`PROMPT_EVALUATION_INCREMENTAL`** (court, 2 derniers échanges)
- Pas de message final

### `/evaluate` utilise (selon le cas) :

#### Si scores incrémentaux disponibles :
- ❌ **PAS** `PROMPT_EVALUATION` (scores déjà calculés)
- ✅ **SEULEMENT** `PROMPT_MESSAGE_FINAL` (génère le message)

#### Si pas de scores incrémentaux (fallback) :
- ✅ `PROMPT_EVALUATION` (évaluation complète)
- ✅ `PROMPT_MESSAGE_FINAL` (message final)

---

## 📊 Flux Détaillé

### Échange 2 : Évaluation Incrémentale
```
Frontend → POST /evaluate/incremental
  ↓
Backend :
  ├─ Utilise PROMPT_EVALUATION_INCREMENTAL
  ├─ Évalue les 2 derniers échanges
  ├─ Stocke dans incremental_scores[dialogue_id][0]
  └─ Retourne {scores: {...}}
```

### Échange 4 : Évaluation Incrémentale
```
Frontend → POST /evaluate/incremental
  ↓
Backend :
  ├─ Utilise PROMPT_EVALUATION_INCREMENTAL
  ├─ Évalue les 2 derniers échanges
  ├─ Stocke dans incremental_scores[dialogue_id][1]
  └─ Retourne {scores: {...}}
```

### Échange 5 : Évaluation Finale (Optimisée)
```
Frontend → POST /evaluate
  ↓
Backend :
  ├─ Vérifie incremental_scores[dialogue_id]
  ├─ Trouve 2 scores incrémentaux
  ├─ Agrège les scores (moyenne pondérée) → PAS d'appel modèle
  ├─ Génère message final (PROMPT_MESSAGE_FINAL) → 1 appel modèle
  └─ Retourne {score_final, message_final, details_model}
```

---

## 🔑 Points Clés

1. **Deux endpoints séparés** : `/evaluate/incremental` et `/evaluate`
2. **Deux prompts différents** :
   - `PROMPT_EVALUATION_INCREMENTAL` (court) → pour l'incrémentale
   - `PROMPT_EVALUATION` (complet) → pour l'évaluation finale (fallback seulement)
   - `PROMPT_MESSAGE_FINAL` → toujours utilisé pour le message final
3. **Stockage partagé** : `incremental_scores` est partagé entre les deux endpoints
4. **Optimisation** : `/evaluate` évite `PROMPT_EVALUATION` si scores incrémentaux disponibles

---

## ✅ Code à Copier dans Colab

Le code dans `ENDPOINT_EVALUATE_OPTIMISE.py` remplace l'endpoint `/evaluate` actuel.

**Important** : Les deux endpoints doivent partager la même variable `incremental_scores` (définie dans `CELLULE_EVALUATION_INCREMENTALE.py`).

