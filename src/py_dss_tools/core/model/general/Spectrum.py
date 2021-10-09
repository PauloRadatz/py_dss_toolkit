# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:09:38
 Project: py_dss_tools [set, 2021]
"""


class Spectrum:
    name = "Spectrum"
    name_plural = "Spectrums"
    columns = ['%mag', 'angle', 'csvfile', 'harmonic', 'like', 'numharm']

    def __init__(self):
        self.__percent_mag = None
        self.__angle = None
        self.__csvfile = None
        self.__harmonic = None
        self.__numharm = None

    @property
    def percent_mag(self):
        return self.__percent_mag

    @percent_mag.setter
    def percent_mag(self, value):
        self.__percent_mag = value

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, value):
        self.__angle = value

    @property
    def csvfile(self):
        return self.__csvfile

    @csvfile.setter
    def csvfile(self, value):
        self.__csvfile = value

    @property
    def harmonic(self):
        return self.__harmonic

    @harmonic.setter
    def harmonic(self, value):
        self.__harmonic = value

    @property
    def numharm(self):
        return self.__numharm

    @numharm.setter
    def numharm(self, value):
        self.__numharm = value
