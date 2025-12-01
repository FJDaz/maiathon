#!/bin/bash
# Script de test pour déploiement RunPod/Vast.ai
# Usage: ./test_runpod_deployment.sh <URL_BACKEND>

if [ -z "$1" ]; then
    echo "Usage: $0 <URL_BACKEND>"
    echo "Exemple: $0 https://abc123xyz-8000.proxy.runpod.net"
    exit 1
fi

API_URL="$1"

echo "🧪 Test des endpoints Spinoza Secours API"
echo "URL: $API_URL"
echo ""

# Test 1: Health check
echo "1️⃣ Test /health"
curl -s "$API_URL/health" | python3 -m json.tool
echo ""
echo ""

# Test 2: Init
echo "2️⃣ Test /init"
INIT_RESPONSE=$(curl -s "$API_URL/init")
echo "$INIT_RESPONSE" | python3 -m json.tool
echo ""
echo ""

# Test 3: Chat
echo "3️⃣ Test /chat"
CHAT_RESPONSE=$(curl -s -X POST "$API_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Bonjour Spinoza, quest-ce que le conatus ?",
    "history": []
  }')
echo "$CHAT_RESPONSE" | python3 -m json.tool
echo ""
echo ""

# Test 4: Evaluate (exemple simple)
echo "4️⃣ Test /evaluate"
EVAL_RESPONSE=$(curl -s -X POST "$API_URL/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "dialogue": "Spinoza: Bonjour ! Je suis Spinoza. Discutons : La liberté est-elle une illusion ?\nÉlève: Je pense que oui, tout est déterminé.\nSpinoza: Tu dis que tout est déterminé... quest-ce que ça veut dire pour toi ?",
    "score_front": 55
  }')
echo "$EVAL_RESPONSE" | python3 -m json.tool
echo ""
echo ""

echo "✅ Tests terminés"
echo ""
echo "Si tous les tests passent, vous pouvez mettre à jour le frontend avec cette URL."
