# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : ElementData.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd


class ElementData:
    def __init__(self, dss: DSS):
        self._dss = dss

    def element_data(self, element_class, element_name):
        self.__is_element_in_model(element_class, element_name)

        self._dss.text(f"select {element_class}.{element_name}")

        element_properties = self._dss.cktelement.property_names

        dict_to_df = dict()
        dict_to_df["name"] = element_name

        for element_property in element_properties:
            property_list = list()

            property_list.append(
                self._dss.dssproperties.value_read(
                    str(self._dss.cktelement.property_names.index(element_property) + 1)))

            dict_to_df[element_property.lower()] = property_list

        df = pd.DataFrame().from_dict(dict_to_df)
        df.set_index("name", inplace=True)

        return df.T

    def __is_element_in_model(self, element_class, element_name):
        elements_list = [e.lower() for e in self._dss.circuit.elements_names]
        element_full_name = f"{element_class}.{element_name}"
        if element_full_name not in elements_list:
            raise ValueError(f"Model does not have {element_class}.{element_name}")

    def edit_element(self, element_class, element_name, properties):
        self.__is_element_in_model(element_class, element_name)

        self._dss.text(f"select {element_class}.{element_name}")
        element_properties = self._dss.cktelement.property_names

        dss_string = f"edit {element_class}.{element_name} "

        for p, v in properties.items():
            if p.lower() not in element_properties:
                raise ValueError(f"{element_class}.{element_name} does not have property {p}")
            dss_string = dss_string + f" {p}={v}"

        self._dss.text(dss_string)

