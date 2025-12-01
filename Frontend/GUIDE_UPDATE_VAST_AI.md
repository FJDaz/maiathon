# Guide : Mise à Jour URL Backend Vast.ai

**Fichier à modifier :** `Frontend/index_spinoza.html`  
**Ligne :** 120

---

## Étape 1 : Obtenir l'URL Backend Vast.ai

Une fois votre instance Vast.ai démarrée :

1. **Dashboard Vast.ai** → **Instances** → Votre instance
2. Cliquer sur **"Connect"** ou **"Public URL"**
3. Récupérer l'URL complète

**Format d'URL Vast.ai :**
- `http://votre-instance.vast.ai:8000`
- ou `https://votre-instance.vast.ai:8000` (si HTTPS activé)

**Exemple :**
```
http://abc123def456.vast.ai:8000
```

---

## Étape 2 : Mettre à Jour le Frontend

### Option A : Modification Directe

1. Ouvrir `Frontend/index_spinoza.html`
2. Trouver la ligne 120 :
   ```javascript
   const API_BASE_URL = 'https://nonremunerative-rory-unbreakably.ngrok-free.dev';
   ```
3. Remplacer par votre URL Vast.ai :
   ```javascript
   const API_BASE_URL = 'http://votre-instance.vast.ai:8000';
   ```
4. Sauvegarder

### Option B : Configuration Dynamique (Recommandé)

Pour faciliter les changements futurs, vous pouvez utiliser une configuration dynamique :

```javascript
// Configuration API - Vast.ai
// ⚠️ REMPLACE par ton URL Vast.ai après déploiement
const API_BASE_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000'  // Développement local
  : 'http://votre-instance.vast.ai:8000';  // Production Vast.ai
```

Ou utiliser une variable d'environnement si vous hébergez le frontend :

```javascript
// Configuration API - Vast.ai
const API_BASE_URL = process.env.VAST_AI_URL || 'http://votre-instance.vast.ai:8000';
```

---

## Étape 3 : Tester la Connexion

### Test 1 : Test Local (Navigateur)

1. Ouvrir `Frontend/index_spinoza.html` dans un navigateur
2. Ouvrir la console développeur (F12)
3. Vérifier qu'il n'y a pas d'erreurs CORS
4. Tester un échange complet avec Spinoza

### Test 2 : Test avec curl

```bash
# Test health check
curl http://votre-instance.vast.ai:8000/health

# Test init
curl http://votre-instance.vast.ai:8000/init

# Test chat
curl -X POST http://votre-instance.vast.ai:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Bonjour", "history": []}'
```

### Test 3 : Test Complet Frontend

1. Ouvrir `index_spinoza.html`
2. Cliquer sur "Commencer"
3. Vérifier que la question initiale de Spinoza s'affiche
4. Envoyer une réponse
5. Vérifier que Spinoza répond
6. Compléter les 5 échanges
7. Vérifier que le Maïeuthon fonctionne (score + message final)

---

## Étape 4 : Mise à Jour sur le Serveur

Si le frontend est hébergé sur `fjdaz.com` ou un autre serveur :

1. **Méthode 1 : FTP/SFTP**
   - Se connecter au serveur
   - Remplacer `index_spinoza.html` par la version mise à jour

2. **Méthode 2 : Git**
   - Committer les changements
   - Pousser sur le dépôt
   - Si déploiement automatique, attendre le déploiement

3. **Méthode 3 : Interface d'hébergement**
   - Utiliser l'interface de votre hébergeur
   - Uploader le fichier mis à jour

---

## 🔧 Configuration CORS

Si vous rencontrez des erreurs CORS, vérifier que le backend autorise votre domaine :

Dans `app_runpod.py`, ligne 543 :
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Pour la production, remplacer `["*"]` par votre domaine :
```python
allow_origins=["https://fjdaz.com", "https://www.fjdaz.com"]
```

---

## 🐛 Troubleshooting

### Erreur CORS

**Symptôme :** `Access to fetch at '...' from origin '...' has been blocked by CORS policy`

**Solution :**
1. Vérifier que `allow_origins` dans le backend inclut votre domaine
2. Vérifier que l'URL backend est correcte (http vs https)
3. Vérifier que le backend est bien démarré

### Erreur de Connexion

**Symptôme :** `Failed to fetch` ou `Network error`

**Solutions :**
1. Vérifier que l'instance Vast.ai est bien démarrée
2. Vérifier que l'URL est correcte (pas de typo)
3. Vérifier que le port 8000 est bien exposé
4. Tester avec `curl` pour isoler le problème

### Le Maïeuthon ne fonctionne pas

**Symptôme :** Le score ne s'affiche pas ou l'évaluation finale échoue

**Solutions :**
1. Vérifier les logs du backend (dashboard Vast.ai)
2. Vérifier que l'endpoint `/evaluate` répond correctement
3. Ouvrir la console développeur pour voir les erreurs JavaScript
4. Vérifier que le format des données correspond à ce que le frontend attend

---

## 📝 Notes Importantes

- **URL temporaire** : L'URL Vast.ai peut changer si vous recréez l'instance
- **HTTPS** : Si vous utilisez HTTPS pour le frontend, vérifier que le backend supporte HTTPS ou utiliser un proxy
- **Cache** : Vider le cache du navigateur après modification si les changements ne s'affichent pas

---

## ✅ Checklist

- [ ] URL Vast.ai obtenue
- [ ] `index_spinoza.html` modifié (ligne 120)
- [ ] Test local réussi (console sans erreurs)
- [ ] Test complet frontend + backend réussi
- [ ] Maïeuthon fonctionne (score + évaluation finale)
- [ ] Frontend mis à jour sur le serveur (si hébergé)
- [ ] Test en production réussi

---

**Dernière mise à jour :** Décembre 2024


