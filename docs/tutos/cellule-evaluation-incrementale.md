# 🎮 Cellule Colab : Évaluation Incrémentale (Fil de l'Eau)

**À ajouter APRÈS la cellule `/evaluate` (Maïeuthon) et AVANT la cellule de Lancement Serveur**

---

## 📝 Code de la Cellule

**⚠️ Fichier de référence :** `Backend/CELLULE_EVALUATION_INCREMENTALE.py` (code brut prêt à copier)

**Code à copier dans Colab :**

```python
# =============================================================================
# ⚡ ÉVALUATION INCRÉMENTALE - Fil de l'Eau (Optimisation Inférence)
# =============================================================================

# Prompt évaluation incrémentale (court, rapide)
PROMPT_EVALUATION_INCREMENTAL = """Évalue rapidement (0-10) :
- Compréhension : Comprend-il mes idées ?
- Coopération : Coopère-t-il dans le dialogue ?
- Progression : Sa pensée progresse-t-elle ?

Dialogue récent (2 derniers échanges) :
{dialogue_recent}

JSON strict (aucune prose) :
{{
 "comprehension": X,
 "cooperation": Y,
 "progression": Z,
 "total": X+Y+Z
}}"""

# Stockage scores incrémentaux (en mémoire)
# Structure : {dialogue_id: [scores_échange_2, scores_échange_4, ...]}
incremental_scores = {}

def evaluer_incremental(dialogue: str) -> dict:
    """
    Évaluation légère au fil de l'eau (tous les 2 échanges)
    - Prompt court (2 derniers échanges seulement)
    - Température basse (0.1) - Strict pour JSON
    - Max tokens réduit (50) - Rapidité
    - Pas de message final - Gain de temps
    """
    # Extraire les 2 derniers échanges seulement (4 lignes : Élève + Spinoza x2)
    lines = [l.strip() for l in dialogue.split('\n') if l.strip()]
    if len(lines) > 4:
        recent_exchanges = '\n'.join(lines[-4:])  # 2 derniers échanges
    else:
        recent_exchanges = dialogue
    
    prompt_eval = PROMPT_EVALUATION_INCREMENTAL.format(dialogue_recent=recent_exchanges)
    
    # Formatage Mistral
    prompt_eval_formatted = f"<s>[INST] {prompt_eval} [/INST]"
    
    inputs = tokenizer(prompt_eval_formatted, return_tensors="pt").to(model.device)
    input_length = inputs['input_ids'].shape[1]
    
    device_type = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16 if device_type == "cuda" else torch.float32
    
    # Inférence rapide (température basse, tokens réduits)
    with torch.autocast(device_type=device_type, dtype=dtype):
        outputs = model.generate(
            **inputs,
            max_new_tokens=50,  # Court pour rapidité
            temperature=0.1,    # Strict pour JSON
            top_p=0.9,
            do_sample=True,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
    
    new_tokens = outputs[0][input_length:]
    reponse_eval = tokenizer.decode(new_tokens, skip_special_tokens=True)
    
    # Parser JSON (amélioré pour capturer même avec texte autour)
    json_pattern = r'\{[^{}]*"comprehension"[^{}]*"cooperation"[^{}]*"progression"[^{}]*"total"[^{}]*\}'
    json_match = re.search(json_pattern, reponse_eval, re.DOTALL)
    
    if json_match:
        try:
            details_model = json.loads(json_match.group(0))
            # Valider que tous les champs sont présents
            required_fields = ["comprehension", "cooperation", "progression", "total"]
            for field in required_fields:
                if field not in details_model:
                    details_model[field] = 5 if field != "total" else 15
        except json.JSONDecodeError as e:
            print(f"⚠️ Erreur parsing JSON incrémental: {e}")
            print(f"   Réponse brute: {reponse_eval[:200]}")
            details_model = {"comprehension": 5, "cooperation": 5, "progression": 5, "total": 15}
    else:
        print(f"⚠️ JSON non trouvé dans réponse incrémentale: {reponse_eval[:200]}")
        details_model = {"comprehension": 5, "cooperation": 5, "progression": 5, "total": 15}
    
    return details_model

# Endpoint FastAPI pour évaluation incrémentale
@app.post("/evaluate/incremental")
def evaluate_incremental(req: EvaluateRequest):
    """
    Évaluation légère au fil de l'eau (tous les 2 échanges)
    - Appelé par le frontend après chaque 2 échanges
    - Stocke les scores pour l'évaluation finale
    - Retourne seulement les scores (pas de message final)
    """
    # Évaluer le dialogue récent
    details_model = evaluer_incremental(req.dialogue)
    
    # Stocker pour l'évaluation finale
    # Utiliser un ID simple basé sur le hash du dialogue
    # En production, utiliser un vrai ID de session
    dialogue_id = hash(req.dialogue)
    
    if dialogue_id not in incremental_scores:
        incremental_scores[dialogue_id] = []
    
    incremental_scores[dialogue_id].append({
        "scores": details_model,
        "exchange_count": len(incremental_scores[dialogue_id]) + 1
    })
    
    return {
        "scores": details_model,
        "exchange_count": len(incremental_scores[dialogue_id]),
        "accumulated": len(incremental_scores[dialogue_id]) > 0
    }

print("✅ Endpoint /evaluate/incremental créé pour évaluation au fil de l'eau")
```

---

## 🔧 Modification de l'Évaluation Finale

**Modifier la fonction `evaluer_dialogue()` existante** pour utiliser les scores incrémentaux :

```python
def evaluer_dialogue(dialogue: str, score_front: int) -> dict:
    """
    Évalue le dialogue et génère le message final.
    Utilise les scores incrémentaux si disponibles pour optimiser.
    """
    dialogue_id = hash(dialogue)
    
    # Si scores incrémentaux disponibles, les utiliser comme base
    if dialogue_id in incremental_scores and len(incremental_scores[dialogue_id]) > 0:
        scores_inc = incremental_scores[dialogue_id]
        
        # Agréger les scores incrémentaux (moyenne pondérée par ordre)
        # Le dernier échange est plus important (poids croissant)
        n = len(scores_inc)
        weights = [i+1 for i in range(n)]  # [1, 2, 3, ...]
        total_weight = sum(weights)
        
        # Calculer moyenne pondérée
        details_model = {
            "comprehension": int(round(
                sum(s["scores"]["comprehension"] * w for s, w in zip(scores_inc, weights)) / total_weight
            )),
            "cooperation": int(round(
                sum(s["scores"]["cooperation"] * w for s, w in zip(scores_inc, weights)) / total_weight
            )),
            "progression": int(round(
                sum(s["scores"]["progression"] * w for s, w in zip(scores_inc, weights)) / total_weight
            ))
        }
        details_model["total"] = details_model["comprehension"] + details_model["cooperation"] + details_model["progression"]
        
        print(f"📊 Scores incrémentaux utilisés: {len(scores_inc)} évaluations")
        
        # Score total
        score_backend = details_model.get("total", 15)
        score_final = score_front + score_backend
        
        # Message final uniquement (scores déjà calculés)
        # ... (code génération message final existant) ...
        
        return {
            "score_final": score_final,
            "message_final": message_final,
            "details_model": details_model,
            "used_incremental": True  # Flag pour debug
        }
    
    # Sinon, évaluation classique (fallback si pas de scores incrémentaux)
    # ... (code existant d'évaluation complète) ...
```

---

## 📋 Instructions d'Ajout dans Colab

### Étape 1 : Ajouter la Cellule d'Évaluation Incrémentale

1. **Ouvrir** le notebook `RAG_Spinoza_secours.ipynb` dans Colab
2. **Trouver** la cellule avec `/evaluate` (après la cellule 7)
3. **Insérer une nouvelle cellule** juste après cette cellule
4. **Copier-coller** le code de l'évaluation incrémentale
5. **Exécuter** la cellule

### Étape 2 : Modifier l'Évaluation Finale

1. **Modifier** la fonction `evaluer_dialogue()` existante
2. **Ajouter** la logique pour utiliser les scores incrémentaux
3. **Tester** avec un dialogue complet

---

## ✅ Vérification

Après ajout, tester avec :

```bash
# Test évaluation incrémentale
curl -X POST https://ton-url-ngrok.ngrok-free.dev/evaluate/incremental \
  -H "Content-Type: application/json" \
  -d '{"dialogue": "Élève: Bonjour\nSpinoza: Salut\nÉlève: Qu'est-ce que la liberté ?", "score_front": 100}'
```

**Résultat attendu :**
```json
{
  "scores": {
    "comprehension": 7,
    "cooperation": 8,
    "progression": 6,
    "total": 21
  },
  "exchange_count": 1,
  "accumulated": true
}
```

---

## 🎯 Bénéfices

1. ✅ **Charge distribuée** : Pas de pic en fin de dialogue
2. ✅ **Moins de fatigue** : Évaluation de segments courts
3. ✅ **Détection précoce** : Problèmes identifiés tôt
4. ✅ **Évaluation finale optimisée** : Utilise les scores pré-calculés

---

**Note :** L'évaluation incrémentale est **invisible** à l'utilisateur (pas de feedback visuel pendant le dialogue) pour préserver la qualité du dialogue.

---

**Document créé le :** 21 novembre 2025

