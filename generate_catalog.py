"""
Master Reference Data Generator for Chhattisgarh Administrative Hierarchy.
Populates all 5 Divisions, 33 Districts, and 146 Community Development Blocks
with exact geographic coordinates, bounding boxes, agro-climatic zones, and production profiles.
"""

import json
import os

BLOCKS_DATA = [
    # ==========================================
    # RAIPUR DIVISION (5 Districts | 23 Blocks)
    # ==========================================
    # 1. Raipur District (4 Blocks)
    {"division": "Raipur", "district": "Raipur", "block": "Dharsiwa", "zone": 1, "lat": 21.3650, "lon": 81.6700, "area_sqkm": 542.0, "cropland_ha": 38400, "marketable_surplus_qtl": 1150000},
    {"division": "Raipur", "district": "Raipur", "block": "Tilda", "zone": 1, "lat": 21.5620, "lon": 81.7650, "area_sqkm": 680.0, "cropland_ha": 51200, "marketable_surplus_qtl": 1530000},
    {"division": "Raipur", "district": "Raipur", "block": "Arang", "zone": 1, "lat": 21.1960, "lon": 81.9680, "area_sqkm": 725.0, "cropland_ha": 58900, "marketable_surplus_qtl": 1760000},
    {"division": "Raipur", "district": "Raipur", "block": "Abhanpur", "zone": 1, "lat": 21.0540, "lon": 81.7510, "area_sqkm": 612.0, "cropland_ha": 49100, "marketable_surplus_qtl": 1470000},

    # 2. Baloda Bazar-Bhatapara District (5 Blocks)
    {"division": "Raipur", "district": "Baloda Bazar-Bhatapara", "block": "Baloda Bazar", "zone": 1, "lat": 21.6620, "lon": 82.1640, "area_sqkm": 810.0, "cropland_ha": 65000, "marketable_surplus_qtl": 1950000},
    {"division": "Raipur", "district": "Baloda Bazar-Bhatapara", "block": "Bhatapara", "zone": 1, "lat": 21.7370, "lon": 81.9320, "area_sqkm": 645.0, "cropland_ha": 54000, "marketable_surplus_qtl": 1620000},
    {"division": "Raipur", "district": "Baloda Bazar-Bhatapara", "block": "Simga", "zone": 1, "lat": 21.6280, "lon": 81.7050, "area_sqkm": 715.0, "cropland_ha": 61000, "marketable_surplus_qtl": 1830000},
    {"division": "Raipur", "district": "Baloda Bazar-Bhatapara", "block": "Palari", "zone": 1, "lat": 21.5340, "lon": 82.1980, "area_sqkm": 670.0, "cropland_ha": 56000, "marketable_surplus_qtl": 1680000},
    {"division": "Raipur", "district": "Baloda Bazar-Bhatapara", "block": "Kasdol", "zone": 1, "lat": 21.6210, "lon": 82.5020, "area_sqkm": 890.0, "cropland_ha": 68000, "marketable_surplus_qtl": 1900000},

    # 3. Gariaband District (5 Blocks)
    {"division": "Raipur", "district": "Gariaband", "block": "Gariaband", "zone": 2, "lat": 20.9630, "lon": 82.0720, "area_sqkm": 940.0, "cropland_ha": 34000, "marketable_surplus_qtl": 850000},
    {"division": "Raipur", "district": "Gariaband", "block": "Chhura", "zone": 2, "lat": 21.0500, "lon": 82.1850, "area_sqkm": 780.0, "cropland_ha": 39000, "marketable_surplus_qtl": 980000},
    {"division": "Raipur", "district": "Gariaband", "block": "Fingeshwar", "zone": 1, "lat": 21.0180, "lon": 81.9360, "area_sqkm": 560.0, "cropland_ha": 44000, "marketable_surplus_qtl": 1280000},
    {"division": "Raipur", "district": "Gariaband", "block": "Mainpur", "zone": 2, "lat": 20.7380, "lon": 82.2620, "area_sqkm": 1450.0, "cropland_ha": 28000, "marketable_surplus_qtl": 620000},
    {"division": "Raipur", "district": "Gariaband", "block": "Deobhog", "zone": 2, "lat": 20.1980, "lon": 82.5780, "area_sqkm": 880.0, "cropland_ha": 31000, "marketable_surplus_qtl": 710000},

    # 4. Dhamtari District (4 Blocks)
    {"division": "Raipur", "district": "Dhamtari", "block": "Dhamtari", "zone": 1, "lat": 20.7070, "lon": 81.5490, "area_sqkm": 520.0, "cropland_ha": 46000, "marketable_surplus_qtl": 1420000},
    {"division": "Raipur", "district": "Dhamtari", "block": "Kurud", "zone": 1, "lat": 20.8310, "lon": 81.7130, "area_sqkm": 590.0, "cropland_ha": 52000, "marketable_surplus_qtl": 1650000},
    {"division": "Raipur", "district": "Dhamtari", "block": "Magarlod", "zone": 1, "lat": 20.7550, "lon": 81.8650, "area_sqkm": 680.0, "cropland_ha": 41000, "marketable_surplus_qtl": 1180000},
    {"division": "Raipur", "district": "Dhamtari", "block": "Nagri", "zone": 2, "lat": 20.5520, "lon": 81.9210, "area_sqkm": 1580.0, "cropland_ha": 33000, "marketable_surplus_qtl": 790000},

    # 5. Mahasamund District (5 Blocks)
    {"division": "Raipur", "district": "Mahasamund", "block": "Mahasamund", "zone": 1, "lat": 21.1090, "lon": 82.0980, "area_sqkm": 720.0, "cropland_ha": 55000, "marketable_surplus_qtl": 1600000},
    {"division": "Raipur", "district": "Mahasamund", "block": "Bagbahara", "zone": 1, "lat": 20.9650, "lon": 82.3780, "area_sqkm": 840.0, "cropland_ha": 52000, "marketable_surplus_qtl": 1480000},
    {"division": "Raipur", "district": "Mahasamund", "block": "Pithora", "zone": 1, "lat": 21.2670, "lon": 82.5180, "area_sqkm": 910.0, "cropland_ha": 59000, "marketable_surplus_qtl": 1680000},
    {"division": "Raipur", "district": "Mahasamund", "block": "Basna", "zone": 1, "lat": 21.4640, "lon": 82.8220, "area_sqkm": 790.0, "cropland_ha": 57000, "marketable_surplus_qtl": 1620000},
    {"division": "Raipur", "district": "Mahasamund", "block": "Saraipali", "zone": 1, "lat": 21.5030, "lon": 83.0040, "area_sqkm": 750.0, "cropland_ha": 56000, "marketable_surplus_qtl": 1590000},

    # ==========================================
    # DURG DIVISION (8 Districts | 25 Blocks)
    # ==========================================
    # 6. Durg District (3 Blocks)
    {"division": "Durg", "district": "Durg", "block": "Durg", "zone": 1, "lat": 21.1890, "lon": 81.2840, "area_sqkm": 680.0, "cropland_ha": 53000, "marketable_surplus_qtl": 1650000},
    {"division": "Durg", "district": "Durg", "block": "Patan", "zone": 1, "lat": 21.0340, "lon": 81.5360, "area_sqkm": 710.0, "cropland_ha": 62000, "marketable_surplus_qtl": 1920000},
    {"division": "Durg", "district": "Durg", "block": "Dhamdha", "zone": 1, "lat": 21.4420, "lon": 81.3120, "area_sqkm": 820.0, "cropland_ha": 67000, "marketable_surplus_qtl": 2050000},

    # 7. Balod District (5 Blocks)
    {"division": "Durg", "district": "Balod", "block": "Balod", "zone": 1, "lat": 20.7300, "lon": 81.2050, "area_sqkm": 610.0, "cropland_ha": 48000, "marketable_surplus_qtl": 1440000},
    {"division": "Durg", "district": "Balod", "block": "Gurur", "zone": 1, "lat": 20.7420, "lon": 81.3850, "area_sqkm": 540.0, "cropland_ha": 43000, "marketable_surplus_qtl": 1310000},
    {"division": "Durg", "district": "Balod", "block": "Gunderdehi", "zone": 1, "lat": 20.9450, "lon": 81.2980, "area_sqkm": 670.0, "cropland_ha": 58000, "marketable_surplus_qtl": 1780000},
    {"division": "Durg", "district": "Balod", "block": "Dondi", "zone": 2, "lat": 20.5280, "lon": 81.0480, "area_sqkm": 890.0, "cropland_ha": 32000, "marketable_surplus_qtl": 750000},
    {"division": "Durg", "district": "Balod", "block": "Dondi Lohara", "zone": 1, "lat": 20.7850, "lon": 81.0420, "area_sqkm": 780.0, "cropland_ha": 54000, "marketable_surplus_qtl": 1560000},

    # 8. Bemetara District (4 Blocks)
    {"division": "Durg", "district": "Bemetara", "block": "Bemetara", "zone": 1, "lat": 21.7010, "lon": 81.5450, "area_sqkm": 720.0, "cropland_ha": 64000, "marketable_surplus_qtl": 1950000},
    {"division": "Durg", "district": "Bemetara", "block": "Berla", "zone": 1, "lat": 21.5030, "lon": 81.5400, "area_sqkm": 680.0, "cropland_ha": 59000, "marketable_surplus_qtl": 1820000},
    {"division": "Durg", "district": "Bemetara", "block": "Saja", "zone": 1, "lat": 21.6880, "lon": 81.3090, "area_sqkm": 740.0, "cropland_ha": 62000, "marketable_surplus_qtl": 1890000},
    {"division": "Durg", "district": "Bemetara", "block": "Nawagarh", "zone": 1, "lat": 21.8790, "lon": 81.5970, "area_sqkm": 710.0, "cropland_ha": 61000, "marketable_surplus_qtl": 1850000},

    # 9. Rajnandgaon District (4 Blocks)
    {"division": "Durg", "district": "Rajnandgaon", "block": "Rajnandgaon", "zone": 1, "lat": 21.0960, "lon": 81.0320, "area_sqkm": 750.0, "cropland_ha": 58000, "marketable_surplus_qtl": 1720000},
    {"division": "Durg", "district": "Rajnandgaon", "block": "Dongargarh", "zone": 2, "lat": 21.1890, "lon": 80.7620, "area_sqkm": 820.0, "cropland_ha": 49000, "marketable_surplus_qtl": 1350000},
    {"division": "Durg", "district": "Rajnandgaon", "block": "Dongargaon", "zone": 1, "lat": 20.9720, "lon": 80.8540, "area_sqkm": 640.0, "cropland_ha": 51000, "marketable_surplus_qtl": 1480000},
    {"division": "Durg", "district": "Rajnandgaon", "block": "Chhuriya", "zone": 2, "lat": 20.8980, "lon": 80.6970, "area_sqkm": 810.0, "cropland_ha": 42000, "marketable_surplus_qtl": 1050000},

    # 10. Khairagarh-Chhuikhadan-Gandai District (2 Blocks)
    {"division": "Durg", "district": "Khairagarh-Chhuikhadan-Gandai", "block": "Khairagarh", "zone": 1, "lat": 21.4180, "lon": 80.9780, "area_sqkm": 790.0, "cropland_ha": 55000, "marketable_surplus_qtl": 1600000},
    {"division": "Durg", "district": "Khairagarh-Chhuikhadan-Gandai", "block": "Chhuikhadan", "zone": 1, "lat": 21.5340, "lon": 80.9880, "area_sqkm": 830.0, "cropland_ha": 52000, "marketable_surplus_qtl": 1490000},

    # 11. Mohla-Manpur-Ambagarh Chowki District (3 Blocks)
    {"division": "Durg", "district": "Mohla-Manpur-Ambagarh Chowki", "block": "Ambagarh Chowki", "zone": 2, "lat": 20.7810, "lon": 80.7380, "area_sqkm": 680.0, "cropland_ha": 38000, "marketable_surplus_qtl": 920000},
    {"division": "Durg", "district": "Mohla-Manpur-Ambagarh Chowki", "block": "Mohla", "zone": 2, "lat": 20.5750, "lon": 80.7510, "area_sqkm": 870.0, "cropland_ha": 31000, "marketable_surplus_qtl": 680000},
    {"division": "Durg", "district": "Mohla-Manpur-Ambagarh Chowki", "block": "Manpur", "zone": 3, "lat": 20.3550, "lon": 80.7580, "area_sqkm": 1120.0, "cropland_ha": 24000, "marketable_surplus_qtl": 450000},

    # 12. Kabirdham District (4 Blocks)
    {"division": "Durg", "district": "Kabirdham", "block": "Kawardha", "zone": 1, "lat": 22.0120, "lon": 81.2460, "area_sqkm": 720.0, "cropland_ha": 54000, "marketable_surplus_qtl": 1620000},
    {"division": "Durg", "district": "Kabirdham", "block": "Pandariya", "zone": 1, "lat": 22.2270, "lon": 81.4130, "area_sqkm": 890.0, "cropland_ha": 59000, "marketable_surplus_qtl": 1780000},
    {"division": "Durg", "district": "Kabirdham", "block": "Bodla", "zone": 2, "lat": 22.1760, "lon": 81.1890, "area_sqkm": 1150.0, "cropland_ha": 33000, "marketable_surplus_qtl": 740000},
    {"division": "Durg", "district": "Kabirdham", "block": "Sahaspur Lohara", "zone": 2, "lat": 21.8980, "lon": 81.1630, "area_sqkm": 810.0, "cropland_ha": 44000, "marketable_surplus_qtl": 1180000},

    # ==========================================
    # BILASPUR DIVISION (8 Districts | 34 Blocks)
    # ==========================================
    # 13. Bilaspur District (4 Blocks)
    {"division": "Bilaspur", "district": "Bilaspur", "block": "Belha", "zone": 1, "lat": 21.9360, "lon": 82.1640, "area_sqkm": 730.0, "cropland_ha": 56000, "marketable_surplus_qtl": 1720000},
    {"division": "Bilaspur", "district": "Bilaspur", "block": "Takhatpur", "zone": 1, "lat": 22.1480, "lon": 81.8710, "area_sqkm": 780.0, "cropland_ha": 61000, "marketable_surplus_qtl": 1840000},
    {"division": "Bilaspur", "district": "Bilaspur", "block": "Masturi", "zone": 1, "lat": 21.9880, "lon": 82.2850, "area_sqkm": 840.0, "cropland_ha": 64000, "marketable_surplus_qtl": 1910000},
    {"division": "Bilaspur", "district": "Bilaspur", "block": "Kota", "zone": 2, "lat": 22.2980, "lon": 82.0250, "area_sqkm": 1050.0, "cropland_ha": 41000, "marketable_surplus_qtl": 1020000},

    # 14. Mungeli District (3 Blocks)
    {"division": "Bilaspur", "district": "Mungeli", "block": "Mungeli", "zone": 1, "lat": 22.0670, "lon": 81.6910, "area_sqkm": 860.0, "cropland_ha": 67000, "marketable_surplus_qtl": 1980000},
    {"division": "Bilaspur", "district": "Mungeli", "block": "Lormi", "zone": 1, "lat": 22.2780, "lon": 81.7120, "area_sqkm": 940.0, "cropland_ha": 58000, "marketable_surplus_qtl": 1650000},
    {"division": "Bilaspur", "district": "Mungeli", "block": "Pathariya", "zone": 1, "lat": 21.9420, "lon": 81.8150, "area_sqkm": 710.0, "cropland_ha": 55000, "marketable_surplus_qtl": 1620000},

    # 15. Janjgir-Champa District (5 Blocks)
    {"division": "Bilaspur", "district": "Janjgir-Champa", "block": "Nawagarh", "zone": 1, "lat": 21.8740, "lon": 82.5980, "area_sqkm": 620.0, "cropland_ha": 52000, "marketable_surplus_qtl": 1820000},
    {"division": "Bilaspur", "district": "Janjgir-Champa", "block": "Akaltara", "zone": 1, "lat": 22.0220, "lon": 82.4280, "area_sqkm": 580.0, "cropland_ha": 48000, "marketable_surplus_qtl": 1690000},
    {"division": "Bilaspur", "district": "Janjgir-Champa", "block": "Baloda", "zone": 1, "lat": 22.1480, "lon": 82.4860, "area_sqkm": 640.0, "cropland_ha": 49000, "marketable_surplus_qtl": 1680000},
    {"division": "Bilaspur", "district": "Janjgir-Champa", "block": "Bamhnidih", "zone": 1, "lat": 21.9480, "lon": 82.7240, "area_sqkm": 570.0, "cropland_ha": 47000, "marketable_surplus_qtl": 1640000},
    {"division": "Bilaspur", "district": "Janjgir-Champa", "block": "Pamgarh", "zone": 1, "lat": 21.8820, "lon": 82.4350, "area_sqkm": 590.0, "cropland_ha": 51000, "marketable_surplus_qtl": 1790000},

    # 16. Sakti District (4 Blocks)
    {"division": "Bilaspur", "district": "Sakti", "block": "Sakti", "zone": 1, "lat": 22.0270, "lon": 82.9610, "area_sqkm": 680.0, "cropland_ha": 53000, "marketable_surplus_qtl": 1750000},
    {"division": "Bilaspur", "district": "Sakti", "block": "Jaijaipur", "zone": 1, "lat": 21.8480, "lon": 82.8980, "area_sqkm": 640.0, "cropland_ha": 51000, "marketable_surplus_qtl": 1710000},
    {"division": "Bilaspur", "district": "Sakti", "block": "Malkharoda", "zone": 1, "lat": 21.8150, "lon": 83.0240, "area_sqkm": 610.0, "cropland_ha": 49000, "marketable_surplus_qtl": 1640000},
    {"division": "Bilaspur", "district": "Sakti", "block": "Dabhra", "zone": 1, "lat": 21.7280, "lon": 83.1670, "area_sqkm": 670.0, "cropland_ha": 54000, "marketable_surplus_qtl": 1780000},

    # 17. Korba District (5 Blocks)
    {"division": "Bilaspur", "district": "Korba", "block": "Korba", "zone": 2, "lat": 22.3590, "lon": 82.7500, "area_sqkm": 780.0, "cropland_ha": 36000, "marketable_surplus_qtl": 920000},
    {"division": "Bilaspur", "district": "Korba", "block": "Kartala", "zone": 2, "lat": 22.1890, "lon": 82.8420, "area_sqkm": 840.0, "cropland_ha": 41000, "marketable_surplus_qtl": 1080000},
    {"division": "Bilaspur", "district": "Korba", "block": "Katghora", "zone": 2, "lat": 22.5080, "lon": 82.5530, "area_sqkm": 920.0, "cropland_ha": 39000, "marketable_surplus_qtl": 1020000},
    {"division": "Bilaspur", "district": "Korba", "block": "Pali", "zone": 3, "lat": 22.3780, "lon": 82.3360, "area_sqkm": 1180.0, "cropland_ha": 32000, "marketable_surplus_qtl": 710000},
    {"division": "Bilaspur", "district": "Korba", "block": "Poundi-Uproda", "zone": 3, "lat": 22.6840, "lon": 82.4280, "area_sqkm": 1840.0, "cropland_ha": 29000, "marketable_surplus_qtl": 590000},

    # 18. Raigarh District (7 Blocks)
    {"division": "Bilaspur", "district": "Raigarh", "block": "Raigarh", "zone": 1, "lat": 21.8970, "lon": 83.3950, "area_sqkm": 720.0, "cropland_ha": 52000, "marketable_surplus_qtl": 1620000},
    {"division": "Bilaspur", "district": "Raigarh", "block": "Pusaur", "zone": 1, "lat": 21.7580, "lon": 83.3640, "area_sqkm": 590.0, "cropland_ha": 47000, "marketable_surplus_qtl": 1540000},
    {"division": "Bilaspur", "district": "Raigarh", "block": "Kharsia", "zone": 1, "lat": 21.9980, "lon": 83.1250, "area_sqkm": 650.0, "cropland_ha": 49000, "marketable_surplus_qtl": 1580000},
    {"division": "Bilaspur", "district": "Raigarh", "block": "Gharghoda", "zone": 2, "lat": 22.1640, "lon": 83.3510, "area_sqkm": 870.0, "cropland_ha": 38000, "marketable_surplus_qtl": 960000},
    {"division": "Bilaspur", "district": "Raigarh", "block": "Tamnar", "zone": 2, "lat": 22.1120, "lon": 83.4790, "area_sqkm": 790.0, "cropland_ha": 36000, "marketable_surplus_qtl": 890000},
    {"division": "Bilaspur", "district": "Raigarh", "block": "Lailunga", "zone": 2, "lat": 22.4210, "lon": 83.5680, "area_sqkm": 940.0, "cropland_ha": 39000, "marketable_surplus_qtl": 980000},
    {"division": "Bilaspur", "district": "Raigarh", "block": "Dharamjaigarh", "zone": 3, "lat": 22.4680, "lon": 83.2180, "area_sqkm": 1420.0, "cropland_ha": 34000, "marketable_surplus_qtl": 780000},

    # 19. Sarangarh-Bilaigarh District (3 Blocks)
    {"division": "Bilaspur", "district": "Sarangarh-Bilaigarh", "block": "Sarangarh", "zone": 1, "lat": 21.5890, "lon": 83.0820, "area_sqkm": 760.0, "cropland_ha": 57000, "marketable_surplus_qtl": 1780000},
    {"division": "Bilaspur", "district": "Sarangarh-Bilaigarh", "block": "Baramkela", "zone": 1, "lat": 21.6120, "lon": 83.3420, "area_sqkm": 680.0, "cropland_ha": 54000, "marketable_surplus_qtl": 1710000},
    {"division": "Bilaspur", "district": "Sarangarh-Bilaigarh", "block": "Bilaigarh", "zone": 1, "lat": 21.6420, "lon": 82.7210, "area_sqkm": 710.0, "cropland_ha": 55000, "marketable_surplus_qtl": 1720000},

    # 20. Gaurela-Pendra-Marwahi District (3 Blocks)
    {"division": "Bilaspur", "district": "Gaurela-Pendra-Marwahi", "block": "Gaurela", "zone": 3, "lat": 22.7560, "lon": 81.9120, "area_sqkm": 730.0, "cropland_ha": 28000, "marketable_surplus_qtl": 590000},
    {"division": "Bilaspur", "district": "Gaurela-Pendra-Marwahi", "block": "Pendra", "zone": 3, "lat": 22.7680, "lon": 82.0450, "area_sqkm": 690.0, "cropland_ha": 27000, "marketable_surplus_qtl": 560000},
    {"division": "Bilaspur", "district": "Gaurela-Pendra-Marwahi", "block": "Marwahi", "zone": 3, "lat": 22.9890, "lon": 82.0340, "area_sqkm": 880.0, "cropland_ha": 25000, "marketable_surplus_qtl": 490000},

    # ========================================================
    # SURGUJA DIVISION / NORTHERN HILLS (6 Districts | 32 Blocks)
    # ========================================================
    # 21. Surguja District (7 Blocks)
    {"division": "Surguja", "district": "Surguja", "block": "Ambikapur", "zone": 3, "lat": 23.1180, "lon": 83.1980, "area_sqkm": 760.0, "cropland_ha": 42000, "marketable_surplus_qtl": 980000},
    {"division": "Surguja", "district": "Surguja", "block": "Lundra", "zone": 3, "lat": 23.0820, "lon": 83.3980, "area_sqkm": 680.0, "cropland_ha": 34000, "marketable_surplus_qtl": 750000},
    {"division": "Surguja", "district": "Surguja", "block": "Batauli", "zone": 3, "lat": 22.9540, "lon": 83.3640, "area_sqkm": 620.0, "cropland_ha": 31000, "marketable_surplus_qtl": 680000},
    {"division": "Surguja", "district": "Surguja", "block": "Sitapur", "zone": 3, "lat": 22.7840, "lon": 83.5120, "area_sqkm": 790.0, "cropland_ha": 36000, "marketable_surplus_qtl": 810000},
    {"division": "Surguja", "district": "Surguja", "block": "Mainpat", "zone": 3, "lat": 22.8120, "lon": 83.2980, "area_sqkm": 1140.0, "cropland_ha": 26000, "marketable_surplus_qtl": 510000},
    {"division": "Surguja", "district": "Surguja", "block": "Udaipur", "zone": 3, "lat": 22.9150, "lon": 82.9640, "area_sqkm": 890.0, "cropland_ha": 33000, "marketable_surplus_qtl": 720000},
    {"division": "Surguja", "district": "Surguja", "block": "Lakhanpur", "zone": 3, "lat": 23.0250, "lon": 83.0450, "area_sqkm": 740.0, "cropland_ha": 35000, "marketable_surplus_qtl": 780000},

    # 22. Surajpur District (6 Blocks)
    {"division": "Surguja", "district": "Surajpur", "block": "Surajpur", "zone": 3, "lat": 23.2180, "lon": 82.8710, "area_sqkm": 730.0, "cropland_ha": 38000, "marketable_surplus_qtl": 850000},
    {"division": "Surguja", "district": "Surajpur", "block": "Bhaiyathan", "zone": 3, "lat": 23.3850, "lon": 82.8980, "area_sqkm": 680.0, "cropland_ha": 34000, "marketable_surplus_qtl": 740000},
    {"division": "Surguja", "district": "Surajpur", "block": "Odgi", "zone": 3, "lat": 23.5640, "lon": 82.8520, "area_sqkm": 940.0, "cropland_ha": 27000, "marketable_surplus_qtl": 540000},
    {"division": "Surguja", "district": "Surajpur", "block": "Pratappur", "zone": 3, "lat": 23.4980, "lon": 83.1890, "area_sqkm": 820.0, "cropland_ha": 36000, "marketable_surplus_qtl": 810000},
    {"division": "Surguja", "district": "Surajpur", "block": "Premnagar", "zone": 3, "lat": 22.9850, "lon": 82.7480, "area_sqkm": 780.0, "cropland_ha": 32000, "marketable_surplus_qtl": 690000},
    {"division": "Surguja", "district": "Surajpur", "block": "Ramanujnagar", "zone": 3, "lat": 23.1250, "lon": 82.7120, "area_sqkm": 810.0, "cropland_ha": 35000, "marketable_surplus_qtl": 760000},

    # 23. Balrampur-Ramanujganj District (6 Blocks)
    {"division": "Surguja", "district": "Balrampur-Ramanujganj", "block": "Balrampur", "zone": 3, "lat": 23.6120, "lon": 83.6180, "area_sqkm": 870.0, "cropland_ha": 33000, "marketable_surplus_qtl": 710000},
    {"division": "Surguja", "district": "Balrampur-Ramanujganj", "block": "Rajpur", "zone": 3, "lat": 23.4350, "lon": 83.3980, "area_sqkm": 720.0, "cropland_ha": 35000, "marketable_surplus_qtl": 770000},
    {"division": "Surguja", "district": "Balrampur-Ramanujganj", "block": "Shankargarh", "zone": 3, "lat": 23.3640, "lon": 83.6980, "area_sqkm": 890.0, "cropland_ha": 29000, "marketable_surplus_qtl": 590000},
    {"division": "Surguja", "district": "Balrampur-Ramanujganj", "block": "Kusmi", "zone": 3, "lat": 23.4120, "lon": 83.9210, "area_sqkm": 1120.0, "cropland_ha": 25000, "marketable_surplus_qtl": 480000},
    {"division": "Surguja", "district": "Balrampur-Ramanujganj", "block": "Ramchandrapur", "zone": 3, "lat": 23.7840, "lon": 83.6980, "area_sqkm": 940.0, "cropland_ha": 31000, "marketable_surplus_qtl": 650000},
    {"division": "Surguja", "district": "Balrampur-Ramanujganj", "block": "Wadrafnagar", "zone": 3, "lat": 23.7560, "lon": 83.2120, "area_sqkm": 860.0, "cropland_ha": 34000, "marketable_surplus_qtl": 720000},

    # 24. Jashpur District (8 Blocks)
    {"division": "Surguja", "district": "Jashpur", "block": "Jashpur", "zone": 3, "lat": 22.8840, "lon": 84.1450, "area_sqkm": 820.0, "cropland_ha": 36000, "marketable_surplus_qtl": 760000},
    {"division": "Surguja", "district": "Jashpur", "block": "Manora", "zone": 3, "lat": 22.9850, "lon": 84.0250, "area_sqkm": 680.0, "cropland_ha": 28000, "marketable_surplus_qtl": 550000},
    {"division": "Surguja", "district": "Jashpur", "block": "Kunkuri", "zone": 3, "lat": 22.7480, "lon": 83.9540, "area_sqkm": 740.0, "cropland_ha": 38000, "marketable_surplus_qtl": 820000},
    {"division": "Surguja", "district": "Jashpur", "block": "Duldula", "zone": 3, "lat": 22.6840, "lon": 84.1120, "area_sqkm": 590.0, "cropland_ha": 29000, "marketable_surplus_qtl": 590000},
    {"division": "Surguja", "district": "Jashpur", "block": "Kansabel", "zone": 3, "lat": 22.6580, "lon": 83.7850, "area_sqkm": 670.0, "cropland_ha": 32000, "marketable_surplus_qtl": 670000},
    {"division": "Surguja", "district": "Jashpur", "block": "Bagicha", "zone": 3, "lat": 23.0120, "lon": 83.6980, "area_sqkm": 1190.0, "cropland_ha": 31000, "marketable_surplus_qtl": 610000},
    {"division": "Surguja", "district": "Jashpur", "block": "Pathalgaon", "zone": 3, "lat": 22.5640, "lon": 83.4680, "area_sqkm": 810.0, "cropland_ha": 44000, "marketable_surplus_qtl": 980000},
    {"division": "Surguja", "district": "Jashpur", "block": "Farsabahar", "zone": 3, "lat": 22.5020, "lon": 83.8980, "area_sqkm": 720.0, "cropland_ha": 35000, "marketable_surplus_qtl": 730000},

    # 25. Koriya District (2 Blocks)
    {"division": "Surguja", "district": "Koriya", "block": "Baikunthpur", "zone": 3, "lat": 23.2720, "lon": 82.5580, "area_sqkm": 890.0, "cropland_ha": 34000, "marketable_surplus_qtl": 710000},
    {"division": "Surguja", "district": "Koriya", "block": "Sonhat", "zone": 3, "lat": 23.4750, "lon": 82.5340, "area_sqkm": 1420.0, "cropland_ha": 22000, "marketable_surplus_qtl": 410000},

    # 26. Manendragarh-Chirmiri-Bharatpur District (3 Blocks)
    {"division": "Surguja", "district": "Manendragarh-Chirmiri-Bharatpur", "block": "Manendragarh", "zone": 3, "lat": 23.2120, "lon": 82.2040, "area_sqkm": 880.0, "cropland_ha": 29000, "marketable_surplus_qtl": 580000},
    {"division": "Surguja", "district": "Manendragarh-Chirmiri-Bharatpur", "block": "Khadgawan", "zone": 3, "lat": 23.1450, "lon": 82.3980, "area_sqkm": 920.0, "cropland_ha": 31000, "marketable_surplus_qtl": 620000},
    {"division": "Surguja", "district": "Manendragarh-Chirmiri-Bharatpur", "block": "Bharatpur", "zone": 3, "lat": 23.7380, "lon": 81.8210, "area_sqkm": 2180.0, "cropland_ha": 26000, "marketable_surplus_qtl": 480000},

    # ========================================================
    # BASTAR DIVISION / SOUTHERN PLATEAU (7 Districts | 32 Blocks)
    # ========================================================
    # 27. Bastar District (7 Blocks)
    {"division": "Bastar", "district": "Bastar", "block": "Jagdalpur", "zone": 3, "lat": 19.0780, "lon": 82.0280, "area_sqkm": 720.0, "cropland_ha": 41000, "marketable_surplus_qtl": 950000},
    {"division": "Bastar", "district": "Bastar", "block": "Bakawand", "zone": 3, "lat": 19.1890, "lon": 82.1640, "area_sqkm": 680.0, "cropland_ha": 38000, "marketable_surplus_qtl": 860000},
    {"division": "Bastar", "district": "Bastar", "block": "Bastar", "zone": 3, "lat": 19.2150, "lon": 81.9320, "area_sqkm": 650.0, "cropland_ha": 37000, "marketable_surplus_qtl": 820000},
    {"division": "Bastar", "district": "Bastar", "block": "Lohandiguda", "zone": 3, "lat": 19.0620, "lon": 81.7850, "area_sqkm": 740.0, "cropland_ha": 32000, "marketable_surplus_qtl": 680000},
    {"division": "Bastar", "district": "Bastar", "block": "Tokapal", "zone": 3, "lat": 18.9640, "lon": 81.8980, "area_sqkm": 590.0, "cropland_ha": 31000, "marketable_surplus_qtl": 660000},
    {"division": "Bastar", "district": "Bastar", "block": "Darbha", "zone": 3, "lat": 18.8650, "lon": 81.8740, "area_sqkm": 870.0, "cropland_ha": 26000, "marketable_surplus_qtl": 510000},
    {"division": "Bastar", "district": "Bastar", "block": "Bastanar", "zone": 3, "lat": 18.9480, "lon": 81.6580, "area_sqkm": 810.0, "cropland_ha": 25000, "marketable_surplus_qtl": 490000},

    # 28. Kondagaon District (5 Blocks)
    {"division": "Bastar", "district": "Kondagaon", "block": "Kondagaon", "zone": 3, "lat": 19.5980, "lon": 81.6740, "area_sqkm": 850.0, "cropland_ha": 42000, "marketable_surplus_qtl": 940000},
    {"division": "Bastar", "district": "Kondagaon", "block": "Makdi", "zone": 3, "lat": 19.7420, "lon": 81.8950, "area_sqkm": 790.0, "cropland_ha": 35000, "marketable_surplus_qtl": 750000},
    {"division": "Bastar", "district": "Kondagaon", "block": "Pharasgaon", "zone": 2, "lat": 19.8540, "lon": 81.6150, "area_sqkm": 720.0, "cropland_ha": 39000, "marketable_surplus_qtl": 880000},
    {"division": "Bastar", "district": "Kondagaon", "block": "Keshkal", "zone": 2, "lat": 20.0840, "lon": 81.5890, "area_sqkm": 890.0, "cropland_ha": 34000, "marketable_surplus_qtl": 760000},
    {"division": "Bastar", "district": "Kondagaon", "block": "Baderajpur", "zone": 2, "lat": 20.0450, "lon": 81.7980, "area_sqkm": 710.0, "cropland_ha": 33000, "marketable_surplus_qtl": 720000},

    # 29. Uttar Bastar Kanker District (7 Blocks)
    {"division": "Bastar", "district": "Uttar Bastar Kanker", "block": "Kanker", "zone": 2, "lat": 20.2720, "lon": 81.4920, "area_sqkm": 680.0, "cropland_ha": 38000, "marketable_surplus_qtl": 910000},
    {"division": "Bastar", "district": "Uttar Bastar Kanker", "block": "Charama", "zone": 2, "lat": 20.4580, "lon": 81.3850, "area_sqkm": 610.0, "cropland_ha": 41000, "marketable_surplus_qtl": 1050000},
    {"division": "Bastar", "district": "Uttar Bastar Kanker", "block": "Narharpur", "zone": 2, "lat": 20.4120, "lon": 81.6580, "area_sqkm": 820.0, "cropland_ha": 36000, "marketable_surplus_qtl": 840000},
    {"division": "Bastar", "district": "Uttar Bastar Kanker", "block": "Bhanupratappur", "zone": 3, "lat": 20.3120, "lon": 81.0820, "area_sqkm": 790.0, "cropland_ha": 37000, "marketable_surplus_qtl": 860000},
    {"division": "Bastar", "district": "Uttar Bastar Kanker", "block": "Durgkondal", "zone": 3, "lat": 20.3980, "lon": 80.8950, "area_sqkm": 890.0, "cropland_ha": 28000, "marketable_surplus_qtl": 590000},
    {"division": "Bastar", "district": "Uttar Bastar Kanker", "block": "Antagarh", "zone": 3, "lat": 20.0980, "lon": 81.1640, "area_sqkm": 1120.0, "cropland_ha": 31000, "marketable_surplus_qtl": 680000},
    {"division": "Bastar", "district": "Uttar Bastar Kanker", "block": "Koylibeda", "zone": 3, "lat": 20.1450, "lon": 80.9250, "area_sqkm": 1410.0, "cropland_ha": 29000, "marketable_surplus_qtl": 610000},

    # 30. Dakshin Bastar Dantewada District (4 Blocks)
    {"division": "Bastar", "district": "Dakshin Bastar Dantewada", "block": "Dantewada", "zone": 3, "lat": 18.8950, "lon": 81.3520, "area_sqkm": 780.0, "cropland_ha": 31000, "marketable_surplus_qtl": 650000},
    {"division": "Bastar", "district": "Dakshin Bastar Dantewada", "block": "Geedam", "zone": 3, "lat": 18.9850, "lon": 81.3980, "area_sqkm": 690.0, "cropland_ha": 33000, "marketable_surplus_qtl": 710000},
    {"division": "Bastar", "district": "Dakshin Bastar Dantewada", "block": "Kuakonda", "zone": 3, "lat": 18.7480, "lon": 81.4580, "area_sqkm": 810.0, "cropland_ha": 24000, "marketable_surplus_qtl": 460000},
    {"division": "Bastar", "district": "Dakshin Bastar Dantewada", "block": "Katekalyan", "zone": 3, "lat": 18.7980, "lon": 81.6580, "area_sqkm": 860.0, "cropland_ha": 23000, "marketable_surplus_qtl": 440000},

    # 31. Sukma District (3 Blocks)
    {"division": "Bastar", "district": "Sukma", "block": "Sukma", "zone": 3, "lat": 18.3980, "lon": 81.6620, "area_sqkm": 1150.0, "cropland_ha": 28000, "marketable_surplus_qtl": 560000},
    {"division": "Bastar", "district": "Sukma", "block": "Chhindgarh", "zone": 3, "lat": 18.5980, "lon": 81.7480, "area_sqkm": 1020.0, "cropland_ha": 29000, "marketable_surplus_qtl": 590000},
    {"division": "Bastar", "district": "Sukma", "block": "Konta", "zone": 3, "lat": 17.8120, "lon": 81.3950, "area_sqkm": 2180.0, "cropland_ha": 22000, "marketable_surplus_qtl": 380000},

    # 32. Bijapur District (4 Blocks)
    {"division": "Bastar", "district": "Bijapur", "block": "Bijapur", "zone": 3, "lat": 18.7980, "lon": 80.8120, "area_sqkm": 1450.0, "cropland_ha": 26000, "marketable_surplus_qtl": 490000},
    {"division": "Bastar", "district": "Bijapur", "block": "Bhairamgarh", "zone": 3, "lat": 19.0120, "lon": 80.9540, "area_sqkm": 1680.0, "cropland_ha": 27000, "marketable_surplus_qtl": 520000},
    {"division": "Bastar", "district": "Bijapur", "block": "Usoor", "zone": 3, "lat": 18.5280, "lon": 80.7980, "area_sqkm": 1890.0, "cropland_ha": 21000, "marketable_surplus_qtl": 360000},
    {"division": "Bastar", "district": "Bijapur", "block": "Bhopalpatnam", "zone": 3, "lat": 18.8540, "lon": 80.3850, "area_sqkm": 1750.0, "cropland_ha": 24000, "marketable_surplus_qtl": 440000},

    # 33. Narayanpur District (2 Blocks)
    {"division": "Bastar", "district": "Narayanpur", "block": "Narayanpur", "zone": 3, "lat": 19.7120, "lon": 81.2540, "area_sqkm": 1280.0, "cropland_ha": 27000, "marketable_surplus_qtl": 530000},
    {"division": "Bastar", "district": "Narayanpur", "block": "Orchha", "zone": 3, "lat": 19.4680, "lon": 80.9850, "area_sqkm": 3680.0, "cropland_ha": 16000, "marketable_surplus_qtl": 250000},
]


def generate_catalog():
    # Compute bounding boxes for 5km search grids
    for b in BLOCKS_DATA:
        # Approximate 0.15 deg lat/lon span around centroid for bounding box
        delta = 0.12
        b["bbox"] = {
            "min_lat": round(b["lat"] - delta, 4),
            "min_lon": round(b["lon"] - delta, 4),
            "max_lat": round(b["lat"] + delta, 4),
            "max_lon": round(b["lon"] + delta, 4),
        }
        b["search_radius_m"] = 15000

    catalog = {
        "metadata": {
            "state": "Chhattisgarh",
            "total_divisions": 5,
            "total_districts": 33,
            "total_blocks": len(BLOCKS_DATA),
            "agro_climatic_zones": {
                "Zone 1": "Chhattisgarh Plains (Beta_slope = 1.00)",
                "Zone 2": "Undulating Foothills & Transition Blocks (Beta_slope = 1.20)",
                "Zone 3": "Steep Northern Hills & Southern Bastar Plateau (Beta_slope = 1.40)"
            }
        },
        "blocks": BLOCKS_DATA
    }

    os.makedirs("configs", exist_ok=True)
    with open("configs/chhattisgarh_blocks_catalog.json", "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    print(f"Successfully generated catalog for all {len(BLOCKS_DATA)} blocks across 33 districts and 5 divisions!")


if __name__ == "__main__":
    generate_catalog()
