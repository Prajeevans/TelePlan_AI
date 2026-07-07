import random


def generate_weather():

    weather_type = random.choice(
        [
            "Clear",
            "Light Rain",
            "Heavy Rain",
            "Storm"
        ]
    )


    if weather_type == "Clear":

        rain_rate = 0

        rain_loss = 0


    elif weather_type == "Light Rain":

        rain_rate = random.uniform(
            1,
            5
        )

        rain_loss = random.uniform(
            0.1,
            0.5
        )


    elif weather_type == "Heavy Rain":

        rain_rate = random.uniform(
            10,
            30
        )

        rain_loss = random.uniform(
            0.5,
            2
        )


    else:  # Storm

        rain_rate = random.uniform(
            30,
            80
        )

        rain_loss = random.uniform(
            2,
            5
        )


    return {

        "weather_type": weather_type,

        # Rain intensity (mm/hr)
        "rain_rate": round(
            rain_rate,
            2
        ),

        # Additional attenuation in dB
        "rain_loss": round(
            rain_loss,
            3
        )
    }