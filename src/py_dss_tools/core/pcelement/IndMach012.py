# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:03:27
 Project: py_dss_tools [set, 2021]
"""
from .PCElement import PCElement


class IndMach012(PCElement):
    name = "IndMach012"
    name_plural = "IndMach012s"
    columns = ['basefreq', 'bus1', 'conn', 'd', 'daily', 'debugtrace', 'duty', 'enabled', 'h', 'kv', 'kva', 'kw',
               'like', 'maxslip', 'pf', 'phases', 'purr', 'purs', 'puxm', 'puxr', 'puxs', 'slip', 'slipoption',
               'spectrum', 'yearly']

    def __init__(self):
        super().__init__()
        self.__conn = None
        self.__d = None
        self.__daily = None
        self.__debugtrace = None
        self.__duty = None
        self.__h = None
        self.__kv = None
        self.__kva = None
        self.__kw = None
        self.__maxslip = None
        self.__pf = None
        self.__purr = None
        self.__purs = None
        self.__puxm = None
        self.__puxr = None
        self.__puxs = None
        self.__slip = None
        self.__slipoption = None
        self.__yearly = None

    @property
    def conn(self):
        return self.__conn

    @conn.setter
    def conn(self, value):
        self.__conn = value

    @property
    def d(self):
        return self.__d

    @d.setter
    def d(self, value):
        self.__d = value

    @property
    def daily(self):
        return self.__daily

    @daily.setter
    def daily(self, value):
        self.__daily = value

    @property
    def debugtrace(self):
        return self.__debugtrace

    @debugtrace.setter
    def debugtrace(self, value):
        self.__debugtrace = value

    @property
    def duty(self):
        return self.__duty

    @duty.setter
    def duty(self, value):
        self.__duty = value

    @property
    def h(self):
        return self.__h

    @h.setter
    def h(self, value):
        self.__h = value

    @property
    def kv(self):
        return self.__kv

    @kv.setter
    def kv(self, value):
        self.__kv = value

    @property
    def kva(self):
        return self.__kva

    @kva.setter
    def kva(self, value):
        self.__kva = value

    @property
    def kw(self):
        return self.__kw

    @kw.setter
    def kw(self, value):
        self.__kw = value

    @property
    def maxslip(self):
        return self.__maxslip

    @maxslip.setter
    def maxslip(self, value):
        self.__maxslip = value

    @property
    def pf(self):
        return self.__pf

    @pf.setter
    def pf(self, value):
        self.__pf = value

    @property
    def purr(self):
        return self.__purr

    @purr.setter
    def purr(self, value):
        self.__purr = value

    @property
    def purs(self):
        return self.__purs

    @purs.setter
    def purs(self, value):
        self.__purs = value

    @property
    def puxm(self):
        return self.__puxm

    @puxm.setter
    def puxm(self, value):
        self.__puxm = value

    @property
    def puxr(self):
        return self.__puxr

    @puxr.setter
    def puxr(self, value):
        self.__puxr = value

    @property
    def puxs(self):
        return self.__puxs

    @puxs.setter
    def puxs(self, value):
        self.__puxs = value

    @property
    def slip(self):
        return self.__slip

    @slip.setter
    def slip(self, value):
        self.__slip = value

    @property
    def slipoption(self):
        return self.__slipoption

    @slipoption.setter
    def slipoption(self, value):
        self.__slipoption = value

    @property
    def yearly(self):
        return self.__yearly

    @yearly.setter
    def yearly(self, value):
        self.__yearly = value
