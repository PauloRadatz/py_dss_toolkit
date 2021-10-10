# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:11:12
 Project: py_dss_tools [set, 2021]
"""


class Sensor:
    name = "Sensor"
    name_plural = "Sensors"
    columns = ['%error', 'action', 'basefreq', 'clear', 'conn', 'currents', 'deltadirection', 'element', 'enabled',
               'kvars', 'kvbase', 'kvs', 'kws', 'like', 'terminal', 'weight']

    def __init__(self):
        self.__percent_error = None
        self.__clear = None
        self.__conn = None
        self.__currents = None
        self.__deltadirection = None
        self.__kvars = None
        self.__kvbase = None
        self.__kvs = None
        self.__kws = None
        self.__weight = None

    @property
    def percent_error(self):
        return self.__percent_error

    @percent_error.setter
    def percent_error(self, value):
        self.__percent_error = value

    @property
    def clear(self):
        return self.__clear

    @clear.setter
    def clear(self, value):
        self.__clear = value

    @property
    def conn(self):
        return self.__conn

    @conn.setter
    def conn(self, value):
        self.__conn = value

    @property
    def currents(self):
        return self.__currents

    @currents.setter
    def currents(self, value):
        self.__currents = value

    @property
    def deltadirection(self):
        return self.__deltadirection

    @deltadirection.setter
    def deltadirection(self, value):
        self.__deltadirection = value

    @property
    def kvars(self):
        return self.__kvars

    @kvars.setter
    def kvars(self, value):
        self.__kvars = value

    @property
    def kvbase(self):
        return self.__kvbase

    @kvbase.setter
    def kvbase(self, value):
        self.__kvbase = value

    @property
    def kvs(self):
        return self.__kvs

    @kvs.setter
    def kvs(self, value):
        self.__kvs = value

    @property
    def kws(self):
        return self.__kws

    @kws.setter
    def kws(self, value):
        self.__kws = value

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        self.__weight = value
