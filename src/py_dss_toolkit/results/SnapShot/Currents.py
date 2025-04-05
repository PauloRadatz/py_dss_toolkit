# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Tuple

import pandas as pd
from py_dss_interface import DSS


class Currents:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def currents_elements(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return self.__create_dataframe()

    def __create_dataframe(self):
        node_order = [node.lower() for node in self._dss.circuit.y_node_order]
        element_nodes = dict()
        element_imags = dict()
        element_iangs = dict()
        elements = list()

        is_there_pd = self._dss.circuit.pd_element_first()
        while is_there_pd:
            element = self._dss.cktelement.name.lower()
            num_phases = self._dss.cktelement.num_phases
            num_terminals = self._dss.cktelement.num_terminals
            num_conductors = self._dss.cktelement.num_conductors

            nodes = self.__create_terminal_list(self._dss.cktelement.node_order, num_terminals)
            imags = self._dss.cktelement.currents_mag_ang[: 2 * num_terminals * num_conductors: 2]
            iangs = self._dss.cktelement.currents_mag_ang[1: 2 * num_terminals * num_conductors: 2]

            element_nodes[element] = nodes
            element_imags[element] = imags
            element_iangs[element] = iangs
            elements.append(element)

            if not self._dss.circuit.pd_element_next():
                is_there_pd = False

        is_there_pc = self._dss.circuit.pc_element_first()
        while is_there_pc:
            element = self._dss.cktelement.name.lower()
            num_phases = self._dss.cktelement.num_phases
            num_terminals = self._dss.cktelement.num_terminals
            num_conductors = self._dss.cktelement.num_conductors

            nodes = self.__create_terminal_list(self._dss.cktelement.node_order, num_terminals)
            imags = self._dss.cktelement.currents_mag_ang[: 2 * num_terminals * num_conductors: 2]
            iangs = self._dss.cktelement.currents_mag_ang[1: 2 * num_terminals * num_conductors: 2]

            element_nodes[element] = nodes
            element_imags[element] = imags
            element_iangs[element] = iangs
            elements.append(element)

            if not self._dss.circuit.pc_element_next():
                is_there_pc = False

        imags_df = pd.DataFrame(index=elements)

        for element, nodes in element_nodes.items():
            for order, node in enumerate(nodes):
                # column_name = f'node{node}'
                imags_df.loc[element, node] = element_imags[element][order]

        iangs_df = pd.DataFrame(index=elements)

        for element, nodes in element_nodes.items():
            for order, node in enumerate(nodes):
                # column_name = f'node{node}'
                iangs_df.loc[element, node] = element_iangs[element][order]

        return imags_df, iangs_df

    def __create_terminal_list(self, nodes, num_terminals):
        terminal_list = []
        for i, node in enumerate(nodes):
            terminal_number = int((i // (len(nodes) / num_terminals))) + 1
            terminal_list.append(f'Terminal{terminal_number}.{node}')

        return terminal_list
