# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 09/10/2021 at 01:07:44
 Project: py-dss-tools [out, 2021]
"""
from py_dss_tools.api.Converter import conv_circuit, conv_line
from py_dss_tools.core.Scenario import Scenario
from py_dss_tools.core.secondary import Circuit
from py_dss_tools.utils import Utils


def check_scenario_exist(sc):
    return isinstance(sc, Scenario)


def check_circuit_exist(circuit):
    return isinstance(circuit, Circuit)


def create_scenario():
    """Create a scenario to starts work with OpenDSS."""
    return Scenario()


# TODO: exceto Circuit todos os demais devem ser adicionados diretamente no DF contindo no Circuit, posteriormente
#  converte o DF em DSS


def create_circuit(sc: Scenario, name, basekv=115, bus1='sourcebus', pu=1.0001, phases=3, angle=0, mvasc3=20000,
                   mvasc1=21000):
    name = Utils.remove_blank_spaces(name)
    if check_scenario_exist(sc):
        sc.circuit = Circuit(sc.dss, name=name, basekv=basekv, bus1=bus1, pu=pu, phases=phases, angle=angle,
                             mvasc3=mvasc3, mvasc1=mvasc1)
        conv_circuit(sc)
        # update_circuit_df(sc)
    else:
        print("You must create a Scenario first!")
        exit()


def update_circuit_df(sc: Scenario):
    if sc.circuit.created:
        names = sc.circuit.dss.cktelement_all_property_names()
        total = int(sc.circuit.dss.cktelement_num_properties())
        for i in range(total):
            command_ = f"sc.circuit.{names[i].lower()} = '{sc.circuit.dss.dssproperties_read_value(str(i + 1))}'"
            exec(command_)


def create_line(sc: Scenario, name, bus1, bus2, length=1, phases=3, linecode='', units='none'):
    # basefreq = sc.frequency_base
    row = ['', '', 60, bus1, bus2, '', '', '', '', 'Deri', 600, 'true', 0.1, '', length, '', linecode, 'oh', name, 400,
           20,
           phases, '', '', '', 3, '', '', '', 1, '', 'False', '', units, '', '', '', '', '']
    if check_circuit_exist(sc.circuit):
        sc.circuit.df_lines = row
    else:
        print("You must create a Circuit first!")
        exit()
    conv_line(sc, row)

# TODO: criar tipos de conexões, enumerate:?!
