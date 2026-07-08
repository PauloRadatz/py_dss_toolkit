# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Tuple

import pandas as pd
from py_dss_interface import DSS

from .voltages_nodal_utils import create_nodal_ll_voltage_dataframes
from .voltages_nodal_utils import create_nodal_ll_voltage_records
from .voltages_nodal_utils import create_nodal_voltage_dataframes
from .voltages_nodal_utils import create_nodal_voltage_records


class VoltagesNodal:
    """Nodal voltages per bus from OpenDSS (line-to-neutral and line-to-line)."""

    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def _voltage_mag_ln_nodes_records(self) -> dict:
        return create_nodal_voltage_records(self._dss)[0]

    @property
    def _voltage_ang_ln_nodes_records(self) -> dict:
        return create_nodal_voltage_records(self._dss)[1]

    @property
    def _voltage_mag_ll_nodes_records(self) -> dict:
        return create_nodal_ll_voltage_records(self._dss)[0]

    @property
    def _voltage_ang_ll_nodes_records(self) -> dict:
        return create_nodal_ll_voltage_records(self._dss)[1]

    @property
    def voltage_ln_nodes(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Line-to-neutral per-unit nodal voltages (magnitude and angle) for every bus.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: ``(vmags_df, vangs_df)``, one row per bus,
            columns ``node1``, ``node2``, ``node3``, … Magnitudes in per-unit; angles in degrees.
        """
        return create_nodal_voltage_dataframes(self._dss)

    @property
    def voltage_ll_nodes(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Line-to-line per-unit nodal voltages (magnitude and angle) for every bus.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: ``(vmags_df, vangs_df)`` in the same
            layout as :attr:`voltage_ln_nodes`, but derived from ``pu_vll``.
        """
        return create_nodal_ll_voltage_dataframes(self._dss)
