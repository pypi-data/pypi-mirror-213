"""Module providingFunction printing python version."""
from tssm.utils import Period
from tssm.time_series_scaling_module import TimeSeriesScalingModule
import tssm.calculation_models.profile_generation as profile_generation

DAILY = Period.DAILY
YEARLY = Period.YEARLY
MONTHLY = Period.MONTHLY
WEEKLY = Period.WEEKLY
HOURLY = Period.HOURLY
HOURLY_AND_MONTHLY = Period.HOURLY_AND_MONTHLY
TSSM = TimeSeriesScalingModule
