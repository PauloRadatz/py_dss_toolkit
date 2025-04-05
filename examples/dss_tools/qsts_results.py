# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : qsts_results.py
# @Software: PyCharm

import os
import pathlib
import py_dss_interface
from py_dss_toolkit import dss_tools

# Define the script path and path to the DSS file
script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("..", "feeders", "123Bus", "IEEE123Master.dss")

# Create an instance of DSS
dss = py_dss_interface.DSS()

# Connect the DSS instance to the dss_tools
dss_tools.update_dss(dss)

# Compile the DSS model from the specified file
dss.text(f"compile [{dss_file}]")
# Load bus coordinates for visualization
dss.text(f"buscoords buscoords.dat")
# You can add a short line (impedance almost zero) between the Vsource.source and the first element(s)
# to make sure there is only one PD element connected to the Vsource.source. So, you can add energymeter and monitors
# for voltage and power in the feeder head.
dss_tools.model.add_line_in_vsource(add_meter=True, add_monitors=True)
# Solve the QSTS simulation for the system.
# You can use different command to solve the QSTS simulation, let's use available in dss_tools.
# There are parameters in the solve_daily method that you can change if desired.
dss_tools.simulation.solve_daily()

# You can get a dataframe with results for all meters in the system
energymeters_df = dss_tools.results.energymeters
energymeters_df

# You can get dataframe for monitors as well
monitor_pq_df = dss_tools.results.monitor("monitor_feeder_head_pq")
monitor_vi_df = dss_tools.results.monitor("monitor_feeder_head_vi")
monitor_pq_df
monitor_vi_df

