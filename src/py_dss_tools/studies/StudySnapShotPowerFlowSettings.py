# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : StudySnapShotPowerFlowSettings.py
# @Software: PyCharm

from typing import List, Tuple, Union
from dataclasses import dataclass, field, asdict
from py_dss_interface import DSS
from py_dss_tools.studies.StudySettings import StudySettings
import pandas as pd
from py_dss_tools.studies.settings_utils import *
from typing import List, Tuple, Union
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class StudySnapShotPowerFlowSettings(StudySettings):
    _dss: DSS
    _mode: str = field(init=False)
    _number: int = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self._mode = self._dss.text(f"get mode")
        self._number = int(self._dss.text(f"get number"))
        validate_mode(self._dss, self.mode, ["snapshot", "snap"])
        # validate_number(self._dss, self.number, 100)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value: str):
        validate_mode(self._dss, value, ["snapshot", "snap"])
        self._dss.text(f"set mode={value}")
        self._mode = value

    # @property
    # def number(self):
    #     return self._number
    #
    # @number.setter
    # def number(self, value: int):
    #     validate_number(self._dss, value, 1)
    #     self._dss.text(f"set number={value}")
    #     self._number = value

    def get_settings(self) -> dict:
        """Returns a dictionary of settings."""
        return get_settings(self.__dict__)
