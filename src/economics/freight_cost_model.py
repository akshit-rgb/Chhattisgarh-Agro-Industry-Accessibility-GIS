"""
Regional Piecewise Agricultural Freight Transportation Cost Model for Chhattisgarh.
Implements Two-Tier Piecewise Equations:
Tier 1: Farm Gate to Mandi/PACS via Tractor-Trolley (3-5 MT)
Tier 2: Mandi/PACS to Parboiling Mill/Silo via Multi-Axle Truck (14-16 MT)
"""

import logging
from typing import Dict, Any

logger = logging.getLogger("FreightCostModel")


class RegionalFreightCostModel:
    """
    Computes farm-to-market and market-to-mill transportation costs (INR/Quintal and INR/MT-km).
    """

    # Tier 1 Parameters (Tractor-Trolley / LCV Pickup)
    R_TRACTOR_MT_KM = 20.0       # INR / MT-km
    R_TRACTOR_QTL_KM = 2.00      # INR / Quintal-km (1 MT = 10 Qtl)
    C_HANDLING_FARM_MANDI = 12.0 # INR / Quintal

    # Tier 2 Parameters (14-16 MT Multi-Axle Truck)
    R_TRUCK_MT_KM = 8.5          # INR / MT-km
    R_TRUCK_QTL_KM = 0.85        # INR / Quintal-km
    C_HANDLING_MANDI_MILL = 8.0  # INR / Quintal (Hamali / Stacking)

    # Road Surface Multipliers (Alpha_road)
    ALPHA_ROAD = {
        "nh_sh_paved": 1.00,
        "rural_tertiary_paved": 1.25,
        "unpaved_track": 1.60
    }

    # Topographic Gradient Multipliers (Beta_slope)
    BETA_SLOPE = {
        1: 1.00,  # Zone 1 — Chhattisgarh Plains
        2: 1.20,  # Zone 2 — Undulating Foothills & Transition Blocks
        3: 1.40   # Zone 3 — Steep Northern Hills & Southern Bastar Plateau
    }

    @classmethod
    def compute_farm_to_mandi_cost(cls, dist_km: float, zone: int = 1,
                                   unpaved_ratio: float = 0.25,
                                   rural_paved_ratio: float = 0.45,
                                   highway_ratio: float = 0.30) -> Dict[str, float]:
        """
        Computes Tier 1 Farm-to-Mandi freight cost (INR/Quintal).
        Formula: C_farm = C_handling + dist * R_tractor * Alpha_road * Beta_slope
        """
        beta = cls.BETA_SLOPE.get(zone, 1.00)
        # Weighted road roughness multiplier
        alpha_eff = (unpaved_ratio * cls.ALPHA_ROAD["unpaved_track"] +
                     rural_paved_ratio * cls.ALPHA_ROAD["rural_tertiary_paved"] +
                     highway_ratio * cls.ALPHA_ROAD["nh_sh_paved"])

        variable_freight_qtl = dist_km * cls.R_TRACTOR_QTL_KM * alpha_eff * beta
        total_cost_qtl = cls.C_HANDLING_FARM_MANDI + variable_freight_qtl
        rate_mt_km = (variable_freight_qtl * 10.0) / max(dist_km, 0.1)

        return {
            "farm_to_mandi_cost_inr_qtl": round(total_cost_qtl, 2),
            "farm_to_mandi_variable_qtl": round(variable_freight_qtl, 2),
            "farm_to_mandi_handling_qtl": cls.C_HANDLING_FARM_MANDI,
            "effective_rate_tractor_inr_mt_km": round(rate_mt_km, 2),
            "alpha_road": round(alpha_eff, 3),
            "beta_slope": beta
        }

    @classmethod
    def compute_mandi_to_mill_cost(cls, dist_km: float, zone: int = 1,
                                   rural_paved_ratio: float = 0.15,
                                   highway_ratio: float = 0.85) -> Dict[str, float]:
        """
        Computes Tier 2 Mandi-to-Mill freight cost (INR/Quintal).
        Formula: C_mill = C_handling + dist * R_truck * Alpha_road * Beta_slope
        """
        beta = cls.BETA_SLOPE.get(zone, 1.00)
        alpha_eff = (rural_paved_ratio * cls.ALPHA_ROAD["rural_tertiary_paved"] +
                     highway_ratio * cls.ALPHA_ROAD["nh_sh_paved"])

        variable_freight_qtl = dist_km * cls.R_TRUCK_QTL_KM * alpha_eff * beta
        total_cost_qtl = cls.C_HANDLING_MANDI_MILL + variable_freight_qtl
        rate_mt_km = (variable_freight_qtl * 10.0) / max(dist_km, 0.1)

        return {
            "mandi_to_mill_cost_inr_qtl": round(total_cost_qtl, 2),
            "mandi_to_mill_variable_qtl": round(variable_freight_qtl, 2),
            "mandi_to_mill_handling_qtl": cls.C_HANDLING_MANDI_MILL,
            "effective_rate_truck_inr_mt_km": round(rate_mt_km, 2),
            "alpha_road": round(alpha_eff, 3),
            "beta_slope": beta
        }

    @classmethod
    def compute_total_logistics_cost(cls, farm_dist_km: float, mill_dist_km: float, zone: int = 1) -> Dict[str, float]:
        """
        Computes combined block logistics freight cost (INR/Quintal).
        """
        tier1 = cls.compute_farm_to_mandi_cost(farm_dist_km, zone=zone)
        tier2 = cls.compute_mandi_to_mill_cost(mill_dist_km, zone=zone)
        total_cost_qtl = tier1["farm_to_mandi_cost_inr_qtl"] + tier2["mandi_to_mill_cost_inr_qtl"]

        return {
            "farm_to_mandi_cost_inr_qtl": tier1["farm_to_mandi_cost_inr_qtl"],
            "mandi_to_mill_cost_inr_qtl": tier2["mandi_to_mill_cost_inr_qtl"],
            "total_logistics_cost_inr_qtl": round(total_cost_qtl, 2),
            "farm_to_mandi_rate_inr_mt_km": tier1["effective_rate_tractor_inr_mt_km"],
            "mandi_to_mill_rate_inr_mt_km": tier2["effective_rate_truck_inr_mt_km"],
        }
