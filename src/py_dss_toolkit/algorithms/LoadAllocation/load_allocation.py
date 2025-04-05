# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : load_allocation.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from py_dss_toolkit.studies import StudyGeneric
from typing import Union


class LoadAllocation:

    def __init__(self, study: StudyGeneric):
        self._study = study
        self._dss = self._study.dss

    def run_load_allocation_kw(self, target_kw: Union[int, float]):

        self._dss.text("solve")
        for _ in range(10):
            kw = -1 * self._dss.circuit.total_power[0]
            delta_kw = target_kw - kw
            mult_factor = delta_kw / target_kw

            self._dss.loads.first()
            for _ in range(self._dss.loads.count):
                self._dss.loads.kw = self._dss.loads.kw * (1 + mult_factor)
                self._dss.loads.next()

            self._dss.text("solve")

        self.delta_kw = delta_kw
        self.mult_factor = mult_factor

    def get_status(self):
        return self.delta_kw, self.mult_factor
