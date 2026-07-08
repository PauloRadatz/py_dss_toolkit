from typing import Callable
from typing import Dict
from typing import Tuple
from typing import Union

import pandas as pd
from py_dss_interface import DSS

from .snapshot_utils import dataframe_to_column_records
from .voltages_nodal_utils import create_nodal_ll_voltage_dataframes
from .voltages_nodal_utils import create_nodal_smart_voltage_dataframes
from .voltages_nodal_utils import create_nodal_voltage_dataframes


def _undervoltage_overvoltage_from_vmags(
    vmags_df: pd.DataFrame, v_min: float, v_max: float
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    numeric = vmags_df.select_dtypes(include="number")
    undervoltage_violations_df = vmags_df[(numeric < v_min).any(axis=1)]
    overvoltage_violations_df = vmags_df[(numeric > v_max).any(axis=1)]
    return undervoltage_violations_df, overvoltage_violations_df


class VoltagesNodalViolations:
    def __init__(
        self,
        dss: DSS,
        connection_type_map: Union[Dict[str, str], Callable[[], Dict[str, str]], None] = None,
    ):
        self._dss = dss
        if not hasattr(self, "_raw_connection_type_map"):
            self._raw_connection_type_map = connection_type_map

        self.set_violation_voltage_ln_limits()

    @property
    def _connection_type_map(self) -> Dict[str, str]:
        m = self._raw_connection_type_map
        if callable(m):
            return m() or {}
        return m or {}

    def set_violation_voltage_ln_limits(self, v_min_pu: float = 0.95, v_max_pu: float = 1.05):
        self.v_min_pu = v_min_pu
        self.v_max_pu = v_max_pu

    @property
    def violation_voltage_ln_nodes(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Identifies and returns nodal voltage violations based on per-unit voltage limits.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]:
                - The first DataFrame contains all buses with at least one nodal voltage below the minimum per-unit limit (undervoltage violations).
                - The second DataFrame contains all buses with at least one nodal voltage above the maximum per-unit limit (overvoltage violations).

        Note:
            For each bus, all nodal voltages are checked.
            If any nodal voltage is less than ``v_min_pu``, the bus is included in the
            undervoltage DataFrame. If any is greater than ``v_max_pu``, it is included
            in the overvoltage DataFrame. Both DataFrames include all nodal voltages
            for the violating buses.
        """
        vmags_df, _ = create_nodal_voltage_dataframes(self._dss)
        return _undervoltage_overvoltage_from_vmags(vmags_df, self.v_min_pu, self.v_max_pu)

    @property
    def violation_voltage_ll_nodes(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Nodal voltage violations using line-to-line per-unit magnitudes per bus.

        Uses the same ``v_min_pu`` / ``v_max_pu`` as :meth:`set_violation_voltage_ln_limits`.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: ``(undervoltage_df, overvoltage_df)``.
            Same structure as :attr:`violation_voltage_ln_nodes`, but magnitudes are
            LL-based.
        """
        vmags_df, _ = create_nodal_ll_voltage_dataframes(self._dss)
        return _undervoltage_overvoltage_from_vmags(vmags_df, self.v_min_pu, self.v_max_pu)

    @property
    def violation_voltage_nodes(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Nodal voltage violations with per-bus LN or LL magnitudes (same selection as
        :attr:`py_dss_toolkit.results.SnapShot.VoltagesNodalSmart.voltage_nodes`).

        The returned DataFrames include a ``voltage_type`` column when present in the
        underlying magnitude frame.

        Uses the same ``v_min_pu`` / ``v_max_pu`` as :meth:`set_violation_voltage_ln_limits`.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: ``(undervoltage_df, overvoltage_df)``.
            Same structure as :attr:`violation_voltage_ln_nodes`; magnitudes follow
            per-bus LN/LL selection and may include a ``voltage_type`` column.
        """
        vmags_df, _ = create_nodal_smart_voltage_dataframes(self._dss, self._connection_type_map)
        return _undervoltage_overvoltage_from_vmags(vmags_df, self.v_min_pu, self.v_max_pu)

    @property
    def _violation_voltage_ln_nodes_records(self) -> dict:
        u_df, o_df = self.violation_voltage_ln_nodes
        return {
            "undervoltage": dataframe_to_column_records(u_df),
            "overvoltage": dataframe_to_column_records(o_df),
        }

    @property
    def _violation_voltage_ll_nodes_records(self) -> dict:
        u_df, o_df = self.violation_voltage_ll_nodes
        return {
            "undervoltage": dataframe_to_column_records(u_df),
            "overvoltage": dataframe_to_column_records(o_df),
        }

    @property
    def _violation_voltage_nodes_records(self) -> dict:
        u_df, o_df = self.violation_voltage_nodes
        return {
            "undervoltage": dataframe_to_column_records(u_df),
            "overvoltage": dataframe_to_column_records(o_df),
        }
