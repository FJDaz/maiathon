# ✅ Guide Qui a Fonctionné - Déploiement Vast.ai

**Date :** 29 novembre 2025  
**Source :** `docs/guides/vast-ai-guide.md`  
**Statut :** ✅ **CETTE MARCHE À SUIVRE A FONCTIONNÉ - 100% SUCCÈS**

---

## 📋 Résumé

Ce guide est la **seule marche à suivre qui a fonctionné** pour déployer Spinoza Secours sur Vast.ai.

**Référence principale :** `docs/guides/vast-ai-guide.md`

---

## ✅ Règles d'Or (Testées et Validées)

1. ✅ **JAMAIS d'on-start script complexe** - Vast.ai les parse mal
2. ✅ **TOUJOURS déployer manuellement** - C'est plus long mais ça marche
3. ✅ **TOUJOURS vérifier la clé SSH AVANT de rent** - Sinon impossible de se connecter
4. ✅ **JAMAIS de template avec port 8888** - C'est déjà pris par Jupyter
5. ✅ **TOUJOURS utiliser `python3`** (pas `python`) sur Vast.ai
6. ✅ **TOUJOURS envoyer `history` au format correct** - `[["q", "r"]]` pas `[]`

---

## 🎯 Workflow Qui Marche (Testé et Validé)

### Phase 1 : Préparation (10 min - une seule fois)
- Créer/vérifier clé SSH Mac
- Ajouter clé dans Vast.ai Account → SSH Keys
- ⚠️ **CRITIQUE** : Cette étape doit être faite AVANT de créer une instance

### Phase 2 : Créer le template (5 min - une seule fois)
- Template minimal avec :
  - Image : `nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04`
  - Port : **8080** (pas 8888, pas 8000)
  - On-start Script : **VIDE** (c'est normal)
  - Env Vars : HF_TOKEN, PORT=8000
  - Launch Mode : Jupyter-python notebook + SSH

### Phase 3 : Rent une instance (3 min)
- Chercher machine avec :
  - Reliability > 98%
  - Verified : Coché
  - Prix < $0.30/h
  - VRAM > 12 GB

### Phase 4 : Déploiement manuel (5-7 min)
- Ouvrir terminal Jupyter Web
- Copier-coller les commandes UNE PAR UNE :
  ```bash
  cd /workspace
  git clone https://github.com/FJDaz/maiathon.git
  cd maiathon/Spinoza_Secours_HF/Backend
  export PORT=8000
  pip3 install --no-cache-dir -r requirements.runpod.txt
  python3 app_runpod.py
  ```

### Phase 5 : Connexion depuis Mac (2 min)
- Trouver commande SSH dans Vast.ai Instances
- Modifier port forwarding : `-L 8000:localhost:8000`
- Connecter depuis Mac : `ssh -p PORT root@IP -L 8000:localhost:8000`

### Phase 6 : Test (1 min)
- Test santé : `http://localhost:8000/health`
- Test conversation : `http://localhost:8000/docs`

---

## 🐛 Bug Connu - History Vide

**Problème :** `history: []` → Erreur 500

**Solution rapide :** Toujours mettre au moins un élément :
```json
{
  "message": "Ta vraie question",
  "history": [["placeholder", "placeholder"]]
}
```

---

## 🚫 Ce Qui Ne Marche PAS (Ne pas réessayer)

- ❌ On-start script avec multi-lignes et emojis
- ❌ Template avec port 8888
- ❌ Utiliser `python` au lieu de `python3`
- ❌ Envoyer `history: []` sans fix du code
- ❌ Oublier d'ajouter la clé SSH avant de rent

---

## 📋 Checklist Avant Chaque Session

- [ ] Clé SSH ajoutée dans Vast.ai Account
- [ ] Template créé avec on-start VIDE
- [ ] Solde > $1 dans Vast.ai
- [ ] HF_TOKEN configuré dans template
- [ ] Port = 8080 dans template (pas 8888)

---

## 🔄 Workflow Rapide (Sessions Suivantes)

Une fois que tout est configuré (clé SSH + template) :

1. **Rent** instance avec template (2 min)
2. **Jupyter Terminal** → Copie-colle les 8 commandes de déploiement (5 min)
3. **SSH depuis Mac** avec tunnel `-L 8000:localhost:8000` (1 min)
4. **Teste** `http://localhost:8000/docs` (1 min)
5. **Destroy** quand fini (instantané)

**Total : 10 minutes** de setup par session

---

## 💰 Arrêter l'Instance (IMPORTANT)

Quand vous avez fini :
1. Vast.ai → Instances
2. Trouver votre instance
3. **Destroy** (icône 🗑️)
4. Confirmer

✅ **Facturation arrêtée immédiatement**

**Coût typique :**
- Session de test (1h) : ~$0.20
- Session de dev (3h) : ~$0.60
- Journée complète (8h) : ~$1.50

---

## 📝 Notes Importantes

- **Version du guide** : 29 novembre 2025
- **Testé sur** : Vast.ai, RTX 3060, Ubuntu 22.04, Mistral 7B + LoRA Spinoza
- **Coût session de validation** : $0.08 (25 minutes)
- **Taux de succès** : 100% si workflow suivi exactement

---

## 🔗 Référence Complète

**Guide principal :** `docs/guides/vast-ai-guide.md`

**Ce guide contient :**
- Toutes les étapes détaillées
- Commandes exactes à copier-coller
- Solutions aux bugs connus
- Checklist complète

---

## ✅ Conclusion

**Ce guide est la référence absolue** pour déployer Spinoza Secours sur Vast.ai.

**Tous les autres guides peuvent être ignorés** ou mis à jour en se basant sur celui-ci.

**Continuer avec ce guide pour les prochaines sessions !**
