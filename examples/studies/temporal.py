# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : temporal.py
# @Software: PyCharm

import os
import pathlib

from py_dss_tools import CreateStudy

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("..", "feeders", "123Bus", "IEEE123Master.dss")
bus_coords = pathlib.Path(script_path).joinpath("..", "feeders", "123Bus", "buscoords.dat")

# Creat SnapShot study object
study = CreateStudy.timeseries("My Study", dss_file=dss_file)

# Load bus coordinates for visualization
study.dss.text(f"buscoords buscoords.dat")

# Set loadshape to all loads
study.model.batchedit("load", "daily", "default")

# Add energymeter and monitors at the feeder head
study.model.add_line_in_vsource()

# Run temporal simulation
study.run()

energymeters_df = study.results.energymeters
monitor_pq_df = study.results.monitor("monitor_feeder_head_pq")


study.static_view.p_vs_time("monitor_feeder_head_pq")

study.interactive_view.p_vs_time("monitor_feeder_head_pq")

study.dss_view.p_vs_time("monitor_feeder_head_pq")

print("here")
