"""
Two-Step Floating Catchment Area (2SFCA) Spatial Accessibility Scoring.
Models agricultural supply (block marketable surplus) vs processing capacity (mills/silos).
Calculates localized processing accessibility score for every block in Chhattisgarh.
"""

import math
import logging
import numpy as np
from typing import List, Dict, Any

logger = logging.getLogger("Accessibility2SFCA")


class TwoStepFloatingCatchmentArea:
    """
    Implements 2SFCA algorithm with continuous Gaussian impedance decay function.
    """

    def __init__(self, catchment_time_min: float = 60.0):
        self.t0 = catchment_time_min

    def gaussian_decay(self, travel_time_min: float) -> float:
        """
        Continuous Gaussian decay function f(T) bounded between 1.0 (at T=0) and 0.0 (at T=T0).
        """
        if travel_time_min > self.t0:
            return 0.0
        numerator = math.exp(-0.5 * (travel_time_min / self.t0) ** 2) - math.exp(-0.5)
        denominator = 1.0 - math.exp(-0.5)
        return max(0.0, numerator / denominator)

    def compute_2sfca_scores(self, blocks: List[Dict[str, Any]], pois: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Computes 2SFCA accessibility score for all blocks.
        """
        # Filter agro-processing destination units
        processing_units = [
            p for p in pois
            if p["category"] == "Agro-Processing" and p.get("capacity_mt_day", 0) > 0
        ]

        if not processing_units:
            logger.warning("No processing units found for 2SFCA. Returning zero scores.")
            return {b["block"]: 0.0 for b in blocks}

        # Step 1: Compute Provider-to-Demand ratio R_j for each facility j
        facility_ratios = []
        for fac in processing_units:
            cap_sj = fac.get("capacity_mt_day", 10.0)
            fac_lat = fac["latitude"]
            fac_lon = fac["longitude"]

            weighted_demand = 0.0
            for b in blocks:
                b_lat = b["lat"]
                b_lon = b["lon"]
                # Approximate network travel time
                dist_km = math.sqrt((fac_lat - b_lat)**2 + (fac_lon - b_lon)**2) * 111.0 * 1.35
                travel_time_min = (dist_km / 35.0) * 60.0

                weight = self.gaussian_decay(travel_time_min)
                if weight > 0:
                    demand_pk = b.get("marketable_surplus_qtl", 500000) / 1000.0  # In thousands of quintals
                    weighted_demand += demand_pk * weight

            rj = cap_sj / max(weighted_demand, 1.0)
            facility_ratios.append({"facility": fac, "R_j": rj, "lat": fac_lat, "lon": fac_lon})

        # Step 2: For each block i, sum R_j * f(T_ij)
        raw_scores = {}
        for b in blocks:
            b_name = b["block"]
            b_lat = b["lat"]
            b_lon = b["lon"]

            ai = 0.0
            for fac_r in facility_ratios:
                dist_km = math.sqrt((fac_r["lat"] - b_lat)**2 + (fac_r["lon"] - b_lon)**2) * 111.0 * 1.35
                travel_time_min = (dist_km / 35.0) * 60.0

                weight = self.gaussian_decay(travel_time_min)
                if weight > 0:
                    ai += fac_r["R_j"] * weight

            raw_scores[b_name] = ai

        # Normalize scores to 0 - 100 scale
        max_val = max(raw_scores.values()) if raw_scores.values() else 1.0
        normalized_scores = {
            b_name: round((val / max(max_val, 0.001)) * 100.0, 2)
            for b_name, val in raw_scores.items()
        }

        return normalized_scores
