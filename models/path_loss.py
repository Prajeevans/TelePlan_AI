import math

# free space path loss (FSPL) and log-distance path loss models 
def fspl(distance_km, frequency_mhz):
    """
    Free Space Path Loss (FSPL)

    L = 32.44 + 20log10(d) + 20log10(f)
    """

    if distance_km <= 0:
        distance_km = 0.001  # avoid log(0)

    return (
        32.44
        + 20 * math.log10(distance_km)
        + 20 * math.log10(frequency_mhz)
    )


def log_distance_path_loss(distance_km, frequency_mhz, path_loss_exponent=3.5):
    """
    Log-distance path loss model (more realistic than FSPL)
    
    L = FSPL + 10 * n * log10(d)
    """

    fspl_value = fspl(1, frequency_mhz)  # reference at 1 km baseline

    return fspl_value + 10 * path_loss_exponent * math.log10(max(distance_km, 0.001))