# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 01/09/2021 at 19:27:32
 Project: py_dss_tools [set, 2021]
"""
import py_dss_tools as pt

# TODO tqdm

sc = pt.create_scenario()

pt.create_circuit(sc, name="Meu_Circuito", bus1="sourcebus", angle=30)
print(sc.circuit)
# TODO - pegar basefreq do options
# pt.create_line(sc, name="650632", phases=3, bus1="RG60.1.2.3", bus2="632.1.2.3", length=2000, units='ft')
# pt.create_line(sc, name="632670", phases=3, bus1="632.1.2.3", bus2="670.1.2.3", length=667, units='ft')
# pt.create_line(sc, name="670671", phases=3, bus1="670.1.2.3", bus2="671.1.2.3", length=1333, units='ft')


# print(sc.dss.text("get basefrequency"))
# sc.circuit.dss.text("FormEdit circuit.Meu_Circuito")
# from tabulate import tabulate
# print(tabulate(sc.dss.circuit_name(), showindex="always", headers="keys", tablefmt="fancy_grid"))
# print(tabulate(sc.circuit.df_lines[['b0', 'b1']], showindex="always", headers="keys", tablefmt="fancy_grid"))
