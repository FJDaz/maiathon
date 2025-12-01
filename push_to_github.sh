#!/bin/bash
# Script pour pousser les fichiers Vast.ai vers GitHub
# Usage: ./push_to_github.sh

set -e

echo "🔄 Synchronisation fichiers Vast.ai vers GitHub"
echo ""

cd "$(dirname "$0")"

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "Backend/Dockerfile.runpod" ]; then
    echo "❌ Erreur: Backend/Dockerfile.runpod non trouvé"
    echo "   Assurez-vous d'être dans le répertoire Spinoza_Secours_HF"
    exit 1
fi

echo "📋 Fichiers à ajouter:"
echo "  - Backend/Dockerfile.runpod"
echo "  - Backend/app_runpod.py"
echo "  - Backend/requirements.runpod.txt"
echo "  - Backend/Notebooks/Spinoza_Secours_DER"
echo ""

# Vérifier l'état git
echo "📊 État actuel:"
git status --short Backend/Dockerfile.runpod Backend/app_runpod.py Backend/requirements.runpod.txt Backend/Notebooks/Spinoza_Secours_DER 2>/dev/null || echo "Fichiers non trackés"
echo ""

# Demander confirmation
read -p "Voulez-vous ajouter ces fichiers et les pousser vers GitHub? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Annulé"
    exit 1
fi

# Ajouter les fichiers
echo "➕ Ajout des fichiers..."
git add Backend/Dockerfile.runpod
git add Backend/app_runpod.py
git add Backend/requirements.runpod.txt
git add Backend/Notebooks/Spinoza_Secours_DER

# Vérifier ce qui sera commité
echo ""
echo "📝 Fichiers à commiter:"
git status --short

# Commit
echo ""
read -p "Message de commit (défaut: 'Add Vast.ai deployment files'): " commit_msg
commit_msg=${commit_msg:-"Add Vast.ai deployment files"}
git commit -m "$commit_msg"

# Push
echo ""
echo "🚀 Push vers GitHub..."
echo "   Remote: github ou spinoza-secours"
read -p "Quel remote utiliser? (github/spinoza-secours, défaut: github): " remote
remote=${remote:-github}

git push "$remote" main

echo ""
echo "✅ Fichiers poussés vers GitHub!"
echo "   Vérifier: https://github.com/FJDaz/Spinoza_secours/tree/main/Backend"


