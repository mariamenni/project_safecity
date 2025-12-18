import requests
import pandas as pd
from .config import COMMUNES_URL

def fetch_population() -> pd.DataFrame:
    data = requests.get(COMMUNES_URL).json()
    df = pd.DataFrame(data)

    df["population"] = df["population"].fillna(0).astype(int)
    df["codeDepartement"] = df["codeDepartement"].astype(str).str.zfill(2)

    df_dep = (
        df.groupby("codeDepartement", as_index=False)["population"]
        .sum()
    )

    return df_dep
