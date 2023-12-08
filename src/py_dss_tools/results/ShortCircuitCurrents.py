# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ShortCircuitImpedances.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from dataclasses import dataclass, field
from typing import Tuple


class ShortCircuitCurrents:
    def __init__(self, dss: DSS):
        self._dss = dss

    def delete_short_circuit_test(self):
        pass
