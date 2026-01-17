# 🔄 Migration vers la nouvelle architecture

## ✅ Nettoyage effectué

### Fichiers supprimés (obsolètes)

| Fichier | Raison | Remplacé par |
|---------|--------|--------------|
| `const/reading_status.py` | Statuts de lecture retirés du catalogue | ❌ Supprimé |
| `models/bouquin.py` | Ancien modèle abstrait | `models/oeuvre.py` |
| `models/livre.py` | Ancien modèle concret | `models/edition.py` |
| `services/stockage.py` | Fichier vide jamais utilisé | ❌ Supprimé |
| `test_livre.json` | Fichier temporaire de test | ❌ Supprimé |

### Fichiers mis à jour

| Fichier | Modifications |
|---------|---------------|
| `models/__init__.py` | Export `Oeuvre` et `Edition` |
| `const/__init__.py` | Export `BookFormat` et `Genre` |

### Fichiers conservés (à mettre à jour)

| Fichier | Statut | Action requise |
|---------|--------|----------------|
| `services/database.py` | ⚠️ Ancien schéma | Réécrire pour Oeuvre + Edition |
| `services/bibliotheque.py` | ⚠️ Ancien modèle | Adapter pour la nouvelle architecture |
| `services/repository.py` | ✅ OK | Interface générique, peut être réutilisée |
| `services/memory_repository.py` | ✅ OK | Garder pour tests |
| `api.py` | ⚠️ Anciens modèles | Réécrire endpoints |
| `app.py` | ⚠️ Anciens modèles | Réécrire interface Streamlit |
| `tests/*.py` | ⚠️ Anciens modèles | Réécrire tous les tests |

### Bases de données existantes

| Fichier | Statut | Action |
|---------|--------|---------|
| `bibliotheque.db` | ⚠️ Ancien schéma | Conserver pour migration des données |
| `catalogue.db` | ⚠️ Ancien schéma | Conserver pour migration des données |

## 📋 Nouvelle structure du projet

```
bibliotheque/
├── const/                          # ✅ Énumérations
│   ├── __init__.py                 # ✨ NOUVEAU
│   ├── book_format.py              # ✨ NOUVEAU
│   └── genre.py                    # ✨ NOUVEAU
│
├── models/                         # ✅ Modèles de domaine
│   ├── __init__.py                 # 🔄 MIS À JOUR
│   ├── oeuvre.py                   # ✨ NOUVEAU
│   └── edition.py                  # ✨ NOUVEAU
│
├── services/                       # ⚠️ À METTRE À JOUR
│   ├── __init__.py
│   ├── repository.py               # ✅ OK (interface générique)
│   ├── memory_repository.py        # ✅ OK (pour tests)
│   ├── oeuvre_repository.py        # ⏳ À CRÉER
│   ├── edition_repository.py       # ⏳ À CRÉER
│   ├── database.py                 # ⚠️ À RÉÉCRIRE
│   └── bibliotheque.py             # ⚠️ À ADAPTER
│
├── unicorn/                        # ✅ Utilitaires (OK)
│   └── u_string.py
│
├── tests/                          # ⚠️ À RÉÉCRIRE
│   ├── test_oeuvre.py              # ⏳ À CRÉER
│   ├── test_edition.py             # ⏳ À CRÉER
│   └── ...
│
├── ARCHITECTURE.md                 # ✨ NOUVEAU - Documentation
├── MIGRATION.md                    # ✨ NOUVEAU - Ce fichier
├── API_README.md                   # ⚠️ À METTRE À JOUR
├── api.py                          # ⚠️ À RÉÉCRIRE
├── app.py                          # ⚠️ À RÉÉCRIRE
├── requirements.txt                # ✅ OK
└── pytest.ini                      # ✅ OK
```

## 🎯 Prochaines étapes

### Étape 1 : Créer les repositories ⏳
- [ ] `services/oeuvre_repository.py` - Repository pour les œuvres
- [ ] `services/edition_repository.py` - Repository pour les éditions
- [ ] Mettre à jour `services/database.py` avec les 2 nouvelles tables

### Étape 2 : Mettre à jour l'API ⏳
- [ ] Créer `api_models.py` pour Oeuvre et Edition
- [ ] Réécrire `api.py` avec les nouveaux endpoints
- [ ] Mettre à jour `API_README.md`

### Étape 3 : Mettre à jour Streamlit ⏳
- [ ] Réécrire `app.py` pour gérer Oeuvres + Editions
- [ ] Interface pour lier des éditions à une œuvre

### Étape 4 : Tests ⏳
- [ ] Tests unitaires pour Oeuvre
- [ ] Tests unitaires pour Edition
- [ ] Tests d'intégration avec repositories

### Étape 5 : Migration des données ⏳
- [ ] Script pour migrer `bibliotheque.db` vers le nouveau schéma
- [ ] Créer des œuvres depuis les anciens livres
- [ ] Transformer livres en éditions

### Étape 6 : Fonctionnalités OCR 🚀
- [ ] Module d'extraction d'informations depuis images
- [ ] Détection automatique des œuvres existantes
- [ ] Interface pour photographier les couvertures

## 📊 Schéma de migration des données

### Ancien modèle → Nouveau modèle

```python
# ANCIEN (table: livres)
Livre:
  isbn: "978-2-07-036222-6"
  title: "Les Misérables"
  author: "Victor Hugo"
  publisher: "Gallimard"
  publication_year: 2020
```

↓ **Migration** ↓

```python
# NOUVEAU (tables: oeuvres + editions)

# 1. Créer ou trouver l'œuvre
Oeuvre:
  work_id: "WORK-001" (généré)
  title: "Les Misérables"
  author: "Victor Hugo"
  original_publication_year: 1862  # À rechercher

# 2. Créer l'édition liée
Edition:
  isbn: "978-2-07-036222-6"
  work_id: "WORK-001"  # Référence
  publisher: "Gallimard"
  publication_year: 2020
```

## 🔧 Script de migration (à créer)

```python
# migrate_database.py

def migrate():
    # 1. Charger toutes les anciennes données
    old_livres = load_from_old_db()

    # 2. Grouper par (titre, auteur) pour détecter les œuvres
    oeuvres_map = {}
    for livre in old_livres:
        key = (livre.title, livre.author)
        if key not in oeuvres_map:
            # Créer nouvelle œuvre
            oeuvre = create_oeuvre(livre)
            oeuvres_map[key] = oeuvre

        # Créer édition liée
        edition = create_edition(livre, oeuvres_map[key].work_id)

    # 3. Sauvegarder dans nouvelle BDD
    save_to_new_db(oeuvres_map.values(), editions)
```

## 📝 Notes importantes

### Différences clés

**AVANT (ancien modèle) :**
- 1 table `livres`
- Duplication des données (auteur/titre répétés pour chaque ISBN)
- Pas de gestion des éditions multiples
- Pas de champs pour images de couvertures

**APRÈS (nouveau modèle) :**
- 2 tables `oeuvres` + `editions` avec relation 1:N
- Zéro duplication (œuvre stockée une fois)
- Gestion native des éditions multiples
- Champs `cover_front_url`, `cover_back_url` pour OCR
- Attributs enrichis (dimensions, poids, format, etc.)

### Avantages de la migration

✅ **Performance** : Moins de duplication = moins d'espace disque
✅ **Cohérence** : Une seule source de vérité pour l'œuvre
✅ **Extensibilité** : Facile d'ajouter de nouvelles éditions
✅ **OCR-ready** : Prêt pour l'extraction automatique depuis photos
✅ **Statistiques** : Distinction claire entre "œuvres uniques" et "exemplaires"

## 🎨 Exemple concret après migration

**Scénario : Vous avez "Les Misérables" en 3 formats**

**AVANT :**
```
livres:
  - isbn: 978-2-07-036222-6, title: Les Misérables, author: Victor Hugo, publisher: Gallimard
  - isbn: 978-2-07-010142-1, title: Les Misérables, author: Victor Hugo, publisher: Pléiade
  - isbn: B00ABC123, title: Les Misérables, author: Victor Hugo, publisher: Amazon
```
→ 3 entrées, auteur/titre dupliqués 3 fois

**APRÈS :**
```
oeuvres:
  - work_id: WORK-001, title: Les Misérables, author: Victor Hugo

editions:
  - isbn: 978-2-07-036222-6, work_id: WORK-001, publisher: Gallimard, format: POCHE
  - isbn: 978-2-07-010142-1, work_id: WORK-001, publisher: Pléiade, format: RELIE
  - isbn: B00ABC123, work_id: WORK-001, publisher: Amazon, format: KINDLE
```
→ 1 œuvre + 3 éditions, organisation claire
