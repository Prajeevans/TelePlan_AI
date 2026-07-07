import models.config as c
from models.config import *

class LinkBudget:

    def __init__(self):

        # Transmitter
        self.tx_power_dbm = c.DEFAULT_TX_POWER
        self.tx_antenna_gain_dbi = c.TX_ANTENNA_GAIN
        self.tx_cable_loss_db = c.TX_CABLE_LOSS
        self.tx_connector_loss_db = c.TX_CONNECTOR_LOSS

        # Environment losses
        self.shadow_fading_db = c.SHADOW_FADING
        self.rain_attenuation_db = c.RAIN_ATTENUATION
        self.misc_loss_db = c.MISC_LOSS

        # Receiver
        self.rx_antenna_gain_dbi = c.RX_ANTENNA_GAIN
        self.rx_cable_loss_db = c.RX_CABLE_LOSS

    def total_losses(self, path_loss_db):

        return (
            path_loss_db
            + self.tx_cable_loss_db
            + self.tx_connector_loss_db
            + self.shadow_fading_db
            + self.rain_attenuation_db
            + self.misc_loss_db
            + self.rx_cable_loss_db
        )

    def received_power(self, path_loss_db, tx_power_dbm=None):

        tx_power = tx_power_dbm if tx_power_dbm is not None else self.tx_power_dbm
        total_gain = tx_power + self.tx_antenna_gain_dbi + self.rx_antenna_gain_dbi

        total_loss = self.total_losses(path_loss_db)

        return total_gain - total_loss