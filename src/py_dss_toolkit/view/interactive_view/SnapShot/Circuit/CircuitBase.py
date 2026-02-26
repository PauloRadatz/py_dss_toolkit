# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : CircuitBase.py
# @Software: PyCharm

import numpy as np
import pandas as pd
import warnings
from typing import Literal, Optional, List, Tuple
from py_dss_interface import DSS

# Type alias for circuit plot parameter options
CircuitPlotParameter = Literal[
    "active power",
    "reactive power",
    "voltage",
    "user numerical defined",
    "phases",
    "voltage violations",
    "thermal violations",
    "user categorical defined",
    "distance"
]
from py_dss_toolkit.results.SnapShot.SnapShotPowerFlowResults import SnapShotPowerFlowResults
from py_dss_toolkit.model.ModelBase import ModelBase
from py_dss_toolkit.view.interactive_view.InteractiveCustomPlotStyle import InteractiveCustomPlotStyle
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.ActivePowerSettings import ActivePowerSettings
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.VoltageSettings import VoltageSettings
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.UserDefinedNumericalSettings import UserDefinedNumericalSettings
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.UserDefinedCategoricalSettings import UserDefinedCategoricalSettings
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.PhasesSettings import PhasesSettings
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.ThermalViolationSettings import ThermalViolationSettings
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.VoltageViolationSettings import VoltageViolationSettings
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.DistanceSettings import DistanceSettings
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitBusMarker import CircuitBusMarker


class PlotParameterStrategy:
    """Base class for plot parameter strategies."""

    def __init__(self, circuit_instance: "CircuitBase"):
        """
        Initialize the strategy with a CircuitBase instance.

        Args:
            circuit_instance: The CircuitBase instance that provides access to
                settings, results, model, and DSS interface.
        """
        self._circuit = circuit_instance

    def get_settings_and_results(self, lines_df: "pd.DataFrame" = None):
        """Return (settings, results, hovertemplate, numerical_plot)"""
        raise NotImplementedError


class ActivePowerStrategy(PlotParameterStrategy):
    def get_settings_and_results(self, lines_df=None):
        settings = self._circuit._active_power_settings
        columns = self._circuit._results.powers_elements[0].columns
        if "Terminal1.1" not in columns or "Terminal1.2" not in columns or "Terminal1.3" not in columns:
            raise ValueError("A non 3-phase circuit can't be plotted")
        results = self._circuit._results.powers_elements[0].loc[:, ["Terminal1.1", "Terminal1.2", "Terminal1.3"]].sum(axis=1)
        hovertemplate = ("<b>%{customdata[0]}</b><br>" +
                        "<b>Bus1: </b>%{customdata[1]} | <b>Bus2: </b>%{customdata[2]}<br>" +
                        "<b>Total P: </b>%{customdata[3]:.2f} kW<br>")
        return settings, results, hovertemplate, True


class ReactivePowerStrategy(PlotParameterStrategy):
    def get_settings_and_results(self, lines_df=None):
        settings = self._circuit._active_power_settings
        columns = self._circuit._results.powers_elements[1].columns
        if "Terminal1.1" not in columns or "Terminal1.2" not in columns or "Terminal1.3" not in columns:
            raise ValueError("A non 3-phase circuit can't be plotted")
        results = self._circuit._results.powers_elements[1].loc[:, ["Terminal1.1", "Terminal1.2", "Terminal1.3"]].sum(axis=1)
        hovertemplate = ("<b>%{customdata[0]}</b><br>" +
                        "<b>Bus1: </b>%{customdata[1]} | <b>Bus2: </b>%{customdata[2]}<br>" +
                        "<b>Total Q: </b>%{customdata[3]:.2f} kvar<br>")
        return settings, results, hovertemplate, True


class VoltageStrategy(PlotParameterStrategy):
    def get_settings_and_results(self, lines_df=None):
        settings = self._circuit._voltage_settings
        bus = settings.bus
        columns = self._circuit._results.voltages_elements[0].columns
        if bus == "bus1":
            p = 1
        else:
            p = 2
        if "Terminal1.1" not in columns or "Terminal1.2" not in columns or "Terminal1.3" not in columns:
            raise ValueError("A non 3-phase circuit can't be plotted")
        v = self._circuit._results.voltages_elements[0].loc[:, [f"Terminal{p}.1", f"Terminal{p}.2", f"Terminal{p}.3"]]
        if settings.nodes_voltage_value == "mean":
            results = v.mean(axis=1)
        elif settings.nodes_voltage_value == "min":
            results = v.min(axis=1)
        elif settings.nodes_voltage_value == "max":
            results = v.max(axis=1)
        hovertemplate = ("<b>%{customdata[0]}</b><br>" +
                        "<b>Bus1: </b>%{customdata[1]} | <b>Bus2: </b>%{customdata[2]}<br>" +
                        f"<b>{settings.nodes_voltage_value.capitalize()} {bus.capitalize()} Voltage: </b>" +
                        "%{customdata[3]:.4f} pu<br>")
        return settings, results, hovertemplate, True


class UserNumericalDefinedStrategy(PlotParameterStrategy):
    def get_settings_and_results(self, lines_df=None):
        settings = self._circuit._user_numerical_defined_settings
        parameter = settings.parameter
        unit = settings.unit
        num_decimal_points = settings.num_decimal_points
        if settings.results is None:
            raise ValueError(f"No results found for 'user numerical defined' parameter. "
                           f"Please set the results using: "
                           f"circuit.user_numerical_defined_settings.results = your_data")
        else:
            results = settings.results
            hovertemplate = ("<b>%{customdata[0]}</b><br>" +
                            "<b>Bus1: </b>%{customdata[1]} | <b>Bus2: </b>%{customdata[2]}<br>" +
                            f"<b>{parameter}:</b>" + " %{customdata[3]:" + f".{num_decimal_points}" + "f}" + f" {unit}<br>")
        return settings, results, hovertemplate, True


class PhasesStrategy(PlotParameterStrategy):
    def get_settings_and_results(self, lines_df=None):
        settings = self._circuit._phases_settings
        if lines_df is None:
            lines_df = self._circuit._model.lines_df
            lines_df['name'] = 'line.' + lines_df['name']
        results = lines_df.set_index("name")["phases"]
        hovertemplate = ("<b>%{customdata[0]}</b><br>" +
                        "<b>Bus1: </b>%{customdata[1]} | <b>Bus2: </b>%{customdata[2]}<br>" +
                        "<b>Phases: </b>%{customdata[3]}<br>")
        return settings, results, hovertemplate, False


class VoltageViolationsStrategy(PlotParameterStrategy):
    def get_settings_and_results(self, lines_df=None):
        settings = self._circuit._voltage_violation_settings
        under_v_bus_violations = self._circuit._results.violation_voltage_ln_nodes[0].index
        over_v_bus_violations = self._circuit._results.violation_voltage_ln_nodes[1].index
        both_v_bus_violations = under_v_bus_violations.intersection(over_v_bus_violations)
        if lines_df is None:
            lines_df = self._circuit._model.lines_df
            lines_df['name'] = 'line.' + lines_df['name']
        results = lines_df.set_index("name")
        results["bus"] = results['bus1'].str.split('.', n=1).str[0]
        results["violation"] = "0"
        results.loc[results['bus'].isin(under_v_bus_violations), 'violation'] = "1"
        results.loc[results['bus'].isin(over_v_bus_violations), 'violation'] = "2"
        results.loc[results['bus'].isin(both_v_bus_violations), 'violation'] = "3"
        results = results["violation"]
        hovertemplate = ("<b>%{customdata[0]}</b><br>" +
                        "<b>Bus1: </b>%{customdata[1]} | <b>Bus2: </b>%{customdata[2]}<br>")
        return settings, results, hovertemplate, False


class ThermalViolationsStrategy(PlotParameterStrategy):
    def get_settings_and_results(self, lines_df=None):
        settings = self._circuit._thermal_violation_settings
        line_violations = self._circuit._results.violation_currents_elements.index
        if lines_df is None:
            lines_df = self._circuit._model.lines_df
            lines_df['name'] = 'line.' + lines_df['name']
        results = lines_df.set_index("name")
        results["violation"] = "0"
        results.loc[results.index.isin(line_violations), 'violation'] = "1"
        results = results["violation"]
        hovertemplate = ("<b>%{customdata[0]}</b><br>" +
                        "<b>Bus1: </b>%{customdata[1]} | <b>Bus2: </b>%{customdata[2]}<br>")
        return settings, results, hovertemplate, False


class UserCategoricalDefinedStrategy(PlotParameterStrategy):
    def get_settings_and_results(self, lines_df=None):
        settings = self._circuit._user_categorical_defined_settings
        parameter = settings.parameter
        if settings.results is None:
            raise ValueError(f"No results found for 'user categorical defined' parameter. "
                           f"Please set the results using: "
                           f"circuit.user_categorical_defined_settings.results = your_data")
        else:
            results = settings.results
            hovertemplate = ("<b>%{customdata[0]}</b><br>" +
                            "<b>Bus1: </b>%{customdata[1]} | <b>Bus2: </b>%{customdata[2]}<br>" +
                            f"<b>{parameter}:</b>" + " %{customdata[3]}")
        return settings, results, hovertemplate, False

class DistanceStrategy(PlotParameterStrategy):
    def get_settings_and_results(self, lines_df=None):
        """
        Calculate distance from energymeter for each line element.

        For each line, uses the maximum distance of its two connected buses
        from the energymeter as the line's distance value.
        """
        settings = self._circuit._distance_settings

        if self._circuit._dss.meters.count == 0:
            raise ValueError("No energymeter found. Distance plotting requires at least one energymeter in the circuit.")

        buses_df = self._circuit._model.buses_df
        bus_distance_map = {
            bus_name.lower().split(".")[0]: distance
            for bus_name, distance in zip(buses_df['name'], buses_df['distance'])
        }

        if lines_df is not None:
            line_df = lines_df.copy()
        else:
            line_df = self._circuit._model.lines_df.copy()
            line_df['name'] = 'line.' + line_df['name']

        line_df['bus1_name'] = line_df['bus1'].str.split('.').str[0].str.lower()
        line_df['bus2_name'] = line_df['bus2'].str.split('.').str[0].str.lower()

        line_df['bus1_dist'] = line_df['bus1_name'].map(bus_distance_map)
        line_df['bus2_dist'] = line_df['bus2_name'].map(bus_distance_map)

        line_df['distance'] = line_df[['bus1_dist', 'bus2_dist']].max(axis=1)

        # Return DataFrame with distance info for customdata construction
        results = line_df.set_index("name")['distance']

        hovertemplate = ("<b>%{customdata[0]}</b><br>" +
                        "<b>Bus1: </b>%{customdata[1]} | <b>Bus2: </b>%{customdata[2]}<br>" +
                        "<b>Bus farthest from Energymeter: </b>%{customdata[3]:.2f} km<br>")
        return settings, results, hovertemplate, True

class CircuitSettingsContainer:
    """Container for circuit plot settings to enable dependency injection."""

    def __init__(self, circuit_base_instance):
        """Initialize settings container from a CircuitBase instance."""
        self._plot_style = circuit_base_instance._plot_style
        self._active_power_settings = circuit_base_instance._active_power_settings
        self._voltage_settings = circuit_base_instance._voltage_settings
        self._user_numerical_defined_settings = circuit_base_instance._user_numerical_defined_settings
        self._user_categorical_defined_settings = circuit_base_instance._user_categorical_defined_settings
        self._phases_settings = circuit_base_instance._phases_settings
        self._thermal_violation_settings = circuit_base_instance._thermal_violation_settings
        self._voltage_violation_settings = circuit_base_instance._voltage_violation_settings
        self._distance_settings = circuit_base_instance._distance_settings
        self._parameter_strategies = circuit_base_instance._parameter_strategies


class CircuitBase:
    """Base class containing shared logic for circuit plotting."""

    def __init__(self, dss: DSS, results: SnapShotPowerFlowResults, model: ModelBase,
                 settings_container: Optional[CircuitSettingsContainer] = None):
        """
        Initialize CircuitBase.

        Args:
            dss: DSS interface instance
            results: Power flow results
            model: Model data
            settings_container: Optional shared settings container. If None, creates new settings.
        """
        self._dss = dss
        self._results = results
        self._model = model

        if settings_container is not None:
            # Use shared settings from container
            self._plot_style = settings_container._plot_style
            self._active_power_settings = settings_container._active_power_settings
            self._voltage_settings = settings_container._voltage_settings
            self._user_numerical_defined_settings = settings_container._user_numerical_defined_settings
            self._user_categorical_defined_settings = settings_container._user_categorical_defined_settings
            self._phases_settings = settings_container._phases_settings
            self._thermal_violation_settings = settings_container._thermal_violation_settings
            self._voltage_violation_settings = settings_container._voltage_violation_settings
            self._distance_settings = settings_container._distance_settings
            self._parameter_strategies = settings_container._parameter_strategies
        else:
            # Create new settings instances
            self._plot_style = InteractiveCustomPlotStyle()
            self._active_power_settings = ActivePowerSettings()
            self._voltage_settings = VoltageSettings()
            self._user_numerical_defined_settings = UserDefinedNumericalSettings()
            self._user_categorical_defined_settings = UserDefinedCategoricalSettings()
            self._phases_settings = PhasesSettings()
            self._thermal_violation_settings = ThermalViolationSettings()
            self._voltage_violation_settings = VoltageViolationSettings()
            self._distance_settings = DistanceSettings()

            # Strategy pattern mapping for plot parameters
            self._parameter_strategies = {
                "active power": ActivePowerStrategy(self),
                "reactive power": ReactivePowerStrategy(self),
                "voltage": VoltageStrategy(self),
                "user numerical defined": UserNumericalDefinedStrategy(self),
                "phases": PhasesStrategy(self),
                "voltage violations": VoltageViolationsStrategy(self),
                "thermal violations": ThermalViolationsStrategy(self),
                "user categorical defined": UserCategoricalDefinedStrategy(self),
                "distance": DistanceStrategy(self)
            }

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

    @property
    def distance_settings(self):
        return self._distance_settings

    def _get_plot_settings(self, parameter: CircuitPlotParameter, lines_df: pd.DataFrame = None):
        """
        Helper to get settings, results, hovertemplate, and numerical_plot for a given parameter.

        Supported parameters:
            - 'active power': Plots total active power (kW) per line.
            - 'reactive power': Plots total reactive power (kvar) per line.
            - 'voltage': Plots voltage statistics (mean/min/max) per line terminal.
            - 'user numerical defined': Plots user-defined numerical results.
            - 'phases': Plots the number of phases per line.
            - 'user categorical defined': Plots user-defined categorical results.
            - 'voltage violations': Highlights lines connected to buses with voltage violations.
            - 'thermal violations': Highlights lines with thermal (current) violations.
            - 'distance': Plots distance from energymeter (km) per line.

        Returns:
            settings: The settings object for the parameter.
            results: The results Series/DataFrame for plotting.
            hovertemplate: The hovertemplate string for Plotly.
            numerical_plot: Boolean, True if the plot is numerical/continuous, False if categorical/binary.
        """
        if parameter not in self._parameter_strategies:
            raise ValueError(f"Unknown parameter: {parameter}. Supported parameters: {list(self._parameter_strategies.keys())}")

        strategy = self._parameter_strategies[parameter]
        return strategy.get_settings_and_results(lines_df=lines_df)

    def _prepare_plot_data(self, parameter: CircuitPlotParameter, warn_zero_coord_buses: bool = False):
        """
        Prepare common data for both circuit_plot and circuit_geoplot methods.

        Returns:
            dict: Contains all the data needed for plotting
        """
        line_df = self._model.lines_df.copy()
        line_df['name'] = 'line.' + line_df['name']
        settings, results, hovertemplate, numerical_plot = self._get_plot_settings(parameter, lines_df=line_df)
        num_phases = line_df.set_index("name")["phases"]
        line_type = line_df.set_index("name")["linetype"]

        segments_df = self._model.segments_df
        line_segments = segments_df[
            (segments_df["type"] == "line") & (segments_df["enabled"])
        ]

        if len(line_segments) > 0:
            bus1_df = line_segments[["bus1", "x1", "y1"]].rename(
                columns={"bus1": "bus", "x1": "x", "y1": "y"}
            )
            bus2_df = line_segments[["bus2", "x2", "y2"]].rename(
                columns={"bus2": "bus", "x2": "x", "y2": "y"}
            )
            bus_coords_df = pd.concat([bus1_df, bus2_df]).drop_duplicates(
                subset=["bus"], keep="first"
            )
            bus_to_coord = {
                str(r.bus).lower(): (float(r.x), float(r.y))
                for r in bus_coords_df.itertuples(index=False)
            }
        else:
            bus_to_coord = {}

        buses = sorted(bus_to_coord.keys())
        bus_coords = np.array([bus_to_coord[b] for b in buses])
        zero_coord_buses = [b for b in buses if bus_to_coord[b] == (0.0, 0.0)]
        connections = [
            [r.name, (str(r.bus1).lower(), str(r.bus2).lower())]
            for r in line_segments.itertuples(index=False)
        ]
        if len(line_segments) > 0:
            result_values = results.loc[line_segments["name"]].values
        else:
            result_values = np.array([])

        # Check if all buses have undefined coordinates
        if len(zero_coord_buses) == len(buses) and len(buses) > 0:
            raise ValueError(
                "All buses have undefined coordinates (0,0). "
                "Please define bus coordinates using the 'buscoords' command in OpenDSS or set bus x/y properties."
            )

        # Warn if some buses with undefined coordinates were found
        if warn_zero_coord_buses and zero_coord_buses and len(zero_coord_buses) < len(buses):
            warnings.warn(
                f"{len(zero_coord_buses)} bus(es) have undefined coordinates (0,0) and will be skipped in the plot. "
                f"OpenDSS uses (0,0) to indicate undefined coordinates. "
                f"First few buses: {', '.join(zero_coord_buses[:5])}{'...' if len(zero_coord_buses) > 5 else ''}",
                UserWarning,
                stacklevel=3
            )

        # Create bus-to-index mapping for O(1) lookups in plotting methods
        bus_to_idx = {bus: idx for idx, bus in enumerate(buses)}

        return {
            'settings': settings,
            'results': results,
            'hovertemplate': hovertemplate,
            'numerical_plot': numerical_plot,
            'line_df': line_df,
            'num_phases': num_phases,
            'line_type': line_type,
            'buses': buses,
            'bus_coords': bus_coords,
            'bus_to_idx': bus_to_idx,
            'connections': connections,
            'result_values': result_values
        }

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

    def _calculate_colorbar_range(self, settings, result_values: np.ndarray) -> Tuple[float, float]:
        """
        Calculate the colorbar min and max values.

        Args:
            settings: The settings object containing colorbar_cmin and colorbar_cmax.
            result_values: Array of result values.

        Returns:
            tuple: (cmin, cmax) values for the colorbar.
        """
        cmin = settings.colorbar_cmin if settings.colorbar_cmin is not None else np.min(result_values)
        cmax = settings.colorbar_cmax if settings.colorbar_cmax is not None else np.max(result_values)
        return cmin, cmax

    def _calculate_colorbar_ticks(self, settings, result_values: np.ndarray) -> Tuple[Optional[np.ndarray], Optional[List[str]]]:
        """
        Calculate the colorbar tick values and text.

        Args:
            settings: The settings object containing colorbar tick configuration.
            result_values: Array of result values.

        Returns:
            tuple: (tickvals, ticktext) for the colorbar, or (None, None) if using defaults.
        """
        custom_tickvals = None
        custom_ticktext = None

        if settings.colorbar_tickvals is not None:
            custom_tickvals = np.linspace(np.min(result_values), np.max(result_values),
                                          settings.colorbar_tickvals)
            if settings.colorbar_ticktext_decimal_points:
                custom_ticktext = [f"{v:.{settings.colorbar_ticktext_decimal_points}f}" for v in
                                   custom_tickvals]
            else:
                custom_ticktext = [f"{v:.0f}" for v in custom_tickvals]

        if settings.colorbar_tickvals_list:
            custom_tickvals = settings.colorbar_tickvals_list
            custom_ticktext = settings.colorbar_tickvals_list

        return custom_tickvals, custom_ticktext
