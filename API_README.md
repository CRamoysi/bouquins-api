# 📚 API Catalogue de Livres

API REST complète pour gérer un catalogue de livres avec recherche intelligente.

## 🚀 Démarrage rapide

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Lancer l'API

```bash
# Méthode 1 : Avec uvicorn directement
uvicorn api:app --reload

# Méthode 2 : Avec Python
python api.py

# Méthode 3 : Avec uvicorn et options personnalisées
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

L'API sera accessible sur : **http://localhost:8000**

## 📖 Documentation interactive

FastAPI génère automatiquement une documentation interactive :

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🎯 Endpoints disponibles

### Informations

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Informations sur l'API |
| GET | `/stats` | Statistiques du catalogue |

### CRUD Livres

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/livres` | Liste tous les livres (pagination) |
| GET | `/livres/{isbn}` | Récupère un livre par ISBN |
| POST | `/livres` | Ajoute un nouveau livre |
| PUT | `/livres/{isbn}` | Met à jour un livre |
| DELETE | `/livres/{isbn}` | Supprime un livre |

### Recherche

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/livres/search/?q=terme` | Recherche intelligente (floue) |
| GET | `/livres/author/{author}` | Livres par auteur |
| GET | `/livres/year/{year}` | Livres par année |

## 💡 Exemples d'utilisation

### 1. Récupérer tous les livres

```bash
curl http://localhost:8000/livres
```

Avec pagination :
```bash
curl "http://localhost:8000/livres?skip=0&limit=10"
```

### 2. Ajouter un nouveau livre

```bash
curl -X POST "http://localhost:8000/livres" \
  -H "Content-Type: application/json" \
  -d '{
    "isbn": "978-2-07-036222-6",
    "title": "Les Misérables",
    "author": "Victor Hugo",
    "publisher": "Gallimard",
    "publication_year": 1862,
    "summary": "Un roman historique et social..."
  }'
```

### 3. Rechercher un livre par ISBN

```bash
curl http://localhost:8000/livres/978-2-07-036222-6
```

### 4. Recherche intelligente

```bash
# Recherche floue (tolérante aux fautes)
curl "http://localhost:8000/livres/search/?q=victor%20hugo"

# Avec limite de résultats
curl "http://localhost:8000/livres/search/?q=hugo&limit=5"
```

### 5. Mettre à jour un livre

```bash
curl -X PUT "http://localhost:8000/livres/978-2-07-036222-6" \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "Nouveau résumé mis à jour"
  }'
```

### 6. Supprimer un livre

```bash
curl -X DELETE http://localhost:8000/livres/978-2-07-036222-6
```

### 7. Statistiques du catalogue

```bash
curl http://localhost:8000/stats
```

### 8. Livres par auteur

```bash
curl http://localhost:8000/livres/author/Victor%20Hugo
```

### 9. Livres par année

```bash
curl http://localhost:8000/livres/year/1862
```

## 📊 Exemples avec Python (requests)

```python
import requests

# URL de base
BASE_URL = "http://localhost:8000"

# 1. Ajouter un livre
nouveau_livre = {
    "isbn": "978-2-07-036222-6",
    "title": "Les Misérables",
    "author": "Victor Hugo",
    "publisher": "Gallimard",
    "publication_year": 1862,
    "summary": "Un roman historique et social..."
}

response = requests.post(f"{BASE_URL}/livres", json=nouveau_livre)
print(response.json())

# 2. Récupérer tous les livres
response = requests.get(f"{BASE_URL}/livres")
livres = response.json()
print(f"Total: {len(livres)} livres")

# 3. Recherche intelligente
response = requests.get(f"{BASE_URL}/livres/search/", params={"q": "Victor Hugo"})
resultats = response.json()
print(f"Résultats trouvés: {len(resultats)}")

# 4. Récupérer un livre par ISBN
isbn = "978-2-07-036222-6"
response = requests.get(f"{BASE_URL}/livres/{isbn}")
livre = response.json()
print(f"Titre: {livre['title']}")

# 5. Mettre à jour un livre
update_data = {"summary": "Nouveau résumé"}
response = requests.put(f"{BASE_URL}/livres/{isbn}", json=update_data)
print(response.json())

# 6. Supprimer un livre
response = requests.delete(f"{BASE_URL}/livres/{isbn}")
print(response.json())

# 7. Statistiques
response = requests.get(f"{BASE_URL}/stats")
stats = response.json()
print(f"Total de livres: {stats['total_livres']}")
```

## 🔧 Configuration

### Base de données

L'API utilise SQLite avec le fichier `catalogue.db` créé automatiquement au premier lancement.

### CORS

Par défaut, l'API accepte les requêtes de toutes les origines (`*`). En production, modifiez cette configuration dans `api.py` :

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://monsite.com"],  # Spécifiez vos domaines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📝 Modèle de données

### LivreCreate (POST /livres)

```json
{
  "isbn": "string (requis)",
  "title": "string (requis)",
  "author": "string (requis)",
  "publisher": "string (optionnel)",
  "publication_year": "integer -1000 à 3000 (optionnel)",
  "summary": "string (optionnel)"
}
```

### LivreResponse (Réponse)

```json
{
  "isbn": "string",
  "title": "string",
  "author": "string",
  "publisher": "string",
  "publication_year": "integer ou null",
  "summary": "string ou null",
  "type": "Livre"
}
```

## ⚡ Fonctionnalités avancées

### Recherche floue

La recherche utilise l'algorithme de Levenshtein pour être tolérante aux fautes de frappe :
- Recherche "vicor huho" trouve "Victor Hugo"
- Recherche "misrable" trouve "Misérables"

### Pagination

Utilisez les paramètres `skip` et `limit` pour paginer les résultats :
```bash
# Page 1 (10 premiers livres)
curl "http://localhost:8000/livres?skip=0&limit=10"

# Page 2 (livres 11-20)
curl "http://localhost:8000/livres?skip=10&limit=10"
```

## 🛠️ Technologies utilisées

- **FastAPI** : Framework web moderne et rapide
- **Pydantic** : Validation des données
- **SQLite** : Base de données légère
- **Uvicorn** : Serveur ASGI haute performance
- **Pattern Repository** : Abstraction de la couche de persistance

## 📦 Structure du projet

```
bibliotheque/
├── api.py              # Point d'entrée de l'API
├── api_models.py       # Modèles Pydantic pour l'API
├── app.py              # Application Streamlit (interface web)
├── models/             # Modèles de domaine (POO)
│   ├── bouquin.py
│   └── livre.py
├── services/           # Logique métier et repositories
│   ├── bibliotheque.py
│   ├── database.py
│   └── repository.py
├── catalogue.db        # Base de données SQLite (créé automatiquement)
└── requirements.txt    # Dépendances Python
```

## 🎓 Pour aller plus loin

### Tester l'API avec HTTPie

```bash
# Installer HTTPie
pip install httpie

# Exemples
http GET localhost:8000/livres
http POST localhost:8000/livres isbn="123" title="Test" author="Auteur"
http DELETE localhost:8000/livres/123
```

### Utiliser l'API avec JavaScript (fetch)

```javascript
// Récupérer tous les livres
fetch('http://localhost:8000/livres')
  .then(response => response.json())
  .then(data => console.log(data));

// Ajouter un livre
fetch('http://localhost:8000/livres', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    isbn: "978-2-07-036222-6",
    title: "Les Misérables",
    author: "Victor Hugo",
    publisher: "Gallimard",
    publication_year: 1862
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## 🐛 Gestion des erreurs

L'API renvoie des codes HTTP appropriés :

- `200 OK` : Succès
- `201 Created` : Ressource créée
- `400 Bad Request` : Données invalides
- `404 Not Found` : Ressource non trouvée
- `409 Conflict` : Conflit (ex: ISBN déjà existant)
- `500 Internal Server Error` : Erreur serveur

Exemple de réponse d'erreur :
```json
{
  "detail": "Aucun livre trouvé avec l'ISBN: 123456"
}
```
