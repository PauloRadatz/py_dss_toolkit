# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Tuple

import pandas as pd
from py_dss_interface import DSS

from .snapshot_utils import create_terminal_list


class Powers:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def _powers_p_records(self) -> dict:
        return self._create_powers_records()[0]

    @property
    def _powers_q_records(self) -> dict:
        return self._create_powers_records()[1]

    @property
    def powers_elements(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return self.__create_dataframe()

    def _create_powers_records(self) -> Tuple[dict, dict, list]:
        element_nodes = dict()
        element_p = dict()
        element_q = dict()
        elements = list()

        is_there_pd = self._dss.circuit.pd_element_first()
        while is_there_pd:
            element = self._dss.cktelement.name.lower()
            num_terminals = self._dss.cktelement.num_terminals
            num_conductors = self._dss.cktelement.num_conductors

            nodes = create_terminal_list(self._dss.cktelement.node_order, num_terminals)
            p = self._dss.cktelement.powers[: 2 * num_terminals * num_conductors : 2]
            q = self._dss.cktelement.powers[1 : 2 * num_terminals * num_conductors : 2]

            element_nodes[element] = nodes
            element_p[element] = p
            element_q[element] = q
            elements.append(element)

            if not self._dss.circuit.pd_element_next():
                is_there_pd = False

        is_there_pc = self._dss.circuit.pc_element_first()
        while is_there_pc:
            element = self._dss.cktelement.name.lower()
            num_terminals = self._dss.cktelement.num_terminals
            num_conductors = self._dss.cktelement.num_conductors

            nodes = create_terminal_list(self._dss.cktelement.node_order, num_terminals)
            p = self._dss.cktelement.powers[: 2 * num_terminals * num_conductors : 2]
            q = self._dss.cktelement.powers[1 : 2 * num_terminals * num_conductors : 2]

            element_nodes[element] = nodes
            element_p[element] = p
            element_q[element] = q
            elements.append(element)

            if not self._dss.circuit.pc_element_next():
                is_there_pc = False

        p_records = {
            element: {node: element_p[element][order] for order, node in enumerate(nodes)}
            for element, nodes in element_nodes.items()
        }

        q_records = {
            element: {node: element_q[element][order] for order, node in enumerate(nodes)}
            for element, nodes in element_nodes.items()
        }

        return p_records, q_records, elements

    def __create_dataframe(self):
        p_records, q_records, elements = self._create_powers_records()

        p_df = pd.DataFrame.from_dict(p_records, orient="index")
        p_df = p_df.reindex(elements)

        q_df = pd.DataFrame.from_dict(q_records, orient="index")
        q_df = q_df.reindex(elements)

        return p_df, q_df
