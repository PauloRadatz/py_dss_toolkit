# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:11:45
 Project: py_dss_tools [set, 2021]
"""
from .OtherElement import OtherElement


class ISource(OtherElement):
    name = "ISource"
    name_plural = "ISources"
    columns = ['amps', 'angle', 'basefreq', 'bus1', 'bus2', 'daily', 'duty', 'enabled', 'frequency', 'like', 'phases',
               'scantype', 'sequence', 'spectrum', 'yearly']

    def __init__(self):
        super().__init__()
        self.__amps = None
        self.__angle = None
        self.__bus1 = None
        self.__bus2 = None
        self.__daily = None
        self.__duty = None
        self.__frequency = None
        self.__scantype = None
        self.__sequence = None
        self.__spectrum = None
        self.__yearly = None

    @property
    def amps(self):
        return self.__amps

    @amps.setter
    def amps(self, value):
        self.__amps = value

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, value):
        self.__angle = value

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
    def daily(self):
        return self.__daily

    @daily.setter
    def daily(self, value):
        self.__daily = value

    @property
    def duty(self):
        return self.__duty

    @duty.setter
    def duty(self, value):
        self.__duty = value

    @property
    def frequency(self):
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
        self.__frequency = value

    @property
    def scantype(self):
        return self.__scantype

    @scantype.setter
    def scantype(self, value):
        self.__scantype = value

    @property
    def sequence(self):
        return self.__sequence

    @sequence.setter
    def sequence(self, value):
        self.__sequence = value

    @property
    def spectrum(self):
        return self.__spectrum

    @spectrum.setter
    def spectrum(self, value):
        self.__spectrum = value

    @property
    def yearly(self):
        return self.__yearly

    @yearly.setter
    def yearly(self, value):
        self.__yearly = value
