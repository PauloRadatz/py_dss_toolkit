# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 04/09/2021 at 20:38:16
 Project: py_dss_tools [set, 2021]
"""


class Fuse:
    name = "Fuse"
    name_plural = "Fuses"
    columns = ['action', 'basefreq', 'delay', 'enabled', 'fusecurve', 'like', 'monitoredobj', 'monitoredterm',
               'ratedcurrent', 'switchedobj', 'switchedterm']

    def __init__(self):
        self.__action = None
        self.__delay = None
        self.__fusecurve = None
        self.__monitoredobj = None
        self.__monitoredterm = None
        self.__ratedcurrent = None
        self.__switchedobj = None
        self.__switchedterm = None

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, value):
        self.__action = value

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, value):
        self.__delay = value

    @property
    def fusecurve(self):
        return self.__fusecurve

    @fusecurve.setter
    def fusecurve(self, value):
        self.__fusecurve = value

    @property
    def monitoredobj(self):
        return self.__monitoredobj

    @monitoredobj.setter
    def monitoredobj(self, value):
        self.__monitoredobj = value

    @property
    def monitoredterm(self):
        return self.__monitoredterm

    @monitoredterm.setter
    def monitoredterm(self, value):
        self.__monitoredterm = value

    @property
    def ratedcurrent(self):
        return self.__ratedcurrent

    @ratedcurrent.setter
    def ratedcurrent(self, value):
        self.__ratedcurrent = value

    @property
    def switchedobj(self):
        return self.__switchedobj

    @switchedobj.setter
    def switchedobj(self, value):
        self.__switchedobj = value

    @property
    def switchedterm(self):
        return self.__switchedterm

    @switchedterm.setter
    def switchedterm(self, value):
        self.__switchedterm = value
