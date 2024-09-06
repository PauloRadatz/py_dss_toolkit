# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : no_study.py
# @Software: PyCharm

import os
import pathlib
import py_dss_interface
from py_dss_tools import dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("feeders", "123Bus", "IEEE123Master.dss")
bus_coords = pathlib.Path(script_path).joinpath("feeders", "123Bus", "buscoords.dat")

dss = py_dss_interface.DSS()
dss_tools.update_dss(dss)

dss.text(f"compile [{dss_file}]")
dss.text("batchedit load..* daily=default")
dss.text(f"buscoords {bus_coords}")
dss_tools.model.add_line_in_vsource(add_meter=True)
dss.text("solve")


dss_tools.interactive_view.plot_feeder_topology()

# dss_tools.static_view.vmag_vs_time("v")
# dss_tools.static_view.p_vs_time("p")
#
# dss_tools.interactive_view.vmag_vs_time("v")
# dss_tools.interactive_view.p_vs_time("p")

# dss_tools.dss_view.vmag_vs_time("v")
# dss_tools.dss_view.p_vs_time("p")

print("here")
