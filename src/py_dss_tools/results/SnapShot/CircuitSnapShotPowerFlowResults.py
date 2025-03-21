# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from py_dss_interface import DSS
import pandas as pd

class CircuitSnapShotPowerFlowResults:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def circuit_summary(self) -> pd.DataFrame:
        return self.__create_dataframe()

    def __create_dataframe(self):
        p_feeder_kw = -self._dss.circuit.total_power[0]
        q_feeder_kvar = -self._dss.circuit.total_power[1]
        p_losses_feeder_kw = self._dss.circuit.losses[0] / 1000.0
        q_losses_feeder_kvar = self._dss.circuit.losses[1] / 1000.0
        max_v_pu = max(self._dss.circuit.buses_vmag_pu)
        min_v_pu = min(self._dss.circuit.buses_vmag_pu)

        data = {
            'P feeder (kW)': [p_feeder_kw],
            'Q feeder (kvar)': [q_feeder_kvar],
            'P losses (kW)': [p_losses_feeder_kw],
            'Q losses (kvar)': [q_losses_feeder_kvar],
            'max voltage (pu)': [max_v_pu],
            'min voltage (pu)': [min_v_pu]
        }

        df = pd.DataFrame(data)
        df = df.T.rename(columns={0: 'Results'})

        return df

