# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:09:58
 Project: py_dss_tools [set, 2021]
"""


class TShape:
    name = "TShape"
    name_plural = "TShapes"
    columns = ['action', 'csvfile', 'dblfile', 'hour', 'interval', 'like', 'mean', 'minterval', 'npts', 'sinterval',
               'sngfile', 'stddev', 'temp']

    def __init__(self):
        self.__action = None
        self.__csvfile = None
        self.__dblfile = None
        self.__hour = None
        self.__interval = None
        self.__mean = None
        self.__minterval = None
        self.__npts = None
        self.__sinterval = None
        self.__sngfile = None
        self.__stddev = None
        self.__temp = None

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, value):
        self.__action = value

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
    def hour(self):
        return self.__hour

    @hour.setter
    def hour(self, value):
        self.__hour = value

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, value):
        self.__interval = value

    @property
    def mean(self):
        return self.__mean

    @mean.setter
    def mean(self, value):
        self.__mean = value

    @property
    def minterval(self):
        return self.__minterval

    @minterval.setter
    def minterval(self, value):
        self.__minterval = value

    @property
    def npts(self):
        return self.__npts

    @npts.setter
    def npts(self, value):
        self.__npts = value

    @property
    def sinterval(self):
        return self.__sinterval

    @sinterval.setter
    def sinterval(self, value):
        self.__sinterval = value

    @property
    def sngfile(self):
        return self.__sngfile

    @sngfile.setter
    def sngfile(self, value):
        self.__sngfile = value

    @property
    def stddev(self):
        return self.__stddev

    @stddev.setter
    def stddev(self, value):
        self.__stddev = value

    @property
    def temp(self):
        return self.__temp

    @temp.setter
    def temp(self, value):
        self.__temp = value
