# 📚 GUIDE D'EXERCICES - Bibliothèque Python

## 🎯 Objectif
Développer une application web de gestion de bibliothèque en implémentant progressivement les fonctionnalités.

---

## 📝 PARTIE 1 : Modèles (POO)

### 📘 Fichier: `models/livre.py`

**TODO 1 : Constructeur de la classe Livre**
```python
def __init__(self, titre: str, auteur: str, annee: int, isbn: str = ""):
    self.titre = titre
    self.auteur = auteur
    self.annee = annee
    self.isbn = isbn
    self.date_ajout = datetime.now().strftime("%Y-%m-%d")
    self.lu = False
    self.note = None
```

**TODO 2 : Méthode abstraite**
```python
@abstractmethod
def get_type(self) -> str:
    pass
```
💡 Les classes enfants DOIVENT implémenter cette méthode.

**TODO 3 : Property info_complete**
```python
@property
def info_complete(self) -> str:
    info = f"{self.titre} - {self.auteur} ({self.annee})"
    if self.lu:
        info += " ✓"
    if self.note:
        info += f" [{self.note}/5]"
    return info
```

**TODO 4 : Marquer comme lu**
```python
def marquer_comme_lu(self, note: int = None):
    self.lu = True
    if note and 0 <= note <= 5:
        self.note = note
```

**TODO 5 : Conversion en dictionnaire**
```python
def to_dict(self) -> dict:
    return {
        'type': self.get_type(),
        'titre': self.titre,
        'auteur': self.auteur,
        'annee': self.annee,
        'isbn': self.isbn,
        'date_ajout': self.date_ajout,
        'lu': self.lu,
        'note': self.note
    }
```

**TODO 6 : Méthode __str__**
```python
def __str__(self) -> str:
    statut = "Lu" if self.lu else "Non lu"
    return f"[{self.get_type()}] {self.info_complete} - {statut}"
```

**TODO 7 : Méthode __eq__ (égalité)**
```python
def __eq__(self, other) -> bool:
    if not isinstance(other, Livre):
        return False
    return self.isbn == other.isbn if self.isbn else self.titre == other.titre
```

---

### 📱 Fichier: `models/livre_numerique.py`

**TODO 8-11 : Héritage**
```python
def __init__(self, titre, auteur, annee, isbn="", format_fichier="PDF", taille_mo=0):
    super().__init__(titre, auteur, annee, isbn)  # Appel parent
    self.format_fichier = format_fichier.upper()
    self.taille_mo = taille_mo

def get_type(self) -> str:
    return "eBook"

def to_dict(self) -> dict:
    data = super().to_dict()  # Récupère dict parent
    data['format_fichier'] = self.format_fichier
    data['taille_mo'] = self.taille_mo
    return data

def __str__(self) -> str:
    base = super().__str__()
    return f"{base} [{self.format_fichier}, {self.taille_mo}Mo]"
```

---

### 📰 Fichier: `models/magazine.py`

**TODO 12-15 : Même logique que LivreNumerique**
- Constructeur avec `super().__init__()`
- Attributs spécifiques: `numero`, `mois`
- `get_type()` retourne `"Magazine"`
- `to_dict()` et `__str__()` ajoutent les infos du magazine

---

## 🔧 PARTIE 2 : Services (Logique métier)

### 📚 Fichier: `services/bibliotheque.py`

**TODO 16 : Ajouter un livre**
```python
def ajouter(self, livre: Livre) -> bool:
    if livre not in self.livres:
        self.livres.append(livre)
        return True
    return False
```

**TODO 17 : Supprimer**
```python
def supprimer(self, livre: Livre) -> bool:
    if livre in self.livres:
        self.livres.remove(livre)
        return True
    return False
```

**TODO 18 : Rechercher**
```python
def rechercher(self, query: str) -> List[Livre]:
    query = query.lower()
    return [
        livre for livre in self.livres
        if query in livre.titre.lower() or query in livre.auteur.lower()
    ]
```

**TODO 19 : Filtrer par type**
```python
def filtrer_par_type(self, type_livre: str) -> List[Livre]:
    return [livre for livre in self.livres if livre.get_type() == type_livre]
```

**TODO 20 : Statistiques**
```python
def statistiques(self) -> dict:
    total = len(self.livres)
    lus = len([l for l in self.livres if l.lu])
    
    return {
        'total': total,
        'lus': lus,
        'non_lus': total - lus,
        'ebooks': len(self.filtrer_par_type("eBook")),
        'magazines': len(self.filtrer_par_type("Magazine")),
        'pourcentage_lus': round(lus / total * 100, 1) if total > 0 else 0
    }
```

---

### 💾 Fichier: `services/stockage.py`

**TODO 21 : Sauvegarder en JSON**
```python
def sauvegarder(self, livres: List[Livre]) -> bool:
    try:
        data = [livre.to_dict() for livre in livres]
        with open(self.fichier, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Erreur: {e}")
        return False
```

**TODO 22 : Charger depuis JSON**
```python
def charger(self) -> List[Livre]:
    if not self.fichier.exists():
        return []
    
    try:
        with open(self.fichier, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        livres = []
        for item in data:
            livre = self._dict_to_livre(item)
            if livre:
                livres.append(livre)
        
        return livres
    except Exception as e:
        print(f"Erreur: {e}")
        return []
```

**TODO 23 : Convertir dict → Livre**
```python
def _dict_to_livre(self, data: dict) -> Livre | None:
    try:
        type_livre = data.get('type')
        
        if type_livre == "eBook":
            livre = LivreNumerique(
                titre=data['titre'],
                auteur=data['auteur'],
                annee=data['annee'],
                isbn=data.get('isbn', ''),
                format_fichier=data.get('format_fichier', 'PDF'),
                taille_mo=data.get('taille_mo', 0)
            )
        elif type_livre == "Magazine":
            livre = Magazine(
                titre=data['titre'],
                auteur=data['auteur'],
                annee=data['annee'],
                isbn=data.get('isbn', ''),
                numero=data.get('numero', 1),
                mois=data.get('mois', '')
            )
        else:
            return None
        
        # Restaurer propriétés
        livre.date_ajout = data.get('date_ajout', livre.date_ajout)
        livre.lu = data.get('lu', False)
        livre.note = data.get('note')
        
        return livre
    except Exception as e:
        print(f"Erreur: {e}")
        return None
```

---

## 🎨 PARTIE 3 : Interface Streamlit

Voir `STREAMLIT_EXEMPLES.md` pour des exemples détaillés !

---

## ✅ Checklist de progression

### Modèles
- [ ] TODO 1-7 : Classe Livre complète
- [ ] TODO 8-11 : LivreNumerique
- [ ] TODO 12-15 : Magazine
- [ ] Tester: créer instances et vérifier `__str__`, `to_dict()`

### Services
- [ ] TODO 16-20 : Bibliothèque (ajouter, rechercher, stats)
- [ ] TODO 21-23 : Stockage JSON
- [ ] Tester: sauvegarder/charger des livres

### Interface (déjà fonctionnelle)
- [ ] Comprendre la structure de `app.py`
- [ ] Personnaliser l'interface
- [ ] Ajouter des fonctionnalités

---

## 🚀 Pour tester

```python
# Test rapide dans un fichier test.py
from models import LivreNumerique, Magazine

livre = LivreNumerique("Python Crash Course", "Eric Matthes", 2023, "", "PDF", 12.5)
print(livre)
livre.marquer_comme_lu(5)
print(livre.to_dict())
```

---

## 💡 Améliorations bonus

1. **Ajouter une classe LivrePapier**
   - Attributs: nb_pages, editeur, etat (neuf/bon/abîmé)

2. **Système de catégories**
   - Ajouter un attribut `categories: List[str]`
   - Filtrer par catégorie

3. **Export CSV**
   - Méthode dans Stockage pour exporter en CSV

4. **Graphiques**
   - Utiliser `st.bar_chart()` pour visualiser les stats

5. **API Google Books**
   - Récupérer automatiquement les infos d'un livre via son ISBN
