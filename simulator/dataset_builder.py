import pandas as pd
import random
import os
import sys
sys.path.append(os.getcwd())

from tower_generator import generate_tower
from user_generator import generate_user
from environment_generator import generate_environment
from weather_generator import generate_weather
from traffic_generator import generate_traffic

from models.propagation import FreeSpacePropagation
from models.link_budget import LinkBudget
from models.rsrp import RSRPEngine
from utils.calculations import haversine_distance


SAMPLES = 100000


def build_dataset():

    propagation = FreeSpacePropagation()
    link_budget = LinkBudget()
    rsrp_engine = RSRPEngine()


    dataset = []


    for i in range(SAMPLES):

        # Generate tower
        tower = generate_tower()


        # Generate user
        user = generate_user()


        # Environment information
        environment = generate_environment()


        # Weather condition
        weather = generate_weather()


        # Network traffic
        traffic = generate_traffic()


        # Distance calculation
        distance = haversine_distance(
            tower["lat"],
            tower["lon"],
            user["lat"],
            user["lon"]
        )


        # Propagation calculation

        path_loss = propagation.path_loss(
            distance,
            tower["frequency"]
        )


        received_power = (
            tower["tx_power"]
            + tower["antenna_gain"]
            - path_loss
            - weather["rain_loss"]
            - environment["shadow_fading"]
        )


        rsrp = rsrp_engine.calculate(
            received_power
        )


        dataset.append({

            "tower_lat":
                tower["lat"],

            "tower_lon":
                tower["lon"],


            "user_lat":
                user["lat"],

            "user_lon":
                user["lon"],


            "distance_km":
                distance,


            "frequency":
                tower["frequency"],


            "tx_power":
                tower["tx_power"],


            "tower_height":
                tower["height"],


            "antenna_gain":
                tower["antenna_gain"],


            "environment":
                environment["type"],


            "building_density":
                environment["building_density"],


            "terrain_height":
                environment["terrain_height"],


            "shadow_fading":
                environment["shadow_fading"],


            "rain_loss":
                weather["rain_loss"],


            "user_density":
                traffic["user_density"],


            "traffic_load":
                traffic["traffic_load"],


            "path_loss":
                path_loss,


            "received_power":
                received_power,


            "rsrp":
                rsrp
        })


        if i % 10000 == 0:
            print(
                f"{i}/{SAMPLES} samples generated"
            )


    return pd.DataFrame(dataset)



if __name__ == "__main__":


    df = build_dataset()


    os.makedirs(
        "data",
        exist_ok=True
    )


    df.to_csv(
        "data/telecom_dataset.csv",
        index=False
    )


    print("\nDataset generation completed!")
    print(df.head())
    print(df.shape)