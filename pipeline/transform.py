import pandas as pd

def transform_crimes(df: pd.DataFrame) -> pd.DataFrame:
    # Exclure DOM (non présents dans le geojson)
    df = df[~df["Code_departement"].isin(["971", "972", "973", "974", "976"])]

    return df
