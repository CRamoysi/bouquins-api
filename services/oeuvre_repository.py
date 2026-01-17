"""
Repository en mémoire pour les Oeuvres
"""

from typing import List, Optional, Dict
from models.oeuvre import Oeuvre
from services.repository import IRepository
from unicorn.u_string import U_String


class OeuvreMemoryRepository(IRepository[Oeuvre]):
    """
    Repository en mémoire pour stocker les œuvres littéraires
    Utilise un dictionnaire {work_id: Oeuvre}
    """

    def __init__(self) -> None:
        """Initialise le repository avec un dictionnaire vide"""
        self._oeuvres: Dict[str, Oeuvre] = {}

    def get_by_id(self, work_id: str) -> Optional[Oeuvre]:
        """
        Récupère une œuvre par son work_id

        Args:
            work_id: L'identifiant de l'œuvre

        Returns:
            L'œuvre trouvée ou None
        """
        return self._oeuvres.get(work_id)

    def get_all(self) -> List[Oeuvre]:
        """
        Récupère toutes les œuvres

        Returns:
            Liste de toutes les œuvres
        """
        return list(self._oeuvres.values())

    def add(self, oeuvre: Oeuvre) -> bool:
        """
        Ajoute une nouvelle œuvre

        Args:
            oeuvre: L'œuvre à ajouter

        Returns:
            True si l'ajout a réussi, False si le work_id existe déjà
        """
        if oeuvre.work_id in self._oeuvres:
            return False

        self._oeuvres[oeuvre.work_id] = oeuvre
        return True

    def update(self, oeuvre: Oeuvre) -> bool:
        """
        Met à jour une œuvre existante

        Args:
            oeuvre: L'œuvre avec les nouvelles données

        Returns:
            True si la mise à jour a réussi, False si l'œuvre n'existe pas
        """
        if oeuvre.work_id not in self._oeuvres:
            return False

        self._oeuvres[oeuvre.work_id] = oeuvre
        return True

    def delete(self, work_id: str) -> bool:
        """
        Supprime une œuvre

        Args:
            work_id: L'identifiant de l'œuvre à supprimer

        Returns:
            True si la suppression a réussi, False si l'œuvre n'existe pas
        """
        if work_id not in self._oeuvres:
            return False

        del self._oeuvres[work_id]
        return True

    def search(self, query: str) -> List[Oeuvre]:
        """
        Recherche des œuvres par titre ou auteur (recherche floue)

        Args:
            query: La requête de recherche

        Returns:
            Liste des œuvres correspondantes
        """
        if not query.strip():
            return []

        # Normaliser et diviser la requête en mots
        query_words = [word for word in U_String(query).remove_diacritics().lower().split() if word]

        def oeuvre_matches(oeuvre: Oeuvre) -> bool:
            combined_text = U_String(f"{oeuvre.title} {oeuvre.author}")
            # Une œuvre correspond si tous les mots de la requête correspondent (avec tolérance)
            return all(combined_text.fuzzy_match(word) for word in query_words)

        return [oeuvre for oeuvre in self._oeuvres.values() if oeuvre_matches(oeuvre)]

    def get_by_author(self, author: str) -> List[Oeuvre]:
        """
        Récupère toutes les œuvres d'un auteur

        Args:
            author: Le nom de l'auteur

        Returns:
            Liste des œuvres de cet auteur
        """
        author_normalized = U_String(author).remove_diacritics().lower()
        return [
            oeuvre for oeuvre in self._oeuvres.values()
            if U_String(oeuvre.author).remove_diacritics().lower() == author_normalized
        ]

    def get_by_series(self, series: str) -> List[Oeuvre]:
        """
        Récupère toutes les œuvres d'une série

        Args:
            series: Le nom de la série

        Returns:
            Liste des œuvres de cette série, triées par numéro
        """
        series_normalized = U_String(series).remove_diacritics().lower()
        oeuvres = [
            oeuvre for oeuvre in self._oeuvres.values()
            if oeuvre.series and U_String(oeuvre.series).remove_diacritics().lower() == series_normalized
        ]
        return sorted(oeuvres, key=lambda o: o.series_number or 0)
