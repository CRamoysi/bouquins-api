"""
Application Streamlit pour visualiser le catalogue de livres
Mode lecture seule - L'ajout se fera via OCR de couvertures
"""

import streamlit as st
from services.bibliotheque import Bibliotheque
from services.database import OeuvreSQLiteRepository, EditionSQLiteRepository
from const import BookFormat, Genre


# Configuration de la page
st.set_page_config(
    page_title="Catalogue de Livres",
    page_icon="📚",
    layout="wide"
)

# Initialiser la bibliothèque avec SQLite
@st.cache_resource
def get_bibliotheque():
    """Retourne une instance de Bibliotheque avec repositories SQLite"""
    return Bibliotheque(
        OeuvreSQLiteRepository("catalogue.db"),
        EditionSQLiteRepository("catalogue.db")
    )


biblio = get_bibliotheque()

# Titre principal
st.title("📚 Catalogue de Livres")

# Sidebar pour les statistiques et filtres
with st.sidebar:
    st.header("📊 Statistiques")
    stats = biblio.get_stats()

    st.metric("Œuvres", stats["total_oeuvres"])
    st.metric("Éditions", stats["total_editions"])
    st.metric("Éditions numériques", stats["editions_numeriques"])
    st.metric("Éditions physiques", stats["editions_physiques"])

    st.divider()

    st.header("🔍 Filtres")
    search_query = st.text_input("Rechercher", placeholder="Titre, auteur, ISBN...")

    view_mode = st.radio(
        "Vue",
        ["📖 Par Œuvres", "📚 Par Éditions"],
        index=0
    )

# Zone principale
if view_mode == "📖 Par Œuvres":
    st.header("📖 Liste des Œuvres")

    # Récupérer les œuvres
    if search_query:
        oeuvres = biblio.search_oeuvres(search_query)
        st.caption(f"{len(oeuvres)} résultat(s) pour '{search_query}'")
    else:
        oeuvres = biblio.oeuvres

    if not oeuvres:
        st.info("Aucune œuvre dans le catalogue. Utilisez le scan de couverture pour ajouter des livres.")
    else:
        # Afficher chaque œuvre
        for oeuvre in oeuvres:
            with st.expander(f"📖 {oeuvre.title} — {oeuvre.author}"):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown(f"**Auteur:** {oeuvre.author}")

                    if oeuvre.co_authors:
                        st.markdown(f"**Co-auteurs:** {', '.join(oeuvre.co_authors)}")

                    if oeuvre.original_publication_year:
                        st.markdown(f"**Première publication:** {oeuvre.original_publication_year}")

                    if oeuvre.original_language:
                        st.markdown(f"**Langue originale:** {oeuvre.original_language}")

                    if oeuvre.genres:
                        genres_str = ", ".join([g.value for g in oeuvre.genres])
                        st.markdown(f"**Genres:** {genres_str}")

                    if oeuvre.series:
                        series_info = f"{oeuvre.series}"
                        if oeuvre.series_number:
                            series_info += f" (Tome {oeuvre.series_number})"
                        st.markdown(f"**Série:** {series_info}")

                    if oeuvre.summary:
                        st.markdown("**Résumé:**")
                        st.text_area("", oeuvre.summary, height=100, disabled=True, key=f"summary_{oeuvre.work_id}")

                with col2:
                    st.markdown(f"**ID:** `{oeuvre.work_id}`")

                    if oeuvre.awards:
                        st.markdown("**Prix:**")
                        for award in oeuvre.awards:
                            st.markdown(f"- {award}")

                    if oeuvre.themes:
                        st.markdown("**Thèmes:**")
                        for theme in oeuvre.themes:
                            st.markdown(f"- {theme}")

                # Afficher les éditions de cette œuvre
                editions = biblio.get_editions_of_oeuvre(oeuvre.work_id)
                if editions:
                    st.markdown(f"**📚 {len(editions)} édition(s) disponible(s):**")

                    for edition in editions:
                        format_icon = "💾" if edition.is_digital else "📕"
                        format_text = edition.format.value if edition.format else "Non spécifié"

                        edition_info = f"{format_icon} {edition.isbn} — {edition.publisher}"
                        if edition.publication_year:
                            edition_info += f" ({edition.publication_year})"
                        edition_info += f" — {format_text}"

                        st.markdown(f"- {edition_info}")

else:  # Mode "Par Éditions"
    st.header("📚 Liste des Éditions")

    # Récupérer les éditions
    if search_query:
        editions = biblio.search_editions(search_query)
        st.caption(f"{len(editions)} résultat(s) pour '{search_query}'")
    else:
        editions = biblio.editions

    if not editions:
        st.info("Aucune édition dans le catalogue. Utilisez le scan de couverture pour ajouter des livres.")
    else:
        # Afficher chaque édition
        for edition in editions:
            # Récupérer l'œuvre associée
            oeuvre = biblio.get_oeuvre_of_edition(edition.isbn)
            oeuvre_title = oeuvre.title if oeuvre else "Œuvre inconnue"
            oeuvre_author = oeuvre.author if oeuvre else ""

            format_icon = "💾" if edition.is_digital else "📕"
            title = f"{format_icon} {oeuvre_title} — {edition.isbn}"

            with st.expander(title):
                col1, col2, col3 = st.columns([2, 2, 1])

                with col1:
                    st.markdown("### Informations de l'œuvre")
                    if oeuvre:
                        st.markdown(f"**Titre:** {oeuvre.title}")
                        st.markdown(f"**Auteur:** {oeuvre.author}")
                        if oeuvre.original_publication_year:
                            st.markdown(f"**Publication originale:** {oeuvre.original_publication_year}")
                    else:
                        st.warning("Œuvre non liée")

                with col2:
                    st.markdown("### Informations de l'édition")
                    st.markdown(f"**ISBN:** {edition.isbn}")
                    st.markdown(f"**Éditeur:** {edition.publisher}")

                    if edition.publication_year:
                        st.markdown(f"**Année:** {edition.publication_year}")

                    if edition.format:
                        st.markdown(f"**Format:** {edition.format.value}")

                    if edition.language:
                        st.markdown(f"**Langue:** {edition.language}")

                    if edition.pages:
                        st.markdown(f"**Pages:** {edition.pages}")

                    if edition.collection:
                        st.markdown(f"**Collection:** {edition.collection}")

                with col3:
                    st.markdown("### Détails")

                    if edition.translator:
                        st.markdown(f"**Traducteur:** {edition.translator}")

                    if edition.illustrator:
                        st.markdown(f"**Illustrateur:** {edition.illustrator}")

                    if edition.price:
                        currency = edition.currency or "EUR"
                        st.markdown(f"**Prix:** {edition.price} {currency}")

                # Dimensions et caractéristiques physiques
                if edition.dimensions_height or edition.weight:
                    st.markdown("### Caractéristiques physiques")
                    dim_col1, dim_col2 = st.columns(2)

                    with dim_col1:
                        if edition.dimensions_height:
                            dims = f"{edition.dimensions_height}"
                            if edition.dimensions_width:
                                dims += f" × {edition.dimensions_width}"
                            if edition.dimensions_thickness:
                                dims += f" × {edition.dimensions_thickness}"
                            st.markdown(f"**Dimensions (H×L×E):** {dims} cm")

                    with dim_col2:
                        if edition.weight:
                            st.markdown(f"**Poids:** {edition.weight} g")

                # Images de couverture
                if edition.has_cover_images:
                    st.markdown("### 📷 Couvertures")
                    img_cols = st.columns(3)

                    if edition.cover_front_url:
                        with img_cols[0]:
                            st.markdown("**Couverture avant**")
                            st.image(edition.cover_front_url, use_container_width=True)

                    if edition.cover_back_url:
                        with img_cols[1]:
                            st.markdown("**4ème de couverture**")
                            st.image(edition.cover_back_url, use_container_width=True)

                    if edition.cover_spine_url:
                        with img_cols[2]:
                            st.markdown("**Dos**")
                            st.image(edition.cover_spine_url, use_container_width=True)

# Footer
st.divider()
st.caption("💡 Utilisez le scan OCR de couvertures pour ajouter de nouveaux livres au catalogue.")
