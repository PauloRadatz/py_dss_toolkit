# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Tuple

import pandas as pd
from py_dss_interface import DSS
from .voltages_nodal_utils import create_nodal_voltage_dataframes


class VoltagesNodal:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def voltage_ln_nodes(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return create_nodal_voltage_dataframes(self._dss)
