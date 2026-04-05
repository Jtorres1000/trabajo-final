# src/utils/calculos.py
import pandas as pd

def calcular_metricas_duracion(df_filtered):
    
    duracion_pais_tiempo = df_filtered.groupby(['año', 'country'])['duration_min'].mean().reset_index()
    duracion_pais_tiempo = duracion_pais_tiempo.rename(columns={'country': 'país', 'duration_min': 'duración_promedio'})

    distribucion_años = df_filtered[['año', 'duration_min']].sort_values(by='año').reset_index(drop=True)
    media_anual_duracion = distribucion_años.groupby('año')['duration_min'].mean().reset_index(name='duración_promedio')
    
    return duracion_pais_tiempo, distribucion_años, media_anual_duracion

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
    
    return f"{minutos} minutos y {segundos} segundos."
