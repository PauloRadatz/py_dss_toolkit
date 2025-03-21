# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : DSSViewSnapShotPowerFlowResults.py
# @Software: PyCharm

from py_dss_tools.view.dss_view.SnapShot.DSSVoltageProfile import DSSVoltageProfile
from py_dss_interface import DSS


class DSSViewSnapShotPowerFlowResults(DSSVoltageProfile):

    def __init__(self, dss: DSS):
        DSSVoltageProfile.__init__(self, dss)
