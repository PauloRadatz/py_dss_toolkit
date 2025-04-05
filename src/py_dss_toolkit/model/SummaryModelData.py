# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

import pandas as pd
from py_dss_interface import DSS


class SummaryModelData:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def summary_df(self):
        return self.__create_dataframe()

    def __create_dataframe(self):
        r_dict = dict()
        r_order = ["buses", "nodes", "ckt elements"]
        r_dict[r_order[0]] = self._dss.circuit.num_buses
        r_dict[r_order[1]] = self._dss.circuit.num_nodes
        r_dict[r_order[2]] = self._dss.circuit.num_ckt_elements

        elements_list = self._dss.circuit.elements_names

        element_counts = dict()

        for item in elements_list:
            self._dss.circuit.set_active_element(item)
            if self._dss.cktelement.is_enabled:
                element_class = item.split(".")[0]
                if element_class in element_counts:
                    element_counts[element_class] += 1
                else:
                    element_counts[element_class] = 1

        for element_class, count in element_counts.items():
            r_order.append(f"{element_class.lower()}")
            r_dict[r_order[-1]] = count

        line_length = 0
        for element in elements_list:
            if element.split(".")[0].lower() == "line":
                self._dss.circuit.set_active_element(element)
                self._dss.lines.name = element.split(".")[1].lower()
                if self._dss.cktelement.is_enabled:
                    line_length += self._dss.lines.length

        max_line_norm_amps, min_line_norm_amps = self.__get_max_min_norm_amps(elements_list, "line")
        max_transformer_norm_amps, min_transformer_norm_amps = self.__get_max_min_norm_amps(elements_list,
                                                                                            "transformer")
        max_reactor_norm_amps, min_reactor_norm_amps = self.__get_max_min_norm_amps(elements_list, "reactor")

        r_dict["line length"] = line_length
        if min_line_norm_amps != 9999:
            r_dict["line min norm amps"] = min_line_norm_amps
            r_dict["line max norm amps"] = max_line_norm_amps
        if min_transformer_norm_amps != 9999:
            r_dict["transformer min norm amps"] = min_transformer_norm_amps
            r_dict["transformer max norm amps"] = max_transformer_norm_amps
        if min_reactor_norm_amps != 9999:
            r_dict["reactor min norm amps"] = min_reactor_norm_amps
            r_dict["reactor max norm amps"] = max_reactor_norm_amps

        max_load_kw = -9999
        min_load_kw = 9999
        for element in elements_list:
            if element.split(".")[0].lower() == "load":
                self._dss.circuit.set_active_element(element)
                self._dss.loads.name = element.split(".")[1].lower()
                if self._dss.cktelement.is_enabled:
                    load_kw = self._dss.loads.kw
                    if load_kw < min_load_kw:
                        min_load_kw = load_kw
                    if load_kw > max_load_kw:
                        max_load_kw = load_kw

        if min_load_kw != 9999:
            r_dict["load min kw"] = min_load_kw
            r_dict["load max kw"] = max_load_kw

        df = pd.DataFrame.from_dict(r_dict, orient='index', columns=['count'])
        return df

    def __get_max_min_norm_amps(self, elements_list, element_type):
        max_norm_amps = -9999
        min_norm_amps = 9999
        for element in elements_list:
            if element.split(".")[0].lower() == element_type.lower():
                self._dss.circuit.set_active_element(element)
                if self._dss.cktelement.is_enabled:
                    norm_amps = self._dss.cktelement.norm_amps
                    if norm_amps < min_norm_amps:
                        min_norm_amps = norm_amps
                    if norm_amps > max_norm_amps:
                        max_norm_amps = norm_amps
        return max_norm_amps, min_norm_amps
