# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:04:50
 Project: py_dss_tools [set, 2021]
"""
from .PDElement import PDElement


class Reactor(PDElement):
    name = "Reactor"
    name_plural = "Reactors"
    columns = ['basefreq', 'bus1', 'bus2', 'conn', 'emergamps', 'enabled', 'faultrate', 'kv', 'kvar', 'lcurve', 'like',
               'lmh', 'normamps', 'parallel', 'pctperm', 'phases', 'r', 'rcurve', 'repair', 'rmatrix', 'rp', 'x',
               'xmatrix', 'z', 'z0', 'z1', 'z2']

    @property
    def emergamps(self):
        return NotImplementedError

    @property
    def enabled(self):
        return NotImplementedError

    @property
    def faultrate(self):
        return NotImplementedError

    @property
    def like(self):
        return NotImplementedError

    @property
    def normamps(self):
        return NotImplementedError

    @property
    def pctperm(self):
        return NotImplementedError

    @property
    def phases(self):
        return NotImplementedError

    @property
    def repair(self):
        return NotImplementedError

    def __init__(self):
        super().__init__()
