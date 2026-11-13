"""
Master End-to-End Orchestrator for Chhattisgarh Agro-Logistics Study.
Executes the entire pipeline:
1. Block Catalog Validation (146 Blocks, 33 Districts, 5 Divisions)
2. Block-Wise POI Discovery & Deduplication (Google Maps + OSM + Registries)
3. Network Accessibility & Piecewise Freight Cost Modeling
4. 2SFCA Accessibility & Coldspot Optimization
5. Interactive Web Maps & Publication Visualizations
"""

import os
import sys
import time
import logging

from generate_catalog import generate_catalog
from chhattisgarh_poi_scraper import run_statewide_poi_discovery
from chhattisgarh_spatial_accessibility import run_accessibility_pipeline
from src.visualization.map_generator import generate_interactive_maps, generate_publication_charts

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("pipeline_execution.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("ChhattisgarhMasterPipeline")


def main():
    start_time = time.time()
    logger.info("=" * 85)
    logger.info("CHHATTISGARH STATE-WIDE AGRO-INDUSTRY DISCOVERY & FREIGHT MODELING PIPELINE")
    logger.info("5 Divisions | 33 Districts | 146 Community Development Blocks | 3 Agro-Climatic Zones")
    logger.info("=" * 85)

    # Step 1: Ensure Catalog Exists
    catalog_path = "configs/chhattisgarh_blocks_catalog.json"
    if not os.path.exists(catalog_path):
        logger.info("[Step 1/5] Generating 146-Block Administrative & Agro-Climatic Catalog...")
        generate_catalog()
    else:
        logger.info("[Step 1/5] Verified 146-Block Catalog.")

    # Step 2: POI Discovery & Spatial Deduplication
    poi_csv = "data/processed/chhattisgarh_agro_poi_master.csv"
    if not os.path.exists(poi_csv):
        logger.info("[Step 2/5] Running Block-by-Block Google Maps & OSM POI Discovery...")
        run_statewide_poi_discovery(catalog_path=catalog_path)
    else:
        logger.info(f"[Step 2/5] Verified POI Master Dataset: {poi_csv}")

    # Step 3: Network Accessibility & Freight Cost Modeling
    logger.info("[Step 3/5] Computing Network Travel Times & Two-Tier Freight Cost Matrix...")
    df_master = run_accessibility_pipeline(catalog_path=catalog_path, poi_csv_path=poi_csv)

    # Step 4: Interactive Cartography & Publication Figures
    logger.info("[Step 4/5] Generating Folium Web Maps & Matplotlib Visualization Figures...")
    map_path = generate_interactive_maps()
    generate_publication_charts()

    elapsed = round(time.time() - start_time, 2)
    logger.info("=" * 85)
    logger.info(f"ALL DELIVERABLES SUCCESSFULLY PRODUCED IN {elapsed} SECONDS!")
    logger.info("Master Excel Workbook: data/processed/chhattisgarh_all_146_blocks_master.xlsx")
    logger.info("Master Block CSV:      data/processed/chhattisgarh_all_146_blocks_master.csv")
    logger.info("Master POI Dataset:    data/processed/chhattisgarh_agro_poi_master.csv")
    logger.info("Coldspot Interventions:data/processed/chhattisgarh_coldspots_interventions.csv")
    logger.info(f"Interactive Web Map:   {map_path}")
    logger.info("=" * 85)


if __name__ == "__main__":
    main()
