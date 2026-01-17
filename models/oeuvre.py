"""
Modèle Oeuvre - Représente une œuvre littéraire (indépendante de ses éditions)
"""
from typing import Optional, List
from const.genre import Genre


class Oeuvre:
    """
    Classe représentant une œuvre littéraire
    Une œuvre peut avoir plusieurs éditions avec des ISBN différents

    Attributs:
        work_id: Identifiant unique de l'œuvre
        title: Titre original de l'œuvre
        author: Auteur(s) principal(aux)
        co_authors: Co-auteurs éventuels
        original_language: Langue originale
        original_publication_year: Année de première publication
        summary: Résumé de l'œuvre
        genres: Genres littéraires (liste)
        themes: Thèmes abordés
        awards: Prix littéraires reçus
        series: Nom de la série (si applicable)
        series_number: Numéro dans la série
    """

    def __init__(self, work_id: str) -> None:
        """
        Initialise une nouvelle œuvre

        Args:
            work_id: Identifiant unique (peut être généré automatiquement)
        """
        self.work_id: str = work_id
        self.title: str = ""
        self.author: str = ""
        self.co_authors: List[str] = []

        # Informations de publication originale
        self.original_language: str = "fr"  # Par défaut français
        self._original_publication_year: Optional[int] = None

        # Description
        self.summary: Optional[str] = None
        self.genres: List[Genre] = []
        self.themes: List[str] = []

        # Distinctions
        self.awards: List[str] = []

        # Série
        self.series: Optional[str] = None
        self.series_number: Optional[int] = None

    @property
    def original_publication_year(self) -> Optional[int]:
        """Getter pour l'année de publication originale"""
        return self._original_publication_year

    @original_publication_year.setter
    def original_publication_year(self, year: Optional[int]) -> None:
        """Setter pour l'année de publication originale avec validation"""
        if year is not None and (year < -3000 or year > 3000):
            raise ValueError("L'année de publication doit être entre -3000 et 3000")
        self._original_publication_year = year

    @property
    def full_title(self) -> str:
        """Retourne le titre complet avec série si applicable"""
        if self.series and self.series_number:
            return f"{self.series} - Tome {self.series_number}: {self.title}"
        elif self.series:
            return f"{self.series}: {self.title}"
        return self.title

    @property
    def authors_list(self) -> List[str]:
        """Retourne la liste complète des auteurs"""
        authors = [self.author] if self.author else []
        authors.extend(self.co_authors)
        return authors

    def add_genre(self, genre: Genre) -> None:
        """Ajoute un genre littéraire"""
        if genre not in self.genres:
            self.genres.append(genre)

    def remove_genre(self, genre: Genre) -> None:
        """Retire un genre littéraire"""
        if genre in self.genres:
            self.genres.remove(genre)

    def add_theme(self, theme: str) -> None:
        """Ajoute un thème"""
        if theme and theme not in self.themes:
            self.themes.append(theme)

    def add_award(self, award: str) -> None:
        """Ajoute un prix littéraire"""
        if award and award not in self.awards:
            self.awards.append(award)

    def add_co_author(self, author: str) -> None:
        """Ajoute un co-auteur"""
        if author and author not in self.co_authors:
            self.co_authors.append(author)

    def __repr__(self) -> str:
        """Représentation textuelle de l'œuvre"""
        authors = ", ".join(self.authors_list)
        return f"Oeuvre({self.work_id}): {self.title} par {authors} ({self.original_publication_year})"

    def __str__(self) -> str:
        """Version lisible de l'œuvre"""
        return f"{self.full_title} par {self.author}"
