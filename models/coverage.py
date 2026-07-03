def estimate_radius(power_dbm, frequency_mhz):
    """Simple heuristic to estimate coverage radius based on power and frequency"""
    if frequency_mhz < 1000:
        return 5000

    elif frequency_mhz < 2500:
        return 3000

    elif frequency_mhz < 4000:
        return 1500

    else:
        return 800