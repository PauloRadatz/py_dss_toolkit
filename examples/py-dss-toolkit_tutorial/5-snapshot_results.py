import os
import pathlib
import py_dss_interface
from py_dss_toolkit import dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("123Bus", "IEEE123Master.dss")
dss = py_dss_interface.DSS()
dss_tools.update_dss(dss)

dss.text(f"compile [{dss_file}]")
dss.text("buscoords buscoords.dat")

dss_tools.simulation.solve_snapshot(max_iterations=20, max_control_iter=20)

summary = dss_tools.results.summary_df

bus_vmag = dss_tools.results.voltage_ln_nodes[0]
bus_vang = dss_tools.results.voltage_ln_nodes[1]

elem_vmag = dss_tools.results.voltages_elements[0]
elem_vang = dss_tools.results.voltages_elements[1]

elem_imag = dss_tools.results.currents_elements[0]
lines_df = dss_tools.model.lines_df

norm_current_loading_percent = dss_tools.results.current_loading_percent
dss_tools.results.set_violation_current_limit_type("emerg_amps")
emerg_current_loading_percent = dss_tools.results.current_loading_percent
print("here")