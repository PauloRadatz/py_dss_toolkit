# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:05:36
 Project: py_dss_tools [set, 2021]
"""


class ExpControl:
    name = "ExpControl"
    name_plural = "ExpControls"
    columns = ['basefreq', 'deltaq_factor', 'enabled', 'eventlog', 'like', 'preferq', 'pvsystemlist', 'qbias',
               'qmaxlag', 'qmaxlead', 'slope', 'tresponse', 'vreg', 'vregmax', 'vregmin', 'vregtau']

    def __init__(self):
        self.__deltaq_factor = None
        self.__eventlog = None
        self.__preferq = None
        self.__pvsystemlist = None
        self.__qbias = None
        self.__qmaxlag = None
        self.__qmaxlead = None
        self.__slope = None
        self.__tresponse = None
        self.__vreg = None
        self.__vregmax = None
        self.__vregmin = None
        self.__vregtau = None

    @property
    def deltaq_factor(self):
        return self.__deltaq_factor

    @deltaq_factor.setter
    def deltaq_factor(self, value):
        self.__deltaq_factor = value

    @property
    def eventlog(self):
        return self.__eventlog

    @eventlog.setter
    def eventlog(self, value):
        self.__eventlog = value

    @property
    def preferq(self):
        return self.__preferq

    @preferq.setter
    def preferq(self, value):
        self.__preferq = value

    @property
    def pvsystemlist(self):
        return self.__pvsystemlist

    @pvsystemlist.setter
    def pvsystemlist(self, value):
        self.__pvsystemlist = value

    @property
    def qbias(self):
        return self.__qbias

    @qbias.setter
    def qbias(self, value):
        self.__qbias = value

    @property
    def qmaxlag(self):
        return self.__qmaxlag

    @qmaxlag.setter
    def qmaxlag(self, value):
        self.__qmaxlag = value

    @property
    def qmaxlead(self):
        return self.__qmaxlead

    @qmaxlead.setter
    def qmaxlead(self, value):
        self.__qmaxlead = value

    @property
    def slope(self):
        return self.__slope

    @slope.setter
    def slope(self, value):
        self.__slope = value

    @property
    def tresponse(self):
        return self.__tresponse

    @tresponse.setter
    def tresponse(self, value):
        self.__tresponse = value

    @property
    def vreg(self):
        return self.__vreg

    @vreg.setter
    def vreg(self, value):
        self.__vreg = value

    @property
    def vregmax(self):
        return self.__vregmax

    @vregmax.setter
    def vregmax(self, value):
        self.__vregmax = value

    @property
    def vregmin(self):
        return self.__vregmin

    @vregmin.setter
    def vregmin(self, value):
        self.__vregmin = value

    @property
    def vregtau(self):
        return self.__vregtau

    @vregtau.setter
    def vregtau(self, value):
        self.__vregtau = value
