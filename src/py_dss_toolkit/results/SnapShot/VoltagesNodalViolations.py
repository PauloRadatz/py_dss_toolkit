import pandas as pd
from py_dss_interface import DSS
from .voltages_nodal_utils import create_nodal_voltage_dataframes

class VoltagesNodalViolations:
    def __init__(self, dss: DSS):
        self._dss = dss

        self.set_violation_voltage_ln_limits()

    def set_violation_voltage_ln_limits(self, v_min_pu: float = 0.95, v_max_pu: float = 1.05):
        self.v_min_pu = v_min_pu
        self.v_max_pu = v_max_pu

    @property
    def violation_voltage_ln_nodes(self) -> pd.DataFrame:
        """
        Returns a DataFrame with buses that have at least one nodal voltage outside [v_min_pu, v_max_pu].
        The DataFrame includes all nodal voltages for those buses.
        """
        vmags_df, _ = create_nodal_voltage_dataframes(self._dss)
        mask = (vmags_df < self.v_min_pu) | (vmags_df > self.v_max_pu)
        buses_with_violations = mask.any(axis=1)
        violations_df = vmags_df[buses_with_violations]
        return violations_df
