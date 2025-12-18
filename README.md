

```markdown
# 🛡️ SafeCity - Dashboard de Criminalité Urbaine

**SafeCity** est un tableau de bord interactif conçu pour l'analyse de la criminalité urbaine en France. Il permet de visualiser les tendances par département, de comparer les territoires et de générer des analyses automatiques grâce à l'intelligence artificielle.

---

## 📋 Description
L'objectif de SafeCity est de rendre les données de sécurité publique accessibles et compréhensibles. À l'aide de visualisations dynamiques et d'un agent IA intégré, l'utilisateur peut explorer l'évolution des délits et obtenir des synthèses précises par zone géographique.

## 🎯 Fonctionnalités
- **🌍 Cartographie interactive** : Visualisation des crimes par département (via Plotly & Folium).
- **📈 Évolution temporelle** : Graphiques détaillés par type de délit sur plusieurs années.
- **⚖️ Comparateur territorial** : Analyse comparative entre plusieurs départements.
- **🤖 Analyse IA (LLaMA 3.3)** : Synthèse automatique des tendances via l'API Groq.
- **💬 Chatbot interactif** : Posez des questions directement sur les statistiques criminelles.
- **📄 Export de rapports** : Génération de synthèses au format PDF ou Markdown.
- **🧪 Fiabilité garantie** : Tests unitaires pour valider le traitement des données.
- **🚀 Cloud Ready** : Déploiement optimisé pour Streamlit Cloud.

## 🛠️ Stack Technique
- **Frontend** : Streamlit
- **Analyse de données** : Pandas, NumPy
- **Visualisation** : Plotly, Folium
- **IA/LLM** : LLaMA 3.3 (via Groq API)
- **Gestion de projet** : UV (gestionnaire de packages ultra-rapide)

## ⚙️ Installation

### 1. Cloner le projet
```bash
git clone [URL_DU_REPO]
cd safecity-dashboard
```

### 2. Installer les dépendances
Nous utilisons `uv` pour une gestion efficace de l'environnement :
```bash
uv sync
```

### 3. Configurer les variables d'environnement
Créez un fichier `.env` à la racine du projet et ajoutez vos clés API (notamment pour Groq) :
```bash
cp .env.example .env
# Éditez .env avec vos accès
```

## 🚀 Lancement

**Pour lancer le dashboard Streamlit :**
```bash
uv run streamlit run app.py
```

**Pour lancer la version Gradio (si configurée) :**
```bash
uv run python app.py
```

## 🌐 Déploiement
Le dashboard est accessible en ligne ici : [[Lien vers SafeCity Streamlit App]](https://projectsafecity-fwff9penvyvxsded7xqcbx.streamlit.app/)(#) 

## 📊 Sources de données
Les données proviennent de sources officielles et ouvertes :
- **Ministère de l’Intérieur** : API Open Data pour les crimes et délits.
- **IGN / OpenStreetMap** : Fichiers SIG pour les contours géographiques des départements.
- **INSEE** : Données de population pour le calcul des taux de criminalité pour 1000 habitants.

## ✅ Tests
Le projet inclut une suite de tests unitaires pour assurer la qualité du code :
- Extraction et nettoyage automatique des données.
- Calcul des indicateurs statistiques.
- Filtrage et préparation des données pour les graphiques.

Pour lancer les tests :
```bash
uv run pytest
```

## 👥 Équipe
- **Ikhlas Laghmich**
- **Maria Menni**

---
