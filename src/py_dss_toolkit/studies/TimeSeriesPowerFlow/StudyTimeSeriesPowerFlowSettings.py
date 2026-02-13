# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : StudyTimeSeriesPowerFlowSettings.py
# @Software: PyCharm


from dataclasses import dataclass, field

from py_dss_interface import DSS

from py_dss_toolkit.studies.StudySettings import StudySettings
from py_dss_toolkit.studies.settings_utils import (
    TimeSeriesModeType, VALID_TIMESERIES_MODES, validate_mode, validate_number, validate_stepsize, get_settings
)


@dataclass(kw_only=True)
class StudyTimeSeriesPowerFlowSettings(StudySettings):
    _dss: DSS
    _mode: str = field(init=False)
    _number: int = field(init=False)
    _stepsize: float = field(init=False)

    def __post_init__(self):
        self._initialize_mode()
        self.validate_settings()

    def _initialize_mode(self):
        """Initialize mode to 'daily' if current mode is not valid."""
        current_mode = self._dss.text("get mode").lower()
        if current_mode not in VALID_TIMESERIES_MODES:
            print(f"Mode {current_mode} changed to daily")
            self._dss.text("set mode=daily")

    @property
    def mode(self) -> str:
        """Get the current simulation mode.
        
        Returns:
            Mode string: 'daily', 'yearly', or 'dutycycle'
        """
        self._mode = self._dss.text("get mode").lower()
        return self._mode

    @mode.setter
    def mode(self, value: TimeSeriesModeType):
        """Set the simulation mode.
        
        Args:
            value: Mode string - 'daily', 'yearly', or 'dutycycle'
        """
        validated = validate_mode(value, VALID_TIMESERIES_MODES)
        self._dss.text(f"set mode={validated}")
        self._mode = validated

    @property
    def number(self) -> int:
        self._number = int(self._dss.text("get number"))
        return self._number

    @number.setter
    def number(self, value: int):
        validate_number(value)
        self._dss.text(f"set number={value}")
        self._number = value

    @property
    def stepsize(self) -> float:
        self._stepsize = float(self._dss.text("get stepsize"))
        return self._stepsize

    @stepsize.setter
    def stepsize(self, value: float):
        validate_stepsize(value)
        self._dss.text(f"set stepsize={value}")
        self._stepsize = value

    def get_settings(self):
        return get_settings(self.__dict__)

    def validate_settings(self):
        validate_mode(self.mode, VALID_TIMESERIES_MODES)
        validate_number(self.number)
        validate_stepsize(self.stepsize)
        super().validate_settings()
