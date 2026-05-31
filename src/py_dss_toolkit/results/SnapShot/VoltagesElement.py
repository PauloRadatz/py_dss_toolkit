# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Tuple

import pandas as pd
from py_dss_interface import DSS

from .voltages_element_utils import (
    create_element_voltage_records,
    create_element_voltage_dataframes,
    create_element_voltage_records_loop,
    create_element_voltage_dataframes_loop,
)


class VoltagesElement:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def _voltages_element_mag_records(self) -> dict:
        return create_element_voltage_records(self._dss)[0]

    @property
    def _voltages_element_ang_records(self) -> dict:
        return create_element_voltage_records(self._dss)[1]

    @property
    def _voltages_element_mag_records_loop(self) -> dict:
        return create_element_voltage_records_loop(self._dss)[0]

    @property
    def _voltages_element_ang_records_loop(self) -> dict:
        return create_element_voltage_records_loop(self._dss)[1]

    @property
    def voltages_elements(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return create_element_voltage_dataframes(self._dss)

    @property
    def voltages_elements_loop(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Original loop-based implementation of :attr:`voltages_elements`.

        Kept for reference/fallback while migrating to ``dss.export.elem_voltages``;
        scheduled for removal once the new path is fully validated.
        """
        return create_element_voltage_dataframes_loop(self._dss)
