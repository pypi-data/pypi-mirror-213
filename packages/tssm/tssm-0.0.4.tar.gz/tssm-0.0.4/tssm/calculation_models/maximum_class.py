"""
script for maximum class
"""


class Maximum:  # pylint: disable=too-few-public-methods
    """class to store maximum value and index"""

    __slots__ = ("value", "idx")

    def __init__(self, value: float, idx: int):
        self.value: float = value
        self.idx: int = idx
