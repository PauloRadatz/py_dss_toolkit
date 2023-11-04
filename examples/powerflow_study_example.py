# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : powerflow_study_example.py
# @Software: PyCharm

import os
import pathlib
import py_dss_tools
from py_dss_tools.algorithms.PowerFlow import PowerFlow

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("feeders", "13Bus", "IEEE13Nodeckt.dss")

study = py_dss_tools.create_scenario(name="Test", dss_file=str(dss_file), study_type="powerflow")
study.dss_command("New EnergyMeter.M element=Transformer.Sub terminal=1")

study.solve_snapshot()

print(study.model.lines_df)
