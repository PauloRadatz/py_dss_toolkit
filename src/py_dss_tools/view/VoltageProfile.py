# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : VoltageProfile.py
# @Software: PyCharm

from py_dss_tools.results.StaticResults import StaticResults
from py_dss_interface import DSS
from py_dss_tools.view.CustomPlotStyle import CustomPlotStyle
from typing import Optional, Union, Tuple, Dict
from py_dss_tools.dss_tools.plot_utils import voltage_profile
from py_dss_tools.dss_tools.VoltageProfileBusMarker import VoltageProfileBusMarker


class VoltageProfile:

    def __init__(self, dss: DSS, results: StaticResults):
        self._results = results
        self._dss = dss

        self._plot_style = CustomPlotStyle()

    @property
    def voltage_profile_plot_style(self):
        return self._plot_style

    def voltage_profile_get_bus_mark(self, name: str, marker: str = "x",
                     size: float = 10,
                     color: str = "black",
                     annotate: bool = False,
                     annotation_label: Optional[str] = None,
                     annotation_delta_x: float = -0.02,
                     annotation_delta_y: float = -0.02):
        if not annotation_label:
            annotation_label = name
        return VoltageProfileBusMarker(name=name,
                                       marker=marker,
                                       size=size,
                                       color=color,
                                       annotate=annotate,
                                       annotation_label=annotation_label,
                                       annotation_delta_x=annotation_delta_x,
                                       annotation_delta_y=annotation_delta_y)

    def voltage_profile(self,
                        title: Optional[str] = "Voltage Profile",
                        xlabel: Optional[str] = "Distance",
                        ylabel: Optional[str] = "Voltage (pu)",
                        xlim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                        ylim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                        buses_marker: Optional[Dict[str, VoltageProfileBusMarker]] = None,
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
                        buses_marker,
                        tight_layout,
                        legend,
                        dpi,
                        save_file_path,
                        show,
                        **kwargs)
