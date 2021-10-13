# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 22:44:49
 Project: py_dss_tools [set, 2021]
"""
from py_dss_tools.model.pdelement import PDElement


class GICTransformer(PDElement):
    name = "GICTransformer"
    name_plural = "GICTransformers"
    columns = ['porcentagem_r1', 'porcentagem__r2', 'basefreq', 'bush', 'busnh', 'busnx', 'busx', 'emergamps',
               'enabled', 'faultrate', 'k', 'kvll1', 'kvll2', 'like', 'mva', 'normamps', 'pctperm', 'phases', 'r1',
               'r2', 'repair', 'type', 'varcurve']

    def __init__(self):
        super().__init__()
        self.__porcentagem_r1 = None
        self.__porcentagem_r2 = None
        self.__bush = None
        self.__busnh = None
        self.__busnx = None
        self.__busx = None
        self.__k = None
        self.__kvll1 = None
        self.__kvll2 = None
        self.__mva = None
        self.__r1 = None
        self.__r2 = None
        self.__type = None
        self.__varcurve = None

    @property
    def porcentagem_r1(self):
        return self.__porcentagem_r1

    @porcentagem_r1.setter
    def porcentagem_r1(self, value):
        self.__porcentagem_r1 = value

    @property
    def porcentagem_r2(self):
        return self.__porcentagem_r2

    @porcentagem_r2.setter
    def porcentagem_r2(self, value):
        self.__porcentagem_r2 = value

    @property
    def bush(self):
        return self.__bush

    @bush.setter
    def bush(self, value):
        self.__bush = value

    @property
    def busnh(self):
        return self.__busnh

    @busnh.setter
    def busnh(self, value):
        self.__busnh = value

    @property
    def busnx(self):
        return self.__busnx

    @busnx.setter
    def busnx(self, value):
        self.__busnx = value

    @property
    def busx(self):
        return self.__busx

    @busx.setter
    def busx(self, value):
        self.__busx = value

    @property
    def k(self):
        return self.__k

    @k.setter
    def k(self, value):
        self.__k = value

    @property
    def kvll1(self):
        return self.__kvll1

    @kvll1.setter
    def kvll1(self, value):
        self.__kvll1 = value

    @property
    def kvll2(self):
        return self.__kvll2

    @kvll2.setter
    def kvll2(self, value):
        self.__kvll2 = value

    @property
    def mva(self):
        return self.__mva

    @mva.setter
    def mva(self, value):
        self.__mva = value

    @property
    def r1(self):
        return self.__r1

    @r1.setter
    def r1(self, value):
        self.__r1 = value

    @property
    def r2(self):
        return self.__r2

    @r2.setter
    def r2(self, value):
        self.__r2 = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def varcurve(self):
        return self.__varcurve

    @varcurve.setter
    def varcurve(self, value):
        self.__varcurve = value
