## 📋 Description
SafeCity est un tableau de bord interactif pour l'analyse de la criminalité urbaine en France.  
Il permet de visualiser les tendances par département, de comparer les territoires et de générer des rapports automatiques via IA.

## 🎯 Fonctionnalités
- Cartographie interactive des crimes par département (Plotly / Folium)  
- Graphiques d'évolution temporelle par type de délit  
- Comparateur territorial multi-départements  
- Analyse et synthèse automatique via LLaMA 3.3 (Groq)  
- Chatbot interactif pour répondre aux questions statistiques  
- Export de rapports PDF / Markdown  
- Tests unitaires pour valider la fiabilité des fonctions clés  
- Déploiement en ligne sur Streamlit

## 🛠️ Installation

```bash
# Cloner le repo
git clone [url]
cd safecity-dashboard

# Installer avec uv
uv sync

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API

🚀 Lancement local

uv run streamlit run app.py
# ou
uv run python app.py  # pour Gradio

🌐 Déploiement en ligne
Dashboard accessible : SafeCity Streamlit App
📊 Sources de données
Ministère de l’Intérieur
API Open Data : crimes et délits par année et département
IGN / OpenStreetMap
Fichiers SIG : contours géographiques
INSEE
CSV : population par département
✅ Tests
Tests unitaires inclus pour vérifier :
Extraction et nettoyage des données
Calcul des indicateurs statistiques
Filtrage et préparation des données pour le dashboard
👥 Équipe
Ikhlas Laghmich
Maria Menni

