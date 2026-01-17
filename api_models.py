"""
Modèles Pydantic pour l'API REST
Ces modèles servent à la validation des données et à la documentation automatique de l'API
"""
from pydantic import BaseModel, Field
from typing import Optional


class LivreCreate(BaseModel):
    """Modèle pour créer un nouveau livre"""
    isbn: str = Field(..., description="ISBN unique du livre", example="978-2-07-036222-6")
    title: str = Field(..., description="Titre du livre", example="Les Misérables")
    author: str = Field(..., description="Auteur du livre", example="Victor Hugo")
    publisher: str = Field(default="", description="Éditeur du livre", example="Gallimard")
    publication_year: Optional[int] = Field(None, ge=-1000, le=3000, description="Année de publication", example=1862)
    summary: Optional[str] = Field(None, description="Résumé du livre")

    class Config:
        json_schema_extra = {
            "example": {
                "isbn": "978-2-07-036222-6",
                "title": "Les Misérables",
                "author": "Victor Hugo",
                "publisher": "Gallimard",
                "publication_year": 1862,
                "summary": "Un roman historique et social qui suit le destin de Jean Valjean..."
            }
        }


class LivreResponse(BaseModel):
    """Modèle pour la réponse avec un livre"""
    isbn: str
    title: str
    author: str
    publisher: str
    publication_year: Optional[int]
    summary: Optional[str]
    type: str = "Livre"

    class Config:
        from_attributes = True


class LivreUpdate(BaseModel):
    """Modèle pour mettre à jour un livre (tous les champs optionnels)"""
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    publication_year: Optional[int] = Field(None, ge=-1000, le=3000)
    summary: Optional[str] = None


class ErrorResponse(BaseModel):
    """Modèle pour les réponses d'erreur"""
    detail: str
    error_code: Optional[str] = None


class SuccessResponse(BaseModel):
    """Modèle pour les réponses de succès"""
    message: str
    isbn: Optional[str] = None


class StatsResponse(BaseModel):
    """Modèle pour les statistiques du catalogue"""
    total_livres: int
    total_auteurs: int
    annee_plus_ancienne: Optional[int]
    annee_plus_recente: Optional[int]
