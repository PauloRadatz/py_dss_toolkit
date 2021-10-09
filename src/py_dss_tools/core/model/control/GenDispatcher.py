# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:05:57
 Project: py_dss_tools [set, 2021]
"""


class GenDispatcher:
    name = "GenDispatcher"
    name_plural = "GenDispatchers"
    columns = ['basefreq', 'element', 'enabled', 'genlist', 'kvarlimit', 'kwband', 'kwlimit', 'like', 'terminal']

    def __init__(self):
        self.__element = None
        self.__genlist = None
        self.__kvarlimit = None
        self.__kwband = None
        self.__kwlimit = None
        self.__terminal = None

    @property
    def element(self):
        return self.__element

    @element.setter
    def element(self, value):
        self.__element = value

    @property
    def genlist(self):
        return self.__genlist

    @genlist.setter
    def genlist(self, value):
        self.__genlist = value

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
    def kwlimit(self):
        return self.__kwlimit

    @kwlimit.setter
    def kwlimit(self, value):
        self.__kwlimit = value

    @property
    def terminal(self):
        return self.__terminal

    @terminal.setter
    def terminal(self, value):
        self.__terminal = value
