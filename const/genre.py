"""
Énumération des genres littéraires
"""
from enum import Enum


class Genre(Enum):
    """Genres littéraires principaux"""
    # Fiction
    ROMAN = "Roman"
    NOUVELLE = "Nouvelle"
    SCIENCE_FICTION = "Science-fiction"
    FANTASY = "Fantasy"
    POLICIER = "Policier"
    THRILLER = "Thriller"
    HORREUR = "Horreur"
    ROMANCE = "Romance"
    HISTORIQUE = "Roman historique"
    AVENTURE = "Aventure"
    YOUNG_ADULT = "Young Adult"
    DYSTOPIE = "Dystopie"

    # Non-fiction
    BIOGRAPHIE = "Biographie"
    AUTOBIOGRAPHIE = "Autobiographie"
    ESSAI = "Essai"
    DOCUMENTAIRE = "Documentaire"
    HISTOIRE = "Histoire"
    PHILOSOPHIE = "Philosophie"
    PSYCHOLOGIE = "Psychologie"
    SCIENCES = "Sciences"
    POLITIQUE = "Politique"
    RELIGION = "Religion"

    # Autres
    POESIE = "Poésie"
    THEATRE = "Théâtre"
    BD = "Bande dessinée"
    MANGA = "Manga"
    COMICS = "Comics"
    CUISINE = "Cuisine"
    ART = "Art"
    VOYAGE = "Voyage"
    DEVELOPPEMENT_PERSONNEL = "Développement personnel"
    JEUNESSE = "Jeunesse"
    SCOLAIRE = "Scolaire"
    AUTRE = "Autre"

    @classmethod
    def all_genres(cls):
        """Retourne tous les genres disponibles"""
        return list(cls)

    @classmethod
    def fiction_genres(cls):
        """Retourne les genres de fiction"""
        return [
            cls.ROMAN, cls.NOUVELLE, cls.SCIENCE_FICTION, cls.FANTASY,
            cls.POLICIER, cls.THRILLER, cls.HORREUR, cls.ROMANCE,
            cls.HISTORIQUE, cls.AVENTURE, cls.YOUNG_ADULT, cls.DYSTOPIE
        ]

    @classmethod
    def nonfiction_genres(cls):
        """Retourne les genres de non-fiction"""
        return [
            cls.BIOGRAPHIE, cls.AUTOBIOGRAPHIE, cls.ESSAI, cls.DOCUMENTAIRE,
            cls.HISTOIRE, cls.PHILOSOPHIE, cls.PSYCHOLOGIE, cls.SCIENCES,
            cls.POLITIQUE, cls.RELIGION
        ]
