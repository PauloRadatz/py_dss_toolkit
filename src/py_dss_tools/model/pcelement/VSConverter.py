# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:04:01
 Project: py_dss_tools [set, 2021]
"""
from .PCElement import PCElement


class VSConverter(PCElement):
    name = "VSConverter"
    name_plural = "VSConverterS"
    columns = ['basefreq', 'bus1', 'd0', 'enabled', 'iacmax', 'idcmax', 'kvac', 'kvdc', 'kw', 'like', 'm0', 'mmax',
               'mmin', 'ndc', 'pacref', 'phases', 'qacref', 'rac', 'spectrum', 'vacref', 'vdcref', 'vscmode', 'xac']

    def __init__(self):
        super().__init__()
        self.__d0 = None
        self.__iacmax = None
        self.__idcmax = None
        self.__kvac = None
        self.__kvdc = None
        self.__kw = None
        self.__m0 = None
        self.__mmax = None
        self.__mmin = None
        self.__ndc = None
        self.__pacref = None
        self.__qacref = None
        self.__rac = None
        self.__vacref = None
        self.__vdcref = None
        self.__vscmode = None
        self.__xac = None

    @property
    def d0(self):
        return self.__d0

    @d0.setter
    def d0(self, value):
        self.__d0 = value

    @property
    def iacmax(self):
        return self.__iacmax

    @iacmax.setter
    def iacmax(self, value):
        self.__iacmax = value

    @property
    def idcmax(self):
        return self.__idcmax

    @idcmax.setter
    def idcmax(self, value):
        self.__idcmax = value

    @property
    def kvac(self):
        return self.__kvac

    @kvac.setter
    def kvac(self, value):
        self.__kvac = value

    @property
    def kvdc(self):
        return self.__kvdc

    @kvdc.setter
    def kvdc(self, value):
        self.__kvdc = value

    @property
    def kw(self):
        return self.__kw

    @kw.setter
    def kw(self, value):
        self.__kw = value

    @property
    def m0(self):
        return self.__m0

    @m0.setter
    def m0(self, value):
        self.__m0 = value

    @property
    def mmax(self):
        return self.__mmax

    @mmax.setter
    def mmax(self, value):
        self.__mmax = value

    @property
    def mmin(self):
        return self.__mmin

    @mmin.setter
    def mmin(self, value):
        self.__mmin = value

    @property
    def ndc(self):
        return self.__ndc

    @ndc.setter
    def ndc(self, value):
        self.__ndc = value

    @property
    def pacref(self):
        return self.__pacref

    @pacref.setter
    def pacref(self, value):
        self.__pacref = value

    @property
    def qacref(self):
        return self.__qacref

    @qacref.setter
    def qacref(self, value):
        self.__qacref = value

    @property
    def rac(self):
        return self.__rac

    @rac.setter
    def rac(self, value):
        self.__rac = value

    @property
    def vacref(self):
        return self.__vacref

    @vacref.setter
    def vacref(self, value):
        self.__vacref = value

    @property
    def vdcref(self):
        return self.__vdcref

    @vdcref.setter
    def vdcref(self, value):
        self.__vdcref = value

    @property
    def vscmode(self):
        return self.__vscmode

    @vscmode.setter
    def vscmode(self, value):
        self.__vscmode = value

    @property
    def xac(self):
        return self.__xac

    @xac.setter
    def xac(self, value):
        self.__xac = value
