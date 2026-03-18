# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Tuple

import pandas as pd
from py_dss_interface import DSS
from .snapshot_utils import create_currents_elements_records, create_currents_elements_dataframes


class Currents:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def _currents_element_mag_records(self) -> dict:
        return create_currents_elements_records(self._dss)[0]

    @property
    def _currents_element_ang_records(self) -> dict:
        return create_currents_elements_records(self._dss)[1]

    @property
    def _currents_element_norm_amps_records(self) -> dict:
        return create_currents_elements_records(self._dss)[3]

    @property
    def _currents_element_emerg_amps_records(self) -> dict:
        return create_currents_elements_records(self._dss)[4]

    @property
    def currents_elements(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return create_currents_elements_dataframes(self._dss)
