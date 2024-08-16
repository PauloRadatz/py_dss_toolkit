# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : Powers.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from dataclasses import dataclass, field
from typing import Tuple


class Powers:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def powers_elements(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return self.__create_dataframe()

    def __create_dataframe(self):
        node_order = [node.lower() for node in self._dss.circuit.y_node_order]
        element_nodes = dict()
        element_p = dict()
        element_q = dict()
        elements = list()

        is_there_pd = self._dss.circuit.pd_element_first()
        while is_there_pd:
            element = self._dss.cktelement.name.lower()
            num_phases = self._dss.cktelement.num_phases
            num_terminals = self._dss.cktelement.num_terminals
            num_conductors = self._dss.cktelement.num_conductors

            nodes = self.__create_terminal_list(self._dss.cktelement.node_order, num_terminals)
            p = self._dss.cktelement.powers[: 2 * num_terminals * num_conductors: 2]
            q = self._dss.cktelement.powers[1: 2 * num_terminals * num_conductors: 2]

            element_nodes[element] = nodes
            element_p[element] = p
            element_q[element] = q
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
            p = self._dss.cktelement.powers[: 2 * num_terminals * num_conductors: 2]
            q = self._dss.cktelement.powers[1: 2 * num_terminals * num_conductors: 2]

            element_nodes[element] = nodes
            element_p[element] = p
            element_q[element] = q
            elements.append(element)

            if not self._dss.circuit.pc_element_next():
                is_there_pc = False

        p_df = pd.DataFrame(index=elements)

        for element, nodes in element_nodes.items():
            for order, node in enumerate(nodes):
                # column_name = f'node{node}'
                p_df.loc[element, node] = element_p[element][order]

        q_df = pd.DataFrame(index=elements)

        for element, nodes in element_nodes.items():
            for order, node in enumerate(nodes):
                # column_name = f'node{node}'
                q_df.loc[element, node] = element_q[element][order]

        return p_df, q_df

    # TODO move around
    def __create_terminal_list(self, nodes, num_terminals):
        terminal_list = []
        for i, node in enumerate(nodes):
            terminal_number = int((i // (len(nodes) / num_terminals))) + 1
            terminal_list.append(f'Terminal{terminal_number}.{node}')

        return terminal_list
