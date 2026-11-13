"""
OpenStreetMap (OSM) Overpass QL Query Engine for Chhattisgarh Agro-Infrastructure.
Extracts rice mills, agricultural workshops, rural mandis, and industrial estates.
"""

import json
import logging
import hashlib
from typing import List, Dict, Any, Optional

logger = logging.getLogger("OSMOverpass")

OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://z.overpass-api.de/api/interpreter"
]


class OSMOverpassClient:
    """Queries OpenStreetMap Overpass API for agro-industrial infrastructure."""

    def __init__(self, timeout_sec: int = 60):
        self.timeout_sec = timeout_sec

    def build_block_query(self, bbox: Dict[str, float]) -> str:
        """
        Builds Overpass QL query string for a bounding box.
        bbox: min_lat, min_lon, max_lat, max_lon
        """
        min_lat = bbox["min_lat"]
        min_lon = bbox["min_lon"]
        max_lat = bbox["max_lat"]
        max_lon = bbox["max_lon"]

        query = f"""
        [out:json][timeout:{self.timeout_sec}];
        (
          node["industrial"="rice_mill"]({min_lat},{min_lon},{max_lat},{max_lon});
          way["industrial"="rice_mill"]({min_lat},{min_lon},{max_lat},{max_lon});
          node["man_made"="works"]["food"]({min_lat},{min_lon},{max_lat},{max_lon});
          node["amenity"="marketplace"]({min_lat},{min_lon},{max_lat},{max_lon});
          node["shop"="agrarian"]({min_lat},{min_lon},{max_lat},{max_lon});
          node["landuse"="industrial"]["industrial"="agro"]({min_lat},{min_lon},{max_lat},{max_lon});
        );
        out body center;
        >;
        out skel qt;
        """
        return query

    def parse_osm_elements(self, osm_json: Dict[str, Any], block_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parses Overpass API JSON response into standardized POI format."""
        pois = []
        elements = osm_json.get("elements", [])
        block_name = block_info["block"]
        district_name = block_info["district"]
        division_name = block_info["division"]

        for el in elements:
            tags = el.get("tags", {})
            name = tags.get("name") or tags.get("name:en") or f"Agro Facility {el.get('id')}"

            lat = el.get("lat")
            lon = el.get("lon")
            if lat is None and "center" in el:
                lat = el["center"].get("lat")
                lon = el["center"].get("lon")

            if lat is None or lon is None:
                continue

            # Determine category
            category = "Agro-Processing"
            sub_category = tags.get("industrial", tags.get("food", "Agro Unit"))
            if tags.get("amenity") == "marketplace":
                category = "Regulated_Market"
                sub_category = "Rural Haat / Mandi Yard"
            elif tags.get("shop") == "agrarian":
                category = "Agro_Inputs"
                sub_category = "Krishi Kendra / Input Dealer"

            osm_id = f"OSM_{el.get('type')}_{el.get('id')}"
            pois.append({
                "place_id": osm_id,
                "name": name,
                "category": category,
                "sub_category": sub_category,
                "scale": "Micro/Small",
                "capacity_mt_day": 10.0,
                "latitude": round(lat, 5),
                "longitude": round(lon, 5),
                "plus_code": "",
                "address": tags.get("addr:full") or f"{block_name}, {district_name}, Chhattisgarh",
                "block": block_name,
                "district": district_name,
                "division": division_name,
                "phone": tags.get("phone", tags.get("contact:phone", "")),
                "rating": 4.0,
                "review_count": 5,
                "operational_status": "OPERATIONAL",
                "source": "OpenStreetMap_Overpass"
            })

        return pois
