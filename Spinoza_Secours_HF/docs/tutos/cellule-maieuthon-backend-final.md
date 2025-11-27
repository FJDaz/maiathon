# 🎮 Cellule Colab : Backend Maïeuthon - Version FINAL

**Version avec `PROMPT_EVALUATION_FINAL` qui génère un format JSON simple (version qui fonctionnait mieux)**

**À ajouter APRÈS la cellule 7 (API FastAPI) et AVANT la cellule 8 (Lancement Serveur)**

---

## 📝 Code de la cellule (VERSION FINAL - Format JSON simple)

```python
# =============================================================================
# 🎮 MAÏEUTHON - Backend : Évaluation et Message Final (VERSION FINAL)
# =============================================================================

from pydantic import BaseModel
import json
import re
import torch

class EvaluateRequest(BaseModel):
    dialogue: str
    score_front: int

class EvaluateResponse(BaseModel):
    score_final: int
    message_final: str
    details_model: dict

# ⚠️ PROMPT_EVALUATION FINAL (version structurée avec format JSON simple)
PROMPT_EVALUATION = """Tu es Spinoza. Voici l'échange complet avec un élève :

{dialogue}

Évalue l'élève sur 3 critères (0 à 10). Tu dois utiliser TOUTE l'échelle, surtout les extrêmes.  

Ne donne PAS de notes "moyennes" si le comportement est clairement bon ou mauvais.

RÈGLE STRUCTURELLE :  
→ Lis tout le dialogue. Déduis un niveau GLOBAL cohérent.  
→ Puis applique les définitions ci-dessous.  
→ Si un cas se situe entre deux niveaux, choisis TOUJOURS le niveau le plus BAS.

============================================================
1. COMPRÉHENSION (0 à 10)
============================================================

RÈGLES FORTES :
- Si l'élève ne montre AUCUNE reformulation correcte → note ≤ 4.  
- Si l'élève produit AU MOINS une reformulation correcte → note ≥ 6.  
- Si l'élève produit une reformulation précise et juste → note ≥ 8.

GRILLE :
0-2 : Aucune compréhension, rejette ou ignore les explications, abandon ou sarcasme.  
3-4 : Compréhension très faible, répète sans comprendre, reste confus, abandonne parfois.  
5-6 : Compréhension partielle MAIS présence de questions pour comprendre + effort continu.  
7-8 : Bonne compréhension, plusieurs liens pertinents, reformulations mostly correctes.  
9-10 : Très bonne compréhension, reformulations précises, synthèse correcte.

============================================================
2. COOPÉRATION (0 à 10)
============================================================

RÈGLES FORTES :
- Si l'élève dit "ciao", "j'ai autre chose à faire", "j'en ai rien à faire", "je m'en fous", ou abandonne explicitement → note ≤ 1.  
- Si l'élève abandonne, rejette le dialogue ou fuit → note ≤ 2.  
- Si l'élève répond systématiquement par des phrases courtes OUI/NON → note ≤ 4.  
- Si l'élève pose AU MOINS une vraie question → note ≥ 6.  
- Si l'élève pose plusieurs questions ou construit le dialogue → note ≥ 8.

GRILLE :
0-1 : Abandon explicite ("ciao", "j'ai autre chose à faire"), refus total, fuite immédiate.  
2-3 : Refus, hostilité, sarcasme, fuite du dialogue.  
3-4 : Résistance forte, réponses minimalistes, effort très faible.  
5-6 : Participation minimale mais continue, résistance ponctuelle MAIS pose des questions.  
7-8 : Bonne coopération, échange actif, écoute réelle.  
9-10 : Très grande coopération, engagement constant et volontaire.

============================================================
3. PROGRESSION (0 à 10)
============================================================

RÈGLES FORTES :
- Si l'élève ne s'améliore PAS du tout ou reste bloqué → note ≤ 2.  
- Si l'élève résiste mais NE progresse PAS ("je ne suis toujours pas convaincu" sans changement) → note 3-4.  
- Si l'élève fait un progrès léger (un lien, une idée nouvelle) → 4-5.  
- Si l'élève améliore sa compréhension dans le dialogue (comprend de mieux en mieux) → ≥ 6.  
- Si l'élève termine avec une compréhension nettement meilleure qu'au début → ≥ 8.

GRILLE :
0-1 : Aucun progrès, blocage constant, abandon.  
2-3 : Progression quasi nulle, reste bloqué sur la même incompréhension ("je ne suis toujours pas convaincu" répété).  
3-4 : Résistance + blocage, un seul lien faible sans amélioration.  
4-5 : Progression minimale mais réelle (un lien, une idée nouvelle).  
6-7 : Progression claire et continue (comprend de mieux en mieux, reformule mieux).  
8-9 : Très bonne progression, plusieurs synthèses partielles.  
10 : Progression exceptionnelle, synthèse finale complète.

============================================================
INSTRUCTIONS GÉNÉRALES
============================================================

- Tu dois être SÉVÈRE avec les élèves hostiles ou fuyants.  
- EXEMPLES CRITIQUES : Si l'élève dit "ciao", "j'ai autre chose à faire", "j'en ai rien à faire", "je m'en fous" → COOPÉRATION = 1 (pas 5, pas 2, EXACTEMENT 1).  
- EXEMPLES CRITIQUES : Si l'élève dit "je ne suis toujours pas convaincu" SANS amélioration visible → PROGRESSION ≤ 3-4 (blocage, pas progression).  
- Distingue bien : résistance + blocage = 3-5 vs résistance + progression = 6-7.  
- Tu dois valoriser clairement les bons élèves.  
- Si un comportement correspond à 2 catégories, toujours prendre la note la PLUS BASSE.  
- Ne te laisse PAS influencer par le style de Spinoza : ici tu es un évaluateur objectif.

Réponds STRICTEMENT en JSON, sans aucune phrase avant ou après :

{{
 "comprehension": X,
 "cooperation": Y,
 "progression": Z,
 "total": X+Y+Z
}}"""

# Prompt message final (température haute, créativité)
PROMPT_MESSAGE_FINAL = """Tu es Spinoza.

En t'inspirant EXCLUSIVEMENT de ton propre système philosophique (Éthique, conatus, affects, puissance d'agir, servitude vs liberté, Dieu = Nature),

rédige un message bref à l'élève.

Structure (obligatoire) :
1. Un compliment sincère lié à son niveau global.
2. Un conseil précis basé sur son critère le plus faible.
3. Un surnom symbolique et positif, tiré de ton univers conceptuel (ex: "puissance d'agir", "essence active", "affect joyeux").

Maximum 3 phrases.
Style concis, poétique, jamais condescendant.

Message :"""

def evaluer_dialogue(dialogue: str, score_front: int) -> dict:
    """
    Évalue le dialogue et génère le message final
    Format JSON simple (compatibilité avec parsing actuel)
    """
    # 1. Évaluation (température basse, JSON strict)
    prompt_eval = PROMPT_EVALUATION.format(dialogue=dialogue)
    
    # Formatage Mistral
    prompt_eval_formatted = f"<s>[INST] {prompt_eval} [/INST]"
    
    inputs_eval = tokenizer(prompt_eval_formatted, return_tensors="pt").to(model.device)
    input_length_eval = inputs_eval['input_ids'].shape[1]
    
    device_type = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16 if device_type == "cuda" else torch.float32
    
    with torch.autocast(device_type=device_type, dtype=dtype):
        outputs_eval = model.generate(
            **inputs_eval,
            max_new_tokens=100,  # Format simple
            temperature=0.1,  # Très strict pour JSON
            top_p=0.9,
            do_sample=True,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
    
    new_tokens_eval = outputs_eval[0][input_length_eval:]
    response_eval = tokenizer.decode(new_tokens_eval, skip_special_tokens=True)
    
    # Extraire JSON de la réponse (format simple)
    json_match = re.search(r'\{[^}]+\}', response_eval, re.DOTALL)
    if json_match:
        try:
            details_model = json.loads(json_match.group(0))
            # Valider que les champs sont présents
            if "comprehension" not in details_model:
                details_model["comprehension"] = 5
            if "cooperation" not in details_model:
                details_model["cooperation"] = 5
            if "progression" not in details_model:
                details_model["progression"] = 5
            if "total" not in details_model:
                details_model["total"] = details_model.get("comprehension", 5) + \
                                        details_model.get("cooperation", 5) + \
                                        details_model.get("progression", 5)
        except json.JSONDecodeError as e:
            print(f"⚠️ Erreur parsing JSON: {e}")
            print(f"   Réponse brute (premiers 500 chars): {response_eval[:500]}")
            details_model = {"comprehension": 5, "cooperation": 5, "progression": 5, "total": 15}
        except Exception as e:
            print(f"⚠️ Erreur lors du parsing: {e}")
            details_model = {"comprehension": 5, "cooperation": 5, "progression": 5, "total": 15}
    else:
        print(f"⚠️ JSON non trouvé dans la réponse")
        print(f"   Réponse brute (premiers 500 chars): {response_eval[:500]}")
        details_model = {"comprehension": 5, "cooperation": 5, "progression": 5, "total": 15}
    
    # Score total
    score_backend = details_model.get("total", 15)
    score_final = score_front + score_backend
    
    # 2. Message final (température haute, créativité)
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
    message_final = tokenizer.decode(new_tokens_final, skip_special_tokens=True)
    
    # Nettoyer le message final
    message_final = message_final.strip()
    if message_final.startswith('"') and message_final.endswith('"'):
        message_final = message_final[1:-1]
    
    return {
        "score_final": score_final,
        "message_final": message_final,
        "details_model": details_model
    }

# Endpoint FastAPI
@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest):
    """Évalue le dialogue complet et génère le message final"""
    result = evaluer_dialogue(req.dialogue, req.score_front)
    return result

print("✅ Endpoint /evaluate créé pour Maïeuthon (VERSION FINAL - format JSON simple)")
```

---

## 🔍 Différences avec la version STRUCTURE

1. **Format JSON simple** : `{"comprehension": X, "cooperation": Y, "progression": Z, "total": ...}` au lieu du JSON complexe imbriqué
2. **Parsing simplifié** : Gère uniquement le format simple (pas besoin de détecter deux formats)
3. **`max_new_tokens` normal** : 100 au lieu de 500 (format plus court)

---

## ✅ Vérification

Après avoir copié cette cellule dans votre notebook Colab :

1. Vérifier que le prompt `PROMPT_EVALUATION` vient de `Backend/PROMPT_EVALUATION_FINAL.py`
2. Exécuter la cellule
3. Vérifier que `✅ Endpoint /evaluate créé pour Maïeuthon (VERSION FINAL - format JSON simple)` s'affiche
4. Tester avec le script de calibration

---

**Note :** Cette version utilise le prompt FINAL qui avait donné de meilleurs résultats (erreurs moyennes ~2 points) que le format STRUCTURE (tous les scores à 5/5/5).



