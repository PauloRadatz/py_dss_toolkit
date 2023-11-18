# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : Energymeters.py
# @Software: PyCharm


from py_dss_interface import DSS
import pandas as pd
from dataclasses import dataclass, field
from typing import Optional


class Energymeters:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def energymeters(self) -> Optional[pd.DataFrame]:
        return self.__create_dataframe()

    def __create_dataframe(self):
        if self._dss.meters.count == 0:
            return None

        dict_to_df = dict()

        name_list = list()
        self._dss.meters.first()
        for _ in range(self._dss.meters.count):
            if self._dss.cktelement.is_enabled:
                name_list.append(self._dss.meters.name.lower())
                self._dss.meters.next()
        dict_to_df["name"] = name_list

        for index, element_property in enumerate(self._dss.meters.register_names):
            property_list = list()

            self._dss.meters.first()
            for _ in range(self._dss.meters.count):
                property_list.append(self._dss.meters.register_values[index])
                self._dss.meters.next()

            dict_to_df[element_property.lower()] = property_list

        return pd.DataFrame().from_dict(dict_to_df)
