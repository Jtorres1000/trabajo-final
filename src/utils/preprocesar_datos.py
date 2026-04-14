import pandas as pd
import numpy as np

#Energy min 0.02 energy max 0.99, tempo min 60, tempo max 200 [60-90 lento, 90-120 medio, 120-200 rápido]

def preprocesar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocesa el DataFrame de Spotify."""
    df = df.convert_dtypes()
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df= df.head(15000)
    df["duration_ms"] = df["duration_ms"].div(1000 * 60).round(2)
    df = df.rename(columns={'duration_ms': 'duration_min'})
    df['release_date'] = pd.to_datetime(df['release_date'])
    df['año'] = df['release_date'].dt.year
    df["segmento_tempo"] = pd.cut(df['tempo'], bins=[60, 90, 120, 200], labels=['Lenta', 'Medio', 'Rápida'])
    df["segmento_energy"] = pd.cut(df['energy'], bins=[0.02, 0.33, 0.66, 0.99], labels=['Baja', 'Media', 'Alta'])

    return df