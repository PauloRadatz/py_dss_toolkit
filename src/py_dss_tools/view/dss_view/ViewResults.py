# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewResults.py
# @Software: PyCharm

from py_dss_tools.view.dss_view.SnapShot.DSSViewSnapShotPowerFlowResults import DSSViewSnapShotPowerFlowResults
from py_dss_tools.view.dss_view.Temporal.ViewTemporalResults import ViewTemporalResults
from py_dss_interface import DSS


class ViewResults(DSSViewSnapShotPowerFlowResults, ViewTemporalResults):

    def __init__(self, dss: DSS):
        DSSViewSnapShotPowerFlowResults.__init__(self, dss)
        ViewTemporalResults.__init__(self, dss)
