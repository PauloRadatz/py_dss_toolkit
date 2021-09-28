# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:08:29
 Project: py_dss_tools [set, 2021]
"""


class GrowthShape:
    name = "GrowthShape"
    name_plural = "GrowthShapes"
    columns = ['csvfile', 'dblfile', 'like', 'mult', 'npts', 'sngfile', 'year']

    def __init__(self):
        self.__csvfile = None
        self.__dblfile = None
        self.__mult = None
        self.__npts = None
        self.__sngfile = None
        self.__year = None

    @property
    def csvfile(self):
        return self.__csvfile

    @csvfile.setter
    def csvfile(self, value):
        self.__csvfile = value

    @property
    def dblfile(self):
        return self.__dblfile

    @dblfile.setter
    def dblfile(self, value):
        self.__dblfile = value

    @property
    def mult(self):
        return self.__mult

    @mult.setter
    def mult(self, value):
        self.__mult = value

    @property
    def npts(self):
        return self.__npts

    @npts.setter
    def npts(self, value):
        self.__npts = value

    @property
    def sngfile(self):
        return self.__sngfile

    @sngfile.setter
    def sngfile(self, value):
        self.__sngfile = value

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        self.__year = value
