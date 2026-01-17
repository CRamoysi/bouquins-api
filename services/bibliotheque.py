"""
Service Bibliothèque gérant les Oeuvres et Editions
Architecture à 2 niveaux avec pattern Repository
"""

from typing import List, Optional

from models.oeuvre import Oeuvre
from models.edition import Edition
from services.repository import IRepository
from services.oeuvre_repository import OeuvreMemoryRepository
from services.edition_repository import EditionMemoryRepository


class Bibliotheque:
    """
    Service principal gérant le catalogue de livres
    Coordonne les repositories Oeuvre et Edition
    """

    def __init__(
        self,
        oeuvre_repository: Optional[IRepository[Oeuvre]] = None,
        edition_repository: Optional[IRepository[Edition]] = None
    ) -> None:
        """
        Initialise la bibliothèque avec des repositories

        Args:
            oeuvre_repository: Repository pour les œuvres (en mémoire par défaut)
            edition_repository: Repository pour les éditions (en mémoire par défaut)
        """
        self._oeuvre_repo = oeuvre_repository if oeuvre_repository else OeuvreMemoryRepository()
        self._edition_repo = edition_repository if edition_repository else EditionMemoryRepository()

    ####################################################
    # Propriétés
    ####################################################

    @property
    def oeuvres(self) -> List[Oeuvre]:
        """Retourne la liste de toutes les œuvres"""
        return self._oeuvre_repo.get_all()

    @property
    def editions(self) -> List[Edition]:
        """Retourne la liste de toutes les éditions"""
        return self._edition_repo.get_all()

    ####################################################
    # CRUD Oeuvres
    ####################################################

    def add_oeuvre(self, oeuvre: Oeuvre) -> None:
        """
        Ajoute une œuvre à la bibliothèque

        Args:
            oeuvre: L'œuvre à ajouter

        Raises:
            TypeError: Si l'objet n'est pas une Oeuvre
            ValueError: Si le work_id existe déjà
        """
        if not isinstance(oeuvre, Oeuvre):
            raise TypeError("Seuls les objets de type Oeuvre peuvent être ajoutés")

        if not self._oeuvre_repo.add(oeuvre):
            raise ValueError(f"Une œuvre avec le work_id {oeuvre.work_id} existe déjà")

    def get_oeuvre(self, work_id: str) -> Optional[Oeuvre]:
        """
        Récupère une œuvre par son identifiant

        Args:
            work_id: L'identifiant de l'œuvre

        Returns:
            L'œuvre trouvée ou None
        """
        return self._oeuvre_repo.get_by_id(work_id)

    def update_oeuvre(self, oeuvre: Oeuvre) -> None:
        """
        Met à jour une œuvre existante

        Args:
            oeuvre: L'œuvre avec les nouvelles données

        Raises:
            ValueError: Si l'œuvre n'existe pas
        """
        if not self._oeuvre_repo.update(oeuvre):
            raise ValueError(f"Aucune œuvre avec le work_id {oeuvre.work_id}")

    def remove_oeuvre(self, work_id: str) -> None:
        """
        Retire une œuvre de la bibliothèque

        Args:
            work_id: L'identifiant de l'œuvre à supprimer

        Raises:
            ValueError: Si l'œuvre n'existe pas

        Note:
            Supprime aussi toutes les éditions associées
        """
        if not self._oeuvre_repo.delete(work_id):
            raise ValueError(f"Aucune œuvre avec le work_id {work_id}")

        # Supprimer toutes les éditions de cette œuvre
        editions = self._edition_repo.get_all()
        for edition in editions:
            if edition.work_id == work_id:
                self._edition_repo.delete(edition.isbn)

    def search_oeuvres(self, query: str) -> List[Oeuvre]:
        """
        Recherche des œuvres par titre ou auteur

        Args:
            query: La requête de recherche

        Returns:
            Liste des œuvres correspondantes
        """
        return self._oeuvre_repo.search(query)

    ####################################################
    # CRUD Editions
    ####################################################

    def add_edition(self, edition: Edition) -> None:
        """
        Ajoute une édition à la bibliothèque

        Args:
            edition: L'édition à ajouter

        Raises:
            TypeError: Si l'objet n'est pas une Edition
            ValueError: Si l'ISBN existe déjà ou si le work_id n'existe pas
        """
        if not isinstance(edition, Edition):
            raise TypeError("Seuls les objets de type Edition peuvent être ajoutés")

        # Vérifier que l'œuvre existe
        if edition.work_id and not self._oeuvre_repo.get_by_id(edition.work_id):
            raise ValueError(f"Aucune œuvre avec le work_id {edition.work_id}")

        if not self._edition_repo.add(edition):
            raise ValueError(f"Une édition avec l'ISBN {edition.isbn} existe déjà")

    def get_edition(self, isbn: str) -> Optional[Edition]:
        """
        Récupère une édition par son ISBN

        Args:
            isbn: L'ISBN de l'édition

        Returns:
            L'édition trouvée ou None
        """
        return self._edition_repo.get_by_id(isbn)

    def update_edition(self, edition: Edition) -> None:
        """
        Met à jour une édition existante

        Args:
            edition: L'édition avec les nouvelles données

        Raises:
            ValueError: Si l'édition n'existe pas
        """
        if not self._edition_repo.update(edition):
            raise ValueError(f"Aucune édition avec l'ISBN {edition.isbn}")

    def remove_edition(self, isbn: str) -> None:
        """
        Retire une édition de la bibliothèque

        Args:
            isbn: L'ISBN de l'édition à supprimer

        Raises:
            ValueError: Si l'édition n'existe pas
        """
        if not self._edition_repo.delete(isbn):
            raise ValueError(f"Aucune édition avec l'ISBN {isbn}")

    def search_editions(self, query: str) -> List[Edition]:
        """
        Recherche des éditions par ISBN ou éditeur

        Args:
            query: La requête de recherche

        Returns:
            Liste des éditions correspondantes
        """
        return self._edition_repo.search(query)

    ####################################################
    # Relations Oeuvre ↔ Editions
    ####################################################

    def get_editions_of_oeuvre(self, work_id: str) -> List[Edition]:
        """
        Récupère toutes les éditions d'une œuvre

        Args:
            work_id: L'identifiant de l'œuvre

        Returns:
            Liste des éditions de cette œuvre
        """
        editions = self._edition_repo.get_all()
        return [e for e in editions if e.work_id == work_id]

    def get_oeuvre_of_edition(self, isbn: str) -> Optional[Oeuvre]:
        """
        Récupère l'œuvre d'une édition

        Args:
            isbn: L'ISBN de l'édition

        Returns:
            L'œuvre correspondante ou None
        """
        edition = self._edition_repo.get_by_id(isbn)
        if not edition or not edition.work_id:
            return None

        return self._oeuvre_repo.get_by_id(edition.work_id)

    ####################################################
    # Statistiques
    ####################################################

    def get_stats(self) -> dict:
        """
        Récupère les statistiques de la bibliothèque

        Returns:
            Dictionnaire avec les statistiques
        """
        oeuvres = self._oeuvre_repo.get_all()
        editions = self._edition_repo.get_all()

        # Compter les éditions numériques et physiques
        digital_count = sum(1 for e in editions if e.is_digital)
        physical_count = sum(1 for e in editions if e.is_physical)

        # Compter les œuvres avec/sans éditions
        oeuvres_with_editions = set(e.work_id for e in editions if e.work_id)
        oeuvres_without_editions = len([o for o in oeuvres if o.work_id not in oeuvres_with_editions])

        return {
            "total_oeuvres": len(oeuvres),
            "total_editions": len(editions),
            "editions_numeriques": digital_count,
            "editions_physiques": physical_count,
            "oeuvres_avec_editions": len(oeuvres_with_editions),
            "oeuvres_sans_editions": oeuvres_without_editions,
        }
