# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from dataclasses import dataclass
from py_dss_tools.studies.StudyBase import StudyBase
from py_dss_tools.results.TimeSeries.TimeSeriesPowerFlowResults import TimeSeriesPowerFlowResults
from py_dss_tools.view.static_view.TimeSeries.StaticViewTimeSeriesPowerFlowResults import \
    StaticViewTimeSeriesPowerFlowResults as StaticView
from py_dss_tools.view.interactive_view.TimeSeries.InteractiveViewTimeSeriesPowerFlowResults import \
    InteractiveViewTimeSeriesPowerFlowResults as InteractiveView
from py_dss_tools.view.dss_view.TimeSeries.DSSViewTimeSeriesPowerFlowResults import \
    DSSViewTimeSeriesPowerFlowResults as DSSView
from py_dss_tools.studies.TimeSeriesPowerFlow.StudyTimeSeriesPowerFlowSettings import StudyTimeSeriesPowerFlowSettings
from typing import List, Tuple, Union

from py_dss_tools.dss_tools.dss_tools import dss_tools

@dataclass(kw_only=True)
class StudyTimeSeriesPowerFlow(StudyBase):
    _reset_monitors_energymeters: bool = True

    def __post_init__(self):
        super().__post_init__()
        self._results = TimeSeriesPowerFlowResults(self._dss)
        self._settings = self._initialize_settings()
        self._initialize_views()
        dss_tools.update_dss(self._dss)

    def _initialize_views(self):
        """Initialize all DSS-related views."""
        self._static_view = StaticView(self._dss, self._results)
        self._interactive_view = InteractiveView(self._dss, self._results)
        self._dss_view = DSSView(self._dss)

    def _initialize_settings(self):
        """Configure settings for the study."""
        return StudyTimeSeriesPowerFlowSettings(_dss=self.dss)

    @property
    def results(self):
        return self._results

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
    def settings(self):
        return self._settings

    @property
    def reset_monitors_energymeters(self) -> bool:
        return self._reset_monitors_energymeters

    @reset_monitors_energymeters.setter
    def reset_monitors_energymeters(self, value: bool):
        self._reset_monitors_energymeters = value

    def run(self):
        """Run the study by validating settings and executing the DSS solve command."""

        self._reset_meter_elements()

        self._validate_settings()
        self.dss.text("solve")

    def run_one_step(self, time: Tuple[float, float]):

        # TODO mention that it will run one more step
        self._reset_meter_elements()

        self.settings.validate_settings()
        time_old = self.settings.time
        number_old = self.settings.number
        self.settings.time = time
        self.settings.number = 1
        self.dss.text("solve")
        self.settings.time = time_old
        self.settings.number = number_old

    def _reset_meter_elements(self):
        if self.reset_monitors_energymeters:
            self.dss.monitors.reset_all()
            self.dss.meters.reset_all()

    def _validate_settings(self):
        """Validate settings before running the study."""
        self.settings.validate_settings()
