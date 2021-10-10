# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 03/09/2021 at 17:43:57
 Project: py_dss_tools [set, 2021]
"""
from .PCElement import PCElement


class PVSystem(PCElement):
    name = "PCSystem"
    name_plural = "PVSystems"
    columns = ['%cutin', '%cutout', '%pminkvarmax', '%pminnovars', '%pmpp', '%r', '%x', 'balanced', 'basefreq', 'bus1',
               'class', 'conn', 'daily', 'debugtrace', 'duty', 'dutystart', 'effcurve', 'enabled', 'irradiance', 'kv',
               'kva', 'kvar', 'kvarmax', 'kvarmaxabs', 'like', 'limitcurrent', 'model', 'pf', 'pfpriority', 'phases',
               'pmpp', 'p-tcurve', 'spectrum', 'tdaily', 'tduty', 'temperature', 'tyearly', 'userdata', 'usermodel',
               'varfollowinverter', 'vmaxpu', 'vminpu', 'wattpriority', 'yearly']

    def __init__(self):
        super().__init__()
        self.__percent_cutin = None
        self.__percent_cutout = None
        self.__percent_pminkvarmax = None
        self.__percent_pminnovars = None
        self.__percent_pmpp = None
        self.__percent_r = None
        self.__percent_x = None
        self.__balanced = None
        self.__class_ = None
        self.__conn = None
        self.__daily = None
        self.__debugtrace = None
        self.__duty = None
        self.__dutystart = None
        self.__effcurve = None
        self.__irradiance = None
        self.__kv = None
        self.__kva = None
        self.__kvar = None
        self.__kvarmax = None
        self.__kvarmaxabs = None
        self.__limitcurrent = None
        self.__model = None
        self.__pf = None
        self.__pfpriority = None
        self.__pmpp = None
        self.__ptcurve = None
        self.__tdaily = None
        self.__tduty = None
        self.__temperature = None
        self.__tyearly = None
        self.__userdata = None
        self.__usermodel = None
        self.__varfollowinverter = None
        self.__vmaxpu = None
        self.__vminpu = None
        self.__wattpriority = None
        self.__yearly = None

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
    def percent_pmpp(self):
        return self.__percent_pmpp

    @percent_pmpp.setter
    def percent_pmpp(self, value):
        self.__percent_pmpp = value

    @property
    def percent_r(self):
        return self.__percent_r

    @percent_r.setter
    def percent_r(self, value):
        self.__percent_r = value

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
    def effcurve(self):
        return self.__effcurve

    @effcurve.setter
    def effcurve(self, value):
        self.__effcurve = value

    @property
    def irradiance(self):
        return self.__irradiance

    @irradiance.setter
    def irradiance(self, value):
        self.__irradiance = value

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
    def pmpp(self):
        return self.__pmpp

    @pmpp.setter
    def pmpp(self, value):
        self.__pmpp = value

    @property
    def ptcurve(self):
        return self.__ptcurve

    @ptcurve.setter
    def ptcurve(self, value):
        self.__ptcurve = value

    @property
    def tdaily(self):
        return self.__tdaily

    @tdaily.setter
    def tdaily(self, value):
        self.__tdaily = value

    @property
    def tduty(self):
        return self.__tduty

    @tduty.setter
    def tduty(self, value):
        self.__tduty = value

    @property
    def temperature(self):
        return self.__temperature

    @temperature.setter
    def temperature(self, value):
        self.__temperature = value

    @property
    def tyearly(self):
        return self.__tyearly

    @tyearly.setter
    def tyearly(self, value):
        self.__tyearly = value

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
