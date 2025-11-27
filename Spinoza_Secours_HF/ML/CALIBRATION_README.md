# 🎯 Calibration Maïeuthon - Guide d'Utilisation

**Script :** `calibrate_evaluator.py`  
**Documentation :** `../docs/references/calibration-evaluation.md`

---

## 📋 État Actuel

### ✅ Ce qui est en place

1. **Script de calibration** : `ML/calibrate_evaluator.py`
   - 5 avatars prédéfinis (bons, mauvais, moyens)
   - Dialogue réel intégré (avatar_2_medium)
   - Fonctions de comparaison et métriques

2. **Dialogues de référence** : `ML/dialogue-reel-1.txt`
   - Dialogue réel extrait des logs
   - Score frontend : 127
   - Utilisé pour créer l'avatar_2_medium

3. **Routine d'évaluation** : Backend `/evaluate`
   - Endpoint disponible dans `Backend/RAG_Spinoza_secours.ipynb`
   - Évalue sur 3 critères : Compréhension, Coopération, Progression

---

## 🚀 Lancer la Calibration

### Étape 1 : Vérifier que le Backend tourne

1. **Ouvrir** le notebook Colab `Backend/RAG_Spinoza_secours.ipynb`
2. **Exécuter** toutes les cellules jusqu'à l'endpoint `/evaluate`
3. **Récupérer** l'URL ngrok générée (ex: `https://xxx.ngrok-free.dev`)

### Étape 2 : Mettre à jour l'URL dans le script

Modifier la ligne 17 dans `calibrate_evaluator.py` :

```python
API_BASE_URL = "https://xxx.ngrok-free.dev"  # Remettre votre URL ngrok
ENDPOINT_EVALUATE = f"{API_BASE_URL}/evaluate"
```

### Étape 3 : Lancer le script

```bash
cd Spinoza_Secours_HF/ML
python calibrate_evaluator.py https://xxx.ngrok-free.dev/evaluate
```

**Ou sans argument** (utilise l'URL par défaut) :

```bash
python calibrate_evaluator.py
```

---

## 📊 Interpréter les Résultats

### Métriques affichées

Le script affiche :
- **Erreur moyenne** par critère (compréhension, coopération, progression)
- **Erreur max** par critère
- **Erreur totale** moyenne

### Seuil acceptable

- ✅ **Erreur < 2 points** : Calibration acceptable
- ⚠️ **Erreur 2-3 points** : Calibration à améliorer
- ❌ **Erreur > 3 points** : Ajustement nécessaire

### Recommandations automatiques

Le script propose des recommandations si l'erreur moyenne > 2 :
- ⚠️ Compréhension sous/sur-évaluée → Ajuster le prompt pour clarifier ce critère
- ⚠️ Coopération sous/sur-évaluée → Ajouter des exemples de coopération dans le prompt
- ⚠️ Progression sous/sur-évaluée → Clarifier la définition de la progression dans le prompt

---

## 📝 Résultats Sauvegardés

Le script sauvegarde automatiquement les résultats dans :
- **`calibration_results.json`** (dans le dossier ML/)

**Contenu :**
```json
{
  "metrics": {
    "mean_error_comprehension": 1.5,
    "mean_error_cooperation": 2.1,
    "mean_error_progression": 1.8,
    ...
  },
  "results": [
    {
      "avatar": {...},
      "generated": {...},
      "expected": {...},
      "errors": {...}
    },
    ...
  ]
}
```

---

## 🔧 Ajuster la Calibration

Si l'erreur est trop élevée, ajuster :

### 1. Le Prompt d'Évaluation

Modifier `PROMPT_EVALUATION` dans `Backend/RAG_Spinoza_secours.ipynb` :

```python
PROMPT_EVALUATION = """Tu es Spinoza. Voici l'échange complet avec un élève :

{dialogue}

Évalue l'élève sur 3 critères (0 à 10) :
1. Compréhension de tes idées (signes : reformule, pose des questions pertinentes, montre qu'il comprend)
2. Coopération dans le dialogue (signes : écoute, répond aux questions, ne résiste pas systématiquement)
3. Progression de la pensée (signes : fait des liens, avance dans sa réflexion, progresse)

[...]
"""
```

### 2. La Température

Dans `evaluer_dialogue()`, ajuster la température :
- **Température basse (0.1-0.2)** : Plus strict, moins de variation
- **Température haute (0.3-0.5)** : Plus flexible, plus de variation

### 3. Les Poids des Critères

Si un critère est systématiquement sous/sur-évalué, ajouter des exemples dans le prompt pour ce critère.

---

## 📋 Avatars Actuels

### Avatar 1 : Bon élève
- **Type :** good
- **Scores attendus :** Compréhension 9, Coopération 9, Progression 9, Total 27

### Avatar 2 : Dialogue réel (moyen)
- **Type :** medium
- **Scores attendus :** Compréhension 6, Coopération 7, Progression 7, Total 20
- **Dialogue :** Dialogue réel extrait des logs (dialogue-reel-1.txt)

### Avatar 3 : Mauvais élève
- **Type :** bad
- **Scores attendus :** Compréhension 1, Coopération 1, Progression 0, Total 2

### Avatar 4 : Excellent élève progressif
- **Type :** good
- **Scores attendus :** Compréhension 10, Coopération 10, Progression 10, Total 30

### Avatar 5 : Élève résistant
- **Type :** bad
- **Scores attendus :** Compréhension 4, Coopération 5, Progression 3, Total 12

---

## 🎯 Prochaines Étapes

1. **Lancer la calibration** avec le script actuel
2. **Analyser les résultats** et identifier les critères à ajuster
3. **Modifier les prompts** dans le notebook Colab si nécessaire
4. **Relancer la calibration** pour vérifier les améliorations
5. **Itérer** jusqu'à obtenir une erreur acceptable (< 2 points)

---

## 💡 Astuces

- **Tester avec un seul avatar d'abord** : Modifier le script pour ne tester qu'un avatar (ex: avatar_2_medium) pour valider rapidement
- **Ajouter des avatars** : Si besoin, ajouter plus d'avatars dans la liste `AVATARS` du script
- **Comparer avec les logs** : Utiliser les dialogues réels des logs pour créer de nouveaux avatars

---

**Prêt à lancer !** Il suffit de mettre à jour l'URL ngrok et de lancer le script.

