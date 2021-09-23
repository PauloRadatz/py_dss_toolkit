# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:05:36
 Project: py_dss_tools [set, 2021]
"""


class ExpControl:
    name = "ExpControl"
    name_plural = "ExpControls"
    columns = ['basefreq', 'deltaq_factor', 'enabled', 'eventlog', 'like', 'preferq', 'pvsystemlist', 'qbias',
               'qmaxlag', 'qmaxlead', 'slope', 'tresponse', 'vreg', 'vregmax', 'vregmin', 'vregtau']

    def __init__(self):
        pass
