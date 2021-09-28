# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:08:48
 Project: py_dss_tools [set, 2021]
"""


class LineCode:
    name = "LineCode"
    name_plural = "LineCodes"
    columns = ['b0', 'b1', 'basefreq', 'c0', 'c1', 'cmatrix', 'emergamps', 'faultrate', 'kron', 'like', 'linetype',
               'neutral', 'normamps', 'nphases', 'pctperm', 'r0', 'r1', 'ratings', 'repair', 'rg', 'rho', 'rmatrix',
               'seasons', 'units', 'x0', 'x1', 'xg', 'xmatrix']

    def __init__(self):
        self.__b0 = None
        self.__b1 = None
        self.__basefreq = None
        self.__c0 = None
        self.__c1 = None
        self.__cmatrix = None
        self.__emergamps = None
        self.__faultrate = None
        self.__kron = None
        self.__linetype = None
        self.__neutral = None
        self.__normamps = None
        self.__nphases = None
        self.__pctperm = None
        self.__r0 = None
        self.__r1 = None
        self.__ratings = None
        self.__repair = None
        self.__rg = None
        self.__rho = None
        self.__rmatrix = None
        self.__seasons = None
        self.__units = None
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
    def basefreq(self):
        return self.__basefreq

    @basefreq.setter
    def basefreq(self, value):
        self.__basefreq = value

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
    def emergamps(self):
        return self.__emergamps

    @emergamps.setter
    def emergamps(self, value):
        self.__emergamps = value

    @property
    def faultrate(self):
        return self.__faultrate

    @faultrate.setter
    def faultrate(self, value):
        self.__faultrate = value

    @property
    def kron(self):
        return self.__kron

    @kron.setter
    def kron(self, value):
        self.__kron = value

    @property
    def linetype(self):
        return self.__linetype

    @linetype.setter
    def linetype(self, value):
        self.__linetype = value

    @property
    def neutral(self):
        return self.__neutral

    @neutral.setter
    def neutral(self, value):
        self.__neutral = value

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
    def pctperm(self):
        return self.__pctperm

    @pctperm.setter
    def pctperm(self, value):
        self.__pctperm = value

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
    def repair(self):
        return self.__repair

    @repair.setter
    def repair(self, value):
        self.__repair = value

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
    def units(self):
        return self.__units

    @units.setter
    def units(self, value):
        self.__units = value

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
