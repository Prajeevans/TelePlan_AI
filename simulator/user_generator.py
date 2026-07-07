import random


def generate_user():

    user = {

        # User location (Sri Lanka region)
        "lat": random.uniform(6.5, 9.5),

        "lon": random.uniform(79.5, 82.0),


        # User type
        "user_type": random.choice(
            [
                "mobile",
                "fixed",
                "IoT"
            ]
        ),


        # Device characteristics
        "device_category": random.choice(
            [
                "low_end",
                "mid_range",
                "high_end"
            ]
        ),


        # Traffic requirement (Mbps)
        "data_demand": round(
            random.uniform(0.5, 100),
            2
        )

    }

    return user