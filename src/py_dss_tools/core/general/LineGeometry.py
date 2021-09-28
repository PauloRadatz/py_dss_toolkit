# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:09:05
 Project: py_dss_tools [set, 2021]
"""


class LineGeometry:
    name = "LineGeometry"
    name_plural = "LineGeometries"
    columns = ['cncable', 'cncables', 'cond', 'emergamps', 'h', 'like', 'linetype', 'nconds', 'normamps', 'nphases',
               'ratings', 'reduce', 'seasons', 'spacing', 'tscable', 'tscables', 'units', 'wire', 'wires', 'x']

    def __init__(self):
        self.__cncable = None
        self.__cncables = None
        self.__cond = None
        self.__emergamps = None
        self.__h = None
        self.__linetype = None
        self.__nconds = None
        self.__normamps = None
        self.__nphases = None
        self.__ratings = None
        self.__reduce = None
        self.__seasons = None
        self.__spacing = None
        self.__tscable = None
        self.__tscables = None
        self.__units = None
        self.__wire = None
        self.__wires = None
        self.__x = None

    @property
    def cncable(self):
        return self.__cncable

    @cncable.setter
    def cncable(self, value):
        self.__cncable = value

    @property
    def cncables(self):
        return self.__cncables

    @cncables.setter
    def cncables(self, value):
        self.__cncables = value

    @property
    def cond(self):
        return self.__cond

    @cond.setter
    def cond(self, value):
        self.__cond = value

    @property
    def emergamps(self):
        return self.__emergamps

    @emergamps.setter
    def emergamps(self, value):
        self.__emergamps = value

    @property
    def h(self):
        return self.__h

    @h.setter
    def h(self, value):
        self.__h = value

    @property
    def linetype(self):
        return self.__linetype

    @linetype.setter
    def linetype(self, value):
        self.__linetype = value

    @property
    def nconds(self):
        return self.__nconds

    @nconds.setter
    def nconds(self, value):
        self.__nconds = value

    @property
    def normamps(self):
        return self.__normamps

    @normamps.setter
    def normamps(self, value):
        self.__normamps = value

    @property
    def nphases(self):
        return self.__nphases

    @nphases.setter
    def nphases(self, value):
        self.__nphases = value

    @property
    def ratings(self):
        return self.__ratings

    @ratings.setter
    def ratings(self, value):
        self.__ratings = value

    @property
    def reduce(self):
        return self.__reduce

    @reduce.setter
    def reduce(self, value):
        self.__reduce = value

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
    def tscable(self):
        return self.__tscable

    @tscable.setter
    def tscable(self, value):
        self.__tscable = value

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
    def wire(self):
        return self.__wire

    @wire.setter
    def wire(self, value):
        self.__wire = value

    @property
    def wires(self):
        return self.__wires

    @wires.setter
    def wires(self, value):
        self.__wires = value

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value
