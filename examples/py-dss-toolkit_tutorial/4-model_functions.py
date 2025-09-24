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

meters_df = dss_tools.model.meters_df
dss_tools.model.add_line_in_vsource(add_meter=True)
meters_new_df = dss_tools.model.meters_df
lines_new_df = dss_tools.model.lines_df

dss_tools.model.add_element("load", "my_load", dict(phases=3, bus1=1, kv=4.16, kw=100))
new_2_loads_df = dss_tools.model.loads_df

dss_tools.model.edit_element("load", "my_load", dict(bus1=10))
new_3_loads_df = dss_tools.model.loads_df

loads_df = dss_tools.model.loads_df
# dss_tools.model.disable_elements_type("load")
# new_loads_df = dss_tools.model.loads_df

dss_tools.model.batchedit("load", "daily", "default")
loads_new_df = dss_tools.model.loads_df


is_line_l115 = dss_tools.model.is_element_in_model("line", "l115")
line_l115_data = dss_tools.model.element_data("line", "l115")

print("here")