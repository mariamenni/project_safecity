import pandas as pd
from .config import CRIMES_URL

def fetch_crimes() -> pd.DataFrame:
    df = pd.read_csv(CRIMES_URL, sep=";", low_memory=False)

    # Correction typage
    df["Code_departement"] = df["Code_departement"].astype(str).str.zfill(2)
    df["annee"] = df["annee"].astype(int)
    df["nombre"] = df["nombre"].fillna(0).astype(int)

    # taux avec virgule -> float
    df["taux_pour_mille"] = (
        df["taux_pour_mille"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    return df
