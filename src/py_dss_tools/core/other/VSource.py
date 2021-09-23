# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:11:52
 Project: py_dss_tools [set, 2021]
"""


class VSource:
    name = "VSource"
    name_plural = "VSources"
    columns = ['angle', 'basefreq', 'basekv', 'basemva', 'bus1', 'bus2', 'daily', 'duty', 'enabled', 'frequency',
               'isc1', 'isc3', 'like', 'model', 'mvasc1', 'mvasc3', 'phases', 'pu', 'puz0', 'puz1', 'puz2', 'puzideal',
               'r0', 'r1', 'scantype', 'sequence', 'spectrum', 'x0', 'x0r0', 'x1', 'x1r1', 'yearly', 'z0', 'z1', 'z2']

    def __init__(self, basekv="115", name="MY_Vsource"):
        self.angle = '0'
        self.basekv = basekv
        self.basefreq = '60'
        self.basemva = '100'
        self.bus1 = 'sourcebus'
        self.bus2 = 'sourcebus.0.0.0'
        self.daily = ''
        self.duty = ''
        self.enabled = 'true'
        self.frequency = '60'
        self.isc1 = ''
        self.isc3 = ''
        self.like = ''
        self.model = 'Thevenin'
        self.mvasc1 = '21000'
        self.mvasc3 = '20000'
        self.name = name
        self.phases = '3'
        self.pu = '1.0001'
        self.puz0 = ''
        self.puz1 = ''
        self.puz2 = ''
        self.puzideal = ''
        self.r0 = ''
        self.r1 = ''
        self.scantype = 'Pos'
        self.sequence = 'Pos'
        self.spectrum = 'defaultvsource'
        self.x0 = ''
        self.x0r0 = ''
        self.x1 = ''
        self.x1r1 = ''
        self.yearly = ''
        self.z0 = ''
        self.z1 = ''
        self.z2 = ''
