# -*- coding: utf-8 -*-
# @Author  : Ana Camila Mamede
# @Email   : anacamilamamede@gmail.com
# @File    : circuit_interactive_view_geomap.py
# @Software: VS Code  


# Import necessary libraries
import os
import pathlib
import py_dss_interface
from py_dss_toolkit import dss_tools

# Define the script path and path to the DSS file
script_path = os.path.dirname(os.getcwd())
dss_file = os.path.join(script_path, "feeders", "1_3PAS_1", "Master__202312598_1_3PAS_1_------1-----.dss")

# Create an instance of DSS
dss = py_dss_interface.DSS()

# Connect the DSS instance to the dss_tools
dss_tools.update_dss(dss)

# Compile the DSS model from the specified file
dss.text(f"compile [{dss_file}]")

# Solve the power flow for the system
dss.text(f"solve")

# Plot active power using default parameters
fig = dss_tools.interactive_view.circuit_geoplot(parameter="active power", show=False)
fig.show()

# Customize plot: Active power with title and custom line widths
fig = dss_tools.interactive_view.circuit_geoplot(parameter="active power", show=False, 
                                        title="<b>Active Power [KW]", 
                                        width_2ph=2, width_1ph=1)
fig.show()

# Mark a specific bus in the circuit plot
bus_list = [dss_tools.interactive_view.circuit_get_bus_marker(name=dss.circuit.buses_names[0], marker_name="My Bus", 
                                                              color="red", size=20, symbol = 'circle')]
fig = dss_tools.interactive_view.circuit_geoplot(parameter="active power", show=False, 
                                                 title="<b>Active Power [KW] with Marked Bus", 
                                                 bus_markers=bus_list)
fig.show()

# Change base map and highlight specific buses
fig = dss_tools.interactive_view.circuit_geoplot(parameter="active power", show=False, 
                                                title="<b>Active Power [KW] with Marked Bus", 
                                                bus_markers=bus_list, 
                                                map_style="satellite")
fig.show()


# Adjust power settings and plot active power with modified settings
dss_tools.interactive_view.active_power_settings.colorbar_cmax = 300
dss_tools.interactive_view.active_power_settings.colorbar_title = "P max = 300 kW"
fig = dss_tools.interactive_view.circuit_geoplot(parameter="active power", show=False,
                                                 title="<b>Active Power [KW] with changes in the power settings")
fig.show()

# Plot the voltage in the circuit
fig = dss_tools.interactive_view.circuit_geoplot(parameter="voltage", show=False, title="Voltage [pu]")
fig.show()

# We can visualize the phases in the circuit using a categorical plot, assigning specific colors to 3-phase, 2-phase, and 1-phase lines.
fig = dss_tools.interactive_view.circuit_geoplot(parameter="phases", title="Phases", show=False)
fig.show()

# User-defined numerical plot: Active power in MW
dss_tools.interactive_view.user_numerical_defined_settings.results = dss_tools.results.powers_elements[0].iloc[:, :3].sum(axis=1) / 1000
dss_tools.interactive_view.user_numerical_defined_settings.unit = "MW"
fig = dss_tools.interactive_view.circuit_geoplot(parameter="user numerical defined", title="Active Power [MW]", show=False)
fig.show()