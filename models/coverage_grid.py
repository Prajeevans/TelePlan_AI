import numpy as np
from models.signal import calculate_rsrp


def generate_grid(lat_min, lat_max, lon_min, lon_max, resolution=0.01):
    """
    Creates a latitude/longitude grid.
    """

    lat_points = np.arange(lat_min, lat_max, resolution)
    lon_points = np.arange(lon_min, lon_max, resolution)

    grid = []

    for lat in lat_points:
        for lon in lon_points:
            grid.append((lat, lon))

    return grid


def compute_coverage(grid, tower, link_budget):
    """
    Computes RSRP for each grid point.
    """

    results = []

    for lat, lon in grid:

        # simple distance approximation (we improve later)
        distance_km = (
            ((lat - tower["lat"]) ** 2 + (lon - tower["lon"]) ** 2) ** 0.5
        ) * 111  # approx km conversion

        rsrp = calculate_rsrp(
            distance_km,
            link_budget,
            tx_power_dbm=tower.get("power"),
            frequency_mhz=tower.get("freq")
        )

        results.append((lat, lon, rsrp))

    return results