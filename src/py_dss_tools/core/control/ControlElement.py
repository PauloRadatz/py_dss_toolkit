# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 25/09/2021 at 00:01:58
 Project: py_dss_tools [set, 2021]
"""


class ControlElement:

    def __init__(self):
        self.__basefreq = None
        self.__enabled = None
        self.__like = None

    @property
    def basefreq(self):
        return self.__basefreq

    @basefreq.setter
    def basefreq(self, value):
        self.__basefreq = value

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
