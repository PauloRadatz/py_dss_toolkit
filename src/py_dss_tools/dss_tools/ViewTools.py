# -*- coding: utf-8 -*-
# @Time    : 3/30/2024 12:03 PM
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewTools.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from typing import Dict
import matplotlib.pyplot as plt
from typing import List, Optional, Union, Tuple
from .ResultsTools import ResultsTools
from py_dss_tools.view.CustomPlotStyle import CustomPlotStyle
from py_dss_tools.dss_tools.plot_utils import voltage_profile, vmag_vs_time, p_vs_time


class ViewTools:

    def __init__(self, dss: DSS):
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
        results = ResultsTools(self._dss).circuit_vmag_vang_dfs()[0]
        voltage_profile(self._dss,
                        results,
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
        results = ResultsTools(self._dss).monitor_df(name)
        vmag_vs_time(self._dss,
                     results,
                     self._plot_style,
                     name,
                     unit,
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
                     **kwargs
                     )

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
        results = ResultsTools(self._dss).monitor_df(name)
        p_vs_time(self._dss,
                  results,
                  self._plot_style,
                  name,
                  unit,
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
                  **kwargs
                  )
