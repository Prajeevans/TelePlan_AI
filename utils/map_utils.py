import folium

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