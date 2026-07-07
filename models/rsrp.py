class RSRPEngine:

    def __init__(self, resource_block_correction=3):

        self.correction = resource_block_correction


    def calculate(self, received_power):

        """
        Simplified RSRP estimation.

        received_power:
            Total received signal power (dBm)

        returns:
            RSRP (dBm)
        """

        rsrp = received_power - self.correction

        return rsrp


    def classify(self, rsrp):

        if rsrp >= -80:
            return "Excellent"

        elif rsrp >= -90:
            return "Good"

        elif rsrp >= -105:
            return "Fair"

        else:
            return "Poor"