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

dss_tools.model.add_line_in_vsource(add_meter=True, add_monitors=True)

dss_tools.model.batchedit("load", "daily", "default")

dss_tools.simulation.solve_daily()

energymeters = dss_tools.results.energymeters

vi = dss_tools.results.monitor("monitor_feeder_head_vi")
pq = dss_tools.results.monitor("monitor_feeder_head_pq")

# dss_tools.dss_view.p_vs_time("monitor_feeder_head_pq")


dss_tools.static_view.monitor_plot_style.grid_color = "orange"
dss_tools.static_view.p_vs_time("monitor_feeder_head_pq", show=True)

# dss_tools.interactive_view.p_vs_time("monitor_feeder_head_pq", show=True)
# dss_tools.interactive_view.p_vs_time("monitor_feeder_head_vi", show=True)
dss_tools.interactive_view.vmag_vs_time("monitor_feeder_head_vi", show=True)

print("here")