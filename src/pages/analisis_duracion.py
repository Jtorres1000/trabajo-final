import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_echarts import st_echarts, Map
from src.utils.calculos import calcular_metricas_duracion
from src.utils.cargar_json import load_map_data

def pagina_analisis_duracion():

    duracion_pais_tiempo, distribucion_años, media_anual_duracion = calcular_metricas_duracion(st.session_state.get('df_filtered', None))
    df_processed = st.session_state.get('df_processed', None)
    PALETA_SPOTIFY = st.session_state["PALETA_SPOTIFY"]

    st.title("Análisis de duración 🔎")
    
    # Gráfico ECharts

    df_pivot = duracion_pais_tiempo.pivot(index='año', columns='país', values='duración_promedio')

    años, paises = df_pivot.index.tolist(), df_pivot.columns.tolist()

    series_data = []
    series_mapa_data = {}

    for año, fila in df_pivot.iterrows():
        año_str = str(año) 
        data_del_año = []
        
        for pais, valor in fila.items():
            
            data_del_año.append({
                "name": pais, 
                "value": round(valor, 3) 
            })
            
        series_mapa_data[año_str] = data_del_año

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
        "min": duracion_pais_tiempo['duración_promedio'].min().round() - 1,
        "max": duracion_pais_tiempo['duración_promedio'].max().round() + 1
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

    # Convertimos las columnas a listas normales
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
            "min" : 3
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

    world_geojson = load_map_data()

    map_obj = Map(map_name="world", geo_json=world_geojson)



    año_seleccionado = st.selectbox(
        "Selecciona el año para cargar la data de un año en concreto.",
        options= sorted(df_processed['release_date'].dt.year.dropna().unique()),
        index=0 # Por defecto, la primera opción ("Inicial (en blanco)")
    )

    options = {
    "title": {
        "text": f"Duración Promedio de canciones por país para el año {año_seleccionado}",
        "left": "center"
    },
    "tooltip": {
        "trigger": "item",
        "showDelay": 0,
        "transitionDuration": 0.3,
    },
    "visualMap": {
        "text": ["Mayor duración", "Menor duración"],
        "realtime": False,
        "calculable": True,
        "min": series_mapa_data.get(str(año_seleccionado), [{"value": 0}])[0]["value"],
        "max": series_mapa_data.get(str(año_seleccionado), [{"value": 0}])[-1]["value"],
        "inRange": {
            "color": ["#ffffbf", "#fdae61", "#d73027"] 
        }
    },
    "series": [
        {
            "name": "Duración Promedio",
            "type": "map",
            "map": "world", 
            "roam": True,   
            "itemStyle": {
                "emphasis": {"label": {"show": True}}
            },
            "data": series_mapa_data.get(str(año_seleccionado), [])
        }
    ]
}
    st_echarts(options=options, map=map_obj, height="600px")

    st.markdown(
    """
    <div style="background-color: #f0f2f6; padding: 15px; margin-bottom:15px; border-radius: 10px; border-left: 5px solid #1DB954;">
        <p style="color: #31333F; margin: 0;">
            Este gráfico solo puede mostrar la data de un año, asegurate de no tener filtros del rango de años activados en el sidebar.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)