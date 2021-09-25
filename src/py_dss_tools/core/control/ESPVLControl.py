# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:05:30
 Project: py_dss_tools [set, 2021]
"""


class ESPVLControl:
    name = "ESPVLControl"
    name_plural = "ESPVLControls"
    columns = ['basefreq', 'element', 'enabled', 'forecast', 'kvarlimit', 'kwband', 'like', 'localcontrollist',
               'localcontrolweights', 'pvsystemlist', 'pvsystemweights', 'storagelist', 'storageweights', 'terminal',
               'type']

    def __init__(self):
        self.__element = None
        self.__forecast = None
        self.__kvarlimit = None
        self.__kwband = None
        self.__localcontrollist = None
        self.__localcontrolweights = None
        self.__pvsystemlist = None
        self.__pvsystemweights = None
        self.__storagelist = None
        self.__storageweights = None
        self.__terminal = None
        self.__type = None

    @property
    def element(self):
        return self.__element

    @element.setter
    def element(self, value):
        self.__element = value

    @property
    def forecast(self):
        return self.__forecast

    @forecast.setter
    def forecast(self, value):
        self.__forecast = value

    @property
    def kvarlimit(self):
        return self.__kvarlimit

    @kvarlimit.setter
    def kvarlimit(self, value):
        self.__kvarlimit = value

    @property
    def kwband(self):
        return self.__kwband

    @kwband.setter
    def kwband(self, value):
        self.__kwband = value

    @property
    def localcontrollist(self):
        return self.__localcontrollist

    @localcontrollist.setter
    def localcontrollist(self, value):
        self.__localcontrollist = value

    @property
    def localcontrolweights(self):
        return self.__localcontrolweights

    @localcontrolweights.setter
    def localcontrolweights(self, value):
        self.__localcontrolweights = value

    @property
    def pvsystemlist(self):
        return self.__pvsystemlist

    @pvsystemlist.setter
    def pvsystemlist(self, value):
        self.__pvsystemlist = value

    @property
    def pvsystemweights(self):
        return self.__pvsystemweights

    @pvsystemweights.setter
    def pvsystemweights(self, value):
        self.__pvsystemweights = value

    @property
    def storagelist(self):
        return self.__storagelist

    @storagelist.setter
    def storagelist(self, value):
        self.__storagelist = value

    @property
    def storageweights(self):
        return self.__storageweights

    @storageweights.setter
    def storageweights(self, value):
        self.__storageweights = value

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
