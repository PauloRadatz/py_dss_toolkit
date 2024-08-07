# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : Energymeters.py
# @Software: PyCharm


from py_dss_interface import DSS
import pandas as pd
from dataclasses import dataclass, field
from typing import Optional
from py_dss_tools.dss_tools import DSSTools


class Energymeters:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def energymeters(self) -> Optional[pd.DataFrame]:
        return self.__create_dataframe()

    def __create_dataframe(self):
        return DSSTools(self._dss).results.energymeters_df()
