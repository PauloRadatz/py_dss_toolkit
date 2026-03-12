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
    from py_dss_toolkit.model_verification.ModelVerification import ModelVerification


class DSSTools:

    def __init__(self, dss: Optional[DSS]):
        self._dss = dss
        self._results = None
        self._model = None
        self._model_verification = None
        self._dss_view = None
        self._static_view = None
        self._interactive_view = None
        self._simulation = None
        self._configuration = None
        self._utilities = None

        if dss:
            self.__load_objects()

    def __load_objects(self):
        from py_dss_toolkit.results.Results import Results
        from py_dss_toolkit.model.ModelBase import ModelBase
        from py_dss_toolkit.model_verification.ModelVerification import ModelVerification
        from py_dss_toolkit.view.static_view.ViewResults import ViewResults as StaticView
        from py_dss_toolkit.view.interactive_view.ViewResults import ViewResults as InteractiveView
        from py_dss_toolkit.view.dss_view.ViewResults import ViewResults as DSSView
        self._model = ModelBase(self._dss)
        self._results = Results(self._dss, lambda: self._model.bus_connection_type_map)
        self._model_verification = ModelVerification(self._dss, self._model)
        self._static_view = StaticView(self._dss, self._results)
        self._interactive_view = InteractiveView(self._dss, self._results, self._model)
        self._dss_view = DSSView(self._dss)
        self._simulation = SimulationTools(self._dss)
        self._configuration = ConfigurationTools(self._dss)
        self._utilities = UtilitiesTools(self._dss)

    def update_dss(self, dss: DSS):
        self._dss = dss
        self.__load_objects()

    def __raise_if_dss_not_connected(self):
        if self._dss is None:
            raise RuntimeError("DSS is not connected. Use dss_tools.update_dss(dss) before accessing this property. Where dss is an instance of py_dss_interface.DSS()")

    @property
    def dss(self) -> DSS:
        self.__raise_if_dss_not_connected()
        return self._dss

    @property
    def results(self) -> "Results":
        self.__raise_if_dss_not_connected()
        return self._results

    @property
    def model(self) -> "ModelBase":
        self.__raise_if_dss_not_connected()
        return self._model

    @property
    def model_verification(self) -> "ModelVerification":
        self.__raise_if_dss_not_connected()
        return self._model_verification

    @property
    def dss_view(self) -> "DSSView":
        self.__raise_if_dss_not_connected()
        return self._dss_view

    @property
    def static_view(self) -> "StaticView":
        self.__raise_if_dss_not_connected()
        return self._static_view

    @property
    def interactive_view(self) -> "InteractiveView":
        self.__raise_if_dss_not_connected()
        return self._interactive_view

    @property
    def simulation(self) -> SimulationTools:
        self.__raise_if_dss_not_connected()
        return self._simulation

    @property
    def configuration(self) -> ConfigurationTools:
        self.__raise_if_dss_not_connected()
        return self._configuration

    @property
    def utilities(self) -> UtilitiesTools:
        self.__raise_if_dss_not_connected()
        return self._utilities

    def text(self, command: str) -> str:
        self.__raise_if_dss_not_connected()
        return self._dss.text(command)


dss_tools = DSSTools(None)
