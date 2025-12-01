# 🌐 Fix Accès Réseau - Port 8000 Non Accessible

**Date :** 28 novembre 2025
**Problème :** FastAPI tourne sur le port 8000 mais timeout depuis l'extérieur

---

## 🔍 Diagnostic

### Dans le terminal Jupyter de votre instance :

```bash
# Vérifier que FastAPI écoute bien sur 0.0.0.0:8000
netstat -tlnp | grep 8000

# Tester depuis l'intérieur de l'instance
curl http://localhost:8000/health

# Voir l'IP publique réelle
curl -s ifconfig.me
```

**Envoyez-moi les résultats** de ces 3 commandes.

---

## 🔧 Solutions Possibles

### Solution 1 : Le Port 8000 N'est Pas Exposé dans la Config Vast.ai

Dans l'interface Vast.ai, **éditez votre instance ou template** :

Cherchez une section :
- **"Port Mappings"** ou
- **"Exposed Ports"** ou
- **"TCP Ports"** ou
- **"Direct Port"**

**Ajoutez le port :**
```
8000
```

OU si c'est un mapping :
```
8000:8000
```

**Puis redémarrez l'instance.**

---

### Solution 2 : L'IP Publique N'est Pas 195.139.22.91

L'IP a peut-être changé après le reboot.

**Dans l'interface Vast.ai :**
- Cherchez l'IP publique actuelle de votre instance
- Elle devrait être affichée quelque part (colonne "IP", "Public IP", "Connect", etc.)

**OU dans le terminal :**
```bash
curl -s ifconfig.me
```

**Puis testez avec la vraie IP :**
```
http://[VRAIE_IP]:8000/health
```

---

### Solution 3 : Utiliser l'URL Fournie par Vast.ai

Vast.ai fournit parfois une **URL proxy** au lieu de l'IP directe.

**Dans l'interface Vast.ai :**

Cherchez un bouton ou lien :
- "Open"
- "Connect"
- "Public URL"
- "Jupyter URL" (mais avec le port 8000)

L'URL pourrait ressembler à :
```
https://jupyter-28314448-8000.vast.ai
```

OU
```
http://195.139.22.91:PORT_MAPPE/
```

---

### Solution 4 : Le Firewall Bloque le Port 8000

Certaines instances Vast.ai ont un firewall.

**Dans le terminal :**
```bash
# Vérifier si iptables bloque
sudo iptables -L -n | grep 8000

# Vérifier si ufw est actif
sudo ufw status
```

**Si ufw est actif :**
```bash
sudo ufw allow 8000/tcp
```

---

### Solution 5 : FastAPI Écoute sur 127.0.0.1 au Lieu de 0.0.0.0

Vérifiez dans les logs que vous voyez bien :
```
Uvicorn running on http://0.0.0.0:8000
```

**Pas** `http://127.0.0.1:8000`

Si c'est `127.0.0.1`, il faut modifier `app_runpod.py`.

---

## 🧪 Tests à Faire MAINTENANT

### Test 1 : Depuis l'intérieur de l'instance

Dans le terminal Jupyter :
```bash
curl http://localhost:8000/health
```

**Si ça marche :** Le problème est la config réseau Vast.ai (port non exposé)

**Si ça ne marche pas :** Le problème est dans FastAPI lui-même

---

### Test 2 : Vérifier l'IP Réelle

```bash
curl -s ifconfig.me
```

**Est-ce bien `195.139.22.91` ?**

---

### Test 3 : Vérifier les Ports Exposés

Dans l'interface Vast.ai, regardez la configuration de votre instance.

**Cherchez :**
- Section "Ports" ou "Port Mappings"
- Liste des ports exposés

**Le port 8000 apparaît-il ?**

---

## 📋 Checklist de Diagnostic

Faites ces commandes et envoyez-moi les résultats :

```bash
# 1. FastAPI écoute-t-il ?
netstat -tlnp | grep 8000

# 2. Test local
curl http://localhost:8000/health

# 3. IP publique
curl -s ifconfig.me

# 4. Ports ouverts
ss -tlnp | grep 8000

# 5. Firewall
sudo iptables -L -n | grep 8000 || echo "Pas de règle iptables pour 8000"
```

---

## 🎯 Action Immédiate

1. **Dans le terminal Jupyter**, testez :
```bash
curl http://localhost:8000/health
```

2. **Regardez l'interface Vast.ai** :
   - Cherchez la section "Ports" ou "Port Mappings"
   - Vérifiez que le port 8000 est listé

3. **Envoyez-moi** :
   - Le résultat de `curl http://localhost:8000/health`
   - L'IP affichée dans l'interface Vast.ai
   - Si vous voyez une section "Ports" : ce qui est affiché dedans

---

## 🔗 URLs Possibles à Tester

Si l'IP a changé ou si Vast.ai utilise un proxy, testez :

```
http://195.139.22.91:8000/health
https://195.139.22.91:8000/health (avec HTTPS)
http://[IP_REELLE]:8000/health
http://[INSTANCE_ID].vast.ai:8000/health
```

---

**Question prioritaire :** Que donne `curl http://localhost:8000/health` depuis le terminal Jupyter ?
