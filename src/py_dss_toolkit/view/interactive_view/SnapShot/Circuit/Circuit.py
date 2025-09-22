# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : Circuit.py
# @Software: PyCharm

import plotly.graph_objects as go
from typing import Optional, List
from py_dss_interface import DSS
from py_dss_toolkit.results.SnapShot.SnapShotPowerFlowResults import SnapShotPowerFlowResults
from py_dss_toolkit.model.ModelBase import ModelBase
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitBase import CircuitBase
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitPlot import CircuitPlot
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitGeoPlot import CircuitGeoPlot
from py_dss_toolkit.view.interactive_view.SnapShot.Circuit.CircuitBusMarker import CircuitBusMarker


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
        
        # Create instances of the specialized plotting classes
        self._circuit_plot = CircuitPlot(dss, results, model)
        self._circuit_geoplot = CircuitGeoPlot(dss, results, model)
        
        # Share all settings and strategy objects between instances
        self._share_instances(self._circuit_plot)
        self._share_instances(self._circuit_geoplot)

    def circuit_plot(self, *args, **kwargs):
        """Delegate to CircuitPlot class."""
        return self._circuit_plot.circuit_plot(*args, **kwargs)

    def circuit_geoplot(self, *args, **kwargs):
        """Delegate to CircuitGeoPlot class."""
        return self._circuit_geoplot.circuit_geoplot(*args, **kwargs)

    def _share_instances(self, target_instance):
        """Share all settings and strategy objects with the target instance."""
        # Share settings objects
        target_instance._active_power_settings = self._active_power_settings
        target_instance._voltage_settings = self._voltage_settings
        target_instance._user_numerical_defined_settings = self._user_numerical_defined_settings
        target_instance._user_categorical_defined_settings = self._user_categorical_defined_settings
        target_instance._phases_settings = self._phases_settings
        target_instance._thermal_violation_settings = self._thermal_violation_settings
        target_instance._voltage_violation_settings = self._voltage_violation_settings
        target_instance._plot_style = self._plot_style
        
        # Share strategy objects (they reference the same settings)
        target_instance._parameter_strategies = self._parameter_strategies
