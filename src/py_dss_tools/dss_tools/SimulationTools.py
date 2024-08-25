# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : SimulationTools.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd


class SimulationTools:

    def __init__(self, dss: DSS):
        self._dss = dss

    def solve_snapshot(self, control_mode="Static", max_iterations=15, max_control_iter=10):
        self._dss.text("Set maxiterations=" + str(max_iterations))
        self._dss.text("Set maxcontroliter=" + str(max_control_iter))
        self._dss.text("set ControlMode=" + control_mode)
        self._dss.text("Set Mode=SnapShot")
        self._dss.text("solve")
