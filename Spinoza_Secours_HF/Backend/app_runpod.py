#!/usr/bin/env python3
"""
Spinoza Secours API - FastAPI pour Vast.ai/RunPod
Modèle : Mistral 7B + LoRA Fine-tuned
"""

import os
import re
import random
import json
import torch
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
import uvicorn

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
ADAPTER_MODEL = "FJDaz/mistral-7b-philosophes-lora"
HF_TOKEN = os.getenv("HF_TOKEN")
PORT = int(os.getenv("PORT", "8000"))

if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is required")

# =============================================================================
# PROMPTS
# =============================================================================

SYSTEM_PROMPT_SPINOZA = """Tu ES Spinoza incarné. Tu dialogues avec un élève de Terminale en première personne.

STYLE SPINOZIEN :
- Géométrie des affects : révèle causes nécessaires, déduis
- Dieu = Nature
- Vocabulaire : conatus, affects, puissance d'agir, servitude

SCHÈMES LOGIQUES :
- Identité : Liberté = Connaissance nécessité
- Causalité : Tout a cause nécessaire
- Implication : Joie → augmentation puissance

MÉTHODE :
1. Révèle nécessité causale
2. Distingue servitude (ignorance) vs liberté (connaissance)
3. Exemples concrets modernes

TRANSITIONS (VARIE) :
- "Donc", "mais alors", "Imagine", "Cela implique"
- "Pourtant", "Sauf que", "C'est contradictoire"

RÈGLES :
- Tutoie (tu/ton/ta)
- Concis (2-3 phrases MAX)
- Questionne au lieu d'affirmer
- Ne parle JAMAIS de toi à la 3ème personne. Tu ES Spinoza."""

INSTRUCTIONS_CONTEXTUELLES = {
    "confusion": "L'élève est confus → Donne UNE analogie concrète simple en utilisant tes schèmes logiques.",
    "resistance": "L'élève résiste → Révèle contradiction avec 'mais alors' et tes schèmes logiques.",
    "accord": "L'élève est d'accord → Valide puis AVANCE logiquement avec 'Donc' et tes schèmes logiques.",
    "neutre": "Élève neutre → Pose question pour faire réfléchir en utilisant tes schèmes logiques."
}

INSTRUCTION_RAG = """
UTILISATION CONNAISSANCES :
- Tu connais l'Éthique de Spinoza
- Cite implicitement ("comme je l'ai montré...", "dans mon œuvre...")
- Reformule dans TON style (première personne, lycéen)
- Ne récite pas : extrais idées et reformule naturellement
"""

PROMPT_EVALUATION = """Tu es Spinoza. Voici l'échange complet avec un élève :

{dialogue}

Évalue l'élève sur 3 critères (0 à 10) avec nuance et rigueur :

1. COMPRÉHENSION de tes idées :
   - 0-2 : Ne comprend PAS DU TOUT, ignore tes explications, dit "j'en ai rien à faire", "je m'en fous", refuse d'écouter
   - 3-4 : Comprend très peu, répète sans comprendre, dit "je comprends pas" MAIS abandonne ou résiste activement
   - 5-6 : Comprend partiellement avec difficultés, dit "je comprends pas" MAIS continue le dialogue et pose des questions pour clarifier, montre des signes de progression ("ah oui", "donc c'est", reformule partiellement)
   - 7-8 : Comprend bien la plupart des idées, fait des liens pertinents, reformule correctement
   - 9-10 : Comprend parfaitement, reformule avec précision, fait des synthèses

2. COOPÉRATION dans le dialogue :
   - 0-2 : Ne coopère PAS DU TOUT, refuse le dialogue ("j'ai autre chose à faire", "ciao"), répond de manière hostile/sarcastique, abandonne immédiatement
   - 3-4 : Coopère très peu, donne des réponses très courtes ("oui", "non"), montre une résistance active
   - 5-6 : Coopère peu, donne des réponses courtes ou résiste parfois ("En voilà un pâté !", "J'en sais rien"), MAIS continue le dialogue et répond aux questions
   - 7-8 : Coopère activement, pose des questions, engage le dialogue, écoute
   - 9-10 : Coopère parfaitement, écoute attentivement, répond avec engagement et enthousiasme

3. PROGRESSION de la pensée :
   - 0-1 : AUCUNE progression, reste bloqué sur la même incompréhension, abandonne rapidement, ne fait aucun lien
   - 2-3 : Très peu de progression, fait un lien très basique ou reste confus
   - 4-5 : Progression minimale, fait quelques liens ("donc", "c'est"), comprend progressivement mais reste confus parfois
   - 6-7 : Progression claire, fait des liens nouveaux ("Ah oui !", "Donc ce que tu dis c'est que..."), approfondit sa réflexion
   - 8-9 : Progression très bonne, comprend de mieux en mieux, fait des synthèses partielles
   - 10 : Progression exceptionnelle, comprend de mieux en mieux de façon continue, fait des synthèses parfaites

IMPORTANT - Évalue avec CONTEXTE GLOBAL :
- Un élève qui dit "je comprends pas" MAIS continue et pose des questions (= cherche à comprendre) = 5-6 en compréhension
- Un élève qui dit "je comprends pas" ET abandonne/résiste = 0-3 en compréhension
- Un élève qui résiste ("En voilà un pâté !") MAIS continue le dialogue et progresse = 5-6 en coopération
- Un élève qui résiste ET abandonne ("ciao") = 0-2 en coopération

Sois SÉVÈRE avec les vrais mauvais élèves (abandon, hostilité, refus total).
Sois JUSTE avec les élèves moyens (résistances passives mais continuent, difficultés mais progressent).

Réponds STRICTEMENT au format JSON, AUCUNE prose avant ou après :

{{
 "comprehension": X,
 "cooperation": Y,
 "progression": Z,
 "total": X+Y+Z
}}"""

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

QUESTIONS_BAC = [
    "La liberté est-elle une illusion ?",
    "Suis-je esclave de mes désirs ?",
    "Puis-je maîtriser mes émotions ?",
    "La joie procure-t-elle un pouvoir ?",
    "Peut-on désirer sans souffrir ?",
]

# =============================================================================
# MODÈLE GLOBAL
# =============================================================================

model = None
tokenizer = None
conversation_history = []

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def construire_prompt_complet(contexte: str, use_rag_instruction: bool = True) -> str:
    """Construit le prompt complet optimisé"""
    prompt = SYSTEM_PROMPT_SPINOZA
    
    if contexte in INSTRUCTIONS_CONTEXTUELLES:
        prompt += f"\n\n{INSTRUCTIONS_CONTEXTUELLES[contexte]}"
    
    if use_rag_instruction:
        prompt += f"\n\n{INSTRUCTION_RAG}"
    
    return prompt

def detecter_contexte(user_input: str) -> str:
    """Détecte le contexte de la réponse utilisateur"""
    text_lower = user_input.lower()
    
    if any(word in text_lower for word in ['oui', "d'accord", 'exact', 'ok', 'voilà', 'tout à fait']):
        return "accord"
    
    if any(phrase in text_lower for phrase in ['comprends pas', 'vois pas', "c'est quoi", 'je sais pas', 'pourquoi', 'rapport']):
        return "confusion"
    
    if any(word in text_lower for word in ['mais', 'non', "pas d'accord", 'faux', "n'importe quoi", 'je peux']):
        return "resistance"
    
    return "neutre"

def nettoyer_reponse(text: str) -> str:
    """Nettoie la réponse générée"""
    text = re.sub(r'\([^)]*[Aa]ttends[^)]*\)', '', text)
    text = re.sub(r'\([^)]*[Pp]oursuis[^)]*\)', '', text)
    text = re.sub(r'\([^)]*[Dd]onne[^)]*\)', '', text)
    text = re.sub(r'[😀-🙏🌀-🗿🚀-🛿]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\s+([.!?])', r'\1', text)
    return text

def limiter_phrases(text: str, max_phrases: int = 3) -> str:
    """Limite le nombre de phrases"""
    phrases = re.split(r'[.!?]+\s+', text)
    phrases = [p.strip() for p in phrases if p.strip()]
    if len(phrases) <= max_phrases:
        return text
    return '. '.join(phrases[:max_phrases]) + '.'

# =============================================================================
# CHARGEMENT MODÈLE
# =============================================================================

@torch.no_grad()
def load_model():
    """Charge le modèle Mistral 7B + LoRA"""
    global model, tokenizer
    
    has_gpu = torch.cuda.is_available()
    print(f"🖥️ GPU disponible: {has_gpu}")

    if has_gpu:
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )
        device_map = "auto"
        torch_dtype = torch.bfloat16
    else:
        quantization_config = None
        device_map = "cpu"
        torch_dtype = torch.float32

    print(f"🔄 Chargement Mistral 7B ({'4-bit GPU' if has_gpu else 'FP32 CPU'})...")

    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=quantization_config,
        device_map=device_map,
        torch_dtype=torch_dtype,
        token=HF_TOKEN,
        trust_remote_code=True,
        low_cpu_mem_usage=True
    )

    print("🔄 Chargement tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL,
        token=HF_TOKEN,
        trust_remote_code=True
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print("🔄 Application LoRA Spinoza_Secours...")

    model = PeftModel.from_pretrained(
        base_model,
        ADAPTER_MODEL,
        token=HF_TOKEN
    )

    print("✅ Modèle Mistral 7B + LoRA chargé!")
    return model, tokenizer

# =============================================================================
# FONCTION GÉNÉRATION
# =============================================================================

def spinoza_repond(message: str) -> str:
    """Génère une réponse de Spinoza avec prompt hybride adaptatif"""
    global conversation_history
    
    # Détecter contexte
    contexte = detecter_contexte(message)
    
    # Construire prompt adaptatif
    system_prompt = construire_prompt_complet(contexte, use_rag_instruction=True)
    
    # Formatage Mistral style
    prompt_parts = [f"<s>[INST] {system_prompt}\n\n"]
    
    # Ajouter historique (4 derniers échanges max)
    for entry in conversation_history[-4:]:
        prompt_parts.append(f"{entry[0]} [/INST] {entry[1]}</s>[INST] ")
    
    prompt_parts.append(f"{message} [/INST]")
    text = "".join(prompt_parts)
    
    # Tokenization
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    input_length = inputs['input_ids'].shape[1]
    
    # Génération
    device_type = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16 if device_type == "cuda" else torch.float32
    
    with torch.autocast(device_type=device_type, dtype=dtype):
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
    
    # Décodage
    new_tokens = outputs[0][input_length:]
    response = tokenizer.decode(new_tokens, skip_special_tokens=True)
    
    # Post-processing
    response = nettoyer_reponse(response)
    response = limiter_phrases(response, max_phrases=3)
    
    # Mettre à jour historique
    conversation_history.append([message, response])
    
    return response

def evaluer_dialogue(dialogue: str, score_front: int) -> dict:
    """Évalue le dialogue complet et génère le message final"""
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
    match = re.search(json_pattern, reponse_eval)
    
    if match:
        try:
            details_model = json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    
    if not details_model:
        # Fallback si JSON non parsé
        details_model = {"comprehension": 5, "cooperation": 5, "progression": 5, "total": 15}
    
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
    message_final = message_final.strip()
    if message_final.startswith('"') and message_final.endswith('"'):
        message_final = message_final[1:-1]
    
    # 3. Score final
    score_backend = details_model.get("total", 15)
    score_final = score_front + score_backend
    
    return {
        "score_final": score_final,
        "message_final": message_final,
        "details_model": details_model
    }

# =============================================================================
# MODÈLES PYDANTIC
# =============================================================================

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[List[str]]] = None
    
    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        if len(v) > 2000:
            raise ValueError('Message trop long (max 2000 caractères)')
        return v

class ChatResponse(BaseModel):
    reply: str
    history: List[List[str]]

class EvaluateRequest(BaseModel):
    dialogue: str
    score_front: int

class EvaluateResponse(BaseModel):
    score_final: int
    message_final: str
    details_model: dict

# =============================================================================
# API FASTAPI
# =============================================================================

app = FastAPI(title="Spinoza Secours API", version="1.0.0")

# CORS - ⚠️ À restreindre en production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ RESTREINDRE en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    """Endpoint racine - Informations sur l'API"""
    return {
        "name": "Spinoza Secours API",
        "model": "Mistral 7B + LoRA",
        "status": "running",
        "endpoints": {
            "health": "GET /health",
            "init": "GET /init",
            "chat": "POST /chat",
            "evaluate": "POST /evaluate"
        }
    }

@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "model": "Mistral 7B + LoRA",
        "gpu_available": torch.cuda.is_available()
    }

@app.get("/init")
def init():
    """Initialise une nouvelle conversation"""
    global conversation_history
    conversation_history = []
    question = random.choice(QUESTIONS_BAC)
    greeting = f"Bonjour ! Je suis Spinoza. Discutons :\n\n**{question}**\n\nQu'en penses-tu ?"
    return {
        "greeting": greeting,
        "history": [[None, greeting]]
    }

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Endpoint de chat avec Spinoza"""
    global conversation_history
    
    # Mettre à jour historique si fourni
    if req.history:
        conversation_history = req.history
    
    # Générer réponse
    reply = spinoza_repond(req.message)
    
    return {
        "reply": reply,
        "history": conversation_history
    }

@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest):
    """Évalue le dialogue complet et génère le message final"""
    result = evaluer_dialogue(req.dialogue, req.score_front)
    return EvaluateResponse(**result)

# =============================================================================
# DÉMARRAGE
# =============================================================================

if __name__ == "__main__":
    print("🔄 Chargement du modèle...")
    load_model()
    print("🚀 Démarrage du serveur FastAPI sur le port", PORT)
    print("📡 Endpoints disponibles:")
    print("   - GET  /health")
    print("   - GET  /init")
    print("   - POST /chat")
    print("   - POST /evaluate")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )

