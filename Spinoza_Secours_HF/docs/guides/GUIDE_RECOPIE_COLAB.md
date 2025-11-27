# 📋 Guide de Recopie dans Colab

## 🎯 Fichiers à Recopier (dans l'ordre)

### 1. Évaluation Incrémentale
**Fichier** : `CELLULE_EVALUATION_INCREMENTALE.py`  
**Où** : Dans votre notebook Colab, **après la cellule API FastAPI** (cellule 7)  
**Contenu** : Crée l'endpoint `/evaluate/incremental`

### 2. Endpoint /evaluate Optimisé
**Fichier** : `ENDPOINT_EVALUATE_OPTIMISE.py`  
**Où** : Dans votre notebook Colab, **remplace l'endpoint `/evaluate` existant**  
**Contenu** : Version optimisée qui utilise les scores incrémentaux

### 3. Prompt Message Final (Bienveillant)
**Fichier** : `PROMPT_EVALUATION_FINAL.py` (lignes 98-122)  
**Où** : Dans votre notebook Colab, **remplace `PROMPT_MESSAGE_FINAL`**  
**Contenu** : Version bienveillante du prompt (pas "acide")

---

## 📝 Ordre d'Implémentation dans Colab

### Étape 1 : Ajouter l'Évaluation Incrémentale
```
1. Ouvrir CELLULE_EVALUATION_INCREMENTALE.py
2. Copier TOUT le contenu
3. Créer une nouvelle cellule dans Colab (après cellule API FastAPI)
4. Coller le code
5. Exécuter
```

**Résultat attendu** : `✅ Endpoint /evaluate/incremental créé pour évaluation au fil de l'eau`

---

### Étape 2 : Optimiser l'Endpoint /evaluate
```
1. Ouvrir ENDPOINT_EVALUATE_OPTIMISE.py
2. Copier TOUT le contenu
3. Dans Colab, trouver la cellule qui contient l'endpoint /evaluate actuel
4. Remplacer l'endpoint /evaluate par le code optimisé
5. Exécuter
```

**Résultat attendu** : `✅ Endpoint /evaluate optimisé (utilise scores incrémentaux si disponibles)`

---

### Étape 3 : Mettre à jour le Prompt Message Final
```
1. Ouvrir PROMPT_EVALUATION_FINAL.py
2. Copier les lignes 98-122 (PROMPT_MESSAGE_FINAL)
3. Dans Colab, trouver où PROMPT_MESSAGE_FINAL est défini
4. Remplacer par la version bienveillante
5. Exécuter
```

---

## 🔍 Comment Trouver les Cellules dans Colab

### Cellule API FastAPI
Cherchez dans votre notebook :
```python
@app.post("/chat")
def chat(req: ChatRequest):
    ...
```

### Cellule Endpoint /evaluate (actuel)
Cherchez dans votre notebook :
```python
@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest):
    ...
```

### Cellule PROMPT_MESSAGE_FINAL
Cherchez dans votre notebook :
```python
PROMPT_MESSAGE_FINAL = """Tu es Spinoza.
...
```

---

## ✅ Checklist de Vérification

Après recopie, vérifiez dans les logs Colab :

- [ ] `✅ Endpoint /evaluate/incremental créé pour évaluation au fil de l'eau`
- [ ] `✅ Endpoint /evaluate optimisé (utilise scores incrémentaux si disponibles)`
- [ ] Lors d'un dialogue complet, vous voyez dans les logs :
  - `📊 [OPTIMISATION] Utilisation des scores incrémentaux (2 évaluations)`
  - `📊 [OPTIMISATION] Scores agrégés: {...}`

---

## 📂 Emplacement des Fichiers

Tous les fichiers sont dans :
```
/Users/francois-jeandazin/bergsonAndFriends/Spinoza_Secours_HF/Backend/
```

Fichiers à recopier :
1. `CELLULE_EVALUATION_INCREMENTALE.py` → Code complet
2. `ENDPOINT_EVALUATE_OPTIMISE.py` → Code complet
3. `PROMPT_EVALUATION_FINAL.py` → Lignes 98-122 seulement

---

## 🚨 Points d'Attention

1. **Variable partagée** : Les deux endpoints doivent partager `incremental_scores`
   - Définie dans `CELLULE_EVALUATION_INCREMENTALE.py`
   - Utilisée dans `ENDPOINT_EVALUATE_OPTIMISE.py`

2. **Ordre d'exécution** : 
   - D'abord `CELLULE_EVALUATION_INCREMENTALE.py` (crée `incremental_scores`)
   - Ensuite `ENDPOINT_EVALUATE_OPTIMISE.py` (utilise `incremental_scores`)

3. **Frontend** : Déjà configuré dans `index_spinoza.html`
   - Appelle `/evaluate/incremental` tous les 2 échanges
   - Appelle `/evaluate` à la fin

