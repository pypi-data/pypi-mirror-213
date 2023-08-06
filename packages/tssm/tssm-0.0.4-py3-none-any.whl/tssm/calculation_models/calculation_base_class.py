"""
Time series scaling module script for calculation model base class
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray

    from tssm.value_storage import DataStorage

    from .simultaneity_factor import SimultaneityFactor


class CalculationClass(ABC):
    """class to calculate new profile using a reference scaling profile"""

    __slots__ = "data", "simultaneity_factor", "one_2_many", "number_of_buildings"

    def __init__(self, values: DataStorage, simultaneity_factor: SimultaneityFactor, number_of_buildings: int, *, one_2_many: bool = True):
        """
        init of CalculationUsingAverageValues class\n
        :param values: ValueStorage to get original values from
        :param simultaneity_factor: simultaneity factor to be up-scaled
        :param number_of_buildings: number of buildings
        :param one_2_many: should the profile be scaled form one profile to many (True) or many to one (False)
        """
        self.data: DataStorage = values
        self.simultaneity_factor: SimultaneityFactor = simultaneity_factor
        self.one_2_many: bool = one_2_many
        self.simultaneity_factor.use = simultaneity_factor.old if one_2_many else 1 / simultaneity_factor.old
        self.number_of_buildings: int = number_of_buildings

    @abstractmethod
    def calculate(self, *, scaling_factor: float | None = None) -> tuple[NDArray[np.float64], SimultaneityFactor]:
        """function to calculate new scaled profile"""

    @abstractmethod
    def calculate_new_values(self) -> None:
        """
        Calculates the new value for each timestamp.
        """
