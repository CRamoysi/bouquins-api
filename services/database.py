"""
Repository SQLite pour Oeuvres et Editions
Architecture à 2 tables avec relation 1:N
"""

import sqlite3
from typing import List, Optional
from contextlib import contextmanager

from models.oeuvre import Oeuvre
from models.edition import Edition
from const.book_format import BookFormat
from const.genre import Genre
from services.repository import IRepository


class OeuvreSQLiteRepository(IRepository[Oeuvre]):
    """Repository SQLite pour les Oeuvres"""

    def __init__(self, db_path: str = "catalogue.db") -> None:
        """
        Initialise le repository avec la base de données SQLite

        Args:
            db_path: Chemin vers le fichier de base de données
        """
        self.db_path = db_path
        self._create_table()

    @contextmanager
    def _get_connection(self):
        """Context manager pour gérer les connexions SQLite"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _create_table(self) -> None:
        """Crée la table oeuvres si elle n'existe pas"""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS oeuvres (
                    work_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    co_authors TEXT,
                    original_language TEXT,
                    original_publication_year INTEGER,
                    summary TEXT,
                    genres TEXT,
                    themes TEXT,
                    awards TEXT,
                    series TEXT,
                    series_number INTEGER
                )
            """)

    def get_by_id(self, work_id: str) -> Optional[Oeuvre]:
        """Récupère une œuvre par son work_id"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM oeuvres WHERE work_id = ?",
                (work_id,)
            )
            row = cursor.fetchone()
            return self._row_to_oeuvre(row) if row else None

    def get_all(self) -> List[Oeuvre]:
        """Récupère toutes les œuvres"""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM oeuvres ORDER BY title")
            return [self._row_to_oeuvre(row) for row in cursor.fetchall()]

    def add(self, oeuvre: Oeuvre) -> bool:
        """Ajoute une nouvelle œuvre"""
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT INTO oeuvres (
                        work_id, title, author, co_authors, original_language,
                        original_publication_year, summary, genres, themes,
                        awards, series, series_number
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    oeuvre.work_id,
                    oeuvre.title,
                    oeuvre.author,
                    ",".join(oeuvre.co_authors) if oeuvre.co_authors else None,
                    oeuvre.original_language,
                    oeuvre.original_publication_year,
                    oeuvre.summary,
                    ",".join([g.value for g in oeuvre.genres]) if oeuvre.genres else None,
                    ",".join(oeuvre.themes) if oeuvre.themes else None,
                    ",".join(oeuvre.awards) if oeuvre.awards else None,
                    oeuvre.series,
                    oeuvre.series_number
                ))
                return True
        except sqlite3.IntegrityError:
            return False

    def update(self, oeuvre: Oeuvre) -> bool:
        """Met à jour une œuvre existante"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                UPDATE oeuvres SET
                    title = ?, author = ?, co_authors = ?, original_language = ?,
                    original_publication_year = ?, summary = ?, genres = ?,
                    themes = ?, awards = ?, series = ?, series_number = ?
                WHERE work_id = ?
            """, (
                oeuvre.title,
                oeuvre.author,
                ",".join(oeuvre.co_authors) if oeuvre.co_authors else None,
                oeuvre.original_language,
                oeuvre.original_publication_year,
                oeuvre.summary,
                ",".join([g.value for g in oeuvre.genres]) if oeuvre.genres else None,
                ",".join(oeuvre.themes) if oeuvre.themes else None,
                ",".join(oeuvre.awards) if oeuvre.awards else None,
                oeuvre.series,
                oeuvre.series_number,
                oeuvre.work_id
            ))
            return cursor.rowcount > 0

    def delete(self, work_id: str) -> bool:
        """Supprime une œuvre"""
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM oeuvres WHERE work_id = ?", (work_id,))
            return cursor.rowcount > 0

    def search(self, query: str) -> List[Oeuvre]:
        """Recherche des œuvres par titre ou auteur"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM oeuvres
                WHERE title LIKE ? OR author LIKE ?
                ORDER BY title
            """, (f"%{query}%", f"%{query}%"))
            return [self._row_to_oeuvre(row) for row in cursor.fetchall()]

    def _row_to_oeuvre(self, row: sqlite3.Row) -> Oeuvre:
        """Convertit une ligne SQL en objet Oeuvre"""
        oeuvre = Oeuvre(row['work_id'])
        oeuvre.title = row['title']
        oeuvre.author = row['author']
        oeuvre.co_authors = row['co_authors'].split(',') if row['co_authors'] else []
        oeuvre.original_language = row['original_language'] or 'fr'
        oeuvre.original_publication_year = row['original_publication_year']
        oeuvre.summary = row['summary']

        # Convertir les genres stockés en texte vers des enums
        if row['genres']:
            oeuvre.genres = [Genre(g) for g in row['genres'].split(',')]

        oeuvre.themes = row['themes'].split(',') if row['themes'] else []
        oeuvre.awards = row['awards'].split(',') if row['awards'] else []
        oeuvre.series = row['series']
        oeuvre.series_number = row['series_number']

        return oeuvre


class EditionSQLiteRepository(IRepository[Edition]):
    """Repository SQLite pour les Editions"""

    def __init__(self, db_path: str = "catalogue.db") -> None:
        """
        Initialise le repository avec la base de données SQLite

        Args:
            db_path: Chemin vers le fichier de base de données
        """
        self.db_path = db_path
        self._create_table()

    @contextmanager
    def _get_connection(self):
        """Context manager pour gérer les connexions SQLite"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")  # Activer les clés étrangères
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _create_table(self) -> None:
        """Crée la table editions si elle n'existe pas"""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS editions (
                    isbn TEXT PRIMARY KEY,
                    work_id TEXT,
                    publisher TEXT,
                    publication_year INTEGER,
                    language TEXT,
                    format TEXT,
                    pages INTEGER,
                    dimensions_height REAL,
                    dimensions_width REAL,
                    dimensions_thickness REAL,
                    weight INTEGER,
                    cover_front_url TEXT,
                    cover_back_url TEXT,
                    cover_spine_url TEXT,
                    cover_color TEXT,
                    price REAL,
                    currency TEXT,
                    ean TEXT,
                    edition_number INTEGER,
                    collection TEXT,
                    translator TEXT,
                    illustrator TEXT,
                    preface_by TEXT,
                    FOREIGN KEY (work_id) REFERENCES oeuvres(work_id) ON DELETE CASCADE
                )
            """)

            # Créer un index sur work_id pour accélérer les recherches
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_editions_work_id
                ON editions(work_id)
            """)

    def get_by_id(self, isbn: str) -> Optional[Edition]:
        """Récupère une édition par son ISBN"""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM editions WHERE isbn = ?", (isbn,))
            row = cursor.fetchone()
            return self._row_to_edition(row) if row else None

    def get_all(self) -> List[Edition]:
        """Récupère toutes les éditions"""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM editions ORDER BY isbn")
            return [self._row_to_edition(row) for row in cursor.fetchall()]

    def add(self, edition: Edition) -> bool:
        """Ajoute une nouvelle édition"""
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT INTO editions (
                        isbn, work_id, publisher, publication_year, language,
                        format, pages, dimensions_height, dimensions_width,
                        dimensions_thickness, weight, cover_front_url,
                        cover_back_url, cover_spine_url, cover_color,
                        price, currency, ean, edition_number, collection,
                        translator, illustrator, preface_by
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    edition.isbn,
                    edition.work_id,
                    edition.publisher,
                    edition.publication_year,
                    edition.language,
                    edition.format.value if edition.format else None,
                    edition.pages,
                    edition.dimensions_height,
                    edition.dimensions_width,
                    edition.dimensions_thickness,
                    edition.weight,
                    edition.cover_front_url,
                    edition.cover_back_url,
                    edition.cover_spine_url,
                    edition.cover_color,
                    edition.price,
                    edition.currency,
                    edition.ean,
                    edition.edition_number,
                    edition.collection,
                    edition.translator,
                    edition.illustrator,
                    edition.preface_by
                ))
                return True
        except sqlite3.IntegrityError:
            return False

    def update(self, edition: Edition) -> bool:
        """Met à jour une édition existante"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                UPDATE editions SET
                    work_id = ?, publisher = ?, publication_year = ?, language = ?,
                    format = ?, pages = ?, dimensions_height = ?, dimensions_width = ?,
                    dimensions_thickness = ?, weight = ?, cover_front_url = ?,
                    cover_back_url = ?, cover_spine_url = ?, cover_color = ?,
                    price = ?, currency = ?, ean = ?, edition_number = ?,
                    collection = ?, translator = ?, illustrator = ?, preface_by = ?
                WHERE isbn = ?
            """, (
                edition.work_id,
                edition.publisher,
                edition.publication_year,
                edition.language,
                edition.format.value if edition.format else None,
                edition.pages,
                edition.dimensions_height,
                edition.dimensions_width,
                edition.dimensions_thickness,
                edition.weight,
                edition.cover_front_url,
                edition.cover_back_url,
                edition.cover_spine_url,
                edition.cover_color,
                edition.price,
                edition.currency,
                edition.ean,
                edition.edition_number,
                edition.collection,
                edition.translator,
                edition.illustrator,
                edition.preface_by,
                edition.isbn
            ))
            return cursor.rowcount > 0

    def delete(self, isbn: str) -> bool:
        """Supprime une édition"""
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM editions WHERE isbn = ?", (isbn,))
            return cursor.rowcount > 0

    def search(self, query: str) -> List[Edition]:
        """Recherche des éditions par ISBN ou éditeur"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM editions
                WHERE isbn LIKE ? OR publisher LIKE ?
                ORDER BY isbn
            """, (f"%{query}%", f"%{query}%"))
            return [self._row_to_edition(row) for row in cursor.fetchall()]

    def get_by_work_id(self, work_id: str) -> List[Edition]:
        """Récupère toutes les éditions d'une œuvre"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM editions WHERE work_id = ? ORDER BY publication_year DESC",
                (work_id,)
            )
            return [self._row_to_edition(row) for row in cursor.fetchall()]

    def _row_to_edition(self, row: sqlite3.Row) -> Edition:
        """Convertit une ligne SQL en objet Edition"""
        edition = Edition(row['isbn'], row['work_id'])
        edition.publisher = row['publisher'] or ''
        edition.publication_year = row['publication_year']
        edition.language = row['language'] or 'fr'

        # Convertir le format texte vers enum
        if row['format']:
            edition.format = BookFormat(row['format'])

        edition.pages = row['pages']
        edition.dimensions_height = row['dimensions_height']
        edition.dimensions_width = row['dimensions_width']
        edition.dimensions_thickness = row['dimensions_thickness']
        edition.weight = row['weight']
        edition.cover_front_url = row['cover_front_url']
        edition.cover_back_url = row['cover_back_url']
        edition.cover_spine_url = row['cover_spine_url']
        edition.cover_color = row['cover_color']
        edition.price = row['price']
        edition.currency = row['currency']
        edition.ean = row['ean']
        edition.edition_number = row['edition_number']
        edition.collection = row['collection']
        edition.translator = row['translator']
        edition.illustrator = row['illustrator']
        edition.preface_by = row['preface_by']

        return edition
