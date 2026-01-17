# 📚 Catalogue de Livres avec OCR

Système de gestion de catalogue de livres professionnel avec architecture à deux niveaux (Œuvre + Edition) et extraction automatique d'informations depuis photos de couvertures.

## ✨ Caractéristiques principales

### Architecture avancée
- 🎯 **Modèle à 2 niveaux** : Œuvre (création littéraire) + Edition (exemplaire spécifique)
- 📸 **Prêt pour l'OCR** : Extraction d'infos depuis photos de couvertures
- 🔗 **Gestion des éditions multiples** : Un livre, plusieurs ISBN différents
- 💾 **Pattern Repository** : Abstraction de la persistance des données
- 🗄️ **Base SQLite** : Stockage relationnel performant

### Fonctionnalités
- 📖 Gestion complète des œuvres littéraires
- 📚 Gestion détaillée des éditions (format, dimensions, photos)
- 🔍 Recherche intelligente avec algorithme de Levenshtein
- 🌐 API REST complète (FastAPI)
- 🖥️ Interface web (Streamlit)
- 📊 Statistiques avancées

## 🚀 Démarrage rapide

### Installation

```bash
# Cloner le projet
git clone <repo-url>
cd bibliotheque

# Installer les dépendances
pip install -r requirements.txt
```

### Lancer l'API REST

```bash
# Méthode 1 : uvicorn
uvicorn api:app --reload

# Méthode 2 : Python directement
python api.py
```

L'API sera accessible sur : http://localhost:8000
Documentation interactive : http://localhost:8000/docs

### Lancer l'interface Streamlit

```bash
streamlit run app.py
```

## 📁 Structure du projet

```
bibliotheque/
├── const/                          # Énumérations
│   ├── book_format.py             # Formats de livres (Poche, Broché, etc.)
│   └── genre.py                   # Genres littéraires
│
├── models/                         # Modèles de domaine (POO)
│   ├── oeuvre.py                  # Œuvre littéraire
│   └── edition.py                 # Édition spécifique
│
├── services/                       # Logique métier
│   ├── repository.py              # Interface abstraite
│   ├── memory_repository.py       # Repository en mémoire
│   ├── database.py                # Repository SQLite
│   └── bibliotheque.py            # Service principal
│
├── unicorn/                        # Utilitaires
│   └── u_string.py                # Recherche floue
│
├── tests/                          # Tests unitaires
│
├── api.py                          # API REST (FastAPI)
├── api_models.py                   # Modèles Pydantic
├── app.py                          # Interface Streamlit
│
├── ARCHITECTURE.md                 # Documentation architecture
├── MIGRATION.md                    # Guide de migration
├── API_README.md                   # Documentation API
└── requirements.txt                # Dépendances Python
```

## 🎯 Modèle de données

### Œuvre (Work)
Représente l'œuvre littéraire en tant que création intellectuelle.

```python
Oeuvre:
  work_id                # Identifiant unique
  title                  # Titre original
  author                 # Auteur principal
  co_authors             # Co-auteurs
  original_language      # Langue originale
  original_publication_year  # Première publication
  summary                # Résumé
  genres                 # Genres littéraires
  themes                 # Thèmes abordés
  awards                 # Prix littéraires
  series                 # Série (si applicable)
  series_number          # Numéro dans la série
```

### Édition (Edition)
Représente une édition spécifique avec son ISBN unique.

```python
Edition:
  isbn                   # ISBN unique
  work_id                # Référence vers l'œuvre
  publisher              # Éditeur
  publication_year       # Année d'édition
  language               # Langue

  # Format physique
  format                 # Poche, Broché, eBook, etc.
  pages                  # Nombre de pages
  dimensions_*           # Hauteur, largeur, épaisseur (cm)
  weight                 # Poids (grammes)

  # Images (pour OCR)
  cover_front_url        # 📷 Photo de couverture
  cover_back_url         # 📷 4ème de couverture
  cover_spine_url        # 📷 Dos du livre
  cover_color            # Couleur dominante

  # Commercial
  price                  # Prix
  currency               # Devise
  ean                    # Code-barres

  # Métadonnées éditoriales
  edition_number         # N° d'édition
  collection             # Collection
  translator             # Traducteur
  illustrator            # Illustrateur
  preface_by             # Préfacier
```

## 🔗 Relation : 1 Œuvre → N Éditions

```
Les Misérables (Victor Hugo, 1862)
├─ Édition Poche Gallimard 2020 (ISBN: 978-2-07-036222-6)
├─ Édition Pléiade 1951 (ISBN: 978-2-07-010142-1)
└─ Édition Kindle 2023 (ISBN: B00ABC123)
```

## 🎓 Concepts Python avancés

- ✅ **POO avancée** : Classes, héritage, composition
- ✅ **Type hints modernes** : `str | None`, `List[Type]`, `Optional[T]`
- ✅ **Enums** : Constantes typées
- ✅ **Pattern Repository** : Abstraction de la persistance
- ✅ **Properties avec validation** : Getters/setters personnalisés
- ✅ **Context managers** : Gestion automatique des ressources
- ✅ **FastAPI** : API REST avec validation Pydantic
- ✅ **SQLite relationnel** : Clés étrangères, index, transactions
- ✅ **Recherche floue** : Distance de Levenshtein

## 📡 API REST

### Endpoints principaux

```
# Informations
GET  /                              # Info API
GET  /stats                         # Statistiques

# Gestion des livres (en cours de migration)
GET    /livres                      # Liste tous les livres
GET    /livres/{isbn}               # Récupère un livre
POST   /livres                      # Ajoute un livre
PUT    /livres/{isbn}               # Met à jour
DELETE /livres/{isbn}               # Supprime

# Recherche
GET  /livres/search/?q=terme        # Recherche intelligente
GET  /livres/author/{author}        # Par auteur
GET  /livres/year/{year}            # Par année
```

Documentation complète : [API_README.md](API_README.md)

## 🔄 Migration

Le projet a été refactorisé pour passer d'une architecture simple à une architecture professionnelle à deux niveaux.

Voir [MIGRATION.md](MIGRATION.md) pour :
- Guide de migration des données
- Différences ancien/nouveau modèle
- Scripts de migration

Voir [ARCHITECTURE.md](ARCHITECTURE.md) pour :
- Documentation complète de l'architecture
- Schémas SQL
- Cas d'usage OCR

## 🚀 Fonctionnalités à venir

### En cours de développement
- [ ] Repositories pour Oeuvre et Edition
- [ ] API REST mise à jour avec nouveaux modèles
- [ ] Interface Streamlit refaite

### Roadmap OCR
- [ ] Module d'extraction OCR (Tesseract/Google Vision)
- [ ] Détection automatique ISBN depuis code-barres
- [ ] Extraction titre/auteur/éditeur depuis couverture
- [ ] Extraction résumé depuis 4ème de couverture
- [ ] Détection automatique des œuvres existantes
- [ ] Interface photo : capturer couvertures depuis smartphone

### Fonctionnalités additionnelles
- [ ] Import/Export CSV
- [ ] Intégration APIs externes (Google Books, Open Library)
- [ ] Système d'emprunt/prêt
- [ ] Recommandations basées sur genres/auteurs
- [ ] Application mobile

## 📖 Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture complète du système
- [MIGRATION.md](MIGRATION.md) - Guide de migration
- [API_README.md](API_README.md) - Documentation API REST

## 🧪 Tests

```bash
# Lancer les tests
pytest

# Avec coverage
pytest --cov=.

# Tests spécifiques
pytest tests/test_oeuvre.py
```

## 📝 Licence

Projet pédagogique pour l'apprentissage de Python et de l'architecture logicielle.

## 🤝 Contribution

Ce projet est un exercice d'apprentissage. Les contributions sont les bienvenues pour :
- Améliorer l'architecture
- Ajouter des fonctionnalités OCR
- Optimiser les performances
- Améliorer la documentation
