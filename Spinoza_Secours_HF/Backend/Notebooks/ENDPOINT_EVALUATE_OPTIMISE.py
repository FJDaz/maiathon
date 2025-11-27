# =============================================================================
# 🔧 ENDPOINT /evaluate OPTIMISÉ - Utilise les Scores Incrémentaux
# =============================================================================
# Ce code remplace l'endpoint /evaluate pour utiliser les scores incrémentaux
# et éviter la double évaluation (allège le modèle)
# =============================================================================
# À copier dans votre notebook Colab, dans la cellule Maïeuthon
# =============================================================================

@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate_endpoint(req: EvaluateRequest):
    """
    Évaluation finale optimisée :
    - Si scores incrémentaux disponibles → les agrège + génère seulement le message final
    - Sinon → évaluation complète normale (fallback)
    
    Cela évite la double charge sur le modèle.
    """
    dialogue_id = hash(req.dialogue)
    
    # Vérifier si scores incrémentaux disponibles
    if dialogue_id in incremental_scores and len(incremental_scores[dialogue_id]) > 0:
        scores_inc = incremental_scores[dialogue_id]
        
        print(f"📊 [OPTIMISATION] Utilisation des scores incrémentaux ({len(scores_inc)} évaluations)")
        
        # Agréger les scores incrémentaux (moyenne pondérée par ordre)
        # Le dernier échange est plus important (poids croissant)
        n = len(scores_inc)
        weights = [i+1 for i in range(n)]  # [1, 2, 3, ...] pour n=2
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
        details_model["total"] = sum([
            details_model["comprehension"],
            details_model["cooperation"],
            details_model["progression"]
        ])
        
        print(f"📊 [OPTIMISATION] Scores agrégés: {details_model}")
        
        # Score total
        score_backend = details_model.get("total", 15)
        score_final = req.score_front + score_backend
        
        # ⚡ OPTIMISATION : Générer SEULEMENT le message final (scores déjà calculés)
        # Pas besoin de réévaluer le dialogue complet → Gain de temps et charge
        prompt_final = PROMPT_MESSAGE_FINAL
        
        prompt_final_formatted = f"<s>[INST] {prompt_final} [/INST]"
        
        inputs_final = tokenizer(prompt_final_formatted, return_tensors="pt").to(model.device)
        input_length_final = inputs_final['input_ids'].shape[1]
        
        device_type = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.bfloat16 if device_type == "cuda" else torch.float32
        
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
        message_final = message_final.strip()
        if message_final.startswith('"') and message_final.endswith('"'):
            message_final = message_final[1:-1]
        
        # Nettoyer les scores incrémentaux après utilisation (optionnel, pour libérer mémoire)
        # del incremental_scores[dialogue_id]
        
        return EvaluateResponse(
            score_final=score_final,
            message_final=message_final,
            details_model=details_model
        )
    
    else:
        # Fallback : évaluation complète si pas de scores incrémentaux
        print("⚠️ [FALLBACK] Pas de scores incrémentaux, évaluation complète")
        return evaluer_dialogue(req.dialogue, req.score_front)

print("✅ Endpoint /evaluate optimisé (utilise scores incrémentaux si disponibles)")

