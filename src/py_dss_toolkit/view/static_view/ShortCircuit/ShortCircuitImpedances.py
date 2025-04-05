# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : VoltageProfile.py
# @Software: PyCharm

from py_dss_toolkit.results.ShortCircuit.FaultResults import FaultResults
import matplotlib.pyplot as plt
from py_dss_interface import DSS
from py_dss_toolkit.view.static_view.StaticCustomPlotStyle import StaticCustomPlotStyle
from typing import Optional, Union, Tuple


class ShortCircuitImpedances:

    def __init__(self, dss: DSS, results: FaultResults):
        self._results = results
        self._dss = dss

        self._plot_style = StaticCustomPlotStyle()

    @property
    def short_circuit_impedances_plot_style(self):
        return self._plot_style

    def impedances_vs_distance(self,
                        title: Optional[str] = "-------",
                        xlabel: Optional[str] = "Distance",
                        ylabel: Optional[str] = "Impedance (Ohms)",
                        xlim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                        ylim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                        tight_layout: Optional[bool] = True,
                        legend: Optional[bool] = True,
                        dpi: Optional[int] = 200,
                        save_file_path: Optional[str] = None,
                        show: Optional[bool] = True,
                        **kwargs
                        ):

        self._plot_style.apply_style()
        fig, ax = plt.subplots()
        for key, value in kwargs.items():
            setattr(fig, key, value)

        df = self._results.short_circuit_impedances

        # Plotting
        plt.scatter(df['Distance (m?)'], df['r1 (Ohm)'], label='r1 (Ohm)', marker='o', c="red")
        plt.scatter(df['Distance (m?)'], df['r0 (Ohm)'], label='r0 (Ohm)', marker='o', c="blue")
        plt.scatter(df['Distance (m?)'], df['x1 (Ohm)'], label='x1 (Ohm)', marker='o', c="yellow")
        plt.scatter(df['Distance (m?)'], df['x0 (Ohm)'], label='x0 (Ohm)', marker='o', c="green")

        if legend:
            plt.legend()

        fig.suptitle(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        if tight_layout:
            fig.tight_layout()

        fig.set_dpi(dpi)

        if save_file_path:
            plt.savefig(save_file_path)

        if show:
            plt.show()
