# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:03:49
 Project: py_dss_tools [set, 2021]
"""
from .PCElement import PCElement


class UPFC(PCElement):
    name = "UPFC"
    name_plural = "UPFCs"
    columns = ['basefreq', 'bus1', 'bus2', 'climit', 'enabled', 'frequency', 'kvarlimit', 'like', 'losscurve', 'mode',
               'pf', 'phases', 'refkv', 'refkv2', 'spectrum', 'tol1', 'vhlimit', 'vllimit', 'vpqmax', 'xs']

    def __init__(self):
        super().__init__()
        self.__bus2 = None
        self.__climit = None
        self.__frequency = None
        self.__kvarlimit = None
        self.__losscurve = None
        self.__mode = None
        self.__pf = None
        self.__refkv = None
        self.__refkv2 = None
        self.__tol1 = None
        self.__vhlimit = None
        self.__vllimit = None
        self.__vpqmax = None
        self.__xs = None

    @property
    def bus2(self):
        return self.__bus2

    @bus2.setter
    def bus2(self, value):
        self.__bus2 = value

    @property
    def climit(self):
        return self.__climit

    @climit.setter
    def climit(self, value):
        self.__climit = value

    @property
    def frequency(self):
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
        self.__frequency = value

    @property
    def kvarlimit(self):
        return self.__kvarlimit

    @kvarlimit.setter
    def kvarlimit(self, value):
        self.__kvarlimit = value

    @property
    def losscurve(self):
        return self.__losscurve

    @losscurve.setter
    def losscurve(self, value):
        self.__losscurve = value

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        self.__mode = value

    @property
    def pf(self):
        return self.__pf

    @pf.setter
    def pf(self, value):
        self.__pf = value

    @property
    def refkv(self):
        return self.__refkv

    @refkv.setter
    def refkv(self, value):
        self.__refkv = value

    @property
    def refkv2(self):
        return self.__refkv2

    @refkv2.setter
    def refkv2(self, value):
        self.__refkv2 = value

    @property
    def tol1(self):
        return self.__tol1

    @tol1.setter
    def tol1(self, value):
        self.__tol1 = value

    @property
    def vhlimit(self):
        return self.__vhlimit

    @vhlimit.setter
    def vhlimit(self, value):
        self.__vhlimit = value

    @property
    def vllimit(self):
        return self.__vllimit

    @vllimit.setter
    def vllimit(self, value):
        self.__vllimit = value

    @property
    def vpqmax(self):
        return self.__vpqmax

    @vpqmax.setter
    def vpqmax(self, value):
        self.__vpqmax = value

    @property
    def xs(self):
        return self.__xs

    @xs.setter
    def xs(self, value):
        self.__xs = value
