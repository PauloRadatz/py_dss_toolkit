# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Tuple

import pandas as pd
from py_dss_interface import DSS
from .snapshot_utils import create_terminal_list


class VoltagesElement:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def voltages_elements(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return self.__create_dataframe()

    def _create_voltages_element_records(self) -> Tuple[dict, dict, list]:
        element_nodes = dict()
        element_vmags = dict()
        element_vangs = dict()
        elements = list()

        is_there_pd = self._dss.circuit.pd_element_first()
        while is_there_pd:
            element = self._dss.cktelement.name.lower()
            num_terminals = self._dss.cktelement.num_terminals
            num_conductors = self._dss.cktelement.num_conductors

            nodes = create_terminal_list(self._dss.cktelement.node_order, num_terminals)
            vmags = self._dss.cktelement.voltages_mag_ang[: 2 * num_terminals * num_conductors: 2]
            vangs = self._dss.cktelement.voltages_mag_ang[1: 2 * num_terminals * num_conductors: 2]

            bus1, bus2 = self._dss.cktelement.bus_names[0].split(".")[0].lower(), \
                self._dss.cktelement.bus_names[1].split(".")[0].lower()

            self._dss.circuit.set_active_bus(bus1)
            kv_base1 = self._dss.bus.kv_base * 1000.0

            self._dss.circuit.set_active_bus(bus2)
            kv_base2 = self._dss.bus.kv_base * 1000.0

            for i in range(int(len(vmags) / 2)):
                vmags[i] = vmags[i] / kv_base1

            for i in range(int(len(vmags) / 2), len(vmags)):
                vmags[i] = vmags[i] / kv_base2

            element_nodes[element] = nodes
            element_vmags[element] = vmags
            element_vangs[element] = vangs
            elements.append(element)

            if not self._dss.circuit.pd_element_next():
                is_there_pd = False

        is_there_pc = self._dss.circuit.pc_element_first()
        while is_there_pc:
            element = self._dss.cktelement.name.lower()
            num_terminals = self._dss.cktelement.num_terminals
            num_conductors = self._dss.cktelement.num_conductors

            nodes = create_terminal_list(self._dss.cktelement.node_order, num_terminals)
            vmags = self._dss.cktelement.voltages_mag_ang[: 2 * num_terminals * num_conductors: 2]
            vangs = self._dss.cktelement.voltages_mag_ang[1: 2 * num_terminals * num_conductors: 2]

            bus1 = self._dss.cktelement.bus_names[0].split(".")[0].lower()

            self._dss.circuit.set_active_bus(bus1)
            kv_base1 = self._dss.bus.kv_base * 1000.0

            for i in range(len(vmags)):
                vmags[i] = vmags[i] / kv_base1

            element_nodes[element] = nodes
            element_vmags[element] = vmags
            element_vangs[element] = vangs
            elements.append(element)

            if not self._dss.circuit.pc_element_next():
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

    def __create_dataframe(self):
        vmags_records, vangs_records, elements = self._create_voltages_element_records()

        vmags_df = pd.DataFrame.from_dict(vmags_records, orient='index')
        vmags_df = vmags_df.reindex(elements)

        vangs_df = pd.DataFrame.from_dict(vangs_records, orient='index')
        vangs_df = vangs_df.reindex(elements)

        return vmags_df, vangs_df
