# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:03:15
 Project: py_dss_tools [set, 2021]
"""
from .PCElement import PCElement


class GICLine(PCElement):
    name = "GICLine"
    name_plural = "GICLines"
    columns = ['angle', 'basefreq', 'bus1', 'bus2', 'c', 'ee', 'en', 'enabled', 'frequency', 'lat1', 'lat2', 'like',
               'lon1', 'lon2', 'phases', 'r', 'spectrum', 'volts', 'x']

    def __init__(self):
        super().__init__()
        self.__angle = None
        self.__bus2 = None
        self.__c = None
        self.__ee = None
        self.__en = None
        self.__frequency = None
        self.__lat1 = None
        self.__lat2 = None
        self.__lon1 = None
        self.__lon2 = None
        self.__r = None
        self.__volts = None
        self.__x = None

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, value):
        self.__angle = value

    @property
    def bus2(self):
        return self.__bus2

    @bus2.setter
    def bus2(self, value):
        self.__bus2 = value

    @property
    def c(self):
        return self.__c

    @c.setter
    def c(self, value):
        self.__c = value

    @property
    def ee(self):
        return self.__ee

    @ee.setter
    def ee(self, value):
        self.__ee = value

    @property
    def en(self):
        return self.__en

    @en.setter
    def en(self, value):
        self.__en = value

    @property
    def frequency(self):
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
        self.__frequency = value

    @property
    def lat1(self):
        return self.__lat1

    @lat1.setter
    def lat1(self, value):
        self.__lat1 = value

    @property
    def lat2(self):
        return self.__lat2

    @lat2.setter
    def lat2(self, value):
        self.__lat2 = value

    @property
    def lon1(self):
        return self.__lon1

    @lon1.setter
    def lon1(self, value):
        self.__lon1 = value

    @property
    def lon2(self):
        return self.__lon2

    @lon2.setter
    def lon2(self, value):
        self.__lon2 = value

    @property
    def r(self):
        return self.__r

    @r.setter
    def r(self, value):
        self.__r = value

    @property
    def volts(self):
        return self.__volts

    @volts.setter
    def volts(self, value):
        self.__volts = value

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value
