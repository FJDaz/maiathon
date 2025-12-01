# 📍 Où Placer le Code dans Colab - Guide Visuel

## 🎯 Réponse Rapide

**Remplacez SEULEMENT l'endpoint FastAPI** `@app.post("/evaluate")`, **PAS** la fonction `evaluer_dialogue()`.

---

## 📋 Structure dans votre Colab (Cellule Maïeuthon)

### ✅ Ce qui RESTE (ne pas toucher)

```python
# Fonction evaluer_dialogue() - GARDEZ-LA !
def evaluer_dialogue(dialogue: str, score_front: int) -> dict:
    """
    Évalue le dialogue et génère le message final
    Gère les formats JSON ancien et STRUCTURE
    """
    # 1. Évaluation (température basse, JSON strict)
    prompt_eval = PROMPT_EVALUATION.format(dialogue=dialogue)
    # ... tout le code d'évaluation ...
    
    return {
        "score_final": score_final,
        "message_final": message_final,
        "details_model": details_model
    }
```

**Cette fonction est utilisée en fallback (ligne 99 de ENDPOINT_EVALUATE_OPTIMISE.py)**

---

### ❌ Ce qui est REMPLACÉ

**Ancien endpoint (à SUPPRIMER) :**
```python
# ❌ SUPPRIMEZ CETTE PARTIE
@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest):
    """
    Évalue le dialogue complet et génère le message final
    """
    result = evaluer_dialogue(req.dialogue, req.score_front)
    return EvaluateResponse(**result)

print("✅ Endpoint /evaluate créé pour Maïeuthon")
```

---

### ✅ Nouveau endpoint (à COLLER)

**Remplacez par le code de `ENDPOINT_EVALUATE_OPTIMISE.py` :**
```python
# ✅ COLLEZ CETTE PARTIE (remplace l'ancien endpoint)
@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate_endpoint(req: EvaluateRequest):
    """
    Évaluation finale optimisée :
    - Si scores incrémentaux disponibles → les agrège + génère seulement le message final
    - Sinon → évaluation complète normale (fallback)
    """
    dialogue_id = hash(req.dialogue)
    
    # Vérifier si scores incrémentaux disponibles
    if dialogue_id in incremental_scores and len(incremental_scores[dialogue_id]) > 0:
        # ... code d'agrégation des scores ...
        # ... génération message final ...
        return EvaluateResponse(...)
    
    else:
        # Fallback : utilise evaluer_dialogue() (votre fonction existante)
        return evaluer_dialogue(req.dialogue, req.score_front)

print("✅ Endpoint /evaluate optimisé (utilise scores incrémentaux si disponibles)")
```

---

## 🔍 Comment Trouver dans Colab

### Étape 1 : Trouver la cellule Maïeuthon
Cherchez dans votre notebook :
- `def evaluer_dialogue(...)`
- `@app.post("/evaluate", ...)`

### Étape 2 : Identifier la partie à remplacer
Vous devriez voir quelque chose comme :
```python
# Fonction evaluer_dialogue() - GARDEZ
def evaluer_dialogue(...):
    ...

# Endpoint FastAPI - REMPLACEZ SEULEMENT CETTE PARTIE
@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest):
    result = evaluer_dialogue(req.dialogue, req.score_front)
    return EvaluateResponse(**result)
```

### Étape 3 : Remplacer
1. **Supprimez** les lignes de l'endpoint `@app.post("/evaluate")` (l'ancien)
2. **Collez** le code de `ENDPOINT_EVALUATE_OPTIMISE.py`
3. **Gardez** la fonction `evaluer_dialogue()` intacte

---

## 📊 Schéma Visuel

```
┌─────────────────────────────────────────────────┐
│  CELLULE MAÏEUTHON (dans Colab)                 │
├─────────────────────────────────────────────────┤
│                                                  │
│  ✅ GARDEZ :                                     │
│  def evaluer_dialogue(...):                     │
│      # Votre prompt système PROMPT_EVALUATION   │
│      # ... tout le code ...                      │
│      return {...}                                │
│                                                  │
│  ❌ SUPPRIMEZ :                                  │
│  @app.post("/evaluate")                          │
│  def evaluate(req):                             │
│      return evaluer_dialogue(...)                │
│                                                  │
│  ✅ COLLEZ (remplace l'ancien endpoint) :        │
│  @app.post("/evaluate")                         │
│  def evaluate_endpoint(req):                    │
│      if scores_inc existent:                    │
│          # Agrège + message                      │
│      else:                                       │
│          return evaluer_dialogue(...)  ← FALLBACK│
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## ✅ Checklist

- [ ] J'ai trouvé la cellule Maïeuthon dans Colab
- [ ] J'ai identifié la fonction `evaluer_dialogue()` (à garder)
- [ ] J'ai identifié l'endpoint `@app.post("/evaluate")` (à remplacer)
- [ ] J'ai supprimé l'ancien endpoint
- [ ] J'ai collé le code de `ENDPOINT_EVALUATE_OPTIMISE.py`
- [ ] La fonction `evaluer_dialogue()` est toujours présente (fallback)

---

## 🚨 Points d'Attention

1. **Ne supprimez PAS** `evaluer_dialogue()` - elle est utilisée en fallback
2. **Remplacez SEULEMENT** l'endpoint FastAPI `@app.post("/evaluate")`
3. **L'ordre** : D'abord `CELLULE_EVALUATION_INCREMENTALE.py`, puis `ENDPOINT_EVALUATE_OPTIMISE.py`

---

## 📝 Résumé

**Action** : Remplacer l'endpoint FastAPI, pas la fonction d'évaluation.

**Où** : Dans la cellule Maïeuthon, après la fonction `evaluer_dialogue()`.

**Quoi** : Le code de `ENDPOINT_EVALUATE_OPTIMISE.py` remplace l'ancien `@app.post("/evaluate")`.

