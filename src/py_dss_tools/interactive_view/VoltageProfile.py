# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : VoltageProfile.py
# @Software: PyCharm

import plotly.graph_objects as go
from py_dss_tools.results.Static.StaticResults import StaticResults
from py_dss_interface import DSS
from typing import Optional, Union, Tuple, Dict


class VoltageProfile:

    def __init__(self, dss: DSS, results: StaticResults):
        self._results = results
        self._dss = dss

    def voltage_profile_get_bus_mark(self, name: str, symbol: str = "circle",
                                            size: float = 10,
                                            color: str = "black",
                                            annotate: bool = False,
                                            annotation_label: Optional[str] = None):
        if not annotation_label:
            annotation_label = name
        return {
            "name": name,
            "symbol": symbol,
            "size": size,
            "color": color,
            "annotate": annotate,
            "annotation_label": annotation_label
        }

    def voltage_profile(self,
                               title: Optional[str] = "Voltage Profile",
                               xlabel: Optional[str] = "Distance",
                               ylabel: Optional[str] = "Voltage (pu)",
                               xlim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                               ylim: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
                               buses_marker: Optional[Dict[str, dict]] = None,
                               show: Optional[bool] = True,
                               save_file_path: Optional[str] = None):
        if self._dss.meters.count == 0:
            raise ValueError('One energy meter should exist to plot the voltage profile.')
        elif self._dss.meters.count > 1:
            count_enabled = 0
            self._dss.meters.first()
            for _ in range(self._dss.meters.count):
                self._dss.circuit.set_active_element(f"energymeter.{self._dss.meters.name}")
                if self._dss.cktelement.is_enabled:
                    count_enabled += 1
                self._dss.meters.next()

            if count_enabled == 0:
                raise ValueError('At least one energy meter should be enabled to plot the voltage profile.')
            elif count_enabled > 1:
                raise ValueError('Only one energy meter should be enabled to plot the voltage profile.')

        # Prepare data for the plot
        df = self._results.voltage_ln_nodes[0]
        buses = [bus.lower().split(".")[0] for bus in self._dss.circuit.buses_names]
        distances = self._dss.circuit.buses_distances

        sections = []
        elements_list = self._dss.circuit.elements_names
        for element in elements_list:
            if element.split(".")[0].lower() in ["line", "reactor"]:
                self._dss.circuit.set_active_element(element)
                if self._dss.cktelement.is_enabled:
                    sections.append(
                        (self._dss.cktelement.bus_names[0].lower().split(".")[0],
                         self._dss.cktelement.bus_names[1].lower().split(".")[0]))

        # Create Plotly figure
        fig = go.Figure()

        # Add voltage profile lines
        node_colors = {1: 'black', 2: 'red', 3: 'blue'}

        for node in range(1, 4):
            for section in sections:
                bus1, bus2 = section
                distance1 = distances[buses.index(bus1)]
                distance2 = distances[buses.index(bus2)]
                fig.add_trace(go.Scatter(x=[distance1, distance2],
                                         y=[df.loc[bus1, f'node{node}'], df.loc[bus2, f'node{node}']],
                                         mode='lines+markers',
                                         name=f'Node {node}',
                                         marker=dict(color=node_colors[node]),
                                         line=dict(color=node_colors[node])))

                # Add bus markers if specified
                if buses_marker:
                    bus_marker = buses_marker.get(bus1)
                    if bus_marker:
                        fig.add_trace(go.Scatter(x=[distance1],
                                                 y=[df.loc[bus1, f'node{node}']],
                                                 mode='markers',
                                                 marker=dict(symbol=bus_marker['symbol'],
                                                             size=bus_marker['size'],
                                                             color=bus_marker['color']),
                                                 name=bus_marker['annotation_label'] if bus_marker['annotate'] else bus1))

        # Customize layout
        fig.update_layout(title=title,
                          xaxis_title=xlabel,
                          yaxis_title=ylabel,
                          xaxis=dict(range=xlim),
                          yaxis=dict(range=ylim),
                          showlegend=True)

        # Show or save the plot
        if save_file_path:
            fig.write_html(save_file_path)
        if show:
            fig.show()
