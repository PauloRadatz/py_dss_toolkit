# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : SummaryModelData.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd


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
            element_class = item.split(".")[0]
            if element_class in element_counts:
                element_counts[element_class] += 1
            else:
                element_counts[element_class] = 1

        for element_class, count in element_counts.items():
            r_order.append(f"{element_class.lower()}")
            r_dict[r_order[-1]] = count

        df = pd.DataFrame.from_dict(r_dict, orient='index', columns=['count'])
        return df
