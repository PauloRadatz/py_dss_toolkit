# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : PowerFlowResults.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from dataclasses import dataclass, field
from typing import Tuple

from py_dss_tools.results.Voltages import Voltages
from py_dss_tools.results.Currents import Currents
from py_dss_tools.results.Powers import Powers


class StaticResults(Voltages, Currents, Powers):
    def __init__(self, dss: DSS):
        self._dss = dss
        Voltages.__init__(self, self._dss)
        Currents.__init__(self, self._dss)
        Powers.__init__(self, self._dss)
