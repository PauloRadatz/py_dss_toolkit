# -*- coding: utf-8 -*-
# @Author  : Iury Zanelato
# @Email   : iury.ribeirozanelato@gmail.com
# @File    : Load_Transformer.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Tuple


class LoadsTransformerVoltage:

    def __init__(self, dss: DSS):
        self._dss = dss
        self._load_transformer = pd.DataFrame()

    @property
    def loads_transformer_voltage_mismatch(self) -> pd.DataFrame:
        return self.__check_load_transformer()  # Todo - it should return a dataframe with the element names

    def __check_load_transformer(self):
        energymeter_voltage = dict()
        self._dss.transformers.first()
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
                    vll = vln
                elif num_wdg == 3:
                    self._dss.transformers.wdg = 2
                    vln = self._dss.transformers.kv
                    vll = 2 * vln

            energymeter_voltage[self._dss.transformers.name] = (round(vll, 2), round(vln, 2))
            self._dss.transformers.next()
        self._dss.text("solve")

        self._dss.meters.first()
        for _ in range(self._dss.meters.count):
            loads = self._dss.meters.all_pce_in_zone

            for load in loads:
                if load.split(".")[0].lower() == "load":
                    self._dss.circuit.set_active_element(load)
                    load_ph = self._dss.cktelement.num_phases

                    vll = energymeter_voltage[self._dss.meters.name][0]
                    vln = energymeter_voltage[self._dss.meters.name][1]

                    if load_ph == 3:
                        if round(self._dss.loads.kv, 2) != vll:
                            print(
                                f"\nLoad: {self._dss.loads.name} with kV {self._dss.loads.kv} but should be {energymeter_voltage[self._dss.meters.name][0]}")
                    elif load_ph == 1:
                        nodes = self._dss.cktelement.bus_names[0].split(".")[1:]

                        if ("1" in nodes and "2" in nodes) or ("1" in nodes and "3" in nodes) or (
                            "3" in nodes and "2" in nodes):
                            if round(self._dss.loads.kv, 2) != vll:
                                print(
                                    f"\nLoad: {self._dss.loads.name} with kV {self._dss.loads.kv} but should be {energymeter_voltage[self._dss.meters.name][0]}")
                        elif "1" in nodes or "2" in nodes or "3" in nodes:
                            if round(self._dss.loads.kv, 2) != vln:
                                print(
                                    f"\nLoad: {self._dss.loads.name} with kV {self._dss.loads.kv} but should be {energymeter_voltage[self._dss.meters.name][1]}")

        self._dss.meters.next()
