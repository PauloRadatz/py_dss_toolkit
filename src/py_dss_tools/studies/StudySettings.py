# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : StudySettings.py
# @Software: PyCharm


from typing import List, Tuple, Union
from dataclasses import dataclass, field
from py_dss_interface import DSS
@dataclass(kw_only=True)
class StudySettings:
    _dss: DSS
    _algorithm: str = field(default="normal")
    _mode: str = field(default="snapshot")
    _number: int = field(default=1)
    _time: Union[List[float], Tuple[float]] = field(default=(0, 0))

    @property
    def dss(self):
        return self._dss
    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value):
        # Add any validation logic here if needed
        self._algorithm = value
    @property
    def mode(self):
        return self._mode
    @property
    def number(self):
        return self._number
    @property
    def time(self):
        return self._time
