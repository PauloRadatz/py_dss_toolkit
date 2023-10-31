# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : dss_utils.py
# @Software: PyCharm


from dataclasses import dataclass
from typing import Optional
from py_dss_interface import DSS


class DSSUtils:

    def __init__(self, dss: DSS):
        self._dss = dss

    def update_dss(self, dss: DSS):
        self._dss = dss

    def compile_dss(self, dss_file):
        self._dss.text("ClearAll")
        self._dss.text("Compile " + "[" + dss_file + "]")

    def solve_snapshot(self, control_mode="Static", max_control_iter=10):
        self._dss.text("Set maxcontroliter=" + str(max_control_iter))
        self._dss.text("set ControlMode=" + control_mode)
        self._dss.text("Set Mode=SnapShot")
        self._dss.text("solve")

    def dss_command(self, command: str):
        self._dss.text(command)


dss_utils = DSSUtils(None)
