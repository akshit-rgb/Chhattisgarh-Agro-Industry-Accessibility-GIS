"""
Terrain & Hydrological Friction Surface Model for Chhattisgarh.
Incorporates SRTM 30m slope impedance, river basin bottlenecks, and agro-climatic zone multipliers.
"""

import math
import logging

logger = logging.getLogger("SlopeFriction")


class TerrainFrictionModel:
    """
    Computes slope impedance multipliers and river basin delay penalties.
    """

    # Topographic & Agro-Climatic Gradient Multiplier (Beta_slope)
    ZONE_BETA_SLOPE = {
        1: 1.00,  # Zone 1 — Chhattisgarh Plains
        2: 1.20,  # Zone 2 — Undulating Foothills & Transition Blocks
        3: 1.40   # Zone 3 — Steep Northern Hills & Southern Bastar Plateau
    }

    # Mean slope percentages by Zone based on SRTM 30m DEM
    MEAN_SLOPE_PCT = {
        1: 1.5,   # Gentle plains
        2: 6.8,   # Undulating foothills
        3: 14.5   # Rugged hills / ghats
    }

    # Major river basins in Chhattisgarh with monsoon crossing delays
    RIVER_BASINS = [
        "Mahanadi", "Seonath", "Hasdeo", "Indravati",
        "Sabari", "Kharun", "Arpa", "Kanhar"
    ]

    @classmethod
    def get_beta_slope(cls, zone: int) -> float:
        """Returns the agro-climatic terrain gradient multiplier."""
        return cls.ZONE_BETA_SLOPE.get(zone, 1.00)

    @classmethod
    def get_mean_slope(cls, zone: int) -> float:
        """Returns the mean SRTM slope percentage for the zone."""
        return cls.MEAN_SLOPE_PCT.get(zone, 2.0)

    @classmethod
    def calculate_impedance_factor(cls, zone: int, river_crossing: bool = False) -> float:
        """
        Calculates combined terrain and hydrological impedance factor.
        """
        beta = cls.get_beta_slope(zone)
        river_penalty = 1.15 if river_crossing else 1.00
        return round(beta * river_penalty, 3)
