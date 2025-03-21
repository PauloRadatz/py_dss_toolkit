# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : DSSViewSnapShotPowerFlowResults.py
# @Software: PyCharm

from py_dss_tools.view.interactive_view.SnapShot.VoltageProfile import VoltageProfile
from py_dss_tools.results.SnapShot.SnapShotPowerFlowResults import SnapShotPowerFlowResults
from py_dss_interface import DSS
from py_dss_tools.view.interactive_view.SnapShot.Circuit.ViewCircuitResults import ViewCircuitResults
from py_dss_tools.model.ModelBase import ModelBase


class InteractiveViewSnapShotPowerFlowResults(VoltageProfile, ViewCircuitResults):

    def __init__(self, dss: DSS, results: SnapShotPowerFlowResults, model: [ModelBase]):
        VoltageProfile.__init__(self, dss, results)
        ViewCircuitResults.__init__(self, dss, results, model)
