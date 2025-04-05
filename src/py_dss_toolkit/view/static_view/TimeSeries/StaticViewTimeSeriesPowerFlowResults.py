# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : DSSViewTimeSeriesPowerFlowResults.py
# @Software: PyCharm

from py_dss_interface import DSS
from py_dss_toolkit.results.TimeSeries import TimeSeriesPowerFlowResults
from py_dss_toolkit.view.static_view.TimeSeries.StaticMonitor import StaticMonitor


class StaticViewTimeSeriesPowerFlowResults(StaticMonitor):

    def __init__(self, dss: DSS, results: TimeSeriesPowerFlowResults):
        self._dss = dss
        self._results = results
        StaticMonitor.__init__(self, self._dss, self._results)
