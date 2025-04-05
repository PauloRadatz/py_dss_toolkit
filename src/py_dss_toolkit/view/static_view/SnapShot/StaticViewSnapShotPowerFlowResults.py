# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ViewResults.py
# @Software: PyCharm

from py_dss_toolkit.view.static_view.SnapShot.StaticVoltageProfile import StaticVoltageProfile
from py_dss_toolkit.results.SnapShot.SnapShotPowerFlowResults import SnapShotPowerFlowResults
from py_dss_interface import DSS


class StaticViewSnapShotPowerFlowResults(StaticVoltageProfile):

    def __init__(self, dss: DSS, results: SnapShotPowerFlowResults):
        StaticVoltageProfile.__init__(self, dss, results)
