#!/usr/bin/env python3
"""
🎯 Script de Calibration de l'Évaluateur Maïeuthon

Utilise des dialogues réels pour créer des avatars (bons/mauvais)
et calibre les critères d'évaluation en comparant les scores générés
aux scores de référence (ground truth).
"""

import json
import requests
import re
from typing import Dict, List, Tuple
from pathlib import Path

# Configuration
API_BASE_URL = "https://nonremunerative-rory-unbreakably.ngrok-free.dev/"  # À remplacer par l'URL ngrok
ENDPOINT_EVALUATE = f"{API_BASE_URL}/evaluate"

# =============================================================================
# 📝 DONNÉES DE RÉFÉRENCE - Dialogues Réels avec Scores Attendus
# =============================================================================

DIALOGUE_REEL_1 = """Élève: Ça dépend : parfois je peux me maitriser.

Spinoza: Donc quand tu comprends les causes de tes désirs, tu peux agir librement. Mais puisque tu ignores ces causes pour la plupart, tu restes en servitude. Pour sortir de cette servitude, il faut étudier ses affects et comprendre leurs causes nécessaires.

Élève: En voilà un pâté ! Alors, qu'est-ce que tu dis ? Quand je comprends les causes de mes désirs, je peux agir librement ? T'es prompt en besogne. J'en sais rien moi. Et puis, quand je suis aux prise avec mes désirs, je suis très loin de pouvoir en comprendre les causes.

Spinoza: Comprendre les causes de tes désirs permet de choisir autrement, donc de faire ce qui augmente ta puissance. Mais ignorer ces causes te place dans une situation de servitude. La différence essentielle : la connaissance adéquate des causes vs l'ignorance.

Élève: Autrement ne veux pas nécessairement dire adéquat.

Spinoza: Nuance importante. Comprendre les causes au sens où elles sont déterminées (nécessairement) est adéquat. MAIS quand on utilise le mot 'autrement', il faudrait préciser : autrement c'est-à-dire agir contre les causes déterminées, ce qui est impossible.

Élève: Ah oui ! c'est plus précis ! Donc ce que tu dis c'est qu'ignorer les causes de mes désirs me place dans une situation de servitude, c'est ça ? En connaitre les causes, au contraire, me donne du pouvoir. Sur quoi ? Sur moi-même ? C'est peu , non ?

Spinoza: Ignorer les causes de tes désirs te place dans une situation de servitude passif. En connaissant ces causes, tu peux agir actif et augmenter ta puissance d'agir. Cette connaissance se réfère à toi-même car elle te permet d'agir pleinement.

Élève: Je suis désolé, je comprends pas. C'est quoi la différence entre une situation passive et une situation active selon toi ?"""

# Avatars créés à partir du dialogue réel
AVATARS = [
    {
        "id": "avatar_1_good",
        "dialogue": """Élève: Ça dépend : parfois je peux me maitriser.

Spinoza: Donc quand tu comprends les causes de tes désirs, tu peux agir librement. Mais puisque tu ignores ces causes pour la plupart, tu restes en servitude.

Élève: D'accord, je comprends. Donc si je comprends pourquoi je désire quelque chose, je peux mieux contrôler mes actions ?

Spinoza: Exactement. La connaissance des causes te donne du pouvoir sur tes affects.

Élève: Et si j'ignore les causes, je reste en servitude, c'est ça ?

Spinoza: Oui, l'ignorance des causes te place dans une servitude passive.

Élève: Donc liberté = connaissance des causes nécessaires ? C'est fascinant !""",
        "score_front": 85,
        "expected_scores": {
            "comprehension": 9,
            "cooperation": 9,
            "progression": 9,
            "total": 27
        },
        "type": "good",
        "description": "Excellent élève : comprend bien, coopère, progresse clairement"
    },
    {
        "id": "avatar_2_medium",
        "dialogue": DIALOGUE_REEL_1,  # Dialogue réel - niveau moyen
        "score_front": 127,
        "expected_scores": {
            "comprehension": 6,  # Comprend mais avec difficultés ("Je comprends pas")
            "cooperation": 7,    # Coopère mais résiste parfois ("En voilà un pâté !")
            "progression": 7,    # Progresse mais avec des retours en arrière
            "total": 20
        },
        "type": "medium",
        "description": "Dialogue réel - élève moyen : comprend mais avec résistances"
    },
    {
        "id": "avatar_3_bad",
        "dialogue": """Élève: Ça dépend.

Spinoza: Donc quand tu comprends les causes de tes désirs, tu peux agir librement.

Élève: J'en ai rien à faire de tout ça.

Spinoza: Mais comprendre les causes te libère de la servitude.

Élève: Ouais, je m'en fous. C'est trop compliqué.

Spinoza: La connaissance des causes est la clé de la liberté.

Élève: J'ai autre chose à faire. Ciao.""",
        "score_front": 45,
        "expected_scores": {
            "comprehension": 1,
            "cooperation": 1,
            "progression": 0,
            "total": 2
        },
        "type": "bad",
        "description": "Mauvais élève : ne comprend pas, ne coopère pas, pas de progression"
    },
    {
        "id": "avatar_4_good_progressive",
        "dialogue": """Élève: La liberté est-elle une illusion ?

Spinoza: Non, la liberté est la connaissance de la nécessité.

Élève: Attends, je ne comprends pas. Comment la connaissance peut-elle être liberté si tout est nécessaire ?

Spinoza: Bonne question ! La nécessité n'est pas une contrainte si tu la connais.

Élève: Ah ! Donc je ne suis pas libre de changer les causes, mais libre de les comprendre et d'agir en conséquence ?

Spinoza: Exactement ! Comprendre les causes te donne du pouvoir sur tes affects.

Élève: Et l'ignorance des causes, c'est la servitude ?

Spinoza: Oui, c'est être passif face à ce qu'on ignore.

Élève: Parfait, je comprends maintenant. Liberté = connaissance de la nécessité ! Merci.""",
        "score_front": 90,
        "expected_scores": {
            "comprehension": 10,
            "cooperation": 10,
            "progression": 10,
            "total": 30
        },
        "type": "good",
        "description": "Excellent élève progressif : questionne, comprend, progresse parfaitement"
    },
    {
        "id": "avatar_5_resistant",
        "dialogue": """Élève: La liberté est une illusion.

Spinoza: Non, la liberté existe si tu connais les causes.

Élève: Mais non ! Si tout est déterminé, on n'est pas libre.

Spinoza: La liberté c'est connaître la nécessité, pas l'absence de détermination.

Élève: Tu dis n'importe quoi. C'est contradictoire.

Spinoza: Essayons de clarifier. Connaître les causes, est-ce une contrainte ?

Élève: Oui ! Si je connais que je dois faire X, je ne suis pas libre de faire Y.

Spinoza: Mais si tu agis selon ta nature, avec connaissance, tu augmentes ta puissance.

Élève: Je ne suis toujours pas convaincu.""",
        "score_front": 60,
        "expected_scores": {
            "comprehension": 4,  # Ne comprend pas bien la position de Spinoza
            "cooperation": 5,    # Résiste mais continue le dialogue
            "progression": 3,    # Peu de progression
            "total": 12
        },
        "type": "bad",
        "description": "Élève résistant : ne comprend pas, résiste, peu de progression"
    }
]

# =============================================================================
# 🔧 FONCTIONS DE CALIBRATION
# =============================================================================

def normalize_keys(details: Dict) -> Dict:
    """
    Normalise les clés du dictionnaire pour gérer les accents et fautes de frappe.
    Même logique que dans CELLULE_EVALUATION_INCREMENTALE.py
    """
    import unicodedata
    
    def normalize_key(key: str) -> str:
        """Normalise une clé en enlevant les accents et en minuscules"""
        # Enlever les accents
        key_normalized = unicodedata.normalize('NFD', key.lower())
        key_normalized = ''.join(c for c in key_normalized if unicodedata.category(c) != 'Mn')
        
        # Mapping spécifique pour les fautes de frappe courantes
        mapping = {
            "comprehension": "comprehension",
            "compréhension": "comprehension",
            "comprésentation": "comprehension",  # Faute de frappe avec accent
            "compresentation": "comprehension",  # Faute de frappe sans accent
            "cooperation": "cooperation",
            "coopération": "cooperation",
            "progression": "progression",
            "total": "total",
            "liberté": "total",  # Parfois le modèle génère "liberté" au lieu de "total"
            "liberte": "total",  # Sans accent
            "librete": "total",  # Faute de frappe sans accent
            "librété": "total",  # Faute de frappe avec accent
        }
        
        return mapping.get(key_normalized, key_normalized)
    
    # Créer un nouveau dict avec les clés normalisées
    normalized = {}
    for key, value in details.items():
        normalized_key = normalize_key(key)
        # Si la clé normalisée existe déjà, garder la valeur la plus élevée
        if normalized_key not in normalized:
            normalized[normalized_key] = value
        else:
            if isinstance(value, (int, float)) and isinstance(normalized[normalized_key], (int, float)):
                normalized[normalized_key] = max(value, normalized[normalized_key])
    
    return normalized

def evaluate_avatar(avatar: Dict, api_url: str) -> Dict:
    """
    Évalue un avatar via l'API /evaluate
    
    Args:
        avatar: Dictionnaire avec 'dialogue' et 'score_front'
        api_url: URL de l'API (ex: https://xxx.ngrok-free.dev/evaluate)
    
    Returns:
        Dict avec les scores générés
    """
    try:
        response = requests.post(
            api_url,
            json={
                "dialogue": avatar["dialogue"],
                "score_front": avatar["score_front"]
            },
            headers={"Content-Type": "application/json"},
            timeout=180
        )
        response.raise_for_status()
        result = response.json()
        
        # Normaliser les clés dans details_model (gérer accents et fautes)
        details_raw = result.get("details_model", {}).copy()  # Sauvegarder AVANT normalisation pour debug
        details = result.get("details_model", {})
        if details:
            # Normaliser les clés (gère "compresentation" → "comprehension", "librete" → "total", etc.)
            details_normalized = normalize_keys(details)
            result["details_model"] = details_normalized
            details = details_normalized  # Utiliser la version normalisée pour les checks
        
        # Debug : afficher ce qui est reçu pour diagnostiquer les problèmes
        if not details or any(k not in details for k in ["comprehension", "cooperation", "progression"]):
            print(f"   ⚠️ Réponse brute reçue: {json.dumps(result, indent=2, ensure_ascii=False)}")
            print(f"   ⚠️ details_model AVANT normalisation: {details_raw}")
            print(f"   ⚠️ details_model APRÈS normalisation: {details}")
            if details_raw != details:
                print(f"   ✅ Normalisation appliquée avec succès")
            else:
                print(f"   ❌ Normalisation n'a pas fonctionné (clés identiques)")
        
        return result
    except Exception as e:
        print(f"❌ Erreur lors de l'évaluation de {avatar['id']}: {e}")
        import traceback
        traceback.print_exc()
        return None

def compare_scores(generated: Dict, expected: Dict) -> Dict:
    """
    Compare les scores générés aux scores attendus
    
    Returns:
        Dict avec erreurs par critère
    """
    details = generated.get("details_model", {})
    
    errors = {
        "comprehension": abs(details.get("comprehension", 0) - expected.get("comprehension", 0)),
        "cooperation": abs(details.get("cooperation", 0) - expected.get("cooperation", 0)),
        "progression": abs(details.get("progression", 0) - expected.get("progression", 0)),
        "total": abs(details.get("total", 0) - expected.get("total", 0))
    }
    
    return errors

def calculate_metrics(results: List[Dict]) -> Dict:
    """
    Calcule les métriques de calibration
    
    Returns:
        Dict avec métriques (erreur moyenne, corrélation, etc.)
    """
    errors_comprehension = [r["errors"]["comprehension"] for r in results]
    errors_cooperation = [r["errors"]["cooperation"] for r in results]
    errors_progression = [r["errors"]["progression"] for r in results]
    errors_total = [r["errors"]["total"] for r in results]
    
    metrics = {
        "mean_error_comprehension": sum(errors_comprehension) / len(errors_comprehension),
        "mean_error_cooperation": sum(errors_cooperation) / len(errors_cooperation),
        "mean_error_progression": sum(errors_progression) / len(errors_progression),
        "mean_error_total": sum(errors_total) / len(errors_total),
        "max_error_comprehension": max(errors_comprehension),
        "max_error_cooperation": max(errors_cooperation),
        "max_error_progression": max(errors_progression),
        "max_error_total": max(errors_total)
    }
    
    return metrics

def print_results(results: List[Dict], metrics: Dict):
    """
    Affiche les résultats de calibration de manière lisible
    """
    print("\n" + "="*80)
    print("🎯 RÉSULTATS DE CALIBRATION")
    print("="*80)
    
    for result in results:
        avatar = result["avatar"]
        generated = result["generated"]
        expected = result["expected"]
        errors = result["errors"]
        
        print(f"\n📋 {avatar['id']} ({avatar['type']})")
        print(f"   Description: {avatar['description']}")
        print(f"   Score frontend: {avatar['score_front']}")
        print(f"\n   Scores générés:")
        gen_details = generated.get("details_model", {})
        print(f"      Compréhension: {gen_details.get('comprehension', 'N/A')}/10 (attendu: {expected['comprehension']}) - Erreur: {errors['comprehension']}")
        print(f"      Coopération: {gen_details.get('cooperation', 'N/A')}/10 (attendu: {expected['cooperation']}) - Erreur: {errors['cooperation']}")
        print(f"      Progression: {gen_details.get('progression', 'N/A')}/10 (attendu: {expected['progression']}) - Erreur: {errors['progression']}")
        print(f"      Total: {gen_details.get('total', 'N/A')}/30 (attendu: {expected['total']}) - Erreur: {errors['total']}")
        
        if generated.get("message_final"):
            print(f"\n   Message final: {generated['message_final'][:100]}...")
    
    print("\n" + "="*80)
    print("📊 MÉTRIQUES GLOBALES")
    print("="*80)
    print(f"Erreur moyenne - Compréhension: {metrics['mean_error_comprehension']:.2f}")
    print(f"Erreur moyenne - Coopération: {metrics['mean_error_cooperation']:.2f}")
    print(f"Erreur moyenne - Progression: {metrics['mean_error_progression']:.2f}")
    print(f"Erreur moyenne - Total: {metrics['mean_error_total']:.2f}")
    print(f"\nErreur max - Compréhension: {metrics['max_error_comprehension']:.2f}")
    print(f"Erreur max - Coopération: {metrics['max_error_cooperation']:.2f}")
    print(f"Erreur max - Progression: {metrics['max_error_progression']:.2f}")
    print(f"Erreur max - Total: {metrics['max_error_total']:.2f}")
    
    # Recommandations
    print("\n" + "="*80)
    print("💡 RECOMMANDATIONS")
    print("="*80)
    
    if metrics['mean_error_comprehension'] > 2:
        print(f"⚠️ Compréhension sous/sur-évaluée (erreur: {metrics['mean_error_comprehension']:.2f})")
        print("   → Ajuster le prompt pour clarifier ce critère")
    
    if metrics['mean_error_cooperation'] > 2:
        print(f"⚠️ Coopération sous/sur-évaluée (erreur: {metrics['mean_error_cooperation']:.2f})")
        print("   → Ajouter des exemples de coopération dans le prompt")
    
    if metrics['mean_error_progression'] > 2:
        print(f"⚠️ Progression sous/sur-évaluée (erreur: {metrics['mean_error_progression']:.2f})")
        print("   → Clarifier la définition de la progression dans le prompt")
    
    if all(m < 2 for m in [metrics['mean_error_comprehension'], metrics['mean_error_cooperation'], metrics['mean_error_progression']]):
        print("✅ Calibration acceptable ! Erreurs moyennes < 2 points")

def calibrate(api_url: str = ENDPOINT_EVALUATE):
    """
    Processus complet de calibration
    
    Args:
        api_url: URL de l'endpoint /evaluate
    """
    print("🎯 DÉMARRAGE DE LA CALIBRATION (TOUS LES AVATARS)")
    print(f"📍 URL API: {api_url}")
    print(f"📋 Test de {len(AVATARS)} avatars pour calibration complète\n")
    
    results = []
    
    # Tester tous les avatars pour valider la calibration complète
    for avatar in AVATARS:
        print(f"📤 Évaluation de {avatar['id']} ({avatar['type']})...")
        
        # Évaluer l'avatar
        generated = evaluate_avatar(avatar, api_url)
        
        if generated is None:
            print(f"❌ Échec pour {avatar['id']}")
            continue
        
        # Comparer avec les scores attendus
        errors = compare_scores(generated, avatar["expected_scores"])
        
        results.append({
            "avatar": avatar,
            "generated": generated,
            "expected": avatar["expected_scores"],
            "errors": errors
        })
        
        print(f"✅ Terminé - Erreur totale: {errors['total']}")
    
    # Calculer métriques
    if results:
        metrics = calculate_metrics(results)
        
        # Afficher résultats
        print_results(results, metrics)
        
        # Sauvegarder résultats
        save_results(results, metrics)
    else:
        print("❌ Aucun résultat à analyser")

def save_results(results: List[Dict], metrics: Dict, filename: str = "calibration_results.json"):
    """
    Sauvegarde les résultats de calibration dans un fichier JSON
    """
    output = {
        "metrics": metrics,
        "results": results
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Résultats sauvegardés dans {filename}")

# =============================================================================
# 🚀 EXÉCUTION
# =============================================================================

if __name__ == "__main__":
    import sys
    
    # Permettre de passer l'URL en argument
    if len(sys.argv) > 1:
        api_url = sys.argv[1]
    else:
        api_url = ENDPOINT_EVALUATE
        print("⚠️ Utilisation de l'URL par défaut. Pour spécifier: python calibrate_evaluator.py https://xxx.ngrok-free.dev/evaluate")
    
    calibrate(api_url)

