# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : DSSMonitor.py
# @Software: PyCharm

import plotly.graph_objects as go
from py_dss_toolkit.results.TimeSeries.TimeSeriesPowerFlowResults import TimeSeriesPowerFlowResults
from py_dss_interface import DSS
from py_dss_toolkit.view.interactive_view.InteractiveCustomPlotStyle import InteractiveCustomPlotStyle
from typing import Optional, Union, Tuple
from py_dss_toolkit.view.view_base.MonitorBase import MonitorBase


class InteractiveMonitor(MonitorBase):

    def __init__(self, dss: DSS, results: TimeSeriesPowerFlowResults):
        self._results = results
        self._dss = dss
        MonitorBase.__init__(self, self._dss, self._results)

        self._plot_style = InteractiveCustomPlotStyle()  # Use custom Plotly styles

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
                     legend: Optional[bool] = True,
                     save_file_path: Optional[str] = None,
                     show: Optional[bool] = True,
                     get_fig_obj: bool = False
                     ) -> Optional[go.Figure]:
        self._check_v_monitor(name)

        elem_nodes, v_base = self._organize_v_results(name)

        self._dss.monitors.name = name
        df = self._results.monitor(name)

        fig = go.Figure()

        node_colors = {1: 'black', 2: 'red', 3: 'blue'}

        for index, node in enumerate(elem_nodes):
            if unit == "kV":
                df[f" V{index + 1}"] = df[f" V{index + 1}"] / 1000.0
            elif unit == "pu":
                df[f" V{index + 1}"] = df[f" V{index + 1}"] / v_base
            customdata = [[unit] for _ in range(len(df["Hour"]))]
            fig.add_trace(go.Scatter(x=df["Hour"], y=df[f" V{index + 1}"],
                                     mode='lines',
                                     line=dict(color=node_colors[node]),
                                     name=f"V{node}",
                                     customdata=customdata,
                                     hovertemplate=(
                                         "Hour: %{x}<br>"
                                         "Voltage: %{y:.4f} %{customdata[0]}<extra></extra>"
                                     # Voltage displayed with 3 decimal places
                                     ))
                          )

        # Apply custom Plotly styles
        self._plot_style.apply_style(fig)

        # Set plot title and labels
        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            xaxis=dict(range=xlim),
            yaxis=dict(range=ylim),
            showlegend=legend
        )

        # Save or show the plot
        if save_file_path:
            fig.write_html(save_file_path)
        if show:
            fig.show()
        if get_fig_obj:
            return fig

    def p_vs_time(self,
                  name: str,
                  title: Optional[str] = "Active Power Vs Time",
                  xlabel: Optional[str] = "Time",
                  ylabel: Optional[str] = "Active Power (kW)",
                  xlim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                  ylim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                  legend: Optional[bool] = True,
                  save_file_path: Optional[str] = None,
                  show: Optional[bool] = True,
                  get_fig_obj: bool = False
                  ) -> Optional[go.Figure]:
        self._check_p_monitor(name)

        elem_nodes = self._organize_p_results(name)

        self._dss.monitors.name = name
        df = self._results.monitor(name)

        fig = go.Figure()

        node_colors = {1: 'black', 2: 'red', 3: 'blue'}

        for index, node in enumerate(elem_nodes):
            fig.add_trace(go.Scatter(x=df["Hour"], y=df[f" P{index + 1} (kW)"],
                                     mode='lines',
                                     line=dict(color=node_colors[node]),
                                     name=f"P{node}",
                                     hovertemplate=(
                                         "Hour: %{x}<br>"
                                         "Active Power: %{y:.1f} kW<extra></extra>"
                                     )))

        # Apply custom Plotly styles
        self._plot_style.apply_style(fig)

        # Set plot title and labels
        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            xaxis=dict(range=xlim),
            yaxis=dict(range=ylim),
            showlegend=legend
        )

        # Save or show the plot
        if save_file_path:
            fig.write_html(save_file_path)
        if show:
            fig.show()
        if get_fig_obj:
            return fig
