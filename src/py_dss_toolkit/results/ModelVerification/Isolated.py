# -*- coding: utf-8 -*-
# @Author  : Iury Zanelato
# @Email   : iury.ribeirozanelato@gmail.com
# @File    : Isolated.py
# @Software: PyCharm

import pandas as pd
from py_dss_interface import DSS


class Isolated:

    def __init__(self, dss: DSS):
        self._dss = dss
        self._isolated = pd.DataFrame()

    @property
    def isolated(self) -> pd.DataFrame:
        return self.__check_isolated()  # Todo - it should return a dataframe with the element names

    def __check_isolated(self):
        self._dss.text("solve")

        branches_isolated = self._dss.topology.all_isolated_branches
        loads_isolated = self._dss.topology.all_isolated_loads

        # Clear NONE to not get into the for loop
        if "NONE" == branches_isolated[0]:
            branches_isolated.remove("NONE")
        if "NONE" == loads_isolated[0]:
            loads_isolated.remove("NONE")

        data = []

        for branch in branches_isolated:
            self._dss.circuit.set_active_element(branch)
            name = self._dss.cktelement.name.lower()
            if len(self._dss.cktelement.bus_names) == 2:
                bus1 = self._dss.cktelement.bus_names[0].split(".")[0]
                bus2 = self._dss.cktelement.bus_names[1].split(".")[0]

            else:
                bus1 = self._dss.cktelement.bus_names[0].split(".")[0]
                bus2 = ""

            data.append([name, bus1, bus2])

        for load in loads_isolated:
            self._dss.circuit.set_active_element(load)
            name = self._dss.cktelement.name.lower()
            bus1 = self._dss.cktelement.bus_names[0].split(".")[0]
            bus2 = ""

            data.append([name, bus1, bus2])

        return pd.DataFrame(data, columns=["element name", "bus1", "bus2"])

if __name__ == '__main__':
    import os
    import pathlib

    dss = DSS()

    script_path = os.path.dirname(os.path.abspath(__file__))
    dss_file = pathlib.Path(script_path).joinpath("..", "..","..", "..", "examples", "feeders", "123Bus", "IEEE123Master.dss")
    bus_coords = pathlib.Path(script_path).joinpath("..", "..","..", "..", "examples", "feeders", "123Bus", "buscoords.dat")

    dss.text(f"compile [{dss_file}]")
    dss.text(f"buscoords buscoords.dat")
    dss.text("new energymeter.m element=line.l115")

    result_1 = Isolated(dss).isolated  # To get results.
    print("No problem added")
    print(result_1)

    # Add problem
    dss.text("edit Line.L112 bus2=open")

    result_2 = Isolated(dss).isolated
    print("\nproblem added")
    print(result_2)
