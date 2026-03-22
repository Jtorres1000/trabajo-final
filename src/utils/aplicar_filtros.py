# Aplicar filtros
def aplicar_filtros(df_processed, explicit, selected_genre, selected_cities, selected_labels, year_range):
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
    
    return df_filtered
