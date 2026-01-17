"""
Interface abstraite pour les repositories (Pattern Repository)
Permet d'abstraire la couche de persistance des données
"""

from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')


class IRepository(ABC, Generic[T]):
    """
    Interface générique pour les repositories
    T représente le type d'entité géré (Oeuvre ou Edition)
    """

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Récupère une entité par son identifiant

        Args:
            entity_id: L'identifiant de l'entité (work_id ou isbn)

        Returns:
            L'entité trouvée ou None
        """
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """
        Récupère toutes les entités

        Returns:
            Liste de toutes les entités
        """
        pass

    @abstractmethod
    def add(self, entity: T) -> bool:
        """
        Ajoute une nouvelle entité

        Args:
            entity: L'entité à ajouter

        Returns:
            True si l'ajout a réussi, False si l'ID existe déjà
        """
        pass

    @abstractmethod
    def update(self, entity: T) -> bool:
        """
        Met à jour une entité existante

        Args:
            entity: L'entité avec les nouvelles données

        Returns:
            True si la mise à jour a réussi, False si l'entité n'existe pas
        """
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """
        Supprime une entité

        Args:
            entity_id: L'identifiant de l'entité à supprimer

        Returns:
            True si la suppression a réussi, False si l'entité n'existe pas
        """
        pass

    @abstractmethod
    def search(self, query: str) -> List[T]:
        """
        Recherche des entités par critères

        Args:
            query: La requête de recherche

        Returns:
            Liste des entités correspondantes
        """
        pass
