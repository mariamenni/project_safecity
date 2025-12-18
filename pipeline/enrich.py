import pandas as pd
import geopandas as gpd

def enrich_data(crimes, population, geo):

    df = crimes.merge(
        population,
        left_on="Code_departement",
        right_on="codeDepartement",
        how="left"
    )

    # 🔹 Taux standardisé
    df["taux_pour_100k"] = (
        df["nombre"] / df["population"] * 100_000
    ).replace([float("inf")], 0).fillna(0)

    # 🔹 Évolution annuelle par département et délit
    df = df.sort_values(["Code_departement", "indicateur", "annee"])
    df["evolution_%"] = (
        df.groupby(["Code_departement", "indicateur"])["taux_pour_100k"]
        .pct_change() * 100
    ).fillna(0)

    # 🔹 Moyenne mobile (3 ans)
    df["moyenne_mobile_3a"] = (
        df.groupby(["Code_departement", "indicateur"])["taux_pour_100k"]
        .rolling(3)
        .mean()
        .reset_index(level=[0,1], drop=True)
    )

    gdf = geo.merge(
        df,
        left_on="code",
        right_on="Code_departement",
        how="left"
    )

    return gdf