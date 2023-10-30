# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ElectricModel.py
# @Software: PyCharm

from py_dss_interface import DSS
import attr
import pandas as pd
from dataclasses import dataclass, field

@dataclass(kw_only=True)
class ElectricModel:
    _dss: DSS = field(init=True, repr=False)
    _lines: pd.DataFrame = field(init=False, repr=False)

    def __post_init__(self):
        self._lines = self.__create_dataframe(self._dss.lines)
        self._transformers = self.__create_dataframe(self._dss.transformers)

    @property
    def lines(self):
        return self._lines

    @property
    def transformers(self):
        return self._transformers

    def __create_dataframe(self, element):
        element.first()
        element_properties = self._dss.cktelement.property_names

        dict_to_df = dict()

        name_list = list()
        element.first()
        for _ in range(element.count):
            name_list.append(element.name)
            element.next()
        dict_to_df["name"] = name_list

        for element_property in element_properties:
            property_list = list()

            element.first()
            for _ in range(element.count):
                property_list.append(
                    self._dss.dssproperties.value_read(str(self._dss.cktelement.property_names.index(element_property) + 1)))
                element.next()

            dict_to_df[element_property] = property_list

        return pd.DataFrame().from_dict(dict_to_df)
