# 🔐 Fix HF_TOKEN - Sans Exposer le Token

**Date :** 28 novembre 2025

---

## 🎯 Situation

Le script demande le HF_TOKEN en interactif, mais vous ne voulez pas (et ne devez pas) le taper en clair.

---

## ✅ SOLUTION 1 : Vérifier si le Token est Déjà Défini

### Dans le terminal, tapez :

```bash
env | grep HF_TOKEN
```

**Si vous voyez :**
```
HF_TOKEN=hf_aBcDeFgHiJkLmNoPqRsTuVwXyZ123456
```

➡️ **Le token EST défini !** Le script devrait le lire automatiquement.

**Si vous ne voyez rien :**

➡️ Le token n'est PAS défini dans cette session.

---

## ✅ SOLUTION 2 : Définir le Token de Façon Sécurisée

### Méthode A : Export Simple (Recommandé)

Dans le terminal :

```bash
export HF_TOKEN="COLLEZ_VOTRE_TOKEN_ICI"
```

**⚠️ Important :**
- Copiez votre token depuis https://huggingface.co/settings/tokens
- Collez-le entre les guillemets
- Appuyez sur ENTRÉE
- **Le token sera dans la variable d'environnement, pas dans l'historique**

### Vérifier que ça a marché :

```bash
echo "Token défini: $([ -n "$HF_TOKEN" ] && echo 'OUI' || echo 'NON')"
```

Vous devriez voir : `Token défini: OUI`

---

## ✅ SOLUTION 3 : Modifier app_runpod.py pour Lire le Token Automatiquement

### Option 1 : Le Script Lit Déjà la Variable

Vérifiez si `app_runpod.py` contient déjà :

```bash
grep -n "HF_TOKEN" /workspace/maiathon/Spinoza_Secours_HF/Backend/app_runpod.py
```

**Si vous voyez des lignes comme :**
```python
hf_token = os.getenv("HF_TOKEN")
```

➡️ **Le script lit déjà la variable d'environnement !**

Vous n'avez rien à faire, juste définir `export HF_TOKEN=...` avant de lancer le script.

---

## ✅ SOLUTION 4 : Relancer le Script Correctement

### Si vous avez fait CTRL+C :

1. **Définir le token** :
```bash
export HF_TOKEN="VOTRE_TOKEN_ICI"
```

2. **Vérifier** :
```bash
echo ${#HF_TOKEN}
```
Vous devriez voir un nombre > 0 (par exemple 37)

3. **Relancer le script de déploiement** :
```bash
cd /workspace/maiathon/Spinoza_Secours_HF/Backend
python app_runpod.py > /tmp/spinoza.log 2>&1 &
```

4. **Surveiller les logs** :
```bash
tail -f /tmp/spinoza.log
```

---

## 🔍 Pourquoi le Script Demandait le Token ?

### Possibilité 1 : Input() dans le Code

Le script contient peut-être :
```python
hf_token = input("Enter HF_TOKEN: ")
```

**➡️ À corriger** en :
```python
hf_token = os.getenv("HF_TOKEN")
```

### Possibilité 2 : Token Non Défini

La variable `HF_TOKEN` n'était pas définie dans l'environnement.

**➡️ Solution** : `export HF_TOKEN=...` avant de lancer le script.

---

## 🛠️ Vérifier le Contenu de app_runpod.py

### Voir comment le token est lu :

```bash
grep -A 3 -B 3 "HF_TOKEN\|hf_token\|input" /workspace/maiathon/Spinoza_Secours_HF/Backend/app_runpod.py
```

**Envoyez-moi le résultat** pour que je voie si le script est correct.

---

## 📋 CHECKLIST

- [ ] Faire CTRL+C pour tuer le processus en suspens
- [ ] Vérifier si HF_TOKEN est défini : `env | grep HF_TOKEN`
- [ ] Si non : `export HF_TOKEN="VOTRE_TOKEN"`
- [ ] Vérifier : `echo ${#HF_TOKEN}` (doit être > 0)
- [ ] Relancer : `cd /workspace/maiathon/Spinoza_Secours_HF/Backend && python app_runpod.py > /tmp/spinoza.log 2>&1 &`
- [ ] Surveiller : `tail -f /tmp/spinoza.log`

---

## 🔐 Sécurité du Token

### ✅ BON (sécurisé) :
- `export HF_TOKEN="..."` dans le terminal
- Lire depuis variable d'environnement : `os.getenv("HF_TOKEN")`
- Définir dans les variables d'environnement du template Vast.ai

### ❌ MAUVAIS (à éviter) :
- Taper le token en réponse à `input()`
- Hardcoder le token dans le code : `hf_token = "hf_abc123..."`
- Commiter le token dans Git

---

## 🆘 Si Ça Ne Marche Toujours Pas

Envoyez-moi :

1. **Le résultat de** :
```bash
grep -n "hf_token\|HF_TOKEN\|input" /workspace/maiathon/Spinoza_Secours_HF/Backend/app_runpod.py
```

2. **Le résultat de** :
```bash
env | grep HF
```

3. **Les dernières lignes des logs** :
```bash
tail -20 /tmp/spinoza.log
```

Je pourrai alors vous dire exactement ce qui cloche.
