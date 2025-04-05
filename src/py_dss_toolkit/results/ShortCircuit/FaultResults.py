# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : TemporalResults.py
# @Software: PyCharm
from py_dss_interface import DSS
from py_dss_toolkit.results.ShortCircuit.ShortCircuitImpedances import ShortCircuitImpedances
from py_dss_toolkit.results.ShortCircuit.ShortCircuitCurrents import ShortCircuitCurrents

class FaultResults(ShortCircuitImpedances, ShortCircuitCurrents):

    def __init__(self, dss: DSS):
        self._dss = dss
        ShortCircuitImpedances.__init__(self, self._dss)
        ShortCircuitCurrents.__init__(self, self._dss)

