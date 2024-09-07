# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : PowerFlowResults.py
# @Software: PyCharm

from py_dss_interface import DSS

from py_dss_tools.results.Static.VoltagesNodal import VoltagesNodal
from py_dss_tools.results.Static.VoltagesElement import VoltagesElement
from py_dss_tools.results.Static.Currents import Currents
from py_dss_tools.results.Static.Powers import Powers
from py_dss_tools.results.Static.Circuit import Circuit


class StaticResults(VoltagesNodal, VoltagesElement, Currents, Powers, Circuit):
    def __init__(self, dss: DSS):
        self._dss = dss
        VoltagesNodal.__init__(self, self._dss)
        VoltagesElement.__init__(self, self._dss)
        Currents.__init__(self, self._dss)
        Powers.__init__(self, self._dss)
        Circuit.__init__(self, self._dss)
