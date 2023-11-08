# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : powerflow_study_example.py
# @Software: PyCharm

import os
import pathlib
import py_dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("feeders", "13Bus", "IEEE13Nodeckt.dss")

study = py_dss_tools.CreateStudy.power_flow(name="Test", dss_file=str(dss_file))

study.dss_command("New EnergyMeter.M element=Transformer.Sub terminal=1")

study.solve_snapshot()

print(study.results.voltage_ln_nodes[0])

study.view.plot_profile()
