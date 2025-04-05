# -*- coding: utf-8 -*-
# @Author  : Iury Zanelato
# @Email   : iury.ribeirozanelato@gmail.com
# @File    : Same_Bus.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from dataclasses import dataclass, field
from typing import Tuple


class SameBus:

    def __init__(self, dss: DSS):
        self._dss = dss
        self._same_bus = pd.DataFrame()

    @property
    def same_bus(self) -> pd.DataFrame:
        return self.__check_same_bus()  # Todo - it should return a dataframe with the element names

    def __check_same_bus(self):
        elements = self._dss.circuit.elements_names

        for elem in elements:
            self._dss.circuit.set_active_element(elem)
            elem_name = self._dss.cktelement.name
            buses = self._dss.cktelement.bus_names
            if len(buses) > 1:
                bus1 = self._dss.cktelement.bus_names[0].split(".")[0]
                bus2 = self._dss.cktelement.bus_names[1].split(".")[0]

                if elem_name.split(".")[0] not in ["Vsource", "Capacitor", "Reactor"]:
                    if self._dss.cktelement.bus_names[0] == self._dss.cktelement.bus_names[1]:
                        print(f"Element: {elem_name} with the same bus1 {bus1} and bus2 {bus2}")

        # self._dss.text("solve")
        # elements
