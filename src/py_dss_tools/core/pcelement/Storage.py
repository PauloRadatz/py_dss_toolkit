# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:03:41
 Project: py_dss_tools [set, 2021]
"""
from .PCElement import PCElement


class Storage(PCElement):
    name = "Storage"
    name_plural = "Storages"
    columns = ['%charge', '%cutin', '%cutout', '%discharge', '%effcharge', '%effdischarge', '%idlingkvar', '%idlingkw',
               '%kwrated', '%pminkvarmax', '%pminnovars', '%r', '%reserve', '%stored', '%x', 'balanced', 'basefreq',
               'bus1', 'chargetrigger', 'class', 'conn', 'daily', 'debugtrace', 'dischargetrigger', 'dispmode', 'duty',
               'dynadata', 'dynadll', 'effcurve', 'enabled', 'kv', 'kva', 'kvar', 'kvarmax', 'kvarmaxabs', 'kw',
               'kwhrated', 'kwhstored', 'kwrated', 'like', 'limitcurrent', 'model', 'pf', 'pfpriority', 'phases',
               'spectrum', 'state', 'timechargetrig', 'userdata', 'usermodel', 'varfollowinverter', 'vmaxpu', 'vminpu',
               'wattpriority', 'yearly']

    def __init__(self):
        super().__init__()
        self.__percent_charge = None
        self.__percent_cutin = None
        self.__percent_cutout = None
        self.__percent_discharge = None
        self.__percent_effcharge = None
        self.__percent_effdischarge = None
        self.__percent_idlingkvar = None
        self.__percent_idlingkw = None
        self.__percent_kwrated = None
        self.__percent_pminkvarmax = None
        self.__percent_pminnovars = None
        self.__percent_r = None
        self.__percent_reserve = None
        self.__percent_stored = None
        self.__percent_x = None
        self.__balanced = None
        self.__chargetrigger = None
        self.__class_ = None
        self.__conn = None
        self.__daily = None
        self.__debugtrace = None
        self.__dischargetrigger = None
        self.__dispmode = None
        self.__duty = None
        self.__dynadata = None
        self.__dynadll = None
        self.__effcurve = None
        self.__kv = None
        self.__kva = None
        self.__kvar = None
        self.__kvarmax = None
        self.__kvarmaxabs = None
        self.__kw = None
        self.__kwhrated = None
        self.__kwhstored = None
        self.__kwrated = None
        self.__limitcurrent = None
        self.__model = None
        self.__pf = None
        self.__pfpriority = None
        self.__state = None
        self.__timechargetrig = None
        self.__userdata = None
        self.__usermodel = None
        self.__varfollowinverter = None
        self.__vmaxpu = None
        self.__vminpu = None
        self.__wattpriority = None
        self.__yearly = None

    @property
    def percent_charge(self):
        return self.__percent_charge

    @percent_charge.setter
    def percent_charge(self, value):
        self.__percent_charge = value

    @property
    def percent_cutin(self):
        return self.__percent_cutin

    @percent_cutin.setter
    def percent_cutin(self, value):
        self.__percent_cutin = value

    @property
    def percent_cutout(self):
        return self.__percent_cutout

    @percent_cutout.setter
    def percent_cutout(self, value):
        self.__percent_cutout = value

    @property
    def percent_discharge(self):
        return self.__percent_discharge

    @percent_discharge.setter
    def percent_discharge(self, value):
        self.__percent_discharge = value

    @property
    def percent_effcharge(self):
        return self.__percent_effcharge

    @percent_effcharge.setter
    def percent_effcharge(self, value):
        self.__percent_effcharge = value

    @property
    def percent_effdischarge(self):
        return self.__percent_effdischarge

    @percent_effdischarge.setter
    def percent_effdischarge(self, value):
        self.__percent_effdischarge = value

    @property
    def percent_idlingkvar(self):
        return self.__percent_idlingkvar

    @percent_idlingkvar.setter
    def percent_idlingkvar(self, value):
        self.__percent_idlingkvar = value

    @property
    def percent_idlingkw(self):
        return self.__percent_idlingkw

    @percent_idlingkw.setter
    def percent_idlingkw(self, value):
        self.__percent_idlingkw = value

    @property
    def percent_kwrated(self):
        return self.__percent_kwrated

    @percent_kwrated.setter
    def percent_kwrated(self, value):
        self.__percent_kwrated = value

    @property
    def percent_pminkvarmax(self):
        return self.__percent_pminkvarmax

    @percent_pminkvarmax.setter
    def percent_pminkvarmax(self, value):
        self.__percent_pminkvarmax = value

    @property
    def percent_pminnovars(self):
        return self.__percent_pminnovars

    @percent_pminnovars.setter
    def percent_pminnovars(self, value):
        self.__percent_pminnovars = value

    @property
    def percent_r(self):
        return self.__percent_r

    @percent_r.setter
    def percent_r(self, value):
        self.__percent_r = value

    @property
    def percent_reserve(self):
        return self.__percent_reserve

    @percent_reserve.setter
    def percent_reserve(self, value):
        self.__percent_reserve = value

    @property
    def percent_stored(self):
        return self.__percent_stored

    @percent_stored.setter
    def percent_stored(self, value):
        self.__percent_stored = value

    @property
    def percent_x(self):
        return self.__percent_x

    @percent_x.setter
    def percent_x(self, value):
        self.__percent_x = value

    @property
    def balanced(self):
        return self.__balanced

    @balanced.setter
    def balanced(self, value):
        self.__balanced = value

    @property
    def chargetrigger(self):
        return self.__chargetrigger

    @chargetrigger.setter
    def chargetrigger(self, value):
        self.__chargetrigger = value

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
    def dischargetrigger(self):
        return self.__dischargetrigger

    @dischargetrigger.setter
    def dischargetrigger(self, value):
        self.__dischargetrigger = value

    @property
    def dispmode(self):
        return self.__dispmode

    @dispmode.setter
    def dispmode(self, value):
        self.__dispmode = value

    @property
    def duty(self):
        return self.__duty

    @duty.setter
    def duty(self, value):
        self.__duty = value

    @property
    def dynadata(self):
        return self.__dynadata

    @dynadata.setter
    def dynadata(self, value):
        self.__dynadata = value

    @property
    def dynadll(self):
        return self.__dynadll

    @dynadll.setter
    def dynadll(self, value):
        self.__dynadll = value

    @property
    def effcurve(self):
        return self.__effcurve

    @effcurve.setter
    def effcurve(self, value):
        self.__effcurve = value

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
    def kvarmax(self):
        return self.__kvarmax

    @kvarmax.setter
    def kvarmax(self, value):
        self.__kvarmax = value

    @property
    def kvarmaxabs(self):
        return self.__kvarmaxabs

    @kvarmaxabs.setter
    def kvarmaxabs(self, value):
        self.__kvarmaxabs = value

    @property
    def kw(self):
        return self.__kw

    @kw.setter
    def kw(self, value):
        self.__kw = value

    @property
    def kwhrated(self):
        return self.__kwhrated

    @kwhrated.setter
    def kwhrated(self, value):
        self.__kwhrated = value

    @property
    def kwhstored(self):
        return self.__kwhstored

    @kwhstored.setter
    def kwhstored(self, value):
        self.__kwhstored = value

    @property
    def kwrated(self):
        return self.__kwrated

    @kwrated.setter
    def kwrated(self, value):
        self.__kwrated = value

    @property
    def limitcurrent(self):
        return self.__limitcurrent

    @limitcurrent.setter
    def limitcurrent(self, value):
        self.__limitcurrent = value

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        self.__model = value

    @property
    def pf(self):
        return self.__pf

    @pf.setter
    def pf(self, value):
        self.__pf = value

    @property
    def pfpriority(self):
        return self.__pfpriority

    @pfpriority.setter
    def pfpriority(self, value):
        self.__pfpriority = value

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value

    @property
    def timechargetrig(self):
        return self.__timechargetrig

    @timechargetrig.setter
    def timechargetrig(self, value):
        self.__timechargetrig = value

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
    def varfollowinverter(self):
        return self.__varfollowinverter

    @varfollowinverter.setter
    def varfollowinverter(self, value):
        self.__varfollowinverter = value

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
    def wattpriority(self):
        return self.__wattpriority

    @wattpriority.setter
    def wattpriority(self, value):
        self.__wattpriority = value

    @property
    def yearly(self):
        return self.__yearly

    @yearly.setter
    def yearly(self, value):
        self.__yearly = value
