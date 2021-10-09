# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:09:46
 Project: py_dss_tools [set, 2021]
"""


class TCCCurve:
    name = "TCCCurve"
    name_plural = "TCCCurves"
    columns = ['c_array', 'like', 'npts', 't_array']

    def __init__(self):
        self.__c_array = None
        self.__npts = None
        self.__t_array = None

    @property
    def c_array(self):
        return self.__c_array

    @c_array.setter
    def c_array(self, value):
        self.__c_array = value

    @property
    def npts(self):
        return self.__npts

    @npts.setter
    def npts(self, value):
        self.__npts = value

    @property
    def t_array(self):
        return self.__t_array

    @t_array.setter
    def t_array(self, value):
        self.__t_array = value
