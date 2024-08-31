# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewCircuitResults.py
# @Software: PyCharm

from py_dss_interface import DSS
from py_dss_tools.results.Temporal import TemporalResults
from py_dss_tools.view.interactive_view.Circuit.Circuit import Circuit


class ViewCircuitResults(Circuit):

    def __init__(self, dss: DSS, results: TemporalResults):
        self._dss = dss
        self._results = results
        Circuit.__init__(self, self._dss, self._results)
