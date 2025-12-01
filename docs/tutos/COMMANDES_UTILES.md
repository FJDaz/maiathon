# 🖥️ Commandes Utiles - Spinoza Secours

## Commandes de Base

### `cat` - Afficher le contenu d'un fichier

**Usage :**
```bash
cat nom_du_fichier
```

**Exemples :**
```bash
# Afficher le contenu complet
cat calibration_results.json

# Afficher les premières lignes
cat calibration_results.json | head -30

# Afficher avec numérotation des lignes
cat -n calibration_results.json

# Rechercher dans le fichier
cat calibration_results.json | grep "comprehension"
```

**Dans notre projet :**
```bash
# Voir les résultats de calibration
cd /Users/francois-jeandazin/bergsonAndFriends
cat calibration_results.json

# Ou depuis Spinoza_Secours_HF
cd /Users/francois-jeandazin/bergsonAndFriends/Spinoza_Secours_HF
cat ../calibration_results.json
```

---

## Commandes Python

### Exécuter le script de calibration

```bash
cd /Users/francois-jeandazin/bergsonAndFriends/Spinoza_Secours_HF/ML
python3 calibrate_evaluator.py https://ton-url-ngrok.ngrok-free.dev/evaluate
```

### Tester l'évaluation incrémentale

```bash
cd /Users/francois-jeandazin/bergsonAndFriends/Spinoza_Secours_HF
python3 Backend/test_http_incremental.py https://ton-url-ngrok.ngrok-free.dev
python3 Backend/test_http_incremental.py https://ton-url-ngrok.ngrok-free.dev --debug
```

---

## Commandes Git (Colab)

Voir `docs/tutos/commandes-colab-git.md` pour les commandes Git dans Colab.

---

## Commandes Utiles pour Débugger

### Voir les logs du serveur

Dans Colab, regardez la cellule qui lance le serveur (avec `uvicorn.run()`).

### Voir la réponse brute du modèle

Utiliser le mode debug :
```bash
curl -X POST "https://ton-url/evaluate/incremental?debug=true" \
  -H "Content-Type: application/json" \
  -d '{"dialogue": "...", "score_front": 100}'
```

### Vérifier un fichier JSON

```bash
# Vérifier si le JSON est valide
python3 -m json.tool calibration_results.json

# Formater le JSON pour lecture
python3 -m json.tool calibration_results.json | less
```

---

## Autres Commandes Utiles

### Trouver un fichier

```bash
# Chercher calibration_results.json
find . -name "calibration_results.json" -type f

# Chercher tous les fichiers Python
find . -name "*.py" -type f
```

### Compter les lignes

```bash
# Nombre de lignes dans un fichier
wc -l calibration_results.json

# Nombre de lignes de code Python
find . -name "*.py" -exec wc -l {} +
```

### Voir la taille des fichiers

```bash
# Taille d'un fichier
ls -lh calibration_results.json

# Taille de tous les fichiers dans un dossier
du -sh ML/
```



