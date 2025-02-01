# -*- coding: utf-8 -*-
# @Author  : Arthur Lopes Morais Arantes
# @Email   : arthureletricauftm@gmail.com
# Date     : 19/01/2025
# @File    : SystemPhotovoltaic.py
# @Software: PyCharm
import math

from py_dss_interface import DSS
import pandas as pd
import warnings as ws


class CapacitorData:

    def __init__(self, dss: DSS):
        self._dss = dss
        self._Load_ShapeData__ = pd.DataFrame()

    @property
    def Capacitor_Data(self) -> pd.DataFrame:
        return self.CapacitorData__() #Todo - it should return a dataframe with the element names

    def CapacitorData__(self):

        dss.capacitors.first()
        data = []
        Teste = True
        warning = ""

        while True:

            kv_cap   = dss.capacitors.kv
            kv_cap_new   = kv_cap
            kvar_cap = dss.capacitors.kvar
            kvar_cap_new = kvar_cap

            bus = str(dss.text(f"? Capacitor.{dss.capacitors.name}.bus1"))
            bus_name, bus_node = bus.split(".")[0:1], bus.split(".")[1:]
            #Armazena os nós sem ser aterrado ou isolado
            bus_node_filter = ([node_bus for node_bus in bus_node if node_bus in ['1', '2', '3']])
            len_bus_node_filter =  len(bus_node_filter)
            #Verifica a quantidade de fases
            phases = str(dss.text(f"? Capacitor.{dss.capacitors.name}.phases"))
            phasesnodes_new  = phases

            if kv_cap < 0:
                Teste = False
                kv_cap_new = (-1)*kv_cap
            if kvar_cap < 0:
                Teste = False
                warning = "If kVAR < 0, it must be modeled like a Reactor"
                ws.warn(warning, UserWarning)
                kvar_cap_new = f"{(-1)*kvar_cap} or If kVAR < 0, it must be modeled like a Reactor"

            # CHECK DIFFERENCE BETWEEN BUS NODE AND PHASES
            if phases != len_bus_node_filter:
                    Teste = False
                    phasesnodes_new = len_bus_node_filter
                    warning = f"Other solution: Number of nodes are right. Change phase to {len_bus_node_filter}"
                    ws.warn(warning, UserWarning)

            if dss.capacitors.next() == 0:
                break

            if Teste == False:
                data.append([self._dss.capacitors.name,kv_cap,  kv_cap_new,kvar_cap, kvar_cap_new, phases, phasesnodes_new])

        return pd.DataFrame(data, columns=["Capacitors", "kv set", "kv new", "kvar set", "kvar new", "phases", "phases new"])

if __name__ == '__main__':
    import os
    import pathlib
    dss = DSS()
    script_path = os.path.dirname(os.path.abspath(__file__))

    dss_file = pathlib.Path(script_path).joinpath("..", "..", "..", "..", "examples", "feeders", "RITQ1305", "DU_1_Master_391_ITQ_RITQ1305.dss")
    dss.text(f"compile [{dss_file}]")
    #dss_dir_chosen = r"C:\Users\arthu\Downloads\RITQ1305" #path chosen
    #dss_name_chosen = "DU_1_Master_391_ITQ_RITQ1305.dss"
    #dss_file = pathlib.Path(script_path).joinpath(dss_dir_chosen, dss_name_chosen)
    #dss.dssinterface.clear_all()
    #dss.text(f"set datapath = {dss_dir_chosen}")
    # remove meters if present in dss files
    for name in dss.meters.names:
        dss.text(f"disable energymeter.{name}")


    dss.text("New Capacitor.CAP_165BC00536460911 bus1=MT3674868240264866IT05.1.2.3 kvar=-600.0 kv=-13800.0 phases=2 conn=Delta")

    result_1 = CapacitorData(dss).Capacitor_Data
    print (result_1)

