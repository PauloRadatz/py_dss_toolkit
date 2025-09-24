import os
import pathlib
import py_dss_interface

from py_dss_toolkit import dss_tools

script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("123Bus", "IEEE123Master.dss")

dss = py_dss_interface.DSS()

dss_tools.update_dss(dss)

dss.text(f"compile [{dss_file}]")
dss.text("solve")
dss.text("show voltages ln nodes")

lines = dss_tools.model.lines_df

print("here")