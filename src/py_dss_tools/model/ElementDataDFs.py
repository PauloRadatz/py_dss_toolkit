# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ElementDataDFs.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd
from py_dss_tools.dss_tools import DSSTools


class ElementDataDFs:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def lines_df(self) -> pd.DataFrame:
        return self.__create_dataframe(self._dss.lines)

    @property
    def transformers_df(self) -> pd.DataFrame:
        return self.__create_dataframe(self._dss.transformers)

    @property
    def meters_df(self) -> pd.DataFrame:
        return self.__create_dataframe(self._dss.meters)

    @property
    def generators_df(self) -> pd.DataFrame:
        return self.__create_dataframe(self._dss.generators)

    @property
    def vsources_df(self) -> pd.DataFrame:
        return self.__create_dataframe(self._dss.vsources)

    @property
    def regcontrols_df(self) -> pd.DataFrame:
        return self.__create_dataframe(self._dss.regcontrols)

    @property
    def loads_df(self) -> pd.DataFrame:
        return self.__create_dataframe(self._dss.loads)

    def __create_dataframe(self, element):
        return DSSTools(self._dss).model.element_data_df(element)


