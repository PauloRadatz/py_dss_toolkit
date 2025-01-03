# -*- coding: utf-8 -*-
# @Author  : Ferdinando Crispino
# @Email   : ferdinando.crispino@usp.br
# @File    : CapacitorControlVoltage.py
# @Software: PyCharm

import pandas as pd
import numpy as np
from py_dss_interface import DSS
from py_dss_tools.dss_tools.dss_tools import dss_tools

"""
checks if the regulator control voltage is the phase voltage

"""
class CapacitorControlVoltage:

    def __init__(self, dss: DSS):
        self._dss = dss
        self._capacitorControlVoltage = pd.DataFrame()
        dss_tools.update_dss(self._dss)

    @property
    def capacitorControlVoltage(self) -> pd.DataFrame:
        return self.__check_regulatorControlVoltage()  # Todo - it should return a dataframe with the element names

    def __check_regulatorControlVoltage(self):

        data = []  # list of problem found
        ck_err = False
        self._dss.capcontrols.first()
        for _ in range(self._dss.capcontrols.count):
            name_ctl = self._dss.regcontrols.name
            pt_ratio = self._dss.capcontrols.pt_ratio
            on = self._dss.capcontrols.on_setting
            off = self._dss.capcontrols.off_setting
            cap_kv = self._dss.capacitors.kv
            delta =  self._dss.capacitors.is_delta

            self._dss.capcontrols.next()

            if delta == 1:
                v_ref = cap_kv
            else:
                v_ref = cap_kv / np.sqrt(3)

            v_reg_on = (on * pt_ratio) / 1000
            v_reg_off = (off * pt_ratio) / 1000

            if (v_ref * 0.8) > v_reg_on or v_reg_on > (v_ref * 1.2):
                print(f"CapControl: {name_ctl} Control voltage error: Set Voltage ON {v_reg_on} voltage ref is {v_ref}.")
                ck_err = True
            if (v_ref * 0.8) > v_reg_off or v_reg_off > (v_ref * 1.2):
                print(f"CapControl: {name_ctl} Control voltage error: Set voltage OFF {v_reg_off} voltage ref is {v_ref}.")
                ck_err = True

            if ck_err:
                data.append([name_ctl, on, off, pt_ratio, v_reg_on, v_reg_off, v_ref])
                ck_err = False

        df_data = pd.DataFrame(data, columns=["element_name", "ON", "OFF", "ptratio", "On_set", "off_set", "kv_ref"])
        df_data.drop_duplicates(subset='element_name', keep='first', inplace=True)
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

    result_1 = CapacitorControlVoltage(dss).capacitorControlVoltage  # To get results.
    print("No problem added")
    print(result_1)

    # Set wrong voltage control
    dss.text("edit Regcontrol.creg1a ptratio=10")
    result_1 = CapacitorControlVoltage(dss).capacitorControlVoltage  # To get results.
    print(result_1)

 # verification for real circuit
    #dss_dir = "C:/Users/Ferdinando/Desktop/curso_opendss/1924"
    #dss_name = "DU_1_Master_40_MSU_1924.dss"

    #dss_dir = "C:/Users/Ferdinando/Desktop/curso_opendss/ITQ/RITQ1305"
    #dss_name = "DU_1_Master_391_ITQ_RITQ1305.dss"

    dss_dir = "C:/Users/Ferdinando/Desktop/curso_opendss/RAPA1303"
    dss_name = "DU_1_Master_391_APA_RAPA1303.dss"
    dss_file = pathlib.Path(script_path).joinpath(dss_dir, dss_name)

    dss.dssinterface.clear_all()
    dss.text(f"compile [{dss_file}]")
    result_1 = CapacitorControlVoltage(dss).capacitorControlVoltage  # To get results.
    print(result_1)
