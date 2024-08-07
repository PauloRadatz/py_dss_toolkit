# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : Monitor.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from dataclasses import dataclass, field
from typing import Optional, Dict
from py_dss_tools.dss_tools import DSSTools

class Monitor:
    def __init__(self, dss: DSS):
        self._dss = dss

    def monitor(self, name: str): # -> Optional[Dict[(str, str), pd.DataFrame]]:
        name = name.lower()
        if name not in [m.lower() for m in self._dss.monitors.names]:
            return None

        return self.__create_dataframe(name)

    def __create_dataframe(self, name: str):
        return DSSTools(self._dss).results.monitor_df(name)

