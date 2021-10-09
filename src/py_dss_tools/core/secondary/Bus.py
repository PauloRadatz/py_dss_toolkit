# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 01/09/2021 at 19:51:00
 Project: py_self.dss_tools [set, 2021]
"""
import pandas as pd


class Bus:
    name = "Bus"
    name_plural = "Buses"
    columns = []

    def __init__(self, dss):
        self.dss = dss

    def get_buses(self):
        buses = {
            'names': self.dss.circuit_all_bus_names(),
            'base_kv': [],
            'num_nodes': [],
            'coordinates': [],
            'distance': [],
            'failure_rate_downstream': [],
            'bus_interruptions': [],
            'bus_interruptions_avg_h': [],
            'bus_interruptions_total_customers': [],
            'bus_outage_customer_accum_duration': [],
            'bus_line_total_miles': [],
            'latitude': [],
            'longitude': [],
        }

        for aux, __ in enumerate(buses["names"]):
            self.dss.circuit_set_active_bus_i(aux)
            buses["base_kv"].append(self.dss.bus_kv_base())
            buses["num_nodes"].append(self.dss.bus_nodes())
            buses["coordinates"].append([self.dss.bus_read_x(), self.dss.bus_read_y()])
            buses["distance"].append(self.dss.bus_distance())
            buses["failure_rate_downstream"].append(self.dss.bus_lambda())
            buses["bus_interruptions"].append(self.dss.bus_interruptions_num())
            buses["bus_interruptions_avg_h"].append(self.dss.bus_interruptions_avg_duration())
            buses["bus_interruptions_total_customers"].append(self.dss.bus_interruptions_total_customers())
            buses["bus_outage_customer_accum_duration"].append(self.dss.bus_outage_customer_accum_duration())
            buses["bus_line_total_miles"].append(self.dss.bus_line_total_miles())
            buses["latitude"].append(self.dss.bus_read_latitude())
            buses["longitude"].append(self.dss.bus_read_longitude())
        return pd.DataFrame.from_dict(buses)

    def get_all_one_phase_buses(self):
        buses = self.get_buses()
        return buses[buses["num_nodes"].str.len() == 1]

    def get_all_two_phases_buses(self):
        buses = self.get_buses()
        return buses[buses["num_nodes"].str.len() == 2]

    def get_all_three_phases_buses(self):
        buses = self.get_buses()
        return buses[buses["num_nodes"].str.len() == 3]

    def exist(self, bus_name):
        """
        :param bus_name:
        :return: True if a Bus existe.
        """
        pass

    def check_violation(self):
        pass
