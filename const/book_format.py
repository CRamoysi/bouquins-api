"""
Énumération des formats de livres
"""
from enum import Enum


class BookFormat(Enum):
    """Formats possibles pour une édition de livre"""
    POCHE = "Poche"
    BROCHE = "Broché"
    RELIE = "Relié"
    GRAND_FORMAT = "Grand format"
    EBOOK = "eBook"
    EPUB = "EPUB"
    PDF = "PDF"
    AUDIO = "Livre audio"
    KINDLE = "Kindle"
    LUXE = "Édition de luxe"
    COLLECTOR = "Édition collector"

    @classmethod
    def all_formats(cls):
        """Retourne tous les formats disponibles"""
        return list(cls)

    @classmethod
    def is_digital(cls, format_type) -> bool:
        """Vérifie si un format est numérique"""
        return format_type in [cls.EBOOK, cls.EPUB, cls.PDF, cls.KINDLE]

    @classmethod
    def is_physical(cls, format_type) -> bool:
        """Vérifie si un format est physique"""
        return not cls.is_digital(format_type) and format_type != cls.AUDIO
