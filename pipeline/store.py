import duckdb
from datetime import datetime
from .config import PROCESSED_DIR

def store_parquet(gdf):
    # 🔹 Convertir geometry -> WKT (texte)
    gdf = gdf.copy()
    gdf["geometry"] = gdf["geometry"].astype(str)

    path = PROCESSED_DIR / f"safecity_{datetime.now():%Y%m%d_%H%M%S}.parquet"

    con = duckdb.connect()
    con.register("gdf", gdf)

    con.execute("CREATE TABLE safecity AS SELECT * FROM gdf")
    con.execute(f"COPY safecity TO '{path}' (FORMAT PARQUET)")

    con.close()

    print(f"✅ Parquet généré : {path}")
