# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 03/09/2021 at 17:43:57
 Project: py_dss_tools [set, 2021]
"""


class PVSystem:
    name = "PCSystem"
    name_plural = "PVSystems"
    columns = ['%cutin', '%cutout', '%pminkvarmax', '%pminnovars', '%pmpp', '%r', '%x', 'balanced', 'basefreq', 'bus1',
               'class', 'conn', 'daily', 'debugtrace', 'duty', 'dutystart', 'effcurve', 'enabled', 'irradiance', 'kv',
               'kva', 'kvar', 'kvarmax', 'kvarmaxabs', 'like', 'limitcurrent', 'model', 'pf', 'pfpriority', 'phases',
               'pmpp', 'p-tcurve', 'spectrum', 'tdaily', 'tduty', 'temperature', 'tyearly', 'userdata', 'usermodel',
               'varfollowinverter', 'vmaxpu', 'vminpu', 'wattpriority', 'yearly']

    def __init__(self, dss):
        self.dss = dss

    def get_pv_systems(self, bus_names: list):
        """
        :param bus_names: Buses where GD will be inserted.
        :return:
        """
        pass
