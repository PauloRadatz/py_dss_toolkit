# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : DSSViewTimeSeriesPowerFlowResults.py
# @Software: PyCharm

from py_dss_interface import DSS
from py_dss_tools.view.dss_view.TimeSeries.DSSMonitor import DSSMonitor
from py_dss_tools.view.dss_view.SnapShot.DSSVoltageProfile import DSSVoltageProfile

class DSSViewTimeSeriesPowerFlowResults(DSSMonitor, DSSVoltageProfile):

    def __init__(self, dss: DSS):
        self._dss = dss
        DSSMonitor.__init__(self, self._dss)
        DSSVoltageProfile.__init__(self, self._dss)
