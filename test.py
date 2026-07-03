from models.link_budget import LinkBudget
from models.signal import calculate_rsrp

lb = LinkBudget()

distance_km = 1.0

rsrp = calculate_rsrp(distance_km, lb)

print("RSRP at 1 km:", rsrp, "dBm")