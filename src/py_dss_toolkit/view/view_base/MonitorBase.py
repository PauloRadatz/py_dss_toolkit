# -*- coding: utf-8 -*-
# @Time    : 8/27/2024 4:36 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : MonitorBase.py
# @Software: PyCharm

from py_dss_interface import DSS
from py_dss_toolkit.results.TimeSeries.TimeSeriesPowerFlowResults import TimeSeriesPowerFlowResults
from typing import Optional

class MonitorBase:

    def __init__(self, dss: DSS, results: Optional[TimeSeriesPowerFlowResults]):
        self._dss = dss
        self._results = results

    def _check_v_monitor(self, name):
        if name.lower() not in self._dss.monitors.names:
            raise ValueError(f"{name} is not a monitor")
        self._dss.monitors.name = name
        m_mode = self._dss.monitors.mode
        vi_polar = self._dss.text(f"? monitor.{name}.vipolar").lower()
        if m_mode != 0:
            error_message = f'Invalid monitor mode. It should be 0 not {m_mode}'
            raise ValueError(error_message)
        if vi_polar in ["false", "no"]:
            raise ValueError(f'Invalid monitor vipolar. It should be True or Yes not {vi_polar}')

    def _organize_v_results(self, name):
        self._dss.monitors.name = name
        element = self._dss.monitors.element
        terminal = self._dss.monitors.terminal
        self._dss.circuit.set_active_element(element)
        elem_num_phases = self._dss.cktelement.num_phases
        elem_num_conductors = self._dss.cktelement.num_conductors
        if terminal == 1:
            elem_nodes = self._dss.cktelement.node_order[: elem_num_phases]
            bus = self._dss.cktelement.bus_names[0].split(".")[0]
            self._dss.circuit.set_active_bus(bus)
            v_base = self._dss.bus.kv_base * 1000.0
        elif terminal == 2:
            elem_nodes = self._dss.cktelement.node_order[elem_num_conductors: elem_num_conductors + elem_num_phases]
        else:
            raise ValueError(f'terminal=3 not implemented')
        return elem_nodes, v_base

    def _check_p_monitor(self, name):
        if name.lower() not in self._dss.monitors.names:
            raise ValueError(f"{name} is not a monitor")
        self._dss.monitors.name = name
        m_mode = self._dss.monitors.mode
        p_polar = self._dss.text(f"? monitor.{name}.ppolar").lower()
        if m_mode != 1:
            raise ValueError(f'Invalid monitor mode. It should be 1 not {m_mode}')
        if p_polar in ["true", "yes"]:
            raise ValueError(f'Invalid monitor ppolar. It should be True or Yes not {p_polar}')

    def _organize_p_results(self, name):
        self._dss.monitors.name = name
        element = self._dss.monitors.element
        terminal = self._dss.monitors.terminal
        self._dss.circuit.set_active_element(element)
        elem_num_phases = self._dss.cktelement.num_phases
        elem_num_conductors = self._dss.cktelement.num_conductors
        if terminal == 1:
            elem_nodes = self._dss.cktelement.node_order[: elem_num_phases]
        elif terminal == 2:
            elem_nodes = self._dss.cktelement.node_order[elem_num_conductors: elem_num_conductors + elem_num_phases]
        else:
            raise ValueError(f'terminal=3 not implemented')
        return elem_nodes
