#!/bin/bash
# Script de monitoring pour instance Vast.ai
# Usage: Ajouter dans cron pour vérifier régulièrement
# Exemple cron: 0 * * * * /chemin/vers/monitor_vast_ai.sh

# Configuration
INSTANCE_URL="${VAST_AI_URL:-http://votre-instance.vast.ai:8000}"
ALERT_EMAIL="${ALERT_EMAIL:-votre-email@example.com}"
LOG_FILE="${LOG_FILE:-/tmp/vast_ai_monitor.log}"

# Fonction de logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Test health check
log "Vérification health check..."
response=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$INSTANCE_URL/health")

if [ "$response" != "200" ]; then
    log "❌ ALERT: Instance Vast.ai down (HTTP $response)"
    
    # Envoyer email si mail disponible
    if command -v mail &> /dev/null; then
        echo "Instance Vast.ai inaccessible. HTTP Status: $response" | \
            mail -s "🚨 Vast.ai Alert - Instance Down" "$ALERT_EMAIL"
    fi
    
    exit 1
fi

# Test init endpoint (optionnel, plus lourd)
# response_init=$(curl -s -o /dev/null -w "%{http_code}" --max-time 15 "$INSTANCE_URL/init")
# if [ "$response_init" != "200" ]; then
#     log "⚠️ WARNING: Endpoint /init retourne $response_init"
# fi

log "✅ Instance Vast.ai opérationnelle (HTTP $response)"
exit 0

