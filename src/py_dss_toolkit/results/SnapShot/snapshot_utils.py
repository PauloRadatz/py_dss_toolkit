# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

import pandas as pd
from py_dss_interface import DSS
from typing import Tuple

_violation_current_limit_type = "norm_amps"

def set_violation_current_limit_type(limit_type: str = "norm_amps"):
    global _violation_current_limit_type
    assert limit_type in ("norm_amps", "emerg_amps"), "limit_type must be 'norm_amps' or 'emerg_amps'"
    _violation_current_limit_type = limit_type

def get_violation_current_limit_type() -> str:
    return _violation_current_limit_type

def create_terminal_list(nodes, num_terminals):
    terminal_list = []
    for i, node in enumerate(nodes):
        terminal_number = int((i // (len(nodes) / num_terminals))) + 1
        terminal_list.append(f'Terminal{terminal_number}.{node}')
    return terminal_list

def create_currents_elements_records(dss: DSS) -> Tuple[dict, dict, list, dict, dict]:
    element_nodes = dict()
    element_imags = dict()
    element_iangs = dict()
    element_norm_amps = dict()
    element_emerg_amps = dict()
    elements = list()

    is_there_pd = dss.circuit.pd_element_first()
    while is_there_pd:
        element = dss.cktelement.name.lower()
        num_terminals = dss.cktelement.num_terminals
        num_conductors = dss.cktelement.num_conductors
        nodes = create_terminal_list(dss.cktelement.node_order, num_terminals)
        imags = dss.cktelement.currents_mag_ang[: 2 * num_terminals * num_conductors: 2]
        iangs = dss.cktelement.currents_mag_ang[1: 2 * num_terminals * num_conductors: 2]
        element_nodes[element] = nodes
        element_imags[element] = imags
        element_iangs[element] = iangs
        element_norm_amps[element] = dss.cktelement.norm_amps
        element_emerg_amps[element] = dss.cktelement.emerg_amps
        elements.append(element)
        if not dss.circuit.pd_element_next():
            is_there_pd = False

    is_there_pc = dss.circuit.pc_element_first()
    while is_there_pc:
        element = dss.cktelement.name.lower()
        num_terminals = dss.cktelement.num_terminals
        num_conductors = dss.cktelement.num_conductors
        nodes = create_terminal_list(dss.cktelement.node_order, num_terminals)
        imags = dss.cktelement.currents_mag_ang[: 2 * num_terminals * num_conductors: 2]
        iangs = dss.cktelement.currents_mag_ang[1: 2 * num_terminals * num_conductors: 2]
        element_nodes[element] = nodes
        element_imags[element] = imags
        element_iangs[element] = iangs
        elements.append(element)
        if not dss.circuit.pc_element_next():
            is_there_pc = False

    imags_records = {
        element: {node: element_imags[element][order] for order, node in enumerate(nodes)}
        for element, nodes in element_nodes.items()
    }

    iangs_records = {
        element: {node: element_iangs[element][order] for order, node in enumerate(nodes)}
        for element, nodes in element_nodes.items()
    }

    return imags_records, iangs_records, elements, element_norm_amps, element_emerg_amps

def create_currents_elements_dataframes(dss: DSS) -> Tuple[pd.DataFrame, pd.DataFrame]:
    imags_records, iangs_records, elements, _, _ = create_currents_elements_records(dss)

    imags_df = pd.DataFrame.from_dict(imags_records, orient='index')
    imags_df = imags_df.reindex(elements)

    iangs_df = pd.DataFrame.from_dict(iangs_records, orient='index')
    iangs_df = iangs_df.reindex(elements)

    return imags_df, iangs_df
