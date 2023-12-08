# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : first_example.py
# @Software: PyCharm

import os
import pathlib
import py_dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("feeders", "13Bus", "IEEE13Nodeckt.dss")

study = py_dss_tools.CreateStudy.generic(name="Test", dss_file=str(dss_file))
study.utils.dss_command("New EnergyMeter.M element=Transformer.Sub terminal=1")
study.utils.dss_command("New monitor.MP element=Transformer.Sub terminal=1 mode=1 ppolar=no")

study.utils.dss_command("batchedit load..* daily=default")
study.dss.text("set mode=daily")
study.dss.text("solve")
# study.dss.text("sample")

# study.view.p_vs_time("MP")
voltages = study.results.voltage_ln_nodes[0]
currents = study.results.currents_elements[0]
powers = study.results.powers_elements[0]

study.view.voltage_profile()
