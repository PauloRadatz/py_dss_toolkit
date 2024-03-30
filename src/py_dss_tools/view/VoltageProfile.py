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
from py_dss_tools.dss_tools.plot_utils import voltage_profile


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

        voltage_profile(self._dss,
                        self._results.voltage_ln_nodes[0],
                        self._plot_style,
                        title,
                        xlabel,
                        ylabel,
                        xlim,
                        ylim,
                        tight_layout,
                        legend,
                        dpi,
                        save_file_path,
                        show,
                        **kwargs)
