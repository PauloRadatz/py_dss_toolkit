# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : static.py
# @Software: PyCharm

import os
import pathlib
from py_dss_tools import CreateStudy

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("..", "feeders", "123Bus", "IEEE123Master.dss")
bus_coords = pathlib.Path(script_path).joinpath("..", "feeders", "123Bus", "buscoords.dat")

# Creat SnapShot study object
study = CreateStudy.snapshot("My Study", dss_file=dss_file)

# Load bus coordinates for visualization
study.dss.text(f"buscoords buscoords.dat")

# Add energymeter at the feeder head
study.model.add_line_in_vsource(add_meter=True)

# Run snapshot simulation
study.run()

# You can use results to get powers, currents, voltages, circuit summary results
p_kw_df = study.results.powers_elements[0]
q_kvar_df = study.results.powers_elements[1]

study.static_view.voltage_profile()

study.interactive_view.voltage_profile()

study.interactive_view.circuit_plot()

study.dss_view.voltage_profile()
