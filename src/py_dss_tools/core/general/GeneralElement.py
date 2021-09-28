# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 24/09/2021 at 23:51:07
 Project: py_dss_tools [set, 2021]
"""


class GeneralElement:
    def __init__(self):
        self.__like = None

    @property
    def like(self):
        return self.__like

    @like.setter
    def like(self, value):
        self.__like = value
