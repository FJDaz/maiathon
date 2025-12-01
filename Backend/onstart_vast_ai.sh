#!/bin/bash
# On-start Script pour Vast.ai - Spinoza Secours
# Ce script s'exécute au démarrage de l'instance

set -e

echo "🚀 Démarrage Spinoza Secours sur Vast.ai..."

# Créer répertoire de travail
mkdir -p /workspace/spinoza-secours
cd /workspace/spinoza-secours

# Cloner le repository GitHub
echo "📥 Clonage du repository GitHub..."
if [ ! -d "maiathon" ]; then
    git clone https://github.com/FJDaz/maiathon.git
fi

cd maiathon/Spinoza_Secours_HF/Backend

# Installer les dépendances Python
echo "📦 Installation des dépendances..."
pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.runpod.txt

# Lancer l'application FastAPI
echo "🚀 Lancement de l'application FastAPI..."
python app_runpod.py

