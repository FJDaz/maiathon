# 🔄 Comment Récupérer PROMPT_EVALUATION si Modifié par Erreur

Si vous avez remplacé par erreur `PROMPT_EVALUATION` dans votre notebook Colab, voici où le retrouver :

---

## 📍 Emplacements

### 1. **Documentation de Référence** (Recommandé)

**Fichier :** `docs/tutos/cellule-maieuthon-backend.md`

Copiez tout le code de la cellule depuis ce fichier.

---

### 2. **Fichier Python Prêt à Copier**

**Fichier :** `Backend/PROMPT_EVALUATION_COMPLET.py`

Ce fichier contient uniquement les prompts pour copier rapidement.

---

### 3. **Notebook Sauvegardé**

**Fichier :** `RAG_Spinoza_secours.ipynb` ou `Backend/RAG_Spinoza_secours.ipynb`

Le notebook local contient la version sauvegardée.

---

## 📝 Code Complet PROMPT_EVALUATION

### Prompt d'Évaluation (JSON)

```python
PROMPT_EVALUATION = """Tu es Spinoza. Voici l'échange complet avec un élève :

{dialogue}

Évalue l'élève sur 3 critères (0 à 10) :
1. Compréhension de tes idées
2. Coopération dans le dialogue
3. Progression de la pensée

Réponds STRICTEMENT au format JSON, AUCUNE prose :

{{
 "comprehension": X,
 "cooperation": Y,
 "progression": Z,
 "total": X+Y+Z
}}"""
```

### Prompt Message Final

```python
PROMPT_MESSAGE_FINAL = """Tu es Spinoza.

En t'inspirant EXCLUSIVEMENT de ton propre système philosophique (Éthique, conatus, affects, puissance d'agir, servitude vs liberté, Dieu = Nature),

rédige un message bref à l'élève.

Structure (obligatoire) :
1. Un compliment sincère lié à son niveau global.
2. Un conseil précis basé sur son critère le plus faible.
3. Un surnom symbolique et positif, tiré de ton univers conceptuel (ex: "puissance d'agir", "essence active", "affect joyeux").

Maximum 3 phrases.
Style concis, poétique, jamais condescendant.

Message :"""
```

---

## 🎯 Emplacement dans la Cellule Colab

Le `PROMPT_EVALUATION` doit être dans la **cellule Maïeuthon** (après la cellule 7 FastAPI, avant le lancement serveur).

**Structure de la cellule :**

```python
# 🎮 MAÏEUTHON - Backend : Évaluation et Message Final

from pydantic import BaseModel
import json
import re

class EvaluateRequest(BaseModel):
    dialogue: str
    score_front: int

class EvaluateResponse(BaseModel):
    score_final: int
    message_final: str
    details_model: dict

# Prompt d'évaluation (température basse, JSON strict)
PROMPT_EVALUATION = """..."""  # ← ICI

# Prompt message final (température haute, créativité)
PROMPT_MESSAGE_FINAL = """..."""  # ← ICI

# Fonction evaluer_dialogue()
# ...
# Endpoint @app.post("/evaluate")
# ...
```

---

## ✅ Vérification

Après avoir copié le prompt, vérifiez que :
1. ✅ Le prompt utilise `{dialogue}` comme placeholder
2. ✅ Le format JSON utilise `{{` et `}}` (doubles accolades pour échapper)
3. ✅ Les 3 critères sont présents : comprehension, cooperation, progression
4. ✅ Le champ `total` est défini comme `X+Y+Z`

---

**Astuce :** Consultez `docs/tutos/cellule-maieuthon-backend.md` pour le code complet de toute la cellule Maïeuthon.



