# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : DSSViewSnapShotPowerFlowResults.py
# @Software: PyCharm

from py_dss_tools.view.dss_view.SnapShot.VoltageProfile import VoltageProfile
from py_dss_interface import DSS


class DSSViewSnapShotPowerFlowResults(VoltageProfile):

    def __init__(self, dss: DSS):
        VoltageProfile.__init__(self, dss)
