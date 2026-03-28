import pandas as pd
import numpy as np

def preprocesar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocesa el DataFrame de Spotify."""
    df = df.convert_dtypes()
    df = df.head(15000).copy()
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df["duration_ms"] = df["duration_ms"].div(1000 * 60).round(2)
    df = df.rename(columns={'duration_ms': 'duration_min'})
    df['release_date'] = pd.to_datetime(df['release_date'])
    df['año'] = df['release_date'].dt.year

    return df