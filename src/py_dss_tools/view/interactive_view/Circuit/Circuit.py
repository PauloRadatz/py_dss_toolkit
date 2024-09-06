# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : Circuit.py
# @Software: PyCharm

import plotly.graph_objects as go
from plotly.colors import sample_colorscale
from py_dss_tools.results.Static.StaticResults import StaticResults
from py_dss_interface import DSS
from py_dss_tools.view.interactive_view.CustomPlotStyle import CustomPlotStyle
import numpy as np


class Circuit:

    def __init__(self, dss: DSS, results: StaticResults):
        self._dss = dss
        self._results = results
        self._plot_style = CustomPlotStyle()

    @property
    def circuit_plot_style(self):
        return self._plot_style

    def plot_feeder_topology(self, parameter="active power"):
        # 1. Extract the topology data
        buses = list()
        bus_coords = list()
        elements_list = [element.lower() for element in self._dss.circuit.elements_names]
        connections = []
        for element in elements_list:
            if element.split(".")[0].lower() in ["line"]:
                self._dss.circuit.set_active_element(element)
                bus1, bus2 = self._dss.cktelement.bus_names[0].split(".")[0].lower(), \
                self._dss.cktelement.bus_names[1].split(".")[0].lower()
                connections.append([element, (bus1.lower(), bus2.lower())])

                if bus1 not in buses:
                    self._dss.circuit.set_active_bus(bus1)
                    x, y = self._dss.bus.x, self._dss.bus.y
                    bus_coords.append((x, y))
                    buses.append(bus1)

                if bus2 not in buses:
                    self._dss.circuit.set_active_bus(bus2)
                    x, y = self._dss.bus.x, self._dss.bus.y
                    bus_coords.append((x, y))
                    buses.append(bus2)
        bus_coords = np.array(bus_coords)

        # 2. User-defined results for color coding


        results = self._results.powers_elements[0].iloc[:, :3].sum(axis=1)
        result_values = list()
        for element in elements_list:
            if element.split(".")[0].lower() in ["line"]:
                result_values.append(results.loc[element])
        result_values = np.array(result_values)

        # 3. Normalize results for color mapping
        norm_values = (result_values - np.min(result_values)) / (np.max(result_values) - np.min(result_values))

        # 4. Create plotly traces for the topology
        fig = go.Figure()

        colorscale = 'Viridis'
        colorbar_trace_values = np.linspace(np.min(result_values), np.max(result_values), 100)

        # Plot the connections (lines)
        for connection, value in zip(connections, norm_values):
            element, (bus1, bus2) = connection
            x0, y0 = bus_coords[buses.index(bus1)]
            x1, y1 = bus_coords[buses.index(bus2)]

            # Map the normalized value to a color from the colorscale
            color = sample_colorscale(colorscale, value)[0]

            customdata = [[element, parameter, results.loc[element]], [element, parameter, results.loc[element]]]

            hovertemplate = "<b>Element: </b>%{customdata[0]}<br>" + \
                            "<b>Parameter: </b>%{customdata[1]}<br>" + \
                            "<b>Result: </b>%{customdata[2]:.2f}MW<br>"

            fig.add_trace(go.Scatter(
                x=[x0, x1], y=[y0, y1],
                mode='lines+markers',
                line=dict(color=color, width=3),
                showlegend=False,
                name='',
                text=element,
                hoverinfo='text',
                customdata=customdata,
                hovertemplate=hovertemplate
            ))

        # Add a dummy trace to represent the colorbar
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(
                colorscale=colorscale,
                color=colorbar_trace_values,  # Use the range of values
                cmin=np.min(result_values),
                cmax=np.max(result_values),
                colorbar=dict(
                    title=parameter,
                    thickness=20,
                    len=0.75,
                    ticks="outside"
                ),
                showscale=True
            ),
            hoverinfo='none'
        ))

        # Set layout
        fig.update_layout(
            title=f'Feeder Topology with {parameter} Color Mapping',
            xaxis_title='X Coordinate',
            yaxis_title='Y Coordinate',
            showlegend=False
        )

        # Show the plot
        fig.show()
