# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : dss_utils.py
# @Software: PyCharm


from dataclasses import dataclass
from typing import Optional, Union
from py_dss_interface import DSS


class DSSUtils:

    def __init__(self, dss: DSS):
        self._dss = dss

    def update_dss(self, dss: DSS):
        self._dss = dss

    def compile_dss(self, dss_file: str):
        self._dss.text("ClearAll")
        self._dss.text("Compile " + "[" + dss_file + "]")

    def solve_snapshot(self, control_mode="Static", max_control_iter=10):
        self._dss.text("Set maxcontroliter=" + str(max_control_iter))
        self._dss.text("set ControlMode=" + control_mode)
        self._dss.text("Set Mode=SnapShot")
        self._dss.text("solve")

    def dss_command(self, command: str):
        self._dss.text(command)

    def add_meter(self, meter_name: str, element: str, terminal: int = 1):
        self._dss.text(f"new energymeter.{meter_name} element={element} terminal={terminal}")

    def batchedit(self, element_type: str, property: str, value: str):
        self._dss.text(f"batchedit {element_type}..* {property}={value}")

    def calc_voltage_base(self):
        self._dss.text("calcvoltagebase")

    def save_circuit(self, output_dir: Optional[str] = None, case_name: Optional[str] = None):
        if output_dir:
            self._dss.dssinterface.datapath = f"{output_dir}"

        if case_name:
            self._dss.text(f"set casename='{case_name}'")
            self._dss.text(f"save circuit Dir={case_name}")
        else:
            self._dss.text(f"save circuit")


dss_utils = DSSUtils(None)
