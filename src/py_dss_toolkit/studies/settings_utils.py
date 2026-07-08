# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : settings_utils.py
# @Software: PyCharm

from typing import Dict
from typing import List
from typing import Literal
from typing import Tuple
from typing import Union
from typing import get_args

import pandas as pd
from py_dss_interface import DSS

AlgorithmType = Literal["normal", "newton", "ncim"]
SnapshotModeType = Literal["snapshot", "snap"]
TimeSeriesModeType = Literal["daily", "yearly", "dutycycle"]
FaultModeType = Literal["faultstudy", "f", "fault"]


VALID_ALGORITHMS: List[str] = list(get_args(AlgorithmType))
VALID_SNAPSHOT_MODES: List[str] = list(get_args(SnapshotModeType))
VALID_TIMESERIES_MODES: List[str] = list(get_args(TimeSeriesModeType))
VALID_FAULT_MODES: List[str] = list(get_args(FaultModeType))


def validate_algorithm(algorithm: AlgorithmType) -> str:
    """Validate algorithm string.

    Args:
        algorithm: Algorithm string (case-insensitive): 'normal', 'newton', 'ncim'

    Returns:
        Validated algorithm string (lowercase)

    Raises:
        ValueError: If algorithm is not valid
    """
    if algorithm.lower() not in VALID_ALGORITHMS:
        raise ValueError(f"Invalid value for algorithm. Should be one of the following options: {VALID_ALGORITHMS}.")
    return algorithm.lower()


def validate_time(time: Tuple[Union[int, float], Union[int, float]]):
    if not (isinstance(time, (tuple, list)) and len(time) == 2 and all(isinstance(v, (float, int)) for v in time)):
        raise ValueError("Invalid time format. Expected a tuple or list with two numerical values.")


def validate_number(number: int):
    if number < 1:
        raise ValueError("Invalid number value. It should be greater than 0.")


def validate_stepsize(stepsize: Union[int, float]):
    if stepsize < 1:
        raise ValueError("Invalid stepsize value. It should be greater than 0.")


def validate_mode(mode: str, valid_modes: List[str]) -> str:
    """Validate mode string.

    Args:
        mode: Mode string (case-insensitive)
        valid_modes: List of valid mode values

    Returns:
        Validated mode string (lowercase)

    Raises:
        ValueError: If mode is not valid
    """
    if mode.lower() not in valid_modes:
        raise ValueError(f"Invalid value for mode. Should be one of the following options: {valid_modes}.")
    return mode.lower()


def check_mode(dss: DSS, valid_modes: List[str]) -> str:
    """Check current mode and set to default if not valid.

    Args:
        dss: DSS instance
        valid_modes: List of valid mode values

    Returns:
        Current or default mode string
    """
    current_mode = dss.text("get mode").lower()
    default_mode = valid_modes[0]

    if current_mode not in valid_modes:
        print(f"Simulation Mode changed to {default_mode}")
        dss.text(f"set mode={default_mode}")
        return default_mode

    return current_mode


def set_mode(dss: DSS, valid_modes: List[str], value: str) -> str:
    """Set the simulation mode.

    Args:
        dss: DSS instance
        valid_modes: List of valid mode values
        value: Mode string (case-insensitive)

    Returns:
        The validated mode string

    Raises:
        ValueError: If mode is not valid
    """
    validated_mode = validate_mode(value, valid_modes)
    dss.text(f"set mode={validated_mode}")
    return validated_mode


def get_settings(settings_dict: Dict):
    data = dict()
    for at, v in settings_dict.items():
        if at != "_dss":
            data[at.replace("_", "")] = v
    df = pd.DataFrame([data]).T
    df.columns = ["Settings"]
    return df
