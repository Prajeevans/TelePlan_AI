from models.path_loss import fspl
from models.link_budget import LinkBudget


def calculate_rsrp(distance_km, link_budget: LinkBudget):

    path_loss_db = fspl(distance_km, link_budget.frequency_mhz)

    rsrp_dbm = link_budget.received_power(path_loss_db)

    return rsrp_dbm