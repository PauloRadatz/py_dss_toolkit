# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : Powers.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from dataclasses import dataclass, field
from typing import Tuple
from py_dss_tools.dss_utils import DSSUtils


class Powers:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def powers_elements(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return self.__create_dataframe()

    def __create_dataframe(self):
        return DSSUtils(self._dss).results.circuit_p_q_dfs()
