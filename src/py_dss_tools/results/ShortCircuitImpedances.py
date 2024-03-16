# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ShortCircuitImpedances.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from dataclasses import dataclass, field
from typing import Tuple
from py_dss_tools.dss_tools import DSSTools


class ShortCircuitImpedances:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def short_circuit_impedances(self) -> pd.DataFrame:
        return self.__short_circuit_impedances()

    def __short_circuit_impedances(self) -> pd.DataFrame:
        return DSSTools(self._dss).results.short_circuit_impedances()
