# -*- coding: utf-8 -*-
# @Time    : 9/11/2024 9:22 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : test1.py
# @Software: PyCharm

import os
import pathlib
import py_dss_interface

from py_dss_tools import dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("feeders", "123Bus", "IEEE123Master.dss")
bus_coords = pathlib.Path(script_path).joinpath("feeders", "123Bus", "buscoords.dat")

dss_file = r"C:\PauloRadatz\GitHub\bdgd2opendss\dss_models_output\1_3PAS_1\Master_DO_01_1_3PAS_1.dss"

dss = py_dss_interface.DSS()
dss_tools.update_dss(dss)

dss.text(f"compile [{dss_file}]")
# dss.text("batchedit load..* daily=default")
# dss.text(f"buscoords {bus_coords}")
dss_tools.model.batchedit("energymeter", "enabled", "no")
dss_tools.model.add_line_in_vsource(add_meter=True)
# dss.text("new energymeter.m element=line.l115 terminal=1")
dss.text("solve")

dss_tools.interactive_view.voltage_profile()

print("here")
