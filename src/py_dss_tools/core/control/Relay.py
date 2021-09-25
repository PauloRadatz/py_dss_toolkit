# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:06:39
 Project: py_dss_tools [set, 2021]
"""


class Relay:
    name = "Relay"
    name_plural = "Relays"
    columns = ['46%pickup', '46baseamps', '46isqt', '47%pickup', 'action', 'basefreq', 'breakertime', 'delay',
               'enabled', 'groundcurve', 'groundinst', 'groundtrip', 'kvbase', 'like', 'monitoredobj', 'monitoredterm',
               'overtrip', 'overvoltcurve', 'phasecurve', 'phaseinst', 'phasetrip', 'recloseintervals', 'reset',
               'shots', 'switchedobj', 'switchedterm', 'tdground', 'tdphase', 'type', 'undertrip', 'undervoltcurve',
               'variable']

    def __init__(self):
        self.__percent_46_pickup = None
        self.__baseamps_46 = None
        self.__isqt_46 = None
        self.__percent_47_pickup = None
        self.__action = None
        self.__breakertime = None
        self.__delay = None
        self.__groundcurve = None
        self.__groundinst = None
        self.__groundtrip = None
        self.__kvbase = None
        self.__monitoredobj = None
        self.__monitoredterm = None
        self.__overtrip = None
        self.__overvoltcurve = None
        self.__phasecurve = None
        self.__phaseinst = None
        self.__phasetrip = None
        self.__recloseintervals = None
        self.__reset = None
        self.__shots = None
        self.__switchedobj = None
        self.__switchedterm = None
        self.__tdground = None
        self.__tdphase = None
        self.__type = None
        self.__undertrip = None
        self.__undervoltcurve = None
        self.__variable = None

    @property
    def percent_46_pickup(self):
        return self.__percent_46_pickup

    @percent_46_pickup.setter
    def percent_46_pickup(self, value):
        self.__percent_46_pickup = value

    @property
    def baseamps_46(self):
        return self.__baseamps_46

    @baseamps_46.setter
    def baseamps_46(self, value):
        self.__baseamps_46 = value

    @property
    def isqt_46(self):
        return self.__isqt_46

    @isqt_46.setter
    def isqt_46(self, value):
        self.__isqt_46 = value

    @property
    def percent_47_pickup(self):
        return self.__percent_47_pickup

    @percent_47_pickup.setter
    def percent_47_pickup(self, value):
        self.__percent_47_pickup = value

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, value):
        self.__action = value

    @property
    def breakertime(self):
        return self.__breakertime

    @breakertime.setter
    def breakertime(self, value):
        self.__breakertime = value

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, value):
        self.__delay = value

    @property
    def groundcurve(self):
        return self.__groundcurve

    @groundcurve.setter
    def groundcurve(self, value):
        self.__groundcurve = value

    @property
    def groundinst(self):
        return self.__groundinst

    @groundinst.setter
    def groundinst(self, value):
        self.__groundinst = value

    @property
    def groundtrip(self):
        return self.__groundtrip

    @groundtrip.setter
    def groundtrip(self, value):
        self.__groundtrip = value

    @property
    def kvbase(self):
        return self.__kvbase

    @kvbase.setter
    def kvbase(self, value):
        self.__kvbase = value

    @property
    def monitoredobj(self):
        return self.__monitoredobj

    @monitoredobj.setter
    def monitoredobj(self, value):
        self.__monitoredobj = value

    @property
    def monitoredterm(self):
        return self.__monitoredterm

    @monitoredterm.setter
    def monitoredterm(self, value):
        self.__monitoredterm = value

    @property
    def overtrip(self):
        return self.__overtrip

    @overtrip.setter
    def overtrip(self, value):
        self.__overtrip = value

    @property
    def overvoltcurve(self):
        return self.__overvoltcurve

    @overvoltcurve.setter
    def overvoltcurve(self, value):
        self.__overvoltcurve = value

    @property
    def phasecurve(self):
        return self.__phasecurve

    @phasecurve.setter
    def phasecurve(self, value):
        self.__phasecurve = value

    @property
    def phaseinst(self):
        return self.__phaseinst

    @phaseinst.setter
    def phaseinst(self, value):
        self.__phaseinst = value

    @property
    def phasetrip(self):
        return self.__phasetrip

    @phasetrip.setter
    def phasetrip(self, value):
        self.__phasetrip = value

    @property
    def recloseintervals(self):
        return self.__recloseintervals

    @recloseintervals.setter
    def recloseintervals(self, value):
        self.__recloseintervals = value

    @property
    def reset(self):
        return self.__reset

    @reset.setter
    def reset(self, value):
        self.__reset = value

    @property
    def shots(self):
        return self.__shots

    @shots.setter
    def shots(self, value):
        self.__shots = value

    @property
    def switchedobj(self):
        return self.__switchedobj

    @switchedobj.setter
    def switchedobj(self, value):
        self.__switchedobj = value

    @property
    def switchedterm(self):
        return self.__switchedterm

    @switchedterm.setter
    def switchedterm(self, value):
        self.__switchedterm = value

    @property
    def tdground(self):
        return self.__tdground

    @tdground.setter
    def tdground(self, value):
        self.__tdground = value

    @property
    def tdphase(self):
        return self.__tdphase

    @tdphase.setter
    def tdphase(self, value):
        self.__tdphase = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def undertrip(self):
        return self.__undertrip

    @undertrip.setter
    def undertrip(self, value):
        self.__undertrip = value

    @property
    def undervoltcurve(self):
        return self.__undervoltcurve

    @undervoltcurve.setter
    def undervoltcurve(self, value):
        self.__undervoltcurve = value

    @property
    def variable(self):
        return self.__variable

    @variable.setter
    def variable(self, value):
        self.__variable = value
