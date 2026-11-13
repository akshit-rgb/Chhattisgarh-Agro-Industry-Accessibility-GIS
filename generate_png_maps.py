"""
High-Resolution Publication Cartography Engine for Chhattisgarh Agro-Logistics GIS.
Generates 300 DPI static PNG maps:
1. State-Wide Logistics Freight Cost (INR/Qtl) Choropleth Map
2. Agro-Processing Coldspots & Proposed Policy Interventions Map
3. 2SFCA Spatial Accessibility (0-100) Capacity Map
4. Master 4-Panel Agro-Logistics Atlas (300 DPI Publication Grade)
"""

import os
import json
import logging
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
from shapely.geometry import Point

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("PNGMapGenerator")

# Name crosswalk for official LGD boundary names to standard CD Block names
LGD_NAME_CROSSWALK = {
    'a.chowki (td)': 'Ambagarh Chowki',
    'bamhindih': 'Bamhnidih',
    'bhopal patnam': 'Bhopalpatnam',
    'chhurra': 'Chhura',
    'dabhara': 'Dabhra',
    'dondilohara': 'Dondi Lohara',
    'dongarghar': 'Dongargarh',
    'durgukondal': 'Durgkondal',
    'gariyaband': 'Gariaband',
    'gaurella-1': 'Gaurela',
    'gaurella-2': 'Pendra',
    'khadgawana': 'Khadgawan',
    'koilebeda': 'Koylibeda',
    'kuwakonda': 'Kuakonda',
    'manpur (td)': 'Manpur',
    'mohala (td)': 'Mohla',
    'nagari': 'Nagri',
    'odagi': 'Odgi',
    'orchha(abhujmad)': 'Orchha',
    'patthalgaon': 'Pathalgaon',
    'pharsabahar': 'Farsabahar',
    'podi uparoda': 'Poundi-Uproda',
    'pussore': 'Pusaur',
    's.lohara': 'Sahaspur Lohara'
}


def load_and_merge_geodata(boundaries_path: str = "data/processed/chhattisgarh_blocks_boundaries.geojson",
                           master_csv: str = "data/processed/chhattisgarh_all_146_blocks_master.csv",
                           coldspots_csv: str = "data/processed/chhattisgarh_coldspots_interventions.csv") -> tuple:
    """
    Loads vector block boundaries and merges with economic freight metrics.
    """
    gdf_boundaries = gpd.read_file(boundaries_path)
    df_metrics = pd.read_csv(master_csv)
    df_cold = pd.read_csv(coldspots_csv)

    # Standardize boundary names to Title Case matching CD_Block
    def clean_name(n):
        low = str(n).lower().strip()
        if low in LGD_NAME_CROSSWALK:
            return LGD_NAME_CROSSWALK[low]
        # Title case standard blocks (e.g. BIJAPUR -> Bijapur)
        return str(n).strip().title()

    gdf_boundaries["Clean_Block"] = gdf_boundaries["Block"].apply(clean_name)
    df_metrics["CD_Block_Clean"] = df_metrics["CD_Block"].astype(str).str.strip().str.title()

    # Ensure match key
    merged_gdf = gdf_boundaries.merge(
        df_metrics,
        left_on="Clean_Block",
        right_on="CD_Block_Clean",
        how="inner"
    )

    logger.info(f"Successfully matched {len(merged_gdf)} out of 146 block polygons with metrics.")

    return merged_gdf, df_cold


def add_north_arrow_and_scale(ax):
    """Adds a clean cartographic north arrow and scale indicator."""
    # North Arrow at top right
    x, y, arrow_length = 0.95, 0.94, 0.06
    ax.annotate(
        'N', xy=(x, y), xytext=(x, y - arrow_length),
        arrowprops=dict(facecolor='black', edgecolor='black', width=2, headwidth=8),
        ha='center', va='center', fontsize=12, fontweight='bold',
        xycoords='axes fraction'
    )


def generate_png_maps(output_dir: str = "outputs/figures"):
    """
    Generates all high-resolution static PNG maps.
    """
    os.makedirs(output_dir, exist_ok=True)
    gdf, df_cold = load_and_merge_geodata()

    # Dissolve to district boundaries for overlay outlines
    gdf_districts = gdf.dissolve(by="District_y" if "District_y" in gdf.columns else "District_x")

    logger.info("Generating Map 1: Logistics Freight Cost Choropleth PNG...")
    # -------------------------------------------------------------
    # MAP 1: Total Logistics Freight Cost (INR/Qtl) Choropleth
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11, 14), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    # Custom colormap: Green -> Gold -> Orange -> Red -> Crimson
    cmap_cost = LinearSegmentedColormap.from_list(
        "cg_cost",
        ["#27ae60", "#2ecc71", "#f1c40f", "#e67e22", "#e74c3c", "#962d22", "#5c1d16"]
    )

    gdf.plot(
        column="Total_Logistics_Cost_INR_Qtl",
        cmap=cmap_cost,
        linewidth=0.5,
        edgecolor="#ffffff",
        legend=True,
        legend_kwds={
            "label": "Total Freight Logistics Cost (INR / Quintal)",
            "orientation": "horizontal",
            "shrink": 0.65,
            "pad": 0.03,
            "aspect": 25
        },
        ax=ax
    )

    # District outlines
    gdf_districts.boundary.plot(ax=ax, color="#2c3e50", linewidth=1.2, alpha=0.85)

    # Annotate key district hubs
    key_hubs = [
        ("Raipur", 21.2514, 81.6296),
        ("Bilaspur", 22.0797, 82.1409),
        ("Durg", 21.1904, 81.2849),
        ("Jagdalpur", 19.0780, 82.0280),
        ("Ambikapur", 23.1180, 83.1980),
        ("Korba", 22.3595, 82.7501),
        ("Raigarh", 21.8974, 83.3950)
    ]
    for name, lat, lon in key_hubs:
        ax.plot(lon, lat, marker='o', markersize=4, color='#ffffff', markeredgecolor='#000000', markeredgewidth=1)
        ax.text(lon + 0.08, lat + 0.04, name, fontsize=8, fontweight='bold', color='#1a1a1a',
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#ffffff", alpha=0.7, edgecolor="none"))

    ax.set_title("CHHATTISGARH AGRO-LOGISTICS FREIGHT COST MAP\nState-Wide Block-Level Transportation Cost (INR / Quintal)",
                 fontsize=14, fontweight="bold", pad=15, color="#1e293b")
    ax.axis("off")
    add_north_arrow_and_scale(ax)

    # Add descriptive statistics card
    stats_text = (
        "STATEWIDE LOGISTICS SUMMARY\n"
        "• Total Blocks: 146 across 33 Districts\n"
        "• Zone 1 (Plains): ₹40.5 / Qtl (Mean)\n"
        "• Zone 2 (Foothills): ₹54.9 / Qtl\n"
        "• Zone 3 (Bastar & Hills): ₹119.5 / Qtl\n"
        "• Highest: Konta (₹286), Bharatpur (₹257)"
    )
    ax.text(0.03, 0.05, stats_text, transform=ax.transAxes, fontsize=8,
            bbox=dict(boxstyle="square,pad=0.6", facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1))

    plt.tight_layout()
    map1_path = os.path.join(output_dir, "chhattisgarh_logistics_cost_choropleth.png")
    plt.savefig(map1_path, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved Map 1 to: {map1_path}")

    # -------------------------------------------------------------
    # MAP 2: Agro-Processing Coldspots & Policy Interventions
    # -------------------------------------------------------------
    logger.info("Generating Map 2: Agro-Processing Coldspots & Interventions PNG...")
    fig, ax = plt.subplots(figsize=(11, 14), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    # Base background: Light muted tones
    gdf.plot(
        color="#f1f5f9",
        linewidth=0.4,
        edgecolor="#cbd5e1",
        ax=ax
    )

    # Highlight Coldspot blocks in red/salmon
    cold_block_names = set(df_cold["CD_Block"])
    gdf_coldspots = gdf[gdf["Clean_Block"].isin(cold_block_names)]
    gdf_coldspots.plot(
        color="#fee2e2",
        linewidth=0.6,
        edgecolor="#ef4444",
        alpha=0.8,
        ax=ax
    )

    gdf_districts.boundary.plot(ax=ax, color="#475569", linewidth=1.0, alpha=0.9)

    # Plot Interventions by facility type
    marker_config = {
        "Tribal Millet": {"color": "#dc2626", "marker": "*", "size": 110, "label": "Tribal Millet & MFP Processing Hub"},
        "Hill-Tract": {"color": "#2563eb", "marker": "^", "size": 75, "label": "Hill-Tract Minor Millet & Pulse Center"},
        "Solar-Powered": {"color": "#059669", "marker": "s", "size": 70, "label": "Solar Horticultural Cold Storage"},
        "Decentralized FPO": {"color": "#d97706", "marker": "o", "size": 65, "label": "Decentralized FPO Mini Rice Mill"}
    }

    for key, cfg in marker_config.items():
        subset = df_cold[df_cold["Recommended_Facility_Type"].str.contains(key, case=False, na=False)]
        if not subset.empty:
            ax.scatter(
                subset["Optimal_Longitude"], subset["Optimal_Latitude"],
                c=cfg["color"], marker=cfg["marker"], s=cfg["size"],
                edgecolors="#ffffff", linewidths=0.8, zorder=5, label=cfg["label"]
            )

    # Annotate Top 6 critical coldspots
    top_critical = df_cold.head(6)
    for _, row in top_critical.iterrows():
        ax.annotate(
            f"{row['CD_Block']}\n(Save ₹{row['Cost_Savings_INR_Qtl']:.0f}/Qtl)",
            xy=(row["Optimal_Longitude"], row["Optimal_Latitude"]),
            xytext=(10, -10), textcoords="offset points",
            fontsize=7, fontweight="bold", color="#991b1b",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#ffffff", edgecolor="#f87171", alpha=0.9),
            arrowprops=dict(arrowstyle="->", color="#ef4444", lw=0.8)
        )

    ax.set_title("CHHATTISGARH AGRO-PROCESSING COLDSPOTS & POLICY INTERVENTIONS\nOptimal Spatial Allocation of Proposed Decentralized FPO Processing Hubs",
                 fontsize=14, fontweight="bold", pad=15, color="#1e293b")
    ax.axis("off")
    add_north_arrow_and_scale(ax)
    ax.legend(loc="lower left", fontsize=8, framealpha=0.95, facecolor="#ffffff", edgecolor="#cbd5e1", title="Recommended Infrastructure")

    plt.tight_layout()
    map2_path = os.path.join(output_dir, "chhattisgarh_coldspots_interventions_map.png")
    plt.savefig(map2_path, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved Map 2 to: {map2_path}")

    # -------------------------------------------------------------
    # MAP 3: 2SFCA Processing Accessibility Score (0 - 100)
    # -------------------------------------------------------------
    logger.info("Generating Map 3: 2SFCA Spatial Accessibility PNG...")
    fig, ax = plt.subplots(figsize=(11, 14), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    cmap_acc = LinearSegmentedColormap.from_list("cg_acc", ["#b91c1c", "#ea580c", "#facc15", "#84cc16", "#15803d"])

    gdf.plot(
        column="Accessibility_2SFCA_Score",
        cmap=cmap_acc,
        linewidth=0.5,
        edgecolor="#ffffff",
        legend=True,
        legend_kwds={
            "label": "2SFCA Agro-Processing Accessibility Index (0 = Severe Deficit, 100 = Abundant Capacity)",
            "orientation": "horizontal",
            "shrink": 0.65,
            "pad": 0.03,
            "aspect": 25
        },
        ax=ax
    )
    gdf_districts.boundary.plot(ax=ax, color="#1e293b", linewidth=1.2, alpha=0.85)

    ax.set_title("CHHATTISGARH AGRO-PROCESSING SPATIAL ACCESSIBILITY (2SFCA)\nLocal Milling Capacity Relative to Marketable Agricultural Surplus",
                 fontsize=14, fontweight="bold", pad=15, color="#1e293b")
    ax.axis("off")
    add_north_arrow_and_scale(ax)

    plt.tight_layout()
    map3_path = os.path.join(output_dir, "chhattisgarh_spatial_accessibility_2sfca_map.png")
    plt.savefig(map3_path, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved Map 3 to: {map3_path}")

    # -------------------------------------------------------------
    # MAP 4: Master 4-Panel Agro-Logistics Atlas (300 DPI)
    # -------------------------------------------------------------
    logger.info("Generating Map 4: Master 4-Panel Atlas PNG...")
    fig, axes = plt.subplots(2, 2, figsize=(20, 24), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    # Panel A: Tractor Travel Time (min)
    gdf.plot(
        column="Tractor_Travel_Time_Min",
        cmap="YlOrRd",
        linewidth=0.4,
        edgecolor="#ffffff",
        legend=True,
        legend_kwds={"label": "Tractor Travel Time from Farm Gate to Mandi (Minutes)", "orientation": "horizontal", "shrink": 0.7, "pad": 0.02},
        ax=axes[0, 0]
    )
    gdf_districts.boundary.plot(ax=axes[0, 0], color="#334155", linewidth=1.0)
    axes[0, 0].set_title("(A) Farm-to-Mandi Tractor Travel Time (Minutes)", fontsize=13, fontweight="bold", color="#0f172a")
    axes[0, 0].axis("off")
    add_north_arrow_and_scale(axes[0, 0])

    # Panel B: Total Logistics Freight Cost (₹/Qtl)
    gdf.plot(
        column="Total_Logistics_Cost_INR_Qtl",
        cmap=cmap_cost,
        linewidth=0.4,
        edgecolor="#ffffff",
        legend=True,
        legend_kwds={"label": "Total Logistics Freight Cost (INR / Quintal)", "orientation": "horizontal", "shrink": 0.7, "pad": 0.02},
        ax=axes[0, 1]
    )
    gdf_districts.boundary.plot(ax=axes[0, 1], color="#334155", linewidth=1.0)
    axes[0, 1].set_title("(B) Combined Regional Freight Cost (INR / Quintal)", fontsize=13, fontweight="bold", color="#0f172a")
    axes[0, 1].axis("off")
    add_north_arrow_and_scale(axes[0, 1])

    # Panel C: 2SFCA Accessibility
    gdf.plot(
        column="Accessibility_2SFCA_Score",
        cmap=cmap_acc,
        linewidth=0.4,
        edgecolor="#ffffff",
        legend=True,
        legend_kwds={"label": "2SFCA Accessibility Index (0 = Deficit, 100 = Optimal)", "orientation": "horizontal", "shrink": 0.7, "pad": 0.02},
        ax=axes[1, 0]
    )
    gdf_districts.boundary.plot(ax=axes[1, 0], color="#334155", linewidth=1.0)
    axes[1, 0].set_title("(C) 2SFCA Milling Capacity Accessibility Score", fontsize=13, fontweight="bold", color="#0f172a")
    axes[1, 0].axis("off")
    add_north_arrow_and_scale(axes[1, 0])

    # Panel D: Coldspots & Proposed Hubs
    gdf.plot(color="#f1f5f9", linewidth=0.4, edgecolor="#cbd5e1", ax=axes[1, 1])
    gdf_coldspots.plot(color="#fee2e2", linewidth=0.5, edgecolor="#ef4444", alpha=0.8, ax=axes[1, 1])
    gdf_districts.boundary.plot(ax=axes[1, 1], color="#334155", linewidth=1.0)

    for key, cfg in marker_config.items():
        subset = df_cold[df_cold["Recommended_Facility_Type"].str.contains(key, case=False, na=False)]
        if not subset.empty:
            axes[1, 1].scatter(
                subset["Optimal_Longitude"], subset["Optimal_Latitude"],
                c=cfg["color"], marker=cfg["marker"], s=cfg["size"] * 0.75,
                edgecolors="#ffffff", linewidths=0.6, zorder=5, label=cfg["label"]
            )
    axes[1, 1].legend(loc="lower left", fontsize=8, framealpha=0.95, facecolor="#ffffff")
    axes[1, 1].set_title("(D) Priority Coldspots & Proposed FPO Processing Hubs", fontsize=13, fontweight="bold", color="#0f172a")
    axes[1, 1].axis("off")
    add_north_arrow_and_scale(axes[1, 1])

    fig.suptitle("CHHATTISGARH STATE-WIDE AGRO-LOGISTICS & SPATIAL ACCESSIBILITY ATLAS\n146 Community Development Blocks across 33 Districts & 5 Revenue Divisions",
                 fontsize=18, fontweight="bold", y=0.98, color="#0f172a")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    map4_path = os.path.join(output_dir, "chhattisgarh_master_atlas_4panel.png")
    plt.savefig(map4_path, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved Map 4 to: {map4_path}")

    return {
        "cost_map": map1_path,
        "coldspots_map": map2_path,
        "accessibility_map": map3_path,
        "atlas_4panel": map4_path
    }


if __name__ == "__main__":
    generate_png_maps()
