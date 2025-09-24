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

violations_mag_voltage_ln_nodes_dfs = dss_tools.results.violation_voltage_ln_nodes
undervoltage_df = violations_mag_voltage_ln_nodes_dfs[0]
overvoltage_df = violations_mag_voltage_ln_nodes_dfs[1]

dss_tools.results.set_violation_voltage_ln_limits(0.98, 1.04)

norm_violations_mag_current_df = dss_tools.results.violation_currents_elements

dss_tools.results.set_violation_current_limit_type("emerg_amps")
emerg_violations_mag_current_df = dss_tools.results.violation_currents_elements

print("here")
