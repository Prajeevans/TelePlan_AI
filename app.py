import streamlit as st
import folium
from streamlit_folium import st_folium
from models.coverage import CoverageEngine
from models.propagation import FreeSpacePropagation, OkumuraHataPropagation
from models.link_budget import LinkBudget
from utils.map_utils import add_tower, add_heatmap
from models.coverage_grid import generate_grid, compute_coverage
from models.network import NetworkPlanner

# Page config
st.set_page_config(page_title="TelePlan AI", layout="wide")
st.title("TelePlan AI - Telecom Network Planner")

# Default location (Sri Lanka center)
default_lat = 7.8731
default_lon = 80.7718

# ── Session state initialisation ────────────────────────────────────────────
if "towers" not in st.session_state:
    st.session_state.towers = []
if "coverage_generated" not in st.session_state:
    st.session_state.coverage_generated = False
if "heatmap_data" not in st.session_state:
    st.session_state.heatmap_data = []       # list of (lat, lon, rsrp) per tower
if "network_map" not in st.session_state:
    st.session_state.network_map = []
if "prediction" not in st.session_state:
    st.session_state.prediction = []

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.header("Add Tower")

lat = st.sidebar.number_input("Latitude", value=default_lat)
lon = st.sidebar.number_input("Longitude", value=default_lon)
height = st.sidebar.number_input("Height (m)", value=30)
power = st.sidebar.number_input("Tx Power (dBm)", value=43)
freq = st.sidebar.number_input("Frequency (MHz)", value=3500)
propagation_model = st.sidebar.selectbox(
    "Propagation Model",
    ["Free Space", "Okumura-Hata"]
)
environment = st.sidebar.selectbox(
    "Environment",
    ["Urban", "Suburban", "Rural"]
)

ue_height = st.sidebar.number_input(
    "User Equipment Height (m)",
    value=1.5
)

if st.sidebar.button("Add Tower"):
    tower_id = len(st.session_state.towers) + 1
    st.session_state.towers.append({
        "id": tower_id,
        "lat": lat,
        "lon": lon,
        "height": height,
        "power": power,
        "freq": freq,
    })
    # Clear cached results so they are recomputed after adding a tower
    st.session_state.coverage_generated = False
    st.session_state.heatmap_data = []
    st.session_state.network_map = []
    st.session_state.prediction = []
    st.success(f"Tower {tower_id} added successfully!")

if st.sidebar.button("Clear Towers"):
    st.session_state.towers = []
    st.session_state.coverage_generated = False
    st.session_state.heatmap_data = []
    st.session_state.network_map = []
    st.session_state.prediction = []
    st.sidebar.success("All towers cleared.")

# ── Generate Coverage button ─────────────────────────────────────────────────
generate_clicked = st.button("Generate Coverage Map", type="primary")

if generate_clicked:
    if not st.session_state.towers:
        st.warning("Please add at least one tower before generating coverage.")
    else:
        with st.spinner("Computing coverage — please wait..."):
            lb = LinkBudget()

            # --- Heatmap grid ---
            min_lat = min(t["lat"] for t in st.session_state.towers)
            max_lat = max(t["lat"] for t in st.session_state.towers)

            min_lon = min(t["lon"] for t in st.session_state.towers)
            max_lon = max(t["lon"] for t in st.session_state.towers)


            # Add margin around towers
            margin = 0.05

            lat_min = min_lat - margin
            lat_max = max_lat + margin

            lon_min = min_lon - margin
            lon_max = max_lon + margin

            # Make grid square
            lat_span = lat_max - lat_min
            lon_span = lon_max - min_lon

            if lat_span > lon_span:
                center_lon = (lon_min + lon_max) / 2
                lon_min = center_lon - lat_span / 2
                lon_max = center_lon + lat_span / 2
            elif lon_span > lat_span:
                center_lat = (lat_min + lat_max) / 2
                lat_min = center_lat - lon_span / 2
                lat_max = center_lat + lon_span / 2
                
            grid = generate_grid(
                lat_min=lat_min,
                lat_max=lat_max,
                lon_min=lon_min,
                lon_max=lon_max,
                resolution=0.05
            )
            st.session_state.heatmap_data = []
            for tower in st.session_state.towers:
                coverage = compute_coverage(grid, tower, lb)
                st.session_state.heatmap_data.append(coverage)

            # --- Propagation model ---
            if propagation_model == "Free Space":
                model = FreeSpacePropagation()
            else:
                model = OkumuraHataPropagation(
                    base_height=height,
                    mobile_height=ue_height,
                    environment=environment
                )

            engine = CoverageEngine(
                propagation_model=model,
                link_budget=LinkBudget()
            )

            # --- Best-server network map ---
            planner = NetworkPlanner(engine)
            st.session_state.network_map = planner.calculate_best_server(
                st.session_state.towers
            )

            # --- Per-tower prediction (first tower shown as coloured dots) ---
            st.session_state.prediction = engine.predict(st.session_state.towers[0])

            st.session_state.coverage_generated = True
        st.success("Coverage map generated!")

# ── Build the folium map (ALL layers must be added BEFORE st_folium) ─────────
m = folium.Map(location=[default_lat, default_lon], zoom_start=9)

# 1. Tower markers
for idx, tower in enumerate(st.session_state.towers):
    folium.Marker(
        location=[tower["lat"], tower["lon"]],
        popup=f"Tower {idx + 1}\nFreq: {tower['freq']} MHz\nPower: {tower['power']} dBm",
        icon=folium.Icon(color="red", icon="signal", prefix="fa")
    ).add_to(m)

# 2. Heatmap (only when coverage has been generated)
if st.session_state.coverage_generated:
    for coverage in st.session_state.heatmap_data:
        add_heatmap(m, coverage)

    # 3. Best-server coloured circle markers
    for point in st.session_state.network_map:
        folium.CircleMarker(
            location=[point["lat"], point["lon"]],
            radius=4,
            color=point["color"],
            fill=True,
            fill_color=point["color"],
            fill_opacity=0.5,
            popup=(
                f"Serving Tower: {point['serving_tower']}\n"
                f"Rx Power: {point['rx_power']:.2f} dBm"
            )
        ).add_to(m)

    # 4. Per-tower prediction dots (quality colour)
    for point in st.session_state.prediction:
        folium.CircleMarker(
            location=[point["lat"], point["lon"]],
            radius=3,
            color=point["color"],
            fill=True,
            fill_color=point["color"],
            fill_opacity=0.6
        ).add_to(m)

# ── Render the map ONCE, after all layers are added ──────────────────────────
st_data = st_folium(m, width=1100, height=600, key="main_map")
st.info(f"Current Propagation Model: {propagation_model}")

# ── Info panels below the map ─────────────────────────────────────────────────
st.subheader("Tower List")
if st.session_state.towers:
    st.write(st.session_state.towers)
else:
    st.write("No towers added yet.")

if st.session_state.coverage_generated and st.session_state.prediction:
    st.subheader("Sample Prediction Points (first tower)")
    st.write(st.session_state.prediction[:5])