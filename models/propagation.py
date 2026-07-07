from abc import ABC, abstractmethod
import math


class PropagationModel(ABC):
    """
    Base class for all propagation models.
    """

    @abstractmethod
    def path_loss(self, distance_km: float, frequency_mhz: float, **kwargs) -> float:
        """
        Returns path loss in dB.
        """
        pass


class FreeSpacePropagation(PropagationModel):
    """
    Free Space Path Loss (FSPL)

    Equation:

    FSPL(dB) = 32.44
               + 20log10(distance_km)
               + 20log10(frequency_mhz)

    Assumptions:
    - Perfect line of sight
    - No buildings
    - No terrain obstruction
    - No atmospheric losses
    """

    def path_loss(self, distance_km: float, frequency_mhz: float, **kwargs) -> float:

        if distance_km <= 0:
            distance_km = 0.001

        return (
            32.44
            + 20 * math.log10(distance_km)
            + 20 * math.log10(frequency_mhz)
        )


class OkumuraHataPropagation(PropagationModel):

    def __init__(
        self,
        base_height=30,
        mobile_height=1.5,
        environment="urban"
    ):
        self.base_height = base_height
        self.mobile_height = mobile_height
        self.environment = environment.lower()

    def path_loss(self, distance_km, frequency_mhz, base_height=None, **kwargs):
        if frequency_mhz < 150 or frequency_mhz > 1500:
            raise ValueError(
                "Okumura-Hata model is valid only for 150-1500 MHz"
            )
            
        if distance_km <= 0:
            distance_km = 0.001

        hb = base_height if base_height is not None else self.base_height
        hm = self.mobile_height
        f = frequency_mhz
        d = distance_km

        # Mobile antenna correction factor
        a_hm = (
            (1.1 * math.log10(f) - 0.7) * hm
            - (1.56 * math.log10(f) - 0.8)
        )

        # Urban Path Loss
        path_loss = (
            69.55
            + 26.16 * math.log10(f)
            - 13.82 * math.log10(hb)
            - a_hm
            + (44.9 - 6.55 * math.log10(hb))
            * math.log10(d)
        )

        # Environment correction
        if self.environment == "suburban":
            path_loss -= (
                2 * (math.log10(f / 28)) ** 2
                + 5.4
            )

        elif self.environment == "rural":
            path_loss -= (
                4.78 * (math.log10(f)) ** 2
                - 18.33 * math.log10(f)
                + 40.94
            )

        return path_loss


class COST231Propagation(PropagationModel):
    """
    Placeholder.

    Will be implemented later.
    """

    def path_loss(self, distance_km: float, frequency_mhz: float, **kwargs) -> float:
        raise NotImplementedError("COST-231 model not implemented yet.")