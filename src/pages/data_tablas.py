import streamlit as st
from src.utils.calculos import calcular_metricas_correlacion, calcular_metricas_duracion, calcular_metricas_tempo_energy
def pagina_data_tablas():

    df_filtered = st.session_state.get('df_filtered', None)

    duracion_pais_tiempo, distribucion_años, media_anual_duracion = calcular_metricas_duracion(df_filtered)
    media_tempo_energy, años_tempo_energy, tempo_lista, energy_lista = calcular_metricas_tempo_energy(df_filtered)
    corr_matrix, corr_nombres, datos_pyecharts = calcular_metricas_correlacion(df_filtered)

    st.title("Data en tablas 📈")
    st.write(f"**Mostrando {len(df_filtered)} canciones:**")

    st.markdown("### Datos en tablas filtrados:")
    st.dataframe(df_filtered[["release_date", "genre", "duration_min", "popularity", "stream_count", "energy", "country", "explicit", "label", "año"]], width='stretch')

    st.markdown("### Duración promedio por país y año:")
    st.dataframe(duracion_pais_tiempo, width='stretch')

    st.markdown("### Duración promedio de las canciones por año")
    st.dataframe(media_anual_duracion, width='stretch')

    st.markdown("### Matriz de correlación de las variables:")
    st.dataframe(corr_matrix, width='stretch')

    st.markdown("### Media de tiempo y energy por año:")
    st.dataframe(media_tempo_energy, width='stretch')
