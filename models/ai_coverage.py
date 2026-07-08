from models.ai_predictor import AIPredictor
from models.propagation import FreeSpacePropagation
from models.link_budget import LinkBudget

from utils.calculations import haversine_distance


class AICoverage:

    def __init__(self):

        self.ai = AIPredictor()

        self.propagation = FreeSpacePropagation()

        self.link_budget = LinkBudget()


    def predict_grid(
        self,
        tower,
        environment="Urban"
    ):

        predictions = []

        step = 0.002


        for i in range(-25,26):

            for j in range(-25,26):

                lat = tower["lat"] + i*step
                lon = tower["lon"] + j*step


                distance = haversine_distance(
                    tower["lat"],
                    tower["lon"],
                    lat,
                    lon
                )

                # Skip points on top of the tower — they produce an
                # artificially perfect signal (green patch artefact).
                if distance < 0.05:
                    continue

                path_loss = self.propagation.path_loss(
                    distance,
                    tower["freq"]
                )


                received_power = self.link_budget.received_power(
                    path_loss
                )


                sample = {

                    "tower_lat": tower["lat"],
                    "tower_lon": tower["lon"],

                    "user_lat": lat,
                    "user_lon": lon,

                    "distance_km": distance,

                    "frequency": tower["freq"],

                    "tx_power": tower["power"],

                    "tower_height": tower["height"],

                    "antenna_gain": 17,

                    "environment": environment,

                    "building_density": 0.7,

                    "terrain_height": 30,

                    "shadow_fading": 8,

                    "rain_loss": 0.5,

                    "user_density": 400,

                    "traffic_load": 0.6,

                    "path_loss": path_loss,

                    "received_power": received_power
                }


                rsrp = self.ai.predict(sample)


                predictions.append({

                    "lat": lat,

                    "lon": lon,

                    "rsrp": rsrp
                })


        return predictions