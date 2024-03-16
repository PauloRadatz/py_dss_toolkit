# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : settings_utils.py
# @Software: PyCharm

from typing import List, Dict
from py_dss_interface import DSS
import pandas as pd


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
