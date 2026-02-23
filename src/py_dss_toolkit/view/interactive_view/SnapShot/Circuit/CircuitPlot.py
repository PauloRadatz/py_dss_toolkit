# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : CircuitPlot.py
# @Software: PyCharm

import plotly.graph_objects as go
from plotly.colors import sample_colorscale
import numpy as np
import pandas as pd
from typing import Optional, List
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitBase import CircuitPlotParameter
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitBase import CircuitBase
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitBusMarker import CircuitBusMarker


class CircuitPlot(CircuitBase):
    """Class for creating regular (non-geographic) circuit plots."""

    def __init__(self, dss, results, model, settings_container=None):
        """Initialize CircuitPlot with optional shared settings container."""
        super().__init__(dss, results, model, settings_container=settings_container)

    def circuit_plot(self,
                     parameter: CircuitPlotParameter = "active power",
                     title: Optional[str] = "Circuit Plot",
                     xlabel: Optional[str] = 'X Coordinate',
                     ylabel: Optional[str] = 'Y Coordinate',
                     width_3ph: int = 3,
                     width_2ph: int = 3,
                     width_1ph: int = 3,
                     dash_3ph: Optional[str] = None,
                     dash_2ph: Optional[str] = None,
                     dash_1ph: Optional[str] = None,
                     dash_oh: Optional[str] = None,
                     dash_ug: Optional[str] = None,
                     mark_buses: bool = True,
                     bus_markers: Optional[List[CircuitBusMarker]] = None,
                     show_colorbar: bool = True,
                     show: bool = False,
                     save_file_path: Optional[str] = None) -> Optional[go.Figure]:

        if mark_buses:
            mode = 'lines+markers'
        else:
            mode = 'lines'

        plot_data = self._prepare_plot_data(parameter)
        settings = plot_data['settings']
        results = plot_data['results']
        hovertemplate = plot_data['hovertemplate']
        numerical_plot = plot_data['numerical_plot']
        num_phases = plot_data['num_phases']
        line_type = plot_data['line_type']
        buses = plot_data['buses']
        bus_coords = plot_data['bus_coords']
        bus_to_idx = plot_data['bus_to_idx']
        connections = plot_data['connections']
        result_values = plot_data['result_values']

        fig = go.Figure()
        self._plot_style.apply_style(fig)

        if numerical_plot:
            self._add_numerical_plot_traces(fig, settings, results, hovertemplate, connections,
                                          bus_coords, bus_to_idx, result_values, num_phases, line_type,
                                          width_1ph, width_2ph, width_3ph, dash_1ph, dash_2ph,
                                          dash_3ph, dash_oh, dash_ug, mode, show_colorbar)
        else:
            self._add_categorical_plot_traces(fig, settings, results, hovertemplate, connections,
                                            bus_coords, bus_to_idx, num_phases, line_type,
                                            width_1ph, width_2ph, width_3ph, dash_1ph, dash_2ph,
                                            dash_3ph, dash_oh, dash_ug, mode)

        self._add_bus_markers(fig, bus_markers, bus_to_idx, bus_coords)

        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
        )

        if save_file_path:
            fig.write_html(save_file_path)
        if show:
            fig.show()

        return fig

    def _add_numerical_plot_traces(self, fig, settings, results, hovertemplate, connections,
                                 bus_coords, bus_to_idx, result_values, num_phases, line_type,
                                 width_1ph, width_2ph, width_3ph, dash_1ph, dash_2ph,
                                 dash_3ph, dash_oh, dash_ug, mode, show_colorbar):
        """Add traces for numerical plots."""
        cmin, cmax = self._calculate_colorbar_range(settings, result_values)
        colorbar_trace_values = np.linspace(cmin, cmax, 100)
        norm_values = np.clip((result_values - cmin) / (cmax - cmin), 0, 1)

        for connection, value in zip(connections, norm_values):
            element, (bus1, bus2) = connection
            x0, y0 = bus_coords[bus_to_idx[bus1]]
            x1, y1 = bus_coords[bus_to_idx[bus2]]

            # Skip buses with (0,0) coordinates - OpenDSS uses this to indicate undefined coordinates
            # Note: If your circuit legitimately has a bus at (0,0), offset it slightly (e.g., 0.0001, 0.0001)
            if x0 == 0 and y0 == 0:
                continue
            if x1 == 0 and y1 == 0:
                continue

            midpoint_x, midpoint_y = (x0 + x1) / 2, (y0 + y1) / 2
            color = sample_colorscale(settings.colorscale, value)[0]
            
            result_value = results.loc[element]
            
            customdata = [[element, bus1, bus2, result_value],
                            [element, bus1, bus2, result_value]]

            fig.add_trace(go.Scatter(
                x=[x0, x1], y=[y0, y1],
                mode=mode,
                line=dict(
                    color=color,
                    width=self._get_phase_width(element, num_phases, width_1ph, width_2ph, width_3ph),
                    dash=self._get_dash(element, num_phases, dash_1ph, dash_2ph, dash_3ph, line_type, dash_oh, dash_ug)),
                showlegend=False,
                name='',
                text=element,
                hoverinfo='skip'
            ))

            fig.add_trace(go.Scatter(
                x=[midpoint_x], y=[midpoint_y],
                mode='markers',
                marker=dict(size=0.1, color=color, opacity=0),
                showlegend=False,
                name="",
                hoverinfo='text',
                customdata=customdata,
                hovertemplate=hovertemplate
            ))

        if show_colorbar:
            self._add_colorbar(fig, settings, colorbar_trace_values, cmin, cmax, result_values)

    def _add_categorical_plot_traces(self, fig, settings, results, hovertemplate, connections,
                                   bus_coords, bus_to_idx, num_phases, line_type,
                                   width_1ph, width_2ph, width_3ph, dash_1ph, dash_2ph,
                                   dash_3ph, dash_oh, dash_ug, mode):
        """Add traces for categorical plots."""
        legend_added = set()
        for connection in connections:
            element, (bus1, bus2) = connection
            x0, y0 = bus_coords[bus_to_idx[bus1]]
            x1, y1 = bus_coords[bus_to_idx[bus2]]

            # Skip buses with (0,0) coordinates - OpenDSS uses this to indicate undefined coordinates
            # Note: If your circuit legitimately has a bus at (0,0), offset it slightly (e.g., 0.0001, 0.0001)
            if x0 == 0 and y0 == 0:
                continue
            if x1 == 0 and y1 == 0:
                continue

            midpoint_x, midpoint_y = (x0 + x1) / 2, (y0 + y1) / 2
            result_value = results.loc[element]
            color = settings.color_map[result_value][1]
            category = settings.color_map[result_value][0]

            customdata = [[element, bus1, bus2, result_value],
                         [element, bus1, bus2, result_value]]

            show_legend = False
            if category not in legend_added:
                show_legend = True
                legend_added.add(category)

            fig.add_trace(go.Scatter(
                x=[x0, x1], y=[y0, y1],
                mode=mode,
                line=dict(
                    color=color,
                    width=self._get_phase_width(element, num_phases, width_1ph, width_2ph, width_3ph),
                    dash=self._get_dash(element, num_phases, dash_1ph, dash_2ph, dash_3ph, line_type, dash_oh, dash_ug)),
                showlegend=show_legend,
                name=category,
                hoverinfo='skip',
                legendgroup="group",
                legendgrouptitle_text=settings.legendgrouptitle_text
            ))

            fig.add_trace(go.Scatter(
                x=[midpoint_x], y=[midpoint_y],
                mode='markers',
                marker=dict(size=0.1, color=color, opacity=0),
                showlegend=False,
                name="",
                hoverinfo='text',
                customdata=customdata,
                hovertemplate=hovertemplate,
                legendgroup="group"
            ))

        fig.update_layout(
            showlegend=True,
            legend=dict(
                x=1.2,
                y=1,
                traceorder="normal"
            )
        )

    def _add_colorbar(self, fig, settings, colorbar_trace_values, cmin, cmax, result_values):
        """Add colorbar to the plot."""
        custom_tickvals, custom_ticktext = self._calculate_colorbar_ticks(settings, result_values)

        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(
                colorscale=settings.colorscale,
                color=colorbar_trace_values,
                cmin=cmin,
                cmax=cmax,
                colorbar=dict(
                    title=settings.colorbar_title,
                    thickness=20,
                    len=0.75,
                    ticks="outside",
                    tickvals=custom_tickvals,
                    ticktext=custom_ticktext
                ),
                showscale=True
            ),
            hoverinfo='none'
        ))
        fig.update_layout(showlegend=False)

    def _add_bus_markers(self, fig, bus_markers, bus_to_idx, bus_coords):
        """Add bus markers to the plot."""
        if bus_markers:
            for marker in bus_markers:
                if marker.name in bus_to_idx:
                    bus_x, bus_y = bus_coords[bus_to_idx[marker.name]]
                    fig.add_trace(go.Scatter(
                        x=[bus_x],
                        y=[bus_y],
                        mode='markers',
                        marker=dict(
                            symbol=marker.symbol,
                            size=marker.size,
                            color=marker.color
                        ),
                        showlegend=False,
                        name="",
                        hoverinfo='text',
                        customdata=[[marker.name]],
                        hovertemplate=("<b>Bus: </b>%{customdata[0]}<br>"),
                    ))
