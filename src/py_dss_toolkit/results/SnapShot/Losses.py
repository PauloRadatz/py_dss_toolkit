# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Tuple

import pandas as pd
from py_dss_interface import DSS


class Losses:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def _losses_p_records(self) -> dict:
        return self._create_losses_records()[0]

    @property
    def _losses_q_records(self) -> dict:
        return self._create_losses_records()[1]

    @property
    def losses_elements(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return self.__create_dataframe()

    def _create_losses_records(self) -> Tuple[dict, dict, list]:
        element_p_losses = dict()
        element_q_losses = dict()
        elements = list()

        is_there_pd = self._dss.circuit.pd_element_first()
        while is_there_pd:
            element = self._dss.cktelement.name.lower()
            losses = self._dss.cktelement.losses

            element_p_losses[element] = losses[0] / 1000.0
            element_q_losses[element] = losses[1] / 1000.0
            elements.append(element)

            if not self._dss.circuit.pd_element_next():
                is_there_pd = False

        p_records = {
            element: {"P losses (kW)": element_p_losses[element]}
            for element in elements
        }

        q_records = {
            element: {"Q losses (kvar)": element_q_losses[element]}
            for element in elements
        }

        return p_records, q_records, elements

    def __create_dataframe(self):
        p_records, q_records, elements = self._create_losses_records()

        p_df = pd.DataFrame.from_dict(p_records, orient='index')
        p_df = p_df.reindex(elements)

        q_df = pd.DataFrame.from_dict(q_records, orient='index')
        q_df = q_df.reindex(elements)

        return p_df, q_df
