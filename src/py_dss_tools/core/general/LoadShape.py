# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 04/09/2021 at 20:39:34
 Project: py_dss_tools [set, 2021]
"""


class LoadShape:
    name = "LoadShape"
    name_plural = "LoadShapes"
    columns = ['action', 'csvfile', 'dblfile', 'hour', 'interval', 'like', 'mean', 'minterval', 'mult', 'npts', 'pbase',
               'pmax', 'pmult', 'pqcsvfile', 'qbase', 'qmax', 'qmult', 'sinterval', 'sngfile', 'stddev', 'useactual']

    def __init__(self):
        self.__action = None
        self.__csvfile = None
        self.__dblfile = None
        self.__hour = None
        self.__interval = None
        self.__mean = None
        self.__minterval = None
        self.__mult = None
        self.__npts = None
        self.__pbase = None
        self.__pmax = None
        self.__pmult = None
        self.__pqcsvfile = None
        self.__qbase = None
        self.__qmax = None
        self.__qmult = None
        self.__sinterval = None
        self.__sngfile = None
        self.__stddev = None
        self.__useactual = None

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
    def pbase(self):
        return self.__pbase

    @pbase.setter
    def pbase(self, value):
        self.__pbase = value

    @property
    def pmax(self):
        return self.__pmax

    @pmax.setter
    def pmax(self, value):
        self.__pmax = value

    @property
    def pmult(self):
        return self.__pmult

    @pmult.setter
    def pmult(self, value):
        self.__pmult = value

    @property
    def pqcsvfile(self):
        return self.__pqcsvfile

    @pqcsvfile.setter
    def pqcsvfile(self, value):
        self.__pqcsvfile = value

    @property
    def qbase(self):
        return self.__qbase

    @qbase.setter
    def qbase(self, value):
        self.__qbase = value

    @property
    def qmax(self):
        return self.__qmax

    @qmax.setter
    def qmax(self, value):
        self.__qmax = value

    @property
    def qmult(self):
        return self.__qmult

    @qmult.setter
    def qmult(self, value):
        self.__qmult = value

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
    def useactual(self):
        return self.__useactual

    @useactual.setter
    def useactual(self, value):
        self.__useactual = value
