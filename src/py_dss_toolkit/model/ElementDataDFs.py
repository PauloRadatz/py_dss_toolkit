# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com


from typing import Optional, Dict, List

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

    def _create_element_data_records(self, element) -> Optional[Dict[str, List]]:
        if element.count == 0:
            return None

        element.first()
        element_properties = self._dss.cktelement.property_names
        prop_keys = [p.lower() for p in element_properties]
        num_props = len(element_properties)

        rows = []
        for element_name in element.names:
            element.name = element_name
            if self._dss.cktelement.is_enabled:
                row = [element.name.lower()]
                for idx in range(num_props):
                    row.append(self._dss.dssproperties.value_read(str(idx + 1)))
                rows.append(row)

        if not rows:
            return None

        columns = ["name"] + prop_keys
        records = {col: [r[i] for r in rows] for i, col in enumerate(columns)}
        return records

    def __create_dataframe(self, element):
        records = self._create_element_data_records(element)
        if records is None:
            return None
        return pd.DataFrame.from_dict(records)
