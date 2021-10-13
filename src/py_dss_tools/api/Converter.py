# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 09/10/2021 at 01:10:03
 Project: py-dss-tools [out, 2021]
"""
from py_dss_tools.secondary.Scenario import Scenario


def conv_circuit(sc: Scenario):
    dss = sc.dss
    circuit = sc.circuit

    my_dict = {}
    for item, value in circuit.__dict__.items():
        if '_df' not in item and 'dss' not in item:
            item = item.replace("_Other__", "")
            item = item.replace("_VSource__", "")
            item = item.replace("_Circuit__", "")
            item = item.replace("_", "")
            if item in ['name', 'id']:
                continue
            if value == '':
                continue
            else:
                my_dict[item] = value

    result = ''.join(f"{k}={v} " for k, v in my_dict.items())
    dss.text(f"new circuit.{sc.circuit.name} {result}")


def conv_line(sc: Scenario, row):
    total = zip(sc.circuit.df_lines.columns_, row)
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
