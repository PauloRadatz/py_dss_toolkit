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

    def plot_feeder_topology(self, parameter="voltage"):
        # 1. Extract the topology data
        buses = [bus.lower() for bus in self._dss.circuit.buses_names]

        bus_coords = list()
        for bus in buses:
            self._dss.circuit.set_active_bus(bus)
            x, y = self._dss.bus.x, self._dss.bus.y
            bus_coords.append((x, y))

        bus_coords = np.array(bus_coords)

        elements_list = [element.lower() for element in self._dss.circuit.elements_names]
        connections = []
        for element in elements_list:
            if element.split(".")[0].lower() in ["line", "transformer"]:
                self._dss.circuit.set_active_element(element)
                bus1, bus2 = self._dss.cktelement.bus_names[0].split(".")[0].lower(), \
                self._dss.cktelement.bus_names[1].split(".")[0].lower()
                connections.append([element, (bus1.lower(), bus2.lower())])

        # 2. User-defined results for color coding
        results = self._results.powers_elements[0].iloc[:, :3].sum(axis=1)
        result_values = list()
        for element in elements_list:
            if element.split(".")[0].lower() in ["line", "transformer"]:
                result_values.append(results.loc[element])
        result_values = np.array(result_values)

        # 3. Normalize results for color mapping
        norm_values = (result_values - np.min(result_values)) / (np.max(result_values) - np.min(result_values))

        # 4. Create plotly traces for the topology
        fig = go.Figure()

        colorscale = 'Viridis'

        # Plot the connections (lines)
        for connection, value in zip(connections, norm_values):
            element, (bus1, bus2) = connection
            x0, y0 = bus_coords[buses.index(bus1)]
            x1, y1 = bus_coords[buses.index(bus2)]

            # Map the normalized value to a color from the colorscale
            color = sample_colorscale(colorscale, value)[0]

            fig.add_trace(go.Scatter(
                x=[x0, x1], y=[y0, y1],
                mode='lines',
                line=dict(color=color, width=3),
                hoverinfo='text',
                text=f'{element}: {parameter} = {results.loc[element]:.3f}',
                showlegend=False
            ))

        # Plot the nodes (buses)
        fig.add_trace(go.Scatter(
            x=bus_coords[:, 0], y=bus_coords[:, 1],
            mode='markers',
            marker=dict(size=10, color='black'),
            text=[f'Bus: {bus}' for bus in buses],
            hoverinfo='text',
            showlegend=False
        ))

        # 5. Add a colorbar
        fig.update_layout(coloraxis_colorbar=dict(
            title=parameter,
            thicknessmode="pixels", thickness=20,
            lenmode="pixels", len=200,
            yanchor="top", y=1,
            ticks="outside",
            ticksuffix="",
            dtick=5
        ))

        # Set plot title and axis labels
        fig.update_layout(
            title=f'Feeder Topology with {parameter} Color Mapping',
            xaxis_title='X Coordinate',
            yaxis_title='Y Coordinate',
            showlegend=False,
            coloraxis=dict(colorscale='Viridis')
        )

        # Show the plot
        fig.show()
