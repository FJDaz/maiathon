# 🔧 Adaptation du Parsing pour PROMPT_EVALUATION_STRUCTURE

Le prompt `PROMPT_EVALUATION_STRUCTURE.py` génère un format JSON détaillé différent du format actuel. Voici comment adapter le parsing.

## 📋 Format Actuel vs Format STRUCTURE

### Format actuel (attendu par le code)
```json
{
  "comprehension": X,
  "cooperation": Y,
  "progression": Z,
  "total": X+Y+Z
}
```

### Format STRUCTURE (généré par le nouveau prompt)
```json
{
  "analysis": {
    "signals": {
      "comprehension_positive": [...],
      "comprehension_negative": [...],
      "cooperation_positive": [...],
      "cooperation_negative": [...],
      "progression_signs": [...]
    },
    "interpretation": {
      "comprehension": "...",
      "cooperation": "...",
      "progression": "..."
    },
    "scores": {
      "comprehension": X,
      "cooperation": Y,
      "progression": Z
    }
  },
  "message_final": "..."
}
```

## 🔄 Modification du Code `evaluer_dialogue()`

Dans la cellule Maïeuthon (`RAG_Spinoza_secours.ipynb`), modifier la fonction `evaluer_dialogue()` :

### Code actuel (à modifier)
```python
# Extraire JSON de la réponse
json_match = re.search(r'\{[^}]+\}', response_eval, re.DOTALL)
if json_match:
    try:
        details_model = json.loads(json_match.group(0))
    except:
        details_model = {"comprehension": 5, "cooperation": 5, "progression": 5, "total": 15}
else:
    details_model = {"comprehension": 5, "cooperation": 5, "progression": 5, "total": 15}
```

### Code adapté (nouveau)
```python
# Extraire JSON de la réponse
json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_eval, re.DOTALL)
if json_match:
    try:
        result_json = json.loads(json_match.group(0))
        
        # Si format STRUCTURE (avec "analysis")
        if "analysis" in result_json and "scores" in result_json["analysis"]:
            scores = result_json["analysis"]["scores"]
            details_model = {
                "comprehension": scores.get("comprehension", 5),
                "cooperation": scores.get("cooperation", 5),
                "progression": scores.get("progression", 5)
            }
            details_model["total"] = sum([
                details_model["comprehension"],
                details_model["cooperation"],
                details_model["progression"]
            ])
            # Message final vient de result_json["message_final"]
            message_final_direct = result_json.get("message_final", "")
        # Si format ancien (direct)
        elif "comprehension" in result_json:
            details_model = result_json
            if "total" not in details_model:
                details_model["total"] = sum([
                    details_model.get("comprehension", 5),
                    details_model.get("cooperation", 5),
                    details_model.get("progression", 5)
                ])
            message_final_direct = None
        else:
            details_model = {"comprehension": 5, "cooperation": 5, "progression": 5, "total": 15}
            message_final_direct = None
    except Exception as e:
        print(f"⚠️ Erreur parsing JSON: {e}")
        details_model = {"comprehension": 5, "cooperation": 5, "progression": 5, "total": 15}
        message_final_direct = None
else:
    details_model = {"comprehension": 5, "cooperation": 5, "progression": 5, "total": 15}
    message_final_direct = None

# Score total
score_backend = details_model.get("total", 15)
score_final = score_front + score_backend

# 2. Message final
# Si message_final_direct existe (format STRUCTURE), l'utiliser directement
# Sinon, générer avec PROMPT_MESSAGE_FINAL comme avant
if message_final_direct:
    message_final = message_final_direct
else:
    # Génération classique avec PROMPT_MESSAGE_FINAL
    prompt_final = PROMPT_MESSAGE_FINAL
    # ... (reste du code de génération du message)
```

## ✅ Avantages du Format STRUCTURE

1. **Raisonnement explicite** : Le modèle doit lister les signaux avant de scorer
2. **Traçabilité** : On peut voir exactement quels signaux ont été détectés
3. **Debug facilité** : Les interprétations montrent le raisonnement du modèle
4. **Meilleure précision** : Le processus en 4 étapes force une analyse rigoureuse

## 🧪 Test

Après adaptation, tester avec :
```bash
python3 Spinoza_Secours_HF/ML/calibrate_evaluator.py <URL_API>
```

Vérifier que les scores sont bien extraits et que les erreurs de calibration diminuent.

