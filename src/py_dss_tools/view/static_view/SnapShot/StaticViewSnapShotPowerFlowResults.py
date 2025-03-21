# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewResults.py
# @Software: PyCharm

from py_dss_tools.view.static_view.SnapShot.VoltageProfile import VoltageProfile
from py_dss_tools.results.SnapShot.SnapShotPowerFlowResults import SnapShotPowerFlowResults
from py_dss_interface import DSS


class StaticViewSnapShotPowerFlowResults(VoltageProfile):

    def __init__(self, dss: DSS, results: SnapShotPowerFlowResults):
        VoltageProfile.__init__(self, dss, results)
