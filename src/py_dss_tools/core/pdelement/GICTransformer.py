# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 22:44:49
 Project: py_dss_tools [set, 2021]
"""


class GICTransformer:
    name = "GICTransformer"
    name_plural = "GICTransformers"
    columns = ['%r1', '%r2', 'basefreq', 'bush', 'busnh', 'busnx', 'busx', 'emergamps', 'enabled', 'faultrate',
               'k', 'kvll1', 'kvll2', 'like', 'mva', 'normamps', 'pctperm', 'phases', 'r1', 'r2', 'repair',
               'type', 'varcurve']

    def __init__(self, dss):
        self.dss = dss
