import geopandas as gpd
from .config import GEO_URL

def fetch_geo() -> gpd.GeoDataFrame:
    gdf = gpd.read_file(GEO_URL)
    gdf["code"] = gdf["code"].astype(str).str.zfill(2)
    return gdf
