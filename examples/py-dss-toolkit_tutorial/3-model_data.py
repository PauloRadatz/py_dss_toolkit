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

line_df = dss_tools.model.lines_df
buses_df = dss_tools.model.buses_df
segments_df = dss_tools.model.segments_df
summary_df = dss_tools.model.summary_df


print("here")

