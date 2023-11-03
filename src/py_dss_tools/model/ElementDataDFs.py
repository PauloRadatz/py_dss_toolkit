# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ElementDataDFs.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd


class ModelDataDFs:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def lines_df(self):
        return self.__create_dataframe(self._dss.lines, "line")

    @property
    def transformers_df(self):
        return self.__create_dataframe(self._dss.transformers, "transformer")

    @property
    def meters_df(self):
        return self.__create_dataframe(self._dss.meters, "meter")

    def __create_dataframe(self, element, element_type):

        if element.count == 0:
            self._dss.text(f"New {element_type}.not_valid_element enabled=no")

        element.first()
        element_properties = self._dss.cktelement.property_names

        dict_to_df = dict()

        name_list = list()
        element.first()
        for _ in range(element.count):
            if self._dss.cktelement.is_enabled:
                name_list.append(element.name.lower())
                element.next()
        dict_to_df["name"] = name_list

        for element_property in element_properties:
            property_list = list()

            element.first()
            for _ in range(element.count):
                if self._dss.cktelement.is_enabled:
                    property_list.append(
                        self._dss.dssproperties.value_read(
                            str(self._dss.cktelement.property_names.index(element_property) + 1)))
                element.next()

            dict_to_df[element_property.lower()] = property_list

        return pd.DataFrame().from_dict(dict_to_df)

