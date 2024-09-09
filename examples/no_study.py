# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : no_study.py
# @Software: PyCharm

import os
import pathlib
import py_dss_interface

from py_dss_tools import dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("feeders", "123Bus", "IEEE123Master.dss")
bus_coords = pathlib.Path(script_path).joinpath("feeders", "123Bus", "buscoords.dat")

dss_file = r"C:\Program Files\OpenDSS\EPRITestCircuits\ckt5\Master_ckt5.dss"

dss = py_dss_interface.DSS()
dss_tools.update_dss(dss)

dss.text(f"compile [{dss_file}]")
# dss.text("batchedit load..* daily=default")
# dss.text(f"buscoords {bus_coords}")
dss_tools.model.add_line_in_vsource(add_meter=True)
dss.text("solve")

dss_tools.results.voltages_elements

# buses = [dss_tools.interactive_view.circuit_get_bus_marker("79")]
# dss_tools.interactive_view.active_power_settings.colorbar_title = "my tutkle"
# dss_tools.interactive_view.circuit_plot(parameter="phases", bus_markers=buses, width_1ph=1)

# dss_tools.interactive_view.user_numerical_defined_settings.results = dss_tools.results.powers_elements[0].iloc[:, :3].sum(axis=1)
# dss_tools.interactive_view.circuit_plot(parameter="user numerical defined")

# dss_tools.interactive_view.circuit_plot(parameter="phases", bus_markers=[dss_tools.interactive_view.circuit_get_bus_marker("79")])
# dss_tools.interactive_view.circuit_plot(parameter="voltage", dash_3ph="dot", bus_markers=[dss_tools.interactive_view.circuit_get_bus_marker("79")])

line_df = dss_tools.model.lines_df
line_df['name'] = 'line.' + line_df['name']
num_phases = line_df.set_index("name")["phases"]

dss_tools.interactive_view.circuit_plot_style.template = "plotly_white"
dss_tools.interactive_view.user_categorical_defined_settings.results = num_phases
dss_tools.interactive_view.user_categorical_defined_settings.color_map = {'3': ["3-phases", "blue"],
        '2': ["2-phases", "red"],
        '1': ["1-phase", "green"]}
dss_tools.interactive_view.circuit_plot(parameter="user categorical defined")

print("here")
