import numpy as np
from utils.calculations import haversine_distance

TOWER_COLORS = [
    "#3b82f6",  # Vibrant Blue
    "#ef4444",  # Vibrant Red
    "#10b981",  # Vibrant Emerald Green
    "#f59e0b",  # Vibrant Amber/Yellow
    "#8b5cf6",  # Vibrant Purple
    "#ec4899",  # Vibrant Pink
    "#06b6d4",  # Vibrant Cyan
    "#f97316",  # Vibrant Orange
    "#14b8a6",  # Vibrant Teal
    "#6b7280"   # Gray
]

class NetworkPlanner:

    def __init__(self, coverage_engine):
        self.coverage_engine = coverage_engine

    def _calculate_rx_power(self, tower, lat, lon):
        distance = haversine_distance(
            tower["lat"],
            tower["lon"],
            lat,
            lon
        )
        path_loss = self.coverage_engine.propagation.path_loss(
            distance,
            tower["freq"],
            base_height=tower.get("height")
        )
        rx_power = self.coverage_engine.link_budget.received_power(
            path_loss,
            tx_power_dbm=tower.get("power")
        )
        return rx_power

    def calculate_best_server(self, towers):
        if not towers:
            return []

        # Determine bounding box of all towers
        lats = [t["lat"] for t in towers]
        lons = [t["lon"] for t in towers]
        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)

        # 2.5 km margin (~0.022 degrees) to cover edges
        margin = 0.022
        min_lat -= margin
        max_lat += margin
        min_lon -= margin
        max_lon += margin

        # Keep grid resolution bounded (around 30 points per axis) for performance
        lat_span = max_lat - min_lat
        lon_span = max_lon - min_lon
        
        step_lat = max(lat_span / 30, 0.002)
        step_lon = max(lon_span / 30, 0.002)

        lat_points = np.arange(min_lat, max_lat, step_lat)
        lon_points = np.arange(min_lon, max_lon, step_lon)

        network_map = []

        for lat in lat_points:
            for lon in lon_points:
                best_tower = None
                best_power = -999.0
                signals = []

                for tower in towers:
                    rx = self._calculate_rx_power(tower, lat, lon)
                    signals.append({
                        "tower_id": tower["id"],
                        "rx_power": rx
                    })

                    if rx > best_power:
                        best_power = rx
                        best_tower = tower["id"]

                color = TOWER_COLORS[(best_tower - 1) % len(TOWER_COLORS)] if best_tower is not None else "#6b7280"

                network_map.append({
                    "lat": float(lat),
                    "lon": float(lon),
                    "serving_tower": best_tower,
                    "rx_power": best_power,
                    "color": color,
                    "signals": signals
                })

        return network_map