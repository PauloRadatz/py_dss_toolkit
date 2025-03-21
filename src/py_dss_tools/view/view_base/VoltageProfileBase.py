# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : VoltageProfileBase.py
# @Software: PyCharm

from py_dss_interface import DSS
from py_dss_tools.results.SnapShot.SnapShotPowerFlowResults import SnapShotPowerFlowResults
from typing import Optional

class VoltageProfileBase:

    def __init__(self, dss: DSS, results: Optional[SnapShotPowerFlowResults]):
        self._dss = dss
        self._results = results

    def _check_energymeter(self):
        if self._dss.meters.count == 0:
            raise ValueError(f'One enerymeter should exist to plot the voltage profile.')
        elif self._dss.meters.count > 1:
            count_enabled = 0
            for m in self._dss.meters.names:
                self._dss.circuit.set_active_element(f"energymeter.{m}")
                if self._dss.cktelement.is_enabled:
                    count_enabled += 1

            if count_enabled == 0:
                raise ValueError(f'At least one enerymeter should be enabled to plot the voltage profile.')
            elif count_enabled > 1:
                raise ValueError(f'Only one enerymeter should be enabled to plot the voltage profile.')

    def _prepare_results(self):
        df = self._results.voltage_ln_nodes[0]
        buses = [bus.lower().split(".")[0] for bus in self._dss.circuit.buses_names]
        distances = self._dss.circuit.buses_distances
        sections = list()
        elements_list = self._dss.circuit.elements_names
        for element in elements_list:
            if element.split(".")[0].lower() in ["line", "reactor"]:
                self._dss.circuit.set_active_element(element)
                if self._dss.cktelement.is_enabled:
                    sections.append(
                        (self._dss.cktelement.bus_names[0].lower().split(".")[0],
                         self._dss.cktelement.bus_names[1].lower().split(".")[0]))
        return buses, df, distances, sections
