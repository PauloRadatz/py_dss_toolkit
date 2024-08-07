# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ShortCircuitImpedances.py
# @Software: PyCharm

from py_dss_interface import DSS


class ShortCircuitCurrents:
    def __init__(self, dss: DSS):
        self._dss = dss

    def short_circuit_currents(self):
        raise ValueError("Method not implemented")
