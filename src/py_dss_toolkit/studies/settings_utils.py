# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : settings_utils.py
# @Software: PyCharm

from typing import Dict
from typing import List, Tuple

import pandas as pd
from py_dss_interface import DSS


def validate_algorithm(algorithm: str):
    algorithm_list = ["Normal".lower(), "Newton".lower(), "NCIM".lower()]
    if algorithm.lower() not in algorithm_list:
        raise ValueError(f'Invalid value for algorithm. Should be one of the following options: {algorithm_list}.')


def validate_time(time: Tuple[float, float]):
    if not (isinstance(time, (tuple, list)) and len(time) == 2 and all(
        isinstance(v, (float, int)) for v in time)):
        raise ValueError("Invalid time format. Expected a tuple or list with two numerical values.")


def validate_number(number: int):
    if number < 1:
        raise ValueError("Invalid number value. It should be greater than 0.")


def validate_stepsize(stepsize: float):
    if stepsize < 1:
        raise ValueError("Invalid stepsize value. It should be greater than 0.")


def validate_mode(mode: str, modes: List[str]):
    if mode.lower() not in modes:
        raise ValueError(f'Invalid value for mode. Should be one of the following options: {modes}.')


def check_mode(dss: DSS, modes: List[str]):
    mode = modes[0]
    if dss.text("get mode").lower() not in modes:
        print(f"Simulation Mode changed to {modes[0]}")
        dss.text(f"set mode={mode}")

    return mode


def set_mode(dss: DSS, modes: List[str], value: str):
    if value.lower() not in modes:
        raise ValueError(f'Invalid value for mode. Should be {modes}.')
    dss.text(f"set mode={value.lower()}")
    return value.lower()


def get_settings(settings_dict: Dict):
    data = dict()
    for at, v in settings_dict.items():
        if at != "_dss":
            data[at.replace("_", "")] = v
    df = pd.DataFrame([data]).T
    df.columns = ["Settings"]
    return df
