# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : Circuit.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from dataclasses import dataclass, field
from typing import Tuple
from py_dss_tools.dss_tools import DSSTools


class Circuit:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def circuit_summary(self) -> pd.DataFrame:
        return self.__create_dataframe()

    def __create_dataframe(self):
        return DSSTools(self._dss).results.circuit_summary_df()

