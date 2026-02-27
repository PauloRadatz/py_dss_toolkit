# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : Circuit.py
# @Software: PyCharm

import plotly.graph_objects as go
from typing import Optional, List
from py_dss_interface import DSS
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitBase import CircuitPlotParameter
from py_dss_toolkit.results.SnapShot.SnapShotPowerFlowResults import SnapShotPowerFlowResults
from py_dss_toolkit.model.ModelBase import ModelBase
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitBase import CircuitBase
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitPlot import CircuitPlot
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitGeoPlot import CircuitGeoPlot
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitBusMarker import CircuitBusMarker
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitBase import CircuitSettingsContainer


class Circuit(CircuitBase):
    """
    Main Circuit class that combines regular and geographic plotting functionality.

    This class uses composition to delegate plotting functionality to specialized
    CircuitPlot and CircuitGeoPlot classes while maintaining the same API.

    The class maintains the same API as before, but now the implementation is split
    across multiple focused classes for better maintainability.
    """

    def __init__(self, dss: DSS, results: SnapShotPowerFlowResults, model: ModelBase):
        # Initialize the base class which contains all shared logic
        super().__init__(dss, results, model)

        settings_container = CircuitSettingsContainer(self)

        # Create instances of the specialized plotting classes with shared settings
        self._circuit_plot = CircuitPlot(dss, results, model, settings_container=settings_container)
        self._circuit_geoplot = CircuitGeoPlot(dss, results, model, settings_container=settings_container)

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
                     warn_zero_coord_buses: bool = False,
                     show: bool = False,
                     save_file_path: Optional[str] = None) -> go.Figure:
        """
        Create an interactive circuit plot.

        Args:
            parameter (CircuitPlotParameter): The parameter to plot. One of: "active power",
                "reactive power", "voltage", "user numerical defined", "phases",
                "voltage violations", "thermal violations", "user categorical defined",
                "distance". Defaults to "active power".
            title (Optional[str]): Plot title. Defaults to "Circuit Plot".
            xlabel (Optional[str]): X-axis label. Defaults to 'X Coordinate'.
            ylabel (Optional[str]): Y-axis label. Defaults to 'Y Coordinate'.
            width_3ph (int): Line width for 3-phase elements. Defaults to 3.
            width_2ph (int): Line width for 2-phase elements. Defaults to 3.
            width_1ph (int): Line width for 1-phase elements. Defaults to 3.
            dash_3ph (Optional[str]): Dash pattern for 3-phase lines (e.g., "solid", "dash",
                "dot"). None uses default. Defaults to None.
            dash_2ph (Optional[str]): Dash pattern for 2-phase lines. None uses default.
                Defaults to None.
            dash_1ph (Optional[str]): Dash pattern for 1-phase lines. None uses default.
                Defaults to None.
            dash_oh (Optional[str]): Dash pattern for overhead lines. None uses default.
                Defaults to None.
            dash_ug (Optional[str]): Dash pattern for underground lines. None uses default.
                Defaults to None.
            mark_buses (bool): Whether to show bus markers. Defaults to True.
            bus_markers (Optional[List[CircuitBusMarker]]): Custom bus markers to display.
                Defaults to None.
            show_colorbar (bool): Whether to show the colorbar. Defaults to True.
            warn_zero_coord_buses (bool): If True, show warning when buses have undefined (0,0)
                coordinates. Defaults to False.
            show (bool): Whether to display the plot immediately. Defaults to False.
            save_file_path (Optional[str]): Path to save the plot as HTML file. Defaults to None.

        Returns:
            go.Figure: The Plotly figure object.
        """
        return self._circuit_plot.circuit_plot(
            parameter=parameter,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            width_3ph=width_3ph,
            width_2ph=width_2ph,
            width_1ph=width_1ph,
            dash_3ph=dash_3ph,
            dash_2ph=dash_2ph,
            dash_1ph=dash_1ph,
            dash_oh=dash_oh,
            dash_ug=dash_ug,
            mark_buses=mark_buses,
            bus_markers=bus_markers,
            show_colorbar=show_colorbar,
            warn_zero_coord_buses=warn_zero_coord_buses,
            show=show,
            save_file_path=save_file_path
        )

    def circuit_geoplot(self,
                        parameter: CircuitPlotParameter = "active power",
                        title: Optional[str] = "Circuit Plot",
                        width_3ph: int = 3,
                        width_2ph: int = 3,
                        width_1ph: int = 3,
                        mark_buses: bool = True,
                        bus_markers: Optional[List[CircuitBusMarker]] = None,
                        show_colorbar: bool = True,
                        warn_zero_coord_buses: bool = False,
                        show: bool = False,
                        map_style: Optional[str] = 'open-street-map',
                        save_file_path: Optional[str] = None) -> go.Figure:
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
            parameter (CircuitPlotParameter): The parameter to plot. One of: "active power",
                "reactive power", "voltage", "user numerical defined", "phases",
                "voltage violations", "thermal violations", "user categorical defined",
                "distance". Defaults to "active power".
            title (Optional[str]): Title for the plot. Defaults to "Circuit Plot".
            width_3ph (int): Line width for 3-phase elements. Defaults to 3.
            width_2ph (int): Line width for 2-phase elements. Defaults to 3.
            width_1ph (int): Line width for 1-phase elements. Defaults to 3.
            mark_buses (bool): Whether to show bus markers. Defaults to True.
            bus_markers (Optional[List[CircuitBusMarker]]): Custom bus markers to display.
                Defaults to None.
            show_colorbar (bool): Whether to show the colorbar. Defaults to True.
            warn_zero_coord_buses (bool): If True, show warning when buses have undefined (0,0)
                coordinates. Defaults to False.
            show (bool): Whether to display the plot immediately. Defaults to False.
            map_style (Optional[str]): Map style for the background. Options include:
                'open-street-map', 'white-bg', 'carto-positron', 'carto-darkmatter',
                'stamen-terrain', 'stamen-toner', 'stamen-watercolor'. Defaults to 'open-street-map'.
            save_file_path (Optional[str]): Path to save the plot as HTML file. Defaults to None.

        Returns:
            go.Figure: The Plotly figure object.
        """
        return self._circuit_geoplot.circuit_geoplot(
            parameter=parameter,
            title=title,
            width_3ph=width_3ph,
            width_2ph=width_2ph,
            width_1ph=width_1ph,
            mark_buses=mark_buses,
            bus_markers=bus_markers,
            show_colorbar=show_colorbar,
            warn_zero_coord_buses=warn_zero_coord_buses,
            show=show,
            map_style=map_style,
            save_file_path=save_file_path
        )
