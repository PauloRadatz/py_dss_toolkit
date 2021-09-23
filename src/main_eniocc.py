# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 01/09/2021 at 19:27:32
 Project: py_dss_tools [set, 2021]
"""

from py_dss_tools import Scenario

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
