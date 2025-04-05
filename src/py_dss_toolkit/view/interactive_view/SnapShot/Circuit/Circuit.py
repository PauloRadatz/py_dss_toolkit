# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : Circuit.py
# @Software: PyCharm

import plotly.graph_objects as go
from plotly.colors import sample_colorscale
from py_dss_toolkit.results.SnapShot.SnapShotPowerFlowResults import SnapShotPowerFlowResults
from py_dss_toolkit.model.ModelBase import ModelBase
from py_dss_interface import DSS
from py_dss_toolkit.view.interactive_view.InteractiveCustomPlotStyle import InteractiveCustomPlotStyle
import numpy as np
from typing import Optional, List
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.ActivePowerSettings import ActivePowerSettings
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.VoltageSettings import VoltageSettings
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.UserDefinedNumericalSettings import UserDefinedNumericalSettings
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.UserDefinedCategoricalSettings import UserDefinedCategoricalSettings
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.PhasesSettings import PhasesSettings
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitBusMarker import CircuitBusMarker


class Circuit:

    def __init__(self, dss: DSS, results: SnapShotPowerFlowResults, model: ModelBase):
        self._dss = dss
        self._results = results
        self._model = model
        self._plot_style = InteractiveCustomPlotStyle()
        self._active_power_settings = ActivePowerSettings()
        self._voltage_settings = VoltageSettings()
        self._user_numerical_defined_settings = UserDefinedNumericalSettings()
        self._user_categorical_defined_settings = UserDefinedCategoricalSettings()
        self._phases_settings = PhasesSettings()

    def circuit_get_bus_marker(self, name: str, symbol: str = "square",
                               size: float = 10,
                               color: str = "black",
                               marker_name: Optional[str] = None):
        if not marker_name:
            marker_name = name
        return CircuitBusMarker(name=name,
                                symbol=symbol,
                                size=size,
                                color=color,
                                marker_name=marker_name)

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
    def user_numerical_defined_settings(self):
        return self._user_numerical_defined_settings

    @property
    def phases_settings(self):
        return self._phases_settings

    @property
    def user_categorical_defined_settings(self):
        return self._user_categorical_defined_settings

    def circuit_plot(self,
                     parameter="active power",
                     title: Optional[str] = "Circuit Plot",
                     xlabel: Optional[str] = 'X Coordinate',
                     ylabel: Optional[str] = 'Y Coordinate',
                     width_3ph: int = 3,
                     width_2ph: int = 3,
                     width_1ph: int = 3,
                     dash_3ph: Optional[str] = None,  #https://chart-studio.plotly.com/~neda/1950/solid-dashdot-dash-dot.embed
                     dash_2ph: Optional[str] = None,
                     dash_1ph: Optional[str] = None,
                     dash_oh: Optional[str] = None,
                     dash_ug: Optional[str] = None,
                     mark_buses: bool = True,
                     bus_markers: Optional[List[CircuitBusMarker]] = None,
                     show_colorbar: bool = True,
                     show: bool = True,
                     save_file_path: Optional[str] = None) -> Optional[go.Figure]:

        if mark_buses:
            mode = 'lines+markers'
        else:
            mode = 'lines'

        numerical_plot = True

        line_df = self._model.lines_df
        line_df['name'] = 'line.' + line_df['name']
        num_phases = line_df.set_index("name")["phases"]
        line_type = line_df.set_index("name")["linetype"]

        hovertemplate = ("<b>%{customdata[0]}</b><br>" +
                         "<b>Bus1: </b>%{customdata[1]} | <b>Bus2: </b>%{customdata[2]}<br>")
        if parameter == "active power":
            settings = self._active_power_settings
            results = self._results.powers_elements[0].iloc[:, :3].sum(axis=1)
            hovertemplate = hovertemplate + "<b>Total P: </b>%{customdata[3]:.2f} kW<br>"
        elif parameter == "voltage":
            settings = self._voltage_settings
            bus = settings.bus
            if settings.nodes_voltage_value == "mean":
                results = self._results.voltages_elements[0].iloc[:, :3].mean(axis=1)
            elif settings.nodes_voltage_value == "min":
                results = self._results.voltages_elements[0].iloc[:, :3].min(axis=1)
            elif settings.nodes_voltage_value == "max":
                results = self._results.voltages_elements[0].iloc[:, :3].max(axis=1)
            hovertemplate = (hovertemplate +
                             f"<b>{settings.nodes_voltage_value.capitalize()} {bus.capitalize()} Voltage: </b>" +
                             "%{customdata[3]:.4f} pu<br>")
        elif parameter == "user numerical defined":
            settings = self._user_numerical_defined_settings
            parameter = settings.parameter
            unit = settings.unit
            num_decimal_points = settings.num_decimal_points
            if settings.results is None:
                raise Exception("No results found")
            else:
                results = settings.results
                hovertemplate = hovertemplate + f"<b>{parameter}:</b>" + " %{customdata[3]:" + f".{num_decimal_points}" + "f}" + f" {unit}<br>"
        elif parameter == "phases":
            numerical_plot = False
            settings = self._phases_settings
            results = num_phases
            hovertemplate = hovertemplate + "<b>Phases: </b>%{customdata[3]}<br>"
        elif parameter == "user categorical defined":
            numerical_plot = False
            settings = self._user_categorical_defined_settings
            parameter = settings.parameter

            if settings.results is None:
                raise Exception("No results found")
            else:
                results = settings.results
                hovertemplate = hovertemplate + f"<b>{parameter}:</b>" + " %{customdata[3]}"


        buses = list()
        bus_coords = list()
        elements_list = [element.lower() for element in self._dss.circuit.elements_names]
        connections = []

        for element in elements_list:
            if element.split(".")[0].lower() in ["line"]:
                self._dss.circuit.set_active_element(element)
                if self._dss.cktelement.is_enabled:
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
                self._dss.circuit.set_active_element(element)
                if self._dss.cktelement.is_enabled:
                    result_values.append(results.loc[element])
        result_values = np.array(result_values)

        fig = go.Figure()
        self._plot_style.apply_style(fig)

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

            for connection, value in zip(connections, norm_values):
                element, (bus1, bus2) = connection
                x0, y0 = bus_coords[buses.index(bus1)]
                x1, y1 = bus_coords[buses.index(bus2)]

                if x0 == 0 and y0 == 0:
                    continue
                if x1 == 0 and y1 == 0:
                    continue

                midpoint_x, midpoint_y = (x0 + x1) / 2, (y0 + y1) / 2

                color = sample_colorscale(settings.colorscale, value)[0]

                customdata = [[element, bus1, bus2, results.loc[element]], [element, bus1, bus2, results.loc[element]]]

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

                if x0 == 0 and y0 == 0:
                    continue
                if x1 == 0 and y1 == 0:
                    continue

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
                        x=1,
                        y=1,
                        traceorder="normal"
                    )
                )

        if bus_markers:
            for marker in bus_markers:
                if marker.name in buses:
                    index = buses.index(marker.name)
                    bus_x, bus_y = bus_coords[index]
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

    def _get_phase_width(self, element, num_phases, width_1ph, width_2ph, width_3ph):
        num_phase = int(num_phases[element])
        if num_phase >= 3:
            result = width_3ph
        elif num_phase == 2:
            result = width_2ph
        elif num_phase == 1:
            result = width_1ph
        return result

    def _get_dash(self, element, num_phases, dash_1ph, dash_2ph, dash_3ph, line_type, dash_oh, dash_ug):
        num_phase = int(num_phases[element])
        lt = line_type[element]
        default = 'solid'
        if num_phase >= 3 and dash_3ph is not None:
            return dash_3ph
        elif num_phase == 2 and dash_2ph is not None:
            return dash_2ph
        elif num_phase == 1 and dash_1ph is not None:
            return dash_1ph
        elif lt == 'oh' and dash_oh is not None:
            return dash_oh
        elif lt == 'ug' and dash_ug is not None:
            return dash_ug
        return default
