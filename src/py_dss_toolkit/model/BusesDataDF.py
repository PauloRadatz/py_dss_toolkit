# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com

from typing import Dict, List

from py_dss_interface import DSS
import pandas as pd


class BusesDataDF:
    def __init__(self, dss: DSS):
        self._dss = dss

    @property
    def _buses_records(self) -> Dict[str, List]:
        return self._create_buses_records()

    @property
    def buses_df(self) -> pd.DataFrame:
        return self.__create_dataframe()

    def _create_buses_records(self) -> Dict[str, List]:
        buses = self._dss.circuit.buses_names

        bus_properties = ["name", "nodes", "num_nodes", "kv_base", "distance",
                          "coord_defined", "x", "y", "latitude", "longitude",
                          "all_pce_active_bus", "all_pde_active_bus", "line_list", "line_total_miles", "load_list",
                          "section_id", "total_customers"]

        records = {prop: [] for prop in bus_properties}
        for bus in buses:
            self._dss.circuit.set_active_bus(bus)
            for prop in bus_properties:
                records[prop].append(getattr(self._dss.bus, prop))

        return records

    def __create_dataframe(self):
        return pd.DataFrame.from_dict(self._create_buses_records())
