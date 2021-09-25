# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 04/09/2021 at 20:38:47
 Project: py_dss_tools [set, 2021]
"""
from .PCElement import PCElement


class Generator(PCElement):
    name = "Generator"
    name_plural = "Generators"
    columns = ['%fuel', '%reserve', 'balanced', 'basefreq', 'bus1', 'class', 'conn', 'd', 'daily', 'debugtrace',
               'dispmode', 'dispvalue', 'duty', 'dutystart', 'enabled', 'forceon', 'fuelkwh', 'h', 'kv', 'kva', 'kvar',
               'kw', 'like', 'maxkvar', 'minkvar', 'model', 'mva', 'pf', 'phases', 'pvfactor', 'refuel', 'rneut',
               'shaftdata', 'shaftmodel', 'spectrum', 'status', 'usefuel', 'userdata', 'usermodel', 'vmaxpu', 'vminpu',
               'vpu', 'xd', 'xdp', 'xdpp', 'xneut', 'xrdp', 'yearly']

    def __init__(self):
        super().__init__()
        self.__percent_fuel = None
        self.__percent_reserve = None
        self.__balanced = None
        self.__class_ = None
        self.__conn = None
        self.__d = None
        self.__daily = None
        self.__debugtrace = None
        self.__dispmode = None
        self.__dispvalue = None
        self.__duty = None
        self.__dutystart = None
        self.__forceon = None
        self.__fuelkwh = None
        self.__h = None
        self.__kv = None
        self.__kva = None
        self.__kvar = None
        self.__kw = None
        self.__maxkvar = None
        self.__minkvar = None
        self.__model = None
        self.__mva = None
        self.__pf = None
        self.__pvfactor = None
        self.__refuel = None
        self.__rneut = None
        self.__shaftdata = None
        self.__shaftmodel = None
        self.__status = None
        self.__usefuel = None
        self.__userdata = None
        self.__usermodel = None
        self.__vmaxpu = None
        self.__vminpu = None
        self.__vpu = None
        self.__xd = None
        self.__xdp = None
        self.__xdpp = None
        self.__xneut = None
        self.__xrdp = None
        self.__yearly = None

    @property
    def percent_fuel(self):
        return self.__percent_fuel

    @percent_fuel.setter
    def percent_fuel(self, value):
        self.__percent_fuel = value

    @property
    def percent_reserve(self):
        return self.__percent_reserve

    @percent_reserve.setter
    def percent_reserve(self, value):
        self.__percent_reserve = value

    @property
    def balanced(self):
        return self.__balanced

    @balanced.setter
    def balanced(self, value):
        self.__balanced = value

    @property
    def class_(self):
        return self.__class_

    @class_.setter
    def class_(self, value):
        self.__class_ = value

    @property
    def conn(self):
        return self.__conn

    @conn.setter
    def conn(self, value):
        self.__conn = value

    @property
    def d(self):
        return self.__d

    @d.setter
    def d(self, value):
        self.__d = value

    @property
    def daily(self):
        return self.__daily

    @daily.setter
    def daily(self, value):
        self.__daily = value

    @property
    def debugtrace(self):
        return self.__debugtrace

    @debugtrace.setter
    def debugtrace(self, value):
        self.__debugtrace = value

    @property
    def dispmode(self):
        return self.__dispmode

    @dispmode.setter
    def dispmode(self, value):
        self.__dispmode = value

    @property
    def dispvalue(self):
        return self.__dispvalue

    @dispvalue.setter
    def dispvalue(self, value):
        self.__dispvalue = value

    @property
    def duty(self):
        return self.__duty

    @duty.setter
    def duty(self, value):
        self.__duty = value

    @property
    def dutystart(self):
        return self.__dutystart

    @dutystart.setter
    def dutystart(self, value):
        self.__dutystart = value

    @property
    def forceon(self):
        return self.__forceon

    @forceon.setter
    def forceon(self, value):
        self.__forceon = value

    @property
    def fuelkwh(self):
        return self.__fuelkwh

    @fuelkwh.setter
    def fuelkwh(self, value):
        self.__fuelkwh = value

    @property
    def h(self):
        return self.__h

    @h.setter
    def h(self, value):
        self.__h = value

    @property
    def kv(self):
        return self.__kv

    @kv.setter
    def kv(self, value):
        self.__kv = value

    @property
    def kva(self):
        return self.__kva

    @kva.setter
    def kva(self, value):
        self.__kva = value

    @property
    def kvar(self):
        return self.__kvar

    @kvar.setter
    def kvar(self, value):
        self.__kvar = value

    @property
    def kw(self):
        return self.__kw

    @kw.setter
    def kw(self, value):
        self.__kw = value

    @property
    def maxkvar(self):
        return self.__maxkvar

    @maxkvar.setter
    def maxkvar(self, value):
        self.__maxkvar = value

    @property
    def minkvar(self):
        return self.__minkvar

    @minkvar.setter
    def minkvar(self, value):
        self.__minkvar = value

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        self.__model = value

    @property
    def mva(self):
        return self.__mva

    @mva.setter
    def mva(self, value):
        self.__mva = value

    @property
    def pf(self):
        return self.__pf

    @pf.setter
    def pf(self, value):
        self.__pf = value

    @property
    def pvfactor(self):
        return self.__pvfactor

    @pvfactor.setter
    def pvfactor(self, value):
        self.__pvfactor = value

    @property
    def refuel(self):
        return self.__refuel

    @refuel.setter
    def refuel(self, value):
        self.__refuel = value

    @property
    def rneut(self):
        return self.__rneut

    @rneut.setter
    def rneut(self, value):
        self.__rneut = value

    @property
    def shaftdata(self):
        return self.__shaftdata

    @shaftdata.setter
    def shaftdata(self, value):
        self.__shaftdata = value

    @property
    def shaftmodel(self):
        return self.__shaftmodel

    @shaftmodel.setter
    def shaftmodel(self, value):
        self.__shaftmodel = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def usefuel(self):
        return self.__usefuel

    @usefuel.setter
    def usefuel(self, value):
        self.__usefuel = value

    @property
    def userdata(self):
        return self.__userdata

    @userdata.setter
    def userdata(self, value):
        self.__userdata = value

    @property
    def usermodel(self):
        return self.__usermodel

    @usermodel.setter
    def usermodel(self, value):
        self.__usermodel = value

    @property
    def vmaxpu(self):
        return self.__vmaxpu

    @vmaxpu.setter
    def vmaxpu(self, value):
        self.__vmaxpu = value

    @property
    def vminpu(self):
        return self.__vminpu

    @vminpu.setter
    def vminpu(self, value):
        self.__vminpu = value

    @property
    def vpu(self):
        return self.__vpu

    @vpu.setter
    def vpu(self, value):
        self.__vpu = value

    @property
    def xd(self):
        return self.__xd

    @xd.setter
    def xd(self, value):
        self.__xd = value

    @property
    def xdp(self):
        return self.__xdp

    @xdp.setter
    def xdp(self, value):
        self.__xdp = value

    @property
    def xdpp(self):
        return self.__xdpp

    @xdpp.setter
    def xdpp(self, value):
        self.__xdpp = value

    @property
    def xneut(self):
        return self.__xneut

    @xneut.setter
    def xneut(self, value):
        self.__xneut = value

    @property
    def xrdp(self):
        return self.__xrdp

    @xrdp.setter
    def xrdp(self, value):
        self.__xrdp = value

    @property
    def yearly(self):
        return self.__yearly

    @yearly.setter
    def yearly(self, value):
        self.__yearly = value
