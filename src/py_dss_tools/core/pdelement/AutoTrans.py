# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:04:23
 Project: py_dss_tools [set, 2021]
"""


class AutoTrans:
    name = "AutoTrans"
    name_plural = "AutoTrans"
    columns = ['%imag', '%loadloss', '%noloadloss', '%r', '%rs', 'bank', 'basefreq', 'bus', 'buses', 'conn', 'conns',
               'core', 'emergamps', 'emerghkva', 'enabled', 'faultrate', 'flrise', 'hsrise', 'kv', 'kva', 'kvas', 'kvs',
               'leadlag', 'like', 'm', 'maxtap', 'mintap', 'n', 'normamps', 'normhkva', 'numtaps', 'pctperm', 'phases',
               'ppm_antifloat', 'rdcohms', 'repair', 'sub', 'subname', 'tap', 'taps', 'thermal', 'wdg', 'wdgcurrents',
               'windings', 'xfmrcode', 'xht', 'xhx', 'xrconst', 'xscarray', 'xxt']

    def __init__(self, dss):
        self.dss = dss
