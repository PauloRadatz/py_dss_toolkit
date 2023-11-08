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


class StaticResults(Voltages):
    def __init__(self, dss: DSS):
        self._dss = dss
        Voltages.__init__(self, self._dss)
