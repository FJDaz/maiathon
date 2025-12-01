# 🔍 Comment Identifier la Bonne Instance Vast.ai

**Date :** 28 novembre 2025

---

## 🎯 Problème

Vous avez **2 instances** et vous devez identifier laquelle utiliser.

---

## ✅ ÉTAPE 1 : Lister Vos Instances

Dans l'interface Vast.ai, vous devriez voir une **liste ou tableau** avec vos instances.

**Cherchez ces informations pour CHAQUE instance :**

| Information | Où la trouver | Instance 1 | Instance 2 |
|------------|---------------|------------|------------|
| **Instance ID** | Colonne "ID" ou "#" | 28314448 ? | ? |
| **Status** | Colonne "Status" | Running ? | ? |
| **GPU** | Colonne "GPU" | RTX 4090 ? | ? |
| **IP Address** | Colonne "IP" ou "Public IP" | 195.139.22.91 ? | ? |
| **Uptime** | Colonne "Uptime" ou "Age" | ? minutes | ? minutes |
| **Cost/hr** | Colonne "$/hr" | $0.348 ? | ? |

**Note la plus récente (Uptime le plus court) = probablement la mauvaise (créée par erreur)**

---

## ✅ ÉTAPE 2 : Vérifier le HF_TOKEN

### Dans le Terminal de CHAQUE Instance

Ouvrez un terminal pour chaque instance et tapez :

```bash
echo "Token length: ${#HF_TOKEN}"
echo "Token starts with: ${HF_TOKEN:0:10}"
```

**Résultat attendu :**
```
Token length: 37
Token starts with: hf_aBcDeFg
```

**Si vous voyez :**
```
Token length: 0
Token starts with:
```

➡️ **Le HF_TOKEN n'est PAS défini dans cette instance.**

---

## 🔧 ÉTAPE 3 : Définir le HF_TOKEN Manuellement

### Si le Token N'est Pas Défini

Dans le terminal de l'instance :

```bash
export HF_TOKEN="VOTRE_TOKEN_ICI"
```

**⚠️ Remplacez `VOTRE_TOKEN_ICI` par votre vrai token HuggingFace !**

### Vérifier que Ça a Marché

```bash
echo $HF_TOKEN
```

Vous devriez voir votre token s'afficher.

### Puis Relancer le Script de Déploiement

```bash
cd /workspace
rm -rf maiathon
git clone https://github.com/FJDaz/maiathon.git
cd maiathon/Spinoza_Secours_HF/Backend
pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.runpod.txt
nohup python app_runpod.py > /tmp/spinoza.log 2>&1 &
```

---

## 🗑️ ÉTAPE 4 : Supprimer l'Instance Inutile

### Identifier l'Instance à Supprimer

**Critères pour GARDER une instance :**
- ✅ A le HF_TOKEN défini
- ✅ Instance ID = 28314448 (la première créée)
- ✅ IP = 195.139.22.91
- ✅ Application déployée avec succès

**Critères pour SUPPRIMER une instance :**
- ❌ Pas de HF_TOKEN
- ❌ Créée par erreur (Uptime court)
- ❌ Application non déployée
- ❌ Vous ne savez pas laquelle c'est

### Comment Supprimer une Instance

Dans l'interface Vast.ai, pour l'instance à supprimer :

1. **Cherchez** un bouton avec un de ces noms :
   - "Destroy" (le plus probable)
   - "Delete"
   - "Stop & Destroy"
   - "Terminate"
   - Icône poubelle 🗑️
   - Icône X rouge ❌

2. **Cliquez dessus**

3. **Confirmez** la suppression

**⚠️ L'instance sera détruite immédiatement et vous ne serez plus facturé.**

---

## 🎯 GUIDE VISUEL SIMPLIFIÉ

### Scénario A : Vous Avez 2 Instances Running

```
Instance 1                        Instance 2
-------------------              -------------------
ID: 28314448                     ID: 28314XXX
Status: Running                  Status: Running
GPU: RTX 4090                    GPU: RTX 4090
IP: 195.139.22.91                IP: 195.139.XX.XX
Uptime: 30 min                   Uptime: 5 min
```

**➡️ Gardez l'Instance 1 (la plus ancienne)**
**➡️ Détruisez l'Instance 2 (la plus récente)**

### Scénario B : Une Instance Running, Une Stopped

```
Instance 1                        Instance 2
-------------------              -------------------
Status: Running                  Status: Stopped
Uptime: 30 min                   Uptime: 0
```

**➡️ Gardez l'Instance Running**
**➡️ Détruisez l'Instance Stopped**

---

## 📋 CHECKLIST COMPLÈTE

### Pour CHAQUE Instance

- [ ] Noter l'Instance ID
- [ ] Noter le Status (Running/Stopped)
- [ ] Noter l'IP publique
- [ ] Noter l'Uptime
- [ ] Ouvrir le terminal
- [ ] Vérifier le HF_TOKEN avec `echo ${#HF_TOKEN}`
- [ ] Noter si le token est défini (longueur > 0)

### Décider Quelle Instance Garder

- [ ] Garder celle avec HF_TOKEN défini
- [ ] OU garder la plus ancienne (Uptime le plus long)
- [ ] OU garder celle avec IP 195.139.22.91
- [ ] Si aucun critère clair : garder l'Instance ID 28314448

### Nettoyer

- [ ] Détruire l'instance non utilisée
- [ ] Vérifier qu'une seule instance reste dans la liste

---

## 🔐 Où Trouver Votre HF_TOKEN

Si vous avez perdu votre token HuggingFace :

1. Allez sur https://huggingface.co/settings/tokens
2. Connectez-vous
3. Créez un nouveau token (ou copiez un existant)
4. Type: "Read" suffit pour télécharger les modèles

---

## 🆘 Commandes de Diagnostic

### Dans le Terminal de l'Instance

```bash
# Vérifier si HF_TOKEN existe
echo "HF_TOKEN défini: $([ -n "$HF_TOKEN" ] && echo 'OUI' || echo 'NON')"

# Vérifier l'IP publique de l'instance
curl -s ifconfig.me

# Vérifier si l'application tourne
ps aux | grep app_runpod

# Vérifier si le port 8000 est utilisé
netstat -tlnp | grep 8000

# Voir les variables d'environnement définies
env | grep -E "HF_|PORT"
```

---

## 📝 RÉSUMÉ : Action Immédiate

1. **Listez vos 2 instances** dans l'interface Vast.ai
2. **Pour chaque instance**, ouvrez un terminal et tapez : `echo ${#HF_TOKEN}`
3. **Gardez l'instance** où le token est défini (longueur > 0)
4. **Si aucune n'a le token** : gardez la plus ancienne et définissez le token manuellement
5. **Détruisez l'autre instance** pour éviter double facturation
6. **Dans l'instance gardée**, relancez le script de déploiement avec le HF_TOKEN

---

**Question pour vous :**

Pouvez-vous me donner ces infos pour vos 2 instances ?

- Instance 1 : ID, Status, Uptime, IP
- Instance 2 : ID, Status, Uptime, IP
- Instance 1 : `echo ${#HF_TOKEN}` = ?
- Instance 2 : `echo ${#HF_TOKEN}` = ?

Avec ça, je pourrai vous dire précisément laquelle garder et laquelle détruire.
