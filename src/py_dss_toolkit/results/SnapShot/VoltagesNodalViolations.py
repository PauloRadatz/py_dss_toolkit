import pandas as pd
from py_dss_interface import DSS
from .voltages_nodal_utils import create_nodal_voltage_dataframes
from typing import Tuple

class VoltagesNodalViolations:
    def __init__(self, dss: DSS):
        self._dss = dss

        self.set_violation_voltage_ln_limits()

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

        Logic:
            - For each bus, all nodal voltages are checked.
            - If any nodal voltage is less than v_min_pu, the bus is included in the undervoltage violations DataFrame.
            - If any nodal voltage is greater than v_max_pu, the bus is included in the overvoltage violations DataFrame.
            - Both DataFrames include all nodal voltages for the violating buses.
        """
        vmags_df, _ = create_nodal_voltage_dataframes(self._dss)
        undervoltage_violations_df = vmags_df[(vmags_df < self.v_min_pu).any(axis=1)]

        overvoltage_violations_df = vmags_df[(vmags_df > self.v_max_pu).any(axis=1)]
        return undervoltage_violations_df, overvoltage_violations_df
