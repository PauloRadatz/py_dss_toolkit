# -*- coding: utf-8 -*-
# @Author  : Iury Zanelato
# @Email   : iury.ribeirozanelato@gmail.com
# @File    : Isolated.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from dataclasses import dataclass, field
from typing import Tuple

class Isolated:

    def __init__(self, dss: DSS):
        self._dss = dss
        self._isolated = pd.DataFrame()
    @property
    def isolated(self) -> pd.DataFrame:
        return self.check_isolated()
    def check_isolated(self):
        branches_isolated = self._dss.topology.all_isolated_branches
        loads_isolated = self._dss.topology.all_isolated_loads

        for branch in branches_isolated:
            self._dss.circuit.set_active_element(branch)
            name = self._dss.cktelement.name
            if len(self._dss.cktelement.bus_names) == 2:
                bus1 = self._dss.cktelement.bus_names[0].split(".")[0]
                bus2 = self._dss.cktelement.bus_names[1].split(".")[0]

                print(f"{name} bus1: {bus1} bus2: {bus2}")
            else:
                bus1 = self._dss.cktelement.bus_names[0].split(".")[0]
                print(f"{name} bus1: {bus1}")

        for load in loads_isolated:
            self._dss.circuit.set_active_element(load)
            name = self._dss.cktelement.name
            bus1 = self._dss.cktelement.bus_names[0].split(".")[0]

            print(f"{name} bus1: {bus1}")

        self._dss.text("solve")
        branches_isolated
        loads_isolated
