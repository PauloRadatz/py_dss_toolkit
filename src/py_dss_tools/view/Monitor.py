# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : Monitor.py
# @Software: PyCharm

import pandas as pd
from typing import Dict
import matplotlib.pyplot as plt
from typing import Optional, Union, Tuple, List
from py_dss_tools.results.Temporal.TemporalResults import TemporalResults
from py_dss_interface import DSS
from py_dss_tools.view.CustomPlotStyle import CustomPlotStyle
from typing import Optional, Union, Tuple



class Monitor:

    def __init__(self, dss: DSS, results: TemporalResults):
        self._results = results
        self._dss = dss

        self._plot_style = CustomPlotStyle()

    @property
    def monitor_plot_style(self):
        return self._plot_style

    def vmag_vs_time(self,
                     name: str,
                     unit: str = "pu",
                     title: Optional[str] = "Voltage Vs Time",
                     xlabel: Optional[str] = "Time",
                     ylabel: Optional[str] = "Voltage (pu)",
                     xlim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                     ylim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                     tight_layout: Optional[bool] = True,
                     legend: Optional[bool] = True,
                     dpi: Optional[int] = 200,
                     save_file_path: Optional[str] = None,
                     show: Optional[bool] = True,
                     **kwargs
                     ):
        if name.lower() not in self._dss.monitors.names:
            raise ValueError(f"{name} is not a monitor")

        self._plot_style.apply_style()
        df = self._results.monitor(name)

        fig, ax = plt.subplots()
        for key, value in kwargs.items():
            setattr(fig, key, value)

        self._dss.monitors.name = name
        m_mode = self._dss.monitors.mode
        vi_polar = self._dss.text(f"? monitor.{name}.vipolar").lower()

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

        if m_mode != 0:
            error_message = f'Invalid monitor mode. It should be 0 not {m_mode}'
            raise ValueError(error_message)
        if vi_polar in ["false", "no"]:
            raise ValueError(f'Invalid monitor vipolar. It should be True or Yes not {vi_polar}')

        node_colors = {1: 'black', 2: 'red', 3: 'blue'}

        for index, node in enumerate(elem_nodes):
            if unit == "kV":
                df[f" V{index + 1}"] = df[f" V{index + 1}"] / 1000.0
            elif unit == "pu":
                df[f" V{index + 1}"] = df[f" V{index + 1}"] / v_base
            ax.plot(df["Hour"], df[f" V{index + 1}"], color=node_colors[node], label=f"V{node}")

        fig.suptitle(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        if tight_layout:
            fig.tight_layout()

        if legend:
            ax.legend()

        fig.set_dpi(dpi)

        if save_file_path:
            plt.savefig(save_file_path)

        if show:
            plt.show()

    def p_vs_time(self,
                  name: str,
                  unit: str = "kW",
                  title: Optional[str] = "Active Power Vs Time",
                  xlabel: Optional[str] = "Time",
                  ylabel: Optional[str] = "Active Power (kW)",
                  xlim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                  ylim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                  tight_layout: Optional[bool] = True,
                  legend: Optional[bool] = True,
                  dpi: Optional[int] = 200,
                  save_file_path: Optional[str] = None,
                  show: Optional[bool] = True,
                  **kwargs
                  ):
        if name.lower() not in self._dss.monitors.names:
            raise ValueError(f"{name} is not a monitor")

        self._plot_style.apply_style()
        df = self._results.monitor(name)

        fig, ax = plt.subplots()
        for key, value in kwargs.items():
            setattr(fig, key, value)

        self._dss.monitors.name = name
        m_mode = self._dss.monitors.mode
        p_polar = self._dss.text(f"? monitor.{name}.ppolar").lower()

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

        if m_mode != 1:
            raise ValueError(f'Invalid monitor mode. It should be 1 not {m_mode}')
        if p_polar in ["true", "yes"]:
            raise ValueError(f'Invalid monitor ppolar. It should be True or Yes not {p_polar}')

        node_colors = {1: 'black', 2: 'red', 3: 'blue'}

        for index, node in enumerate(elem_nodes):
            if unit == "kW":
                pass
            ax.plot(df["Hour"], df[f" P{index + 1} (kW)"], color=node_colors[node], label=f"P{node}")

        fig.suptitle(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        if tight_layout:
            fig.tight_layout()

        if legend:
            ax.legend()

        fig.set_dpi(dpi)

        if save_file_path:
            plt.savefig(save_file_path)

        if show:
            plt.show()
