import streamlit as st
from src.utils.calculos import calcular_minutos

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
    r1.metric("Total de canciones:", f"{len(df_processed)}", border=True)
    r2.metric("Duración promedio:", f"{calcular_minutos(df_processed['duration_min'].mean())}", border=True)
    r3.metric("Canción más corta.", f"{calcular_minutos(cancion_mas_corta['duration_min'].iloc[0])}", border=True)

    t1, t2, t3 = st.columns([1,1,1])
    with t1:
        st.markdown(
        """
        <div style="height: 360px;font-size:18px; color:#54151d;  padding: 15px; margin-bottom:15px; border-radius: 10px; background: linear-gradient(357deg, #94bbe9, #fe6f61); background-size: 400% 400%; animation: AnimationName 7s ease infinite; -webkit-animation: AnimationName 7s ease infinite;">
            <div style="background: #f5d6db; padding:20px; height:100%;">
            <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" fill="#54151d" class="bi bi-spotify" viewBox="0 0 16 16">
            <path d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0m3.669 11.538a.5.5 0 0 1-.686.165c-1.879-1.147-4.243-1.407-7.028-.77a.499.499 0 0 1-.222-.973c3.048-.696 5.662-.397 7.77.892a.5.5 0 0 1 .166.686m.979-2.178a.624.624 0 0 1-.858.205c-2.15-1.321-5.428-1.704-7.972-.932a.625.625 0 0 1-.362-1.194c2.905-.881 6.517-.454 8.986 1.063a.624.624 0 0 1 .206.858m.084-2.268C10.154 5.56 5.9 5.419 3.438 6.166a.748.748 0 1 1-.434-1.432c2.825-.857 7.523-.692 10.492 1.07a.747.747 0 1 1-.764 1.288"/>
            </svg>
            <h3>Navegación</h3>
            <p >
                Usa el menú de navegación en la parte de arriba para navegar por las distintas páginas y explorar los datos de Spotify.
            </p>
            </div>
        </div>

        <style>
            @keyframes AnimationName {
                0% { background-position: 50% 0%; }
                50% { background-position: 51% 100%; }
                100% { background-position: 50% 0%; }
            }

            @-webkit-keyframes AnimationName {
                0% { background-position: 50% 0%; }
                50% { background-position: 51% 100%; }
                100% { background-position: 50% 0%; }
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    with t2:
        st.markdown(
        """
        <div style="height: 360px;font-size:18px; color:#ecdbbb;  padding: 15px; margin-bottom:15px; border-radius: 10px; background: linear-gradient(357deg, #ca2faf, #d18c3f); background-size: 400% 400%; animation: AnimationName 7s ease infinite; -webkit-animation: AnimationName 7s ease infinite;">
            <div style="background: #7f1c6c; padding:20px; height:100%;">
            <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" fill="#ecdbbb" class="bi bi-spotify" viewBox="0 0 16 16">
            <path d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0m3.669 11.538a.5.5 0 0 1-.686.165c-1.879-1.147-4.243-1.407-7.028-.77a.499.499 0 0 1-.222-.973c3.048-.696 5.662-.397 7.77.892a.5.5 0 0 1 .166.686m.979-2.178a.624.624 0 0 1-.858.205c-2.15-1.321-5.428-1.704-7.972-.932a.625.625 0 0 1-.362-1.194c2.905-.881 6.517-.454 8.986 1.063a.624.624 0 0 1 .206.858m.084-2.268C10.154 5.56 5.9 5.419 3.438 6.166a.748.748 0 1 1-.434-1.432c2.825-.857 7.523-.692 10.492 1.07a.747.747 0 1 1-.764 1.288"/>
            </svg>
            <h3>Filtrado</h3>
            <p >
                Usa el menú de la izquierda para filtrar el dataset, a diferencia de los filtros en los gráficos, este remueve la data del dataset original.
            </p>
            </div>
        </div>

        <style>
        @keyframes AnimationName {
            0% { background-position: 50% 0%; }
            50% { background-position: 51% 100%; }
            100% { background-position: 50% 0%; }
        }

        @-webkit-keyframes AnimationName {
            0% { background-position: 50% 0%; }
            50% { background-position: 51% 100%; }
            100% { background-position: 50% 0%; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
        with t3:
            st.markdown(
        """
        <div style="height: 360px; font-size:18px; color:#3a1d44; padding: 15px; margin-bottom:15px; border-radius: 10px; background: linear-gradient(359deg, #fdd87d, #f69acd); background-size: 400% 400%; animation: AnimationName 8s ease infinite; -webkit-animation: AnimationName 8s ease infinite;">
            <div style="background: #daa3fe; padding:20px; height:100%;">
            <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" fill="#3a1d44" class="bi bi-spotify" viewBox="0 0 16 16">
            <path d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0m3.669 11.538a.5.5 0 0 1-.686.165c-1.879-1.147-4.243-1.407-7.028-.77a.499.499 0 0 1-.222-.973c3.048-.696 5.662-.397 7.77.892a.5.5 0 0 1 .166.686m.979-2.178a.624.624 0 0 1-.858.205c-2.15-1.321-5.428-1.704-7.972-.932a.625.625 0 0 1-.362-1.194c2.905-.881 6.517-.454 8.986 1.063a.624.624 0 0 1 .206.858m.084-2.268C10.154 5.56 5.9 5.419 3.438 6.166a.748.748 0 1 1-.434-1.432c2.825-.857 7.523-.692 10.492 1.07a.747.747 0 1 1-.764 1.288"/>
            </svg>
            <h3>Interacción</h3>
            <p >
                Algunos gráficos cuentan con filtros interactivos, estos no remueven la data del dataset original, sino que solo filtran lo que se muestra en el gráfico.
            </p>
            </div>
        </div>
        <style>
            @-webkit-keyframes AnimationName {
                0%{background-position:49% 0%}
                50%{background-position:52% 100%}
                100%{background-position:49% 0%}
            }
            @-moz-keyframes AnimationName {
                0%{background-position:49% 0%}
                50%{background-position:52% 100%}
                100%{background-position:49% 0%}
            }
            @keyframes AnimationName {
                0%{background-position:49% 0%}
                50%{background-position:52% 100%}
                100%{background-position:49% 0%}
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.info("Puedes acceder al informe estadístico mediante el siguiente enlace: https://trabajo-final-informe.onrender.com/R/informe.pdf", icon=":material/picture_as_pdf:")