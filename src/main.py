# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 01/09/2021 at 19:27:32
 Project: py_dss_tools [set, 2021]
"""

# import py_dss_tools as pt
# import py_dss_tools.core as core

from py_dss_tools import Scenario
from py_dss_tools import Line
from py_dss_tools import Transformer
import pandas as pd

# Creating a Scenario from zero
scenario = Scenario()

# PD Elements
print(scenario.circuit.auto_transformers)
print(scenario.circuit.capacitors)
print(scenario.circuit.gictransformers)
print(scenario.circuit.lines)
print(scenario.circuit.reactors)
print(scenario.circuit.transformers)

# PC Elements
print(scenario.circuit.generators)
print(scenario.circuit.generic5)
print(scenario.circuit.giclines)
print(scenario.circuit.indmach012)
print(scenario.circuit.loads)
print(scenario.circuit.pvsystems)
print(scenario.circuit.storages)
print(scenario.circuit.upfcs)

print(scenario.circuit.vccs)
scenario.circuit.vccs.loc[0] = ['60', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
print()
print(scenario.circuit.vccs.loc[0]['basefreq'])




























## Creating a Scenario from file
# dss_file = r"C:\OpenDSS\IEEETestCases\13Bus\IEEE13Nodeckt.dss"
# dss_file_1 = r"C:\OpenDSS\IEEETestCases\123Bus\IEEE123Master.dss"

# scenario = Scenario(file=dss_file, logging=False)
# scenario.create_scenario_from_file()

# line_0 = Line(scenario, 'My_Line_00', 633, 634)
# print(line_0)

# lines = list()
# lines_from_file = pd.read_csv(r"C:\Users\eniocc\Desktop\py_dss_tools\src\py_dss_tools\networks\13BUs\lines.csv",
#                               delimiter=",")
# for index, row in lines_from_file.iterrows():
#     l = Line(scenario, row['NAME'], row['BUS1'], row['BUS2'], )
#     lines.append(l)
#
# scenario.edit_line('LINE_1', line_code='xxx')
# for l in lines:
#     print(l)
# scenario.dss.text("FormEdit Line.My_Line_00")

# scenario = Scenario()
# scenario.create_scenario()
#
# trafos = list()
# for _ in range(10):
#     trafo = Transformer()
#     trafos.append(trafo)
# trafo.new(scenario.circuit)
# scenario.select(Transformer.name, 'TR1')
# for traf in trafos:
#     traf.__str__()
# print(scenario.dss.text("currents"))
# print(scenario.id)
# print(scenario.losses())
# print(scenario.circuit.seq_currents())
# print(scenario.circuit.seq_powers())
# print(scenario.circuit.seq_voltages())
# summ = scenario.summary()
# print(summ["Status "])

# buses = scenario.circuit.get_all_buses()
# print(buses)
#
#
#
# scenario.clear_all()
# scenario.clear()
# scenario.end_scenario()


# ActiveClass OK
# scenario.dss.active_class_first()
# scenario.dss.active_class_next()
# print(scenario.dss.active_class_count())
# print(scenario.dss.active_class_get_name())
# print(scenario.dss.active_class_get_class_name())
# print(scenario.dss.active_class_parent_class_name())
# print(scenario.dss.active_class_all_names())


# scenario.solve_scenario()
# scenario.select('regcontrol', 'reg3')
# print(scenario.dss.active_class_get_name())
# scenario.select('regcontrol', 'reg2')
# print(scenario.dss.active_class_get_class_name())
# scenario.select('linecode', 'mtx603')
# print(scenario.dss.active_class_get_class_name())
# print(scenario.dss.active_class_get_name())
# scenario.select('load', '646')
# print(scenario.dss.active_class_get_class_name())
# print(scenario.dss.active_class_get_name())

# Circuit.create_circuit(dss, dss_file)
# Circuit.get_all_buses(dss)
# Circuit.get_all_lines(dss)
# dss.solution_solve()
# print(dss.circuit_all_bus_volts())


# dss.solution_solve()
# print(dss.circuit_all_bus_volts())
