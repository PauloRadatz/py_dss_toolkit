# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : VoltageProfile.py
# @Software: PyCharm

import plotly.graph_objects as go
from py_dss_toolkit.results.SnapShot.SnapShotPowerFlowResults import SnapShotPowerFlowResults
from py_dss_interface import DSS
from typing import Optional, Union, Tuple, List
from py_dss_toolkit.view.view_base.VoltageProfileBase import VoltageProfileBase
from py_dss_toolkit.view.interactive_view.SnapShot.InteractiveVoltageProfileBusMarker import InteractiveVoltageProfileBusMarker
from py_dss_toolkit.view.interactive_view.InteractiveCustomPlotStyle import InteractiveCustomPlotStyle


class InteractiveVoltageProfile(VoltageProfileBase):

    def __init__(self, dss: DSS, results: SnapShotPowerFlowResults):
        self._results = results

        self._dss = dss
        VoltageProfileBase.__init__(self, self._dss, self._results)
        self._plot_style = InteractiveCustomPlotStyle()

    @property
    def voltage_profile_plot_style(self):
        return self._plot_style

    def voltage_profile_get_bus_marker(self, name: str, symbol: str = "x",
                                       size: float = 10,
                                       color: str = "black",
                                       annotate: bool = False,
                                       marker_name: Optional[str] = None,
                                       show_legend: bool = False):
        if not marker_name:
            marker_name = name
        return InteractiveVoltageProfileBusMarker(name=name,
                                       symbol=symbol,
                                       size=size,
                                       color=color,
                                       annotate=annotate,
                                       marker_name=marker_name,
                                       show_legend=show_legend)

    def voltage_profile(self,
                        title: Optional[str] = "Voltage Profile",
                        xlabel: Optional[str] = "Distance",
                        ylabel: Optional[str] = "Voltage (pu)",
                        xlim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                        ylim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                        buses_marker: Optional[List[InteractiveVoltageProfileBusMarker]] = None,
                        show: Optional[bool] = True,
                        save_file_path: Optional[str] = None) -> Optional[go.Figure]:
        self._check_energymeter()

        buses, df, distances, sections = self._prepare_results()
        node_colors = {1: 'black', 2: 'red', 3: 'blue'}

        fig = go.Figure()
        self._plot_style.apply_style(fig)

        # Dictionary to track whether the bus has already been added to the legend
        legend_added = {}

        # Step 1: Add voltage profile lines for Node 1, Node 2, and Node 3
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

        # Step 2: Add bus markers
        for node in range(1, 4):
            for section in sections:
                bus1, bus2 = section
                distance1 = distances[buses.index(bus1)]

                # Add bus markers if specified
                if buses_marker:
                    bus_marker = next((bus for bus in buses_marker if bus.name == bus1), None)
                    if bus_marker:
                        hovertemplate = (f"<br>{bus_marker.marker_name}<br>"
                                         "Bus: %{customdata[0]}<br>"
                                         "Distance: %{x}<br>"
                                         "Voltage: %{y:.3f} pu"
                                         )

                        hovertemplate += "<extra></extra>"

                        # Determine if the bus has already been added to the legend
                        show_legend = not legend_added.get(bus1, False)

                        # Add the scatter plot trace for the bus marker
                        fig.add_trace(go.Scatter(
                            x=[distance1],
                            y=[df.loc[bus1, f'node{node}']],
                            mode='markers',
                            marker=dict(symbol=bus_marker.symbol,
                                        size=bus_marker.size,
                                        color=bus_marker.color),
                            legendgroup=f'Bus {bus1}',  # Group markers by bus
                            showlegend=show_legend,  # Show in legend only if not added before
                            name=f'{bus_marker.marker_name}',  # Legend name
                            customdata=[[bus1]],  # Adding bus name to the marker
                            hovertemplate=hovertemplate  # Apply the combined hovertemplate
                        ))

                        # Mark this bus as added to the legend
                        legend_added[bus1] = True

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
        return fig
