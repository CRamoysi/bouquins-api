# 📐 Architecture du Catalogue de Livres

## 🎯 Vue d'ensemble

Le système utilise une architecture à **deux niveaux** pour gérer les livres :
- **Œuvre** : L'œuvre littéraire en tant que création intellectuelle
- **Édition** : Une édition physique ou numérique spécifique d'une œuvre

### Pourquoi cette séparation ?

Un même livre peut exister en plusieurs éditions différentes :
- Édition poche Gallimard 2020
- Édition reliée Pléiade 1951
- Édition numérique Kindle 2023
- Traduction anglaise Penguin 2015

Toutes ces éditions partagent la même **œuvre** mais ont des **ISBN différents**.

## 📚 Modèle de données

### 1. Œuvre (Work)

Représente l'œuvre littéraire indépendamment de ses éditions.

```python
Oeuvre:
  - work_id: str                          # Identifiant unique
  - title: str                            # Titre original
  - author: str                           # Auteur principal
  - co_authors: List[str]                 # Co-auteurs
  - original_language: str                # Langue originale
  - original_publication_year: int?       # Première publication
  - summary: str?                         # Résumé
  - genres: List[Genre]                   # Genres littéraires
  - themes: List[str]                     # Thèmes abordés
  - awards: List[str]                     # Prix littéraires
  - series: str?                          # Nom de la série
  - series_number: int?                   # Numéro dans la série
```

**Exemple :**
```
work_id: "WORK-001"
title: "Les Misérables"
author: "Victor Hugo"
original_language: "fr"
original_publication_year: 1862
genres: [ROMAN, HISTORIQUE]
```

### 2. Édition (Edition)

Représente une édition spécifique avec son ISBN unique.

```python
Edition:
  # Identifiants
  - isbn: str                             # ISBN unique
  - work_id: str                          # Lien vers l'œuvre

  # Publication
  - publisher: str                        # Éditeur
  - publication_year: int?                # Année d'édition
  - publication_date: datetime?           # Date exacte
  - language: str                         # Langue

  # Format physique
  - format: BookFormat                    # Poche, Broché, etc.
  - pages: int?                           # Nombre de pages
  - dimensions_height: float?             # Hauteur (cm)
  - dimensions_width: float?              # Largeur (cm)
  - dimensions_thickness: float?          # Épaisseur (cm)
  - weight: int?                          # Poids (g)

  # Images (pour OCR)
  - cover_front_url: str?                 # 📷 Photo de couverture
  - cover_back_url: str?                  # 📷 4ème de couverture
  - cover_spine_url: str?                 # 📷 Dos du livre
  - cover_color: str?                     # Couleur dominante

  # Commercial
  - price: float?                         # Prix
  - currency: str                         # Devise
  - ean: str?                             # Code-barres

  # Métadonnées éditoriales
  - edition_number: int?                  # N° d'édition
  - collection: str?                      # Collection
  - translator: str?                      # Traducteur
  - illustrator: str?                     # Illustrateur
  - preface_by: str?                      # Préfacier

  # État
  - condition: str                        # État du livre
  - notes: str?                           # Notes personnelles
```

**Exemple :**
```
isbn: "978-2-07-036222-6"
work_id: "WORK-001"
publisher: "Gallimard"
publication_year: 2020
format: POCHE
pages: 1488
cover_front_url: "/images/covers/978-2-07-036222-6-front.jpg"
cover_back_url: "/images/covers/978-2-07-036222-6-back.jpg"
price: 9.90
currency: "EUR"
```

## 🔗 Relations

### Relation 1:N (Une Œuvre → Plusieurs Éditions)

```
┌─────────────────────────────────────┐
│ OEUVRE: Les Misérables              │
│ work_id: WORK-001                   │
│ author: Victor Hugo                 │
│ original_publication_year: 1862     │
└─────────────────────────────────────┘
              ▲
              │ work_id
      ┌───────┼───────┬────────┐
      │               │        │
┌─────▼─────┐  ┌──────▼────┐  ┌▼────────────┐
│ EDITION   │  │ EDITION   │  │ EDITION     │
│ Poche     │  │ Reliée    │  │ Kindle      │
│ 978-2-07  │  │ 978-2-07  │  │ B00ABC123   │
│ Gallimard │  │ Pléiade   │  │ Amazon      │
│ 2020      │  │ 1951      │  │ 2023        │
└───────────┘  └───────────┘  └─────────────┘
```

## 📊 Schéma de base de données

### Table `oeuvres`
```sql
CREATE TABLE oeuvres (
    work_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    co_authors TEXT,                    -- JSON array
    original_language TEXT DEFAULT 'fr',
    original_publication_year INTEGER,
    summary TEXT,
    genres TEXT,                        -- JSON array
    themes TEXT,                        -- JSON array
    awards TEXT,                        -- JSON array
    series TEXT,
    series_number INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Table `editions`
```sql
CREATE TABLE editions (
    isbn TEXT PRIMARY KEY,
    work_id TEXT NOT NULL,
    publisher TEXT DEFAULT '',
    publication_year INTEGER,
    publication_date TEXT,
    language TEXT DEFAULT 'fr',

    -- Format
    format TEXT,
    pages INTEGER,
    dimensions_height REAL,
    dimensions_width REAL,
    dimensions_thickness REAL,
    weight INTEGER,

    -- Images
    cover_front_url TEXT,
    cover_back_url TEXT,
    cover_spine_url TEXT,
    cover_color TEXT,

    -- Commercial
    price REAL,
    currency TEXT DEFAULT 'EUR',
    ean TEXT,

    -- Métadonnées
    edition_number INTEGER,
    collection TEXT,
    translator TEXT,
    illustrator TEXT,
    preface_by TEXT,

    -- État
    condition TEXT DEFAULT 'Neuf',
    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (work_id) REFERENCES oeuvres(work_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX idx_editions_work_id ON editions(work_id);
CREATE INDEX idx_editions_publisher ON editions(publisher);
CREATE INDEX idx_oeuvres_author ON oeuvres(author);
CREATE INDEX idx_oeuvres_title ON oeuvres(title);
```

## 🎨 Cas d'usage pour l'OCR

### Scénario 1 : Ajout d'un nouveau livre via photo

1. **L'utilisateur prend en photo** la couverture et la 4ème de couverture
2. **OCR extrait** :
   - ISBN (code-barres ou texte)
   - Titre
   - Auteur
   - Éditeur
   - Prix
   - Résumé (4ème de couverture)
3. **Le système vérifie** si l'œuvre existe déjà (par titre/auteur)
4. **Si l'œuvre existe** :
   - Créer seulement une nouvelle Édition
   - Lier à l'œuvre existante
5. **Si l'œuvre n'existe pas** :
   - Créer l'Œuvre
   - Créer l'Édition
   - Lier les deux

### Scénario 2 : Recherche d'un livre

**Par ISBN :**
```
GET /editions/978-2-07-036222-6
→ Retourne l'édition + l'œuvre parente
```

**Par titre d'œuvre :**
```
GET /oeuvres/search?q=Les Misérables
→ Retourne l'œuvre
GET /oeuvres/WORK-001/editions
→ Retourne toutes les éditions de cette œuvre
```

## 🛠️ Enums disponibles

### BookFormat
```python
POCHE, BROCHE, RELIE, GRAND_FORMAT,
EBOOK, EPUB, PDF, AUDIO, KINDLE,
LUXE, COLLECTOR
```

### Genre
```python
# Fiction
ROMAN, NOUVELLE, SCIENCE_FICTION, FANTASY,
POLICIER, THRILLER, HORREUR, ROMANCE,
HISTORIQUE, AVENTURE, YOUNG_ADULT, DYSTOPIE

# Non-fiction
BIOGRAPHIE, AUTOBIOGRAPHIE, ESSAI,
DOCUMENTAIRE, HISTOIRE, PHILOSOPHIE,
PSYCHOLOGIE, SCIENCES, POLITIQUE, RELIGION

# Autres
POESIE, THEATRE, BD, MANGA, COMICS,
CUISINE, ART, VOYAGE,
DEVELOPPEMENT_PERSONNEL, JEUNESSE, SCOLAIRE
```

## 📈 Avantages de cette architecture

### ✅ Évite la duplication
- Les informations de l'œuvre (auteur, titre original, résumé) sont stockées une seule fois
- Seules les spécificités de chaque édition sont dupliquées

### ✅ Facilite l'OCR
- L'OCR peut identifier rapidement si une œuvre existe déjà
- Permet de détecter automatiquement les éditions multiples du même livre

### ✅ Gestion des traductions
- Une traduction = nouvelle œuvre OU nouvelle édition selon le cas
- Possibilité de lier les traductions à l'œuvre originale

### ✅ Statistiques précises
- Combien d'œuvres différentes ? → COUNT(oeuvres)
- Combien d'exemplaires physiques ? → COUNT(editions WHERE format NOT IN digital)
- Quel est l'auteur le plus présent ? → GROUP BY oeuvres.author

### ✅ Recherche intelligente
- Recherche par œuvre → tous les formats disponibles
- Recherche par ISBN → édition exacte
- Filtrage par format → uniquement les éditions numériques, etc.

## 🔄 Migration depuis l'ancien modèle

L'ancien modèle `Livre` peut être transformé ainsi :
```python
# Ancien: 1 Livre = 1 entrée
Livre(isbn="123", title="Les Misérables", author="Victor Hugo")

# Nouveau: 1 Œuvre + 1 Édition
Oeuvre(work_id="WORK-001", title="Les Misérables", author="Victor Hugo")
Edition(isbn="123", work_id="WORK-001", publisher="Gallimard")
```

## 🚀 Prochaines étapes

1. Créer les repositories pour Oeuvre et Edition
2. Mettre à jour l'API avec les nouveaux endpoints
3. Créer l'interface Streamlit pour gérer les deux entités
4. Implémenter l'OCR pour extraire les données des couvertures
5. Ajouter la détection automatique des œuvres existantes
