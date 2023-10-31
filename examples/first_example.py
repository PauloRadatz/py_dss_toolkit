# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : first_example.py
# @Software: PyCharm

import os
import pathlib
import py_dss_tools
from py_dss_tools.algorithms.LoadAllocation.load_allocation import LoadAllocation

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("feeders", "13Bus", "IEEE13Nodeckt.dss")

study = py_dss_tools.create_scenario(name="Test", dss_file=str(dss_file))
study.dss_utils.dss_command("New EnergyMeter.M element=Transformer.Sub terminal=1")
study.create_model_dataframes()
# study.dss_command("new line.test bus1=source bus2=B")
# study.update_model_dataframes()

# obj = study.dss_load_allocation()
# obj.check_elements()

study.dss_utils.solve_snapshot()
load_allocation = LoadAllocation(study)
# study.dss_utils.dss_command("set loadmult=3")

load_allocation.run_load_allocation_kw(5000)
study.dss_utils.solve_snapshot()

print(load_allocation.get_status())

# obj.run_load_allocation()
# study.dss_utils.dss_command("show currents elem")
study.dss_utils.dss_command("show power kva elem")

print("here")
