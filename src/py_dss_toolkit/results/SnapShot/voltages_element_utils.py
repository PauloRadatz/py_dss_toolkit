from typing import Tuple

import pandas as pd
from py_dss_interface import DSS

from .snapshot_utils import create_terminal_list


def _loop_element_names(dss: DSS) -> list:
    elements = list()

    is_there_pd = dss.circuit.pd_element_first()
    while is_there_pd:
        elements.append(dss.cktelement.name.lower())
        if not dss.circuit.pd_element_next():
            is_there_pd = False

    is_there_pc = dss.circuit.pc_element_first()
    while is_there_pc:
        elements.append(dss.cktelement.name.lower())
        if not dss.circuit.pc_element_next():
            is_there_pc = False

    return elements


def create_element_voltage_records(dss: DSS) -> Tuple[dict, dict, list]:
    """Element voltage records built from ``dss.export.elem_voltages``.

    Fast replacement for :func:`create_element_voltage_records_loop`.
    """
    csv = dss.export.elem_voltages
    lines = csv.splitlines()

    parsed_vmags = dict()
    parsed_vangs = dict()

    for line in lines[1:]:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        element = parts[0].replace('"', '').lower()
        num_terminals = int(parts[1])
        num_conductors = int(parts[2])
        nvalues = num_terminals * num_conductors

        nodes = list()
        vpus = list()
        vangs = list()
        k = 3
        for _ in range(nvalues):
            if k + 3 >= len(parts):
                break
            nodes.append(int(parts[k]))
            vangs.append(float(parts[k + 2]))
            vpus.append(float(parts[k + 3]))
            k += 4

        terminal_list = create_terminal_list(nodes, num_terminals)
        parsed_vmags[element] = {
            col: vpus[order] for order, col in enumerate(terminal_list)
        }
        parsed_vangs[element] = {
            col: vangs[order] for order, col in enumerate(terminal_list)
        }

    elements = _loop_element_names(dss)
    vmags_records = {el: parsed_vmags[el] for el in elements if el in parsed_vmags}
    vangs_records = {el: parsed_vangs[el] for el in elements if el in parsed_vangs}

    return vmags_records, vangs_records, elements


def create_element_voltage_dataframes(dss: DSS) -> Tuple[pd.DataFrame, pd.DataFrame]:
    vmags_records, vangs_records, elements = create_element_voltage_records(dss)

    vmags_df = pd.DataFrame.from_dict(vmags_records, orient='index')
    vmags_df = vmags_df.reindex(elements)

    vangs_df = pd.DataFrame.from_dict(vangs_records, orient='index')
    vangs_df = vangs_df.reindex(elements)

    return vmags_df, vangs_df


def create_element_voltage_records_loop(dss: DSS) -> Tuple[dict, dict, list]:
    element_nodes = dict()
    element_vmags = dict()
    element_vangs = dict()
    elements = list()

    is_there_pd = dss.circuit.pd_element_first()
    while is_there_pd:
        element = dss.cktelement.name.lower()
        num_terminals = dss.cktelement.num_terminals
        num_conductors = dss.cktelement.num_conductors

        nodes = create_terminal_list(dss.cktelement.node_order, num_terminals)
        vmags = dss.cktelement.voltages_mag_ang[: 2 * num_terminals * num_conductors: 2]
        vangs = dss.cktelement.voltages_mag_ang[1: 2 * num_terminals * num_conductors: 2]

        bus1, bus2 = dss.cktelement.bus_names[0].split(".")[0].lower(), \
            dss.cktelement.bus_names[1].split(".")[0].lower()

        dss.circuit.set_active_bus(bus1)
        kv_base1 = dss.bus.kv_base * 1000.0

        dss.circuit.set_active_bus(bus2)
        kv_base2 = dss.bus.kv_base * 1000.0

        for i in range(int(len(vmags) / 2)):
            vmags[i] = vmags[i] / kv_base1

        for i in range(int(len(vmags) / 2), len(vmags)):
            vmags[i] = vmags[i] / kv_base2

        element_nodes[element] = nodes
        element_vmags[element] = vmags
        element_vangs[element] = vangs
        elements.append(element)

        if not dss.circuit.pd_element_next():
            is_there_pd = False

    is_there_pc = dss.circuit.pc_element_first()
    while is_there_pc:
        element = dss.cktelement.name.lower()
        num_terminals = dss.cktelement.num_terminals
        num_conductors = dss.cktelement.num_conductors

        nodes = create_terminal_list(dss.cktelement.node_order, num_terminals)
        vmags = dss.cktelement.voltages_mag_ang[: 2 * num_terminals * num_conductors: 2]
        vangs = dss.cktelement.voltages_mag_ang[1: 2 * num_terminals * num_conductors: 2]

        bus1 = dss.cktelement.bus_names[0].split(".")[0].lower()

        dss.circuit.set_active_bus(bus1)
        kv_base1 = dss.bus.kv_base * 1000.0

        for i in range(len(vmags)):
            vmags[i] = vmags[i] / kv_base1

        element_nodes[element] = nodes
        element_vmags[element] = vmags
        element_vangs[element] = vangs
        elements.append(element)

        if not dss.circuit.pc_element_next():
            is_there_pc = False

    vmags_records = {
        element: {node: element_vmags[element][order] for order, node in enumerate(nodes)}
        for element, nodes in element_nodes.items()
    }

    vangs_records = {
        element: {node: element_vangs[element][order] for order, node in enumerate(nodes)}
        for element, nodes in element_nodes.items()
    }

    return vmags_records, vangs_records, elements


def create_element_voltage_dataframes_loop(dss: DSS) -> Tuple[pd.DataFrame, pd.DataFrame]:
    vmags_records, vangs_records, elements = create_element_voltage_records_loop(dss)

    vmags_df = pd.DataFrame.from_dict(vmags_records, orient='index')
    vmags_df = vmags_df.reindex(elements)

    vangs_df = pd.DataFrame.from_dict(vangs_records, orient='index')
    vangs_df = vangs_df.reindex(elements)

    return vmags_df, vangs_df
