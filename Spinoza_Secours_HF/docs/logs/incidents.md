# Documentation des Incidents - Spinoza Secours Vast.ai

**Format standardisé pour documenter tous les incidents de production**

---

## Template d'Incident

```markdown
## Incident [YYYY-MM-DD HH:MM]

**Type :** [Downtime / Erreur / Sécurité / Performance / Coût]
**Sévérité :** [Critique / Haute / Moyenne / Basse]
**Durée :** [X minutes/heures]
**Impact utilisateurs :** [Oui/Non - Description]

### Cause
[Description détaillée de la cause racine]

### Symptômes
- [Symptôme 1]
- [Symptôme 2]

### Actions Immédiates
1. [Action prise immédiatement]
2. [Action prise immédiatement]

### Résolution
[Description de la résolution appliquée]

### Prévention
[Mesures mises en place pour éviter récurrence]

### Coût Impact
- **Temps d'indisponibilité :** [X heures]
- **Coût perdu :** [Si applicable]
- **Coût résolution :** [Si applicable]

### Références
- Logs : [Lien vers logs pertinents]
- Dashboard : [Lien vers métriques]
- Tickets : [Numéros de tickets si applicable]
```

---

## Exemples d'Incidents

### Exemple 1 : Instance Crash

```markdown
## Incident 2025-01-15 14:30

**Type :** Downtime
**Sévérité :** Critique
**Durée :** 25 minutes
**Impact utilisateurs :** Oui - Service inaccessible

### Cause
Instance Vast.ai crashée suite à erreur CUDA OOM (Out of Memory) lors d'une requête d'évaluation avec dialogue très long.

### Symptômes
- Health check retourne 502
- Logs montrent "CUDA out of memory"
- Instance status: "Stopped" dans dashboard

### Actions Immédiates
1. Redémarré l'instance depuis dashboard Vast.ai
2. Vérifié que le modèle se recharge correctement
3. Testé les endpoints après redémarrage

### Résolution
- Instance redémarrée manuellement
- Ajouté validation longueur dialogue (max 2000 tokens) dans code
- Commit et push correction
- Redéployé instance avec nouveau code

### Prévention
- Validation longueur inputs renforcée
- Monitoring OOM ajouté dans logs
- Alerte configurée si instance crash

### Coût Impact
- **Temps d'indisponibilité :** 25 minutes
- **Coût perdu :** ~$0.10 (25 min × $0.24/h)
- **Coût résolution :** 0$ (redémarrage gratuit)

### Références
- Logs : Dashboard Vast.ai → Instance → Logs (2025-01-15 14:30-14:55)
- Dashboard : https://vast.ai/console/instances
```

---

## Statistiques

**Total incidents :** 0  
**Temps d'indisponibilité total :** 0 minutes  
**Coût total incidents :** $0

---

**Dernière mise à jour :** Janvier 2025

