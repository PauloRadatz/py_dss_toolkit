# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from py_dss_interface import DSS
import pathlib
from typing import Union


class ConfigurationTools:

    def __init__(self, dss: DSS):
        self._dss = dss

    def compile_dss(self, dss_file: Union[str, pathlib.Path]):
        self._dss.text("ClearAll")
        self._dss.text(f"Compile [{dss_file}]")

    def calc_voltage_base(self):
        self._dss.text("calcvoltagebase")
