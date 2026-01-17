"""
Repository en mémoire pour les Editions
"""

from typing import List, Optional, Dict
from models.edition import Edition
from services.repository import IRepository
from unicorn.u_string import U_String


class EditionMemoryRepository(IRepository[Edition]):
    """
    Repository en mémoire pour stocker les éditions de livres
    Utilise un dictionnaire {isbn: Edition}
    """

    def __init__(self) -> None:
        """Initialise le repository avec un dictionnaire vide"""
        self._editions: Dict[str, Edition] = {}

    def get_by_id(self, isbn: str) -> Optional[Edition]:
        """
        Récupère une édition par son ISBN

        Args:
            isbn: L'ISBN de l'édition

        Returns:
            L'édition trouvée ou None
        """
        return self._editions.get(isbn)

    def get_all(self) -> List[Edition]:
        """
        Récupère toutes les éditions

        Returns:
            Liste de toutes les éditions
        """
        return list(self._editions.values())

    def add(self, edition: Edition) -> bool:
        """
        Ajoute une nouvelle édition

        Args:
            edition: L'édition à ajouter

        Returns:
            True si l'ajout a réussi, False si l'ISBN existe déjà
        """
        if edition.isbn in self._editions:
            return False

        self._editions[edition.isbn] = edition
        return True

    def update(self, edition: Edition) -> bool:
        """
        Met à jour une édition existante

        Args:
            edition: L'édition avec les nouvelles données

        Returns:
            True si la mise à jour a réussi, False si l'édition n'existe pas
        """
        if edition.isbn not in self._editions:
            return False

        self._editions[edition.isbn] = edition
        return True

    def delete(self, isbn: str) -> bool:
        """
        Supprime une édition

        Args:
            isbn: L'ISBN de l'édition à supprimer

        Returns:
            True si la suppression a réussi, False si l'édition n'existe pas
        """
        if isbn not in self._editions:
            return False

        del self._editions[isbn]
        return True

    def search(self, query: str) -> List[Edition]:
        """
        Recherche des éditions par ISBN ou éditeur

        Args:
            query: La requête de recherche

        Returns:
            Liste des éditions correspondantes
        """
        if not query.strip():
            return []

        query_normalized = U_String(query).remove_diacritics().lower()

        results = []
        for edition in self._editions.values():
            # Recherche par ISBN (partiel)
            if query_normalized in edition.isbn.lower():
                results.append(edition)
                continue

            # Recherche par éditeur
            if edition.publisher and query_normalized in U_String(edition.publisher).remove_diacritics().lower():
                results.append(edition)
                continue

        return results

    def get_by_work_id(self, work_id: str) -> List[Edition]:
        """
        Récupère toutes les éditions d'une œuvre

        Args:
            work_id: L'identifiant de l'œuvre

        Returns:
            Liste des éditions de cette œuvre
        """
        return [
            edition for edition in self._editions.values()
            if edition.work_id == work_id
        ]

    def get_by_publisher(self, publisher: str) -> List[Edition]:
        """
        Récupère toutes les éditions d'un éditeur

        Args:
            publisher: Le nom de l'éditeur

        Returns:
            Liste des éditions de cet éditeur
        """
        publisher_normalized = U_String(publisher).remove_diacritics().lower()
        return [
            edition for edition in self._editions.values()
            if edition.publisher and U_String(edition.publisher).remove_diacritics().lower() == publisher_normalized
        ]

    def get_by_year(self, year: int) -> List[Edition]:
        """
        Récupère toutes les éditions publiées une année donnée

        Args:
            year: L'année de publication

        Returns:
            Liste des éditions publiées cette année
        """
        return [
            edition for edition in self._editions.values()
            if edition.publication_year == year
        ]

    def get_digital_editions(self) -> List[Edition]:
        """
        Récupère toutes les éditions numériques

        Returns:
            Liste des éditions numériques
        """
        return [edition for edition in self._editions.values() if edition.is_digital]

    def get_physical_editions(self) -> List[Edition]:
        """
        Récupère toutes les éditions physiques

        Returns:
            Liste des éditions physiques
        """
        return [edition for edition in self._editions.values() if edition.is_physical]
