# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : VoltageProfile.py
# @Software: PyCharm

from py_dss_tools.results.StaticResults import StaticResults
import matplotlib.pyplot as plt
from py_dss_interface import DSS
from py_dss_tools.view.CustomPlotStyle import CustomPlotStyle
from typing import List, Optional, Union, Tuple

class VoltageProfile:

    def __init__(self, dss: DSS, results: StaticResults):
        self._results = results
        self._dss = dss

        self._plot_style = CustomPlotStyle()

    @property
    def voltage_profile_plot_style(self):
        return self._plot_style

    def voltage_profile(self,
                        title: Optional[str] = "Voltage Profile",
                        xlabel: Optional[str] = "Distance",
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

        if self._dss.meters.count == 0:
            raise ValueError(f'At least one enerymeter should exist to plot the voltage profile.')

        self._plot_style.apply_style()
        fig, ax = plt.subplots()
        for key, value in kwargs.items():
            setattr(fig, key, value)

        df = self._results.voltage_ln_nodes[0]
        buses = [bus.lower().split(".")[0] for bus in self._dss.circuit.buses_names]
        distances = self._dss.circuit.buses_distances

        sections = list()
        self._dss.lines.first()
        for _ in range(self._dss.lines.count):
            sections.append((self._dss.lines.bus1.lower().split(".")[0], self._dss.lines.bus2.lower().split(".")[0]))
            self._dss.lines.next()

        node_colors = {1: 'black', 2: 'red', 3: 'blue'}
        plt.figure(figsize=(10, 6))

        for node in range(1, 4):
            for section in sections:
                bus1, bus2 = section
                distance1 = distances[buses.index(bus1)]
                distance2 = distances[buses.index(bus2)]
                ax.plot([distance1, distance2], [df.loc[bus1, f'node{node}'], df.loc[bus2, f'node{node}']], marker='o',
                         color=node_colors[node])


        if legend:
            legend_labels = [f'Node {node}' for node in range(1, 4)]
            legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=node_colors[node], markersize=10)
                              for node in range(1, 4)]
            fig.legend(legend_handles, legend_labels)

        fig.suptitle(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        if tight_layout:
            fig.tight_layout()

        fig.set_dpi(dpi)

        if save_file_path:
            fig.savefig(save_file_path, format="png", dpi=300, bbox_inches='tight')

        if show:
            plt.show()
