# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : Monitor.py
# @Software: PyCharm

from py_dss_tools.results.Temporal.TemporalResults import TemporalResults
from py_dss_interface import DSS
from py_dss_tools.view.CustomPlotStyle import CustomPlotStyle
from typing import Optional, Union, Tuple
from py_dss_tools.dss_tools.plot_utils import vmag_vs_time, p_vs_time


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
        vmag_vs_time(self._dss,
                     self._results.monitor(name),
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
        p_vs_time(self._dss,
                  self._results.monitor(name),
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
