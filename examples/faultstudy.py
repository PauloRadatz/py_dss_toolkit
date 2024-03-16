# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : faultstudy.py
# @Software: PyCharm

import os
import pathlib
import py_dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("feeders", "13Bus", "IEEE13Nodeckt.dss")

study = py_dss_tools.CreateStudy.fault_study(name="Test", dss_file=str(dss_file))

# study.settings.mode = "faultstudy"
study.run()

df = study.results.short_circuit_impedances
df = study.results.short_circuit_currents()
print("here")
