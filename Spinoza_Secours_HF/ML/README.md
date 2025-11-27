# 🤖 ML - Préparation du Modèle

**Dossier :** `ML/`  
**Contenu :** Fichiers liés à la préparation et au travail sur le modèle

---

## 📁 Fichiers

### Prompts Système

- **`prompt_systeme_hybride.py`** - Prompt système optimisé (~250 tokens)
  - Prompt système pour Spinoza
  - Schèmes logiques (identité, causalité, implication)
  - Instructions contextuelles
  - Optimisé pour économie de tokens

### Tests

- **`test_prompt_systeme.py`** - Script de test du prompt système
  - Teste le prompt SANS charger le modèle
  - Vérifie la construction du prompt
  - Détection de contexte
  - Post-processing

### Calibration

- **`calibrate_evaluator.py`** - Script de calibration de l'évaluateur
  - Utilise des dialogues réels avec scores de référence
  - Crée des avatars (bons/mauvais élèves)
  - Compare scores générés vs attendus
  - Calibre les critères d'évaluation

### Données

- **`dialogue-reel-1.txt`** - Dialogue réel pour calibration
  - Dialogue extrait des logs
  - Utilisé pour créer des avatars de calibration
  - Score frontend : 127
  - Niveau : moyen (avec résistances)

---

## 🎯 Structure

### Préparation du Modèle

1. **Prompts** → Définir le comportement du modèle
2. **Tests** → Vérifier que les prompts fonctionnent
3. **Calibration** → Ajuster les critères d'évaluation
4. **Données** → Dialogues réels pour référence

---

## 📝 Usage

### Tester un Prompt

```bash
python test_prompt_systeme.py
```

### Calibrer l'Évaluateur

```bash
python calibrate_evaluator.py https://votre-url-ngrok.ngrok-free.dev/evaluate
```

---

## 🔗 Liens

- **Backend :** `../Backend/`
- **Documentation :** `../docs/references/calibration-evaluation.md`
- **Tutos :** `../docs/tutos/`

---

## 🎯 Workflow ML

```
1. Définir prompt système (prompt_systeme_hybride.py)
   ↓
2. Tester le prompt (test_prompt_systeme.py)
   ↓
3. Déployer dans Backend (Backend/RAG_Spinoza_secours.ipynb)
   ↓
4. Calibrer l'évaluateur (calibrate_evaluator.py)
   ↓
5. Ajuster les paramètres selon résultats
```

