import streamlit as st
import folium
from streamlit_folium import st_folium
from models.coverage import estimate_radius
from utils.map_utils import add_tower
from models.coverage_grid import generate_grid, compute_coverage
from models.link_budget import LinkBudget
from utils.map_utils import add_heatmap

# Page config
st.set_page_config(page_title="TelePlan AI", layout="wide")

st.title("TelePlan AI - Telecom Network Planner")

# Default location (Sri Lanka center)
default_lat = 7.8731
default_lon = 80.7718

# Session state to store towers
if "towers" not in st.session_state:
    st.session_state.towers = []

# Sidebar input
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


# Create map
m = folium.Map(location=[default_lat, default_lon], zoom_start=9)

# Add towers to map
for idx, tower in enumerate(st.session_state.towers):
    folium.Marker(
        location=[tower["lat"], tower["lon"]],
        popup=f"Tower {idx+1}",
        icon=folium.Icon(color="red", icon="signal", prefix="fa")
    ).add_to(m)

# Generate coverage map
if st.button("Generate Coverage Map"):

    lb = LinkBudget()

    # Sri Lanka bounding box (you can adjust)
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


# Display map with towers and coverage
for tower in st.session_state.towers:

    radius = estimate_radius(
        tower["power"],
        tower["freq"]
    )

    add_tower(
        m,
        tower,
        radius
    )

# Display map
st_data = st_folium(m, width=1100, height=600)

# Show tower list
st.subheader("Tower List")
st.write(st.session_state.towers)