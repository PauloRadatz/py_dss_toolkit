# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : VoltageProfile.py
# @Software: PyCharm

import plotly.graph_objects as go
from py_dss_tools.results.Static.StaticResults import StaticResults
from py_dss_interface import DSS
from typing import Optional, Union, Tuple, List
from py_dss_tools.view.view_base.VoltageProfileBase import VoltageProfileBase
from py_dss_tools.view.interactive_view.Static.VoltageProfileBusMarker import VoltageProfileBusMarker
from py_dss_tools.view.interactive_view.CustomPlotStyle import CustomPlotStyle


class VoltageProfile(VoltageProfileBase):

    def __init__(self, dss: DSS, results: StaticResults):
        self._results = results
        self._dss = dss
        VoltageProfileBase.__init__(self, self._dss, self._results)
        self._plot_style = CustomPlotStyle()

    @property
    def voltage_profile_plot_style(self):
        return self._plot_style

    def voltage_profile_get_bus_mark(self, name: str, symbol: str = "x",
                                     size: float = 10,
                                     color: str = "black",
                                     annotate: bool = False,
                                     annotation_label: Optional[str] = None):
        if not annotation_label:
            annotation_label = name
        return VoltageProfileBusMarker(name=name,
                                       symbol=symbol,
                                       size=size,
                                       color=color,
                                       annotate=annotate,
                                       annotation_label=annotation_label)

    def voltage_profile(self,
                        title: Optional[str] = "Voltage Profile",
                        xlabel: Optional[str] = "Distance",
                        ylabel: Optional[str] = "Voltage (pu)",
                        xlim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                        ylim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                        buses_marker: Optional[List[VoltageProfileBusMarker]] = None,
                        show: Optional[bool] = True,
                        save_file_path: Optional[str] = None):
        self._check_energymeter()

        buses, df, distances, sections = self._prepare_results()
        node_colors = {1: 'black', 2: 'red', 3: 'blue'}

        fig = go.Figure()
        self._plot_style.apply_style(fig)

        # Add voltage profile lines
        for node in range(1, 4):
            for section in sections:
                bus1, bus2 = section
                distance1 = distances[buses.index(bus1)]
                distance2 = distances[buses.index(bus2)]

                # Add scatter trace for the voltage profile section
                fig.add_trace(go.Scatter(
                    x=[distance1, distance2],
                    y=[df.loc[bus1, f'node{node}'], df.loc[bus2, f'node{node}']],
                    mode='lines+markers',
                    marker=dict(color=node_colors[node]),
                    line=dict(color=node_colors[node]),
                    legendgroup=f'Node {node}',  # Grouping by node
                    showlegend=(section == sections[0]),  # Only show one legend item for each node
                    name=f'Node {node}',
                    customdata=[[bus1], [bus2]],  # Adding bus name as custom data
                    hovertemplate=(
                        "Bus: %{customdata[0]}<br>"  # Display bus name
                        "Distance: %{x}<br>"
                        "Voltage: %{y:.3f} pu<extra></extra>"  # Voltage displayed with 3 decimal places
                    )
                ))

                # Add bus markers if specified
                if buses_marker:
                    bus_marker = next((bus for bus in buses_marker if bus.name == bus1), None)
                    if bus_marker:
                        fig.add_trace(go.Scatter(
                            x=[distance1],
                            y=[df.loc[bus1, f'node{node}']],
                            mode='markers',
                            marker=dict(symbol=bus_marker.symbol,
                                        size=bus_marker.size,
                                        color=bus_marker.color),
                            legendgroup=f'Node {node}',  # Group markers with their respective node
                            showlegend=False,  # No additional legend items for markers
                            name=bus_marker.annotation_label if bus_marker.annotate else bus1,
                            customdata=[[bus1]],  # Adding bus name to the marker
                            hovertemplate=(
                                "Bus: %{customdata[0]}<br>"
                                "Distance: %{x}<br>"
                                "Voltage: %{y:.3f} pu<extra></extra>"
                            )
                        ))

        # Customize layout
        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            xaxis=dict(range=xlim),
            yaxis=dict(range=ylim),
        )

        # Show or save the plot
        if save_file_path:
            fig.write_html(save_file_path)
        if show:
            fig.show()
