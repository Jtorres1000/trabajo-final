import streamlit as st
from streamlit_echarts import st_echarts
from src.utils.calculos import calcular_metricas_tempo_energy

def pagina_analisis_tempo_energy():

    media_tempo_energy, años_tempo_energy, tempo_lista, energy_lista = calcular_metricas_tempo_energy(st.session_state.get('df_filtered', None))
    
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
            "min" : round(min(tempo_lista), 0) - 5 
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