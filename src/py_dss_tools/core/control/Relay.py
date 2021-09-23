# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:06:39
 Project: py_dss_tools [set, 2021]
"""


class Relay:
    name = "Relay"
    name_plural = "Relays"
    columns = ['46%pickup', '46baseamps', '46isqt', '47%pickup', 'action', 'basefreq', 'breakertime', 'delay',
               'enabled', 'groundcurve', 'groundinst', 'groundtrip', 'kvbase', 'like', 'monitoredobj', 'monitoredterm',
               'overtrip', 'overvoltcurve', 'phasecurve', 'phaseinst', 'phasetrip', 'recloseintervals', 'reset',
               'shots', 'switchedobj', 'switchedterm', 'tdground', 'tdphase', 'type', 'undertrip', 'undervoltcurve',
               'variable']

    def __init__(self):
        pass
