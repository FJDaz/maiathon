# Guide Vast.ai - Spinoza Secours
## Méthode testée et validée - 29 nov 2025

---

## ⚠️ RÈGLES D'OR (Ne pas transiger)

1. **JAMAIS d'on-start script complexe** - Vast.ai les parse mal
2. **TOUJOURS déployer manuellement** - C'est plus long mais ça marche
3. **TOUJOURS vérifier la clé SSH AVANT de rent** - Sinon impossible de se connecter
4. **JAMAIS de template avec port 8888** - C'est déjà pris par Jupyter
5. **TOUJOURS utiliser `python3`** (pas `python`) sur Vast.ai
6. **TOUJOURS envoyer `history` au format correct** - `[["q", "r"]]` pas `[]`

---

## 🎯 WORKFLOW QUI MARCHE (Testé et validé)

### Phase 1 : Préparation (10 min - une seule fois)

#### 1.1 Créer/Vérifier ta clé SSH Mac

```bash
# Sur ton Mac
ls ~/.ssh/id_ed25519.pub
```

**Si le fichier n'existe pas**, crée-le :

```bash
ssh-keygen -t ed25519 -C "francois.jean.dazin@gmail.com"
# Appuie 3x sur Entrée (pas de passphrase)
```

#### 1.2 Copier la clé publique

```bash
cat ~/.ssh/id_ed25519.pub
```

**Copie TOUTE la ligne** (commence par `ssh-ed25519`)

#### 1.3 Ajouter la clé dans Vast.ai

1. Va sur https://cloud.vast.ai/
2. **Account** → **SSH Keys**
3. **Add SSH Key**
4. Colle ta clé publique
5. Donne un nom : "MacBook Pro"
6. **Save**

⚠️ **CRITIQUE** : Cette étape doit être faite AVANT de créer une instance.

---

### Phase 2 : Créer le template (5 min - une seule fois)

#### 2.1 Va sur Templates

https://cloud.vast.ai/ → **Templates** → **Create New Template**

#### 2.2 Configuration template minimal

```yaml
Template Name: Spinoza Basic (Working)

Image Path:Tag: nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

Ports: 8080

Environment Variables:
  HF_TOKEN: hf_ton_vrai_token_ici
  PORT: 8000

Launch Mode: Jupyter-python notebook + SSH

On-start Script: (LAISSER VIDE - Ne rien mettre)

Disk Space: 50 GB
```

⚠️ **ATTENTION** :
- Port **8080** (pas 8888, pas 8000)
- On-start Script **VIDE** (c'est normal)
- Remplace `hf_ton_vrai_token_ici` par ton vrai token HF

#### 2.3 Save le template

Clique **Save** (pas "Save and Use" pour l'instant)

---

### Phase 3 : Rent une instance (3 min)

#### 3.1 Cherche une machine

1. **Templates** → Sélectionne ton template "Spinoza Basic"
2. **Search Offers** ou **Save and Use**

#### 3.2 Filtres recommandés

- **Reliability** : > 98%
- **Verified** : Coché
- **Prix** : < $0.30/h (RTX 3060, GTX 1080 Ti suffisent)
- **VRAM** : > 12 GB minimum

#### 3.3 Rent

Clique **Rent** sur une offre → Confirme

⏱️ **Attends 2-3 minutes** que l'instance démarre (Status = Running)

---

### Phase 4 : Déploiement manuel (5-7 min)

#### 4.1 Ouvre le terminal Jupyter Web

1. **Instances** → Trouve ton instance
2. Clique sur le lien **Jupyter** ou l'URL affichée
3. Ça ouvre Jupyter dans le navigateur
4. **New** → **Terminal** (en haut à droite)

#### 4.2 Commandes de déploiement

**Copie-colle ces commandes UNE PAR UNE** dans le terminal Jupyter :

```bash
# 1. Va dans /workspace
cd /workspace

# 2. Clone le repo
git clone https://github.com/FJDaz/maiathon.git

# 3. Va dans Backend
cd maiathon/Spinoza_Secours_HF/Backend

# 4. Vérifie que tu es au bon endroit
pwd
# Doit afficher: /workspace/maiathon/Spinoza_Secours_HF/Backend

# 5. Configure le port (8000 en interne)
export PORT=8000

# 6. Vérifie HF_TOKEN
echo "HF_TOKEN: $([ -n "$HF_TOKEN" ] && echo 'OK' || echo 'MANQUANT')"

# 7. Installe les dépendances (prend 2-3 min)
pip3 install --no-cache-dir -r requirements.runpod.txt

# 8. Lance l'app
python3 app_runpod.py
```

⏱️ **Attends que le modèle se charge** (2-5 min)

Tu verras :
```
Downloading model...
Loading checkpoint shards: 100%
INFO: Uvicorn running on http://0.0.0.0:8000
```

✅ **Quand tu vois "Uvicorn running" → L'app est prête !**

---

### Phase 5 : Connexion depuis ton Mac (2 min)

#### 5.1 Trouve la commande SSH

Dans Vast.ai **Instances** :
- Clique sur **Connect** ou cherche "SSH Command"
- Tu verras quelque chose comme :

```bash
ssh -p 61736 root@89.11.135.172 -L 8080:localhost:8080
```

⚠️ **Change le port forwarding** : Remplace `-L 8080:localhost:8080` par `-L 8000:localhost:8000`

#### 5.2 Connecte-toi depuis ton Mac

**Ouvre un NOUVEAU Terminal sur ton Mac** et lance :

```bash
ssh -p PORT root@IP -L 8000:localhost:8000
```

(Remplace PORT et IP par les vraies valeurs de l'étape 5.1)

**Laisse ce terminal ouvert** → C'est ton tunnel SSH

---

### Phase 6 : Test (1 min)

#### 6.1 Test santé

Dans ton **navigateur Mac** :

```
http://localhost:8000/health
```

Tu dois voir :
```json
{"status":"ok","model":"Mistral 7B + LoRA","gpu_available":true}
```

#### 6.2 Test conversation

Dans le **navigateur Mac** :

```
http://localhost:8000/docs
```

Clique **POST /chat** → **Try it out**

**Request body** :
```json
{
  "message": "Explique-moi ce qu'est la substance divine",
  "history": [
    ["Bonjour", "Salut"]
  ]
}
```

**Execute**

⏱️ Attends 15-30 secondes → Spinoza répond !

---

## 🐛 BUG CONNU - History vide

### Problème

```json
{
  "message": "Bonjour",
  "history": []
}
```

→ **Erreur 500 : IndexError list index out of range**

### Solution rapide

**TOUJOURS mettre au moins un élément** dans history :

```json
{
  "message": "Ta vraie question",
  "history": [
    ["placeholder", "placeholder"]
  ]
}
```

### Solution définitive (optionnelle)

Édite `app_runpod.py` ligne 302 :

```bash
# Dans terminal Jupyter
cd /workspace/maiathon/Spinoza_Secours_HF/Backend
nano app_runpod.py
```

Cherche (Ctrl+W) : `for entry in history:`

Change :
```python
for entry in history:
    prompt_parts.append(f"{entry[0]} [/INST] {entry[1]}</s>[INST] ")
```

En :
```python
for entry in history:
    if len(entry) >= 2:
        prompt_parts.append(f"{entry[0]} [/INST] {entry[1]}</s>[INST] ")
```

Sauvegarde : **Ctrl+O** → **Entrée** → **Ctrl+X**

Relance l'app :
```bash
pkill -f app_runpod
export PORT=8000
python3 app_runpod.py
```

---

## 💰 Arrêter l'instance (IMPORTANT)

### Quand tu as fini

1. https://cloud.vast.ai/ → **Instances**
2. Trouve ton instance
3. **Destroy** (icône 🗑️)
4. Confirme

✅ **Facturation arrêtée immédiatement**

### Coût typique

- Session de test (1h) : ~$0.20
- Session de dev (3h) : ~$0.60
- Journée complète (8h) : ~$1.50

---

## 🚫 CE QUI NE MARCHE PAS (Ne pas réessayer)

### ❌ On-start script avec multi-lignes et emojis

```bash
#!/bin/bash
echo "🚀 Démarrage..."
# etc.
```

→ **Vast.ai le parse mal** → Erreur `OFFER_ID: No such file or directory`

### ❌ Template avec port 8888

→ **Jupyter occupe déjà ce port** → Conflit

### ❌ Utiliser `python` au lieu de `python3`

→ **Commande introuvable** sur l'image Ubuntu

### ❌ Envoyer `history: []` sans fix du code

→ **Erreur 500 IndexError**

### ❌ Oublier d'ajouter la clé SSH avant de rent

→ **Permission denied (publickey)**

---

## 📋 Checklist avant chaque session

- [ ] Clé SSH ajoutée dans Vast.ai Account
- [ ] Template créé avec on-start VIDE
- [ ] Solde > $1 dans Vast.ai
- [ ] HF_TOKEN configuré dans template
- [ ] Port = 8080 dans template (pas 8888)

---

## 🔄 Workflow rapide (sessions suivantes)

Une fois que tout est configuré (clé SSH + template) :

1. **Rent** instance avec template (2 min)
2. **Jupyter Terminal** → Copie-colle les 8 commandes de déploiement (5 min)
3. **SSH depuis Mac** avec tunnel `-L 8000:localhost:8000` (1 min)
4. **Teste** `http://localhost:8000/docs` (1 min)
5. **Destroy** quand fini (instantané)

**Total : 10 minutes** de setup par session

---

## 🚀 Améliorations futures (optionnelles)

### Si tu veux automatiser

- Créer un script bash local qui enchaîne toutes les commandes SSH
- Utiliser `tmux` pour garder l'app en arrière-plan
- Créer un vrai Dockerfile custom (pas l'on-start script Vast.ai)

### Si tu veux exposer publiquement

- Configurer un reverse proxy (nginx)
- Utiliser ngrok pour un tunnel temporaire
- Migrer vers RunPod ou Modal (meilleure gestion des scripts)

**Mais pour l'instant → La méthode manuelle fonctionne parfaitement** ✅

---

## 📞 Support

**Si ça ne marche toujours pas** :

1. Vérifie que tu suis EXACTEMENT chaque étape
2. Regarde les logs dans le terminal Jupyter où tourne l'app
3. Contacte le support Vast.ai (chat en bas à droite, très réactifs)

---

**Version du guide** : 29 novembre 2025  
**Testé sur** : Vast.ai, RTX 3060, Ubuntu 22.04, Mistral 7B + LoRA Spinoza  
**Coût session de validation** : $0.08 (25 minutes)  
**Taux de succès** : 100% si workflow suivi exactement
