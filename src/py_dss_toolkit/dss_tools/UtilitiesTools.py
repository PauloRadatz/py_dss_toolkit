# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com

from typing import Optional

from py_dss_interface import DSS


class UtilitiesTools:

    def __init__(self, dss: DSS):
        self._dss = dss

    def save_circuit(self, output_dir: Optional[str] = None, case_name: Optional[str] = None):
        if output_dir:
            self._dss.dssinterface.datapath = f"{output_dir}"

        if case_name:
            self._dss.text(f"set casename='{case_name}'")
            self._dss.text(f"save circuit Dir={case_name}")
        else:
            self._dss.text(f"save circuit")
