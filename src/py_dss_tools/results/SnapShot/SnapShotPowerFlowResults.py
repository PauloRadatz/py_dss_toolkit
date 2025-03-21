# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : PowerFlowResults.py
# @Software: PyCharm

from py_dss_interface import DSS

from py_dss_tools.results.SnapShot.VoltagesNodal import VoltagesNodal
from py_dss_tools.results.SnapShot.VoltagesElement import VoltagesElement
from py_dss_tools.results.SnapShot.Currents import Currents
from py_dss_tools.results.SnapShot.Powers import Powers
from py_dss_tools.results.SnapShot.CircuitSnapShotPowerFlowResults import CircuitSnapShotPowerFlowResults


class SnapShotPowerFlowResults(VoltagesNodal, VoltagesElement, Currents, Powers, CircuitSnapShotPowerFlowResults):
    def __init__(self, dss: DSS):
        self._dss = dss
        VoltagesNodal.__init__(self, self._dss)
        VoltagesElement.__init__(self, self._dss)
        Currents.__init__(self, self._dss)
        Powers.__init__(self, self._dss)
        CircuitSnapShotPowerFlowResults.__init__(self, self._dss)
