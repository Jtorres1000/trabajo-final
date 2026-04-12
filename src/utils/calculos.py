# src/utils/calculos.py
import pandas as pd

def calcular_metricas_duracion(df_filtered):
    
    duracion_pais_tiempo = df_filtered.groupby(['año', 'country'])['duration_min'].mean().reset_index()
    duracion_pais_tiempo = duracion_pais_tiempo.rename(columns={'country': 'país', 'duration_min': 'duración_promedio'})

    distribucion_años = df_filtered[['año', 'duration_min']].sort_values(by='año').reset_index(drop=True)
    media_anual_duracion = distribucion_años.groupby('año')['duration_min'].mean().reset_index(name='duración_promedio')
    años_lista = sorted(df_filtered['año'].unique().astype(str).tolist())

    duraciones_lista_boxplot = []

    for año in años_lista:
        # Filtramos el DataFrame original por cada año
        # Y extraemos TODOS los valores de duration_min en una lista
        valores_del_año = df_filtered[df_filtered['año'] == int(año)]['duration_min'].dropna().tolist()
        # Agregamos esta lista de valores a nuestra lista maestra
        duraciones_lista_boxplot.append(valores_del_año)
    
    
    return duracion_pais_tiempo, distribucion_años, media_anual_duracion, duraciones_lista_boxplot, años_lista

def calcular_metricas_tempo_energy(df_filtered):
    media_tempo_energy = df_filtered.groupby('año')[['tempo', 'energy']].mean().sort_values(by='año').reset_index()
    años_tempo_energy = df_filtered['año'].sort_values().unique().tolist()
    tempo_lista = media_tempo_energy['tempo'].tolist()
    energy_lista = media_tempo_energy['energy'].tolist()
    
    return media_tempo_energy, años_tempo_energy, tempo_lista, energy_lista

def calcular_metricas_correlacion(df_filtered):
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
            
    return corr_matrix, corr_nombres, datos_pyecharts

def calcular_minutos(minutos_decimales: float) -> str:
    if minutos_decimales is None:
        return "Sin datos"
    
    valor = float(minutos_decimales)
    
    minutos = int(valor)

    segundos = int(round((valor - minutos) * 60))

    if minutos > 1:
        minutos_texto = f"{minutos} minutos"
    elif minutos == 1:
        minutos_texto = f"{minutos} minuto"
    else:        minutos_texto = ""

    if segundos > 1:
        segundos_texto = f"{segundos} segundos"
    elif segundos == 1:        
        segundos_texto = f"{segundos} segundo"
    else:        segundos_texto = ""

    frase = f"{minutos_texto} y {segundos_texto}.".strip()

    return frase

def calcular_segmentos_distribucion(df_filtered, año_seleccionado=None):
    df_temp = df_filtered.copy()

    if año_seleccionado is not None:
        df_temp = df_temp[df_temp["año"].astype(str) == str(año_seleccionado)]

    # Agrupamos y contamos
    segmentos_tempo = df_temp.groupby(['segmento_tempo'], observed=False).size().reset_index(name='value')
    segmentos_energy = df_temp.groupby(['segmento_energy'], observed=False).size().reset_index(name='value')

    # Renombramos columnas para ECharts
    segmentos_tempo = segmentos_tempo.rename(columns={'segmento_tempo': 'name'})
    segmentos_energy = segmentos_energy.rename(columns={'segmento_energy': 'name'})

    # Convertimos a formato de diccionario para ECharts
    segmentos_tempo_serie = segmentos_tempo.to_dict('records')
    segmentos_energy_serie = segmentos_energy.to_dict('records')
        
    return segmentos_tempo_serie, segmentos_energy_serie
