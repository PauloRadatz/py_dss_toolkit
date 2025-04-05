# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : StudyFaultSettings.py
# @Software: PyCharm

from typing import List, Tuple, Union
from dataclasses import dataclass, field, asdict
from py_dss_interface import DSS
from py_dss_toolkit.studies.StudySettings import StudySettings
import pandas as pd
from py_dss_toolkit.studies.settings_utils import *


@dataclass(kw_only=True)
class StudyFaultSettings(StudySettings):
    modes = ["faultstudy", "f", "fault"]

    def __post_init__(self):
        self._mode = check_mode(self._dss, self.modes)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = set_mode(self._dss, self.modes, value)

    def get_settings(self):
        return get_settings(self.__dict__)
