#!/usr/bin/env python3
"""
Test HTTP de l'endpoint /evaluate/incremental
Usage: python3 test_http_incremental.py <URL_NGROK>
"""

import sys
import json
import requests
from typing import Optional

def test_incremental_endpoint(base_url: str):
    """Test l'endpoint /evaluate/incremental"""
    
    url = f"{base_url}/evaluate/incremental"
    
    # Test dialogue simple
    test_data = {
        "dialogue": "Élève: Bonjour\nSpinoza: Salut\nÉlève: Qu'est-ce que la liberté ?",
        "score_front": 100
    }
    
    # Activer le debug pour voir la réponse brute
    debug = "--debug" in sys.argv or "-d" in sys.argv
    
    if debug:
        url = f"{url}?debug=true"
        print("🔍 Mode DEBUG activé - la réponse contiendra la réponse brute du modèle")
    
    print(f"🧪 Test de l'endpoint: {url}")
    print(f"📤 Envoi de la requête...")
    print(f"   Dialogue: {test_data['dialogue'][:50]}...")
    print(f"   Score front: {test_data['score_front']}")
    print()
    
    try:
        response = requests.post(
            url,
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📥 Statut HTTP: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Réponse reçue:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # Vérifier la structure
            required_keys = ["scores", "exchange_count", "accumulated"]
            missing_keys = [key for key in required_keys if key not in result]
            
            if missing_keys:
                print(f"⚠️  Clés manquantes dans la réponse: {missing_keys}")
                return False
            
            # Vérifier la structure des scores
            if "scores" in result:
                score_keys = ["comprehension", "cooperation", "progression", "total"]
                missing_score_keys = [key for key in score_keys if key not in result["scores"]]
                
            if missing_score_keys:
                print(f"⚠️  Clés manquantes dans scores: {missing_score_keys}")
                return False
            
            # Afficher la réponse debug si présente
            if "debug" in result:
                print()
                print("🔍 [DEBUG] Informations de debug:")
                print(f"   Réponse brute du modèle: {result['debug'].get('raw_model_response', 'N/A')[:300]}...")
                print(f"   Parsing réussi: {result['debug'].get('parsing_success', False)}")
            
            print()
            print("✅ Test réussi ! L'endpoint fonctionne correctement.")
            return True
            
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            print(f"   Réponse: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout: Le serveur ne répond pas (vérifiez que Colab est lancé)")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Erreur de connexion: Impossible de joindre le serveur")
        print(f"   URL testée: {url}")
        print(f"   Vérifiez que:")
        print(f"   1. Le serveur Colab est lancé")
        print(f"   2. ngrok est actif")
        print(f"   3. L'URL ngrok est correcte")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 test_http_incremental.py <URL_NGROK> [--debug]")
        print()
        print("Exemple:")
        print("  python3 test_http_incremental.py https://abc123.ngrok-free.app")
        print("  python3 test_http_incremental.py https://abc123.ngrok-free.app --debug")
        print()
        print("Options:")
        print("  --debug, -d  : Affiche la réponse brute du modèle dans la réponse HTTP")
        print()
        print("Ou avec le chemin complet:")
        print("  python3 test_http_incremental.py https://abc123.ngrok-free.app/evaluate/incremental")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Nettoyer l'URL si elle contient le chemin complet
    if "/evaluate/incremental" in url:
        base_url = url.replace("/evaluate/incremental", "")
    else:
        base_url = url.rstrip("/")
    
    print("="*60)
    print("🧪 Test HTTP de l'endpoint /evaluate/incremental")
    print("="*60)
    print()
    
    success = test_incremental_endpoint(base_url)
    
    print()
    print("="*60)
    if success:
        print("✅ Test terminé avec succès")
    else:
        print("❌ Test échoué")
    print("="*60)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

