# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Dict
from typing import List
from typing import Optional

import pandas as pd
from py_dss_interface import DSS

_PD_PREFIXES = (
    "autotrans.",
    "capacitor.",
    "gictransformer.",
    "line.",
    "reactor.",
    "transformer.",
)


class PDElementsDF:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def _pd_elements_records(self) -> Dict[str, List]:
        return self._create_pd_elements_records()

    @property
    def _enabled_pd_elements_records(self) -> Dict[str, List]:
        return self._filter_pd_elements_records(enabled=True)

    @property
    def _disabled_pd_elements_records(self) -> Dict[str, List]:
        return self._filter_pd_elements_records(enabled=False)

    @property
    def pd_elements_df(self) -> Optional[pd.DataFrame]:
        df = self.__create_dataframe(self._pd_elements_records)
        if df.empty:
            return None
        return df

    @property
    def enabled_pd_elements_df(self) -> Optional[pd.DataFrame]:
        df = self.__create_dataframe(self._enabled_pd_elements_records)
        if df.empty:
            return None
        return df.drop(columns=["enabled"]).reset_index(drop=True)

    @property
    def disabled_pd_elements_df(self) -> Optional[pd.DataFrame]:
        df = self.__create_dataframe(self._disabled_pd_elements_records)
        if df.empty:
            return None
        return df.drop(columns=["enabled"]).reset_index(drop=True)

    def _create_pd_elements_records(self) -> Dict[str, List]:
        elements_names = self._dss.circuit.elements_names

        filtered_elements = [elem for elem in elements_names if any(elem.lower().startswith(p) for p in _PD_PREFIXES)]

        name_list = []
        bus1_list = []
        nodes1_list = []
        bus2_list = []
        nodes2_list = []
        type_list = []
        x1_list = []
        y1_list = []
        x2_list = []
        y2_list = []
        enabled_list = []

        for elem in filtered_elements:
            self._dss.circuit.set_active_element(elem)
            elem_name = self._dss.cktelement.name.lower()
            bus_names = self._dss.cktelement.bus_names
            bus1_full = bus_names[0]
            bus2_full = bus_names[1] if len(bus_names) > 1 else ""

            name_list.append(elem_name)
            bus1_list.append(bus1_full.split(".")[0])
            nodes1 = bus1_full.split(".")[1:]
            nodes1_list.append(nodes1 if nodes1 else ["1", "2", "3"])
            bus2_list.append(bus2_full.split(".")[0] if bus2_full else "")
            nodes2 = bus2_full.split(".")[1:] if bus2_full else []
            nodes2_list.append(nodes2 if nodes2 else (["1", "2", "3"] if bus2_full else []))
            type_list.append(elem_name.split(".")[0])

            self._dss.circuit.set_active_bus(bus1_list[-1])
            x1 = self._dss.bus.x
            y1 = self._dss.bus.y
            x1_list.append(x1)
            y1_list.append(y1)

            if bus2_full:
                self._dss.circuit.set_active_bus(bus2_list[-1])
                x2_list.append(self._dss.bus.x)
                y2_list.append(self._dss.bus.y)
            else:
                x2_list.append(x1)
                y2_list.append(y1)

            enabled_list.append(bool(self._dss.cktelement.is_enabled))

        return {
            "name": name_list,
            "bus1": bus1_list,
            "nodes1": nodes1_list,
            "bus2": bus2_list,
            "nodes2": nodes2_list,
            "type": type_list,
            "x1": x1_list,
            "y1": y1_list,
            "x2": x2_list,
            "y2": y2_list,
            "enabled": enabled_list,
        }

    def _filter_pd_elements_records(self, enabled: bool) -> Dict[str, List]:
        records = self._create_pd_elements_records()
        indexes = [i for i, value in enumerate(records["enabled"]) if value is enabled]
        return {key: [values[i] for i in indexes] for key, values in records.items()}

    def __create_dataframe(self, records: Dict[str, List]):
        return pd.DataFrame.from_dict(records)
