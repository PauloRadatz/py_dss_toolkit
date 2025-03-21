# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

import os
import pathlib
from py_dss_tools import CreateStudy

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("..", "feeders", "123Bus", "IEEE123Master.dss")
bus_coords = pathlib.Path(script_path).joinpath("..", "feeders", "123Bus", "buscoords.dat")

# Creat SnapShot study object
study = CreateStudy.model_verification("My Study", dss_file=dss_file)

# Load bus coordinates for visualization
study.dss.text(f"buscoords buscoords.dat")

# Add energymeter at the feeder head
study.model.add_line_in_vsource(add_meter=True)

result_1 = study.results.isolated
print("No problem added")
print(result_1)

# Add problem
study.dss.text("edit Line.L112 bus2=open")
result_2 = study.results.isolated
print("\nproblem added")
print(result_2)

# Exploring another case
study.dss.text("edit Line.L112 bus2=112.1")

print("\nsame bus")
result = study.results.same_bus
