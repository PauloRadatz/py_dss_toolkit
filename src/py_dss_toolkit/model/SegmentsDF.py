# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com


from typing import Dict, List

import pandas as pd
from py_dss_interface import DSS


class SegmentsDF:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def segments_df(self) -> pd.DataFrame:
        return self.__create_dataframe()

    @property
    def disabled_segments_df(self) -> pd.DataFrame:
        """Segments (lines, transformers, reactors) with enabled=False."""
        df = self.segments_df
        return df[~df["enabled"]].reset_index(drop=True)

    def _create_segments_records(self) -> Dict[str, List]:
        elements_names = self._dss.circuit.elements_names

        filtered_elements = [element for element in elements_names if
                             element.lower().startswith("transformer.") or
                             element.lower().startswith("line.") or
                             element.lower().startswith("reactor.")]

        elem_name_list = list()
        elem_bus1_list = list()
        elem_nodes1_list = list()
        elem_bus2_list = list()
        elem_nodes2_list = list()
        elem_type_list = list()
        elem_x1_list = list()
        elem_y1_list = list()
        elem_x2_list = list()
        elem_y2_list = list()
        enabled_list = list()
        for elem in filtered_elements:
            self._dss.circuit.set_active_element(elem)
            elem_name = self._dss.cktelement.name.lower()
            bus_names = self._dss.cktelement.bus_names
            bus1_full = bus_names[0]
            bus2_full = bus_names[1]

            elem_name_list.append(elem_name)
            elem_bus1_list.append(bus1_full.split(".")[0])
            nodes1 = bus1_full.split(".")[1:]
            if len(nodes1) == 0:
                elem_nodes1_list.append(["1", "2", "3"])
            else:
                elem_nodes1_list.append(nodes1)
            elem_bus2_list.append(bus2_full.split(".")[0])
            nodes2 = bus2_full.split(".")[1:]
            if len(nodes2) == 0:
                elem_nodes2_list.append(["1", "2", "3"])
            else:
                elem_nodes2_list.append(nodes2)
            elem_type_list.append(elem_name.split(".")[0])

            self._dss.circuit.set_active_bus(elem_bus1_list[-1])
            elem_x1_list.append(self._dss.bus.x)
            elem_y1_list.append(self._dss.bus.y)

            self._dss.circuit.set_active_bus(elem_bus2_list[-1])
            elem_x2_list.append(self._dss.bus.x)
            elem_y2_list.append(self._dss.bus.y)

            if self._dss.text(f"? {elem}.enabled").lower() == "false":
                enabled_list.append(False)
            else:
                enabled_list.append(True)

        records = dict()
        records["name"] = elem_name_list
        records["bus1"] = elem_bus1_list
        records["nodes1"] = elem_nodes1_list
        records["bus2"] = elem_bus2_list
        records["nodes2"] = elem_nodes2_list
        records["type"] = elem_type_list
        records["x1"] = elem_x1_list
        records["y1"] = elem_y1_list
        records["x2"] = elem_x2_list
        records["y2"] = elem_y2_list
        records["enabled"] = enabled_list

        return records

    def __create_dataframe(self):
        return pd.DataFrame.from_dict(self._create_segments_records())
