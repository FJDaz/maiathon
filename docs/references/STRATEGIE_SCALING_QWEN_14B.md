# 📈 Stratégie de Scaling vers Qwen 14B + LoRA

**Date :** 28 novembre 2025  
**Migration :** Mistral 7B → Qwen 14B + LoRA (SNB)  
**Objectif :** Planifier la montée en charge future

---

## 🎯 Vue d'Ensemble

### Modèles Comparés

| Critère | Mistral 7B | Qwen 14B | Différence |
|---------|------------|----------|------------|
| **Taille modèle** | ~14 GB | ~28 GB | **+100%** |
| **VRAM nécessaire (4-bit)** | ~6-8 GB | ~12-14 GB | **+75-100%** |
| **VRAM nécessaire (8-bit)** | ~10-12 GB | ~20-24 GB | **+100%** |
| **VRAM recommandée** | 16-24 GB | **32-48 GB** | **+100%** |
| **Latence inference** | ~1-2s | ~2-4s | **+100%** |
| **Coût/h (RTX 4090)** | $0.27-0.29 | $0.27-0.29 | **Identique** |

---

## ❌ Limitation Vast.ai : Changement de GPU

### Réponse Courte : **NON, impossible de changer le GPU dans une instance existante**

**Raisons techniques :**
1. **Instance = GPU spécifique** : Chaque instance Vast.ai est liée à un GPU spécifique au moment de la création
2. **Pas de "GPU swap"** : Vast.ai ne permet pas de changer le GPU d'une instance en cours d'exécution
3. **Container Disk lié au GPU** : Le stockage est attaché à l'instance GPU spécifique

**Ce qui est possible :**
- ✅ Modifier les variables d'environnement
- ✅ Modifier le code Docker (via GitHub)
- ✅ Redémarrer l'instance
- ✅ Changer la taille du Container Disk (dans certaines limites)
- ❌ **Changer le GPU** (impossible)

---

## ✅ Solutions pour Scaling vers Qwen 14B

### Option 1 : Nouvelle Instance (RECOMMANDÉ) ⭐⭐⭐

**Stratégie :** Créer une nouvelle instance avec GPU adapté

**Avantages :**
- ✅ Choix optimal du GPU (32-48GB VRAM)
- ✅ Pas d'interruption de service (Mistral 7B continue)
- ✅ Test en parallèle avant migration
- ✅ Rollback facile (garder les deux instances)
- ✅ Configuration optimisée dès le départ

**Inconvénients :**
- ⚠️ Coût double pendant transition (2 instances)
- ⚠️ Nécessite mise à jour frontend (changement d'URL)

**GPU Recommandés pour Qwen 14B :**

| GPU | VRAM | Coût/h | Recommandation |
|-----|------|--------|----------------|
| **RTX 4090** | 24 GB | $0.27-0.29 | ⚠️ **Limite** (4-bit seulement) |
| **A100 40GB** | 40 GB | $1.00-1.50 | ✅ **Optimal** (4-bit ou 8-bit) |
| **A100 80GB** | 80 GB | $2.00-3.00 | ✅ **Parfait** (8-bit, marge) |
| **RTX 6000 Ada** | 48 GB | $0.80-1.20 | ✅ **Bon compromis** |

**Recommandation :**
- **Usage ponctuel :** RTX 4090 (24GB) avec quantization 4-bit ⚠️ Limite
- **Usage production :** A100 40GB ou RTX 6000 Ada 48GB ✅ Optimal

---

### Option 2 : Template Réutilisable ⭐⭐

**Stratégie :** Créer un template générique réutilisable

**Avantages :**
- ✅ Configuration Docker réutilisable
- ✅ Variables d'environnement paramétrables
- ✅ Migration rapide (créer instance depuis template)

**Configuration Template :**

```yaml
# Template : spinoza-secours-generic
Variables d'environnement :
  - MODEL_NAME: mistralai/Mistral-7B-Instruct-v0.2  # ou Qwen/Qwen2.5-14B-Instruct
  - ADAPTER_NAME: FJDaz/mistral-7b-philosophes-lora  # ou FJDaz/qwen-14b-snb-lora
  - HF_TOKEN: [token]
  - PORT: 8000
  - QUANTIZATION: 4bit  # ou 8bit pour Qwen 14B
```

**Dockerfile générique :**
- Même structure
- Variables d'environnement pour modèle/adapter
- Code Python adaptatif

---

### Option 3 : Migration Progressive (A/B Testing) ⭐⭐⭐

**Stratégie :** Tester Qwen 14B en parallèle avant migration complète

**Étapes :**

1. **Phase 1 : Déploiement Qwen 14B (Test)**
   - Créer nouvelle instance avec A100 40GB
   - Déployer Qwen 14B + LoRA
   - URL test : `spinoza-secours-qwen-test.vast.ai:8000`

2. **Phase 2 : Tests Comparatifs**
   - Comparer latence Mistral 7B vs Qwen 14B
   - Comparer qualité des réponses
   - Tester charge (nombre d'utilisateurs simultanés)

3. **Phase 3 : Migration Progressive**
   - Option A : Frontend avec toggle Mistral/Qwen
   - Option B : Migration complète après validation
   - Option C : Garder les deux (Mistral pour usage ponctuel, Qwen pour production)

4. **Phase 4 : Arrêt Instance Mistral (si migration complète)**
   - Arrêter instance Mistral 7B
   - Mettre à jour frontend avec URL Qwen
   - Libérer ressources

---

## 📋 Plan de Migration Recommandé

### Étape 1 : Préparation (Maintenant)

**Actions :**
- [x] Créer template générique (Dockerfile + app_runpod.py)
- [ ] Ajouter variables d'environnement pour modèle/adapter
- [ ] Tester template avec Mistral 7B
- [ ] Documenter configuration

**Fichiers à modifier :**
- `Backend/app_runpod.py` : Ajouter variables `MODEL_NAME`, `ADAPTER_NAME`
- `Backend/Dockerfile.runpod` : Reste identique
- `Backend/requirements.runpod.txt` : Vérifier compatibilité Qwen

### Étape 2 : Déploiement Qwen 14B (Quand prêt)

**Actions :**
1. **Créer nouvelle instance Vast.ai**
   - GPU : A100 40GB ou RTX 6000 Ada 48GB
   - Container Disk : 100GB (Qwen 14B = ~28GB)
   - Template : Utiliser template générique
   - Variables : `MODEL_NAME=Qwen/Qwen2.5-14B-Instruct`, `ADAPTER_NAME=FJDaz/qwen-14b-snb-lora`

2. **Déployer et tester**
   - Build Docker : 5-10 min
   - Téléchargement Qwen 14B : 15-20 min (~28GB)
   - Chargement GPU : 2-3 min
   - Tests endpoints : `/health`, `/init`, `/chat`, `/evaluate`

3. **Comparaison Mistral vs Qwen**
   - Latence : Mesurer temps de réponse
   - Qualité : Tester dialogues réels
   - Stabilité : Test charge (10-20 utilisateurs simultanés)

### Étape 3 : Migration (Après validation)

**Option A : Migration Complète**
- Arrêter instance Mistral 7B
- Mettre à jour frontend avec URL Qwen
- Monitorer performance

**Option B : Dual Deployment**
- Garder Mistral 7B pour usage ponctuel (coût réduit)
- Utiliser Qwen 14B pour production (meilleure qualité)
- Frontend avec toggle ou routing intelligent

---

## 💰 Coûts Comparés

### Mistral 7B (Actuel)
- **GPU :** RTX 4090 (24GB)
- **Coût :** $0.27-0.29/h
- **Usage ponctuel (3h) :** ~$0.82
- **1 mois (24/7) :** ~$196

### Qwen 14B (Futur)
- **GPU :** A100 40GB (recommandé)
- **Coût :** $1.00-1.50/h
- **Usage ponctuel (3h) :** ~$3.00-4.50
- **1 mois (24/7) :** ~$720-1080

**Alternative RTX 4090 (limite) :**
- **GPU :** RTX 4090 (24GB) ⚠️ Limite
- **Coût :** $0.27-0.29/h (identique)
- **Quantization :** 4-bit obligatoire
- **Risque :** OOM possible si contexte long

---

## 🔧 Modifications Code Nécessaires

### 1. `app_runpod.py` - Variables d'environnement

```python
# Configuration
BASE_MODEL = os.getenv("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.2")
ADAPTER_MODEL = os.getenv("ADAPTER_NAME", "FJDaz/mistral-7b-philosophes-lora")
QUANTIZATION = os.getenv("QUANTIZATION", "4bit")  # 4bit ou 8bit
```

### 2. `app_runpod.py` - Support Qwen

```python
# Formatage prompt selon modèle
if "qwen" in BASE_MODEL.lower():
    # Format Qwen
    prompt_format = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{message}<|im_end|>\n<|im_start|>assistant\n"
else:
    # Format Mistral
    prompt_format = f"<s>[INST] {system_prompt}\n\n{message} [/INST]"
```

### 3. `requirements.runpod.txt` - Vérifier compatibilité

```txt
torch>=2.2.0
transformers>=4.40.0  # Vérifier support Qwen
peft>=0.10.0
bitsandbytes>=0.43.0
accelerate>=0.28.0
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.5.0
slowapi>=0.1.9
```

---

## ✅ Recommandations Finales

### Pour l'Instance Actuelle (RTX 4090 24GB)

**Mistral 7B :** ✅ **Parfait**
- VRAM suffisante (6-8GB avec 4-bit)
- Marge confortable
- Performance optimale

**Qwen 14B :** ⚠️ **Limite**
- VRAM juste suffisante (12-14GB avec 4-bit)
- Pas de marge
- Risque OOM si contexte long
- **Recommandation :** Ne pas utiliser cette instance pour Qwen 14B

### Stratégie Recommandée

1. **Maintenant (Mistral 7B) :**
   - ✅ Utiliser instance RTX 4090 24GB actuelle
   - ✅ Container Disk 50GB
   - ✅ Template générique (préparer pour migration)

2. **Plus tard (Qwen 14B) :**
   - ✅ Créer **nouvelle instance** avec A100 40GB ou RTX 6000 Ada 48GB
   - ✅ Container Disk 100GB
   - ✅ Réutiliser template générique
   - ✅ Tester en parallèle avant migration

3. **Migration :**
   - ✅ A/B testing (Mistral vs Qwen)
   - ✅ Migration progressive ou complète selon résultats
   - ✅ Garder option de rollback (instance Mistral)

---

## 📝 Checklist Migration Qwen 14B

### Préparation
- [ ] Modifier `app_runpod.py` pour support variables d'environnement
- [ ] Tester template générique avec Mistral 7B
- [ ] Vérifier compatibilité Qwen dans `requirements.runpod.txt`
- [ ] Documenter format prompts Qwen

### Déploiement
- [ ] Créer nouvelle instance Vast.ai (A100 40GB ou RTX 6000 Ada 48GB)
- [ ] Configurer Container Disk 100GB
- [ ] Déployer avec variables Qwen
- [ ] Tester endpoints

### Validation
- [ ] Comparer latence Mistral vs Qwen
- [ ] Comparer qualité des réponses
- [ ] Tester charge (utilisateurs simultanés)
- [ ] Valider stabilité

### Migration
- [ ] Décider : migration complète ou dual deployment
- [ ] Mettre à jour frontend (si migration complète)
- [ ] Monitorer performance
- [ ] Documenter changements

---

## 🔗 Références

- **Plan migration actuel :** `docs/references/PLAN_MIGRATION_VAST_AI.md`
- **Template générique :** À créer
- **Documentation Qwen :** À ajouter

---

**Conclusion :** ❌ **Impossible de changer le GPU dans une instance existante**. ✅ **Créer une nouvelle instance avec GPU adapté (A100 40GB ou RTX 6000 Ada 48GB) est la meilleure stratégie.**

