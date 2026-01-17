"""
Modèle Edition - Représente une édition spécifique d'une œuvre
Une édition est identifiée par son ISBN unique
"""
from typing import Optional
from datetime import datetime
from const.book_format import BookFormat


class Edition:
    """
    Classe représentant une édition spécifique d'un livre

    Attributs:
        isbn: ISBN unique (identifiant principal)
        work_id: Référence vers l'œuvre parente
        publisher: Éditeur de cette édition
        publication_year: Année de publication de cette édition
        publication_date: Date exacte de publication
        language: Langue de cette édition

        # Format et dimensions
        format: Format du livre (Poche, Broché, etc.)
        pages: Nombre de pages
        dimensions_height: Hauteur en cm
        dimensions_width: Largeur en cm
        dimensions_thickness: Épaisseur en cm
        weight: Poids en grammes

        # Visuels (pour OCR)
        cover_front_url: URL ou chemin vers la photo de couverture
        cover_back_url: URL ou chemin vers la 4ème de couverture
        cover_spine_url: URL ou chemin vers le dos du livre
        cover_color: Couleur dominante de la couverture

        # Informations commerciales
        price: Prix public
        currency: Devise (EUR, USD, etc.)
        ean: Code-barres EAN

        # Métadonnées éditoriales
        edition_number: Numéro d'édition (1ère, 2ème, etc.)
        collection: Nom de la collection éditoriale
        translator: Traducteur (si applicable)
        illustrator: Illustrateur (si applicable)
        preface_by: Auteur de la préface

        # Qualité et état
        condition: État du livre (Neuf, Bon, Acceptable, etc.)
        notes: Notes personnelles
    """

    def __init__(self, isbn: str, work_id: Optional[str] = None) -> None:
        """
        Initialise une nouvelle édition

        Args:
            isbn: ISBN unique de cette édition
            work_id: ID de l'œuvre parente (optionnel si création manuelle)
        """
        # Identifiants
        self.isbn: str = isbn
        self.work_id: Optional[str] = work_id

        # Éditeur et publication
        self.publisher: str = ""
        self._publication_year: Optional[int] = None
        self.publication_date: Optional[datetime] = None
        self.language: str = "fr"

        # Format et caractéristiques physiques
        self.format: Optional[BookFormat] = None
        self.pages: Optional[int] = None
        self.dimensions_height: Optional[float] = None  # en cm
        self.dimensions_width: Optional[float] = None   # en cm
        self.dimensions_thickness: Optional[float] = None  # en cm
        self.weight: Optional[int] = None  # en grammes

        # Images des couvertures (chemins ou URLs)
        self.cover_front_url: Optional[str] = None
        self.cover_back_url: Optional[str] = None
        self.cover_spine_url: Optional[str] = None
        self.cover_color: Optional[str] = None  # Hex color ou nom

        # Informations commerciales
        self.price: Optional[float] = None
        self.currency: str = "EUR"
        self.ean: Optional[str] = None

        # Informations éditoriales
        self.edition_number: Optional[int] = None  # 1, 2, 3...
        self.collection: Optional[str] = None
        self.translator: Optional[str] = None
        self.illustrator: Optional[str] = None
        self.preface_by: Optional[str] = None

        # État et notes
        self.condition: str = "Neuf"
        self.notes: Optional[str] = None

        # Métadonnées de gestion
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = datetime.now()

    @property
    def publication_year(self) -> Optional[int]:
        """Getter pour l'année de publication"""
        return self._publication_year

    @publication_year.setter
    def publication_year(self, year: Optional[int]) -> None:
        """Setter pour l'année de publication avec validation"""
        if year is not None and (year < 1000 or year > 3000):
            raise ValueError("L'année de publication doit être entre 1000 et 3000")
        self._publication_year = year

    @property
    def dimensions_str(self) -> str:
        """Retourne les dimensions formatées"""
        if all([self.dimensions_height, self.dimensions_width, self.dimensions_thickness]):
            return f"{self.dimensions_height}×{self.dimensions_width}×{self.dimensions_thickness} cm"
        elif self.dimensions_height and self.dimensions_width:
            return f"{self.dimensions_height}×{self.dimensions_width} cm"
        return "Dimensions non renseignées"

    @property
    def price_str(self) -> str:
        """Retourne le prix formaté"""
        if self.price:
            return f"{self.price:.2f} {self.currency}"
        return "Prix non renseigné"

    @property
    def has_cover_images(self) -> bool:
        """Vérifie si l'édition a au moins une image de couverture"""
        return bool(self.cover_front_url or self.cover_back_url)

    @property
    def is_digital(self) -> bool:
        """Vérifie si l'édition est numérique"""
        return bool(self.format and BookFormat.is_digital(self.format))

    @property
    def is_physical(self) -> bool:
        """Vérifie si l'édition est physique"""
        return bool(self.format and BookFormat.is_physical(self.format))

    def set_dimensions(self, height: float, width: float, thickness: Optional[float] = None) -> None:
        """
        Définit les dimensions du livre

        Args:
            height: Hauteur en cm
            width: Largeur en cm
            thickness: Épaisseur en cm (optionnel)
        """
        self.dimensions_height = height
        self.dimensions_width = width
        if thickness:
            self.dimensions_thickness = thickness

    def set_cover_images(
        self,
        front: Optional[str] = None,
        back: Optional[str] = None,
        spine: Optional[str] = None
    ) -> None:
        """
        Définit les URLs/chemins des images de couverture

        Args:
            front: Chemin ou URL de la couverture
            back: Chemin ou URL de la 4ème de couverture
            spine: Chemin ou URL du dos
        """
        if front:
            self.cover_front_url = front
        if back:
            self.cover_back_url = back
        if spine:
            self.cover_spine_url = spine

    def update_timestamp(self) -> None:
        """Met à jour le timestamp de dernière modification"""
        self.updated_at = datetime.now()

    def __repr__(self) -> str:
        """Représentation textuelle de l'édition"""
        format_str = self.format.value if self.format else "Format inconnu"
        return f"Edition(ISBN: {self.isbn}, {format_str}, {self.publisher}, {self.publication_year})"

    def __str__(self) -> str:
        """Version lisible de l'édition"""
        parts = [self.publisher]
        if self.publication_year:
            parts.append(str(self.publication_year))
        if self.format:
            parts.append(self.format.value)
        return f"Édition: {', '.join(parts)} (ISBN: {self.isbn})"
