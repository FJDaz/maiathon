# 📊 Explication du Système de Score Maïeuthon

## 🎯 Le Score Affiché en Haut

Le **score affiché en haut** pendant le dialogue correspond au **Score Frontend** (`scoreFront`).

### Ce que c'est :
- **Score de base** : 50 points au démarrage (équilibré pour permettre montée et descente)
- **Calcul en temps réel** : modifié à chaque message de l'élève
- **Affichage** : visible dans la barre "🎮 Maïeuthon" en haut de l'interface

### Comment il est calculé :

À chaque message, le score est modifié selon 5 critères :

1. **Lexical** (vocabulaire philosophique)
   - Mots de progression (`donc`, `je comprends`, `d'accord`, etc.) : **+3 points chacun**
   - Mots de résistance (`pas d'accord`, `faux`, `tu te trompes`, etc.) : **-2 points chacun**

2. **Longueur** (effort de réponse)
   - Message < 5 caractères : **-5 points**
   - Message > 100 caractères : **+3 points**
   - Message > 50 caractères : **+1 point**
   - Sinon : **0 point**

3. **Cohérence** (qualité linguistique)
   - Mélange français/anglais excessif : **-3 points**
   - Répétitions de caractères (ex: `aaaaa`) : **-1 point par occurrence**
   - MAJUSCULES EXCESSIVES : **-1 point par occurrence**

4. **Répétition** (éviter les messages similaires)
   - Message trop similaire (>80%) à un message précédent : **-5 points**

5. **Fair-play** (respect du jeu)
   - Insultes : **-10 points**
   - Tentative de hack (demander le prompt, mentionner l'IA) : **-10 à -15 points**

### Exemple de calcul :
```
Message : "Ah ok et donc ma volonté de persévérer dans mon être est menacée par mes désirs selon toi ? Comment cela ?"

Lexical : +3 (mot "donc")
Length : +3 (message > 100 caractères)
Coherence : 0
Repetition : 0
FairPlay : 0
─────────────────
Total : +6 points

Score avant : 100
Score après : 106
```

---

## 📈 Amplitude Min et Max du Score

### Score Frontend (affiché en haut)

- **Minimum théorique** : **0** (le score ne peut pas descendre en dessous de 0 grâce à `Math.max(0, scoreFront)`)
- **Maximum théorique** : **Illimité** (mais en pratique rarement > 150)
- **Score de base** : **100**

**Calcul du minimum possible** :
- Si l'élève envoie 5 messages très courts avec insultes et répétitions :
  - Message 1 : -5 (longueur) -10 (insulte) = -15
  - Message 2 : -5 (longueur) -5 (répétition) = -10
  - Message 3 : -5 (longueur) -10 (insulte) = -15
  - Message 4 : -5 (longueur) -5 (répétition) = -10
  - Message 5 : -5 (longueur) -10 (insulte) = -15
  - **Total : -65 points**
  - **Score final frontend : 50 - 65 = -15** (mais plafonné à 0)

**Calcul du maximum possible** :
- Si l'élève envoie 5 messages longs avec beaucoup de mots de progression :
  - Message 1 : +3 (lexical, 1 mot) +3 (longueur) = +6
  - Message 2 : +9 (lexical, 3 mots) +3 (longueur) = +12
  - Message 3 : +6 (lexical, 2 mots) +3 (longueur) = +9
  - Message 4 : +9 (lexical, 3 mots) +3 (longueur) = +12
  - Message 5 : +6 (lexical, 2 mots) +3 (longueur) = +9
  - **Total : +48 points**
  - **Score final frontend : 50 + 48 = 98**

### Score Backend (évaluation finale)

Le backend évalue le dialogue complet sur 3 critères (0-10 chacun) :
- **Compréhension** : 0-10
- **Coopération** : 0-10
- **Progression** : 0-10

**Total backend** : **0 à 30 points**

### Score Final

**Score Final = Score Frontend + Score Backend**

- **Minimum théorique** : 0 (frontend) + 0 (backend) = **0 points**
- **Maximum théorique** : ~100 (frontend) + 30 (backend) = **~130 points**
- **En pratique** : généralement entre **20 et 110 points**

### Affichage Final

Le score final est affiché comme `${finalScore}/100` dans la modal de résultat, mais c'est juste un format d'affichage. Le score réel peut dépasser 100.

**Codes couleur** :
- **Vert** (≥ 80) : Excellent
- **Orange** (50-79) : Correct
- **Rouge** (< 50) : À améliorer

---

## 📝 Résumé

| Élément | Min | Max | Base |
|---------|-----|-----|------|
| **Score Frontend** (affiché en haut) | 0 | ~100 | 50 |
| **Score Backend** (évaluation finale) | 0 | 30 | - |
| **Score Final** | 0 | ~130 | - |

**Le score en haut** = Score Frontend calculé en temps réel pendant le dialogue, modifié à chaque message selon la qualité lexicale, longueur, cohérence, répétition et fair-play.

