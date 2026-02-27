# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Tuple

import pandas as pd
from py_dss_interface import DSS


class AllLosses:
    """Total, load, and no-load losses per PD element using cktelement.all_losses.
    Returns: [P_total, Q_total, P_load, Q_load, P_no_load, Q_no_load] in kW/kvar.
    """

    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def all_losses_elements(self) -> pd.DataFrame:
        return self.__create_dataframe()

    def _create_all_losses_records(self) -> Tuple[dict, list]:
        element_records = dict()
        elements = list()

        is_there_pd = self._dss.circuit.pd_element_first()
        while is_there_pd:
            element = self._dss.cktelement.name.lower()
            all_losses = self._dss.cktelement.all_losses
            # Order: Total, load, no-load. Each complex = (P_W, Q_VAr)
            element_records[element] = {
                "P total (kW)": all_losses[0] / 1000.0,
                "Q total (kvar)": all_losses[1] / 1000.0,
                "P load (kW)": all_losses[2] / 1000.0,
                "Q load (kvar)": all_losses[3] / 1000.0,
                "P no-load (kW)": all_losses[4] / 1000.0,
                "Q no-load (kvar)": all_losses[5] / 1000.0,
            }
            elements.append(element)

            if not self._dss.circuit.pd_element_next():
                is_there_pd = False

        return element_records, elements

    def __create_dataframe(self) -> pd.DataFrame:
        records, elements = self._create_all_losses_records()
        df = pd.DataFrame.from_dict(records, orient="index")
        df = df.reindex(elements)
        return df
