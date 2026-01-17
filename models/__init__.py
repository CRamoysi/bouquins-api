"""
Modèles de domaine pour le catalogue de livres
Architecture à deux niveaux : Oeuvre (œuvre littéraire) et Edition (édition spécifique)
"""

from models.oeuvre import Oeuvre
from models.edition import Edition

__all__ = ['Oeuvre', 'Edition']
