import random


def generate_traffic():

    # Network load condition
    traffic_condition = random.choice(
        [
            "Low",
            "Medium",
            "High",
            "Peak"
        ]
    )


    if traffic_condition == "Low":

        user_density = random.uniform(
            10,
            100
        )

        traffic_load = random.uniform(
            0.1,
            0.3
        )


    elif traffic_condition == "Medium":

        user_density = random.uniform(
            100,
            500
        )

        traffic_load = random.uniform(
            0.3,
            0.6
        )


    elif traffic_condition == "High":

        user_density = random.uniform(
            500,
            1000
        )

        traffic_load = random.uniform(
            0.6,
            0.85
        )


    else:  # Peak

        user_density = random.uniform(
            1000,
            3000
        )

        traffic_load = random.uniform(
            0.85,
            1.0
        )


    return {

        "traffic_condition": traffic_condition,

        # Number of active users per km²
        "user_density": round(
            user_density,
            2
        ),

        # Network utilization percentage
        "traffic_load": round(
            traffic_load,
            3
        )
    }