"""
script to create tssm from GUI data
"""
# pragma: no cover
from __future__ import annotations

import logging
from functools import partial
from typing import TYPE_CHECKING

from tssm import TimeSeriesScalingModule

if TYPE_CHECKING:
    from collections.abc import Callable



def data_2_results(data) -> tuple[TimeSeriesScalingModule, partial[[], None]] | tuple[TimeSeriesScalingModule, Callable[[], None]]:
    # test linear approach for day
    scaling = TimeSeriesScalingModule(data.option_number_buildings, data.option_simultaneity_factor)
    try:
        scaling.data.read_profile_from_csv_with_date(data.option_filename, data.option_column_load[1], data.option_column_date[1], separator=",", decimal=".")
    except ValueError:
        logging.exception("Error:")
    if data.aim_average:
        func = partial(scaling.calculate_using_average_values, data.option_period[0] + 1)
        return scaling, func
    if data.aim_normal:
        func = scaling.calculate_using_normal_distribution
        return scaling, func
    scaling.data.read_scaling_profile_from_csv(data.option_scaling_filename, data.option_scaling_column_load[1])
    if data.aim_scaling:
        func = partial(scaling.calculate_using_scaling_profile, period=data.option_period[0] + 1, same_sum=data.option_scale==0)
        return scaling, func
    func = scaling.calculate_using_scaling_and_normal_distribution
    return scaling, func
