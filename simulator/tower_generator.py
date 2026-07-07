import random


def generate_tower():

    tower = {

        "id": random.randint(1000, 9999),

        # Sri Lanka approximate region
        "lat": random.uniform(6.5, 9.5),

        "lon": random.uniform(79.5, 82.0),


        # Tower parameters
        "height": random.choice(
            [
                20,
                30,
                40,
                50,
                60
            ]
        ),


        "tx_power": random.choice(
            [
                40,
                43,
                46
            ]
        ),


        "frequency": random.choice(
            [
                700,
                900,
                1800,
                2100,
                3500
            ]
        ),


        "antenna_gain": random.choice(
            [
                15,
                17,
                20
            ]
        )
    }


    return tower