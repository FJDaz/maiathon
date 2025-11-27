# 🔧 Fix 404 sur /evaluate - Ajouter l'Endpoint Manquant

## ❌ Problème

Le frontend appelle `/evaluate` mais cet endpoint n'existe pas dans votre notebook Colab, d'où le 404 :

```
nonremunerative-rory-unbreakably.ngrok-free.dev/evaluate:1  
Failed to load resource: the server responded with a status of 404 ()
```

## ✅ Solution : Ajouter l'Endpoint /evaluate

### Option 1 : Version Simple (Recommandée pour démarrer)

Ajoutez cette cellule dans votre notebook Colab **après la cellule API FastAPI** (cellule 7) et **avant le lancement serveur** (cellule 8) :

```python
# =============================================================================
# 🎮 ENDPOINT /evaluate - Évaluation Finale Maïeuthon
# =============================================================================

from pydantic import BaseModel

class EvaluateRequest(BaseModel):
    dialogue: str
    score_front: int

class EvaluateResponse(BaseModel):
    score_final: int
    message_final: str
    details_model: dict

# ⚠️ PROMPT_EVALUATION (à adapter selon vos besoins)
PROMPT_EVALUATION = """Tu évalues un dialogue entre Spinoza et un élève.

DIALOGUE :

{dialogue}

GRILLE D'ÉVALUATION (0-10 pour chaque critère) :

1️⃣ COMPRÉHENSION :
   • 9-10 : Reformule correctement les idées, pose des questions pertinentes, fait des liens
   • 6-8 : Comprend mais demande des clarifications, fait quelques erreurs
   • 3-5 : Comprend partiellement, confusions fréquentes
   • 0-2 : Ne comprend pas, dit "je comprends pas", refuse le dialogue

2️⃣ COOPÉRATION :
   • 9-10 : Répond aux questions, fait avancer le dialogue, s'engage activement
   • 6-8 : Coopère mais avec quelques résistances
   • 3-5 : Résiste souvent, dialogue difficile
   • 0-2 : Refuse de coopérer, dit "j'ai autre chose à faire", part

3️⃣ PROGRESSION :
   • 9-10 : Pensée évolue clairement, conclusions à la fin
   • 6-8 : Progresse lentement, quelques retours en arrière
   • 3-5 : Peu de progression, tourne en rond
   • 0-2 : Aucune évolution, répète les mêmes incompréhensions

Réponds UNIQUEMENT avec ce JSON (aucun texte avant/après) :

{{
 "comprehension": X,
 "cooperation": Y,
 "progression": Z,
 "total": X+Y+Z
}}"""

# ⚠️ PROMPT_MESSAGE_FINAL (message de fin bienveillant)
PROMPT_MESSAGE_FINAL = """Tu es Spinoza. Tu viens de terminer un dialogue avec un élève.

Écris un message final court (2-3 phrases max) qui :
- Valide les efforts de l'élève
- Encourage sa progression
- Reste chaleureux et motivant
- Ne soit jamais académique ou formel

Message :"""

def evaluer_dialogue(dialogue: str, score_front: int) -> dict:
    """
    Évalue le dialogue complet et génère le message final
    """
    import json
    import re
    
    # 1. Évaluation (température basse pour JSON strict)
    prompt_eval = PROMPT_EVALUATION.format(dialogue=dialogue)
    prompt_eval_formatted = f"<s>[INST] {prompt_eval} [/INST]"
    
    inputs = tokenizer(prompt_eval_formatted, return_tensors="pt").to(model.device)
    input_length = inputs['input_ids'].shape[1]
    
    device_type = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16 if device_type == "cuda" else torch.float32
    
    with torch.autocast(device_type=device_type, dtype=dtype):
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.1,  # Basse température pour JSON strict
            top_p=0.9,
            do_sample=True,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
    
    new_tokens = outputs[0][input_length:]
    reponse_eval = tokenizer.decode(new_tokens, skip_special_tokens=True)
    
    # Parser JSON
    details_model = None
    json_pattern = r'\{[^{}]*"comprehension"[^{}]*"cooperation"[^{}]*"progression"[^{}]*"total"[^{}]*\}'
    json_match = re.search(json_pattern, reponse_eval, re.DOTALL)
    
    if json_match:
        try:
            json_str = json_match.group(0).strip()
            details_model = json.loads(json_str)
        except json.JSONDecodeError:
            pass
    
    # Valeurs par défaut si parsing échoue
    if not details_model or not isinstance(details_model, dict):
        details_model = {"comprehension": 5, "cooperation": 5, "progression": 5, "total": 15}
    
    # 2. Message final (température plus haute pour créativité)
    prompt_final = PROMPT_MESSAGE_FINAL
    prompt_final_formatted = f"<s>[INST] {prompt_final} [/INST]"
    
    inputs_final = tokenizer(prompt_final_formatted, return_tensors="pt").to(model.device)
    input_length_final = inputs_final['input_ids'].shape[1]
    
    with torch.autocast(device_type=device_type, dtype=dtype):
        outputs_final = model.generate(
            **inputs_final,
            max_new_tokens=150,
            temperature=1.1,  # Haute température pour créativité
            top_p=0.95,
            do_sample=True,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
    
    new_tokens_final = outputs_final[0][input_length_final:]
    message_final = tokenizer.decode(new_tokens_final, skip_special_tokens=True).strip()
    
    # Nettoyer le message
    if message_final.startswith('"') and message_final.endswith('"'):
        message_final = message_final[1:-1]
    
    # Score total
    score_backend = details_model.get("total", 15)
    score_final = score_front + score_backend
    
    return {
        "score_final": score_final,
        "message_final": message_final,
        "details_model": details_model
    }

# Endpoint FastAPI
@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest):
    """
    Évalue le dialogue complet et génère le message final
    """
    result = evaluer_dialogue(req.dialogue, req.score_front)
    return EvaluateResponse(**result)

print("✅ Endpoint /evaluate créé pour Maïeuthon")
```

### Option 2 : Version Optimisée (Utilise les scores incrémentaux)

Si vous avez déjà ajouté l'évaluation incrémentale (`/evaluate/incremental`), utilisez plutôt le fichier `ENDPOINT_EVALUATE_OPTIMISE.py` qui agrège les scores incrémentaux.

## 📍 Où Placer dans Colab

1. **Ouvrez** votre notebook Colab
2. **Trouvez** la cellule 7 (API FastAPI) qui contient `@app.post("/chat")`
3. **Créez une nouvelle cellule** juste après
4. **Collez** le code ci-dessus
5. **Exécutez** la cellule
6. **Vérifiez** que vous voyez : `✅ Endpoint /evaluate créé pour Maïeuthon`

## ✅ Vérification

Après avoir ajouté l'endpoint, testez dans la console du navigateur :

```javascript
// Tester l'endpoint
fetch('https://votre-url-ngrok.ngrok-free.dev/evaluate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'ngrok-skip-browser-warning': 'true'
  },
  body: JSON.stringify({
    dialogue: "Test dialogue",
    score_front: 100
  })
})
.then(r => r.json())
.then(console.log)
```

Vous devriez recevoir une réponse avec `score_final`, `message_final` et `details_model`.

## 🔍 Si ça ne fonctionne toujours pas

1. **Vérifiez** que la cellule a bien été exécutée (pas d'erreur)
2. **Vérifiez** dans les logs Colab que l'endpoint est bien créé
3. **Redémarrez** le serveur (relancez la cellule de lancement serveur)
4. **Vérifiez** que l'URL ngrok est correcte dans le frontend

