# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 04/09/2021 at 20:39:19
 Project: py_dss_tools [set, 2021]
"""


class Load:
    name = "Load"
    name_plural = "Loads"
    columns = ['%mean', '%seriesrl', '%stddev', 'allocationfactor', 'basefreq', 'bus1', 'cfactor', 'class', 'conn',
               'cvrcurve', 'cvrvars', 'cvrwatts', 'daily', 'duty', 'enabled', 'growth', 'kv', 'kva', 'kvar', 'kw',
               'kwh', 'kwhdays', 'like', 'model', 'numcust', 'pf', 'phases', 'puxharm', 'relweight', 'rneut',
               'spectrum', 'status', 'vlowpu', 'vmaxpu', 'vminemerg', 'vminnorm', 'vminpu', 'xfkva', 'xneut', 'xrharm',
               'yearly', 'zipv']

    def __init__(self):
        pass
