import streamlit as st
import folium
from streamlit_folium import st_folium
from models.coverage import CoverageEngine
from models.propagation import FreeSpacePropagation
from models.link_budget import LinkBudget
from utils.map_utils import add_tower, add_heatmap
from models.coverage_grid import generate_grid, compute_coverage

# Page config
st.set_page_config(page_title="TelePlan AI", layout="wide")
st.title("TelePlan AI - Telecom Network Planner")

# Default location (Sri Lanka center)
default_lat = 7.8731
default_lon = 80.7718

# Session state to store towers
if "towers" not in st.session_state:
    st.session_state.towers = []

# ---------------- Sidebar input ----------------
st.sidebar.header("Add Tower")

lat = st.sidebar.number_input("Latitude", value=default_lat)
lon = st.sidebar.number_input("Longitude", value=default_lon)
height = st.sidebar.number_input("Height (m)", value=30)
power = st.sidebar.number_input("Tx Power (dBm)", value=43)
freq = st.sidebar.number_input("Frequency (MHz)", value=3500)

if st.sidebar.button("Add Tower"):
    st.session_state.towers.append({
        "lat": lat,
        "lon": lon,
        "height": height,
        "power": power,
        "freq": freq
    })
    st.success("Tower added successfully!")

generate_coverage = st.button("Generate Coverage Map")

# ---------------- Build the map (all layers first) ----------------
m = folium.Map(location=[default_lat, default_lon], zoom_start=9)

# 1. Tower markers (single loop, no duplicates)
for idx, tower in enumerate(st.session_state.towers):
    folium.Marker(
        location=[tower["lat"], tower["lon"]],
        popup=f"Tower {idx + 1}",
        icon=folium.Icon(color="red", icon="signal", prefix="fa")
    ).add_to(m)

# 2. Coverage heatmap
if generate_coverage:
    lb = LinkBudget()

    grid = generate_grid(
        lat_min=6.5,
        lat_max=9.5,
        lon_min=79.5,
        lon_max=82.0,
        resolution=0.05
    )

    for tower in st.session_state.towers:
        coverage = compute_coverage(grid, tower, lb)
        add_heatmap(m, coverage)

    st.success("Coverage map generated!")

# 3. Propagation prediction (circle markers) for the first tower
prediction = None
if len(st.session_state.towers) > 0:
    engine = CoverageEngine(
        propagation_model=FreeSpacePropagation(),
        link_budget=LinkBudget()
    )

    prediction = engine.predict(st.session_state.towers[0])

    for point in prediction:
        folium.CircleMarker(
            location=[point["lat"], point["lon"]],
            radius=3,
            color=point["color"],
            fill=True,
            fill_color=point["color"],
            fill_opacity=0.6
        ).add_to(m)

# ---------------- Render the map (once, after everything is added) ----------------
st_data = st_folium(m, width=1100, height=600, key="main_map")

# ---------------- Info panels below the map ----------------
st.subheader("Tower List")
st.write(st.session_state.towers)

if prediction:
    st.subheader("Sample Prediction Points")
    st.write(prediction[:5])