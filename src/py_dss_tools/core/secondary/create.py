# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 24/09/2021 at 00:11:46
 Project: py_dss_tools [set, 2021]
"""
import pandas as pd

from .Scenario import Scenario
from .Circuit import Circuit
from .converter import *


def create_scenario():
    sc = Scenario()
    return sc


def check_scenario_exist():
    return Scenario.created


def check_circuit_exist():
    return Circuit.created


# TODO: exceto Circuit todos os demais devem ser adicionados diretamente no DF contindo no Circuit, posteriormente
#  converte o DF em DSS

def create_circuit(sc: Scenario, name, basekv=115, bus1='sourcebus', pu=1.0001, phases=3, angle=0, mvasc3=20000,
                   mvasc1=21000):
    if check_scenario_exist():
        sc.circuit = Circuit(sc.dss, name=name, basekv=basekv, bus1=bus1, pu=pu, phases=phases, angle=angle,
                             mvasc3=mvasc3, mvasc1=mvasc1)
        conv_circuit(sc)
    else:
        print("You must create a Scenario first!")
        exit()


def create_line_code(sc: Scenario):
    pass


def create_line(sc: Scenario, name, bus1, bus2, length=1, phases=3, linecode='', units='none'):
    row = ['', '', 60, bus1, bus2, '', '', '', '', 'Deri', 600, 'true', 0.1, '', length, '', linecode, 'oh', name, 400, 20,
           phases, '', '', '', 3, '', '', '', 1, '', 'False', '', units, '', '', '', '', '']
    if check_circuit_exist():
        sc.circuit.df_lines = row
    else:
        print("You must create a Circuit first!")
        exit()
    conv_line(sc, row)


# TODO: criar tipos de conexões, enumerate:?!
def create_load(sc: Scenario, name, bus1, phases, conn, model, kv, kw, kvar):
    pass


def create_capacitor(sc: Scenario, name, bus1, phases, kvar, kv):
    pass
