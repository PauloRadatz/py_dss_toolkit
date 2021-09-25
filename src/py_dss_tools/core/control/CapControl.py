# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:05:17
 Project: py_dss_tools [set, 2021]
"""


class CapControl:
    name = "CapControl"
    name_plural = "CapControls"
    columns = ['basefreq', 'capacitor', 'ctphase', 'ctratio', 'deadtime', 'delay', 'delayoff', 'element', 'enabled',
               'eventlog', 'like', 'offsetting', 'onsetting', 'pctminkvar', 'ptphase', 'ptratio', 'reset', 'terminal',
               'type', 'userdata', 'usermodel', 'vbus', 'vmax', 'vmin', 'voltoverride']

    def __init__(self):
        self.__capacitor = None
        self.__ctphase = None
        self.__ctratio = None
        self.__deadtime = None
        self.__delay = None
        self.__delayoff = None
        self.__element = None
        self.__eventlog = None
        self.__offsetting = None
        self.__onsetting = None
        self.__pctminkvar = None
        self.__ptphase = None
        self.__ptratio = None
        self.__reset = None
        self.__terminal = None
        self.__type = None
        self.__userdata = None
        self.__usermodel = None
        self.__vbus = None
        self.__vmax = None
        self.__vmin = None
        self.__voltoverride = None

    @property
    def capacitor(self):
        return self.__capacitor

    @capacitor.setter
    def capacitor(self, value):
        self.__capacitor = value

    @property
    def ctphase(self):
        return self.__ctphase

    @ctphase.setter
    def ctphase(self, value):
        self.__ctphase = value

    @property
    def ctratio(self):
        return self.__ctratio

    @ctratio.setter
    def ctratio(self, value):
        self.__ctratio = value

    @property
    def deadtime(self):
        return self.__deadtime

    @deadtime.setter
    def deadtime(self, value):
        self.__deadtime = value

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, value):
        self.__delay = value

    @property
    def delayoff(self):
        return self.__delayoff

    @delayoff.setter
    def delayoff(self, value):
        self.__delayoff = value

    @property
    def element(self):
        return self.__element

    @element.setter
    def element(self, value):
        self.__element = value

    @property
    def eventlog(self):
        return self.__eventlog

    @eventlog.setter
    def eventlog(self, value):
        self.__eventlog = value

    @property
    def offsetting(self):
        return self.__offsetting

    @offsetting.setter
    def offsetting(self, value):
        self.__offsetting = value

    @property
    def onsetting(self):
        return self.__onsetting

    @onsetting.setter
    def onsetting(self, value):
        self.__onsetting = value

    @property
    def pctminkvar(self):
        return self.__pctminkvar

    @pctminkvar.setter
    def pctminkvar(self, value):
        self.__pctminkvar = value

    @property
    def ptphase(self):
        return self.__ptphase

    @ptphase.setter
    def ptphase(self, value):
        self.__ptphase = value

    @property
    def ptratio(self):
        return self.__ptratio

    @ptratio.setter
    def ptratio(self, value):
        self.__ptratio = value

    @property
    def reset(self):
        return self.__reset

    @reset.setter
    def reset(self, value):
        self.__reset = value

    @property
    def terminal(self):
        return self.__terminal

    @terminal.setter
    def terminal(self, value):
        self.__terminal = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def userdata(self):
        return self.__userdata

    @userdata.setter
    def userdata(self, value):
        self.__userdata = value

    @property
    def usermodel(self):
        return self.__usermodel

    @usermodel.setter
    def usermodel(self, value):
        self.__usermodel = value

    @property
    def vbus(self):
        return self.__vbus

    @vbus.setter
    def vbus(self, value):
        self.__vbus = value

    @property
    def vmax(self):
        return self.__vmax

    @vmax.setter
    def vmax(self, value):
        self.__vmax = value

    @property
    def vmin(self):
        return self.__vmin

    @vmin.setter
    def vmin(self, value):
        self.__vmin = value

    @property
    def voltoverride(self):
        return self.__voltoverride

    @voltoverride.setter
    def voltoverride(self, value):
        self.__voltoverride = value
