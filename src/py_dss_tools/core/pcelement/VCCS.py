# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:03:55
 Project: py_dss_tools [set, 2021]
"""
from .PCElement import PCElement


class VCCS(PCElement):
    name = "VCCS"
    name_plural = "VCCSs"
    columns = ['basefreq', 'bp1', 'bp2', 'bus1', 'enabled', 'filter', 'fsample', 'imaxpu', 'irmstau', 'like', 'phases',
               'ppct', 'prated', 'rmsmode', 'spectrum', 'vrated', 'vrmstau']

    def __init__(self):
        super().__init__()
        self.__bp1 = None
        self.__bp2 = None
        self.__filter = None
        self.__fsample = None
        self.__imaxpu = None
        self.__irmstau = None
        self.__ppct = None
        self.__prated = None
        self.__rmsmode = None
        self.__vrated = None
        self.__vrmstau = None

    @property
    def bp1(self):
        return self.__bp1

    @bp1.setter
    def bp1(self, value):
        self.__bp1 = value

    @property
    def bp2(self):
        return self.__bp2

    @bp2.setter
    def bp2(self, value):
        self.__bp2 = value

    @property
    def filter(self):
        return self.__filter

    @filter.setter
    def filter(self, value):
        self.__filter = value

    @property
    def fsample(self):
        return self.__fsample

    @fsample.setter
    def fsample(self, value):
        self.__fsample = value

    @property
    def imaxpu(self):
        return self.__imaxpu

    @imaxpu.setter
    def imaxpu(self, value):
        self.__imaxpu = value

    @property
    def irmstau(self):
        return self.__irmstau

    @irmstau.setter
    def irmstau(self, value):
        self.__irmstau = value

    @property
    def ppct(self):
        return self.__ppct

    @ppct.setter
    def ppct(self, value):
        self.__ppct = value

    @property
    def prated(self):
        return self.__prated

    @prated.setter
    def prated(self, value):
        self.__prated = value

    @property
    def rmsmode(self):
        return self.__rmsmode

    @rmsmode.setter
    def rmsmode(self, value):
        self.__rmsmode = value

    @property
    def vrated(self):
        return self.__vrated

    @vrated.setter
    def vrated(self, value):
        self.__vrated = value

    @property
    def vrmstau(self):
        return self.__vrmstau

    @vrmstau.setter
    def vrmstau(self, value):
        self.__vrmstau = value
