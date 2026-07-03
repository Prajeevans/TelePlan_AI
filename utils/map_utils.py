import folium
from folium.plugins import HeatMap

# Add tower marker and coverage circle to the map
def add_tower(map_object, tower, radius):

    folium.Marker(
        [tower["lat"], tower["lon"]],
        popup="Tower",
        icon=folium.Icon(color="red")
    ).add_to(map_object)

    folium.Circle(
        location=[tower["lat"], tower["lon"]],
        radius=radius,
        color="blue",
        fill=True,
        fill_opacity=0.2
    ).add_to(map_object)

# Add heatmap to the map
def add_heatmap(map_object, coverage_data):
    """
    coverage_data = [(lat, lon, rsrp)]
    """

    heat_data = []

    for lat, lon, rsrp in coverage_data:

        # normalize signal for visualization
        intensity = max(min((rsrp + 100) / 50, 1), 0)

        heat_data.append([lat, lon, intensity])

    HeatMap(heat_data, radius=15, blur=10).add_to(map_object)