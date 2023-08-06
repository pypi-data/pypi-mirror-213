"""
general utils package
"""
from tssm.utils.calc_indexes import calculate_indexes
from tssm.utils.dict_casting import from_dict, to_dict
from tssm.utils.errors import FactorAmountError, NoScalingProfileError
from tssm.utils.period import Period
from tssm.utils.cast_2_same_sum import scale_scaling_profile_2_same_sum
from tssm.utils.cast_input_2_period import cast_input_2_period
