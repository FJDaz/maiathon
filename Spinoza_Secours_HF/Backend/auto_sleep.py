#!/usr/bin/env python3
"""
Script d'auto-sleep pour Vast.ai
Arrête automatiquement l'instance après une période d'inactivité
Usage: python3 auto_sleep.py --timeout 1800 (30 minutes)
"""

import os
import sys
import time
import argparse
import subprocess
from datetime import datetime, timedelta
from typing import Optional

# Configuration par défaut
DEFAULT_TIMEOUT = 1800  # 30 minutes en secondes
LOG_FILE = "/tmp/auto_sleep.log"
LAST_ACTIVITY_FILE = "/tmp/last_activity.txt"

def log(message: str):
    """Écrit un message dans le log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_message)
    print(log_message.strip())

def get_last_activity() -> Optional[datetime]:
    """Récupère la dernière activité depuis le fichier"""
    if not os.path.exists(LAST_ACTIVITY_FILE):
        return None
    try:
        with open(LAST_ACTIVITY_FILE, "r") as f:
            timestamp_str = f.read().strip()
            return datetime.fromisoformat(timestamp_str)
    except Exception as e:
        log(f"Erreur lecture dernière activité: {e}")
        return None

def update_last_activity():
    """Met à jour le timestamp de dernière activité"""
    try:
        with open(LAST_ACTIVITY_FILE, "w") as f:
            f.write(datetime.now().isoformat())
    except Exception as e:
        log(f"Erreur écriture dernière activité: {e}")

def check_api_activity(api_url: str = "http://localhost:8000") -> bool:
    """Vérifie si l'API a reçu des requêtes récentes"""
    # Vérifier les logs FastAPI ou un endpoint de monitoring
    # Pour simplifier, on vérifie juste si le serveur répond
    try:
        import requests
        response = requests.get(f"{api_url}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def stop_instance():
    """Arrête l'instance Vast.ai"""
    log("🛑 Arrêt de l'instance après période d'inactivité...")
    # Note: Vast.ai n'a pas d'API publique pour arrêter l'instance
    # Il faut le faire manuellement depuis le dashboard ou utiliser leur API si disponible
    log("⚠️  Arrêt manuel requis depuis le dashboard Vast.ai")
    log("💡 Lien: https://vast.ai/console/instances")
    # Alternative: arrêter le processus Python (mais l'instance continue de tourner)
    # sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Auto-sleep pour Vast.ai")
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Timeout en secondes (défaut: {DEFAULT_TIMEOUT}s = {DEFAULT_TIMEOUT//60}min)"
    )
    parser.add_argument(
        "--check-interval",
        type=int,
        default=60,
        help="Intervalle de vérification en secondes (défaut: 60s)"
    )
    args = parser.parse_args()

    log(f"🚀 Auto-sleep démarré (timeout: {args.timeout}s = {args.timeout//60}min)")
    log(f"⏱️  Vérification toutes les {args.check_interval}s")

    while True:
        last_activity = get_last_activity()
        now = datetime.now()

        if last_activity:
            inactive_time = (now - last_activity).total_seconds()
            log(f"⏳ Temps d'inactivité: {inactive_time:.0f}s / {args.timeout}s")

            if inactive_time >= args.timeout:
                log(f"⏰ Timeout atteint ({args.timeout}s)")
                stop_instance()
                break
        else:
            log("📝 Aucune activité précédente enregistrée")
            update_last_activity()

        # Vérifier l'activité de l'API
        if check_api_activity():
            log("✅ Activité détectée, mise à jour du timestamp")
            update_last_activity()

        time.sleep(args.check_interval)

if __name__ == "__main__":
    main()

