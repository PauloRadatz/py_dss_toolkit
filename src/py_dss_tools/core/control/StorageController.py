# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:06:51
 Project: py_dss_tools [set, 2021]
"""


class StorageController:
    name = "StorageController"
    name_plural = "StorageControllers"
    columns = ['%kwband', '%kwbandlow', '%ratecharge', '%ratekw', '%reserve', 'basefreq', 'daily', 'dispfactor', 'duty',
               'element', 'elementlist', 'enabled', 'eventlog', 'inhibittime', 'kwactual', 'kwband', 'kwbandlow',
               'kwhactual', 'kwhtotal', 'kwneed', 'kwtarget', 'kwtargetlow', 'kwthreshold', 'kwtotal', 'like',
               'modecharge', 'modedischarge', 'monphase', 'resetlevel', 'seasons', 'seasontargets', 'seasontargetslow',
               'tdn', 'terminal', 'tflat', 'timechargetrigger', 'timedischargetrigger', 'tup', 'weights', 'yearly']

    def __init__(self):
        self.__percent_kwband = None
        self.__percent_kwbandlow = None
        self.__percent_ratecharge = None
        self.__percent_ratekw = None
        self.__percent_reserve = None
        self.__daily = None
        self.__dispfactor = None
        self.__duty = None
        self.__element = None
        self.__elementlist = None
        self.__eventlog = None
        self.__inhibittime = None
        self.__kwactual = None
        self.__kwband = None
        self.__kwbandlow = None
        self.__kwhactual = None
        self.__kwhtotal = None
        self.__kwneed = None
        self.__kwtarget = None
        self.__kwtargetlow = None
        self.__kwthreshold = None
        self.__kwtotal = None
        self.__modecharge = None
        self.__modedischarge = None
        self.__monphase = None
        self.__resetlevel = None
        self.__seasons = None
        self.__seasontargets = None
        self.__seasontargetslow = None
        self.__tdn = None
        self.__terminal = None
        self.__tflat = None
        self.__timechargetrigger = None
        self.__timedischargetrigger = None
        self.__tup = None
        self.__weights = None
        self.__yearly = None

    @property
    def percent_kwband(self):
        return self.__percent_kwband

    @percent_kwband.setter
    def percent_kwband(self, value):
        self.__percent_kwband = value

    @property
    def percent_kwbandlow(self):
        return self.__percent_kwbandlow

    @percent_kwbandlow.setter
    def percent_kwbandlow(self, value):
        self.__percent_kwbandlow = value

    @property
    def percent_ratecharge(self):
        return self.__percent_ratecharge

    @percent_ratecharge.setter
    def percent_ratecharge(self, value):
        self.__percent_ratecharge = value

    @property
    def percent_ratekw(self):
        return self.__percent_ratekw

    @percent_ratekw.setter
    def percent_ratekw(self, value):
        self.__percent_ratekw = value

    @property
    def percent_reserve(self):
        return self.__percent_reserve

    @percent_reserve.setter
    def percent_reserve(self, value):
        self.__percent_reserve = value

    @property
    def daily(self):
        return self.__daily

    @daily.setter
    def daily(self, value):
        self.__daily = value

    @property
    def dispfactor(self):
        return self.__dispfactor

    @dispfactor.setter
    def dispfactor(self, value):
        self.__dispfactor = value

    @property
    def duty(self):
        return self.__duty

    @duty.setter
    def duty(self, value):
        self.__duty = value

    @property
    def element(self):
        return self.__element

    @element.setter
    def element(self, value):
        self.__element = value

    @property
    def elementlist(self):
        return self.__elementlist

    @elementlist.setter
    def elementlist(self, value):
        self.__elementlist = value

    @property
    def eventlog(self):
        return self.__eventlog

    @eventlog.setter
    def eventlog(self, value):
        self.__eventlog = value

    @property
    def inhibittime(self):
        return self.__inhibittime

    @inhibittime.setter
    def inhibittime(self, value):
        self.__inhibittime = value

    @property
    def kwactual(self):
        return self.__kwactual

    @kwactual.setter
    def kwactual(self, value):
        self.__kwactual = value

    @property
    def kwband(self):
        return self.__kwband

    @kwband.setter
    def kwband(self, value):
        self.__kwband = value

    @property
    def kwbandlow(self):
        return self.__kwbandlow

    @kwbandlow.setter
    def kwbandlow(self, value):
        self.__kwbandlow = value

    @property
    def kwhactual(self):
        return self.__kwhactual

    @kwhactual.setter
    def kwhactual(self, value):
        self.__kwhactual = value

    @property
    def kwhtotal(self):
        return self.__kwhtotal

    @kwhtotal.setter
    def kwhtotal(self, value):
        self.__kwhtotal = value

    @property
    def kwneed(self):
        return self.__kwneed

    @kwneed.setter
    def kwneed(self, value):
        self.__kwneed = value

    @property
    def kwtarget(self):
        return self.__kwtarget

    @kwtarget.setter
    def kwtarget(self, value):
        self.__kwtarget = value

    @property
    def kwtargetlow(self):
        return self.__kwtargetlow

    @kwtargetlow.setter
    def kwtargetlow(self, value):
        self.__kwtargetlow = value

    @property
    def kwthreshold(self):
        return self.__kwthreshold

    @kwthreshold.setter
    def kwthreshold(self, value):
        self.__kwthreshold = value

    @property
    def kwtotal(self):
        return self.__kwtotal

    @kwtotal.setter
    def kwtotal(self, value):
        self.__kwtotal = value

    @property
    def modecharge(self):
        return self.__modecharge

    @modecharge.setter
    def modecharge(self, value):
        self.__modecharge = value

    @property
    def modedischarge(self):
        return self.__modedischarge

    @modedischarge.setter
    def modedischarge(self, value):
        self.__modedischarge = value

    @property
    def monphase(self):
        return self.__monphase

    @monphase.setter
    def monphase(self, value):
        self.__monphase = value

    @property
    def resetlevel(self):
        return self.__resetlevel

    @resetlevel.setter
    def resetlevel(self, value):
        self.__resetlevel = value

    @property
    def seasons(self):
        return self.__seasons

    @seasons.setter
    def seasons(self, value):
        self.__seasons = value

    @property
    def seasontargets(self):
        return self.__seasontargets

    @seasontargets.setter
    def seasontargets(self, value):
        self.__seasontargets = value

    @property
    def seasontargetslow(self):
        return self.__seasontargetslow

    @seasontargetslow.setter
    def seasontargetslow(self, value):
        self.__seasontargetslow = value

    @property
    def tdn(self):
        return self.__tdn

    @tdn.setter
    def tdn(self, value):
        self.__tdn = value

    @property
    def terminal(self):
        return self.__terminal

    @terminal.setter
    def terminal(self, value):
        self.__terminal = value

    @property
    def tflat(self):
        return self.__tflat

    @tflat.setter
    def tflat(self, value):
        self.__tflat = value

    @property
    def timechargetrigger(self):
        return self.__timechargetrigger

    @timechargetrigger.setter
    def timechargetrigger(self, value):
        self.__timechargetrigger = value

    @property
    def timedischargetrigger(self):
        return self.__timedischargetrigger

    @timedischargetrigger.setter
    def timedischargetrigger(self, value):
        self.__timedischargetrigger = value

    @property
    def tup(self):
        return self.__tup

    @tup.setter
    def tup(self, value):
        self.__tup = value

    @property
    def weights(self):
        return self.__weights

    @weights.setter
    def weights(self, value):
        self.__weights = value

    @property
    def yearly(self):
        return self.__yearly

    @yearly.setter
    def yearly(self, value):
        self.__yearly = value
