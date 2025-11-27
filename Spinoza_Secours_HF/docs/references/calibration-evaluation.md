# 🎯 Calibration de la Routine d'Évaluation Maïeuthon

**Objectif :** Calibrer les critères d'évaluation en utilisant des dialogues exemples avec scores de référence (ground truth).

---

## 📋 Concept

1. **Prendre 1-2 dialogues réels** (dans les logs ou fournis manuellement)
2. **Créer des "avatars"** (variantes) de ces dialogues avec scores de référence :
   - ✅ **Pertinents/bons** : Dialogues où l'élève comprend, coopère, progresse
   - ❌ **Mauvais** : Dialogues où l'élève ne comprend pas, ne coopère pas, régresse
3. **Soumettre ces avatars** à la routine d'évaluation `/evaluate`
4. **Comparer** les scores générés vs scores attendus
5. **Ajuster les paramètres** (température, prompts, poids des critères) pour calibrer

---

## 📝 Format des Données de Calibration

### Structure d'un Avatar de Dialogue

```python
{
    "id": "avatar_1_good",
    "dialogue": "Spinoza: Bonjour ! La liberté est-elle une illusion ?\nÉlève: Je pense que oui, car on est toujours contraint.\nSpinoza: Mais qu'est-ce que la contrainte ?\nÉlève: C'est quand on ne peut pas faire ce qu'on veut.\nSpinoza: Et la connaissance des causes, est-ce une contrainte ?\nÉlève: Hmm... Non, ça libère plutôt, non ?",
    "score_front": 85,  # Score calculé côté frontend
    "expected_scores": {  # Scores de référence (ground truth)
        "comprehension": 8,
        "cooperation": 9,
        "progression": 8,
        "total": 25
    },
    "type": "good"  # ou "bad"
}
```

---

## 🔧 Script de Calibration

### Fonctionnalités

1. **Charger des dialogues exemples** (1-2 dialogues réels)
2. **Générer des avatars** :
   - Bon élève : Comprend, coopère, progresse
   - Mauvais élève : Ne comprend pas, résiste, régresse
   - Élève moyen : Mix des deux
3. **Évaluer chaque avatar** avec `/evaluate`
4. **Comparer** scores générés vs attendus
5. **Ajuster** les paramètres pour minimiser l'erreur

---

## 📊 Métriques de Calibration

- **Erreur moyenne** : Différence entre scores générés et attendus
- **Erreur par critère** : Erreur sur chaque critère (compréhension, coopération, progression)
- **Corrélation** : Corrélation entre scores générés et attendus
- **Précision** : Pourcentage de scores dans une marge acceptable (±2 points)

---

## 🎯 Processus de Calibration

### Étape 1 : Collecter Dialogues Exemples

Prendre 1-2 dialogues réels de logs ou fournis manuellement.

### Étape 2 : Créer Avatars avec Scores de Référence

Pour chaque dialogue, créer 3-5 avatars :
- 2 bons (excellente compréhension, coopération, progression)
- 2 mauvais (faible compréhension, résistance, pas de progression)
- 1 moyen (mix)

### Étape 3 : Évaluer avec Routine Actuelle

Soumettre chaque avatar à `/evaluate` et récupérer les scores générés.

### Étape 4 : Calculer Erreurs

Comparer scores générés vs scores attendus pour chaque critère.

### Étape 5 : Ajuster Paramètres

Ajuster :
- **Prompt d'évaluation** : Clarifier les critères, ajouter des exemples
- **Température** : Ajuster entre 0.1 (strict) et 0.3 (plus flexible)
- **Poids des critères** : Si un critère est sous/ sur-évalué

### Étape 6 : Itérer

Répéter jusqu'à obtenir une erreur acceptable (< 2 points par critère).

---

## 📝 Exemple de Dialogue de Référence

### Dialogue 1 : Bon Élève

```
Spinoza: Bonjour ! La liberté est-elle une illusion ?
Élève: Je pense que oui, car on est toujours contraint par quelque chose.
Spinoza: Mais qu'est-ce que la contrainte pour toi ?
Élève: C'est quand on ne peut pas faire ce qu'on veut, quand quelque chose nous empêche.
Spinoza: Et si je te disais que connaître les causes, c'est aussi une forme de contrainte ?
Élève: Hmm... Mais si on connaît les causes, on peut agir mieux, non ? C'est plutôt libérant ?
Spinoza: Exactement ! Connaître la nécessité, c'est la liberté.
Élève: Ah ! Donc liberté = connaissance de la nécessité ?
```

**Scores attendus :**
- Compréhension : 9/10 (comprend progressivement)
- Coopération : 9/10 (questionne, reformule)
- Progression : 9/10 (passe de "liberté = illusion" à "liberté = connaissance")
- Total : 27/30

### Dialogue 2 : Mauvais Élève

```
Spinoza: Bonjour ! La liberté est-elle une illusion ?
Élève: Ouais, je sais pas.
Spinoza: Que penses-tu de la contrainte ?
Élève: J'ai pas envie de réfléchir.
Spinoza: Pourquoi ?
Élève: C'est trop compliqué, j'ai autre chose à faire.
```

**Scores attendus :**
- Compréhension : 2/10 (ne comprend pas, ne s'engage pas)
- Coopération : 2/10 (résiste, refuse)
- Progression : 1/10 (aucune progression)
- Total : 5/30

---

## 🛠️ Implémentation

**Script à créer :** `calibrate_evaluator.py`

**Fonctions principales :**
1. `load_example_dialogues()` - Charger dialogues de référence
2. `create_avatars(dialogue, n_good, n_bad)` - Générer avatars
3. `evaluate_avatar(avatar, api_url)` - Évaluer un avatar via API
4. `compare_scores(generated, expected)` - Comparer scores
5. `adjust_prompt(errors)` - Ajuster prompt selon erreurs
6. `calibrate()` - Processus complet de calibration

---

**Note :** Ce système permet de calibrer finement l'évaluateur pour qu'il donne des scores cohérents et justes selon les attentes pédagogiques.

