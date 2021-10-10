# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 04/09/2021 at 20:39:19
 Project: py_dss_tools [set, 2021]
"""
from .PCElement import PCElement


class Load(PCElement):
    name = "Load"
    name_plural = "Loads"
    columns = ['%mean', '%seriesrl', '%stddev', 'allocationfactor', 'basefreq', 'bus1', 'cfactor', 'class', 'conn',
               'cvrcurve', 'cvrvars', 'cvrwatts', 'daily', 'duty', 'enabled', 'growth', 'kv', 'kva', 'kvar', 'kw',
               'kwh', 'kwhdays', 'like', 'model', 'numcust', 'pf', 'phases', 'puxharm', 'relweight', 'rneut',
               'spectrum', 'status', 'vlowpu', 'vmaxpu', 'vminemerg', 'vminnorm', 'vminpu', 'xfkva', 'xneut', 'xrharm',
               'yearly', 'zipv']

    def __init__(self):
        super().__init__()
        self.__percent_mean = None
        self.__percent_seriesrl = None
        self.__percent_stddev = None
        self.__allocationfactor = None
        self.__cfactor = None
        self.__class_ = None
        self.__conn = None
        self.__cvrcurve = None
        self.__cvrvars = None
        self.__cvrwatts = None
        self.__daily = None
        self.__duty = None
        self.__growth = None
        self.__kv = None
        self.__kva = None
        self.__kvar = None
        self.__kw = None
        self.__kwh = None
        self.__kwhdays = None
        self.__model = None
        self.__numcust = None
        self.__pf = None
        self.__puxharm = None
        self.__relweight = None
        self.__rneut = None
        self.__status = None
        self.__vlowpu = None
        self.__vmaxpu = None
        self.__vminemerg = None
        self.__vminnorm = None
        self.__vminpu = None
        self.__xfkva = None
        self.__xneut = None
        self.__xrharm = None
        self.__yearly = None
        self.__zipv = None

    @property
    def percent_mean(self):
        return self.__percent_mean

    @percent_mean.setter
    def percent_mean(self, value):
        self.__percent_mean = value

    @property
    def percent_seriesrl(self):
        return self.__percent_seriesrl

    @percent_seriesrl.setter
    def percent_seriesrl(self, value):
        self.__percent_seriesrl = value

    @property
    def percent_stddev(self):
        return self.__percent_stddev

    @percent_stddev.setter
    def percent_stddev(self, value):
        self.__percent_stddev = value

    @property
    def allocationfactor(self):
        return self.__allocationfactor

    @allocationfactor.setter
    def allocationfactor(self, value):
        self.__allocationfactor = value

    @property
    def cfactor(self):
        return self.__cfactor

    @cfactor.setter
    def cfactor(self, value):
        self.__cfactor = value

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
    def cvrcurve(self):
        return self.__cvrcurve

    @cvrcurve.setter
    def cvrcurve(self, value):
        self.__cvrcurve = value

    @property
    def cvrvars(self):
        return self.__cvrvars

    @cvrvars.setter
    def cvrvars(self, value):
        self.__cvrvars = value

    @property
    def cvrwatts(self):
        return self.__cvrwatts

    @cvrwatts.setter
    def cvrwatts(self, value):
        self.__cvrwatts = value

    @property
    def daily(self):
        return self.__daily

    @daily.setter
    def daily(self, value):
        self.__daily = value

    @property
    def duty(self):
        return self.__duty

    @duty.setter
    def duty(self, value):
        self.__duty = value

    @property
    def growth(self):
        return self.__growth

    @growth.setter
    def growth(self, value):
        self.__growth = value

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
    def kwh(self):
        return self.__kwh

    @kwh.setter
    def kwh(self, value):
        self.__kwh = value

    @property
    def kwhdays(self):
        return self.__kwhdays

    @kwhdays.setter
    def kwhdays(self, value):
        self.__kwhdays = value

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        self.__model = value

    @property
    def numcust(self):
        return self.__numcust

    @numcust.setter
    def numcust(self, value):
        self.__numcust = value

    @property
    def pf(self):
        return self.__pf

    @pf.setter
    def pf(self, value):
        self.__pf = value

    @property
    def puxharm(self):
        return self.__puxharm

    @puxharm.setter
    def puxharm(self, value):
        self.__puxharm = value

    @property
    def relweight(self):
        return self.__relweight

    @relweight.setter
    def relweight(self, value):
        self.__relweight = value

    @property
    def rneut(self):
        return self.__rneut

    @rneut.setter
    def rneut(self, value):
        self.__rneut = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def vlowpu(self):
        return self.__vlowpu

    @vlowpu.setter
    def vlowpu(self, value):
        self.__vlowpu = value

    @property
    def vmaxpu(self):
        return self.__vmaxpu

    @vmaxpu.setter
    def vmaxpu(self, value):
        self.__vmaxpu = value

    @property
    def vminemerg(self):
        return self.__vminemerg

    @vminemerg.setter
    def vminemerg(self, value):
        self.__vminemerg = value

    @property
    def vminnorm(self):
        return self.__vminnorm

    @vminnorm.setter
    def vminnorm(self, value):
        self.__vminnorm = value

    @property
    def vminpu(self):
        return self.__vminpu

    @vminpu.setter
    def vminpu(self, value):
        self.__vminpu = value

    @property
    def xfkva(self):
        return self.__xfkva

    @xfkva.setter
    def xfkva(self, value):
        self.__xfkva = value

    @property
    def xneut(self):
        return self.__xneut

    @xneut.setter
    def xneut(self, value):
        self.__xneut = value

    @property
    def xrharm(self):
        return self.__xrharm

    @xrharm.setter
    def xrharm(self, value):
        self.__xrharm = value

    @property
    def yearly(self):
        return self.__yearly

    @yearly.setter
    def yearly(self, value):
        self.__yearly = value

    @property
    def zipv(self):
        return self.__zipv

    @zipv.setter
    def zipv(self, value):
        self.__zipv = value
