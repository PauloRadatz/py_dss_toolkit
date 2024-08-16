# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : Results.py
# @Software: PyCharm


from py_dss_tools.results.Static.StaticResults import StaticResults
from py_dss_tools.results.Temporal.TemporalResults import TemporalResults
from py_dss_tools.results.ShortCircuit.FaultResults import FaultResults
from py_dss_interface import DSS


class Results(StaticResults, TemporalResults, FaultResults):

    def __init__(self, dss: DSS):
        self._dss = dss
        StaticResults.__init__(self, self._dss)
        TemporalResults.__init__(self, self._dss)
        FaultResults.__init__(self, self._dss)
