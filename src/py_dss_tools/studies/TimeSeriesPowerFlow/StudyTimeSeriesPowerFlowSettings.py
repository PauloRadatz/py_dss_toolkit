# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : StudyTimeSeriesPowerFlowSettings.py
# @Software: PyCharm


from dataclasses import dataclass, field

from py_dss_tools.studies.StudySettings import StudySettings
from py_dss_tools.studies.settings_utils import *


@dataclass(kw_only=True)
class StudyTimeSeriesPowerFlowSettings(StudySettings):
    _dss: DSS
    _mode: str = field(init=False)
    _number: int = field(init=False)
    _stepsize: float = field(init=False)

    VALID_MODES: List[str] = field(default_factory=lambda: ["daily", "yearly", "dutycycle"], init=False)

    def __post_init__(self):
        self._initialize_mode()
        self.validate_settings()

    def _initialize_mode(self):
        if self.mode not in self.VALID_MODES:
            print(f"Mode {self.mode} to {self.VALID_MODES[0]}")
            self._dss.text(f"set mode={self.VALID_MODES[0]}")

    @property
    def mode(self) -> str:
        self._mode = self._dss.text(f"get mode").lower()
        return self._mode

    @mode.setter
    def mode(self, value: str):
        validate_mode(value, self.VALID_MODES)
        self._dss.text(f"set mode={value}")
        self._mode = value

    @property
    def number(self) -> int:
        self._number = int(self._dss.text(f"get number"))
        return self._number

    @number.setter
    def number(self, value: int):
        validate_number(value)
        self._dss.text(f"set number={value}")
        self._number = value

    @property
    def stepsize(self) -> int:
        self._stepsize = int(self._dss.text(f"get stepsize"))
        return self._stepsize

    @stepsize.setter
    def stepsize(self, value: int):
        validate_stepsize(value)
        self._dss.text(f"set stepsize={value}")
        self._stepsize = value

    def get_settings(self):
        return get_settings(self.__dict__)

    def validate_settings(self):
        validate_mode(self.mode, self.VALID_MODES)
        validate_number(self.number)
        validate_stepsize(self.stepsize)
        super().validate_settings()
