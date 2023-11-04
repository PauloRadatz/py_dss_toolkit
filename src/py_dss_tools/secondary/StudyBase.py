# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : StudyBase.py
# @Software: PyCharm

import attr
import pandas as pd
from py_dss_interface import DSS

from ..utils import Utils

from py_dss_tools.model.ModelData import ModelData
from py_dss_tools.dss_utils import DSSUtils

class StudyBase(DSSUtils):
    def __init__(self, name, dss_file, frequency_base=60, dll=None):
        self._name = name
        self._dll = dll
        self._dss_file = dss_file
        # Objects
        if self._dll:
            self._dss = DSS(self._dll)
        else:
            self._dss = DSS("C:\OpenDSS_rep\Version8\Source")
        self._dss.text(f"compile [{self._dss_file}]")
        self._name = Utils.remove_blank_spaces(self._name)

        # self.dss_utils = DSSUtils(self._dss)
        DSSUtils.__init__(self, self._dss)
        # ModelData.__init__(self, self._dss)

        self._model = ModelData(self._dss)

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

