# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : model_example.py
# @Software: PyCharm

import os
import pathlib
import py_dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("feeders", "13Bus", "IEEE13Nodeckt.dss")

study = py_dss_tools.create_scenario(name="Test", dss_file=str(dss_file))
study.dss_command("New EnergyMeter.M element=Transformer.Sub terminal=1")

# Read an element DataFrame
line_df = study.model.lines_df
generator_df = study.model.generators_df

summary_df = study.model.summary_df

line_650632 = study.model.element(element_class="line", element_name="650632")

print("here")
