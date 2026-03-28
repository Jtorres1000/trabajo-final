import streamlit as st


def pagina_inicio():
    df_processed = st.session_state.get('df_processed', None)
    st.title("Dashboard exploratorio de las canciones de Spotify (2015-2025)", anchor=False, text_alignment="center")
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.image("imagen/Spotify_New_Full_Logo_RGB_Green.png")
        st.markdown("### Bienvenido al dashboard interactivo exploratorio de datos de Spotify!", text_alignment="center")
        st.markdown("Aquí podrás visualizar e interactuar con la data de las canciones de Spotify lanzadas entre 2015 y 2025, cuenta con filtros y gráficos interactivos.", text_alignment="center")
    st.markdown("---")

    cancion_mas_corta = df_processed.sort_values(by="duration_min").head(1)

    r1, r2, r3 = st.columns([1,1,1])
    r1.metric("Total de canciones:", f"{len(df_processed)}")
    r2.metric("Duración promedio:", f"{df_processed['duration_min'].mean():.2f} min")
    r3.metric("Canción más corta.", f"{cancion_mas_corta["duration_min"].iloc[0]} min")
    st.markdown(
    """
    <div style="background-color: #f0f2f6; padding: 15px; margin-bottom:15px; border-radius: 10px; border-left: 5px solid #1DB954;">
        <p style="color: #31333F; margin: 0;">
            Usa el menú de navegación en la parte de arriba para navegar por las distintas páginas y explorar los datos de Spotify.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
    st.markdown(
    """
    <div style="background-color: #f0f2f6; padding: 15px; margin-bottom:15px; border-radius: 10px; border-left: 5px solid #1DB954;">
        <p style="color: #31333F; margin: 0;">
            Usa el menú de la izquierda para filtrar el dataset, a diferencia de los filtros en los gráficos, este remueve la data del dataset original.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)