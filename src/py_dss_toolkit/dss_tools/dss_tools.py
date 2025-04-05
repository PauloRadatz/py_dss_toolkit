# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Optional

from py_dss_interface import DSS

from py_dss_toolkit.dss_tools.ConfigurationTools import ConfigurationTools
from py_dss_toolkit.dss_tools.SimulationTools import SimulationTools
from py_dss_toolkit.dss_tools.UtilitiesTools import UtilitiesTools


class DSSTools:

    def __init__(self, dss: Optional[DSS]):
        self._dss = dss

        if dss:
            self.__load_objects()

    def __load_objects(self):
        # self._results = ResultsTools(self._dss)
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
    def results(self):
        return self._results

    @property
    def model(self):
        return self._model

    @property
    def dss_view(self):
        return self._dss_view

    @property
    def static_view(self):
        return self._static_view

    @property
    def interactive_view(self):
        return self._interactive_view

    @property
    def simulation(self):
        return self._simulation

    @property
    def configuration(self):
        return self._configuration

    @property
    def utilities(self):
        return self._utilities

    def text(self, command: str):
        self._dss.text(command)


dss_tools = DSSTools(None)
