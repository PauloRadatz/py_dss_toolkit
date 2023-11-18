# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : TemporalResults.py
# @Software: PyCharm

from py_dss_interface import DSS
from py_dss_tools.results.Energymeters import Energymeters
from py_dss_tools.results.Monitor import Monitor


class TemporalResults(Energymeters, Monitor):

    def __init__(self, dss: DSS):
        self._dss = dss
        Energymeters.__init__(self, self._dss)
        Monitor.__init__(self, self._dss)
