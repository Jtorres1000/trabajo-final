import streamlit as st
from streamlit_echarts import st_echarts
from src.utils.calculos import calcular_metricas_correlacion

def pagina_analisis_correlacion():
    st.title("Análisis de correlación 🔗")

    corr_matrix, corr_nombres, datos_pyecharts = calcular_metricas_correlacion(st.session_state.get('df_filtered', None))
    
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