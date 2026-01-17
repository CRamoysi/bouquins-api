# 🎨 GUIDE STREAMLIT - Exemples pour l'interface

## 📚 Documentation officielle
https://docs.streamlit.io/

---

## 🎯 Concepts de base

### 1. Structure d'une app Streamlit

```python
import streamlit as st

# Configuration (toujours en premier)
st.set_page_config(
    page_title="Mon App",
    page_icon="📚",
    layout="wide"  # ou "centered"
)

# Titre principal
st.title("📚 Ma Bibliothèque")

# Texte
st.write("Bienvenue dans votre bibliothèque !")
st.markdown("**Texte en gras** et _italique_")

# Séparateur
st.markdown("---")
```

---

## 📊 Composants essentiels

### Textes et titres
```python
st.title("Titre principal")
st.header("En-tête")
st.subheader("Sous-titre")
st.text("Texte simple")
st.markdown("**Markdown** avec *style*")
st.caption("Légende en petit")
```

### Messages
```python
st.success("✅ Opération réussie !")
st.error("❌ Erreur détectée")
st.warning("⚠️ Attention")
st.info("ℹ️ Information")
```

### Métriques
```python
st.metric(label="Total livres", value=42)
st.metric(label="Lus", value=30, delta=5)  # delta = variation

# Colonnes pour plusieurs métriques
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total", 100)
with col2:
    st.metric("Lus", 75)
with col3:
    st.metric("% Lus", "75%")
```

---

## 📝 Formulaires et inputs

### Champs de saisie
```python
# Texte simple
nom = st.text_input("Nom du livre", placeholder="Entrez le titre...")

# Zone de texte multilignes
description = st.text_area("Description", height=100)

# Nombre
annee = st.number_input("Année", min_value=1900, max_value=2026, value=2024, step=1)
prix = st.number_input("Prix", min_value=0.0, value=19.99, step=0.50)

# Date
from datetime import date
date_achat = st.date_input("Date d'achat", value=date.today())
```

### Sélections
```python
# Menu déroulant
format_livre = st.selectbox("Format", ["PDF", "EPUB", "MOBI"])

# Boutons radio
type_livre = st.radio("Type", ["eBook", "Papier", "Magazine"], horizontal=True)

# Case à cocher
est_lu = st.checkbox("Marquer comme lu")

# Slider
note = st.slider("Note", min_value=0, max_value=5, value=3, step=1)
```

### Boutons
```python
# Bouton simple
if st.button("Ajouter"):
    st.write("Livre ajouté !")

# Bouton primaire (bleu)
if st.button("Valider", type="primary"):
    st.success("Validé !")

# Bouton avec clé unique (important dans les boucles)
if st.button("Supprimer", key="btn_del_1"):
    st.write("Supprimé")
```

---

## 📐 Mise en page

### Colonnes
```python
col1, col2 = st.columns(2)  # 2 colonnes égales
col1, col2, col3 = st.columns([2, 1, 1])  # Proportions personnalisées

with col1:
    st.write("Colonne 1")
    
with col2:
    st.write("Colonne 2")
```

### Onglets
```python
tab1, tab2, tab3 = st.tabs(["➕ Ajouter", "📖 Liste", "🔍 Rechercher"])

with tab1:
    st.write("Contenu onglet 1")

with tab2:
    st.write("Contenu onglet 2")
```

### Expander (accordéon)
```python
with st.expander("Voir les détails"):
    st.write("Contenu caché par défaut")
    st.write("Cliquer pour voir")
```

### Sidebar (barre latérale)
```python
with st.sidebar:
    st.header("Menu")
    st.write("Options...")
    
# Ou directement
st.sidebar.metric("Total", 42)
```

### Conteneurs
```python
# Conteneur vide (pour mettre à jour dynamiquement)
placeholder = st.empty()
placeholder.write("Texte initial")
# Plus tard...
placeholder.write("Texte mis à jour")

# Container
with st.container():
    st.write("Groupe d'éléments")
    st.button("Bouton dans container")
```

---

## 💾 État de session (st.session_state)

**Indispensable** pour conserver des données entre les interactions !

```python
# Initialiser (une seule fois)
if 'compteur' not in st.session_state:
    st.session_state.compteur = 0

# Lire
st.write(f"Compteur: {st.session_state.compteur}")

# Modifier
if st.button("Incrémenter"):
    st.session_state.compteur += 1
    st.rerun()  # Rafraîchir la page

# Objets complexes
if 'livres' not in st.session_state:
    st.session_state.livres = []

st.session_state.livres.append(nouveau_livre)
```

---

## 📊 Visualisations

### Tableaux
```python
import pandas as pd

# DataFrame Pandas
df = pd.DataFrame({
    'Titre': ['Livre 1', 'Livre 2'],
    'Auteur': ['Auteur A', 'Auteur B'],
    'Note': [5, 4]
})

st.dataframe(df)  # Tableau interactif
st.table(df)      # Tableau statique
```

### Graphiques simples
```python
# Graphique en barres
data = {'eBooks': 45, 'Papier': 30, 'Magazines': 15}
st.bar_chart(data)

# Graphique linéaire
import pandas as pd
df = pd.DataFrame({
    'Année': [2020, 2021, 2022, 2023],
    'Livres lus': [12, 18, 25, 30]
})
st.line_chart(df.set_index('Année'))
```

### Graphiques avancés (Plotly)
```python
import plotly.express as px

fig = px.pie(
    values=[45, 30, 15],
    names=['eBooks', 'Papier', 'Magazines'],
    title="Répartition par type"
)
st.plotly_chart(fig)
```

---

## 🔄 Rechargement et performance

### Rerun (rafraîchir)
```python
if st.button("Rafraîchir"):
    st.rerun()  # Recharge toute la page
```

### Cache (optimisation)
```python
@st.cache_data  # Pour les données (DataFrames, listes...)
def charger_donnees():
    # Fonction coûteuse
    return donnees

@st.cache_resource  # Pour les ressources (connexions DB, modèles ML...)
def get_connexion():
    return connexion
```

---

## 🎨 Exemple complet : Formulaire d'ajout

```python
import streamlit as st

st.header("Ajouter un livre")

# Formulaire
with st.form("form_ajout"):
    col1, col2 = st.columns(2)
    
    with col1:
        titre = st.text_input("Titre *")
        auteur = st.text_input("Auteur *")
    
    with col2:
        annee = st.number_input("Année", 1900, 2026, 2024)
        note = st.slider("Note", 0, 5, 3)
    
    # Bouton submit (dans le form)
    submitted = st.form_submit_button("Ajouter", type="primary")
    
    if submitted:
        if titre and auteur:
            st.success(f"✅ {titre} ajouté !")
        else:
            st.error("❌ Titre et auteur obligatoires")
```

---

## 🎯 Exemple : Liste avec boutons

```python
livres = ["Livre 1", "Livre 2", "Livre 3"]

for i, livre in enumerate(livres):
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.write(f"📖 {livre}")
    
    with col2:
        # Clé unique importante !
        if st.button("🗑️", key=f"del_{i}"):
            livres.pop(i)
            st.rerun()
```

---

## 🚀 Lancer l'app

```bash
# Terminal
streamlit run app.py

# Ouvre automatiquement http://localhost:8501
```

---

## 💡 Astuces

1. **Clés uniques** : Toujours utiliser `key=` différent pour chaque bouton dans une boucle
2. **st.rerun()** : Rafraîchit la page après modification de session_state
3. **Colonnes** : Utiliser pour alignement horizontal
4. **Expander** : Pour cacher du contenu et gagner de l'espace
5. **Form** : Groupe les inputs, valide en une fois (évite les recharges multiples)

---

## 📖 Pour aller plus loin

- Upload de fichiers : `st.file_uploader()`
- Téléchargement : `st.download_button()`
- Images : `st.image()`
- Audio/Vidéo : `st.audio()`, `st.video()`
- Barre de progression : `st.progress()`
- Spinner : `st.spinner("Chargement...")`
