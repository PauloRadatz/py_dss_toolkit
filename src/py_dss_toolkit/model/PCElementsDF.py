# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Dict, List, Optional

import pandas as pd
from py_dss_interface import DSS

_PC_PREFIXES = (
    "generator.",
    "generic5.",
    "gicline.",
    "indmach012.",
    "load.",
    "pvsystem.",
    "storage.",
    "upfc.",
    "vccs.",
    "vsconverter.",
    "windgen.",
)


class PCElementsDF:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def _pc_elements_records(self) -> Dict[str, List]:
        return self._create_pc_elements_records()

    @property
    def _enabled_pc_elements_records(self) -> Dict[str, List]:
        return self._filter_pc_elements_records(enabled=True)

    @property
    def _disabled_pc_elements_records(self) -> Dict[str, List]:
        return self._filter_pc_elements_records(enabled=False)

    @property
    def pc_elements_df(self) -> Optional[pd.DataFrame]:
        df = self.__create_dataframe(self._pc_elements_records)
        if df.empty:
            return None
        return df

    @property
    def enabled_pc_elements_df(self) -> Optional[pd.DataFrame]:
        df = self.__create_dataframe(self._enabled_pc_elements_records)
        if df.empty:
            return None
        return df.drop(columns=["enabled"]).reset_index(drop=True)

    @property
    def disabled_pc_elements_df(self) -> Optional[pd.DataFrame]:
        df = self.__create_dataframe(self._disabled_pc_elements_records)
        if df.empty:
            return None
        return df.drop(columns=["enabled"]).reset_index(drop=True)

    def _create_pc_elements_records(self) -> Dict[str, List]:
        elements_names = self._dss.circuit.elements_names

        filtered_elements = [
            elem for elem in elements_names
            if any(elem.lower().startswith(p) for p in _PC_PREFIXES)
        ]

        name_list = []
        bus1_list = []
        nodes1_list = []
        type_list = []
        enabled_list = []

        for elem in filtered_elements:
            self._dss.circuit.set_active_element(elem)
            elem_name = self._dss.cktelement.name.lower()
            bus_full = self._dss.cktelement.bus_names[0]
            parts = bus_full.split(".")

            name_list.append(elem_name)
            bus1_list.append(parts[0].lower())
            nodes1 = parts[1:] if len(parts) > 1 else ["1", "2", "3"]
            nodes1_list.append(nodes1)
            type_list.append(elem_name.split(".")[0])
            enabled_list.append(bool(self._dss.cktelement.is_enabled))

        return {
            "name": name_list,
            "bus1": bus1_list,
            "nodes1": nodes1_list,
            "type": type_list,
            "enabled": enabled_list,
        }

    def _filter_pc_elements_records(self, enabled: bool) -> Dict[str, List]:
        records = self._create_pc_elements_records()
        indexes = [i for i, value in enumerate(records["enabled"]) if value is enabled]
        return {key: [values[i] for i in indexes] for key, values in records.items()}

    def __create_dataframe(self, records: Dict[str, List]):
        return pd.DataFrame.from_dict(records)
