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

study = py_dss_tools.CreateStudy.generic(name="Test", dss_file=str(dss_file))
study.dss_command("New EnergyMeter.M element=Transformer.Sub terminal=1")

# Read an element DataFrame
line_df = study.model.lines_df
generator_df = study.model.generators_df

summary_df = study.model.summary_df

line_650632 = study.model.element_data(element_class="line", element_name="650632")

study.model.edit_element(element_class="line", element_name="650632", properties={"length": 10})

line_650632_new = study.model.element_data(element_class="line", element_name="650632")

study.model.add_element(element_class="line", element_name="650632_1", properties={"bus1": "source_bus", "bus2":"a"})

line_650632_1 = study.model.element_data(element_class="line", element_name="650632_1")

print("here")
