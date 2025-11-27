# Guide : Option 1 - Déblocage GitHub (RAPIDE)

**Date :** 27 novembre 2025  
**Problème :** Push bloqué par GitHub Push Protection (token détecté dans l'historique)  
**Solution :** Utiliser l'URL de déblocage GitHub pour autoriser le push une fois

---

## 🎯 Étapes à Suivre

### Étape 1 : Ouvrir l'URL de Déblocage

**URL de déblocage :**  
https://github.com/FJDaz/Spinoza_secours/security/secret-scanning/unblock-secret/364eOrgypCLFzo1HHosOFUljHi3

1. Ouvrez cette URL dans votre navigateur
2. Connectez-vous à GitHub si nécessaire
3. Lisez l'avertissement sur le secret détecté

### Étape 2 : Vérifier le Token

**Token détecté :** GitHub Personal Access Token  
**Fichier :** `Spinoza_Secours_HF/RAG_Spinoza_secours.ipynb` (ligne 1383)  
**Commit :** `d90601c060f9a566bf52848021612b64a8436b67`

**⚠️ IMPORTANT :**
- Si le token est encore actif → **RÉVOQUER** immédiatement sur https://github.com/settings/tokens
- Si le token est déjà révoqué → Vous pouvez autoriser le push

### Étape 3 : Autoriser le Push

1. Sur la page de déblocage GitHub :
   - Cochez "I understand the risks"
   - Cliquez sur "Allow this secret" ou "Autoriser ce secret"
   - Notez que c'est une autorisation **temporaire** (une seule fois)

2. **Alternative :** Si vous préférez révoquer le token :
   - Allez sur https://github.com/settings/tokens
   - Trouvez le token concerné
   - Cliquez sur "Revoke"
   - Retournez sur l'URL de déblocage et autorisez

### Étape 4 : Préparer le Push

Une fois le déblocage autorisé, préparez vos fichiers :

```bash
cd /Users/francois-jeandazin/bergsonAndFriends/Spinoza_Secours_HF

# Vérifier l'état actuel
git status

# Vérifier qu'il n'y a pas de nouveaux secrets
grep -r -E "(HF_TOKEN|NGROK_TOKEN|GITHUB_TOKEN|ghp_[0-9a-zA-Z]{36})" \
  Backend/Dockerfile.runpod Backend/app_runpod.py Backend/requirements.runpod.txt \
  --exclude-dir=.git --exclude-dir=venv --exclude-dir=__pycache__ || echo "✅ Aucun secret détecté"
```

### Étape 5 : Effectuer le Push

```bash
# Vérifier la branche actuelle
git branch --show-current

# Si vous êtes sur une branche locale, pousser vers github/main
git push github <votre-branche>:main --force

# OU si vous êtes déjà sur la branche main locale
git push github main --force
```

---

## ⚠️ Limitations

- **Autorisation temporaire :** Cette autorisation ne fonctionne qu'**une seule fois**
- **Token toujours présent :** Le token reste dans l'historique Git (mais révoqué)
- **Solution temporaire :** Pour une solution permanente, utiliser Option 2 (BFG)

---

## 🔄 Si le Push Échoue Encore

1. **Vérifier que le déblocage a été effectué :**
   - Retournez sur l'URL de déblocage
   - Vérifiez que le statut indique "Allowed" ou "Autorisé"

2. **Vérifier qu'il n'y a pas d'autres secrets :**
   ```bash
   git show HEAD | grep -E "(ghp_|HF_TOKEN|NGROK_TOKEN)" | head -5
   ```

3. **Si d'autres secrets sont détectés :**
   - Répétez le processus pour chaque secret
   - OU passez à l'Option 2 (BFG) pour nettoyer tout l'historique

---

## 📝 Notes

- Cette méthode est **rapide** mais **temporaire**
- Le token reste dans l'historique Git (mais est révoqué)
- Pour un nettoyage complet, utiliser l'Option 2 (BFG Repo-Cleaner)

---

## 🔗 Liens Utiles

- **URL de déblocage :** https://github.com/FJDaz/Spinoza_secours/security/secret-scanning/unblock-secret/364eOrgypCLFzo1HHosOFUljHi3
- **Gestion des tokens GitHub :** https://github.com/settings/tokens
- **Documentation GitHub Push Protection :** https://docs.github.com/code-security/secret-scanning/working-with-secret-scanning-and-push-protection

