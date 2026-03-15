import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import base64
from streamlit_echarts import st_echarts


# Definir una paleta de colores personalizada inspirada en Spotify  

PALETA_SPOTIFY = [
    "#1DB954",  # Verde principal
    "#212121",  # Negro suave
    "#121212",  # Negro profundo
    "#535353",  # Gris oscuro
    "#B3B3B3"   # Gris claro
]

# Configuración inicial del dashboard

sns.set_palette(sns.color_palette(PALETA_SPOTIFY))
st.set_page_config(page_title="Spotify Dashboard Análisis de datos", layout="wide")

# Función para cargar el dataset
@st.cache_data
def cargar_csv(path: str) -> pd.DataFrame:
    """Carga un archivo CSV desde una ruta dada."""
    df = pd.read_csv(path)
    return df

def preprocesar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocesa el DataFrame de Spotify."""
    df = df.convert_dtypes()
    df = df.head(15000).copy()
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df["duration_ms"] = df["duration_ms"].div(1000 * 60).round(2)
    df = df.rename(columns={'duration_ms': 'duration_min'})
    df['release_date'] = pd.to_datetime(df['release_date'])
    
    return df

# Función para agregar fondo personalizado al sidebar.
def background_sidebar(image_file: str):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        section[data-testid="stSidebar"] {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-position: center;
        }}
        section[data-testid="stSidebar"] {{
        backdrop-filter: blur(20px);
    }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Carga inicial
df = cargar_csv("18. Spotify 2015-2025.csv")

df_processed = preprocesar_datos(df)

# Sidebar para filtrado y búsqueda
with st.sidebar:
    background_sidebar("imagen/Background 17.png")
    col1, col2, col3 = st.columns([1,1,1])

    with col2:
        st.image("imagen/Spotify_Primary_Logo_RGB_Green.png", width=100)
    st.audio("imagen/Spotify Wrapped 2025 Background Music (High Quality).mp3", start_time=5, autoplay= True, loop= True)
    st.header("Filtros de búsqueda")

    cities = df_processed['country'].unique()
    selected_cities = st.multiselect("Selecciona una o más ciudades:", cities, default=["Canada", "Brazil", "Germany"], help="Selecciona uno o más países de la lista para filtrar los datos.", placeholder="Escoge una opción...")

    year_range = st.select_slider("Selecciona un rango de años:", options=sorted(df_processed['release_date'].dt.year.unique()), value=(2015, 2025), help="Selecciona un rango de años para filtrar los datos.")

st.title("Dasboard exploratorio de Spotify Data (2015-2025)")
st.markdown("Análisis exploratorio de datos de Spotify utilizando Streamlit, Pandas, Matplotlib y Seaborn.")

df_filtered = df_processed.copy()

# Filtro por Países
if selected_cities:
    df_filtered = df_filtered[df_filtered['country'].isin(selected_cities)]

# Filtro por Años 2015-2025
df_filtered = df_filtered[
    (df_filtered['release_date'].dt.year >= year_range[0]) & 
    (df_filtered['release_date'].dt.year <= year_range[1])
]

st.write(f"Mostrando {len(df_filtered)} canciones:")

with st.expander("Ver datos en formato de tablas filtrados:"):
    st.markdown("## Datos en tablas filtrados:")
    st.dataframe(df_filtered)

    st.markdown("### Duración promedio por país y año:")

    duracion_pais_tiempo = df_filtered.groupby([df_filtered['release_date'].dt.year, 'country'])['duration_min'].mean().reset_index()
    duracion_pais_tiempo = duracion_pais_tiempo.rename(columns={
    'release_date': 'año',
    'country': 'país',
    'duration_min': 'duración_promedio'
})
    st.dataframe(duracion_pais_tiempo)

    duracion_media_año = df_filtered.groupby(df_filtered['release_date'].dt.year)['duration_min'].mean().reset_index()
    
    df_filtered['año'] = df_filtered['release_date'].dt.year

    distribucion_años = df_filtered[['año', 'duration_min']].sort_values(by='año').reset_index(drop=True)

    st.markdown("### Duración promedio por año:")
    st.dataframe(distribucion_años)

    columnas_corr = ['duration_min', 'popularity', 'tempo', 'energy', 'stream_count']

    st.markdown("## Matriz de correlación de las variables:")

    corr_matrix = df_filtered[columnas_corr].corr()

    st.dataframe(corr_matrix)

# Gráficos

# Gráfico de Caja distribución de años de lanzamiento y duración de las canciones
fig = px.box(
    distribucion_años, 
    x='año', 
    y='duration_min', 
    title="Gráfico de caja y bigotes según el año de lanzamiento y la duración en minutos", 
    labels={"año": "Año de lanzamiento", 'duration_min': "Duración (minutos)"}, 
    color_discrete_sequence=PALETA_SPOTIFY
)

fig.update_xaxes(type='category')

st.plotly_chart(fig, use_container_width=True)

fig = px.line(
    duracion_pais_tiempo, 
    x='año', 
    y='duración_promedio', 
    color='país', 
    title="Duración promedio por año de lanzamiento según el país.", 
    labels={
        "año": "Año de lanzamiento", 
        'duración_promedio': "Duración promedio (minutos)",
        "país": "País"
    }, 
)

st.plotly_chart(fig, use_container_width=True)

# Gráfico de mapa de calor según las correlaciones entre las variables numéricas    
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, 
            annot=True, 
            cmap='coolwarm', 
            linewidths=0.6,
            fmt='.4f',
            square=True,
            ax=ax)
ax.set_title('Mapa de Calor - Correlaciones', fontsize=14)

st.pyplot(fig, width='stretch')