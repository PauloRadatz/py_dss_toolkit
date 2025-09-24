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

dss_tools.model.add_line_in_vsource(add_meter=True)

dss.text("solve")

# 1
# dss.text("plot profile phases=PRIMARY")

# 2
# dss_tools.dss_view.voltage_profile(phases="PRIMARY")

# 3
# dss_tools.static_view.voltage_profile(title="MY PROFILE", line_marker_size=10)

# dss_tools.static_view.voltage_profile_plot_style.axes_grid = False
# dss_tools.static_view.voltage_profile_plot_style.axes_labelsize = 20
# dss_tools.static_view.voltage_profile_plot_style.legend_loc = 0
# dss_tools.static_view.voltage_profile()

bus_160 = dss_tools.static_view.voltage_profile_get_bus_mark(name="160r",
                                                   marker_name="MY BUS",
                                                   show_legend=True,
                                                   color="orange")

# dss_tools.static_view.voltage_profile(buses_marker=[bus_160], show=False)



# 4
bus_160 = dss_tools.interactive_view.voltage_profile_get_bus_marker(name="160r",
                                                   marker_name="MY BUS",
                                                   show_legend=True,
                                                   color="orange")
dss_tools.interactive_view.voltage_profile_plot_style.grid_color = "orange"
# dss_tools.interactive_view.voltage_profile_plot_style.show_legend = False
pr = dss_tools.interactive_view.voltage_profile(show=False, buses_marker=[bus_160])
print(type(pr))
pr.show()