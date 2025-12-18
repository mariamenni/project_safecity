import pandas as pd

def transform_crimes(df: pd.DataFrame) -> pd.DataFrame:
    # 🔹 Exclure DOM (non présents dans le geojson)
    df = df[~df["Code_departement"].isin(["971", "972", "973", "974", "976"])]

    # 🔹 Supprimer lignes incohérentes
    df = df[df["nombre"] >= 0]

    # 🔹 Supprimer années aberrantes
    df = df[(df["annee"] >= 2010) & (df["annee"] <= df["annee"].max())]

    # 🔹 Variable temporelle
    df["periode"] = pd.cut(
        df["annee"],
        bins=[2010, 2015, 2020, 2025],
        labels=["2010-2015", "2016-2020", "2021-2025"]
    )

    return df
