# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : models.py
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

# Retrieve key dataframes from the model
summary_df = dss_tools.model.summary_df  # Summary of the model
segments_df = dss_tools.model.segments_df  # Segments data of the network
buses_df = dss_tools.model.buses_df  # Bus data
lines_df = dss_tools.model.lines_df  # Line data

# Demonstrate the usage of different dss_tools methods

# Add a line in series with the Vsource, also adding a meter at the source
dss_tools.model.add_line_in_vsource(add_meter=True)

# Retrieve the data of the newly added line and inspect the first bus in the system
new_line = dss_tools.model.lines_df.iloc[-1]
new_bus = dss_tools.model.buses_df.iloc[0]

# Disable all load elements in the system
dss_tools.model.disable_elements_type("load")

# Check the updated load data
loads_df = dss_tools.model.loads_df

# Fetch data for a specific line (l115) and inspect its properties
line_l115_data = dss_tools.model.element_data("line", "l115")

# Check if the element 'l115' is present in the model
is_line_l115 = dss_tools.model.is_element_in_model("line", "l115")

# Modify properties of the line 'l115' (e.g., change its rating)
dss_tools.model.edit_element("line", "l115", dict(normamps=800, emergamps=1000))

# Verify the changes made to the line 'l115'
new_line_l115_data = dss_tools.model.element_data("line", "l115")

# Add a new load element to the system
dss_tools.model.add_element("load", "my_load", dict(phases=3, bus1=1, kv=4.16, kw=100))

# Check the updated load data
new_loads_df = dss_tools.model.loads_df


