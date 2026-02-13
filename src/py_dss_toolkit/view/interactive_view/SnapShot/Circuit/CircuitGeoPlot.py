# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : CircuitGeoPlot.py
# @Software: PyCharm

import plotly.graph_objects as go
from plotly.colors import sample_colorscale
import numpy as np
import pandas as pd
from typing import Optional, List
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitBase import CircuitPlotParameter
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitBase import CircuitBase
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitBusMarker import CircuitBusMarker


class CircuitGeoPlot(CircuitBase):
    """
    Class for creating geographic circuit plots.

    Note:
        This class uses Plotly's Scattermap traces which only support WGS84 (EPSG:4326)
        coordinate reference system. If your data is in a different CRS, you need to
        transform your coordinates to WGS84 before using this plotting functionality.
        You can use libraries like pyproj or geopandas for coordinate transformation.
    """

    def __init__(self, dss, results, model, settings_container=None):
        """Initialize CircuitGeoPlot with optional shared settings container."""
        super().__init__(dss, results, model, settings_container=settings_container)

    def circuit_geoplot(self,
                        parameter: CircuitPlotParameter = "active power",
                        title: Optional[str] = "Circuit Plot",
                        width_3ph: int = 3,
                        width_2ph: int = 3,
                        width_1ph: int = 3,
                        mark_buses: bool = True,
                        bus_markers: Optional[List[CircuitBusMarker]] = None,
                        show_colorbar: bool = True,
                        show: bool = False,
                        map_style: Optional[str] = 'open-street-map',
                        save_file_path: Optional[str] = None) -> Optional[go.Figure]:
        """
        Create an interactive geographic plot of the circuit.

        This method creates a geographic plot using Plotly's map functionality, displaying
        circuit elements overlaid on a map background.

        Important:
            This method requires coordinates to be in WGS84 (EPSG:4326) format (latitude/longitude).
            If your bus coordinates are in a different coordinate reference system (CRS), you must
            transform them to WGS84 before using this method. Use libraries like pyproj or geopandas
            for coordinate transformation.

        Args:
            parameter (str): The parameter to plot. Defaults to "active power".
            title (Optional[str]): Title for the plot. Defaults to "Circuit Plot".
            width_3ph (int): Line width for 3-phase elements. Defaults to 3.
            width_2ph (int): Line width for 2-phase elements. Defaults to 3.
            width_1ph (int): Line width for 1-phase elements. Defaults to 3.
            mark_buses (bool): Whether to show bus markers. Defaults to True.
            bus_markers (Optional[List[CircuitBusMarker]]): Custom bus markers to display.
            show_colorbar (bool): Whether to show the colorbar. Defaults to True.
            show (bool): Whether to display the plot immediately. Defaults to False.
            map_style (Optional[str]): Map style for the background. Options include:
                'open-street-map', 'white-bg', 'carto-positron', 'carto-darkmatter',
                'stamen-terrain', 'stamen-toner', 'stamen-watercolor'. Defaults to 'open-street-map'.
            save_file_path (Optional[str]): Path to save the plot as HTML file.

        Returns:
            Optional[go.Figure]: The Plotly figure object, or None if save_file_path is provided.


        """

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
        bus_coords = plot_data['bus_coords']
        bus_to_idx = plot_data['bus_to_idx']
        connections = plot_data['connections']
        result_values = plot_data['result_values']

        fig = go.Figure()

        if numerical_plot:
            self._add_geo_numerical_plot_traces(fig, settings, results, hovertemplate, connections,
                                              bus_coords, bus_to_idx, result_values, num_phases,
                                              width_1ph, width_2ph, width_3ph, mode, show_colorbar)
        else:
            self._add_geo_categorical_plot_traces(fig, settings, results, hovertemplate, connections,
                                                bus_coords, bus_to_idx, num_phases,
                                                width_1ph, width_2ph, width_3ph, mode)

        self._add_geo_bus_markers(fig, bus_markers, bus_to_idx, bus_coords)

        self._configure_geo_layout(fig, title, map_style, bus_coords)

        if save_file_path:
            fig.write_html(save_file_path)
        if show:
            fig.show()

        return fig

    def _add_geo_numerical_plot_traces(self, fig, settings, results, hovertemplate, connections,
                                      bus_coords, bus_to_idx, result_values, num_phases,
                                      width_1ph, width_2ph, width_3ph, mode, show_colorbar):
        """Add traces for numerical geographic plots."""
        cmin, cmax = self._calculate_colorbar_range(settings, result_values)
        colorbar_trace_values = np.linspace(cmin, cmax, 100)
        norm_values = (result_values - cmin) / (cmax - cmin)

        rows = []
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
            color = sample_colorscale(settings.colorscale, value)[0]
            width = self._get_phase_width(element, num_phases, width_1ph, width_2ph, width_3ph)
            result_value = results.loc[element]
            # Add two points for the line segment plus a separator
            rows.append({'element': element, 'x': x0, 'y': y0, 'color': color,
                        'bus1': bus1, 'bus2': bus2, 'value': result_value, 'width': width})
            rows.append({'element': element, 'x': x1, 'y': y1, 'color': color,
                        'bus1': bus1, 'bus2': bus2, 'value': result_value, 'width': width})
            rows.append({'element': None, 'x': np.nan, 'y': np.nan, 'color': color,
                        'bus1': np.nan, 'bus2': np.nan, 'value': np.nan, 'width': width})
        geo_df = pd.DataFrame(rows)

        for (color, width), group in geo_df.groupby(['color', 'width']):
            fig.add_trace(go.Scattermap(
                lat=group['y'],
                lon=group['x'],
                mode=mode,
                line=dict(
                    color=color,
                    width=width,
                ),
                name='',
                hoverinfo='skip',
                showlegend=False
            ))

            group_mid = group[['element', 'x', 'y']].groupby('element').mean().reset_index()
            group_mid = pd.merge(group_mid, group[['element', 'bus1', 'bus2', 'value']], on='element')

            fig.add_trace(go.Scattermap(
                lat=group_mid['y'],
                lon=group_mid['x'],
                mode='markers',
                marker=dict(size=0.1, opacity=0, color=color),
                showlegend=False,
                name="",
                hoverinfo='text',
                customdata=group_mid[['element', 'bus1', 'bus2', 'value']],
                hovertemplate=hovertemplate
            ))

        if show_colorbar:
            self._add_geo_colorbar(fig, settings, colorbar_trace_values, cmin, cmax, result_values)

    def _add_geo_categorical_plot_traces(self, fig, settings, results, hovertemplate, connections,
                                        bus_coords, bus_to_idx, num_phases,
                                        width_1ph, width_2ph, width_3ph, mode):
        """Add traces for categorical geographic plots."""
        legend_added = set()
        rows = []
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
            result_value = results.loc[element]
            color = settings.color_map[result_value][1]
            category = settings.color_map[result_value][0]
            width = self._get_phase_width(element, num_phases, width_1ph, width_2ph, width_3ph)
            # Add two points for the line segment plus a separator
            rows.append({'element': element, 'x': x0, 'y': y0, 'color': color,
                        'category': category, 'bus1': bus1, 'bus2': bus2, 'value': result_value, 'width': width})
            rows.append({'element': element, 'x': x1, 'y': y1, 'color': color,
                        'category': category, 'bus1': bus1, 'bus2': bus2, 'value': result_value, 'width': width})
            rows.append({'element': None, 'x': np.nan, 'y': np.nan, 'color': color,
                        'category': category, 'bus1': np.nan, 'bus2': np.nan, 'value': np.nan, 'width': width})
        geo_df = pd.DataFrame(rows)

        for (color, width, category), group in geo_df.groupby(['color', 'width', 'category']):
            show_legend = category not in legend_added
            if show_legend:
                legend_added.add(category)

            fig.add_trace(go.Scattermap(
                lat=group['y'],
                lon=group['x'],
                mode=mode,
                line=dict(
                    color=color,
                    width=width,
                ),
                name=category,
                hoverinfo='skip',
                showlegend=show_legend
            ))

            group_mid = group[['element', 'x', 'y']].groupby('element').mean().reset_index()
            group_mid = pd.merge(group_mid, group[['element', 'bus1', 'bus2', 'value']], on='element')

            fig.add_trace(go.Scattermap(
                lat=group_mid['y'],
                lon=group_mid['x'],
                mode='markers',
                marker=dict(size=0.1, opacity=0, color=color),
                showlegend=False,
                name="",
                hoverinfo='text',
                customdata=group_mid[['element', 'bus1', 'bus2', 'value']],
                hovertemplate=hovertemplate
            ))

        fig.update_layout(
            showlegend=True,
            legend=dict(title=settings.legendgrouptitle_text,
                        x=0.85,
                        y=0.9,
                        traceorder="normal"
                        )
        )

    def _add_geo_colorbar(self, fig, settings, colorbar_trace_values, cmin, cmax, result_values):
        """Add colorbar to the geographic plot."""
        custom_tickvals, custom_ticktext = self._calculate_colorbar_ticks(settings, result_values)

        fig.add_trace(go.Scattermap(
            lat=[None], lon=[None],
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
                    ticktext=custom_ticktext,
                    x=0.9,
                    xanchor='left',
                    yanchor='middle',
                    bgcolor='rgba(0,0,0,0)',
                    borderwidth=0
                ),
                showscale=True
            ),
            hoverinfo='none',
            showlegend=False,
        ))
        fig.update_layout(showlegend=False)

    def _add_geo_bus_markers(self, fig, bus_markers, bus_to_idx, bus_coords):
        """Add bus markers to the geographic plot."""
        if bus_markers:
            for marker in bus_markers:
                if marker.name in bus_to_idx:
                    bus_x, bus_y = bus_coords[bus_to_idx[marker.name]]
                    fig.add_trace(go.Scattermap(
                        lon=[bus_x],
                        lat=[bus_y],
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

    def _configure_geo_layout(self, fig, title, map_style, bus_coords):
        """Configure the geographic plot layout."""
        fig.update_layout(title=title,
                          margin={'r': 0, 't': 32 if title else 0, 'l': 0, 'b': 0},
                          map_style=map_style,
                          autosize=True,
                          hovermode='closest',
                          map=dict(
                              bearing=0,
                              center=dict(
                                  lat=np.mean([lat for _, lat in bus_coords if lat != 0]),
                                  lon=np.mean([lon for lon, _ in bus_coords if lon != 0])
                              ),
                              zoom=10),
                          )
