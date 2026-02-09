import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Definir una paleta de colores personalizada inspirada en Spotify  

PALETA_SPOTIFY = [
    "#1DB954",  # Verde principal
    "#212121",  # Negro suave
    "#121212",  # Negro profundo
    "#535353",  # Gris oscuro
    "#B3B3B3"   # Gris claro
]

sns.set_palette(sns.color_palette(PALETA_SPOTIFY))

# Configuración inicial del dashboard

st.set_page_config(page_title="Spotify Dashboard Análisis de datos", layout="wide")

# Cargar el dataset

df = pd.read_csv("18. Spotify 2015-2025.csv")

# Preprocesamiento de datos

df = df.convert_dtypes()
df = df.replace(r'^\s*$', np.nan, regex=True)
df = df.fillna('Unknown')
df = df.head(10000)

# Convertir release_date to datetime
df['release_date'] = pd.to_datetime(df['release_date'])

df_processed = df

# Sidebar para filtrado y búsqueda
with st.sidebar:
    st.header("Filtros de búsqueda")

    cities = df_processed['country'].unique()
    selected_cities = st.multiselect("Selecciona una o más ciudades:", cities, default=["Canada", "Brazil", "Germany"], help="Selecciona uno o más países de la lista para filtrar los datos.", placeholder="Escoge una opción...")

    genres = df_processed['genre'].unique()    
    selected_genres = st.multiselect("Selecciona uno o más géneros:", genres, default=["Pop", "Rock"], help="Selecciona uno o más géneros de la lista para filtrar los datos.", placeholder="Escoge una opción...")

    year_range = st.select_slider("Selecciona un rango de años:", options=sorted(df_processed['release_date'].dt.year.unique()), value=(2015, 2025), help="Selecciona un rango de años para filtrar los datos.")


st.title("Dasboard exploratorio de Spotify Data (2015-2025)")
st.markdown("Análisis exploratorio de datos de Spotify utilizando Streamlit, Pandas, Matplotlib y Seaborn.")

df_filtered = df_processed.copy()

# Filtro por Países
if selected_cities:
    df_filtered = df_filtered[df_filtered['country'].isin(selected_cities)]

# Filtro por Géneros
if selected_genres:
    df_filtered = df_filtered[df_filtered['genre'].isin(selected_genres)]

# Filtro por Años 2015-2025
df_filtered = df_filtered[
    (df_filtered['release_date'].dt.year >= year_range[0]) & 
    (df_filtered['release_date'].dt.year <= year_range[1])
]

st.write(f"Mostrando {len(df_filtered)} resultados:")
st.dataframe(df_filtered)
