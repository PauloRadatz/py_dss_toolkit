# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from dataclasses import dataclass, field
from typing import List, Tuple, Union
from py_dss_tools.studies.settings_utils import *
from py_dss_interface import DSS
import re

@dataclass(kw_only=True)
class StudySettings:
    _dss: DSS
    _algorithm: str = field(init=False)
    _time: Union[List[float], Tuple[float]] = field(init=False)

    def __post_init__(self):
        self._algorithm = self._dss.text("get algorithm")
        validate_algorithm(self._dss, self.algorithm)
        match = re.search(r'\[\s*([\d.]+)\s*,\s*([\d.]+)\s*\]', self._dss.text(f"get time"))
        x, y = float(match.group(1)), float(match.group(2))
        self._time = (x, y)
        validate_time(self._dss, self.time)

    @property
    def algorithm(self) -> str:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value: str):
        validate_algorithm(self._dss, value)
        self._dss.text(f"set algorithm={value}")
        self._algorithm = value

    @property
    def time(self) -> Union[List[float], Tuple[float]]:
        return self._time

    @time.setter
    def time(self, value: Union[List[float], Tuple[float]]):
        validate_time(self._dss, value)
        self._time = value
        self._dss.text(f"set time=({value[0]}, {value[1]})")
