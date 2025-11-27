# Fix : Confusion des rôles dans le dialogue

## Problème identifié

Le modèle Spinoza dit parfois "Quand tu poses cette question..." alors que dans le scénario, c'est **Spinoza qui pose la question initiale**, pas l'élève. L'élève répond simplement à la question de Spinoza.

### Exemple du bug
```
Spinoza (greeting) : "Bonjour ! Je suis Spinoza. Discutons : **La liberté est-elle une illusion ?** Qu'en penses-tu ?"
Élève : "Je pense que oui, on est déterminés"
Spinoza (bug) : "Quand tu poses cette question, tu demandes aux causes finales de cesser..."
```

Le modèle confond les rôles et pense que l'élève a posé une question.

## Solution

Modification du prompt système dans `Cellule_9.py` pour clarifier :

1. **Ajout d'une section "CONTEXTE INITIAL"** qui précise :
   - C'est Spinoza qui pose la première question
   - L'élève répond à cette question, il ne pose pas de question lui-même au début
   - Répondre toujours à ce que l'élève vient de dire, pas à une question qu'il aurait posée

2. **Ajout d'une règle explicite** :
   - Ne JAMAIS dire "Quand tu poses cette question" → L'élève ne pose pas de question, il répond à la tienne
   - Répondre à ce que l'élève dit, pas à une question qu'il aurait posée

## Action requise

**Mettre à jour le notebook Colab** (`colab_spinoza_secours.ipynb`) avec le prompt modifié de `Cellule_9.py` :

1. Ouvrir la cellule qui contient `SYSTEM_PROMPT_SPINOZA`
2. Remplacer le prompt par celui de `Cellule_9.py` (lignes 5-59)
3. Redémarrer le serveur pour appliquer les changements

## Vérification

Après la mise à jour, tester :
- Le greeting initial doit être une question de Spinoza
- La première réponse de Spinoza doit réagir à ce que l'élève a dit, pas à une question qu'il aurait posée
- Ne plus voir de phrases comme "Quand tu poses cette question..."

