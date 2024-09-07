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
from typing import Optional, Union, Tuple, List
from py_dss_tools.view.interactive_view.Circuit.ActivePowerSettings import ActivePowerSettings
from py_dss_tools.view.interactive_view.Circuit.VoltageSettings import VoltageSettings
from py_dss_tools.view.interactive_view.Circuit.UserDefinedSettings import UserDefinedSettingsSettings
from py_dss_tools.view.interactive_view.Circuit.PhasesSettings import PhasesSettings


class Circuit:

    def __init__(self, dss: DSS, results: StaticResults):
        self._dss = dss
        self._results = results
        self._plot_style = CustomPlotStyle()
        self._active_power_settings = ActivePowerSettings()
        self._voltage_settings = VoltageSettings()
        self._user_defined_settings = UserDefinedSettingsSettings()
        self._phases_settings = PhasesSettings()

    @property
    def circuit_plot_style(self):
        return self._plot_style

    @property
    def active_power_settings(self):
        return self._active_power_settings

    @property
    def voltage_settings(self):
        return self._voltage_settings

    @property
    def user_defined_settings(self):
        return self._user_defined_settings

    @property
    def phases_settings(self):
        return self._phases_settings

    def circuit_plot(self,
                     parameter="active power",
                     title: Optional[str] = "Circuit Plot",
                     xlabel: Optional[str] = 'X Coordinate',
                     ylabel: Optional[str] = 'Y Coordinate',
                     mark_buses: bool = True,
                     show_colorbar: bool = True,
                     show: bool = True,
                     save_file_path: Optional[str] = None,
                     get_fig_obj: bool = False) -> Optional[go.Figure]:

        if mark_buses:
            mode = 'lines+markers'
        else:
            mode = 'lines'

        numerical_plot = True

        if parameter == "active power":
            settings = self._active_power_settings
            results = self._results.powers_elements[0].iloc[:, :3].sum(axis=1)
            hovertemplate = ("</b>%{customdata[0]}<br>" +
                             "<b>Bus1: </b>%{customdata[1]}<br>" +
                             "<b>Bus2: </b>%{customdata[2]}<br>" +
                             "<b>Total P: </b>%{customdata[3]:.2f} kW<br>")
        elif parameter == "voltage":
            settings = self._voltage_settings
            results = self._results.voltages_elements[0].iloc[:, :3].mean(axis=1)
            hovertemplate = ("</b>%{customdata[0]}<br>" +
                             "<b>Bus1: </b>%{customdata[1]}<br>" +
                             "<b>Bus2: </b>%{customdata[2]}<br>" +
                             "<b>Voltage (pu): </b>%{customdata[3]:.4f} pu<br>")
        elif parameter == "user defined":
            settings = self._user_defined_settings
            if settings.results is None:
                raise Exception("No results found")
            else:
                results = settings.results
                hovertemplate = ("</b>%{customdata[0]}<br>" +
                                 "<b>Bus1: </b>%{customdata[1]}<br>" +
                                 "<b>Bus2: </b>%{customdata[2]}<br>" +
                                 "<b>Voltage (pu): </b>%{customdata[3]:.4f} pu<br>")
        elif parameter == "phases":
            numerical_plot = False
            settings = self._phases_settings
            results = self._results.powers_elements[0].iloc[:, :3].count(axis=1)  # TODO use model later
            hovertemplate = ("</b>%{customdata[0]}<br>" +
                             "<b>Bus1: </b>%{customdata[1]}<br>" +
                             "<b>Bus2: </b>%{customdata[2]}<br>" +
                             "<b>Phases: </b>%{customdata[3]}<br>")

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

        result_values = list()
        for element in elements_list:
            if element.split(".")[0].lower() in ["line"]:
                result_values.append(results.loc[element])
        result_values = np.array(result_values)

        fig = go.Figure()

        if numerical_plot:
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

        if numerical_plot:
            for connection, value in zip(connections, norm_values):
                element, (bus1, bus2) = connection
                x0, y0 = bus_coords[buses.index(bus1)]
                x1, y1 = bus_coords[buses.index(bus2)]

                midpoint_x, midpoint_y = (x0 + x1) / 2, (y0 + y1) / 2

                color = sample_colorscale(settings.colorscale, value)[0]

                customdata = [[element, bus1, bus2, results.loc[element]], [element, bus1, bus2, results.loc[element]]]

                fig.add_trace(go.Scatter(
                    x=[x0, x1], y=[y0, y1],
                    mode=mode,
                    line=dict(color=color, width=3),
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
                    hoverinfo='text',
                    customdata=customdata,
                    hovertemplate=hovertemplate
                ))

            if show_colorbar:

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
                fig.update_layout(
                    showlegend=False)

        else:
            legend_added = set()
            for connection in connections:
                element, (bus1, bus2) = connection
                x0, y0 = bus_coords[buses.index(bus1)]
                x1, y1 = bus_coords[buses.index(bus2)]

                midpoint_x, midpoint_y = (x0 + x1) / 2, (y0 + y1) / 2

                color = settings.color_map[results.loc[element]][1]
                category = settings.color_map[results.loc[element]][0]

                customdata = [[element, bus1, bus2, results.loc[element]], [element, bus1, bus2, results.loc[element]]]

                show_legend = False
                if category not in legend_added:
                    show_legend = True
                    legend_added.add(category)

                fig.add_trace(go.Scatter(
                    x=[x0, x1], y=[y0, y1],
                    mode=mode,
                    line=dict(color=color, width=3),
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
                    hoverinfo='text',
                    customdata=customdata,
                    hovertemplate=hovertemplate,
                    legendgroup="group"
                ))

                fig.update_layout(
                    showlegend=True,
                    legend=dict(
                        x=1,
                        y=1,
                        traceorder="normal"
                    )
                )

        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
        )

        if save_file_path:
            fig.write_html(save_file_path)
        if show:
            fig.show()
        if get_fig_obj:
            return fig
