# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:11:29
 Project: py_dss_tools [set, 2021]
"""
from .Other import Other


class Fault(Other):
    name = "Fault"
    name_plural = "Faults"
    columns = ['%stddev', 'basefreq', 'bus1', 'bus2', 'emergamps', 'enabled', 'faultrate', 'gmatrix', 'like', 'minamps',
               'normamps', 'ontime', 'pctperm', 'phases', 'r', 'repair', 'temporary']

    def __init__(self):
        super().__init__()
        self.__percent_stddev = None
        self.__bus1 = None
        self.__bus2 = None
        self.__emergamps = None
        self.__faultrate = None
        self.__gmatrix = None
        self.__minamps = None
        self.__normamps = None
        self.__ontime = None
        self.__pctperm = None
        self.__r = None
        self.__repair = None
        self.__temporary = None

    @property
    def percent_stddev(self):
        return self.__percent_stddev

    @percent_stddev.setter
    def percent_stddev(self, value):
        self.__percent_stddev = value

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
    def gmatrix(self):
        return self.__gmatrix

    @gmatrix.setter
    def gmatrix(self, value):
        self.__gmatrix = value

    @property
    def minamps(self):
        return self.__minamps

    @minamps.setter
    def minamps(self, value):
        self.__minamps = value

    @property
    def normamps(self):
        return self.__normamps

    @normamps.setter
    def normamps(self, value):
        self.__normamps = value

    @property
    def ontime(self):
        return self.__ontime

    @ontime.setter
    def ontime(self, value):
        self.__ontime = value

    @property
    def pctperm(self):
        return self.__pctperm

    @pctperm.setter
    def pctperm(self, value):
        self.__pctperm = value

    @property
    def r(self):
        return self.__r

    @r.setter
    def r(self, value):
        self.__r = value

    @property
    def repair(self):
        return self.__repair

    @repair.setter
    def repair(self, value):
        self.__repair = value

    @property
    def temporary(self):
        return self.__temporary

    @temporary.setter
    def temporary(self, value):
        self.__temporary = value
