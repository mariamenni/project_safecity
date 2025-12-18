import sys
import os
import pandas as pd
import geopandas as gpd
from unittest.mock import patch, MagicMock

# Ajustement du chemin pour trouver le dossier pipeline
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ⚠️ Remplace 'pipeline.fetch_crimes' par le vrai nom de ton fichier/dossier
# Si tes fichiers sont dans un dossier "pipeline", garde ça. 
# Sinon adapte l'import.
from pipeline.fetch_crimes import fetch_crimes
from pipeline.fetch_population import fetch_population
from pipeline.fetch_geo import fetch_geo

# --- TEST 1 : FETCH CRIMES (CSV) ---
@patch("pipeline.fetch_crimes.pd.read_csv")
def test_fetch_crimes(mock_read_csv):
    # 1. On prépare une fausse donnée brute (comme si elle venait du CSV)
    mock_df = pd.DataFrame({
        "Code_departement": [1, 75], # Int qui doit devenir str "01"
        "annee": ["2022", "2022"],
        "nombre": [10, None], # None doit devenir 0
        "taux_pour_mille": ["5,5", "10"] # Virgule à remplacer
    })
    mock_read_csv.return_value = mock_df

    # 2. On lance la fonction
    df_result = fetch_crimes()

    # 3. Vérifications
    assert df_result["Code_departement"].iloc[0] == "01"  # Vérifie le padding (01)
    assert df_result["taux_pour_mille"].iloc[0] == 5.5    # Vérifie la virgule
    assert isinstance(df_result["taux_pour_mille"].iloc[0], float)
    assert df_result["nombre"].iloc[1] == 0               # Vérifie le fillna(0)

# --- TEST 2 : FETCH POPULATION (API) ---
@patch("pipeline.fetch_population.requests.get")
def test_fetch_population(mock_get):
    # 1. On simule la réponse de l'API (JSON)
    # Disons qu'on a 2 communes dans le département 01
    mock_json = [
        {"codeDepartement": "1", "population": 100},
        {"codeDepartement": "01", "population": 200},
        {"codeDepartement": "02", "population": 500}
    ]
    mock_response = MagicMock()
    mock_response.json.return_value = mock_json
    mock_get.return_value = mock_response

    # 2. On lance la fonction
    df_result = fetch_population()

    # 3. Vérifications
    # Le dept 01 doit avoir la somme (100 + 200 = 300)
    pop_01 = df_result[df_result["codeDepartement"] == "01"]["population"].values[0]
    assert pop_01 == 300
    assert df_result["codeDepartement"].iloc[0] == "01" # Vérifie le padding

# --- TEST 3 : FETCH GEO (GEOJSON) ---
@patch("pipeline.fetch_geo.gpd.read_file")
def test_fetch_geo(mock_read_file):
    # 1. On simule le GeoDataFrame
    mock_gdf = gpd.GeoDataFrame({
        "code": ["1", "2A"],
        "geometry": [None, None]
    })
    mock_read_file.return_value = mock_gdf

    # 2. On lance
    gdf_result = fetch_geo()

    # 3. Vérif
    assert gdf_result["code"].iloc[0] == "01" # Vérifie le padding "1" -> "01"
    assert gdf_result["code"].iloc[1] == "2A" # Vérifie que la Corse reste "2A"