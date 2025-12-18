import sys
import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipeline.transform import transform_crimes
from pipeline.enrich import enrich_data

# --- TEST 1 : TRANSFORMATION (FILTRES) ---
def test_transform_crimes():
    # Données sales
    df_input = pd.DataFrame({
        "Code_departement": ["01", "971", "75"], # 971 = DOM (Guadeloupe)
        "nombre": [10, 5, -5],                   # -5 = Aberrant
        "annee": [2022, 2022, 1990]              # 1990 = Hors scope
    })

    # Action
    df_out = transform_crimes(df_input)

    # Vérifications
    codes_restants = df_out["Code_departement"].tolist()
    assert "971" not in codes_restants  # DOM supprimé
    assert "01" in codes_restants       # Métropole gardée
    
    assert len(df_out) == 1 # Seul le code 01 est valide (car 75 a une annee 1990 et nombre -5) ou ajuster selon ta logique exacte
    # Note: Ta logique transform_crimes supprime < 0. Donc le -5 saute.
    # Ta logique supprime annee < 2010. Donc 1990 saute.
    # Il ne reste que la ligne 1.
    
    assert "periode" in df_out.columns # Vérifie que la colonne période est créée

# --- TEST 2 : ENRICHISSEMENT (CALCULS) ---
def test_enrich_data():
    # 1. Mock Dataframes
    # Crimes sur 2 ans pour vérifier l'évolution
    df_crimes = pd.DataFrame({
        "Code_departement": ["01", "01"],
        "indicateur": ["Vols", "Vols"],
        "annee": [2020, 2021],
        "nombre": [100, 120] # Augmentation de 20%
    })
    
    # Population fixe
    df_pop = pd.DataFrame({
        "codeDepartement": ["01"],
        "population": [100000]
    })
    
    # Geo
    df_geo = gpd.GeoDataFrame({
        "code": ["01"],
        "geometry": [Point(0,0)]
    })

    # 2. Action
    gdf_out = enrich_data(df_crimes, df_pop, df_geo)

    # 3. Vérifications
    
    # Vérif Taux pour 100k
    # 2020 : (100 / 100 000) * 100 000 = 100
    row_2020 = gdf_out[gdf_out["annee"] == 2020].iloc[0]
    assert row_2020["taux_pour_100k"] == 100.0

    # Vérif Évolution %
    # 2021 : (120 - 100) / 100 = +20%
    row_2021 = gdf_out[gdf_out["annee"] == 2021].iloc[0]
    # On utilise pytest.approx pour les flottants
    assert row_2021["evolution_%"] == pytest.approx(20.0)
    
    # Vérif Merge Géo
    assert isinstance(gdf_out, gpd.GeoDataFrame)
    assert gdf_out.geometry.name == "geometry"