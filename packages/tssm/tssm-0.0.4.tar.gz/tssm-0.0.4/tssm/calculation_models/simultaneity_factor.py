"""
Time series scaling module script for simultaneity factor base class
"""
from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING

import numpy as np

from tssm.utils.dict_casting import from_dict, to_dict

if TYPE_CHECKING:
    from numpy.typing import NDArray


class SimultaneityFactor:  # pylint: disable=too-few-public-methods
    """class to store old, new and during calculation used simultaneity factor"""

    __slots__ = ("old", "use", "new")

    def __init__(self, old: float):
        """
        init of class

        Parameters
        ----------
        old: float
            old simultaneity factor
        """
        self.old: float = old
        self.use: float = 0
        self.new: NDArray[np.float64] = field(default_factory=lambda: np.zeros(0))

    def to_dict(self) -> dict:
        """
        casts class to dictionary

        Returns
        -------
            dictionary
        """
        return to_dict(self)

    def from_dict(self, dictionary: dict) -> None:
        """
        sets class values from dictionary

        Parameters
        ----------
        dictionary: dict
            dictionary containing class variables

        Returns
        -------
            None
        """
        from_dict(self, dictionary)
