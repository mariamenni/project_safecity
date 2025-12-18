from pipeline.fetch_crimes import fetch_crimes
from pipeline.fetch_population import fetch_population
from pipeline.fetch_geo import fetch_geo
from pipeline.transform import transform_crimes
from pipeline.enrich import enrich_data
from pipeline.store import store_parquet

def run():
    print("📥 Chargement crimes")
    crimes = fetch_crimes()

    print("📥 Chargement population")
    population = fetch_population()

    print("📥 Chargement géométrie")
    geo = fetch_geo()

    print("🔧 Transformation")
    crimes = transform_crimes(crimes)

    print("🔗 Enrichissement")
    gdf = enrich_data(crimes, population, geo)

    print("💾 Stockage")
    store_parquet(gdf)

    print("✅ PIPELINE SAFECITY TERMINÉ")

if __name__ == "__main__":
    run()
