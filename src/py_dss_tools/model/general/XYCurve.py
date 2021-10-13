# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:10:24
 Project: py_dss_tools [set, 2021]
"""


class XYCurve:
    name = "XYCurve"
    name_plural = "XYCurves"
    columns = ['csvfile', 'dblfile', 'like', 'npts', 'points', 'sngfile', 'x', 'xarray', 'xscale', 'xshift', 'y',
               'yarray', 'yscale', 'yshift']

    def __init__(self):
        self.__csvfile = None
        self.__dblfile = None
        self.__npts = None
        self.__points = None
        self.__sngfile = None
        self.__x = None
        self.__xarray = None
        self.__xscale = None
        self.__xshift = None
        self.__y = None
        self.__yarray = None
        self.__yscale = None
        self.__yshift = None

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
    def npts(self):
        return self.__npts

    @npts.setter
    def npts(self, value):
        self.__npts = value

    @property
    def points(self):
        return self.__points

    @points.setter
    def points(self, value):
        self.__points = value

    @property
    def sngfile(self):
        return self.__sngfile

    @sngfile.setter
    def sngfile(self, value):
        self.__sngfile = value

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def xarray(self):
        return self.__xarray

    @xarray.setter
    def xarray(self, value):
        self.__xarray = value

    @property
    def xscale(self):
        return self.__xscale

    @xscale.setter
    def xscale(self, value):
        self.__xscale = value

    @property
    def xshift(self):
        return self.__xshift

    @xshift.setter
    def xshift(self, value):
        self.__xshift = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def yarray(self):
        return self.__yarray

    @yarray.setter
    def yarray(self, value):
        self.__yarray = value

    @property
    def yscale(self):
        return self.__yscale

    @yscale.setter
    def yscale(self, value):
        self.__yscale = value

    @property
    def yshift(self):
        return self.__yshift

    @yshift.setter
    def yshift(self, value):
        self.__yshift = value
