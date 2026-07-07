from models.propagation import FreeSpacePropagation
from models.link_budget import LinkBudget
from utils.calculations import haversine_distance
from utils.signal_classifier import signal_quality

class CoverageEngine:

    def __init__(self, propagation_model, link_budget):
        self.propagation = propagation_model
        self.link_budget = link_budget
        
    def predict(self, tower):

        results = []

        lat = tower["lat"]
        lon = tower["lon"]

        # 5 km x 5 km grid
        step = 0.002

        for i in range(-25, 26):
            for j in range(-25, 26):

                point_lat = lat + i * step
                point_lon = lon + j * step

                distance = haversine_distance(
                    lat,
                    lon,
                    point_lat,
                    point_lon
                )

                path_loss = self.propagation.path_loss(
                    distance,
                    tower["freq"]
                )

                rx_power = self.link_budget.received_power(
                    path_loss
                )
                quality, color = signal_quality(rx_power)
                results.append({
                    "lat": point_lat,
                    "lon": point_lon,
                    "distance": distance,
                    "path_loss": path_loss,
                    "rx_power": rx_power,
                    "quality": quality,
                    "color": color
                })

        return results

    def predict_network(self, towers):
        """
        Predict coverage for multiple towers.
        """
        network_results = []

        for tower in towers:

            tower_results = self.predict(tower)

            network_results.append({
                "tower_id": tower["id"],
                "results": tower_results
            })

        return network_results