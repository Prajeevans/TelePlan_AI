from abc import ABC, abstractmethod
import math


class PropagationModel(ABC):
    """
    Base class for all propagation models.
    """

    @abstractmethod
    def path_loss(self, distance_km: float, frequency_mhz: float) -> float:
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

    def path_loss(self, distance_km: float, frequency_mhz: float) -> float:

        if distance_km <= 0:
            distance_km = 0.001

        return (
            32.44
            + 20 * math.log10(distance_km)
            + 20 * math.log10(frequency_mhz)
        )


class OkumuraHataPropagation(PropagationModel):
    """
    Placeholder.

    Will be implemented later.
    """

    def path_loss(self, distance_km: float, frequency_mhz: float) -> float:
        raise NotImplementedError("Okumura-Hata model not implemented yet.")


class COST231Propagation(PropagationModel):
    """
    Placeholder.

    Will be implemented later.
    """

    def path_loss(self, distance_km: float, frequency_mhz: float) -> float:
        raise NotImplementedError("COST-231 model not implemented yet.")