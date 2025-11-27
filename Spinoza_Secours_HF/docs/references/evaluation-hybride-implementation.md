# 🔧 Implémentation : Évaluation Hybride (Fil de l'Eau + Finale)

**Date :** 21 novembre 2025  
**Objectif :** Optimiser l'inférence en distribuant l'évaluation sur le dialogue

---

## 🎯 Architecture Hybride

### Principe

1. **Évaluation incrémentale** (tous les 2 échanges) : Score rapide invisible
2. **Évaluation finale** (échange 5) : Utilise les scores incrémentaux + message final

---

## 📋 Implémentation Backend

### 1. Nouveau Endpoint : `/evaluate/incremental`

**Ajouter dans `RAG_Spinoza_secours.ipynb` :**

```python
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
incremental_scores = {}  # {dialogue_id: [scores_échange_2, scores_échange_4, ...]}

@app.post("/evaluate/incremental")
def evaluate_incremental(req: EvaluateRequest):
    """
    Évaluation légère au fil de l'eau (tous les 2 échanges)
    - Prompt court
    - Température basse (0.1)
    - Max tokens réduit (50)
    - Pas de message final
    """
    # Extraire les 2 derniers échanges seulement
    lines = req.dialogue.split('\n')
    recent_exchanges = '\n'.join(lines[-4:]) if len(lines) > 4 else req.dialogue
    
    prompt_eval = PROMPT_EVALUATION_INCREMENTAL.format(dialogue_recent=recent_exchanges)
    prompt_eval_formatted = f"<s>[INST] {prompt_eval} [/INST]"
    
    inputs = tokenizer(prompt_eval_formatted, return_tensors="pt").to(model.device)
    input_length = inputs['input_ids'].shape[1]
    
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
    
    # Parser JSON
    json_match = re.search(r'\{[^{}]*"comprehension"[^{}]*"cooperation"[^{}]*"progression"[^{}]*"total"[^{}]*\}', reponse_eval)
    if json_match:
        try:
            details_model = json.loads(json_match.group(0))
        except:
            details_model = {"comprehension": 5, "cooperation": 5, "progression": 5, "total": 15}
    else:
        details_model = {"comprehension": 5, "cooperation": 5, "progression": 5, "total": 15}
    
    # Stocker pour l'évaluation finale
    dialogue_id = hash(req.dialogue)  # Simplifié, utiliser un vrai ID en production
    if dialogue_id not in incremental_scores:
        incremental_scores[dialogue_id] = []
    incremental_scores[dialogue_id].append(details_model)
    
    return {
        "scores": details_model,
        "exchange_count": len(incremental_scores[dialogue_id])
    }

# Modifier l'évaluation finale pour utiliser les scores incrémentaux
def evaluer_dialogue(dialogue: str, score_front: int) -> dict:
    """
    Évaluation finale optimisée (utilise scores incrémentaux si disponibles)
    """
    dialogue_id = hash(dialogue)
    
    # Si scores incrémentaux disponibles, les utiliser
    if dialogue_id in incremental_scores and len(incremental_scores[dialogue_id]) > 0:
        scores_inc = incremental_scores[dialogue_id]
        
        # Agréger les scores incrémentaux (moyenne pondérée par ordre)
        n = len(scores_inc)
        weights = [i+1 for i in range(n)]  # Poids croissant (dernier échange plus important)
        total_weight = sum(weights)
        
        details_model = {
            "comprehension": sum(s["comprehension"] * w for s, w in zip(scores_inc, weights)) / total_weight,
            "cooperation": sum(s["cooperation"] * w for s, w in zip(scores_inc, weights)) / total_weight,
            "progression": sum(s["progression"] * w for s, w in zip(scores_inc, weights)) / total_weight,
        }
        details_model["comprehension"] = int(round(details_model["comprehension"]))
        details_model["cooperation"] = int(round(details_model["cooperation"]))
        details_model["progression"] = int(round(details_model["progression"]))
        details_model["total"] = details_model["comprehension"] + details_model["cooperation"] + details_model["progression"]
        
        # Score total
        score_backend = details_model.get("total", 15)
        score_final = score_front + score_backend
        
        # Message final uniquement (pas besoin de réévaluer)
        prompt_final = PROMPT_MESSAGE_FINAL
        # ... génération message final ...
        
        return {
            "score_final": score_final,
            "message_final": message_final,
            "details_model": details_model,
            "used_incremental": True  # Flag pour debug
        }
    
    # Sinon, évaluation classique (fallback)
    # ... code existant ...
```

---

## 📋 Implémentation Frontend

### Modifier `index_spinoza.html`

```javascript
// Stockage scores incrémentaux
let incrementalScores = [];

// Après chaque 2 échanges, appeler l'évaluation incrémentale
async function handleIncrementalEvaluation() {
  if (exchangeCount % 2 === 0 && exchangeCount < MAX_EXCHANGES) {
    try {
      const response = await fetch(`${API_BASE_URL}/evaluate/incremental`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'ngrok-skip-browser-warning': 'true'
        },
        body: JSON.stringify({
          dialogue: dialogueText,
          score_front: scoreFront
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        incrementalScores.push(data.scores);
        console.log('[MAÏEUTHON] Score incrémental:', data.scores);
        // NE PAS AFFICHER à l'utilisateur (invisible)
      }
    } catch (error) {
      console.warn('[MAÏEUTHON] Erreur évaluation incrémentale:', error);
      // Continuer le dialogue même si échec
    }
  }
}

// Modifier la fonction d'envoi de message
async function sendMessage(userMessage) {
  // ... code existant ...
  
  // Après réception de la réponse
  updateDialogueText(userMessage, data.reply);
  
  // Évaluation incrémentale (tous les 2 échanges)
  await handleIncrementalEvaluation();
  
  // Fin du jeu si max atteint
  if (exchangeCount >= MAX_EXCHANGES) {
    setTimeout(() => endGame(), 1000);
  }
}
```

---

## ⚖️ Arbitrage Qualité vs Performance

### Impact sur la Qualité du Dialogue

#### ✅ **Aucun impact si invisible**

- Évaluation incrémentale **cachée** à l'élève
- Pas de feedback visuel pendant le dialogue
- Le dialogue reste naturel et spontané
- Pas de changement de comportement

#### ❌ **Impact si visible**

- Si l'élève voit ses scores → changement de comportement
- Perte de spontanéité
- Sur-adaptation ou résistance

**Recommandation :** **Toujours invisible** pendant le dialogue.

---

### Impact sur la Performance

#### ✅ **Charge distribuée**

- Évaluation tous les 2 échanges au lieu d'un pic en fin
- Prompt court (dialogue récent seulement)
- Max tokens réduit (50 au lieu de 100-150)
- Pas de message final (gain de temps)

#### ⚠️ **Latence ajoutée**

- 2-3 appels API supplémentaires pendant le dialogue
- ~1-2 secondes de latence par évaluation incrémentale
- Impact acceptable si inférence rapide (< 1s)

**Recommandation :** Optimiser pour inférence < 1s (prompt court, tokens réduits).

---

### Impact sur la Qualité d'Évaluation

#### ✅ **Meilleure détection**

- Détection précoce de problèmes (résistance, incompréhension)
- Suivi de la progression en temps réel
- Scores agrégés plus précis (moyenne pondérée)

#### ✅ **Évaluation finale optimisée**

- Utilise les scores incrémentaux comme base
- Réduit la charge en fin (pas besoin de réévaluer tout)
- Message final uniquement si besoin

**Recommandation :** Valider la cohérence des scores incrémentaux vs finale.

---

## 📊 Comparaison Avant/Après

| Critère | Avant (Finale uniquement) | Après (Hybride) |
|---------|---------------------------|-----------------|
| **Charge en fin** | ❌ Pic élevé | ✅ Distribuée |
| **Fatigue modèle** | ❌ Élevée | ✅ Réduite |
| **Qualité dialogue** | ✅ Naturel | ✅ Naturel (invisible) |
| **Détection précoce** | ❌ Non | ✅ Oui |
| **Latence totale** | ✅ ~2s (fin) | ⚠️ ~5s (distribuée) |
| **Coût GPU** | ✅ 1 évaluation | ⚠️ 3 évaluations |
| **Qualité évaluation** | ⚠️ Vue d'ensemble | ✅ Détails + vue d'ensemble |

---

## 🎯 Recommandation Finale

### ⭐ **Implémenter l'évaluation hybride avec optimisations**

**Avantages :**
- ✅ Charge distribuée (pas de pic en fin)
- ✅ Détection précoce de problèmes
- ✅ Dialogue naturel préservé (invisible)
- ✅ Évaluation finale de qualité (scores pré-calculés)
- ✅ Réduction de la fatigue du modèle

**Risques mitigés :**
- ⚠️ Latence → Optimiser pour < 1s par évaluation incrémentale
- ⚠️ Coût → Évaluations incrémentales légères (prompt court, tokens réduits)
- ⚠️ Complexité → Code bien structuré, documentation claire

**Plan d'action :**
1. Implémenter `/evaluate/incremental` (Phase 1)
2. Modifier le frontend pour appeler tous les 2 échanges (invisible)
3. Optimiser l'évaluation finale pour utiliser les scores incrémentaux
4. Tester et calibrer
5. Mesurer les gains (charge, qualité, latence)

---

**Document créé le :** 21 novembre 2025

