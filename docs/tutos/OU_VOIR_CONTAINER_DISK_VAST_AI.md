# 📍 Où Voir Container Disk et Volume Disk dans Vast.ai

**Date :** 28 novembre 2025  
**Interface :** Vast.ai Console

---

## 🎯 Où Trouver les Options de Stockage

### Étape 1 : Créer une Instance

1. **Aller sur :** https://vast.ai/console/create
2. **Sélectionner l'instance** (ex: 2x RTX 4090 que vous regardez)
3. **Cliquer sur "RENT"** ou "Create Instance"

### Étape 2 : Interface de Configuration

Après avoir cliqué sur "RENT", vous arrivez sur la page de **configuration de l'instance**.

**Les options de stockage se trouvent dans la section "Storage" ou "Disk"** :

---

## 📦 Section Storage/Disk

### Localisation dans l'Interface

**Cherchez une section intitulée :**
- **"Storage"** 
- **"Disk"**
- **"Container Disk"**
- **"Volume Disk"**

**Généralement située :**
- Après la section "GPU"
- Avant la section "Network" ou "Ports"
- Parfois dans un onglet séparé "Storage" ou "Advanced"

---

## 🔍 Détails des Options

### Container Disk (Stockage Éphémère)

**Ce que vous verrez :**
- **Slider ou champ numérique** pour la taille
- **Unité :** GB (Gigabytes)
- **Valeur recommandée :** 50GB minimum (ou plus si disponible)
- **Coût :** Généralement inclus dans le prix GPU (gratuit)

**Exemple d'affichage :**
```
Container Disk: [50 GB] [Slider: 10GB - 200GB]
```

**Caractéristiques :**
- ✅ Gratuit (inclus dans le prix)
- ⚠️ Éphémère (effacé à l'arrêt)
- ⚠️ Modèle retéléchargé à chaque démarrage

---

### Volume Disk (Stockage Persistant)

**Ce que vous verrez :**
- **Case à cocher** "Enable Volume Disk" ou "Persistent Storage"
- **Slider ou champ numérique** pour la taille
- **Unité :** GB
- **Valeur recommandée :** 50-100GB
- **Coût supplémentaire :** Généralement +$0.10-0.20/h

**Exemple d'affichage :**
```
☐ Enable Volume Disk
   Size: [50 GB] [Slider: 10GB - 500GB]
   Cost: +$0.15/h
```

**Caractéristiques :**
- ⚠️ Coût supplémentaire (+$0.10-0.20/h)
- ✅ Persistant (conservé entre redémarrages)
- ✅ Modèle conservé (démarrage rapide)

---

## 📸 Où Exactement dans l'Interface ?

### Option A : Section Dédiée "Storage"

```
┌─────────────────────────────────────┐
│ Create Instance                     │
├─────────────────────────────────────┤
│ GPU: 2x RTX 4090                    │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Storage                        │ │
│ │                                 │ │
│ │ Container Disk: [50 GB]       │ │
│ │ [Slider: 10GB ──────●──── 200GB]│
│ │                                 │ │
│ │ ☐ Enable Volume Disk           │ │
│ │    Size: [50 GB]               │ │
│ │    Cost: +$0.15/h              │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Network / Ports: ...               │
└─────────────────────────────────────┘
```

### Option B : Dans un Onglet "Advanced" ou "Settings"

Parfois, les options de stockage sont dans un onglet :
- **"Advanced"**
- **"Settings"**
- **"Storage"**
- **"Configuration"**

**Cherchez les onglets en haut de la page de configuration.**

---

## ⚠️ Si Vous Ne Voyez Pas les Options

### Cas 1 : Instance Déjà Configurée

Si l'instance est déjà en cours d'exécution :
1. **Dashboard** → **Instances**
2. Cliquer sur votre instance
3. **"Settings"** ou **"Edit"**
4. Chercher section **"Storage"**

### Cas 2 : Options Masquées

Certaines instances peuvent avoir des limitations :
- Container Disk fixe (non modifiable)
- Volume Disk non disponible
- Stockage inclus automatiquement

**Solution :** Vérifier les détails de l'instance avant de louer.

### Cas 3 : Interface Différente

L'interface Vast.ai peut varier selon :
- La version de l'interface
- Le type d'instance
- Les permissions du compte

**Solution :** Chercher dans tous les onglets/sections disponibles.

---

## 🎯 Pour Votre Instance (2x RTX 4090)

### Recommandations

**Container Disk :**
- **Minimum :** 50GB (pour Mistral 7B)
- **Recommandé :** 100GB (pour Qwen 14B futur)
- **Maximum :** Utiliser le maximum disponible si possible

**Volume Disk :**
- **Optionnel** pour usage ponctuel
- **Recommandé** si usage fréquent (>4h/jour avec redémarrages)
- **Taille :** 50-100GB

### Calcul pour 2x RTX 4090

**Avantages :**
- ✅ 48GB VRAM total (2x 24GB)
- ✅ Parfait pour Qwen 14B (peut splitter sur 2 GPUs)
- ✅ Marge confortable

**Stockage nécessaire :**
- Mistral 7B : ~14GB → Container Disk 50GB suffit
- Qwen 14B : ~28GB → Container Disk 100GB recommandé

---

## 📋 Checklist Configuration

Lors de la configuration de votre instance :

- [ ] Trouver la section "Storage" ou "Disk"
- [ ] Configurer Container Disk : **50GB minimum** (100GB si disponible)
- [ ] (Optionnel) Cocher "Enable Volume Disk" si usage fréquent
- [ ] Vérifier le coût total affiché
- [ ] Continuer avec la configuration Docker/Network

---

## 🔗 Références

- **Plan migration :** `docs/references/PLAN_MIGRATION_VAST_AI.md`
- **Section Storage :** Lignes 409-487 du plan

---

**Astuce :** Si vous ne trouvez pas les options, faites défiler toute la page de configuration ou cherchez dans les onglets "Advanced" ou "Settings" !

