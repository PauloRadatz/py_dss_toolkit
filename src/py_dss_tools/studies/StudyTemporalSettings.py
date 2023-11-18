# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : StudyTemporalSettings.py
# @Software: PyCharm


from typing import List, Tuple, Union
from dataclasses import dataclass, field, asdict
from py_dss_interface import DSS
from py_dss_tools.studies.StudySettings import StudySettings
import pandas as pd


@dataclass(kw_only=True)
class StudyTemporalSettings(StudySettings):

    def __post_init__(self):
        self._algorithm = "normal"
        self._mode = "daily"
        self._number = 24
        self._time = (0, 0)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if value.lower() not in ["daily", "yearly", "duty"]:
            raise ValueError(f'Invalid value for mode. Should be {["daily", "yearly", "duty"]}.')
        self.dss.text(f"set mode={value.lower()}")
        self._mode = value.lower()

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self.dss.text(f"set number={value}")
        self._number = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        # Add any validation logic here if needed
        self._time = value

    def get_settings(self):

        data = dict()
        for at, v in self.__dict__.items():
            if at != "_dss":
                data[at.replace("_", "")] = v
        df = pd.DataFrame([data]).T
        df.columns = ["Settings"]
        return df
