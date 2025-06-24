# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : circuit_interactive_view.py
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
# Solve the power flow for the system
dss.text(f"solve")

dss_tools.interactive_view.circuit_plot(parameter="active power")

dss_tools.interactive_view.circuit_plot(parameter="active power", title="Active Power [KW]", width_2ph=2, width_1ph=1)

dss_tools.interactive_view.circuit_plot(parameter="active power", title="Active Power [KW] with dash", dash_2ph="dot", dash_1ph="dash")

bus_list = [dss_tools.interactive_view.circuit_get_bus_marker(name="79", marker_name="My Bus", color="red", size=20)]
dss_tools.interactive_view.circuit_plot(parameter="active power", title="Active Power [KW] with Marked Bus", dash_2ph="dot", dash_1ph="dash", bus_markers=bus_list)

dss_tools.interactive_view.active_power_settings.colorbar_cmax = 5000
dss_tools.interactive_view.active_power_settings.colorbar_title = "P max = 5000 kW"
dss_tools.interactive_view.circuit_plot(parameter="active power", title="Active Power [KW] with changes in the power settings")

dss_tools.interactive_view.circuit_plot(parameter="voltage", title="Voltage [pu]")

dss_tools.interactive_view.user_numerical_defined_settings.results = dss_tools.results.powers_elements[0].iloc[:, :3].sum(axis=1) / 1000
dss_tools.interactive_view.user_numerical_defined_settings.unit = "MW"
dss_tools.interactive_view.circuit_plot(parameter="user numerical defined", title="Active Power [MW]")


dss_tools.interactive_view.circuit_plot(parameter="phases", title="Phases")

line_df = dss_tools.model.lines_df
line_df['name'] = 'line.' + line_df['name']
num_phases = line_df.set_index("name")["phases"]

dss_tools.interactive_view.user_categorical_defined_settings.results = num_phases
dss_tools.interactive_view.user_categorical_defined_settings.color_map = {'3': ["3-phases", "blue"],
        '2': ["2-phases", "red"],
        '1': ["1-phase", "green"]}
dss_tools.interactive_view.circuit_plot(parameter="user categorical defined", title="My Phases")
