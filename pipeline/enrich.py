import pandas as pd
import geopandas as gpd

def enrich_data(
    crimes: pd.DataFrame,
    population: pd.DataFrame,
    geo: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:

    df = crimes.merge(
        population,
        left_on="Code_departement",
        right_on="codeDepartement",
        how="left"
    )

    df["taux_pour_100k"] = (
        df["nombre"] / df["population"] * 100_000
    ).fillna(0)

    gdf = geo.merge(
        df,
        left_on="code",
        right_on="Code_departement",
        how="left"
    )

    return gdf
