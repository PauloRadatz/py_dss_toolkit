# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 24/09/2021 at 22:29:34
 Project: py_dss_tools [set, 2021]
"""


class PDElement:

    def __init__(self):
        self.__basefreq = None
        self.__emergamps = None
        self.__enabled = None
        self.__faultrate = None
        self.__like = None
        self.__normamps = None
        self.__pctperm = None
        self.__phases = None
        self.__repair = None

    @property
    def basefreq(self):
        return self.__basefreq

    @basefreq.setter
    def basefreq(self, value):
        self.__basefreq = value

    @property
    def emergamps(self):
        return self.__emergamps

    @emergamps.setter
    def emergamps(self, value):
        self.__emergamps = value

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, value):
        self.__enabled = value

    @property
    def faultrate(self):
        return self.__faultrate

    @faultrate.setter
    def faultrate(self, value):
        self.__faultrate = value

    @property
    def like(self):
        return self.__like

    @like.setter
    def like(self, value):
        self.__like = value

    @property
    def normamps(self):
        return self.__normamps

    @normamps.setter
    def normamps(self, value):
        self.__normamps = value

    @property
    def pctperm(self):
        return self.__pctperm

    @pctperm.setter
    def pctperm(self, value):
        self.__pctperm = value

    @property
    def phases(self):
        return self.__phases

    @phases.setter
    def phases(self, value):
        self.__phases = value

    @property
    def repair(self):
        return self.__repair

    @repair.setter
    def repair(self, value):
        self.__repair = value
