# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Optional, TYPE_CHECKING

from py_dss_interface import DSS

from py_dss_toolkit.dss_tools.ConfigurationTools import ConfigurationTools
from py_dss_toolkit.dss_tools.SimulationTools import SimulationTools
from py_dss_toolkit.dss_tools.UtilitiesTools import UtilitiesTools

if TYPE_CHECKING:
    from py_dss_toolkit.results.Results import Results
    from py_dss_toolkit.model.ModelBase import ModelBase
    from py_dss_toolkit.view.static_view.ViewResults import ViewResults as StaticView
    from py_dss_toolkit.view.interactive_view.ViewResults import ViewResults as InteractiveView
    from py_dss_toolkit.view.dss_view.ViewResults import ViewResults as DSSView


class DSSTools:

    def __init__(self, dss: Optional[DSS]):
        self._dss = dss

        if dss:
            self.__load_objects()

    def __load_objects(self):
        from py_dss_toolkit.results.Results import Results
        from py_dss_toolkit.model.ModelBase import ModelBase
        from py_dss_toolkit.view.static_view.ViewResults import ViewResults as StaticView
        from py_dss_toolkit.view.interactive_view.ViewResults import ViewResults as InteractiveView
        from py_dss_toolkit.view.dss_view.ViewResults import ViewResults as DSSView
        self._results = Results(self._dss)
        self._model = ModelBase(self._dss)
        self._static_view = StaticView(self._dss, self._results)
        self._interactive_view = InteractiveView(self._dss, self._results, self._model)
        self._dss_view = DSSView(self._dss)
        self._simulation = SimulationTools(self._dss)
        self._configuration = ConfigurationTools(self._dss)
        self._utilities = UtilitiesTools(self._dss)

    def update_dss(self, dss: DSS):
        self._dss = dss
        self.__load_objects()

    @property
    def dss(self) -> DSS:
        return self._dss

    @property
    def results(self) -> "Results":
        return self._results

    @property
    def model(self) -> "ModelBase":
        return self._model

    @property
    def dss_view(self) -> "DSSView":
        return self._dss_view

    @property
    def static_view(self) -> "StaticView":
        return self._static_view

    @property
    def interactive_view(self) -> "InteractiveView":
        return self._interactive_view

    @property
    def simulation(self) -> SimulationTools:
        return self._simulation

    @property
    def configuration(self) -> ConfigurationTools:
        return self._configuration

    @property
    def utilities(self) -> UtilitiesTools:
        return self._utilities

    def text(self, command: str) -> str:
        return self._dss.text(command)


dss_tools = DSSTools(None)
