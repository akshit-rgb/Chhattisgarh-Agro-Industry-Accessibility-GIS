"""
Interactive Cartographic & Visual Analytics Engine for Chhattisgarh Agro-Logistics.
Generates:
1. Interactive Multi-Layer Folium Web Map with Choropleths, POI clusters, and Coldspots.
2. High-Resolution Publication-Grade Matplotlib/Seaborn Charts for Transport Economics.
"""

import os
import json
import logging
import pandas as pd
import folium
from folium import plugins
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("MapVisualizer")

# Set publication style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"font.size": 11, "font.family": "sans-serif"})


def generate_interactive_maps(blocks_csv: str = "data/processed/chhattisgarh_all_146_blocks_master.csv",
                              poi_csv: str = "data/processed/chhattisgarh_agro_poi_master.csv",
                              coldspots_csv: str = "data/processed/chhattisgarh_coldspots_interventions.csv",
                              output_dir: str = "outputs/maps") -> str:
    """
    Builds a comprehensive interactive Leaflet/Folium map of Chhattisgarh's agro-infrastructure.
    """
    logger.info("Generating interactive Folium maps...")
    os.makedirs(output_dir, exist_ok=True)

    df_blocks = pd.read_csv(blocks_csv)
    df_pois = pd.read_csv(poi_csv)
    df_cold = pd.read_csv(coldspots_csv)

    # Center map on Chhattisgarh centroid (approx 21.2787, 81.8661)
    cg_map = folium.Map(
        location=[21.2787, 81.8661],
        zoom_start=7,
        tiles="CartoDB positron"
    )

    # 1. Feature Group: Block Centroids & Accessibility
    fg_blocks = folium.FeatureGroup(name="Block Centers & Logistics Cost (INR/Qtl)", show=True)
    for _, row in df_blocks.iterrows():
        cost = row["Total_Logistics_Cost_INR_Qtl"]
        tractor_t = row["Tractor_Travel_Time_Min"]
        truck_t = row["Truck_Travel_Time_Min"]
        acc_score = row["Accessibility_2SFCA_Score"]

        # Color scale based on cost: green (<35) -> orange (35-50) -> red (>50)
        if cost < 35.0:
            color = "#2ecc71"
            radius = 6
        elif cost <= 50.0:
            color = "#f39c12"
            radius = 8
        else:
            color = "#e74c3c"
            radius = 10

        popup_html = f"""
        <div style="font-family: Arial, sans-serif; width: 240px; font-size: 12px;">
            <h4 style="margin: 0 0 5px 0; color: #2c3e50;">{row['CD_Block']} ({row['District']})</h4>
            <b>Division:</b> {row['Division']}<br/>
            <b>Agro-Climatic Zone:</b> {row['Agro_Climatic_Zone']}<br/>
            <hr style="margin: 4px 0;"/>
            <b>Total Logistics Cost:</b> <span style="color: {color}; font-weight: bold;">₹{cost:.1f} / Qtl</span><br/>
            <b>Farm-to-Mandi Cost:</b> ₹{row['Farm_to_Mandi_Cost_INR_Qtl']:.1f} / Qtl<br/>
            <b>Mandi-to-Mill Cost:</b> ₹{row['Mandi_to_Mill_Cost_INR_Qtl']:.1f} / Qtl<br/>
            <b>Tractor Travel Time:</b> {tractor_t:.0f} mins<br/>
            <b>Truck Travel Time:</b> {truck_t:.0f} mins<br/>
            <b>2SFCA Access Score:</b> {acc_score:.1f} / 100<br/>
            <b>Micro/Small Units:</b> {int(row['Google_Maps_&_OSM_Micro_Small_Units'])}<br/>
            <b>Commercial Mills:</b> {int(row['Medium_Large_Units'])}
        </div>
        """
        folium.CircleMarker(
            location=[row["Centroid_Lat"], row["Centroid_Lon"]],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.75,
            popup=folium.Popup(popup_html, max_width=280),
            tooltip=f"{row['CD_Block']}: ₹{cost:.1f}/Qtl | {tractor_t:.0f} min"
        ).add_to(fg_blocks)
    fg_blocks.add_to(cg_map)

    # 2. Feature Group: Coldspots & Proposed Interventions
    fg_coldspots = folium.FeatureGroup(name="Agro-Processing Coldspots & Proposed FPO Hubs", show=True)
    for _, row in df_cold.iterrows():
        opt_lat = row["Optimal_Latitude"]
        opt_lon = row["Optimal_Longitude"]
        f_type = row["Recommended_Facility_Type"]
        savings_qtl = row["Cost_Savings_INR_Qtl"]
        annual_sav = row["Annual_Farmer_Savings_INR_Lakhs"]

        cold_popup = f"""
        <div style="font-family: Arial, sans-serif; width: 280px; font-size: 12px; background-color: #fcf8e3; padding: 6px; border-left: 4px solid #d9534f;">
            <h4 style="margin: 0 0 5px 0; color: #c9302c;">Policy Intervention: {row['CD_Block']}</h4>
            <b>District:</b> {row['District']} | <b>Priority:</b> {row['Policy_Priority']}<br/>
            <hr style="margin: 4px 0;"/>
            <b>Recommended Unit:</b><br/><i>{f_type}</i><br/>
            <b>Estimated Capex:</b> ₹{row['Estimated_Capex_INR_Lakhs']:.1f} Lakhs<br/>
            <b>Capacity:</b> {row['Capacity_MT_Day']:.0f} MT/Day<br/>
            <b>Current Freight Cost:</b> ₹{row['Pre_Intervention_Transport_Cost_INR_Qtl']:.1f} / Qtl<br/>
            <b>Post-Intervention Cost:</b> ₹{row['Post_Intervention_Transport_Cost_INR_Qtl']:.1f} / Qtl<br/>
            <b>Farmer Savings:</b> <span style="color: #27ae60; font-weight: bold;">₹{savings_qtl:.1f} / Qtl (-48%)</span><br/>
            <b>Annual Block Benefit:</b> <span style="color: #27ae60; font-weight: bold;">₹{annual_sav:.2f} Lakhs</span>
        </div>
        """
        folium.Marker(
            location=[opt_lat, opt_lon],
            icon=folium.Icon(color="red", icon="wrench", prefix="fa"),
            popup=folium.Popup(cold_popup, max_width=320),
            tooltip=f"Proposed Hub: {row['CD_Block']} (Save ₹{savings_qtl:.1f}/Qtl)"
        ).add_to(fg_coldspots)
    fg_coldspots.add_to(cg_map)

    # 3. Feature Group: Major Commercial Mills & Silos
    fg_commercial = folium.FeatureGroup(name="Commercial Mills & Silos (Sample)", show=False)
    sample_mills = df_pois[df_pois["scale"] == "Medium/Large"].sample(min(80, len(df_pois[df_pois["scale"] == "Medium/Large"])))
    for _, row in sample_mills.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=4,
            color="#8e44ad",
            fill=True,
            fill_color="#9b59b6",
            fill_opacity=0.8,
            tooltip=f"{row['name']} ({row['capacity_mt_day']} MT/Day)"
        ).add_to(fg_commercial)
    fg_commercial.add_to(cg_map)

    # 4. Isochrone Buffer Rings around Raipur & Bilaspur Mega Industrial Silo Hubs
    fg_isochrones = folium.FeatureGroup(name="Service Catchment Isochrones (15/30/60/90 mins)", show=False)
    hubs = [
        {"name": "Raipur Central Silo Hub", "lat": 21.2514, "lon": 81.6296},
        {"name": "Bilaspur Agro Logistics Park", "lat": 22.0797, "lon": 82.1409},
        {"name": "Jagdalpur Bastar Hub", "lat": 19.0780, "lon": 82.0280}
    ]
    # Approx radii: 15 min (~11 km), 30 min (~22 km), 60 min (~45 km), 90 min (~68 km)
    isochrone_radii_m = [
        (11000, "#2ecc71", "15-minute Tractor/Truck Catchment"),
        (22000, "#3498db", "30-minute Catchment"),
        (45000, "#f39c12", "60-minute Catchment Threshold"),
        (68000, "#e74c3c", "90-minute Critical Buffer")
    ]
    for hub in hubs:
        for r_m, col, label in isochrone_radii_m:
            folium.Circle(
                location=[hub["lat"], hub["lon"]],
                radius=r_m,
                color=col,
                weight=1.5,
                fill=False,
                tooltip=f"{hub['name']} - {label}"
            ).add_to(fg_isochrones)
    fg_isochrones.add_to(cg_map)

    # Add Layer Control
    folium.LayerControl(collapsed=False).add_to(cg_map)

    # Save HTML map
    map_html_path = os.path.join(output_dir, "chhattisgarh_agro_accessibility_map.html")
    cg_map.save(map_html_path)
    logger.info(f"Saved interactive Folium map to: {map_html_path}")

    return map_html_path


def generate_publication_charts(blocks_csv: str = "data/processed/chhattisgarh_all_146_blocks_master.csv",
                                output_dir: str = "outputs/figures") -> None:
    """
    Generates high-resolution publication charts comparing transportation economics across zones.
    """
    logger.info("Generating publication figures...")
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(blocks_csv)

    # Figure 1: Zone-wise Freight Cost Breakdown
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    sns.boxplot(
        data=df, x="Agro_Climatic_Zone", y="Total_Logistics_Cost_INR_Qtl",
        palette=["#2ecc71", "#f39c12", "#e74c3c"], ax=axes[0]
    )
    axes[0].set_title("Total Logistics Cost (INR/Quintal) by Agro-Climatic Zone", fontweight="bold")
    axes[0].set_xlabel("Agro-Climatic Zone")
    axes[0].set_ylabel("Total Transportation Cost (INR / Quintal)")
    axes[0].axhline(35.0, color="red", linestyle="--", alpha=0.8, label="Coldspot Friction Threshold (₹35/Qtl)")
    axes[0].legend(loc="upper left")

    # Figure 1b: Tractor Travel Time by Zone
    sns.boxplot(
        data=df, x="Agro_Climatic_Zone", y="Tractor_Travel_Time_Min",
        palette=["#2ecc71", "#f39c12", "#e74c3c"], ax=axes[1]
    )
    axes[1].set_title("Farm-to-Mandi Tractor Travel Time (Minutes)", fontweight="bold")
    axes[1].set_xlabel("Agro-Climatic Zone")
    axes[1].set_ylabel("Travel Time (Minutes, including 20 min terminal queue)")
    axes[1].axhline(60.0, color="red", linestyle="--", alpha=0.8, label="Coldspot Time Threshold (60 min)")
    axes[1].legend(loc="upper left")

    plt.tight_layout()
    fig1_path = os.path.join(output_dir, "zone_transport_cost_comparison.png")
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    logger.info(f"Saved Figure 1 to: {fig1_path}")

    # Figure 2: Travel Distance vs Cost with 2SFCA Accessibility Bubble Scatter
    plt.figure(figsize=(10, 6))
    scatter = sns.scatterplot(
        data=df,
        x="Mean_Dist_to_Mandi_km",
        y="Total_Logistics_Cost_INR_Qtl",
        hue="Agro_Climatic_Zone",
        size="Accessibility_2SFCA_Score",
        sizes=(40, 250),
        palette=["#2ecc71", "#f39c12", "#e74c3c"],
        alpha=0.85
    )
    plt.axhline(35.0, color="red", linestyle="--", label="Coldspot Threshold (₹35/Qtl)")
    plt.title("Transportation Freight Cost vs Farm-to-Mandi Distance in Chhattisgarh", fontweight="bold")
    plt.xlabel("Mean Distance to Procurement Mandi / PACS (km)")
    plt.ylabel("Total Logistics Freight Cost (INR / Quintal)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()

    fig2_path = os.path.join(output_dir, "travel_time_vs_distance_scatter.png")
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    logger.info(f"Saved Figure 2 to: {fig2_path}")


if __name__ == "__main__":
    generate_interactive_maps()
    generate_publication_charts()
