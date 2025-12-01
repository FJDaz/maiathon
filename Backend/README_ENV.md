# Configuration Variables d'Environnement

## Variables Requises

### NGROK_TOKEN
- **Description :** Token d'authentification ngrok pour créer un tunnel public vers l'API
- **Où l'obtenir :** https://dashboard.ngrok.com/get-started/your-authtoken
- **Utilisation :** Le notebook `colab_spinoza_secours.ipynb` récupère automatiquement cette variable via `os.getenv("NGROK_TOKEN")`

### HF_TOKEN
- **Description :** Token Hugging Face pour télécharger les modèles
- **Où l'obtenir :** https://huggingface.co/settings/tokens
- **Utilisation :** Utilisé pour télécharger Mistral 7B et le LoRA adapter

## Configuration

### Option 1 : Fichier .env (recommandé pour développement local)

1. Créer un fichier `.env` dans le dossier `Backend/` :
```bash
# Backend/.env
NGROK_TOKEN=votre_token_ngrok_ici
HF_TOKEN=hf_votre_token_huggingface_ici
```

2. Dans votre code Python, charger les variables :
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Charge automatiquement le .env

NGROK_TOKEN = os.getenv("NGROK_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")
```

### Option 2 : Variables d'environnement système

```bash
export NGROK_TOKEN=votre_token_ngrok_ici
export HF_TOKEN=hf_votre_token_huggingface_ici
```

### Option 3 : Dans Colab (Secrets)

Dans Google Colab, utilisez les Secrets :
1. Cliquez sur l'icône 🔑 **Secrets** dans le panneau de gauche
2. Ajoutez :
   - `ngrok` : votre token ngrok
   - `HuggingFaceToken` : votre token Hugging Face

Le notebook récupère automatiquement ces secrets via `userdata.get()`.

## Sécurité

⚠️ **IMPORTANT :**
- Ne jamais commiter le fichier `.env` (il doit être dans `.gitignore`)
- Ne jamais coder en dur les tokens dans le code
- Utiliser toujours des variables d'environnement pour les secrets

## Vérification

Pour vérifier que les variables sont bien chargées :

```python
import os
from dotenv import load_dotenv

load_dotenv()

ngrok_token = os.getenv("NGROK_TOKEN")
if ngrok_token:
    print("✅ NGROK_TOKEN configuré")
else:
    print("❌ NGROK_TOKEN non défini")
```


