# -*- coding: utf-8 -*-
# @Time    : 3/11/2024 2:16 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : no_study.py
# @Software: PyCharm

import os
import pathlib
import py_dss_interface
from py_dss_tools import dss_utils

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("feeders", "13Bus", "IEEE13Nodeckt.dss")

dss = py_dss_interface.DSS()
dss_utils.update_dss(dss)

dss.text(f"compile [{dss_file}]")
v = dss_utils.get_circuit_vmag_vang_dfs()

print("here")
