# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com


import pandas as pd
import numpy as np
from py_dss_interface import DSS
from py_dss_toolkit.dss_tools.dss_tools import dss_tools

"""
checks if the regulator control voltage is the phase voltage

"""
class RegulatorkVA:

    def __init__(self, dss: DSS):
        self._dss = dss
        dss_tools.update_dss(self._dss)

    @property
    def regulator_kva(self) -> pd.DataFrame:
        return self.__check_regulator_kva()

    def __check_regulator_kva(self):

        data = []  # list of problem found

        self._dss.regcontrols.first()
        for _ in range(self._dss.regcontrols.count):
            name_ctl = self._dss.regcontrols.name
            name_tr = self._dss.regcontrols.transformer

            self._dss.circuit.set_active_element(f"Transformer.{name_tr}")
            self._dss.transformers.name = name_tr
            tr_ph = self._dss.cktelement.num_phases

            tr_kva = self._dss.transformers.kva

            if tr_ph == 3:
                if tr_kva < 3000:
                    data.append([name_ctl, name_tr, tr_kva, 3000])
            elif tr_ph == 1:
                if tr_kva < 1000:
                    data.append([name_ctl, name_tr, tr_kva, 1000])

            self._dss.regcontrols.next()
        df_data = pd.DataFrame(data, columns=["Regulator", "Transformer", "kVA", "Expects kVA Greater than"])
        return df_data

if __name__ == '__main__':
    import os
    import pathlib

    dss = DSS()

    script_path = os.path.dirname(os.path.abspath(__file__))
    dss_file = pathlib.Path(script_path).joinpath("..", "..", "..", "..", "examples", "feeders", "123Bus",
                                                  "IEEE123Master.dss")
    bus_coords = pathlib.Path(script_path).joinpath("..", "..", "..", "..", "examples", "feeders", "123Bus",
                                                    "buscoords.dat")

    dss.text(f"compile [{dss_file}]")
    dss.text(f"buscoords buscoords.dat")
    dss.text("new energymeter.m element=line.l115")

    result_1 = RegulatorkVA(dss).regulator_kva  # To get results.
    print("No problem added")
    print(result_1)

    print("\nAdd problem")
    dss.text("edit transformer.reg2a kva=10")
    result_1 = RegulatorkVA(dss).regulator_kva   # To get results.
    print(result_1)


