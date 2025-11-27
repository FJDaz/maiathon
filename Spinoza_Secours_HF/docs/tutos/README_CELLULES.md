# 📚 Guide des Cellules Colab - Spinoza Secours

**Résumé :** Fichiers de référence pour les cellules du notebook Colab

---

## 🎯 Structure des Cellules

Le notebook `Backend/RAG_Spinoza_secours.ipynb` est organisé en cellules :

1. **Cellule 1** : Installation Dépendances
2. **Cellule 2** : Imports + Configuration
3. **Cellule 3** : Prompt Système Hybride
4. **Cellule 4** : Détection Contexte + Post-Processing
5. **Cellule 5** : Chargement Modèle
6. **Cellule 6** : Fonction spinoza_repond()
7. **Cellule 7** : API FastAPI + ngrok
8. **Cellule Maïeuthon** : `/evaluate` (évaluation finale)
9. **Cellule Évaluation Incrémentale** : `/evaluate/incremental` ⬅️ **À AJOUTER**
10. **Cellule 8** : Lancement Serveur + ngrok

---

## 📁 Fichiers de Référence

### Code Brut (Prêt à Copier-Coller)

**Dans `Backend/` :**
- `CELLULE_EVALUATION_INCREMENTALE.py` ⬅️ **Code à copier pour cellule 9**

### Documentation

**Dans `docs/tutos/` :**
- `cellule-evaluation-incrementale.md` ⬅️ **Tuto avec code + instructions**
- `cellule-maieuthon-backend.md` ⬅️ **Tuto cellule Maïeuthon (déjà ajoutée)**

---

## 🔍 Différence Entre les Fichiers

### `Backend/CELLULE_EVALUATION_INCREMENTALE.py`

**Format :** Code Python brut  
**Usage :** Copier-coller directement dans Colab  
**Contenu :** Code uniquement (pas de documentation)

### `docs/tutos/cellule-evaluation-incrementale.md`

**Format :** Documentation Markdown  
**Usage :** Lire les instructions et comprendre le code  
**Contenu :** 
- Code dans bloc markdown (```python)
- Instructions d'ajout
- Explications
- Vérification

**⚠️ Important :** C'est **le même code** dans les deux fichiers, juste des formats différents !

---

## ✅ Recommandation

**Pour ajouter la cellule dans Colab :**

1. **Ouvrir** `Backend/CELLULE_EVALUATION_INCREMENTALE.py` (code brut, facile à copier)
2. **Copier tout le contenu**
3. **Coller** dans une nouvelle cellule Colab
4. **Exécuter**

**Ou** lire `docs/tutos/cellule-evaluation-incrementale.md` pour les instructions détaillées (le code est dedans aussi).

---

**Les deux fichiers contiennent le même code, juste des formats différents !**



