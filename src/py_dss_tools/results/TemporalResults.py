# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : TemporalResults.py
# @Software: PyCharm

from py_dss_interface import DSS


class TemporalResults:

    def __init__(self, dss: DSS):
        self._dss = dss

    def test_results_temp(self):
        self._dss.text("show powers")
