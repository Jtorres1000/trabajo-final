import streamlit as st
from src.utils.background_sidebar import background_sidebar


def sidebar():
    df_processed = st.session_state.get('df_processed', None)
    with st.sidebar:
        background_sidebar("imagen/Background 17.png")
        col1, col2, col3 = st.columns([1,1,1])

        with col2:
            st.image("imagen/Spotify_Primary_Logo_RGB_Green.png", width=100)
        st.audio("imagen/Spotify Wrapped 2025 Background Music (High Quality).mp3", start_time=5, autoplay= True, loop= True)
        st.header("Filtros de búsqueda")

        cities = df_processed['country'].dropna().unique()
        años_disponibles = sorted(df_processed['release_date'].dt.year.dropna().unique())
        genres = df_processed['genre'].unique()
        labels = df_processed['label'].unique()

        selected_cities = st.multiselect(
            "Selecciona una o más ciudades:", 
            cities, 
            default=["Canada", "Brazil", "Germany"], 
            help="Filtra la data según uno o más países.", 
            placeholder="Escoge una opción..."
        )

        year_range = st.select_slider(
            "Selecciona un rango de años:", 
            options=años_disponibles, 
            help="Friltra la data según un rango de años.",
            value=(2015, 2025)
        )
        
        selected_genre = st.multiselect(
            "Selecciona uno o más generos:",
            genres,
            default =["Reggaeton", "Pop", "Hip-Hop"],
            help="Friltra la data según uno o más géneros musicales.",
            placeholder="Escoge una opción..."
        )
        selected_labels = st.multiselect(
            "Selecciona una o mas sellos discográficos:",
            labels,
            default =["Sony Music", "Warner Music", "XL Recordings"],
            help="Filtra la data según uno o más sellos discográficos.",
            placeholder="Escoge una opción..."
        )
        
        explicit = st.toggle("Incluir canciones explícitas", value=True, help="Activa o desactiva la inclusión de canciones con contenido explícito.")
        st.markdown("---")
        st.markdown("##### Acerca de este dashboard:")
        st.caption("Desarrollado usando Streamlit, pandas y streamlit_echarts 🐱.")
        return selected_cities, year_range, selected_genre, selected_labels, explicit

