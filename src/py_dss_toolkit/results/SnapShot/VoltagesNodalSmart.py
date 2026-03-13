# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Callable, Dict, Tuple, Union

import pandas as pd
from py_dss_interface import DSS

from py_dss_toolkit.results.SnapShot.voltages_nodal_utils import (
    create_nodal_smart_voltage_dataframes,
)


class VoltagesNodalSmart:
    def __init__(
        self,
        dss: DSS,
        connection_type_map: Union[Dict[str, str], Callable[[], Dict[str, str]], None] = None,
    ):
        self._dss = dss
        self._raw_connection_type_map = connection_type_map

    @property
    def _connection_type_map(self) -> Dict[str, str]:
        m = self._raw_connection_type_map
        if callable(m):
            return m() or {}
        return m or {}

    @property
    def voltage_nodes(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Auto-selects LN or LL per-unit voltage per bus.

        Uses *connection_type_map* (pre-computed via a single BFS pass) to
        decide per bus.  Buses mapped to ``'ll'`` get line-to-line voltages;
        all others get line-to-neutral voltages.

        Returns
        -------
        (vmags_df, vangs_df)
            Per-unit voltage magnitudes and angles, one row per bus.
        """
        return create_nodal_smart_voltage_dataframes(self._dss, self._connection_type_map)
