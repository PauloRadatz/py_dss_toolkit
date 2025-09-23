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
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitBase import CircuitBase
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitBusMarker import CircuitBusMarker


class CircuitGeoPlot(CircuitBase):
    """Class for creating geographic circuit plots."""

    def circuit_geoplot(self,
                        parameter="active power",
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
        connections = plot_data['connections']
        result_values = plot_data['result_values']

        fig = go.Figure()

        if numerical_plot:
            self._add_geo_numerical_plot_traces(fig, settings, results, hovertemplate, connections,
                                              buses, bus_coords, result_values, num_phases,
                                              width_1ph, width_2ph, width_3ph, mode, show_colorbar)
        else:
            self._add_geo_categorical_plot_traces(fig, settings, results, hovertemplate, connections,
                                                buses, bus_coords, num_phases,
                                                width_1ph, width_2ph, width_3ph, mode)

        self._add_geo_bus_markers(fig, bus_markers, buses, bus_coords)
        
        self._configure_geo_layout(fig, title, map_style, bus_coords)

        if save_file_path:
            fig.write_html(save_file_path)
        if show:
            fig.show()

        return fig

    def _add_geo_numerical_plot_traces(self, fig, settings, results, hovertemplate, connections,
                                      buses, bus_coords, result_values, num_phases,
                                      width_1ph, width_2ph, width_3ph, mode, show_colorbar):
        """Add traces for numerical geographic plots."""
        if not settings.colorbar_cmin:
            cmin = np.min(result_values)
        else:
            cmin = settings.colorbar_cmin

        if not settings.colorbar_cmax:
            cmax = np.max(result_values)
        else:
            cmax = settings.colorbar_cmax

        colorbar_trace_values = np.linspace(cmin, cmax, 100)
        norm_values = (result_values - cmin) / (cmax - cmin)

        geo_df = pd.DataFrame()
        for connection, value in zip(connections, norm_values):
            element, (bus1, bus2) = connection
            x0, y0 = bus_coords[buses.index(bus1)]
            x1, y1 = bus_coords[buses.index(bus2)]
            if x0 == 0 and y0 == 0:
                continue
            if x1 == 0 and y1 == 0:
                continue
            color = sample_colorscale(settings.colorscale, value)[0]
            width = self._get_phase_width(element, num_phases, width_1ph, width_2ph, width_3ph)
            temp = pd.DataFrame({'element': [element, element, None],
                                'x': [x0, x1, np.nan],
                                'y': [y0, y1, np.nan],
                                'color': [color, color, color],
                                'bus1': [bus1, bus1, np.nan],
                                'bus2': [bus2, bus2, np.nan],
                                'value': [results.loc[element], results.loc[element], np.nan],
                                'width': [width, width, width],
                                })
            geo_df = pd.concat([geo_df, temp], axis=0, ignore_index=True)

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
                                        buses, bus_coords, num_phases,
                                        width_1ph, width_2ph, width_3ph, mode):
        """Add traces for categorical geographic plots."""
        legend_added = set()
        geo_df = pd.DataFrame()
        for connection in connections:
            element, (bus1, bus2) = connection
            x0, y0 = bus_coords[buses.index(bus1)]
            x1, y1 = bus_coords[buses.index(bus2)]
            if x0 == 0 and y0 == 0:
                continue
            if x1 == 0 and y1 == 0:
                continue
            color = settings.color_map[results.loc[element]][1]
            category = settings.color_map[results.loc[element]][0]
            width = self._get_phase_width(element, num_phases, width_1ph, width_2ph, width_3ph)
            temp = pd.DataFrame({'element': [element, element, None],
                                'x': [x0, x1, np.nan],
                                'y': [y0, y1, np.nan],
                                'color': [color, color, color],
                                'category': [category, category, category],
                                'bus1': [bus1, bus1, np.nan],
                                'bus2': [bus2, bus2, np.nan],
                                'value': [results.loc[element], results.loc[element], np.nan],
                                'width': [width, width, width],
                                })
            geo_df = pd.concat([geo_df, temp], axis=0, ignore_index=True)

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
        if settings.colorbar_tickvals is not None:
            custom_tickvals = np.linspace(np.min(result_values), np.max(result_values),
                                          settings.colorbar_tickvals)
            if settings.colorbar_ticktext_decimal_points:
                custom_ticktext = [f"{v:.{settings.colorbar_ticktext_decimal_points}f}" for v in
                                   custom_tickvals]
            else:
                custom_ticktext = [f"{v:.{0}f}" for v in custom_tickvals]
        else:
            custom_tickvals = None
            custom_ticktext = None

        if settings.colorbar_tickvals_list:
            custom_tickvals = settings.colorbar_tickvals_list
            custom_ticktext = settings.colorbar_tickvals_list

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

    def _add_geo_bus_markers(self, fig, bus_markers, buses, bus_coords):
        """Add bus markers to the geographic plot."""
        if bus_markers:
            for marker in bus_markers:
                if marker.name in buses:
                    index = buses.index(marker.name)
                    bus_x, bus_y = bus_coords[index]
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
