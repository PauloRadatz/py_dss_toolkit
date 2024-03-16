# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : StudyPowerFlowSettings.py
# @Software: PyCharm

from typing import List, Tuple, Union
from dataclasses import dataclass, field, asdict
from py_dss_interface import DSS
from py_dss_tools.studies.StudySettings import StudySettings
import pandas as pd
from py_dss_tools.studies.settings_utils import *


@dataclass(kw_only=True)
class StudyPowerFlowSettings(StudySettings):
    modes = ["snapshot", "snap", "daily"]

    def __post_init__(self):
        self._algorithm = "normal"
        self._number = 1
        self._time = (0, 0)
        self._mode = check_mode(self._dss, self.modes)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = set_mode(self._dss, self.modes, value)

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        if value != 1:
            raise ValueError("Invalid value for number. Should be 1.")
        self._dss.text(f"set number={value}")
        self._number = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        # Add any validation logic here if needed
        self._time = value

    def get_settings(self):
        return get_settings(self.__dict__)
