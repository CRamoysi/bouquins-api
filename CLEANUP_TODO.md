# 🧹 TODO - Nettoyage des imports obsolètes

## ❌ Fichiers avec imports obsolètes détectés

### Fichiers critiques (à corriger en priorité)

| Fichier | Imports obsolètes | Action requise |
|---------|-------------------|----------------|
| `api.py` | `from models.livre import Livre` | ⚠️ Réécrire avec Oeuvre + Edition |
| `app.py` | `from models.livre import Livre` | ⚠️ Réécrire avec Oeuvre + Edition |
| `services/bibliotheque.py` | `from models.bouquin import Bouquin` | ⚠️ Adapter pour Edition |
| `services/database.py` | `from models.bouquin import Bouquin`<br>`from models.livre import Livre` | ⚠️ Réécrire avec 2 tables |
| `services/memory_repository.py` | `from models.bouquin import Bouquin` | ⚠️ Adapter pour Edition |
| `services/repository.py` | `from models.bouquin import Bouquin` | ⚠️ Rendre générique |

### Fichiers de tests (à réécrire)

| Fichier | Imports obsolètes | Action requise |
|---------|-------------------|----------------|
| `tests/test_bibliotheque.py` | `from models.livre import Livre` | 🔄 Réécrire tests |
| `tests/test_service_bibliotheque.py` | `from models.livre import Livre` | 🔄 Réécrire tests |
| `tests/test_sqlite_repository.py` | `from models.livre import Livre` | 🔄 Réécrire tests |

## 🎯 Plan de nettoyage

### Étape 1 : Rendre les interfaces génériques
- [ ] `services/repository.py` - Utiliser `Any` ou créer 2 repositories (OeuvreRepository, EditionRepository)

### Étape 2 : Créer les nouveaux repositories
- [ ] `services/oeuvre_repository.py` - Repository pour Oeuvre
- [ ] `services/edition_repository.py` - Repository pour Edition
- [ ] `services/database.py` - Réécrire avec 2 tables (oeuvres + editions)

### Étape 3 : Adapter le service Bibliotheque
- [ ] `services/bibliotheque.py` - Gérer Oeuvres ET Editions
- [ ] Créer méthodes séparées : `add_oeuvre()`, `add_edition()`, etc.

### Étape 4 : Réécrire l'API
- [ ] `api_models.py` - Créer OeuvreCreate, OeuvreResponse, EditionCreate, EditionResponse
- [ ] `api.py` - Nouveaux endpoints `/oeuvres` et `/editions`

### Étape 5 : Réécrire Streamlit
- [ ] `app.py` - Interface pour gérer Oeuvres + Editions

### Étape 6 : Réécrire les tests
- [ ] `tests/test_oeuvre.py` - Tests pour Oeuvre
- [ ] `tests/test_edition.py` - Tests pour Edition
- [ ] `tests/test_oeuvre_repository.py`
- [ ] `tests/test_edition_repository.py`

## 🚨 Erreurs potentielles

### Imports qui vont échouer

Tous ces imports vont générer des erreurs car les modules n'existent plus :

```python
from models.bouquin import Bouquin  # ❌ ERREUR - Fichier supprimé
from models.livre import Livre      # ❌ ERREUR - Fichier supprimé
```

### Nouveaux imports à utiliser

```python
from models import Oeuvre, Edition  # ✅ CORRECT
# ou
from models.oeuvre import Oeuvre    # ✅ CORRECT
from models.edition import Edition  # ✅ CORRECT
```

## 📝 Notes

### Pourquoi ne pas tout corriger immédiatement ?

Ces fichiers nécessitent une **refactorisation complète**, pas juste un remplacement d'imports :

1. **Architecture différente** : Passage d'1 modèle à 2 modèles
2. **Base de données** : Passage d'1 table à 2 tables avec relation
3. **Logique métier** : Gérer la relation Oeuvre ↔ Editions
4. **API** : Endpoints séparés pour Oeuvres et Editions

### Approche recommandée

Au lieu de corriger les imports, il vaut mieux **réécrire** ces fichiers avec la nouvelle architecture :

- Créer de nouveaux fichiers (`oeuvre_repository.py`, etc.)
- Garder les anciens temporairement (compatibilité)
- Migrer progressivement
- Supprimer les anciens une fois la migration complète

## 🔄 État actuel

### ✅ Architecture propre (modèles)
- `models/oeuvre.py` ✅
- `models/edition.py` ✅
- `const/book_format.py` ✅
- `const/genre.py` ✅

### ⚠️ Services à migrer
- `services/repository.py` - À rendre générique ou dupliquer
- `services/database.py` - À réécrire complètement
- `services/bibliotheque.py` - À adapter
- `services/memory_repository.py` - À dupliquer (OeuvreRepo + EditionRepo)

### ⚠️ Applications à migrer
- `api.py` - À réécrire
- `app.py` - À réécrire
- `tests/*.py` - À réécrire

## 💡 Recommandation

**Ne pas essayer de "réparer" les imports obsolètes.**
**Créer de nouveaux fichiers avec la nouvelle architecture.**

Cela permet de :
- Garder l'ancien code fonctionnel temporairement
- Migrer progressivement
- Éviter les erreurs en cascade
- Tester la nouvelle architecture avant de supprimer l'ancienne
