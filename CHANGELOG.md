# 📝 Changelog - Nettoyage et refactorisation

## [2.0.0] - 2026-01-17 - Architecture à deux niveaux

### ✨ Ajouts majeurs

#### Nouveaux modèles
- ✅ `models/oeuvre.py` - Classe Oeuvre pour représenter les œuvres littéraires
- ✅ `models/edition.py` - Classe Edition pour les éditions spécifiques avec ISBN
- ✅ `const/book_format.py` - Enum pour les formats de livres (Poche, Broché, eBook, etc.)
- ✅ `const/genre.py` - Enum pour les genres littéraires (40+ genres)

#### Documentation
- ✅ `ARCHITECTURE.md` - Documentation complète de l'architecture à 2 niveaux
- ✅ `MIGRATION.md` - Guide de migration vers la nouvelle architecture
- ✅ `CHANGELOG.md` - Ce fichier
- ✅ `README.md` - Complètement réécrit

#### Configuration
- ✅ `const/__init__.py` - Export des enums
- ✅ `models/__init__.py` - Export de Oeuvre et Edition

### 🗑️ Suppressions (fichiers obsolètes)

- ❌ `const/reading_status.py` - Statuts de lecture retirés du catalogue
- ❌ `models/bouquin.py` - Remplacé par `models/oeuvre.py`
- ❌ `models/livre.py` - Remplacé par `models/edition.py`
- ❌ `services/stockage.py` - Fichier vide jamais utilisé
- ❌ `test_livre.json` - Fichier de test temporaire

### 🔄 Modifications

#### models/__init__.py
```diff
- from .bouquin import Bouquin
- from .livre import Livre
- __all__ = ['Bouquin', 'Livre']
+ from models.oeuvre import Oeuvre
+ from models.edition import Edition
+ __all__ = ['Oeuvre', 'Edition']
```

#### README.md
- Complètement réécrit pour refléter la nouvelle architecture
- Ajout de la documentation du modèle de données
- Ajout du guide de démarrage rapide
- Ajout de la roadmap OCR

### ⚠️ Fichiers à mettre à jour (prochaines étapes)

Les fichiers suivants utilisent encore l'ancienne architecture et devront être réécrits :

1. **services/database.py** - Schéma SQL à mettre à jour pour 2 tables
2. **services/bibliotheque.py** - Service à adapter pour Oeuvre + Edition
3. **api.py** - Endpoints à réécrire pour les nouveaux modèles
4. **api_models.py** - Modèles Pydantic à créer pour Oeuvre et Edition
5. **app.py** - Interface Streamlit à refaire
6. **tests/*.py** - Tous les tests à réécrire

### 📊 Statistiques

**Avant nettoyage :**
- Fichiers Python : ~15
- Modèles : 3 (Bouquin, Livre, Magazine)
- Tables BDD : 1 (livres)
- Architecture : Simple (1 niveau)

**Après nettoyage :**
- Fichiers Python : ~12
- Modèles : 2 (Oeuvre, Edition)
- Enums : 2 (BookFormat, Genre)
- Tables BDD : 2 (oeuvres, editions) - à créer
- Architecture : Professionnelle (2 niveaux)

### 🎯 Objectifs atteints

✅ Suppression du code obsolète
✅ Architecture claire et documentée
✅ Séparation Œuvre/Edition pour gérer éditions multiples
✅ Prêt pour l'OCR (attributs cover_front_url, cover_back_url, etc.)
✅ Modèles enrichis (dimensions, poids, format, etc.)
✅ Documentation complète

### 🔜 Prochaines étapes

1. Créer les repositories pour Oeuvre et Edition
2. Créer le schéma SQL avec 2 tables + relation
3. Réécrire l'API REST
4. Réécrire l'interface Streamlit
5. Implémenter l'OCR
6. Migration des données existantes

## [1.0.0] - Ancienne architecture (dépréciée)

### Caractéristiques
- Modèle simple avec `Livre` unique
- 1 ISBN = 1 entrée complète
- Duplication des données (auteur/titre répétés)
- Pas de gestion des éditions multiples
- Stockage JSON puis migration vers SQLite
- Interface Streamlit basique
- API REST basique

### Problèmes identifiés
- ❌ Duplication des informations pour chaque ISBN
- ❌ Impossible de gérer plusieurs éditions d'une même œuvre
- ❌ Pas de champs pour images de couvertures (OCR)
- ❌ Architecture limitée pour faire évoluer le projet

---

## Notes de migration

### Pour les utilisateurs existants

Si vous avez des données dans l'ancienne architecture :

1. **Ne supprimez pas** `bibliotheque.db` ou `catalogue.db`
2. Consultez [MIGRATION.md](MIGRATION.md) pour le guide complet
3. Un script de migration sera fourni pour convertir vos données

### Compatibilité

- ⚠️ **Breaking changes** : L'ancienne API n'est plus compatible
- ⚠️ Les anciens modèles ont été supprimés
- ⚠️ Le schéma de base de données a changé

### Recommandations

- Pour les nouveaux projets : Utilisez directement la v2.0.0
- Pour les projets existants : Suivez le guide de migration
- Les données peuvent être migrées automatiquement via script

---

## Remerciements

Cette refactorisation permet de passer d'un projet d'apprentissage simple à une architecture professionnelle prête pour la production et l'ajout de fonctionnalités OCR avancées.
