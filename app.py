import streamlit as st
import geopandas as gpd
import plotly.express as px
from utils.data import load_latest_parquet

st.set_page_config(layout="wide")
st.title("🏛️ SafeCity — Sécurité urbaine")

# 🔹 Charger les données
gdf = load_latest_parquet()

# 🔹 S'assurer que le CRS est correct
if gdf.crs is None:
    gdf = gdf.set_crs(epsg=4326)

# 🔹 Filtres
annee = st.selectbox("Année", sorted(gdf["annee"].unique()))
delit = st.selectbox("Type de délit", sorted(gdf["indicateur"].unique()))

gdf_f = gdf[
    (gdf["annee"] == annee) &
    (gdf["indicateur"] == delit)
]

# 🔹 Conversion GeoDataFrame -> GeoJSON
geojson = gdf_f.__geo_interface__

# 🔹 Carte choroplèthe
fig = px.choropleth(
    gdf_f,
    geojson=geojson,
    locations=gdf_f.index,
    color="taux_pour_100k",
    hover_name="nom",
    title=f"{delit} en {annee}",
    color_continuous_scale="Reds"
)

# 🔹 Zoom automatique + nettoyage visuel
fig.update_geos(
    fitbounds="locations",
    visible=False
)

st.plotly_chart(fig, use_container_width=True)
