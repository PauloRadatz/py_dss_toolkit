# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:06:32
 Project: py_dss_tools [set, 2021]
"""


class RegControl:
    name = "RegControl"
    name_plural = "RegControls"
    columns = ['band', 'basefreq', 'bus', 'cogen', 'ctprim', 'debugtrace', 'delay', 'enabled', 'eventlog',
               'inversetime', 'ldc_z', 'like', 'maxtapchange', 'ptphase', 'ptratio', 'r', 'remoteptratio', 'reset',
               'rev_z', 'revband', 'revdelay', 'reversible', 'revneutral', 'revr', 'revthreshold', 'revvreg', 'revx',
               'tapdelay', 'tapnum', 'tapwinding', 'transformer', 'vlimit', 'vreg', 'winding', 'x']

    def __init__(self):
        self.__action = None
        self.__delay = None
        self.__grounddelayed = None
        self.__groundfast = None
        self.__groundinst = None
        self.__groundtrip = None
        self.__monitoredobj = None
        self.__monitoredterm = None
        self.__numfast = None
        self.__phasedelayed = None
        self.__phasefast = None
        self.__phaseinst = None
        self.__phasetrip = None
        self.__recloseintervals = None
        self.__reset = None
        self.__shots = None
        self.__switchedobj = None
        self.__switchedterm = None
        self.__tdgrdelayed = None
        self.__tdgrfast = None
        self.__tdphdelayed = None
        self.__tdphfast = None

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, value):
        self.__action = value

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, value):
        self.__delay = value

    @property
    def grounddelayed(self):
        return self.__grounddelayed

    @grounddelayed.setter
    def grounddelayed(self, value):
        self.__grounddelayed = value

    @property
    def groundfast(self):
        return self.__groundfast

    @groundfast.setter
    def groundfast(self, value):
        self.__groundfast = value

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
    def numfast(self):
        return self.__numfast

    @numfast.setter
    def numfast(self, value):
        self.__numfast = value

    @property
    def phasedelayed(self):
        return self.__phasedelayed

    @phasedelayed.setter
    def phasedelayed(self, value):
        self.__phasedelayed = value

    @property
    def phasefast(self):
        return self.__phasefast

    @phasefast.setter
    def phasefast(self, value):
        self.__phasefast = value

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
    def tdgrdelayed(self):
        return self.__tdgrdelayed

    @tdgrdelayed.setter
    def tdgrdelayed(self, value):
        self.__tdgrdelayed = value

    @property
    def tdgrfast(self):
        return self.__tdgrfast

    @tdgrfast.setter
    def tdgrfast(self, value):
        self.__tdgrfast = value

    @property
    def tdphdelayed(self):
        return self.__tdphdelayed

    @tdphdelayed.setter
    def tdphdelayed(self, value):
        self.__tdphdelayed = value

    @property
    def tdphfast(self):
        return self.__tdphfast

    @tdphfast.setter
    def tdphfast(self, value):
        self.__tdphfast = value
