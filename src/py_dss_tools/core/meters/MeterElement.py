# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 24/09/2021 at 23:37:56
 Project: py_dss_tools [set, 2021]
"""


class MeterElement:

    def __init__(self):
        self.__action = None
        self.__basefreq = None
        self.__element = None
        self.__enabled = None
        self.__like = None
        self.__terminal = None

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, value):
        self.__action = value

    @property
    def basefreq(self):
        return self.__basefreq

    @basefreq.setter
    def basefreq(self, value):
        self.__basefreq = value

    @property
    def element(self):
        return self.__element

    @element.setter
    def element(self, value):
        self.__element = value

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
    def terminal(self):
        return self.__terminal

    @terminal.setter
    def terminal(self, value):
        self.__terminal = value
