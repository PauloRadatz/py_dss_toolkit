# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 01/09/2021 at 19:27:32
 Project: py_dss_tools [set, 2021]
"""
import py_dss_tools as pt

# TODO tqdm

sc = pt.create_scenario()
pt.create_circuit(sc, name="Meu_Circuito", bus1="sourcebus", angle=30)
sc.circuit.dss.text("FormEdit circuit.Meu_Circuito")
