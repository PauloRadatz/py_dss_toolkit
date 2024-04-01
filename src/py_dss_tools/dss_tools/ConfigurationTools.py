# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ConfigurationTools.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd


class ConfigurationTools:

    def __init__(self, dss: DSS):
        self._dss = dss

    def compile_dss(self, dss_file: str):
        self._dss.text("ClearAll")
        self._dss.text("Compile " + "[" + dss_file + "]")

    def calc_voltage_base(self):
        self._dss.text("calcvoltagebase")

    def batchedit(self, element_type: str, property: str, value: str):
        self._dss.text(f"batchedit {element_type}..* {property}={value}")
