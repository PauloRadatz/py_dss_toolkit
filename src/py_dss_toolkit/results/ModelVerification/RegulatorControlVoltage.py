# -*- coding: utf-8 -*-
# @Author  : Ferdinando Crispino
# @Email   : ferdinando.crispino@usp.br
# @File    : RegulatorControlVoltage.py
# @Software: PyCharm

import pandas as pd
import numpy as np
from py_dss_interface import DSS
from py_dss_toolkit.dss_tools.dss_tools import dss_tools

"""
checks if the regulator control voltage is the phase voltage

"""
class RegulatorControlVoltage:

    def __init__(self, dss: DSS):
        self._dss = dss
        self._regulatorControlVoltage = pd.DataFrame()
        dss_tools.update_dss(self._dss)

    @property
    def regulatorControlVoltage(self) -> pd.DataFrame:
        return self.__check_regulatorControlVoltage()  # Todo - it should return a dataframe with the element names

    def voltages_transformer(self, tr_name):
        self._dss.circuit.set_active_element(f"Transformer.{tr_name}")
        self._dss.transformers.name = tr_name
        bus_name = self._dss.bus.name
        tr_ph = self._dss.cktelement.num_phases
        vll = 0
        vln = 0
        if tr_ph == 3:
            self._dss.transformers.wdg = 2
            vll = self._dss.transformers.kv
            vln = vll / np.sqrt(3)
        elif tr_ph == 1:
            num_wdg = self._dss.transformers.num_windings
            if num_wdg == 2:
                self._dss.transformers.wdg = 2
                vln = self._dss.transformers.kv
                vll = vln * np.sqrt(3)
            elif num_wdg == 3:
                self._dss.transformers.wdg = 2
                vln = self._dss.transformers.kv
                vll = 2 * vln

        return  round(vll,3), round(vln,3), self._dss.transformers.is_delta, self._dss.bus.voltages

    def __check_regulatorControlVoltage(self):

        data = []  # list of problem found

        self._dss.regcontrols.first()
        for _ in range(self._dss.regcontrols.count):
            name_ctl = self._dss.regcontrols.name
            name_tr = self._dss.regcontrols.transformer
            pt_ratio = self._dss.regcontrols.pt_ratio
            vreg = self._dss.regcontrols.forward_vreg
            self._dss.regcontrols.next()

            vll, vln, delta, bus_voltages= self.voltages_transformer(name_tr)
            if delta == 1:
                v_ref = vll
            else:
                v_ref = vln

            # check bus voltage (voltage phase) and transformer voltage (voltage phase)
            bus1_voltage = np.sqrt(bus_voltages[0] ** 2 + bus_voltages[1] ** 2)/1000
            bus2_voltage = np.sqrt(bus_voltages[2] ** 2 + bus_voltages[3] ** 2)/1000
            bus3_voltage = np.sqrt(bus_voltages[4] ** 2 + bus_voltages[5] ** 2)/1000
            if round(bus1_voltage, 2) != round(vln, 2):
                print(f" Tensão do Regulador {bus1_voltage} diferente da tensão do bus {v_ref}")

            v_reg = (vreg * pt_ratio)/1000
            if (v_ref * 0.8) > v_reg or v_reg > (v_ref * 1.2):
                print(f"Regulator: {name_ctl} control voltage error: set {v_reg} voltage ref is {v_ref}.")
                data.append([name_ctl, vreg, pt_ratio, v_reg, v_ref])

        df_data = pd.DataFrame(data, columns=["element_name", "vreg", "ptratio", "kv_set", "kv_ref"])
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

    result_1 = RegulatorControlVoltage(dss).regulatorControlVoltage  # To get results.
    print("No problem added")
    print(result_1)

    # Set wrong voltage control
    dss.text("edit Regcontrol.creg1a ptratio=10")
    result_1 = RegulatorControlVoltage(dss).regulatorControlVoltage  # To get results.
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
    result_1 = RegulatorControlVoltage(dss).regulatorControlVoltage  # To get results.
    print(result_1)
