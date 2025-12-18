from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

CRIMES_URL = (
    "https://static.data.gouv.fr/resources/"
    "bases-statistiques-communale-departementale-et-regionale-"
    "de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/"
    "20250710-144639/"
    "donnee-dep-data.gouv-2024-geographie2025-produit-le2025-06-04.csv"
)

GEO_URL = "https://github.com/gregoiredavid/france-geojson/raw/master/departements.geojson"

COMMUNES_URL = "https://geo.api.gouv.fr/communes?fields=code,nom,population,codeDepartement,codeRegion"
