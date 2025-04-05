# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from py_dss_interface import DSS
import pandas as pd


class BusesDataDF:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def buses_df(self):
        return self.__create_dataframe()

    def __create_dataframe(self):
        buses = self._dss.circuit.buses_names

        dict_to_df = dict()

        bus_properties = ["name", "nodes", "num_nodes", "kv_base", "distance",
                          "coord_defined", "x", "y", "latitude", "longitude",
                          "all_pce_active_bus", "all_pde_active_bus", "line_list", "line_total_miles", "load_list",
                          "section_id", "total_customers", "unique_node_number"]

        for bus_property in bus_properties:
            property_list = list()

            for bus in buses:
                self._dss.circuit.set_active_bus(bus)
                property_list.append(getattr(self._dss.bus, bus_property))

            dict_to_df[bus_property] = property_list

        return pd.DataFrame().from_dict(dict_to_df)
