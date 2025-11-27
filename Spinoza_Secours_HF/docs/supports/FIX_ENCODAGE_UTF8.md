# 🔧 Fix Encodage UTF-8 - Problème de caractères mal affichés

## Problème

Les réponses du modèle affichent des caractères mal encodés :
- `Ãªtre` au lieu de `être`
- `connaÃ®tre` au lieu de `connaître`
- `Ã©volution` au lieu de `évolution`
- `libertÃ©` au lieu de `liberté`

## Cause

Le problème vient probablement du **tokenizer** qui décode les tokens en utilisant un mauvais encodage (latin-1 au lieu de UTF-8).

## Solution

### 1. Dans la fonction `spinoza_repond()` (notebook Colab)

Modifier la ligne de décodage pour forcer UTF-8 :

```python
# AVANT (ligne ~875)
response = tokenizer.decode(new_tokens, skip_special_tokens=True)

# APRÈS
response = tokenizer.decode(new_tokens, skip_special_tokens=True, clean_up_tokenization_spaces=True)
# S'assurer que la réponse est bien en UTF-8
if isinstance(response, bytes):
    response = response.decode('utf-8')
elif not isinstance(response, str):
    response = str(response)
```

### 2. Vérifier l'encodage du tokenizer

Ajouter une vérification dans le chargement du modèle :

```python
# Après avoir chargé le tokenizer
print(f"Tokenizer vocab size: {len(tokenizer)}")
print(f"Tokenizer encoding: {tokenizer.encoding if hasattr(tokenizer, 'encoding') else 'N/A'}")

# Tester le décodage
test_tokens = tokenizer.encode("être libre")
test_decode = tokenizer.decode(test_tokens)
print(f"Test décodage: '{test_decode}'")
if "être" not in test_decode:
    print("⚠️ PROBLÈME D'ENCODAGE DÉTECTÉ!")
```

### 3. Forcer UTF-8 dans FastAPI (optionnel mais recommandé)

Dans l'endpoint `/chat`, s'assurer que la réponse est bien encodée :

```python
from fastapi import Response
from fastapi.responses import JSONResponse

@app.post("/chat")
def chat(req: ChatRequest):
    global conversation_history
    
    # Mettre à jour historique si fourni
    if req.history:
        conversation_history = req.history
    
    # Générer réponse
    reply = spinoza_repond(req.message)
    
    # S'assurer que la réponse est en UTF-8
    if isinstance(reply, bytes):
        reply = reply.decode('utf-8')
    
    # Nettoyer les caractères mal encodés (fallback)
    try:
        reply = reply.encode('latin-1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        pass  # Si ça échoue, garder la réponse originale
    
    return JSONResponse(
        content={
            "reply": reply,
            "history": conversation_history
        },
        media_type="application/json; charset=utf-8"
    )
```

### 4. Solution alternative : Nettoyer la réponse après décodage

Ajouter une fonction de nettoyage dans `spinoza_repond()` :

```python
def fix_encoding(text: str) -> str:
    """Corrige les problèmes d'encodage courants"""
    try:
        # Si le texte semble être en latin-1 mal interprété
        if 'Ã' in text or 'Â' in text:
            # Essayer de corriger
            text = text.encode('latin-1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        pass
    return text

# Dans spinoza_repond(), après le décodage :
response = tokenizer.decode(new_tokens, skip_special_tokens=True)
response = fix_encoding(response)  # Ajouter cette ligne
```

## Vérification

Pour tester si le problème est résolu :

1. **Tester avec une question contenant des accents** :
   ```
   "Qu'est-ce que la liberté ?"
   ```

2. **Vérifier la réponse dans la console du navigateur** :
   ```javascript
   console.log(data.reply);
   // Devrait afficher : "Qu'est-ce que la liberté ?" et non "Qu'est-ce que la libertÃ© ?"
   ```

3. **Vérifier les en-têtes HTTP** :
   ```bash
   curl -I https://votre-url.ngrok-free.dev/chat
   # Devrait contenir : Content-Type: application/json; charset=utf-8
   ```

## Solution rapide (temporaire)

Si vous ne pouvez pas modifier le notebook immédiatement, vous pouvez corriger côté frontend dans `index_spinoza.html` :

```javascript
// Dans la fonction submitQuestion(), après avoir reçu data.reply
const data = await response.json();
let reply = data.reply;

// Corriger l'encodage si nécessaire
try {
    // Si le texte semble mal encodé, essayer de le corriger
    if (reply.includes('Ã') || reply.includes('Â')) {
        reply = reply.split('').map(char => {
            try {
                return char.charCodeAt(0) > 127 ? 
                    String.fromCharCode(char.charCodeAt(0)) : char;
            } catch {
                return char;
            }
        }).join('');
        // Essayer de réencoder
        reply = decodeURIComponent(escape(reply));
    }
} catch (e) {
    console.warn('Erreur correction encodage:', e);
}

// Utiliser reply corrigé
conversationHistory.push([userMessage, reply]);
```

**Note :** Cette solution frontend est un contournement. La vraie solution est de corriger le problème côté backend dans le tokenizer.

