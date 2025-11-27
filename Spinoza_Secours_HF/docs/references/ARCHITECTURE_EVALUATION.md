# 🏗️ Architecture Évaluation - Vue d'Ensemble

## 📋 Les Deux Endpoints

### 1. `/evaluate/incremental` (Évaluation Incrémentale)
- **Créé par** : `CELLULE_EVALUATION_INCREMENTALE.py`
- **Appelé** : Tous les 2 échanges (échanges 2, 4)
- **Frontend** : `handleIncrementalEvaluation()` dans `index_spinoza.html`
- **Objectif** : Évaluer rapidement les 2 derniers échanges
- **Stockage** : Scores stockés dans `incremental_scores[dialogue_id]`
- **Visibilité** : Invisible à l'utilisateur (en arrière-plan)
- **Charge** : Légère (prompt court, 2 derniers échanges seulement)

### 2. `/evaluate` (Évaluation Finale)
- **Créé par** : Code dans la cellule Maïeuthon (actuellement `evaluer_dialogue()`)
- **Appelé** : Une fois à la fin (échange 5)
- **Frontend** : `endGame()` dans `index_spinoza.html`
- **Objectif** : Évaluer le dialogue complet et générer le message final
- **Optimisation** : Devrait utiliser les scores incrémentaux si disponibles
- **Visibilité** : Visible (loader + résultats)
- **Charge** : Lourde (dialogue complet) → **À optimiser avec scores incrémentaux**

---

## 🔄 Flux Complet (Système Hybride Optimisé)

### Étape 1 : Échanges 1-2
```
Utilisateur → Spinoza (échange 1)
Spinoza → Utilisateur (échange 2)
```

### Étape 2 : Évaluation Incrémentale #1 (Échange 2)
```
Frontend : handleIncrementalEvaluation()
  ↓
POST /evaluate/incremental
  ↓
Backend : Évalue les 2 derniers échanges
  ↓
Stocke dans incremental_scores[dialogue_id][0]
  ↓
Retourne {scores: {...}, exchange_count: 1}
```

### Étape 3 : Échanges 3-4
```
Utilisateur → Spinoza (échange 3)
Spinoza → Utilisateur (échange 4)
```

### Étape 4 : Évaluation Incrémentale #2 (Échange 4)
```
Frontend : handleIncrementalEvaluation()
  ↓
POST /evaluate/incremental
  ↓
Backend : Évalue les 2 derniers échanges
  ↓
Stocke dans incremental_scores[dialogue_id][1]
  ↓
Retourne {scores: {...}, exchange_count: 2}
```

### Étape 5 : Échange 5 (Dernier)
```
Utilisateur → Spinoza (échange 5)
Spinoza → Utilisateur (dernière réponse)
  ↓
Frontend : Affiche loader "Le jury délibère..."
  ↓
Frontend : endGame()
```

### Étape 6 : Évaluation Finale (Optimisée)
```
POST /evaluate
  ↓
Backend : Vérifie incremental_scores[dialogue_id]
  ↓
Si scores incrémentaux existent :
  ├─ Agrège les scores (moyenne pondérée)
  ├─ Génère SEULEMENT le message final
  └─ Retourne {score_final, message_final, details_model}
  ↓
Sinon (fallback) :
  ├─ Évaluation complète normale
  └─ Retourne {score_final, message_final, details_model}
  ↓
Frontend : Affiche les résultats
```

---

## 📊 Charge Modèle (Comparaison)

### ❌ Système Actuel (Non Optimisé)
```
Échange 2 : /evaluate/incremental → 1 appel modèle
Échange 4 : /evaluate/incremental → 1 appel modèle
Échange 5 : /evaluate → 2 appels modèle (scores + message)
─────────────────────────────────────────────────
Total : 4 appels modèle
```

### ✅ Système Optimisé (Avec ENDPOINT_EVALUATE_OPTIMISE.py)
```
Échange 2 : /evaluate/incremental → 1 appel modèle
Échange 4 : /evaluate/incremental → 1 appel modèle
Échange 5 : /evaluate → 1 appel modèle (message seulement, scores agrégés)
─────────────────────────────────────────────────
Total : 3 appels modèle (gain de 25%)
```

---

## 🔧 Fichiers Clés

### Backend (Colab)
- `CELLULE_EVALUATION_INCREMENTALE.py` → Crée `/evaluate/incremental`
- `ENDPOINT_EVALUATE_OPTIMISE.py` → Remplace `/evaluate` (à copier dans Colab)
- `FONCTION_EVALUER_DIALOGUE_ADAPTEE.py` → Version actuelle (non optimisée)

### Frontend
- `index_spinoza.html` :
  - `handleIncrementalEvaluation()` → Appelle `/evaluate/incremental`
  - `endGame()` → Appelle `/evaluate`
  - `showEvaluationLoader()` → Affiche le loader

---

## ✅ Checklist d'Implémentation

- [x] Frontend : Appel `/evaluate/incremental` tous les 2 échanges
- [x] Frontend : Appel `/evaluate` à la fin
- [x] Frontend : Loader visible pour l'évaluation finale
- [ ] Backend : Endpoint `/evaluate/incremental` créé (dans Colab)
- [ ] Backend : Endpoint `/evaluate` optimisé (utilise scores incrémentaux)
- [ ] Backend : Vérifier que `incremental_scores` est partagé entre les deux endpoints

---

## 🎯 Prochaines Étapes

1. **Copier `ENDPOINT_EVALUATE_OPTIMISE.py` dans votre Colab**
2. **Remplacer l'endpoint `/evaluate` actuel** par le code optimisé
3. **Tester** : Vérifier dans les logs Colab que les scores incrémentaux sont utilisés
4. **Vérifier la latence** : L'évaluation finale devrait être plus rapide

