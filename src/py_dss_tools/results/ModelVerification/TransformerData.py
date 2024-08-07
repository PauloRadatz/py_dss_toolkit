# -*- coding: utf-8 -*-
# @Author  : Iury Zanelato
# @Email   : iury.ribeirozanelato@gmail.com
# @File    : Transformer_data.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import Tuple

class TransformerData:

    def __init__(self, dss: DSS):
        self._dss = dss
        self._transformer_data = pd.DataFrame()
    @property
    def transformer_data(self) -> pd.DataFrame:
        return self.__check_tr_3_wdg() #Todo - it should return a dataframe with the element names
    def __check_tr_3_wdg(self):
        self._dss.transformers.first()
        for _ in range(self._dss.transformers.count):
            num_wdg = self._dss.transformers.num_windings

            if num_wdg == 3:
                self._dss.transformers.wdg = 3
                if self._dss.transformers.kv == 12.47:
                    print(f"transformer {self._dss.transformers.name} with kv missing")

                wdg_3_bus = self._dss.cktelement.bus_names[-1].lower()

                if wdg_3_bus == f"{self._dss.transformers.name.lower()}_3":
                    print(f"transformer {self._dss.transformers.name} with bus missing")

            self._dss.transformers.next()

        self._dss.text("solve")
        num_wdg

