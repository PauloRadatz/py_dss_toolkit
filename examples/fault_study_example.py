# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : fault_study_example.py
# @Software: PyCharm

import os
import pathlib
import py_dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("feeders", "13Bus", "IEEE13Nodeckt.dss")

study = py_dss_tools.CreateStudy.fault_study(name="Test", dss_file=str(dss_file))
study.dss.text("New EnergyMeter.M element=Transformer.Sub terminal=1")

study.dss.text("set mode=fault")
study.dss.text("solve")
df = study.results.short_circuit_impedances



print("here")
