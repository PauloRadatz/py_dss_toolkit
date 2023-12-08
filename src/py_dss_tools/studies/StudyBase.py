# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : StudyBase.py
# @Software: PyCharm

import attr
import pandas as pd
from py_dss_interface import DSS

from py_dss_tools.utils import Utils

from py_dss_tools.model.ModelBase import ModelBase
from dataclasses import dataclass, field
from typing import Union, Optional


@dataclass(kw_only=True)
class StudyBase:
    _name: str = field(default='scenario_' + Utils.generate_random_string(), init=True, repr=True)
    _dss_file: str = field(init=True, repr=True)
    _frequency_base: Union[int, float] = field(default=60, init=True)
    _dll: str = field(default=None, init=True)

    def __post_init__(self):
        if self._dll:
            self._dss = DSS(self._dll)
        else:
            self._dss = DSS()
        self._dss.text(f"compile [{self._dss_file}]")
        self._name = Utils.remove_blank_spaces(self._name)

        # TODO check if there is voltagebase
        self._model = ModelBase(self._dss)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        Utils.check_instance(value, 'name', ['str'], )
        self._name = Utils.remove_blank_spaces(value)

    @property
    def dss(self):
        return self._dss

    @property
    def model(self):
        return self._model
