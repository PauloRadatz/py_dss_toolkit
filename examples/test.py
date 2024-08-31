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
# dss_tools.dss_view.voltage_profile()

bus_marker = [dss_tools.static_view.voltage_profile_get_bus_mark("bus_26", annotate=True, annotation_delta_x=-2)]
dss_tools.static_view.voltage_profile(ylim=[0.95, 1.05], buses_marker=bus_marker)

bus_marker = [dss_tools.interactive_view.voltage_profile_get_bus_mark("bus_26", symbol="x", size=30, color="black", annotate=True)]
dss_tools.interactive_view.voltage_profile(buses_marker=bus_marker, ylim=[0.95, 1.05])

dss_tools.dss_view.voltage_profile()
