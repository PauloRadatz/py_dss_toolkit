# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ShortCircuitImpedances.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from dataclasses import dataclass, field
from typing import Tuple


class ShortCircuitImpedances:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def short_circuit_impedances(self) -> pd.DataFrame:
        return self.__short_circuit_impedances()

    def __short_circuit_impedances(self) -> pd.DataFrame:
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

        dict_to_df = dict()
        dict_to_df["Bus Name"] = buses
        dict_to_df["Distance (m?)"] = distance
        dict_to_df["r1 (Ohm)"] = r1_list
        dict_to_df["x1 (Ohm)"] = x1_list
        dict_to_df["r0 (Ohm)"] = r0_list
        dict_to_df["x0 (Ohm)"] = x0_list

        df = pd.DataFrame.from_dict(dict_to_df)
        df = df.set_index(["Bus Name"])

        return df
