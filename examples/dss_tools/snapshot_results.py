# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : snapshot_results.py
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
# Solve the power flow for the system.
# You can use different command to solve the power flow, let's use available in dss_tools.
# There are parameters in the solve_snapshot method that you can change if desired, for instance, let's change the
# number of maximum control loop iterations
dss_tools.simulation.solve_snapshot(max_control_iter=20)

# You can get the circuit summary
circuit_summary_df = dss_tools.results.summary_df
circuit_summary_df

# You can get the voltage line-neutral nodes similar to when you use 'show voltages LN nodes'
mag_voltage_ln_nodes_df = dss_tools.results.voltage_ln_nodes[0]
mag_voltage_ln_nodes_df.head()
angle_voltage_ln_nodes_df = dss_tools.results.voltage_ln_nodes[1]
angle_voltage_ln_nodes_df.head()

# You can get the active and reactive powers for each element
p_elements_df = dss_tools.results.powers_elements[0]
p_elements_df.head()
q_elements_df = dss_tools.results.powers_elements[1]
q_elements_df.head()

# You can get magnitude and angle for the currents for each element
mag_current_df = dss_tools.results.currents_elements[0]
mag_current_df.head()
angle_current_df = dss_tools.results.currents_elements[1]
angle_current_df.head()

# You can check the loading of the elements
current_loading_df = dss_tools.results.current_loading_percent
current_loading_df.head()

# You can check the loading of the elements using the emergency amps
dss_tools.results.set_violation_current_limit_type("emerg_amps")
current_loading_df = dss_tools.results.current_loading_percent
current_loading_df.head()

# You can check for voltage violations
violations_mag_voltage_ln_nodes_df = dss_tools.results.violation_voltage_ln_nodes
# Undervoltage
violations_mag_voltage_ln_nodes_df[0].head()
# Overvoltage
violations_mag_voltage_ln_nodes_df[1].head()

dss_tools.results.set_violation_voltage_ln_limits(v_min_pu=0.98, v_max_pu=1.04)
violations_mag_voltage_ln_nodes_df = dss_tools.results.violation_voltage_ln_nodes
# Undervoltage
violations_mag_voltage_ln_nodes_df[0].head()
# Overvoltage
violations_mag_voltage_ln_nodes_df[1].head()

# You can check for thermal violations
dss_tools.results.get_violation_current_limit_type()
# Back to normal amps
dss_tools.results.set_violation_current_limit_type("norm_amps")
violations_mag_current_df = dss_tools.results.violation_currents_elements
violations_mag_current_df.head()

# You can check for thermal violations using the emergency amps
dss_tools.results.set_violation_current_limit_type("emerg_amps")
violations_mag_current_df = dss_tools.results.violation_currents_elements
violations_mag_current_df.head()

