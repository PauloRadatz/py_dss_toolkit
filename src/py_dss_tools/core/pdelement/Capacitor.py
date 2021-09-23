# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 22:36:39
 Project: py_dss_tools [set, 2021]
"""


class Capacitor:

    name = "Capacitor"
    name_plural = "Capacitors"
    columns = ['basefreq', 'bus1', 'bus2', 'cmatrix', 'conn', 'cuf', 'emergamps', 'enabled', 'faultrate', 'harm',
               'kv', 'kvar', 'like', 'normamps', 'numsteps', 'pctperm', 'phases', 'r', 'repair', 'states', 'xl']

    def __init__(self, dss):
        self.dss = dss
