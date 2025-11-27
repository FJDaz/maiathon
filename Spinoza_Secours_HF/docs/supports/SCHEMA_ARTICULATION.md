# 🔗 Schéma d'Articulation des Deux Systèmes

## ❌ On ne merge PAS, on COLLABORE

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (index_spinoza.html)            │
└─────────────────────────────────────────────────────────────┘
                            │
                            │
        ┌───────────────────┴───────────────────┐
        │                                         │
        ▼                                         ▼
┌───────────────────────┐              ┌───────────────────────┐
│ /evaluate/incremental │              │      /evaluate        │
│ (Échanges 2, 4)       │              │    (Échange 5)        │
└───────────────────────┘              └───────────────────────┘
        │                                         │
        │ Utilise                                  │ Vérifie
        │ PROMPT_EVALUATION_INCREMENTAL            │ incremental_scores
        │ (court, 2 derniers échanges)            │
        │                                         │
        ▼                                         │
┌───────────────────────┐                        │
│ Évalue 2 échanges    │                        │
│ Stocke dans           │                        │
│ incremental_scores    │                        │
│ [dialogue_id]         │                        │
└───────────────────────┘                        │
        │                                         │
        │                                         │
        └─────────────────┬───────────────────────┘
                          │
                          │ Si scores existent :
                          │ ├─ Agrège les scores (PAS d'appel modèle)
                          │ └─ Génère message (PROMPT_MESSAGE_FINAL)
                          │
                          │ Si pas de scores :
                          │ └─ Évaluation complète (PROMPT_EVALUATION)
                          │
                          ▼
                  ┌───────────────┐
                  │   Résultats   │
                  │   Finaux      │
                  └───────────────┘
```

---

## 📋 Détail des Prompts Utilisés

### Endpoint `/evaluate/incremental`
```
Prompt : PROMPT_EVALUATION_INCREMENTAL
├─ Court (2 derniers échanges seulement)
├─ Pas de prompt système complexe
└─ Retourne : {comprehension, cooperation, progression, total}
```

### Endpoint `/evaluate` (Optimisé)

#### Si scores incrémentaux disponibles :
```
❌ PAS de PROMPT_EVALUATION (scores déjà calculés)
✅ SEULEMENT PROMPT_MESSAGE_FINAL (génère le message)
```

#### Si pas de scores incrémentaux (fallback) :
```
✅ PROMPT_EVALUATION (évaluation complète)
✅ PROMPT_MESSAGE_FINAL (message final)
```

---

## 🔑 Réponses aux Questions

### ❓ "Tu merges les deux ?"
**NON** : Les deux endpoints restent **séparés** mais **collaborent** via `incremental_scores`.

### ❓ "Tu mets le prompt système dans incrémentale ?"
**NON** : 
- L'incrémentale utilise `PROMPT_EVALUATION_INCREMENTAL` (court, simple)
- Le prompt système complet (`PROMPT_EVALUATION`) est utilisé **seulement** en fallback dans `/evaluate`

### ✅ Comment ça marche alors ?

1. **`/evaluate/incremental`** :
   - Prompt court (`PROMPT_EVALUATION_INCREMENTAL`)
   - Évalue 2 derniers échanges
   - Stocke dans `incremental_scores[dialogue_id]`

2. **`/evaluate`** :
   - Vérifie `incremental_scores[dialogue_id]`
   - **Si existe** : Agrège les scores (calcul Python, pas d'appel modèle) + génère message
   - **Si n'existe pas** : Utilise `PROMPT_EVALUATION` (évaluation complète)

---

## 💡 Exemple Concret

### Échange 2
```
Frontend → POST /evaluate/incremental
Backend :
  ├─ PROMPT_EVALUATION_INCREMENTAL
  ├─ Évalue échanges 1-2
  ├─ Stocke : incremental_scores[hash][0] = {scores: {comp: 6, coop: 7, prog: 5}}
  └─ Retourne : {scores: {comp: 6, coop: 7, prog: 5}}
```

### Échange 4
```
Frontend → POST /evaluate/incremental
Backend :
  ├─ PROMPT_EVALUATION_INCREMENTAL
  ├─ Évalue échanges 3-4
  ├─ Stocke : incremental_scores[hash][1] = {scores: {comp: 8, coop: 9, prog: 7}}
  └─ Retourne : {scores: {comp: 8, coop: 9, prog: 7}}
```

### Échange 5 (Final)
```
Frontend → POST /evaluate
Backend :
  ├─ Vérifie incremental_scores[hash]
  ├─ Trouve 2 scores : [{comp: 6, coop: 7, prog: 5}, {comp: 8, coop: 9, prog: 7}]
  ├─ Agrège (pondéré) : {comp: 7, coop: 8, prog: 6} → PAS d'appel modèle
  ├─ Génère message : PROMPT_MESSAGE_FINAL → 1 appel modèle
  └─ Retourne : {score_final: 85, message_final: "...", details_model: {...}}
```

**Résultat** : 3 appels modèle au total (au lieu de 4)

