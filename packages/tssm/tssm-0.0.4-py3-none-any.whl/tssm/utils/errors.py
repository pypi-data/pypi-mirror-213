"""
define tssm errors
"""

class FactorAmountError(ValueError):
    """Error raised if the number of factors did not match"""

    def __init__(self, to_less: bool):
        super().__init__(f"{'Less' if to_less else 'More'} factors than periods")


class NoScalingProfileError(ValueError):
    """Error raised if no scaling profile is selected"""

    def __init__(self):
        super().__init__("No scaling profile selected")