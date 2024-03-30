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
dss_file = pathlib.Path(script_path).joinpath("feeders", "13Bus", "IEEE13Nodeckt.dss")

dss = py_dss_interface.DSS()
dss_tools.update_dss(dss)

dss.text(f"compile [{dss_file}]")
dss_tools.model.summary_df()
dss.text("New monitor.M1 element=Line.692675 terminal=1")
dss.text("New monitor.M1_p element=Line.692675 terminal=1 mode=1 ppolar=no")
dss.text("batchedit load..* daily=default")

dss_tools.model.add_line_in_vsource(add_meter=True)
dss.text("solve")
dss_tools.dss_view.voltage_profile()
dss_tools.view.voltage_profile_plot_style.figure_facecolor = "black"
dss_tools.view.voltage_profile()

dss.text("set mode=daily")
dss.text("solve")

dss_tools.view.p_vs_time("M1_p")
dss_tools.view.vmag_vs_time("M1")

print("here")
