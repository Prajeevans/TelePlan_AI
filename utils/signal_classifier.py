def signal_quality(rx_power):

    if rx_power >= -70:
        return "Excellent", "green"

    elif rx_power >= -85:
        return "Good", "yellow"

    elif rx_power >= -100:
        return "Fair", "orange"

    else:
        return "Poor", "red"