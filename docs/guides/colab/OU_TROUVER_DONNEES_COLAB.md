# 📍 Où Trouver les Données Côté Serveur Colab

## 🔍 Emplacements des Données dans Colab

### 1. Répertoire Principal
Dans Colab, les fichiers sont généralement dans :
```
/content/
```

### 2. Fichiers Uploadés
Quand vous uploadez des fichiers via l'interface Colab (icône 📁 Files), ils vont dans :
```
/content/
```

### 3. Vérifier les Fichiers Disponibles
Dans une cellule Colab, exécutez :
```python
import os

# Lister tous les fichiers dans /content/
print("📁 Fichiers dans /content/ :")
for item in os.listdir('/content/'):
    path = f'/content/{item}'
    if os.path.isfile(path):
        size = os.path.getsize(path)
        print(f"  📄 {item} ({size} bytes)")
    else:
        print(f"  📂 {item}/")

# Chercher un fichier spécifique
import glob
fichiers = glob.glob('/content/**/*', recursive=True)
print(f"\n🔍 Total fichiers trouvés : {len(fichiers)}")
```

### 4. Répertoire de Travail Actuel
Pour voir où vous êtes :
```python
import os
print(f"📂 Répertoire actuel : {os.getcwd()}")
```

## 🚨 Résoudre un 404

### Si vous avez un 404 sur une route API

Les endpoints disponibles dans le serveur FastAPI sont :
- `GET /` - Informations sur l'API
- `GET /health` - Health check
- `GET /init` - Initialiser conversation
- `POST /chat` - Envoyer message
- `POST /evaluate` - Évaluer dialogue (si défini)
- `POST /evaluate/incremental` - Évaluation incrémentale (si défini)

### Vérifier les Endpoints Disponibles
Dans Colab, après avoir lancé le serveur, testez :
```python
import requests

# Remplacer par votre URL ngrok
url_ngrok = "https://votre-url-ngrok.ngrok.io"

# Tester les endpoints
endpoints = ["/", "/health", "/init"]
for endpoint in endpoints:
    try:
        response = requests.get(f"{url_ngrok}{endpoint}")
        print(f"✅ {endpoint} : {response.status_code}")
    except Exception as e:
        print(f"❌ {endpoint} : {e}")
```

### Si vous cherchez un Fichier Spécifique

1. **Dans Colab**, ouvrez le panneau Files (📁 à gauche)
2. **Cherchez** le fichier dans la liste
3. **Cliquez droit** → "Copy path" pour obtenir le chemin exact

### Si vous voulez Servir des Fichiers Statiques

Actuellement, **aucun endpoint ne sert de fichiers statiques**. Si vous avez besoin de servir des fichiers, ajoutez dans votre cellule FastAPI :

```python
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Servir un dossier de fichiers statiques
app.mount("/static", StaticFiles(directory="/content/static"), name="static")

# Ou servir un fichier spécifique
@app.get("/data/{filename}")
def get_file(filename: str):
    file_path = f"/content/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "File not found"}, 404
```

## 📝 Logs du Serveur

Pour voir les erreurs 404 dans les logs :
1. Dans Colab, regardez la **cellule qui lance le serveur** (avec `uvicorn.run()`)
2. Les erreurs 404 apparaîtront dans la sortie de cette cellule

## 🔧 Commandes Utiles

```python
# Lister les fichiers récursivement
import os
for root, dirs, files in os.walk('/content'):
    for file in files:
        print(os.path.join(root, file))

# Chercher un fichier par nom
import glob
resultats = glob.glob('/content/**/nom_du_fichier.*', recursive=True)
print(resultats)

# Vérifier si un fichier existe
import os
chemin = "/content/mon_fichier.json"
if os.path.exists(chemin):
    print(f"✅ Fichier trouvé : {chemin}")
    print(f"   Taille : {os.path.getsize(chemin)} bytes")
else:
    print(f"❌ Fichier non trouvé : {chemin}")
```

