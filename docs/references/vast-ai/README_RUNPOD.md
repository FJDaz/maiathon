# Guide de Déploiement RunPod/Vast.ai - Spinoza Secours

**Modèle :** Mistral 7B + LoRA  
**Budget :** 20€ maximum  
**Usage :** Ponctuel (démos/sessions)

---

## Fichiers Créés

1. **`Dockerfile.runpod`** - Configuration Docker pour RunPod/Vast.ai
2. **`app_runpod.py`** - Application FastAPI complète (tous endpoints)
3. **`requirements.runpod.txt`** - Dépendances Python

---

## Déploiement sur RunPod

### Prérequis

1. **Compte RunPod** avec crédit (vérifier dépôt minimum)
2. **Token Hugging Face** pour télécharger le modèle
3. **GitHub** (optionnel, pour déployer depuis repo)

### Étapes

1. **Créer un Template RunPod**
   - Dashboard RunPod → Templates → Create Template
   - Name : `spinoza-secours-mistral7b`
   - Source : GitHub repo ou Dockerfile
   - Dockerfile : Utiliser `Dockerfile.runpod`

2. **Créer un Pod**
   - GPU : T4 (16GB) ou RTX 3090 (24GB)
   - Container Disk : 50GB minimum
   - Port : 8000 (mappé automatiquement)
   - Environment Variables :
     - `HF_TOKEN` : Votre token Hugging Face
     - `PORT` : 8000

3. **Attendre le démarrage**
   - Build : 5-10 minutes
   - Chargement modèle : 5-10 minutes
   - Total : ~15-20 minutes

4. **Récupérer l'URL publique**
   - Dashboard → Pods → Votre pod → Connect
   - URL type : `https://abc123xyz-8000.proxy.runpod.net`

---

## Déploiement sur Vast.ai

### Prérequis

1. **Compte Vast.ai** (généralement pas de dépôt minimum)
2. **Token Hugging Face**

### Étapes

1. **Créer une instance**
   - GPU : RTX 3090 ou équivalent
   - Image : Docker custom
   - Dockerfile : Utiliser `Dockerfile.runpod`

2. **Configurer les variables d'environnement**
   - `HF_TOKEN` : Votre token Hugging Face
   - `PORT` : 8000

3. **Déployer et récupérer l'URL**

---

## Test des Endpoints

Une fois le pod démarré, tester :

```bash
# Health check
curl https://votre-url.proxy.runpod.net/health

# Init
curl https://votre-url.proxy.runpod.net/init

# Chat
curl -X POST https://votre-url.proxy.runpod.net/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Bonjour Spinoza", "history": []}'

# Evaluate
curl -X POST https://votre-url.proxy.runpod.net/evaluate \
  -H "Content-Type: application/json" \
  -d '{"dialogue": "Spinoza: ...\nÉlève: ...", "score_front": 50}'
```

---

## Mise à Jour du Frontend

Une fois l'URL backend obtenue :

1. Modifier `Frontend/index_spinoza.html` ligne 120
2. Remplacer :
   ```javascript
   const API_BASE_URL = 'https://votre-url.proxy.runpod.net';
   ```
3. Tester la connexion complète

---

## Coûts Estimés

### RunPod
- **T4** : ~$0.30/h = ~0.27€/h
- **3h de démo** : ~0.81€
- **Dépôt minimum** : À vérifier (peut être $100)

### Vast.ai
- **RTX 3090** : ~$0.20-0.40/h = ~0.18-0.36€/h
- **3h de démo** : ~0.54-1.08€
- **Dépôt minimum** : Généralement 0€

---

## Troubleshooting

### Le modèle ne charge pas
- Vérifier que `HF_TOKEN` est bien configuré
- Vérifier la VRAM disponible (logs)
- Essayer un GPU avec plus de VRAM

### L'API ne répond pas
- Vérifier que le port 8000 est bien mappé
- Vérifier les logs du pod
- Tester directement l'URL dans un navigateur

### Erreur de mémoire
- Réduire `max_new_tokens` dans `app_runpod.py`
- Utiliser un GPU avec plus de VRAM

---

## Notes Importantes

- Le modèle sera téléchargé à chaque démarrage (10 min)
- Pour éviter ça, utiliser un Volume Disk persistant (coût supplémentaire)
- Pour usage ponctuel, le retéléchargement est acceptable

---

**Dernière mise à jour :** Décembre 2024


