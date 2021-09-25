# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 24/09/2021 at 01:09:46
 Project: py_dss_tools [set, 2021]
"""
from py_dss_tools.core.secondary import Scenario


def conv_circuit(sc: Scenario):
    dss = sc.dss
    circuit = sc.circuit

    my_dict = {}

    for item, value in circuit.__dict__.items():
        if '_df' not in item and 'dss' not in item:
            item = item.replace("_VSource__", "")
            item = item.replace("_Circuit__", "")
            if item == 'name':
                continue
            if value == '':
                continue
            else:
                my_dict[item] = value

    result = ''
    for k, v in my_dict.items():
        result += f"{k}={v} "
    dss.text(f"new circuit.{sc.circuit.name} {result}")
    # dss.text(f"FormEdit circuit.{sc.circuit.name}")


def conv_line(sc: Scenario, row):
    total = zip(sc.circuit.df_lines.columns, row)
    result = ''
    name = 'unknow_line'
    for item, value in total:
        if item == 'name':
            name = value
            continue
        if value == '':
            continue
        result += f" {item}={value} "
    result = f"new line.{name} {result}"
    sc.dss.text(result)





    # for index, line in sc.circuit.df_lines.iterrows():
    #     print(index, line['bus1'], line['bus2'])
