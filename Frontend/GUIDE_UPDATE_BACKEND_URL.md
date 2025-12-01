# Guide : Mise à Jour URL Backend

**Fichier à modifier :** `Frontend/index_spinoza.html`  
**Ligne :** 120

---

## Étape 1 : Obtenir l'URL Backend

Une fois votre pod RunPod/Vast.ai démarré :

1. **RunPod** : Dashboard → Pods → Votre pod → Connect
2. **Vast.ai** : Dashboard → Instances → Votre instance → URL publique

L'URL sera de type :
- RunPod : `https://abc123xyz-8000.proxy.runpod.net`
- Vast.ai : `https://votre-instance.vast.ai:8000`

---

## Étape 2 : Mettre à Jour le Frontend

1. Ouvrir `Frontend/index_spinoza.html`
2. Trouver la ligne 120 :
   ```javascript
   const API_BASE_URL = 'https://nonremunerative-rory-unbreakably.ngrok-free.dev';
   ```
3. Remplacer par votre nouvelle URL :
   ```javascript
   const API_BASE_URL = 'https://abc123xyz-8000.proxy.runpod.net';
   ```
4. Sauvegarder

---

## Étape 3 : Tester

1. Ouvrir `index_spinoza.html` dans un navigateur
2. Vérifier que la connexion fonctionne
3. Tester un échange complet
4. Vérifier que le Maïeuthon fonctionne

---

## Note

Le frontend est déjà hébergé sur `fjdaz.com`. Si vous modifiez le fichier local, vous devrez également mettre à jour le fichier sur le serveur `fjdaz.com`.


