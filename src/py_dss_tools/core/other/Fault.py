# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:11:29
 Project: py_dss_tools [set, 2021]
"""


class Fault:
    name = "Fault"
    name_plural = "Faults"
    columns = ['%stddev', 'basefreq', 'bus1', 'bus2', 'emergamps', 'enabled', 'faultrate', 'gmatrix', 'like', 'minamps',
               'normamps', 'ontime', 'pctperm', 'phases', 'r', 'repair', 'temporary']

    def __init__(self):
        pass
