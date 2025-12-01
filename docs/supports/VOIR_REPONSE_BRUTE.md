# 🔍 Comment Voir la Réponse Brute du Modèle

## Problème

Vous ne voyez pas les logs dans Colab (cellule serveur), mais vous voulez voir **exactement ce que le modèle génère** pour diagnostiquer pourquoi le parsing JSON échoue.

## Solution : Mode Debug dans la Réponse HTTP

Le code a été modifié pour retourner la réponse brute du modèle **directement dans la réponse HTTP** via un paramètre de requête.

### Méthode 1 : Via le Script de Test

```bash
cd /Users/francois-jeandazin/bergsonAndFriends/Spinoza_Secours_HF
python3 Backend/test_http_incremental.py https://nonremunerative-rory-unbreakably.ngrok-free.dev --debug
```

**Résultat attendu :**
```json
{
  "scores": {...},
  "exchange_count": 1,
  "accumulated": true,
  "debug": {
    "raw_model_response": "...",
    "parsing_success": false
  }
}
```

### Méthode 2 : Via curl

```bash
curl -X POST "https://nonremunerative-rory-unbreakably.ngrok-free.dev/evaluate/incremental?debug=true" \
  -H "Content-Type: application/json" \
  -d '{"dialogue": "Élève: Bonjour\nSpinoza: Salut\nÉlève: Qu'est-ce que la liberté ?", "score_front": 100}'
```

**Important :** Ajoutez `?debug=true` à la fin de l'URL !

### Méthode 3 : Via Python/Requests

```python
import requests

url = "https://nonremunerative-rory-unbreakably.ngrok-free.dev/evaluate/incremental?debug=true"
data = {
    "dialogue": "Élève: Bonjour\nSpinoza: Salut\nÉlève: Qu'est-ce que la liberté ?",
    "score_front": 100
}

response = requests.post(url, json=data)
result = response.json()

if "debug" in result:
    print("🔍 Réponse brute du modèle:")
    print(result["debug"]["raw_model_response"])
    print(f"\n✅ Parsing réussi: {result['debug']['parsing_success']}")
```

## Ce que Vous Verrez

Dans la section `debug` de la réponse, vous aurez :

1. **`raw_model_response`** : Les premiers 500 caractères de la réponse brute du modèle
2. **`parsing_success`** : `true` si le parsing JSON a réussi (pas de valeurs par défaut à 5), `false` sinon

## Diagnostic

Si `parsing_success: false` et les scores sont tous à 5 :
- Regardez `raw_model_response`
- Vérifiez si le modèle génère du texte avant/après le JSON
- Vérifiez si le JSON est mal formé
- Vérifiez si le JSON contient les bons champs

## Exemple de Réponse Debug

```json
{
  "scores": {
    "comprehension": 5,
    "cooperation": 5,
    "progression": 5,
    "total": 15
  },
  "exchange_count": 1,
  "accumulated": true,
  "debug": {
    "raw_model_response": "Voici l'évaluation:\n{\n \"comprehension\": 7,\n \"cooperation\": 8,\n \"progression\": 6,\n \"total\": 21\n}\nC'est correct.",
    "parsing_success": false
  }
}
```

Ici, on voit que le modèle génère du texte avant (`"Voici l'évaluation:\n"`) et après (`"\nC'est correct."`) le JSON, mais le parsing devrait quand même fonctionner avec la regex. Si ça ne fonctionne pas, il faut améliorer la regex ou le prompt.

## Prochaines Étapes

1. **Lancez le test avec `--debug`**
2. **Regardez `raw_model_response`** dans la réponse
3. **Analysez** pourquoi le parsing échoue
4. **Partagez** le contenu de `raw_model_response` si besoin pour ajuster le code

---

**Note :** Le mode debug n'est activé que si vous ajoutez `?debug=true` dans l'URL. Sans ce paramètre, la réponse est normale (sans section `debug`).



