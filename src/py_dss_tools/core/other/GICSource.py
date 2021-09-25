# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:11:36
 Project: py_dss_tools [set, 2021]
"""
from .OtherElement import Other

class GICSource(Other):
    name = "GICSource"
    name_plural = "GICSources"
    columns = ['angle', 'basefreq', 'ee', 'en', 'enabled', 'frequency', 'lat1', 'lat2', 'like', 'lon1', 'lon2',
               'phases', 'spectrum', 'volts']

    def __init__(self):
        super().__init__()
        self.__angle = None
        self.__ee = None
        self.__en = None
        self.__frequency = None
        self.__lat1 = None
        self.__lat2 = None
        self.__lon1 = None
        self.__lon2 = None
        self.__spectrum = None
        self.__volts = None

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, value):
        self.__angle = value

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
    def spectrum(self):
        return self.__spectrum

    @spectrum.setter
    def spectrum(self, value):
        self.__spectrum = value

    @property
    def volts(self):
        return self.__volts

    @volts.setter
    def volts(self, value):
        self.__volts = value
