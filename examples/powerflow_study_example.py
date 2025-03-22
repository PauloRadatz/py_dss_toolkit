# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : powerflow_study_example.py
# @Software: PyCharm

import os
import pathlib
import py_dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("feeders", "123Bus", "IEEE123Master.dss")

study = py_dss_tools.CreateStudy.snapshot(name="Test", dss_file=str(dss_file))
# study.dss.text("New EnergyMeter.M element=Transformer.Sub terminal=1")
study.model.add_line_in_vsource(add_meter=True)
study.run()

# bus_marker = [study.static_view.voltage_profile_get_bus_mark("671", annotate=True, annotation_delta_x=-2)]

# v_view = study.static_view.voltage_profile(buses_marker=bus_marker)

v_view = study.view.voltage_profile()

df = study.results.voltage_ln_nodes


print('here')
