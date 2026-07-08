# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from dataclasses import dataclass
from dataclasses import field

from py_dss_interface import DSS

from py_dss_toolkit.studies.settings_utils import VALID_SNAPSHOT_MODES
from py_dss_toolkit.studies.settings_utils import SnapshotModeType
from py_dss_toolkit.studies.settings_utils import get_settings
from py_dss_toolkit.studies.settings_utils import validate_mode
from py_dss_toolkit.studies.StudySettings import StudySettings


@dataclass(kw_only=True)
class StudySnapShotPowerFlowSettings(StudySettings):
    _dss: DSS
    _mode: str = field(init=False)

    def __post_init__(self):
        self._initialize_mode()
        self.validate_settings()

    def _initialize_mode(self):
        """Initialize mode to 'snapshot' if current mode is not valid."""
        current_mode = self._dss.text("get mode").lower()
        if current_mode not in VALID_SNAPSHOT_MODES:
            print(f"Mode {current_mode} changed to snapshot")
            self._dss.text("set mode=snapshot")

    @property
    def mode(self) -> str:
        """Get the current simulation mode.

        Returns:
            Mode string: 'snapshot' or 'snap'
        """
        self._mode = self._dss.text("get mode").lower()
        return self._mode

    @mode.setter
    def mode(self, value: SnapshotModeType):
        """Set the simulation mode.

        Args:
            value: Mode string - 'snapshot' or 'snap'
        """
        validated = validate_mode(value, VALID_SNAPSHOT_MODES)
        self._dss.text(f"set mode={validated}")
        self._mode = validated

    def get_settings(self) -> dict:
        """Returns a dictionary of settings."""
        return get_settings(self.__dict__)

    def validate_settings(self):
        validate_mode(self.mode, VALID_SNAPSHOT_MODES)
        super().validate_settings()
