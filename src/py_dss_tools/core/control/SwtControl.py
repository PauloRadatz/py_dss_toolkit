# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:06:59
 Project: py_dss_tools [set, 2021]
"""


class SwtControl:
    name = "SwtControl"
    name_plural = "SwtControls"
    columns = ['action', 'basefreq', 'delay', 'enabled', 'like', 'lock', 'normal', 'reset', 'state', 'switchedobj',
               'switchedterm']

    def __init__(self):
        self.__action = None
        self.__delay = None
        self.__lock = None
        self.__normal = None
        self.__reset = None
        self.__state = None
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
    def lock(self):
        return self.__lock

    @lock.setter
    def lock(self, value):
        self.__lock = value

    @property
    def normal(self):
        return self.__normal

    @normal.setter
    def normal(self, value):
        self.__normal = value

    @property
    def reset(self):
        return self.__reset

    @reset.setter
    def reset(self, value):
        self.__reset = value

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value

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
