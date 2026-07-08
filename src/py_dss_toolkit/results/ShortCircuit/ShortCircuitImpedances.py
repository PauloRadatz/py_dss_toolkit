# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ShortCircuitImpedances.py
# @Software: PyCharm


import pandas as pd
from py_dss_interface import DSS


class ShortCircuitImpedances:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def _short_circuit_impedances_records(self) -> dict:
        return self._create_short_circuit_impedances_records()

    @property
    def short_circuit_impedances(self) -> pd.DataFrame:
        records = self._short_circuit_impedances_records
        df = pd.DataFrame.from_dict(records)
        df = df.set_index(["Bus Name"])
        return df

    def _create_short_circuit_impedances_records(self) -> dict:
        buses = self._dss.circuit.buses_names

        distance = list()
        r1_list = list()
        x1_list = list()
        r0_list = list()
        x0_list = list()
        for bus in buses:
            self._dss.circuit.set_active_bus(bus)
            zsc1 = self._dss.bus.zsc1
            zsc0 = self._dss.bus.zsc0

            distance.append(self._dss.bus.distance)
            r1_list.append(zsc1[0])
            x1_list.append(zsc1[1])
            r0_list.append(zsc0[0])
            x0_list.append(zsc0[1])

        return {
            "Bus Name": buses,
            "Distance (m?)": distance,
            "r1 (Ohm)": r1_list,
            "x1 (Ohm)": x1_list,
            "r0 (Ohm)": r0_list,
            "x0 (Ohm)": x0_list,
        }
