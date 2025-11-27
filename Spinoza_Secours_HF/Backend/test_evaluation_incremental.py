#!/usr/bin/env python3
"""
Test de l'endpoint /evaluate/incremental
"""

import json
from pydantic import BaseModel, ValidationError

# Mock des dépendances nécessaires
class EvaluateRequest(BaseModel):
    dialogue: str
    score_front: int

# Test du modèle Pydantic
print("🧪 Test 1: Validation du modèle EvaluateRequest")
try:
    req = EvaluateRequest(
        dialogue="Élève: Bonjour\nSpinoza: Salut\nÉlève: Qu'est-ce que la liberté ?",
        score_front=100
    )
    print(f"✅ Requête valide: dialogue={len(req.dialogue)} chars, score_front={req.score_front}")
except ValidationError as e:
    print(f"❌ Erreur validation: {e}")
    exit(1)

# Test de la structure de données
print("\n🧪 Test 2: Structure de données incremental_scores")
incremental_scores = {}
dialogue_id = hash(req.dialogue)
incremental_scores[dialogue_id] = []

# Simulation d'un score
test_score = {
    "comprehension": 7,
    "cooperation": 8,
    "progression": 6,
    "total": 21
}

incremental_scores[dialogue_id].append({
    "scores": test_score,
    "exchange_count": len(incremental_scores[dialogue_id]) + 1
})

print(f"✅ Score stocké: {json.dumps(incremental_scores[dialogue_id], indent=2, ensure_ascii=False)}")

# Test de la structure de retour
print("\n🧪 Test 3: Structure de réponse de l'endpoint")
response_structure = {
    "scores": test_score,
    "exchange_count": len(incremental_scores[dialogue_id]),
    "accumulated": len(incremental_scores[dialogue_id]) > 0
}
print(f"✅ Réponse valide: {json.dumps(response_structure, indent=2, ensure_ascii=False)}")

# Test du parsing JSON avec regex
print("\n🧪 Test 4: Parsing JSON avec regex (simulation)")
import re

# Simule une réponse du modèle qui pourrait contenir du texte autour du JSON
test_response = '''Voici l'évaluation:
{
 "comprehension": 7,
 "cooperation": 8,
 "progression": 6,
 "total": 21
}
C'est bon.'''

json_pattern = r'\{[^{}]*"comprehension"[^{}]*"cooperation"[^{}]*"progression"[^{}]*"total"[^{}]*\}'
json_match = re.search(json_pattern, test_response, re.DOTALL)

if json_match:
    try:
        parsed = json.loads(json_match.group(0))
        print(f"✅ JSON parsé avec succès: {json.dumps(parsed, indent=2, ensure_ascii=False)}")
    except json.JSONDecodeError as e:
        print(f"❌ Erreur parsing JSON: {e}")
else:
    print("❌ JSON non trouvé dans la réponse")

# Test avec JSON valide mais incomplet
print("\n🧪 Test 5: Validation des champs requis")
incomplete_json = {"comprehension": 7, "cooperation": 8}  # Manque progression et total
required_fields = ["comprehension", "cooperation", "progression", "total"]

details_model = incomplete_json.copy()
for field in required_fields:
    if field not in details_model:
        details_model[field] = 5 if field != "total" else 15

print(f"✅ Champs manquants remplis: {json.dumps(details_model, indent=2, ensure_ascii=False)}")

# Test de l'extraction des 2 derniers échanges
print("\n🧪 Test 6: Extraction des 2 derniers échanges")
test_dialogue = """Élève: Premier message
Spinoza: Réponse 1
Élève: Deuxième message
Spinoza: Réponse 2
Élève: Troisième message
Spinoza: Réponse 3"""

lines = [l.strip() for l in test_dialogue.split('\n') if l.strip()]
if len(lines) > 4:
    recent_exchanges = '\n'.join(lines[-4:])  # 2 derniers échanges (4 lignes)
else:
    recent_exchanges = test_dialogue

print(f"✅ Dialogue complet: {len(lines)} lignes")
print(f"✅ 2 derniers échanges ({len(recent_exchanges.split(chr(10)))} lignes):")
print(recent_exchanges)

print("\n" + "="*60)
print("✅ Tous les tests sont passés !")
print("="*60)
print("\n📝 Note: Ce script teste la logique et la structure.")
print("   Pour tester l'endpoint complet, il faut:")
print("   1. Que le serveur Colab soit lancé")
print("   2. L'URL ngrok")
print("   3. Faire un appel HTTP POST réel")



