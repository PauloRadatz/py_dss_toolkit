# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : first_example.py
# @Software: PyCharm

import os
import pathlib
import py_dss_tools
import py_dss_interface

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("feeders", "13Bus", "IEEE13Nodeckt.dss")

dss = py_dss_interface.DSS()

study = py_dss_tools.create_scenario(dss=dss, name="Test", dss_file=str(dss_file))

study.create_model_dataframes()
study.dss_command("new line.test bus1=source bus2=B")
study.update_model_dataframes()

print("here")
