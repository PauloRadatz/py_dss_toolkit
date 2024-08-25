# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : first_example.py
# @Software: PyCharm

import os
import pathlib
import py_dss_tools
from py_dss_tools.dss_tools import dss_tools

# dss_tools.dss_command()

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("feeders", "13Bus", "IEEE13Nodeckt.dss")

s = py_dss_tools.CreateStudy.power_flow("Study", dss_file=str(dss_file))

s.model.lines_df
