# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:11:45
 Project: py_dss_tools [set, 2021]
"""


class ISource:
    name = "ISource"
    name_plural = "ISources"
    columns = ['amps', 'angle', 'basefreq', 'bus1', 'bus2', 'daily', 'duty', 'enabled', 'frequency', 'like', 'phases',
               'scantype', 'sequence', 'spectrum', 'yearly']

    def __init__(self):
        pass
