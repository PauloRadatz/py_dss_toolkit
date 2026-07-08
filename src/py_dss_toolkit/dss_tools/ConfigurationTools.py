# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

import pathlib
from typing import Dict
from typing import Union

from py_dss_interface import DSS


class ConfigurationTools:
    def __init__(self, dss: DSS):
        self._dss = dss

    def compile_dss(self, dss_file: Union[str, pathlib.Path]):
        self._dss.text("ClearAll")
        self._dss.text(f"Compile [{dss_file}]")

    def calc_voltage_base(self):
        self._dss.text("calcvoltagebase")

    def circuit_readiness(self) -> Dict[str, Union[bool, str]]:
        names = self._dss.circuit.elements_names
        if not names:
            return {
                "ready": False,
                "code": "no_elements",
                "message": "No circuit elements; compile a DSS file first.",
            }
        return {"ready": True, "code": "ok", "message": ""}
