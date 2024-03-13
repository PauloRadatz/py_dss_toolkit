# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : dss_tools.py
# @Software: PyCharm


from dataclasses import dataclass
from typing import Optional, Union
from py_dss_interface import DSS
import pandas as pd
from py_dss_tools.dss_tools.ResultsTools import ResultsTools
from py_dss_tools.dss_tools.ModelTools import ModelTools
from py_dss_tools.dss_tools.DSSViewTools import DSSViewTools


class DSSTools:

    def __init__(self, dss: Optional[DSS]):
        self._dss = dss

        if dss:
            self.load_objects()

    def load_objects(self):
        self._results = ResultsTools(self._dss)
        self._model = ModelTools(self._dss)
        self._dss_view = DSSViewTools(self._dss)

    def update_dss(self, dss: DSS):
        self._dss = dss
        self.load_objects()

    @property
    def results(self):
        return self._results

    @property
    def model(self):
        return self._model

    @property
    def dss_view(self):
        return self._dss_view

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

dss_tools = DSSTools(None)
