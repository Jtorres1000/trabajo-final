import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import base64
from streamlit_echarts import st_echarts

# Configuración inicial de la app, tema, fuentes, etc.

PALETA_SPOTIFY = [
"#1DB954",
"#212121",
"#121212",
"#535353",
"#B3B3B3"
]

sns.set_palette(sns.color_palette(PALETA_SPOTIFY))
st.set_page_config(page_title="Spotify Dashboard", layout="wide", page_icon="🎵")

# Procesamiento, limpieza y carga de datos.

# Función para cargar el dataset
@st.cache_data
def cargar_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

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


# Menu lateral y filtros globales

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
    st.caption("Desarrollado usando Streamlit, pandas, matplotlib y streamlit_echarts 🐱.")

# Aplicar filtros
df_filtered = df_processed.copy()

if explicit:
    df_filtered = df_filtered[(df_filtered['explicit'] == True) | (df_filtered['explicit'] == False)]
else:
    df_filtered = df_filtered[df_filtered['explicit'] == False]

if selected_genre:
    df_filtered = df_filtered[df_filtered['genre'].isin(selected_genre)]
if selected_cities:
    df_filtered = df_filtered[df_filtered['country'].isin(selected_cities)]
if selected_labels:
    df_filtered = df_filtered[df_filtered['label'].isin(selected_labels)]

df_filtered = df_filtered[
    (df_filtered['release_date'].dt.year >= year_range[0]) & 
    (df_filtered['release_date'].dt.year <= year_range[1])
]

# Variables globales para los gráficos
df_filtered['año'] = df_filtered['release_date'].dt.year

duracion_pais_tiempo = df_filtered.groupby(['año', 'country'])['duration_min'].mean().reset_index()
duracion_pais_tiempo = duracion_pais_tiempo.rename(columns={'country': 'país', 'duration_min': 'duración_promedio'})

distribucion_años = df_filtered[['año', 'duration_min']].sort_values(by='año').reset_index(drop=True)
media_anual_duracion = distribucion_años.groupby('año')['duration_min'].mean().reset_index(name='duración_promedio')

media_tempo_energy = df_filtered.groupby('año')[['tempo', 'energy']].mean().sort_values(by='año').reset_index()
años_tempo_energy = df_filtered['año'].sort_values().unique().tolist()
tempo_lista = media_tempo_energy['tempo'].tolist()
energy_lista = media_tempo_energy['energy'].tolist()

columnas_corr = ['duration_min', 'popularity', 'tempo', 'energy', 'stream_count']
columnas_validas = [col for col in columnas_corr if col in df_filtered.columns]
corr_matrix = df_filtered[columnas_validas].corr()

corr_nombres = corr_matrix.columns.tolist() 

datos_pyecharts = []

for x_index in range(len(corr_nombres)): 
    for y_index in range(len(corr_nombres)): 
        
        valor = corr_matrix.iloc[y_index, x_index] 
        
        valor_redondeado = round(valor, 4)
        
        datos_pyecharts.append([x_index, y_index, valor_redondeado])

# Paginas del dashboard

def pagina_inicio():
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

def pagina_analisis_duracion():
    st.title("Análisis de duración 🔎")
    
    # Gráfico ECharts

    df_pivot = duracion_pais_tiempo.pivot(index='año', columns='país', values='duración_promedio')

    años, paises = df_pivot.index.tolist(), df_pivot.columns.tolist()
    
    series_data = []
    for pais in paises:
        valores = df_pivot[pais].where(pd.notnull(df_pivot[pais]), None).tolist()
        series_data.append({
            "name": pais, "type": "line", "data": valores,
            "emphasis": {"focus": "series"}
        })

    options = {
    "title": {"text": "Duración Promedio por Año y País"},
    "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
    "legend": {
        "data": paises,
        "type": "scroll",
        "orient": "vertical",
        "right": "0",
        "top": "center",
        "padding": [5, 10]
    },
    "grid": {
        "left": "3%",
        "right": "15%", 
        "bottom": "15%",
        "containLabel": True
    },
    "xAxis": {
        "type": "category", 
        "boundaryGap": False, 
        "data": años
    },
    "yAxis": {
        "type": "value", 
        "name": "Minutos", 
        "min": 3.5, 
        "max": 5
    },
    "dataZoom": [
        {
            "type": "slider", 
            "xAxisIndex": 0,
            "bottom": "5%"
        }, 
        {
            "type": "inside", 
            "xAxisIndex": 0
        }
    ],
    "series": series_data
}
    st_echarts(options=options, height="500px", key="pyechart-line-duracion-promedio")

    # Gráfico de Caja Plotly
    fig_box = px.box(
        distribucion_años, x='año', y='duration_min', 
        title="Gráfico de caja y bigotes según el año de lanzamiento y la duración en minutos", 
        labels={"año": "Año de lanzamiento", 'duration_min': "Duración (minutos)"}, 
        color_discrete_sequence=PALETA_SPOTIFY
    )
    fig_box.update_xaxes(type='category')
    st.plotly_chart(fig_box, width='stretch')

    # Gráfico de barras

    # Convertimos las columnas a listas normales (ECharts no lee Series de Pandas directamente)
    años_lista = media_anual_duracion["año"].tolist()
    duraciones_lista = media_anual_duracion["duración_promedio"].tolist()
    options = {
        "title": {
        "text": "Valor de duración promedio según el año",
        "left": "center",
        "top": "2%"
    },
    
    "toolbox": {
        "show": True,
        "orient": "vertical", 
        "left": "right",
        "top": "center",
        "feature": {
            "saveAsImage": { 
                "show": True, 
                "title": "Descargar PNG", 
                "type": "png", 
                "pixelRatio": 2 
            }
        }
    },
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {
            "type": "shadow"
        }
    },
    "grid": {
        "left": "3%",
        "right": "4%",
        "bottom": "8%",
        "containLabel": True
    },
    "xAxis": [
        {
            "name": "Año de lanzamiento",
            "nameLocation":"middle",
            "nameGap": 30,
            "type": "category",
            "data": años_lista,        
            "axisTick": {
                "alignWithLabel": True
            }
        }
    ],
    "yAxis": [
        {
            "type": "value",
            "name": "Minutos",
            "min" : 3.5
        }
    ],
    "series": [
        {
            "name": "Duración",
            "type": "bar",
            "barWidth": "60%",
            "data": duraciones_lista,   
            "itemStyle": {
                "color": "#1DB954"       
            }
        }
    ]
}
    st_echarts(options=options, height="500px", key="pyechart-bar-duracion")

def pagina_analisis_tempo_energy():
    st.title("Análisis de tempo y energy 🎶")
    options = {
        "title": {
        "text": "Valor de Tempo promedio según el año",
        "left": "center",
        "top": "2%"
    },
    
    "toolbox": {
        "show": True,
        "orient": "vertical", 
        "left": "right",
        "top": "center",
        "feature": {
            "saveAsImage": { 
                "show": True, 
                "title": "Descargar PNG", 
                "type": "png", 
                "pixelRatio": 2 
            }
        }
    },
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {
            "type": "shadow"
        }
    },
    "grid": {
        "left": "3%",
        "right": "4%",
        "bottom": "8%",
        "containLabel": True
    },
    "xAxis": [
        {
            "type": "category",
            "name": "Año de lanzamiento",
            "nameLocation":"middle",
            "nameGap": 30,
            "data": años_tempo_energy,        
            "axisTick": {
                "alignWithLabel": True
            }
        }
    ],
    "yAxis": [
        {
            "type": "value",
            "name": "Tempo",
            "min" : 126  
        }
    ],
    "series": [
        {
            "name": "Tempo",
            "type": "bar",
            "barWidth": "60%",
            "data": tempo_lista, 
            "itemStyle": {
                "color": "#3b07a3"       
            }
        }
    ]
}
    st_echarts(options=options, height="500px", key="pyechart-line-duracion-energy")
    options = {
    "title": {
        "text": "Valor de Energy promedio según el año",
        "left": "center",
        "top": "2%"
    },
    
    "toolbox": {
        "show": True,
        "orient": "vertical", 
        "left": "right",
        "top": "center",
        "feature": {
            "saveAsImage": { 
                "show": True, 
                "title": "Descargar PNG", 
                "type": "png", 
                "pixelRatio": 2 
            }
        }
    },
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {
            "type": "shadow"
        }
    },
    "grid": {
        "left": "3%",
        "right": "4%",
        "bottom": "8%",
        "containLabel": True
    },
    "xAxis": [
        {
            "type": "category",
            "name": "Año de lanzamiento",
            "nameLocation":"middle",
            "nameGap": 30,
            "data": años_tempo_energy,        
            "axisTick": {
                "alignWithLabel": True
            }
        }
    ],
    "yAxis": [
        {
            "type": "value",
            "name": "Energy",
            "min": 0.4
        }
    ],
    "series": [
        {
            "name": "Energy",
            "type": "bar",
            "barWidth": "60%",
            "data": energy_lista, 
            "itemStyle": {
                "color": "#b2919c"       
            }
        }
    ]
}
    st_echarts(options=options, height="500px", key="pyechart-line-duracion-tempo")

def pagina_data_tablas():
    st.title("Data en tablas 📈")
    st.write(f"**Mostrando {len(df_filtered)} canciones:**")

    st.markdown("### Datos en tablas filtrados:")
    st.dataframe(df_filtered, width='stretch')

    st.markdown("### Duración promedio por país y año:")
    st.dataframe(duracion_pais_tiempo, width='stretch')

    st.markdown("### Duración de las canciones agrupadas por año:")
    st.dataframe(distribucion_años, width='stretch')

    st.markdown("### Duración promedio de las canciones por año")
    st.dataframe(media_anual_duracion, width='stretch')

    st.markdown("### Matriz de correlación de las variables:")
    st.dataframe(corr_matrix, width='stretch')

    st.markdown("### Media de tiempo y energy por año:")
    st.dataframe(media_tempo_energy, width='stretch')

def pagina_analisis_correlacion():
    st.title("Análisis de correlación 🔗")

    options = {
    "title": {
        "text": "Matriz de Correlación de Variables",
        "left": "center",
        "top": "2%"
    },
    
    "toolbox": {
        "show": True,
        "orient": "vertical", 
        "left": "right",
        "top": "center",
        "feature": {
            "saveAsImage": { 
                "show": True, 
                "title": "Descargar PNG", # Texto al pasar el cursor
                "type": "png", # O jpg, svg
                "pixelRatio": 2 # Aumenta la resolución para que no se vea pixelada
            }
        }
    },
    "tooltip": {
        "position": "top"
    },
    "grid": {
        "height": "75%",
        "top": "10%"
    },
    "xAxis": {
        "type": "category",
        "data": corr_nombres,
        "splitArea": {"show": True},
        "axisLabel": {
            "interval": 0, # Fuerza a que se muestren todas las etiquetas
        }
    },
    "yAxis": {
        "type": "category",
        "data": corr_nombres,
        "splitArea": {"show": True}
    },
    "visualMap": {
        "min": -1,
        "max": 1,
        "calculable": True,
        "orient": "horizontal",
        "left": "center",
        "bottom": "2%",
        "inRange": {
            "color": ["#2166ac", "#abd9e9", "#f7f7f7", "#f4a582", "#b2182b"]
        }
    },
    "series": [
        {
            "name": "Coeficiente de correlación",
            "type": "heatmap",
            "data": datos_pyecharts,
            "label": {
                "show": True,
                "color": "#000000" 
            },
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowColor": "rgba(0, 0, 0, 0.5)"
                }
            }
        }
    ]
}
    st_echarts(options=options, height="500px")

# Sistema de navegación entre páginas

# Convertimos las funciones a objetos st.Page para poder acceder a ellas desde el menú de navegación

p_inicio = st.Page(pagina_inicio, title="Inicio", icon="🏠")
p_duracion = st.Page(pagina_analisis_duracion, title="Análisis de duración", icon="🔎")
p_tempo = st.Page(pagina_analisis_tempo_energy, title="Análisis de tempo y energy", icon="🎶")
p_tablas = st.Page(pagina_data_tablas, title="Data en tablas", icon="📈")
p_correlacion = st.Page(pagina_analisis_correlacion, title="Análisis de Correlación", icon="🔗")

# Creamos el menú y lo ejecutamos
pg = st.navigation([p_inicio, p_duracion, p_tempo, p_tablas, p_correlacion], position="top")
pg.run()