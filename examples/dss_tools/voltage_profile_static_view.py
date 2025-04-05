# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : voltage_profile_static_view.py
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

dss.text(f"compile [{dss_file}]")
dss.text(f"buscoords buscoords.dat")
# We need to add an energymeter at the feeder head to be able to plot the voltage profile
dss_tools.model.add_line_in_vsource(add_meter=True)
dss_tools.simulation.solve_snapshot()

# We can plot the voltage profile and use all default parameters
# dss_tools.static_view.voltage_profile()

# You can change parameters by using the method arguments.
# dss_tools.static_view.voltage_profile(title=f"Voltage profile for feeder {dss.circuit.name}")

# You also can mark buses in the profile by provide a list of voltage_profile_get_bus_mark objetcs to the buses_markers of voltage_profile method.
buses_marker = [dss_tools.static_view.voltage_profile_get_bus_mark("160r", show_legend=True)]
dss_tools.static_view.voltage_profile_plot_style.legend_loc = "best"
dss_tools.static_view.voltage_profile(buses_marker=buses_marker)

# You also can use the dss_tools.static_view.voltage_profile_plot_style object to change Matplotlib atributes
# dss_tools.static_view.voltage_profile_plot_style.axes_grid = False
# dss_tools.static_view.voltage_profile()
