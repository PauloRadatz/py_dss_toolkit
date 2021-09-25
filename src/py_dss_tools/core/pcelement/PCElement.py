# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 24/09/2021 at 23:00:35
 Project: py_dss_tools [set, 2021]
"""


class PCElement:
    def __init__(self):
        self.__basefreq = None
        self.__bus1 = None
        self.__enabled = None
        self.__like = None
        self.__phases = None
        self.__spectrum = None

    @property
    def basefreq(self):
        return self.__basefreq

    @basefreq.setter
    def basefreq(self, value):
        self.__basefreq = value

    @property
    def bus1(self):
        return self.__bus1

    @bus1.setter
    def bus1(self, value):
        self.__bus1 = value

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, value):
        self.__enabled = value

    @property
    def like(self):
        return self.__like

    @like.setter
    def like(self, value):
        self.__like = value

    @property
    def phases(self):
        return self.__phases

    @phases.setter
    def phases(self, value):
        self.__phases = value

    @property
    def spectrum(self):
        return self.__spectrum

    @spectrum.setter
    def spectrum(self, value):
        self.__spectrum = value


