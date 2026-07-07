import pandas as pd
import random
import math
import os
import sys
from pathlib import Path

# Add project root directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.propagation import FreeSpacePropagation
from models.link_budget import LinkBudget
from models.rsrp import RSRPEngine
from utils.calculations import haversine_distance


# Number of samples
SAMPLES = 100000


def generate_dataset():

    propagation = FreeSpacePropagation()
    link_budget = LinkBudget()
    rsrp_engine = RSRPEngine()


    data = []


    for _ in range(SAMPLES):

        # Random tower location
        tower_lat = random.uniform(6.5, 9.5)
        tower_lon = random.uniform(79.5, 82.0)


        # Random user location
        user_lat = random.uniform(6.5, 9.5)
        user_lon = random.uniform(79.5, 82.0)


        # Tower parameters
        height = random.randint(20, 80)

        tx_power = random.randint(30, 46)

        frequency = random.choice(
            [
                700,
                900,
                1800,
                2100,
                3500
            ]
        )


        distance = haversine_distance(
            tower_lat,
            tower_lon,
            user_lat,
            user_lon
        )


        # Avoid zero distance
        if distance < 0.01:
            distance = 0.01


        # Path loss
        path_loss = propagation.path_loss(
            distance,
            frequency
        )


        # Received power
        rx_power = (
            tx_power
            + 17
            - path_loss
        )


        # RSRP approximation
        rsrp = rsrp_engine.calculate(
            rx_power
        )


        data.append({

            "tower_lat": tower_lat,

            "tower_lon": tower_lon,

            "user_lat": user_lat,

            "user_lon": user_lon,

            "distance_km": distance,

            "tower_height": height,

            "tx_power": tx_power,

            "frequency": frequency,

            "rsrp": rsrp

        })


    return pd.DataFrame(data)



if __name__ == "__main__":


    df = generate_dataset()


    os.makedirs(
        "../data",
        exist_ok=True
    )


    df.to_csv(
        "../data/rsrp_dataset.csv",
        index=False
    )


    print("Dataset Generated!")
    print(df.head())