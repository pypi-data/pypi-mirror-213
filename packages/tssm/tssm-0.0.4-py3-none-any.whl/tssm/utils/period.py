"""
define period enum
"""
from enum import Enum, auto, unique


@unique
class Period(Enum):
    """Period index"""

    YEARLY = auto()  # 1
    MONTHLY = auto()  # 2
    WEEKLY = auto()  # 3
    DAILY = auto()  # 4
    HOURLY = auto()  # 5
    HOURLY_AND_MONTHLY = auto()  # 6
