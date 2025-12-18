# app.py
import streamlit as st
from utils.data import load_latest_parquet
from chart import map_choropleth, evolution_nationale, comparateur_territorial, top5_departements

# --- 1. CONFIGURATION ---
st.set_page_config(layout="wide", page_title="SafeCity Dashboard", page_icon="🛡️")

# --- 2. CHARGEMENT DES DONNÉES ---
@st.cache_data
def get_data():
    gdf = load_latest_parquet()
    if gdf.crs is None:
        gdf = gdf.set_crs(epsg=4326)
    return gdf

gdf = get_data()

# --- 3. SIDEBAR (Filtres) ---
with st.sidebar:
    st.title("🛡️ SafeCity")
    st.markdown("---")
    annee = st.selectbox("📅 Année", sorted(gdf["annee"].unique(), reverse=True))
    delit = st.selectbox("⚖️ Type de délit", sorted(gdf["indicateur"].unique()))
    st.markdown("---")
    st.info("💡 Utilisez les filtres pour mettre à jour la carte et l'analyse IA.")

# --- 4. PRÉPARATION DES DONNÉES ---
gdf_filtered = gdf[(gdf["annee"] == annee) & (gdf["indicateur"] == delit)].copy()
df_history = gdf[gdf["indicateur"] == delit].copy()

# --- 5. INDICATEURS CLÉS ---
st.title(f"Analyse : {delit} ({annee})")

col1, col2, col3, col4 = st.columns(4)
total_faits = gdf_filtered["nombre"].sum()
taux_moyen = gdf_filtered["taux_pour_100k"].mean()
pire_dept = gdf_filtered.loc[gdf_filtered["taux_pour_100k"].idxmax()]
meilleur_dept = gdf_filtered.loc[gdf_filtered["taux_pour_100k"].idxmin()]

col1.metric("Total Faits", f"{total_faits:,}".replace(",", " "))
col2.metric("Taux Moy. / 100k", f"{taux_moyen:.1f}")
col3.metric("⚠️ Plus touché", f"{pire_dept['nom']}", f"{pire_dept['taux_pour_100k']:.1f}")
col4.metric("✅ Moins touché", f"{meilleur_dept['nom']}", f"{meilleur_dept['taux_pour_100k']:.1f}")

st.markdown("---")

# --- 6. VISUALISATION ---
col_map, col_graph = st.columns([2, 1])

with col_map:
    st.subheader("🗺️ Cartographie")
    st.plotly_chart(map_choropleth(gdf_filtered), use_container_width=True)

with col_graph:
    st.subheader("📈 Évolution temporelle")
    st.plotly_chart(evolution_nationale(df_history, delit), use_container_width=True)

# Comparateur territorial
st.subheader("🆚 Comparaison territoriale")
deps = st.multiselect(
    "Sélectionner des départements à comparer",
    sorted(gdf["nom"].unique()),
    default=["Paris", "Rhône"]
)
df_comp = gdf[(gdf["nom"].isin(deps)) & (gdf["indicateur"] == delit)].copy()
st.plotly_chart(comparateur_territorial(df_comp), use_container_width=True)

# Top 5 départements
st.subheader("📊 Top 5 Départements")
st.plotly_chart(top5_departements(gdf_filtered), use_container_width=True)

# --- 7. SECTION INTELLIGENCE ARTIFICIELLE (Placeholder) ---
st.markdown("---")
st.subheader("🤖 Assistant IA")

col_ia_left, col_ia_right = st.columns([1, 2])
with col_ia_left:
    st.write("Générer un rapport d'analyse automatique pour cette configuration.")
    if st.button("📝 Générer le rapport"):
        st.success("Simulation : Le rapport a été généré (API non connectée).")
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
            st.write("Je suis l'assistant SafeCity. API non connectée, mais je comprends que vous parlez de : " + delit)
