"""
functions to convert class to dict and back
"""
from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd

VAL_2_VAL: dict[type : Callable[[any], any]] = {str: str, np.int64: int, np.int32: int, np.float32: float, int: int, float: float, tuple: list}


def to_dict(obj: object) -> dict:
    """
    This function converts the class variables to a dictionary so it can be saved in a JSON format.
    Currently, it can handle np.ndarray, list, set, str, int, float, tuple

    Parameters
    ----------
    obj: object
        object that is converted to dict

    Returns
    -------
        json dict
    """

    # get all variables in class
    if hasattr(obj, "__slots__"):
        variables: list[str] = list(obj.__slots__)
    else:
        variables = [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__")]

    # initiate dictionary
    dictionary: dict = {}

    # populate dictionary
    for key in variables:
        var = getattr(obj, key)
        if isinstance(var, (int, bool, float, str)):
            dictionary[key] = var
            continue

        if isinstance(var, list):
            dictionary[key] = [[VAL_2_VAL[type(val_i)](val_i) for val_i in val] if isinstance(val, list) else VAL_2_VAL[type(val)](val) for val in var]
            continue

        if isinstance(var, tuple):
            dictionary[key] = {"value": list(var), "type": "tuple"}
            continue

        if isinstance(var, range):
            dictionary[key] = {"value": {"start": var.start, "stop": var.stop, "step": var.step}, "type": "range"}
            continue

        if isinstance(var, np.ndarray):
            dictionary[key] = {"value": var.astype(np.float64).tolist(), "type": "np.ndarray"}
            continue

        if isinstance(var, pd.Series):
            dictionary[key] = {"value": var.astype(np.float64).to_json(), "type": "pd.Series"}
            continue

        if isinstance(var, pd.DataFrame):
            dictionary[key] = {"value": var.astype(np.float64).to_json(), "type": "pd.DataFrame"}
            continue

        if isinstance(var, dict):
            # note that this can cause problems whenever self.key contains values that or not int, bool, float or str
            dictionary[key] = var
            continue

        if isinstance(var, set):
            dictionary[key] = {"value": list(var), "type": "set"}
            continue

        # for all obj-defined classes
        if hasattr(var, "to_dict"):
            dictionary[key] = var.to_dict()

    return dictionary


def from_dict(obj: object, dictionary: dict) -> None:
    """
    This function converts the dictionary values to the class attributes.
    Currently, it can handle np.ndarray, list, set, str, int, float, tuple, pygfunction.Borehole
    and classes within GHEtool.

    Parameters
    ----------
    dictionary
        Dictionary with all the attributes of the class

    Returns
    -------
    None
    """
    for key, value in dictionary.items():
        if not hasattr(obj, key):
            continue

        # for all obj-defined classes
        if hasattr(getattr(obj, key), "from_dict"):
            print(getattr(obj, key))
            getattr(obj, key).from_dict(value)
            continue

        if isinstance(value, (int, bool, float, str, list)):
            setattr(obj, key, value)
            continue

        if isinstance(value, dict):
            # note that this can mean that the value is a dictionary, or it is a np.ndarray, set or tuple
            keys = value.keys()
            if len(keys) == 2 and "type" in keys and "value" in keys:
                type_i = value["type"]
                _value = value["value"]

                if type_i == "set":
                    setattr(obj, key, set(_value))
                    continue
                if type_i == "np.ndarray":
                    setattr(obj, key, np.array(_value))
                    continue
                if type_i == "range":
                    setattr(obj, key, range(_value["start"], _value["stop"], _value["step"]))
                    continue
                if type_i == "tuple":
                    setattr(obj, key, tuple(_value))
                    continue
                if type_i == "pd.DataFrame":
                    setattr(obj, key, pd.read_json(_value))
                    continue
                if type_i == "pd.Series":
                    setattr(obj, key, pd.read_json(_value))
                    continue
            # normal dictionary
            setattr(obj, key, value)
