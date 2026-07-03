class LinkBudget:

    def __init__(self):

        # Transmitter
        self.tx_power_dbm = 43
        self.tx_antenna_gain_dbi = 17
        self.tx_cable_loss_db = 2
        self.tx_connector_loss_db = 0.5

        # Environment
        self.shadow_fading_db = 8
        self.rain_attenuation_db = 1
        self.misc_loss_db = 1

        # Receiver
        self.rx_antenna_gain_dbi = 0
        self.rx_cable_loss_db = 0

        # Frequency (MHz)
        self.frequency_mhz = 3500

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

    def received_power(self, path_loss_db):

        total_gain = self.tx_power_dbm + self.tx_antenna_gain_dbi + self.rx_antenna_gain_dbi

        total_loss = self.total_losses(path_loss_db)

        return total_gain - total_loss