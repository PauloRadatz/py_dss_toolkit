# -*- coding: utf-8 -*-
# @Time    : 8/6/2024 5:24 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : vericacao.py
# @Software: PyCharm

import os
import pathlib
import py_dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("feeders", "13Bus", "IEEE13Nodeckt.dss")

study = py_dss_tools.CreateStudy.analysis_feeder_opendss_study(name="Test", dss_file=str(dss_file))
study.dss.text("New EnergyMeter.M element=Transformer.Sub terminal=1")
study.results.summary

print("here")
