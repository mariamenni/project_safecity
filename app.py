import streamlit as st
from utils.data import load_latest_parquet
# On importe ta logique IA
from logic_ai import get_ai_analysis 
# On suppose que ton fichier chart.py existe et fonctionne
from charts import map_choropleth, evolution_nationale, comparateur_territorial, top5_departements

# --- 1. CONFIGURATION ---
st.set_page_config(layout="wide", page_title="SafeCity Dashboard", page_icon="🛡️")

# --- 2. CHARGEMENT DES DONNÉES ---
@st.cache_data
def get_data():
    gdf = load_latest_parquet()
    if gdf.crs is None:
        gdf = gdf.set_crs(epsg=4326)
    return gdf

try:
    gdf = get_data()
except Exception as e:
    st.error(f"Erreur de chargement : {e}. Avez-vous lancé l'ETL ?")
    st.stop()

# --- 3. SIDEBAR (Filtres) ---
with st.sidebar:
    st.title("🛡️ SafeCity")
    st.markdown("---")
    annee = st.selectbox("📅 Année", sorted(gdf["annee"].unique(), reverse=True))
    delit = st.selectbox("⚖️ Type de délit", sorted(gdf["indicateur"].unique()))
    st.markdown("---")
    st.info("💡 Les filtres mettent à jour l'IA en temps réel.")

# --- 4. PRÉPARATION DES DONNÉES (FILTRAGE) ---
gdf_filtered = gdf[(gdf["annee"] == annee) & (gdf["indicateur"] == delit)].copy()
df_history = gdf[gdf["indicateur"] == delit].copy()

# --- 5. INDICATEURS CLÉS (KPI) ---
st.title(f"Analyse : {delit} ({annee})")

col1, col2, col3, col4 = st.columns(4)

# Calculs de base
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

# Ligne du bas : Comparateur + Top 5
c_bottom_1, c_bottom_2 = st.columns(2)
with c_bottom_1:
    st.subheader("🆚 Comparaison")
    deps = st.multiselect("Départements à comparer", sorted(gdf["nom"].unique()), default=["Paris", "Nord"])
    if deps:
        df_comp = gdf[(gdf["nom"].isin(deps)) & (gdf["indicateur"] == delit)].copy()
        st.plotly_chart(comparateur_territorial(df_comp), use_container_width=True)

with c_bottom_2:
    st.subheader("📊 Top 5 Départements")
    st.plotly_chart(top5_departements(gdf_filtered), use_container_width=True)

# --- 7. PRÉPARATION INTELLIGENTE DES DONNÉES (POUR L'IA) ---
# C'est ici qu'on calcule les "Tendances" pour valider le critère du prof
annee_prev = annee - 1
df_prev = gdf[(gdf["annee"] == annee_prev) & (gdf["indicateur"] == delit)]

evolution_str = "Donnée historique indisponible"
if not df_prev.empty:
    total_prev = df_prev["nombre"].sum()
    if total_prev > 0:
        pct = ((total_faits - total_prev) / total_prev) * 100
        signe = "+" if pct > 0 else ""
        evolution_str = f"{signe}{pct:.1f}% par rapport à {annee_prev}"

# On construit le contexte complet pour l'IA
contexte_ia = f"""
--- DONNÉES CLÉS ---
Année : {annee}
Type de délit : {delit}
Total faits France : {total_faits:,}
TENDANCE (vs N-1) : {evolution_str}

--- GÉOGRAPHIE ---
Département le plus critique : {pire_dept['nom']} (Taux: {pire_dept['taux_pour_100k']:.1f})
Moyenne nationale : {taux_moyen:.1f}
Département le plus sûr : {meilleur_dept['nom']}

--- COMPARAISON ---
Le département critique est {pire_dept['taux_pour_100k']/taux_moyen:.1f}x supérieur à la moyenne.
"""



# --- 8. SECTION INTELLIGENCE ARTIFICIELLE (Design "Cards") ---
st.markdown("---")
st.subheader("🤖 SafeCity AI Studio")

# 3 Onglets clairs pour séparer les usages
tab_analyse, tab_rapport, tab_chat = st.tabs([
    "🔍 Analyses Ciblées", 
    "📄 Rapport Complet", 
    "💬 Chatbot"
])

# --- ONGLET 1 : ANALYSES CIBLÉES (Tendances & Comparaison) ---
with tab_analyse:
    st.markdown("##### 🛠️ Outils d'aide à la décision")
    
    # BOITE 1 : TENDANCES
    with st.container(border=True):
        st.markdown("### 📈 Analyse des Tendances")
        st.write("Cet outil analyse l'évolution temporelle (N vs N-1) pour détecter les ruptures.")
        
        if st.button("Lancer l'analyse Temporelle", key="btn_tend"):
            with st.spinner("Analyse de l'historique..."):
                res = get_ai_analysis(contexte_ia, mode="tendance")
                st.markdown(f"**Résultat :**\n\n{res}")

    # BOITE 2 : COMPARAISON
    with st.container(border=True):
        st.markdown("### 🆚 Comparaison Contextuelle")
        st.write("Cet outil met en perspective les chiffres locaux face à la moyenne nationale.")
        
        if st.button("Lancer l'analyse Contextuelle", key="btn_comp"):
            with st.spinner("Calcul des ratios..."):
                res = get_ai_analysis(contexte_ia, mode="comparaison")
                st.markdown(f"**Résultat :**\n\n{res}")

# --- ONGLET 2 : RAPPORT COMPLET ---
with tab_rapport:
    st.markdown("##### 📑 Synthèse Globale")
    st.write("Génère un document complet reprenant tous les indicateurs.")
    
    if st.button("⚡ Générer le Rapport ", type="primary"):
        with st.spinner("Rédaction du rapport en cours..."):
            res = get_ai_analysis(contexte_ia, mode="rapport")
            st.session_state['full_report'] = res
            
    if 'full_report' in st.session_state:
        st.markdown("---")
        st.markdown(st.session_state['full_report'])
        st.download_button("📥 Télécharger (.md)", st.session_state['full_report'], "rapport.md")

# --- ONGLET 3 : CHATBOT ---
with tab_chat:
    st.markdown("##### 💬 Assistant Virtuel")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Posez votre question..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("..."):
                response = get_ai_analysis(contexte_ia, user_question=prompt, mode="chat")
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})