# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from dataclasses import dataclass

from py_dss_toolkit.results.SnapShot.SnapShotPowerFlowResults import SnapShotPowerFlowResults
from py_dss_toolkit.studies.SnapShotPowerFlow.StudySnapShotPowerFlowSettings import StudySnapShotPowerFlowSettings
from py_dss_toolkit.studies.StudyBase import StudyBase
from py_dss_toolkit.view.dss_view.SnapShot.DSSViewSnapShotPowerFlowResults import \
    DSSViewSnapShotPowerFlowResults as DSSView
from py_dss_toolkit.view.interactive_view.SnapShot.InteractiveViewSnapShotPowerFlowResults import \
    InteractiveViewSnapShotPowerFlowResults as InteractiveView
from py_dss_toolkit.view.static_view.SnapShot.StaticViewSnapShotPowerFlowResults import \
    StaticViewSnapShotPowerFlowResults as StaticView

VALID_MODES = ["snap", "snapshot"]  # List of supported modes


@dataclass(kw_only=True)
class StudySnapShotPowerFlow(StudyBase):
    def __post_init__(self):
        """Initialize the study's main components."""
        super().__post_init__()
        self._results = SnapShotPowerFlowResults(self.dss)
        self._settings = StudySnapShotPowerFlowSettings(_dss=self.dss)
        self._initialize_views()

    def _initialize_views(self):
        """Set up the study's view layers."""
        self._static_view = StaticView(self.dss, self._results)
        self._interactive_view = InteractiveView(self.dss, self._results, self.model)
        self._dss_view = DSSView(self.dss)

    @property
    def results(self):
        """Access study results."""
        return self._results

    @property
    def settings(self):
        """Access the study's settings."""
        return self._settings

    @property
    def dss_view(self):
        """Access the DSS view instance."""
        return self._dss_view

    @property
    def static_view(self):
        """Access the static view instance."""
        return self._static_view

    @property
    def interactive_view(self):
        """Access the interactive view instance."""
        return self._interactive_view

    def run(self):
        """Execute the study and solve the power flow."""
        self._validate_settings()
        self.dss.text("solve")

    def _validate_settings(self):
        """Ensure the study settings are valid before execution."""
        self.settings.validate_settings()
