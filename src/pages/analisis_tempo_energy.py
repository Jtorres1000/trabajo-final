from pyparsing import col
import streamlit as st
from streamlit_echarts import st_echarts
from src.utils.calculos import calcular_metricas_tempo_energy, calcular_minutos, calcular_segmentos_distribucion

def pagina_analisis_tempo_energy():
    media_tempo_energy, años_tempo_energy, tempo_lista, energy_lista = calcular_metricas_tempo_energy(st.session_state.get('df_filtered', None))
    segmentos_tempo_serie, segmentos_energy_serie = calcular_segmentos_distribucion(st.session_state.get('df_filtered', None))

    st.title("Análisis de tempo y energy 🎶")

    st.markdown(
    f"""
    <div style="background-color: #f0f2f6; padding: 15px; margin-bottom:15px; border-radius: 10px; border-left: 5px solid #1DB954;">
        <p style="color: #31333F; margin: 0;">
            Estos gráficos son reactivos, prueba a clickear una barra del lado izquierdo para ver la distribución por categorías para ese año en partícular.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

    #Opciones y eventos del gráfico de barras tempo
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
    events = {
    "click": "function(params) { return [params.type, params.name, params.value] }",
}

    col1, col2 = st.columns(2)

    with col1:
        bar_event = st_echarts(options=options, height="500px", key="pyechart-bar-tempo", events=events)

    año_seleccionado = None

    if bar_event and "chart_event" in bar_event and bar_event["chart_event"] is not None:
        evento = bar_event["chart_event"]
        año_seleccionado = evento[1] 

    segmentos_tempo_serie, _ = calcular_segmentos_distribucion(st.session_state.get('df_filtered', None), año_seleccionado)
    
    #Opciones del gráfico de sectores según las categorías de tempo 

    titulo_pie = f'Distribución de tempo en {año_seleccionado}' if año_seleccionado else 'Distribución de tempo global'
    options_pie = {
            'title': {
                'text': titulo_pie,
                'left': 'center'
            },
            'color': ['#F4D2D7', '#48161E', '#792264'],
            'tooltip': {
                'trigger': 'item'
            },
            'legend': {
                'orient': 'vertical',
                'left': 'left'
            },
            'series': [
                {
                    'name': 'Valor',
                    'type': 'pie',
                    'radius': '50%',
                    'data': segmentos_tempo_serie, 
                    'label': {
                        'show': True,
                        'formatter': '{b}\n{d}%' 
                    },
                    'emphasis': {
                        'itemStyle': {
                            'shadowBlur': 10,
                            'shadowOffsetX': 0,
                            'shadowColor': 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        }
        
    #Gráfico de sectores según las categorías de tempo
    with col2:

        st_echarts(options=options_pie, height="500px", key="pyechart-pie-categorias-tempo")

#Opciones y eventos del gráfico de barras de energy promedio.
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
    events = {
    "click": "function(params) { return [params.type, params.name, params.value] }",
}
    
    with col1:
        bar_two_event = st_echarts(options=options, height="500px", key="pyechart-bar-duracion-tempo", events=events)

    año_seleccionado_energy = None

    if bar_two_event and "chart_event" in bar_two_event and bar_two_event["chart_event"] is not None:
        evento = bar_two_event["chart_event"]
        año_seleccionado_energy = evento[1]
        _, segmentos_energy_serie = calcular_segmentos_distribucion(st.session_state.get('df_filtered', None), año_seleccionado_energy)

#Opciones del gráfico de sectores según las categorías de energy
    titulo_pie_energy = f'Distribución de energy en {año_seleccionado_energy}' if año_seleccionado_energy else 'Distribución de energy global'
    options_pie = {
        'title': {
            'text': titulo_pie_energy,
            'left': 'center'
        },
        "color": ['#C69CF6', '#2B1647', '#E7D8BD'],
        'tooltip': {
            'trigger': 'item'
        },
        'legend': {
            'orient': 'vertical',
            'left': 'left'
        },
        'label': {
        'show': True,
        'formatter': '{b}\n{d}%' 
        },
        'series': [
            {
                'name': 'Access From',
                'type': 'pie',
                'radius': '50%',
                'data': segmentos_energy_serie,
                'emphasis': {
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowOffsetX': 0,
                        'shadowColor': 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    }
    
    with col2:
        st_echarts(options=options_pie, height="500px", key="pyechart-pie-categorias-energy")