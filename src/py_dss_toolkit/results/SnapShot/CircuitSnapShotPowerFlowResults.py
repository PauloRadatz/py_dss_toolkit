# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from py_dss_interface import DSS
import pandas as pd

class CircuitSnapShotPowerFlowResults:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def _summary_records(self) -> dict:
        return self._create_summary_records()

    @property
    def summary_df(self) -> pd.DataFrame:
        data = self._summary_records
        df = pd.DataFrame(data)
        df = df.T.rename(columns={0: 'Results'})
        return df

    def _create_summary_records(self) -> dict:
        return {
            'P feeder (kW)': [-self._dss.circuit.total_power[0]],
            'Q feeder (kvar)': [-self._dss.circuit.total_power[1]],
            'P losses (kW)': [self._dss.circuit.losses[0] / 1000.0],
            'Q losses (kvar)': [self._dss.circuit.losses[1] / 1000.0],
            'max voltage (pu)': [max(self._dss.circuit.buses_vmag_pu)],
            'min voltage (pu)': [min(self._dss.circuit.buses_vmag_pu)],
        }

