# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : MonitorBase.py
# @Software: PyCharm

import matplotlib.pyplot as plt
from py_dss_tools.results.Temporal.TemporalResults import TemporalResults
from py_dss_interface import DSS
from py_dss_tools.view.static_view.StaticCustomPlotStyle import StaticCustomPlotStyle
from typing import Optional, Union, Tuple
from py_dss_tools.view.view_base.MonitorBase import MonitorBase


class Monitor(MonitorBase):

    def __init__(self, dss: DSS, results: TemporalResults):
        self._results = results
        self._dss = dss
        MonitorBase.__init__(self, self._dss, self._results)

        self._plot_style = StaticCustomPlotStyle()

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
        self._check_v_monitor(name)

        elem_nodes, v_base = self._organize_v_results(name)

        self._dss.monitors.name = name
        self._plot_style.apply_style()
        df = self._results.monitor(name)

        fig, ax = plt.subplots()
        for key, value in kwargs.items():
            setattr(fig, key, value)

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
        self._check_p_monitor(name)

        elem_nodes = self._organize_p_results(name)

        self._dss.monitors.name = name
        self._plot_style.apply_style()
        df = self._results.monitor(name)

        fig, ax = plt.subplots()
        for key, value in kwargs.items():
            setattr(fig, key, value)
        node_colors = {1: 'black', 2: 'red', 3: 'blue'}

        for index, node in enumerate(elem_nodes):
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


