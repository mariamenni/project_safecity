from pathlib import Path
import duckdb
import geopandas as gpd
from shapely import wkt
import streamlit as st

def load_latest_parquet():
    files = sorted(Path("data/processed").glob("*.parquet"))
    if not files:
        raise FileNotFoundError("Aucun fichier parquet trouvé dans data/processed")


    con = duckdb.connect()
    df = con.execute(
        f"SELECT * FROM read_parquet('{files[-1]}')"
    ).df()
    con.close()

    # 🔹 Reconvertir WKT -> geometry
    df["geometry"] = df["geometry"].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

    return gdf
