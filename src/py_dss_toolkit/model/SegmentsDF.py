# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com


import pandas as pd
from py_dss_interface import DSS


class SegmentsDF:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def segments_df(self) -> pd.DataFrame:
        return self.__create_dataframe()

    def __create_dataframe(self):
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
            elem_name_list.append(self._dss.cktelement.name.lower())
            elem_bus1_list.append(self._dss.cktelement.bus_names[0].split(".")[0])
            nodes1 = self._dss.cktelement.bus_names[0].split(".")[1:]
            if len(nodes1) == 0:
                elem_nodes1_list.append(["1", "2", "3"])
            else:
                elem_nodes1_list.append(nodes1)
            elem_bus2_list.append(self._dss.cktelement.bus_names[1].split(".")[0])
            nodes2 = self._dss.cktelement.bus_names[1].split(".")[1:]
            if len(nodes2) == 0:
                elem_nodes2_list.append(["1", "2", "3"])
            else:
                elem_nodes2_list.append(nodes2)
            elem_type_list.append(self._dss.cktelement.name.lower().split(".")[0])

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

        dict_df = dict()
        dict_df["name"] = elem_name_list
        dict_df["bus1"] = elem_bus1_list
        dict_df["nodes1"] = elem_nodes1_list
        dict_df["bus2"] = elem_bus2_list
        dict_df["nodes2"] = elem_nodes2_list
        dict_df["type"] = elem_type_list
        dict_df["x1"] = elem_x1_list
        dict_df["y1"] = elem_y1_list
        dict_df["x2"] = elem_x2_list
        dict_df["y2"] = elem_y2_list
        dict_df["enabled"] = enabled_list

        return pd.DataFrame.from_dict(dict_df)
