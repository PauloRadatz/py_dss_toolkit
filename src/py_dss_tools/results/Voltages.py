# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : VoltageLNNodes.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from dataclasses import dataclass, field
from typing import Tuple
from py_dss_tools.dss_utils import DSSUtils


class Voltages:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def voltage_ln_nodes(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return self.__create_dataframe()

    def __create_dataframe(self):
        return DSSUtils(self._dss).results.circuit_vmag_vang_dfs()
