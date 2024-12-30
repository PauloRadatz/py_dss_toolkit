# -*- coding: utf-8 -*-
# @Author  : Iury Zanelato
# @Email   : iury.ribeirozanelato@gmail.com
# @File    : Load_Transformer.py
# @Software: PyCharm
# ---------------------------------------------
# @Alter   : Ferdinando Crispino
# @Date    : 2024-11-18
# @Email   : ferdinando.crispino@usp.br

import math
from py_dss_interface import DSS
import pandas as pd
import numpy as np
import os
import pathlib
from py_dss_tools.dss_tools.dss_tools import dss_tools


class LoadsTransformerVoltage:
    """
    Used to verify if the voltages of the loads declared in dss files are correct according to
    transformers connection voltages.
    return name of loads with problem and presents the voltage values that must be corrected.
    """
    def __init__(self, dss: DSS):
        self._dss = dss
        self._load_transformer = pd.DataFrame()

        dss_tools.update_dss(self._dss)

    @property
    def loads_transformer_voltage_mismatch(self) -> pd.DataFrame:
        return self.__check_load_transformer()  # Todo - it should return a dataframe with the element names

    def __first_element(self):
        """ Retorna o primeiro bus do circuito
            Navega pela topologia da rede de um bus qualquer ate o inicio do circuito
        """
        self._dss.topology.first()
        self._dss.topology.forward_branch()
        while True:
            index_branch = self._dss.topology.backward_branch()
            if index_branch:  # chegou no inicio do alimentador (Vsource)
                self._dss.topology.forward_branch() # avançar para obter o primeiro elemento
                print(self._dss.topology.branch_name)
                return self._dss.topology.branch_name

    def __check_load_transformer(self):

        # remove meters if present in dss files
        for name in self._dss.meters.names:
            self._dss.text(f"disable energymeter.{name}")

        energymeter_voltage = dict()
        self._dss.transformers.first()
        data = []  # list of problem found

        #first_elem = self.__first_element()
        dss_tools.model.add_line_in_vsource(add_meter=True)
        kv_base = self._dss.vsources.base_kv

        # Add energymeter in the first element because have cases where load not connected a transformers.
        #self._dss.text(f"new energymeter.{first_elem} element={first_elem} terminal=1")

        if self._dss.vsources.phases == 1:
            vll = kv_base * math.sqrt(3)
            vln = kv_base
        else:
            vll = kv_base
            vln = kv_base / math.sqrt(3)

        self._dss.meters.first()  # exist only one meter here
        energymeter_voltage[self._dss.meters.name] = (round(vll, 2), round(vln, 2))

        # Add an energymeyter for each of the transformers
        for _ in range(self._dss.transformers.count):
            # 1 - Get buses
            # 2 - for in transformers
            # 3 - Bank? Vll 3ph

            self._dss.text(f"new energymeter.{self._dss.transformers.name} "
                           f"element=transformer.{self._dss.transformers.name} terminal=1")

            self._dss.circuit.set_active_element(f"transformer.{self._dss.transformers.name}")
            tr_ph = self._dss.cktelement.num_phases

            if tr_ph == 3:
                self._dss.transformers.wdg = 2
                vll = self._dss.transformers.kv
                vln = self._dss.transformers.kv / np.sqrt(3)

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

            energymeter_voltage[self._dss.transformers.name] = (round(vll, 2), round(vln, 2))
            self._dss.transformers.next()

        self._dss.text("solve")

        self._dss.meters.first()
        #print(f"Meters: {self._dss.meters.count}")
        for _ in range(self._dss.meters.count):

            loads = self._dss.meters.all_pce_in_zone
            # print(f"Meter: {self._dss.meters.name}")
            # print(loads)
            for load in loads:

                if load.split(".")[0].lower() == "load":

                    self._dss.circuit.set_active_element(load)
                    load_ph = self._dss.cktelement.num_phases

                    vll = energymeter_voltage[self._dss.meters.name][0]
                    vln = energymeter_voltage[self._dss.meters.name][1]

                    if load_ph == 3:
                        if round(self._dss.loads.kv, 2) != vll:
                            data.append([self._dss.loads.name, self._dss.loads.kv,
                                         energymeter_voltage[self._dss.meters.name][0]])
                            print(
                                f"\nLoad three-phase: {self._dss.loads.name} with kV={self._dss.loads.kv} "
                                f"but should be {energymeter_voltage[self._dss.meters.name][0]}")
                    elif load_ph == 1:
                        nodes = self._dss.cktelement.bus_names[0].split(".")[1:]

                        if (("1" in nodes and "2" in nodes) or ("1" in nodes and "3" in nodes) or
                            ("3" in nodes and "2" in nodes)):
                            if round(self._dss.loads.kv, 2) != vll:
                                data.append([self._dss.loads.name, self._dss.loads.kv,
                                             energymeter_voltage[self._dss.meters.name][0]])
                                print(
                                    f"\nLoad bi-phase: {self._dss.loads.name} with kV={self._dss.loads.kv} "
                                    f"but should be {energymeter_voltage[self._dss.meters.name][0]}")
                        elif "1" in nodes or "2" in nodes or "3" in nodes:
                            if round(self._dss.loads.kv, 2) != vln:
                                data.append([self._dss.loads.name, self._dss.loads.kv,
                                             energymeter_voltage[self._dss.meters.name][1]])
                                print(
                                    f"\nLoad single-phase: {self._dss.loads.name} with kV={self._dss.loads.kv} "
                                    f"but should be {energymeter_voltage[self._dss.meters.name][1]}")

            self._dss.meters.next()

        return pd.DataFrame(data, columns=["Load", "kV_set", "kV_use"])


if __name__ == '__main__':

    dss = DSS()
    script_path = os.path.dirname(os.path.abspath(__file__))
    """
    dss_file = pathlib.Path(script_path).joinpath("..", "..","..", "..", "examples", "feeders", "123Bus", "IEEE123Master.dss")
    bus_coords = pathlib.Path(script_path).joinpath("..", "..","..", "..", "examples", "feeders", "123Bus", "buscoords.dat")

    dss.text(f"compile [{dss_file}]")
    dss.text(f"buscoords buscoords.dat")

    # Set kV problem in Load single-phase MT
    dss.text("edit Load.S9a kv=2.6")

    # Set kV problem in Load bi-phase MT
    dss.text("edit Load.S76a kv=2.6")

    # Set kV problem in Load three-phase MT
    dss.text("edit Load.S47 kv=2.6")
    """

    dss_dir = "C:/Users/Ferdinando/Desktop/curso_opendss/1928"
    dss_name = "DU_1_Master_40_MSU_1928.dss"
    dss_file = pathlib.Path(script_path).joinpath(dss_dir, dss_name)

    """
    dss.dssinterface.clear_all()
    dss.text(f"set datapath = {dss_dir}")
    with open(os.path.join(dss_file), 'r') as file:
        for line_dss in file:
            if not(line_dss.startswith('!') or line_dss.startswith('\n') or line_dss.lower().startswith('clear') ):
                dss.text(line_dss.strip('\n') )
            if 'calc' in line_dss:
                break

    """

    dss.text(f"compile [{dss_file}]")

    # Set kV problem in Load three-phase MT
    dss.text("edit Load.MT_063e29c511f31e2a93994610808d5bd7faf1c22b45ae184ba92e3c87aa0dcbb2_M1 kv=2.6")

    # Set kV problem in Load single-phase BT
    dss.text("edit Load.BT_0004b1c7191bc272c7d5898e0b6ba3b6e702bcceaf1b787875430b8baea5dc07_M1 kv=0.35")
    dss.text("edit Load.BT_00428e0b986b2ab894be8e07ce5da321b4916372b44cdf3b079f97bb6a5b3fa1_M1 kv=0.44")
    dss.text("edit Load.MT_8d44761e28a883954dc5753e40333eed6a06b3cadf01ee0cf1e003ec39f5e315_M1 kv=1.35")

    dss.text("edit Load.MT_a134781d570656b755ac35a63d7acbf7cae23ef5b03d8872ec291ef1a0b1da60_M1 kv=0.35")

    # Set kV problem in Load bi-phase BT

    # Set kV problem in Load three-phase BT



    result = LoadsTransformerVoltage(dss).loads_transformer_voltage_mismatch
    print(result)




