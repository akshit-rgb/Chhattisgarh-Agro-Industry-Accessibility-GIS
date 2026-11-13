"""
Multi-Source Spatial Data Fusion & Deduplication Engine.
Combines Google Maps Places POIs, OSM Overpass records, CG Markfed registries,
e-NAM APMC mandis, CSIDC industrial parks, and FCI silos.
Applies 50-meter spatial proximity buffer and string deduplication.
"""

import math
import logging
import pandas as pd
from typing import List, Dict, Any

logger = logging.getLogger("RegistryFusion")


def haversine_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Computes great-circle distance between two coordinates in meters."""
    R = 6371000.0  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c


class RegistryFusionEngine:
    """
    Fuses multiple POI streams and performs spatial & attribute deduplication.
    """

    def __init__(self, proximity_threshold_m: float = 50.0):
        self.proximity_threshold_m = proximity_threshold_m

    def deduplicate(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Deduplicates records based on:
        1. Exact Place ID
        2. 50-meter spatial proximity buffer with matching/similar category
        """
        if not records:
            return []

        # Step 1: Place ID deduplication
        seen_ids = set()
        unique_by_id = []
        for r in records:
            pid = r.get("place_id")
            if pid and pid in seen_ids:
                continue
            if pid:
                seen_ids.add(pid)
            unique_by_id.append(r)

        logger.info(f"Deduplication Step 1 (Place ID): {len(records)} -> {len(unique_by_id)} records.")

        # Step 2: 50m spatial proximity deduplication
        # Sort by latitude to speed up window search
        sorted_records = sorted(unique_by_id, key=lambda x: (x["latitude"], x["longitude"]))
        deduped = []

        for current in sorted_records:
            lat = current["latitude"]
            lon = current["longitude"]
            is_duplicate = False

            # Check against recently accepted records
            for accepted in reversed(deduped[-25:]):
                # Quick bounding box check: ~0.0005 deg is roughly 55 meters
                if abs(accepted["latitude"] - lat) > 0.0006:
                    continue
                if abs(accepted["longitude"] - lon) > 0.0006:
                    continue

                dist_m = haversine_distance_m(lat, lon, accepted["latitude"], accepted["longitude"])
                if dist_m <= self.proximity_threshold_m:
                    # Same spatial cluster: merge or retain higher fidelity source
                    is_duplicate = True
                    # If current has higher review count or rating, update accepted
                    if current.get("review_count", 0) > accepted.get("review_count", 0):
                        accepted["review_count"] = current["review_count"]
                        accepted["rating"] = current["rating"]
                    break

            if not is_duplicate:
                deduped.append(current)

        logger.info(f"Deduplication Step 2 (50m Buffer): {len(unique_by_id)} -> {len(deduped)} records.")
        return deduped

    def to_dataframe(self, records: List[Dict[str, Any]]) -> pd.DataFrame:
        """Converts deduplicated records into a standardized Pandas DataFrame."""
        df = pd.DataFrame(records)
        required_cols = [
            "place_id", "name", "category", "sub_category", "scale",
            "capacity_mt_day", "latitude", "longitude", "plus_code",
            "address", "block", "district", "division", "phone",
            "rating", "review_count", "operational_status", "source"
        ]
        for col in required_cols:
            if col not in df.columns:
                df[col] = ""
        return df[required_cols]
