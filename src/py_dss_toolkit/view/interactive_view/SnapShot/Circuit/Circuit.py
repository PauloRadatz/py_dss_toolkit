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
                     save_file_path: Optional[str] = None) -> Optional[go.Figure]:
        """
        Create an interactive circuit plot.
        
        This method delegates to CircuitPlot.circuit_plot(). See that method's docstring
        for detailed parameter descriptions.
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
                        save_file_path: Optional[str] = None) -> Optional[go.Figure]:
        """
        Create an interactive geographic circuit plot.
        
        This method delegates to CircuitGeoPlot.circuit_geoplot(). See that method's docstring
        for detailed parameter descriptions.
        
        Important:
            This method requires coordinates to be in WGS84 (EPSG:4326) format (latitude/longitude).
            If your bus coordinates are in a different coordinate reference system (CRS), you must
            transform them to WGS84 before using this method.
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
