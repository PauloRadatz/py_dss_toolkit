# -*- coding: utf-8 -*-
# @Time    : 3/30/2024 2:07 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : test.py
# @Software: PyCharm

import os
import pathlib
import py_dss_interface
from py_dss_tools import dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = r"C:\PauloRadatz\GitHub\IEEEP1729-HCA\feeders\105bus\Master.dss"

dss = py_dss_interface.DSS()
dss_tools.update_dss(dss)

dss.text(f"compile [{dss_file}]")
dss.text("set loadmult=0.2")
dss.text("solve")
dss_tools.dss_view.voltage_profile()
dss_tools.view.voltage_profile()
