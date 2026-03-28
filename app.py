import streamlit as st
import seaborn as sns

from src.utils import cargar_csv, preprocesar_datos, aplicar_filtros
from src.components import sidebar
from src.pages import pagina_inicio, pagina_analisis_duracion, pagina_analisis_tempo_energy, pagina_data_tablas, pagina_analisis_correlacion


# Configuración inicial de la app, tema, fuentes, etc.

PALETA_SPOTIFY = [
"#1DB954",
"#212121",
"#121212",
"#535353",
"#B3B3B3"
]

st.session_state["PALETA_SPOTIFY"] = PALETA_SPOTIFY
sns.set_palette(sns.color_palette(PALETA_SPOTIFY))
st.set_page_config(page_title="Spotify Dashboard", layout="wide", page_icon="🎵")

# Carga inicial
df = cargar_csv("18. Spotify 2015-2025.csv")
df_processed = preprocesar_datos(df)

# Inicializar los datos en el session_state
if 'df_processed' not in st.session_state:
    st.session_state['df_processed'] = df_processed

# Menu lateral y filtros globales

selected_cities, year_range, selected_genre, selected_labels, explicit = sidebar()

st.session_state['df_filtered'] = aplicar_filtros(
    st.session_state['df_processed'], 
    explicit, 
    selected_genre, 
    selected_cities, 
    selected_labels, 
    year_range
)

df_filtered = st.session_state['df_filtered']

# Paginas del dashboard

p_inicio = st.Page(pagina_inicio, title="Inicio", icon="🏠")
p_duracion = st.Page(pagina_analisis_duracion, title="Análisis de duración", icon="🔎")
p_tempo = st.Page(pagina_analisis_tempo_energy, title="Análisis de tempo y energy", icon="🎶")
p_tablas = st.Page(pagina_data_tablas, title="Data en tablas", icon="📈")
p_correlacion = st.Page(pagina_analisis_correlacion, title="Análisis de Correlación", icon="🔗")

# Creamos el menú y lo ejecutamos
pg = st.navigation([p_inicio, p_duracion, p_tempo, p_tablas, p_correlacion], position="top")
pg.run()