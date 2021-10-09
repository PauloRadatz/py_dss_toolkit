# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:11:07
 Project: py_dss_tools [set, 2021]
"""


class Monitor:
    name = "Monitor"
    name_plural = "Monitors"
    columns = ['action', 'basefreq', 'element', 'enabled', 'like', 'mode', 'ppolar', 'residual', 'terminal', 'vipolar']

    def __init__(self):
        self.__mode = None
        self.__ppolar = None
        self.__residual = None
        self.__vipolar = None

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        self.__mode = value

    @property
    def ppolar(self):
        return self.__ppolar

    @ppolar.setter
    def ppolar(self, value):
        self.__ppolar = value

    @property
    def residual(self):
        return self.__residual

    @residual.setter
    def residual(self, value):
        self.__residual = value

    @property
    def vipolar(self):
        return self.__vipolar

    @vipolar.setter
    def vipolar(self, value):
        self.__vipolar = value
