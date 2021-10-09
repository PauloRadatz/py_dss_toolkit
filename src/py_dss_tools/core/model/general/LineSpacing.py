# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:09:12
 Project: py_dss_tools [set, 2021]
"""


class LineSpacing:
    name = "LineSpacing"
    name_plural = "LineSpacings"
    columns = ['h', 'like', 'nconds', 'nphases', 'units', 'x']

    def __init__(self):
        self.__h = None
        self.__nconds = None
        self.__nphases = None
        self.__units = None
        self.__x = None

    @property
    def h(self):
        return self.__h

    @h.setter
    def h(self, value):
        self.__h = value

    @property
    def nconds(self):
        return self.__nconds

    @nconds.setter
    def nconds(self, value):
        self.__nconds = value

    @property
    def nphases(self):
        return self.__nphases

    @nphases.setter
    def nphases(self, value):
        self.__nphases = value

    @property
    def units(self):
        return self.__units

    @units.setter
    def units(self, value):
        self.__units = value

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value
