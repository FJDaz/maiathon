# Guide de Déploiement Vast.ai - Spinoza Secours

**Modèle :** Mistral 7B + LoRA  
**Budget :** ~$0.20-0.40/h (RTX 3090)  
**Usage :** Ponctuel (démos/sessions)  
**Dépôt minimum :** Généralement 0€ (paiement à l'usage)

---

## 📋 Prérequis

1. **Compte Vast.ai** : Créer un compte sur [vast.ai](https://vast.ai/)
2. **Token Hugging Face** : Obtenir un token avec accès en lecture sur [Hugging Face](https://huggingface.co/settings/tokens)
3. **GitHub** (optionnel) : Si vous déployez depuis un dépôt GitHub

---

## 🚀 Étapes de Déploiement

### Étape 1 : Préparer les Fichiers

Les fichiers suivants sont déjà prêts dans le projet :
- `Dockerfile.runpod` - Dockerfile compatible Vast.ai
- `app_runpod.py` - Application FastAPI complète
- `requirements.runpod.txt` - Dépendances Python

### Étape 2 : Créer une Instance Vast.ai

1. **Se connecter à Vast.ai**
   - Aller sur [vast.ai](https://vast.ai/)
   - Se connecter ou créer un compte

2. **Créer une nouvelle instance**
   - Cliquer sur **"Create"** ou **"New Instance"**
   - Sélectionner **"Docker"** comme type d'instance

3. **Configurer l'instance**
   - **GPU** : **RTX 3090 (24GB) recommandé** ⭐
     - Coût : $0.20-0.40/h (similaire ou moins cher que T4)
     - Performance : 2-3x plus rapide que T4
     - VRAM : 24GB (suffisant pour Mistral 7B en 4-bit)
     - Alternative : RTX 4090 si besoin de plus de performance ($0.35-0.60/h)
   - **Image Docker** : Sélectionner **"Custom Dockerfile"** ou **"From GitHub"**
   - **Container Disk** : 50GB minimum (pour le modèle Mistral 7B)
   - **Port** : 8000 (exposé automatiquement)

4. **Configurer les variables d'environnement**
   Dans l'interface Vast.ai, ajouter :
   ```
   HF_TOKEN=votre_token_huggingface
   PORT=8000
   ```

5. **Configurer le Dockerfile**
   - Si déploiement depuis GitHub : Spécifier le chemin `Backend/Dockerfile.runpod`
   - Si déploiement direct : Copier le contenu de `Dockerfile.runpod`

### Étape 3 : Déployer

1. **Lancer l'instance**
   - Cliquer sur **"Deploy"** ou **"Start"**
   - Attendre le build de l'image Docker (5-10 minutes)

2. **Attendre le chargement du modèle**
   - Le modèle Mistral 7B sera téléchargé depuis Hugging Face (~10-15 minutes)
   - Surveiller les logs pour voir la progression
   - Message attendu : `✅ Modèle Mistral 7B + LoRA chargé!`

3. **Récupérer l'URL publique**
   - Dans le dashboard Vast.ai → Votre instance → **"Connect"** ou **"Public URL"**
   - L'URL sera de type : `http://votre-instance.vast.ai:8000` ou `https://votre-instance.vast.ai:8000`
   - Notez cette URL pour la configuration du frontend

---

## 🧪 Tests des Endpoints

Une fois l'instance démarrée et le modèle chargé, tester les endpoints :

### Test 1 : Health Check

```bash
curl http://votre-instance.vast.ai:8000/health
```

**Réponse attendue :**
```json
{
  "status": "ok",
  "model": "Mistral 7B + LoRA",
  "gpu_available": true
}
```

### Test 2 : Initialisation

```bash
curl http://votre-instance.vast.ai:8000/init
```

**Réponse attendue :**
```json
{
  "greeting": "Bonjour ! Je suis Spinoza. Discutons :\n\n**La liberté est-elle une illusion ?**\n\nQu'en penses-tu ?",
  "history": [[null, "Bonjour ! Je suis Spinoza..."]]
}
```

### Test 3 : Chat

```bash
curl -X POST http://votre-instance.vast.ai:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Bonjour Spinoza, qu'\''est-ce que le conatus ?",
    "history": []
  }'
```

**Réponse attendue :**
```json
{
  "reply": "Le conatus est l'effort que chaque chose fait pour persévérer dans son être...",
  "history": [["Bonjour Spinoza...", "Le conatus est..."]]
}
```

### Test 4 : Évaluation (Maïeuthon)

```bash
curl -X POST http://votre-instance.vast.ai:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "dialogue": "Spinoza: Bonjour ! Je suis Spinoza. Discutons : La liberté est-elle une illusion ?\nÉlève: Je pense que oui, tout est déterminé.\nSpinoza: Tu dis que tout est déterminé... qu'\''est-ce que ça veut dire pour toi ?",
    "score_front": 55
  }'
```

**Réponse attendue :**
```json
{
  "score_final": 85,
  "message_final": "Ton effort pour comprendre tes propres affects est impressionnant...",
  "details_model": {
    "comprehension": 8,
    "cooperation": 9,
    "progression": 8,
    "total": 25
  }
}
```

### Script de Test Automatique

Vous pouvez utiliser le script existant `test_runpod_deployment.sh` :

```bash
chmod +x Backend/test_runpod_deployment.sh
./Backend/test_runpod_deployment.sh http://votre-instance.vast.ai:8000
```

---

## 💰 Coûts Estimés

### Par Heure
- **RTX 3090** : ~$0.20-0.40/h (~0.18-0.36€/h)
- **RTX 4090** : ~$0.40-0.60/h (~0.36-0.54€/h)

### Exemples de Coûts
- **3h de démo** : ~$0.60-1.20 (0.54-1.08€)
- **8h/jour pendant 1 mois** : ~$48-96 (43-86€)
- **Usage ponctuel (démos)** : Très économique

### Optimisation des Coûts
- **Arrêter l'instance** immédiatement après usage
- **Ne pas laisser tourner** en veille
- **Utiliser un GPU moins puissant** (RTX 3090 au lieu de RTX 4090) si acceptable

---

## 🔧 Configuration Avancée

### Variables d'Environnement Disponibles

| Variable | Description | Obligatoire | Défaut |
|----------|-------------|-------------|--------|
| `HF_TOKEN` | Token Hugging Face pour télécharger le modèle | ✅ Oui | - |
| `HUGGINGFACE_TOKEN` | Alias pour `HF_TOKEN` | ✅ Oui (si `HF_TOKEN` absent) | - |
| `PORT` | Port FastAPI | ❌ Non | `8000` |

### Ports et Réseau

- **Port interne** : 8000 (défini dans le Dockerfile)
- **Port externe** : Mappé automatiquement par Vast.ai
- **URL publique** : Générée automatiquement par Vast.ai

### Stockage Persistant (Optionnel)

Pour éviter de retélécharger le modèle à chaque démarrage :
- Utiliser un **Volume Disk persistant** dans Vast.ai
- Configurer le cache Hugging Face dans le volume
- **Coût supplémentaire** : ~$0.10-0.20/h pour le stockage

### Dockerfile avec CUDA Explicite (Optionnel)

Si vous rencontrez des problèmes de compatibilité CUDA, vous pouvez utiliser une image de base avec CUDA pré-installé :

```dockerfile
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Installer Python
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ... reste identique
```

**Note :** Généralement non nécessaire, Vast.ai fournit CUDA dans l'environnement.

---

## 🐛 Troubleshooting

### Le modèle ne charge pas

**Symptômes :** Erreur `ValueError: HF_TOKEN ou HUGGINGFACE_TOKEN doit être défini`

**Solutions :**
1. Vérifier que `HF_TOKEN` est bien configuré dans les variables d'environnement Vast.ai
2. Vérifier que le token a les permissions de lecture sur Hugging Face
3. Vérifier les logs de l'instance pour voir l'erreur exacte

### L'API ne répond pas

**Symptômes :** Timeout ou erreur de connexion

**Solutions :**
1. Vérifier que le port 8000 est bien exposé dans la configuration Vast.ai
2. Vérifier que l'instance est bien démarrée (status "Running")
3. Vérifier les logs pour voir si le serveur FastAPI a démarré
4. Tester avec `curl` directement depuis votre machine

### Erreur de mémoire (OOM)

**Symptômes :** `CUDA out of memory` dans les logs

**Solutions :**
1. Utiliser un GPU avec plus de VRAM (RTX 3090 24GB minimum)
2. Réduire `max_new_tokens` dans `app_runpod.py` (lignes 401, 449, 489)
3. Vérifier que la quantization 4-bit est bien activée (déjà fait dans le code)

### Le modèle est lent

**Symptômes :** Latence élevée (>10s par requête)

**Solutions :**
1. Vérifier que le GPU est bien utilisé (`gpu_available: true` dans `/health`)
2. Utiliser un GPU plus puissant (RTX 4090 au lieu de RTX 3090)
3. Voir les optimisations de latence dans la documentation

### Problème de compatibilité CUDA

**Symptômes :** Erreur `CUDA error` ou `bitsandbytes` ne fonctionne pas

**Solutions :**
1. **Vast.ai installe généralement CUDA automatiquement** - Le Dockerfile actuel devrait fonctionner
2. Si problème persiste, vérifier la version CUDA dans les logs : `nvidia-smi`
3. Vérifier que PyTorch détecte le GPU : `torch.cuda.is_available()` dans les logs
4. **Compatibilité confirmée** : T4 et RTX 3090 sont tous deux supportés par PyTorch 2.0+ et bitsandbytes 0.41.0+
5. Si nécessaire, utiliser une image Docker avec CUDA explicite (voir section Configuration Avancée)

**Note :** Le code utilise des APIs génériques (`torch.cuda.is_available()`, `device_map="auto"`) qui fonctionnent avec toutes les architectures NVIDIA récentes (Turing, Ampere, Ada).

---

## 📝 Mise à Jour du Frontend

Une fois l'URL Vast.ai obtenue, mettre à jour le frontend :

1. Ouvrir `Frontend/index_spinoza.html`
2. Modifier la ligne 120 :
   ```javascript
   const API_BASE_URL = 'http://votre-instance.vast.ai:8000';
   ```
3. Tester la connexion complète

**Voir le guide détaillé :** `Frontend/GUIDE_UPDATE_VAST_AI.md`

---

## 🔄 Mise à Jour et Maintenance

### Mettre à Jour le Code

1. Modifier les fichiers localement
2. Pousser sur GitHub (si déploiement depuis GitHub)
3. Redémarrer l'instance Vast.ai pour rebuild

### Mettre à Jour le Modèle

Le modèle sera retéléchargé à chaque démarrage si pas de volume persistant.

### Logs et Monitoring

- **Logs** : Accessibles dans le dashboard Vast.ai → Votre instance → Logs
- **Monitoring** : Utiliser `/health` pour vérifier l'état
- **Métriques** : Vast.ai fournit des métriques d'utilisation GPU

---

## 📚 Ressources Complémentaires

- **Documentation Vast.ai** : [docs.vast.ai](https://docs.vast.ai/)
- **Documentation Hugging Face** : [huggingface.co/docs](https://huggingface.co/docs)
- **Guide RunPod** (similaire) : `Backend/README_RUNPOD.md`
- **Architecture complète** : `docs/references/ARCHITECTURE_COMPLETE.md`

---

## ✅ Checklist de Déploiement

- [ ] Compte Vast.ai créé
- [ ] Token Hugging Face obtenu
- [ ] Instance Vast.ai créée avec GPU approprié
- [ ] Variables d'environnement configurées (`HF_TOKEN`, `PORT`)
- [ ] Dockerfile configuré (depuis GitHub ou direct)
- [ ] Instance démarrée et modèle chargé
- [ ] URL publique récupérée
- [ ] Tests des endpoints réussis (`/health`, `/init`, `/chat`, `/evaluate`)
- [ ] Frontend mis à jour avec la nouvelle URL
- [ ] Test complet frontend + backend réussi

---

**Dernière mise à jour :** Décembre 2024

