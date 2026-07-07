from models.path_loss import fspl
from models.link_budget import LinkBudget


def calculate_rsrp(distance_km, link_budget: LinkBudget, tx_power_dbm=None, frequency_mhz=None):

    freq = frequency_mhz if frequency_mhz is not None else link_budget.frequency_mhz
    path_loss_db = fspl(distance_km, freq)

    rsrp_dbm = link_budget.received_power(path_loss_db, tx_power_dbm=tx_power_dbm)

    return rsrp_dbm