import random


def generate_environment():

    environment_type = random.choice(
        [
            "Urban",
            "Suburban",
            "Rural"
        ]
    )


    if environment_type == "Urban":

        building_density = random.uniform(
            0.7,
            1.0
        )

        terrain_height = random.uniform(
            0,
            100
        )

        shadow_fading = random.uniform(
            8,
            12
        )


    elif environment_type == "Suburban":

        building_density = random.uniform(
            0.3,
            0.7
        )

        terrain_height = random.uniform(
            20,
            200
        )

        shadow_fading = random.uniform(
            5,
            8
        )


    else:  # Rural

        building_density = random.uniform(
            0,
            0.3
        )

        terrain_height = random.uniform(
            50,
            500
        )

        shadow_fading = random.uniform(
            2,
            5
        )


    return {

        "type": environment_type,

        "building_density": round(
            building_density,
            3
        ),

        "terrain_height": round(
            terrain_height,
            2
        ),

        "shadow_fading": round(
            shadow_fading,
            2
        )
    }