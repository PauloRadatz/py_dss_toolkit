# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewTemporalResults.py
# @Software: PyCharm

from py_dss_interface import DSS
from py_dss_tools.results.Temporal import TemporalResults
from py_dss_tools.view.interactive_view.Temporal.Monitor import Monitor


class ViewTemporalResults(Monitor):

    def __init__(self, dss: DSS, results: TemporalResults):
        self._dss = dss
        self._results = results
        Monitor.__init__(self, self._dss, self._results)
