import streamlit as st
import geopandas as gpd
import plotly.express as px
import pandas as pd
from utils.data import load_latest_parquet

# --- 1. CONFIGURATION ---
st.set_page_config(layout="wide", page_title="SafeCity Dashboard", page_icon="🛡️")

# --- 2. CHARGEMENT DES DONNÉES ---
@st.cache_data
def get_data():
    gdf = load_latest_parquet()
    # S'assurer que le CRS est correct
    if gdf.crs is None:
        gdf = gdf.set_crs(epsg=4326)
    return gdf

gdf = get_data()

# --- 3. SIDEBAR (Filtres) ---
with st.sidebar:
    st.title("🛡️ SafeCity")
    st.markdown("---")
    
    # Filtres
    annee = st.selectbox("📅 Année", sorted(gdf["annee"].unique(), reverse=True))
    delit = st.selectbox("⚖️ Type de délit", sorted(gdf["indicateur"].unique()))
    
    st.markdown("---")
    st.info("💡 Utilisez les filtres pour mettre à jour la carte et l'analyse IA.")

# --- 4. PRÉPARATION DES DONNÉES ---

# A. Données pour la Carte et les KPIs (Année spécifique)
gdf_filtered = gdf[
    (gdf["annee"] == annee) &
    (gdf["indicateur"] == delit)
].copy()

# B. Données pour l'Historique (Toutes les années pour ce délit)
df_history = gdf[gdf["indicateur"] == delit].copy()

# --- 5. INDICATEURS CLÉS (KPIs) ---
st.title(f"Analyse : {delit} ({annee})")

col1, col2, col3, col4 = st.columns(4)

# Calculs
total_faits = gdf_filtered["nombre"].sum()
taux_moyen = gdf_filtered["taux_pour_100k"].mean()
# Trouver le pire département
pire_dept = gdf_filtered.loc[gdf_filtered["taux_pour_100k"].idxmax()]
# Trouver le département le plus sûr
meilleur_dept = gdf_filtered.loc[gdf_filtered["taux_pour_100k"].idxmin()]

# Affichage
col1.metric("Total Faits", f"{total_faits:,}".replace(",", " "))
col2.metric("Taux Moy. / 100k", f"{taux_moyen:.1f}")
col3.metric("⚠️ Plus touché", f"{pire_dept['nom']}", f"{pire_dept['taux_pour_100k']:.1f}")
col4.metric("✅ Moins touché", f"{meilleur_dept['nom']}", f"{meilleur_dept['taux_pour_100k']:.1f}")

st.markdown("---")

# --- 6. VISUALISATION (Carte + Graphique) ---
col_map, col_graph = st.columns([2, 1])

with col_map:
    st.subheader("🗺️ Cartographie")
    
    # Ta logique de carte (optimisée)
    geojson = gdf_filtered.__geo_interface__
    
    fig_map = px.choropleth(
        gdf_filtered,
        geojson=geojson,
        locations=gdf_filtered.index,
        color="taux_pour_100k",
        hover_name="nom",
        hover_data={"nombre": True, "population": True},
        color_continuous_scale="Reds",
        projection="mercator"
    )
    
    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    st.plotly_chart(fig_map, use_container_width=True)

with col_graph:
    st.subheader("📈 Évolution temporelle")
    
    # Agrégation par année pour voir la tendance nationale
    trend_data = df_history.groupby("annee")["nombre"].sum().reset_index()
    
    fig_line = px.line(
        trend_data, 
        x="annee", 
        y="nombre", 
        markers=True,
        color_discrete_sequence=["#FF4B4B"]
    )
    fig_line.update_layout(xaxis_title="Année", yaxis_title="Nombre de faits")
    st.plotly_chart(fig_line, use_container_width=True)

    st.subheader("📊 Top 5 Départements")
    top5 = gdf_filtered.nlargest(5, "taux_pour_100k").sort_values("taux_pour_100k", ascending=True)
    fig_bar = px.bar(top5, x="taux_pour_100k", y="nom", orientation='h', text="taux_pour_100k")
    fig_bar.update_traces(texttemplate='%{text:.1f}')
    st.plotly_chart(fig_bar, use_container_width=True)

# --- 7. SECTION INTELLIGENCE ARTIFICIELLE (Membre B) ---
st.markdown("---")
st.subheader("🤖 Assistant IA")

col_ia_left, col_ia_right = st.columns([1, 2])

with col_ia_left:
    st.write("Générer un rapport d'analyse automatique pour cette configuration.")
    if st.button("📝 Générer le rapport"):
        # Placeholder pour l'appel API (OpenAI / Mistral)
        st.success("Simulation : Le rapport a été généré (Logique à implémenter par Membre B).")
        
        # Exemple de prompt contextuel
        prompt_context = f"""
        Données : {delit} en {annee}.
        Total national : {total_faits}.
        Département critique : {pire_dept['nom']} ({pire_dept['taux_pour_100k']}).
        """
        st.code(prompt_context, language="text")

with col_ia_right:
    user_input = st.chat_input("Posez une question sur ces données...")
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        with st.chat_message("assistant"):
            st.write("Je suis l'assistant SafeCity. Je n'ai pas encore de cerveau connecté (API Key manquante), mais je vois que vous parlez de : " + delit)