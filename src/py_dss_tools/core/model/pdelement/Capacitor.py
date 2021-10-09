# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 22:36:39
 Project: py_dss_tools [set, 2021]
"""
from py_dss_tools.core.model.pdelement.PDElement import PDElement


class Capacitor(PDElement):
    name = "Capacitor"
    name_plural = "Capacitors"
    columns = ['basefreq', 'bus1', 'bus2', 'cmatrix', 'conn', 'cuf', 'emergamps', 'enabled', 'faultrate', 'harm',
               'kv', 'kvar', 'like', 'normamps', 'numsteps', 'pctperm', 'phases', 'r', 'repair', 'states', 'xl']

    def __init__(self):
        super().__init__()
        self.__bus1 = None
        self.__bus2 = None
        self.__cmatrix = None
        self.__conn = None
        self.__cuf = None
        self.__harm = None
        self.__kv = None
        self.__kvar = None
        self.__numsteps = None
        self.__r = None
        self.__states = None
        self.__xl = None

    @property
    def bus1(self):
        return self.__bus1

    @bus1.setter
    def bus1(self, value):
        self.__bus1 = value

    @property
    def bus2(self):
        return self.__bus2

    @bus2.setter
    def bus2(self, value):
        self.__bus2 = value

    @property
    def cmatrix(self):
        return self.__cmatrix

    @cmatrix.setter
    def cmatrix(self, value):
        self.__cmatrix = value

    @property
    def conn(self):
        return self.__conn

    @conn.setter
    def conn(self, value):
        self.__conn = value

    @property
    def cuf(self):
        return self.__cuf

    @cuf.setter
    def cuf(self, value):
        self.__cuf = value

    @property
    def harm(self):
        return self.__harm

    @harm.setter
    def harm(self, value):
        self.__harm = value

    @property
    def kv(self):
        return self.__kv

    @kv.setter
    def kv(self, value):
        self.__kv = value

    @property
    def kvar(self):
        return self.__kvar

    @kvar.setter
    def kvar(self, value):
        self.__kvar = value

    @property
    def numsteps(self):
        return self.__numsteps

    @numsteps.setter
    def numsteps(self, value):
        self.__numsteps = value

    @property
    def r(self):
        return self.__r

    @r.setter
    def r(self, value):
        self.__r = value

    @property
    def states(self):
        return self.__states

    @states.setter
    def states(self, value):
        self.__states = value

    @property
    def xl(self):
        return self.__xl

    @xl.setter
    def xl(self, value):
        self.__xl = value
