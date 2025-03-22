# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ElementDataDFs.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd


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
    def monitors_df(self) -> pd.DataFrame:
        return self.__create_dataframe(self._dss.monitors)

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
        if element.count == 0:
            return None

        element.first()
        element_properties = self._dss.cktelement.property_names

        dict_to_df = dict()

        name_list = list()

        for element_name in element.names:
            element.name = element_name
            if self._dss.cktelement.is_enabled:
                name_list.append(element.name.lower())
        dict_to_df["name"] = name_list

        for element_property in element_properties:
            property_list = list()

            for element_name in element.names:
                element.name = element_name
                if self._dss.cktelement.is_enabled:
                    property_list.append(
                        self._dss.dssproperties.value_read(
                            str(self._dss.cktelement.property_names.index(element_property) + 1)))

            dict_to_df[element_property.lower()] = property_list

        return pd.DataFrame().from_dict(dict_to_df)
