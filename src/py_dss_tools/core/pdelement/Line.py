# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 04/09/2021 at 20:39:04
 Project: py_dss_tools [set, 2021]
"""
from .PDElement import PDElement


class Line(PDElement):
    name = "Line"
    name_plural = "Lines"
    columns = ['b0', 'b1', 'basefreq', 'bus1', 'bus2', 'c0', 'c1', 'cmatrix', 'cncables', 'earthmodel', 'emergamps',
               'enabled', 'faultrate', 'geometry', 'length', 'like', 'linecode', 'linetype', 'name', 'normamps',
               'pctperm', 'phases', 'r0', 'r1', 'ratings', 'repair', 'rg', 'rho', 'rmatrix', 'seasons', 'spacing',
               'switch', 'tscables', 'units', 'wires', 'x0', 'x1', 'xg', 'xmatrix']

    def __init__(self):
        super().__init__()
        self.__b0 = None
        self.__b1 = None
        self.__bus1 = None
        self.__bus2 = None
        self.__c0 = None
        self.__c1 = None
        self.__cmatrix = None
        self.__cncables = None
        self.__earthmodel = None
        self.__geometry = None
        self.__length = None
        self.__linecode = None
        self.__linetype = None
        self.__name = None
        self.__r0 = None
        self.__r1 = None
        self.__ratings = None
        self.__rg = None
        self.__rho = None
        self.__rmatrix = None
        self.__seasons = None
        self.__spacing = None
        self.__switch = None
        self.__tscables = None
        self.__units = None
        self.__wires = None
        self.__x0 = None
        self.__x1 = None
        self.__xg = None
        self.__xmatrix = None

    @property
    def b0(self):
        return self.__b0

    @b0.setter
    def b0(self, value):
        self.__b0 = value

    @property
    def b1(self):
        return self.__b1

    @b1.setter
    def b1(self, value):
        self.__b1 = value

    @property
    def bus1(self):
        return self.__bus1

    @bus1.setter
    def bus1(self, value):
        self.__bus1 = value

    @property
    def bus2(self):
        return self.__bus2

    @bus2.setter
    def bus2(self, value):
        self.__bus2 = value

    @property
    def c0(self):
        return self.__c0

    @c0.setter
    def c0(self, value):
        self.__c0 = value

    @property
    def c1(self):
        return self.__c1

    @c1.setter
    def c1(self, value):
        self.__c1 = value

    @property
    def cmatrix(self):
        return self.__cmatrix

    @cmatrix.setter
    def cmatrix(self, value):
        self.__cmatrix = value

    @property
    def cncables(self):
        return self.__cncables

    @cncables.setter
    def cncables(self, value):
        self.__cncables = value

    @property
    def earthmodel(self):
        return self.__earthmodel

    @earthmodel.setter
    def earthmodel(self, value):
        self.__earthmodel = value

    @property
    def geometry(self):
        return self.__geometry

    @geometry.setter
    def geometry(self, value):
        self.__geometry = value

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, value):
        self.__length = value

    @property
    def linecode(self):
        return self.__linecode

    @linecode.setter
    def linecode(self, value):
        self.__linecode = value

    @property
    def linetype(self):
        return self.__linetype

    @linetype.setter
    def linetype(self, value):
        self.__linetype = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def r0(self):
        return self.__r0

    @r0.setter
    def r0(self, value):
        self.__r0 = value

    @property
    def r1(self):
        return self.__r1

    @r1.setter
    def r1(self, value):
        self.__r1 = value

    @property
    def ratings(self):
        return self.__ratings

    @ratings.setter
    def ratings(self, value):
        self.__ratings = value

    @property
    def rg(self):
        return self.__rg

    @rg.setter
    def rg(self, value):
        self.__rg = value

    @property
    def rho(self):
        return self.__rho

    @rho.setter
    def rho(self, value):
        self.__rho = value

    @property
    def rmatrix(self):
        return self.__rmatrix

    @rmatrix.setter
    def rmatrix(self, value):
        self.__rmatrix = value

    @property
    def seasons(self):
        return self.__seasons

    @seasons.setter
    def seasons(self, value):
        self.__seasons = value

    @property
    def spacing(self):
        return self.__spacing

    @spacing.setter
    def spacing(self, value):
        self.__spacing = value

    @property
    def switch(self):
        return self.__switch

    @switch.setter
    def switch(self, value):
        self.__switch = value

    @property
    def tscables(self):
        return self.__tscables

    @tscables.setter
    def tscables(self, value):
        self.__tscables = value

    @property
    def units(self):
        return self.__units

    @units.setter
    def units(self, value):
        self.__units = value

    @property
    def wires(self):
        return self.__wires

    @wires.setter
    def wires(self, value):
        self.__wires = value

    @property
    def x0(self):
        return self.__x0

    @x0.setter
    def x0(self, value):
        self.__x0 = value

    @property
    def x1(self):
        return self.__x1

    @x1.setter
    def x1(self, value):
        self.__x1 = value

    @property
    def xg(self):
        return self.__xg

    @xg.setter
    def xg(self, value):
        self.__xg = value

    @property
    def xmatrix(self):
        return self.__xmatrix

    @xmatrix.setter
    def xmatrix(self, value):
        self.__xmatrix = value
