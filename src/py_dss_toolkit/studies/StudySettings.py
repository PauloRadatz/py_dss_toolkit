# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

import re
from dataclasses import dataclass, field
from typing import Tuple

from py_dss_interface import DSS

from py_dss_toolkit.studies.settings_utils import (
    AlgorithmType, validate_algorithm, validate_time, get_settings
)


@dataclass(kw_only=True)
class StudySettings:
    _dss: DSS
    _algorithm: str = field(init=False)
    _time: Tuple[float, float] = field(init=False)

    @property
    def algorithm(self) -> str:
        """Get the current algorithm setting.
        
        Returns:
            Algorithm string: 'normal', 'newton', or 'ncim'
        """
        self._algorithm = self._dss.text("get algorithm").lower()
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value: AlgorithmType):
        """Set the algorithm for power flow solution.
        
        Args:
            value: Algorithm string - 'normal', 'newton', or 'ncim'
        """
        validated = validate_algorithm(value)
        self._dss.text(f"set algorithm={validated}")
        self._algorithm = validated

    @property
    def time(self) -> Tuple[float, float]:
        match = re.search(r'\[\s*([\d.]+)\s*,\s*([\d.]+)\s*\]', self._dss.text(f"get time"))
        x, y = float(match.group(1)), float(match.group(2))
        self._time = (x, y)
        return self._time

    @time.setter
    def time(self, value: Tuple[float, float]):
        validate_time(value)
        self._time = value
        self._dss.text(f"set time=({value[0]}, {value[1]})")

    def validate_settings(self):
        validate_algorithm(self.algorithm)
        validate_time(self.time)
