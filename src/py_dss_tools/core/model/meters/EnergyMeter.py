# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:10:55
 Project: py_dss_tools [set, 2021]
"""


class EnergyMeter:
    name = "EnergyMeter"
    name_plural = "EnergyMeters"
    columns = ['3phaselosses', 'action', 'basefreq', 'caidi', 'custinterrupts', 'element', 'enabled', 'int_duration',
               'int_rate', 'kvaemerg', 'kvanormal', 'like', 'linelosses', 'localonly', 'losses', 'mask', 'option',
               'peakcurrent', 'phasevoltagereport', 'saidi', 'saifi', 'saifikw', 'seqlosses', 'terminal', 'vbaselosses',
               'xfmrlosses', 'zonelist']

    def __init__(self):
        self.__three_phaselosses = None
        self.__caidi = None
        self.__custinterrupts = None
        self.__int_duration = None
        self.__int_rate = None
        self.__kvaemerg = None
        self.__kvanormal = None
        self.__linelosses = None
        self.__localonly = None
        self.__losses = None
        self.__mask = None
        self.__option = None
        self.__peakcurrent = None
        self.__phasevoltagereport = None
        self.__saidi = None
        self.__saifi = None
        self.__saifikw = None
        self.__seqlosses = None
        self.__vbaselosses = None
        self.__xfmrlosses = None
        self.__zonelist = None

    @property
    def three_phaselosses(self):
        return self.__three_phaselosses

    @three_phaselosses.setter
    def three_phaselosses(self, value):
        self.__three_phaselosses = value

    @property
    def caidi(self):
        return self.__caidi

    @caidi.setter
    def caidi(self, value):
        self.__caidi = value

    @property
    def custinterrupts(self):
        return self.__custinterrupts

    @custinterrupts.setter
    def custinterrupts(self, value):
        self.__custinterrupts = value

    @property
    def int_duration(self):
        return self.__int_duration

    @int_duration.setter
    def int_duration(self, value):
        self.__int_duration = value

    @property
    def int_rate(self):
        return self.__int_rate

    @int_rate.setter
    def int_rate(self, value):
        self.__int_rate = value

    @property
    def kvaemerg(self):
        return self.__kvaemerg

    @kvaemerg.setter
    def kvaemerg(self, value):
        self.__kvaemerg = value

    @property
    def kvanormal(self):
        return self.__kvanormal

    @kvanormal.setter
    def kvanormal(self, value):
        self.__kvanormal = value

    @property
    def linelosses(self):
        return self.__linelosses

    @linelosses.setter
    def linelosses(self, value):
        self.__linelosses = value

    @property
    def localonly(self):
        return self.__localonly

    @localonly.setter
    def localonly(self, value):
        self.__localonly = value

    @property
    def losses(self):
        return self.__losses

    @losses.setter
    def losses(self, value):
        self.__losses = value

    @property
    def mask(self):
        return self.__mask

    @mask.setter
    def mask(self, value):
        self.__mask = value

    @property
    def option(self):
        return self.__option

    @option.setter
    def option(self, value):
        self.__option = value

    @property
    def peakcurrent(self):
        return self.__peakcurrent

    @peakcurrent.setter
    def peakcurrent(self, value):
        self.__peakcurrent = value

    @property
    def phasevoltagereport(self):
        return self.__phasevoltagereport

    @phasevoltagereport.setter
    def phasevoltagereport(self, value):
        self.__phasevoltagereport = value

    @property
    def saidi(self):
        return self.__saidi

    @saidi.setter
    def saidi(self, value):
        self.__saidi = value

    @property
    def saifi(self):
        return self.__saifi

    @saifi.setter
    def saifi(self, value):
        self.__saifi = value

    @property
    def saifikw(self):
        return self.__saifikw

    @saifikw.setter
    def saifikw(self, value):
        self.__saifikw = value

    @property
    def seqlosses(self):
        return self.__seqlosses

    @seqlosses.setter
    def seqlosses(self, value):
        self.__seqlosses = value

    @property
    def vbaselosses(self):
        return self.__vbaselosses

    @vbaselosses.setter
    def vbaselosses(self, value):
        self.__vbaselosses = value

    @property
    def xfmrlosses(self):
        return self.__xfmrlosses

    @xfmrlosses.setter
    def xfmrlosses(self, value):
        self.__xfmrlosses = value

    @property
    def zonelist(self):
        return self.__zonelist

    @zonelist.setter
    def zonelist(self, value):
        self.__zonelist = value
