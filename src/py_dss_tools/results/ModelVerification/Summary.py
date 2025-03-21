# -*- coding: utf-8 -*-
# @Author  : Iury Zanelato
# @Email   : iury.ribeirozanelato@gmail.com
# @File    : Summary.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Tuple

class Summary:
    def __init__(self, dss: DSS):
        self._dss = dss
        self._summary = pd.DataFrame()
    @property
    def summary(self):
        return self.__create_dataframe()

    def __round_x(self, y, x: int = 2):
        return round(y, x)

    def __create_dataframe(self):
        summary_dict = dict()
        self._dss.text("set mode=snapshot")
        self._dss.text("solve")

        summary_dict["Status"] = "Solved" if self._dss.solution.converged else "Not Solved"
        v_array = np.array(self._dss.circuit.buses_vmag_pu)
        v_array = v_array[v_array > 0.1]
        v_max = self.__round_x(v_array.max())
        v_min = self.__round_x(v_array.min())
        summary_dict["Max pu. Voltage"] = v_max
        summary_dict["Min pu. Voltage"] = v_min
        summary_dict["Good Voltage?"] = "Yes" if (v_min > 0.7 and v_max < 1.2) else "No"
        total_p = self.__round_x(-self._dss.circuit.total_power[0])
        total_q = self.__round_x(-self._dss.circuit.total_power[1])
        total_p_losses = self.__round_x(self._dss.circuit.losses[0] / 1000.0)
        summary_dict["Total P kW"] = self.__round_x(total_p)
        summary_dict["Total Q kVAr"] = self.__round_x(total_q)
        summary_dict["P Losses %"] = self.__round_x(100.0 * total_p_losses / total_p) if total_p > 0 else "NAN"
        x = self._dss.topology.all_isolated_branches
        if "NONE" in x:
            x.remove("NONE")
        if x:
            summary_dict["Num. Isolated Branches"] = len(x)
        else:
            summary_dict["Num. Isolated Branches"] = 0
        # summary_dict["Loop?"] = "Yes" if dss.topology_looped_branch() > 0 else "No"

        summary_dict["Num. Total Branches"] = self._dss.pdelements.count
        self._dss.circuit.set_active_element("vsource.source")
        p = -1 * np.array(self._dss.cktelement.powers[0:6:2])

        summary_dict["PA Circuit %"] = self.__round_x(p[0] / total_p) * 100.0 if total_p > 0 else "NAN"
        summary_dict["PB Circuit %"] = self.__round_x(p[1] / total_p) * 100.0 if total_p > 0 else "NAN"
        summary_dict["PC Circuit %"] = self.__round_x(p[2] / total_p) * 100.0 if total_p > 0 else "NAN"

        km_mv_lines = 0
        km_lv_lines = 0
        self._dss.lines.first()
        for _ in range(self._dss.lines.count):

            bus = self._dss.lines.bus1

            self._dss.circuit.set_active_bus(bus)

            if 4 not in self._dss.bus.nodes:
                km_mv_lines = km_mv_lines + self._dss.lines.length

            else:
                km_lv_lines = km_lv_lines + self._dss.lines.length

            self._dss.lines.next()

        summary_dict["Lines MV (km)"] = self.__round_x(km_mv_lines)
        summary_dict["Lines LV (km)"] = self.__round_x(km_lv_lines)

        summary_dict["Num. Tran"] = self._dss.transformers.count

        summary_dict["Num. Loads"] = self._dss.loads.count / 2

        max_load_kw = 0
        max_load_name = None
        self._dss.loads.first()
        for _ in range(self._dss.loads.count):
            if self._dss.loads.kw > max_load_kw:
                max_load_kw = self._dss.loads.kw
                max_load_name = self._dss.loads.name

            self._dss.loads.next()

        summary_dict["Max name of One Load"] = max_load_name
        summary_dict["Max kW of One Load"] = max_load_kw

        tr_c = list()
        self._dss.transformers.first()
        for _ in range(self._dss.transformers.count):
            self._dss.circuit.set_active_element(f"transformer.{self._dss.transformers.name}")

            p = sum(self._dss.cktelement.powers[:int(len(self._dss.cktelement.powers) / 2): 2])
            p_n = self._dss.transformers.kva

            tr_c.append(p / p_n * 100)

            self._dss.transformers.next()

        summary_dict["Loading max % transformers"] = np.max(tr_c) if len(tr_c) > 0 else "NAN"
        return pd.DataFrame(summary_dict, index=[0])
