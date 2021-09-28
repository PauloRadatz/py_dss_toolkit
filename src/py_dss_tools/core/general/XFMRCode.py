# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:10:15
 Project: py_dss_tools [set, 2021]
"""


class XFMRCode:
    name = "XFMRCode"
    name_plural = "XFMRCodes"
    columns = ['%imag', '%loadloss', '%noloadloss', '%r', '%rs', 'conn', 'conns', 'emerghkva', 'flrise', 'hsrise', 'kv',
               'kva', 'kvas', 'kvs', 'like', 'm', 'maxtap', 'mintap', 'n', 'normhkva', 'numtaps', 'phases',
               'ppm_antifloat', 'ratings', 'rdcohms', 'rneut', 'seasons', 'tap', 'taps', 'thermal', 'wdg', 'windings',
               'x12', 'x13', 'x23', 'xhl', 'xht', 'xlt', 'xneut', 'xscarray']

    def __init__(self):
        self.__percent_imag = None
        self.__percent_loadloss = None
        self.__percent_noloadloss = None
        self.__percent_r = None
        self.__percent_rs = None
        self.__conn = None
        self.__conns = None
        self.__emerghkva = None
        self.__flrise = None
        self.__hsrise = None
        self.__kv = None
        self.__kva = None
        self.__kvas = None
        self.__kvs = None
        self.__m = None
        self.__maxtap = None
        self.__mintap = None
        self.__n = None
        self.__normhkva = None
        self.__numtaps = None
        self.__phases = None
        self.__ppm_antifloat = None
        self.__ratings = None
        self.__rdcohms = None
        self.__rneut = None
        self.__seasons = None
        self.__tap = None
        self.__taps = None
        self.__thermal = None
        self.__wdg = None
        self.__windings = None
        self.__x12 = None
        self.__x13 = None
        self.__x23 = None
        self.__xhl = None
        self.__xht = None
        self.__xlt = None
        self.__xneut = None
        self.__xscarray = None

    @property
    def percent_imag(self):
        return self.__percent_imag

    @percent_imag.setter
    def percent_imag(self, value):
        self.__percent_imag = value

    @property
    def percent_loadloss(self):
        return self.__percent_loadloss

    @percent_loadloss.setter
    def percent_loadloss(self, value):
        self.__percent_loadloss = value

    @property
    def percent_noloadloss(self):
        return self.__percent_noloadloss

    @percent_noloadloss.setter
    def percent_noloadloss(self, value):
        self.__percent_noloadloss = value

    @property
    def percent_r(self):
        return self.__percent_r

    @percent_r.setter
    def percent_r(self, value):
        self.__percent_r = value

    @property
    def percent_rs(self):
        return self.__percent_rs

    @percent_rs.setter
    def percent_rs(self, value):
        self.__percent_rs = value

    @property
    def conn(self):
        return self.__conn

    @conn.setter
    def conn(self, value):
        self.__conn = value

    @property
    def conns(self):
        return self.__conns

    @conns.setter
    def conns(self, value):
        self.__conns = value

    @property
    def emerghkva(self):
        return self.__emerghkva

    @emerghkva.setter
    def emerghkva(self, value):
        self.__emerghkva = value

    @property
    def flrise(self):
        return self.__flrise

    @flrise.setter
    def flrise(self, value):
        self.__flrise = value

    @property
    def hsrise(self):
        return self.__hsrise

    @hsrise.setter
    def hsrise(self, value):
        self.__hsrise = value

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
    def kvas(self):
        return self.__kvas

    @kvas.setter
    def kvas(self, value):
        self.__kvas = value

    @property
    def kvs(self):
        return self.__kvs

    @kvs.setter
    def kvs(self, value):
        self.__kvs = value

    @property
    def m(self):
        return self.__m

    @m.setter
    def m(self, value):
        self.__m = value

    @property
    def maxtap(self):
        return self.__maxtap

    @maxtap.setter
    def maxtap(self, value):
        self.__maxtap = value

    @property
    def mintap(self):
        return self.__mintap

    @mintap.setter
    def mintap(self, value):
        self.__mintap = value

    @property
    def n(self):
        return self.__n

    @n.setter
    def n(self, value):
        self.__n = value

    @property
    def normhkva(self):
        return self.__normhkva

    @normhkva.setter
    def normhkva(self, value):
        self.__normhkva = value

    @property
    def numtaps(self):
        return self.__numtaps

    @numtaps.setter
    def numtaps(self, value):
        self.__numtaps = value

    @property
    def phases(self):
        return self.__phases

    @phases.setter
    def phases(self, value):
        self.__phases = value

    @property
    def ppm_antifloat(self):
        return self.__ppm_antifloat

    @ppm_antifloat.setter
    def ppm_antifloat(self, value):
        self.__ppm_antifloat = value

    @property
    def ratings(self):
        return self.__ratings

    @ratings.setter
    def ratings(self, value):
        self.__ratings = value

    @property
    def rdcohms(self):
        return self.__rdcohms

    @rdcohms.setter
    def rdcohms(self, value):
        self.__rdcohms = value

    @property
    def rneut(self):
        return self.__rneut

    @rneut.setter
    def rneut(self, value):
        self.__rneut = value

    @property
    def seasons(self):
        return self.__seasons

    @seasons.setter
    def seasons(self, value):
        self.__seasons = value

    @property
    def tap(self):
        return self.__tap

    @tap.setter
    def tap(self, value):
        self.__tap = value

    @property
    def taps(self):
        return self.__taps

    @taps.setter
    def taps(self, value):
        self.__taps = value

    @property
    def thermal(self):
        return self.__thermal

    @thermal.setter
    def thermal(self, value):
        self.__thermal = value

    @property
    def wdg(self):
        return self.__wdg

    @wdg.setter
    def wdg(self, value):
        self.__wdg = value

    @property
    def windings(self):
        return self.__windings

    @windings.setter
    def windings(self, value):
        self.__windings = value

    @property
    def x12(self):
        return self.__x12

    @x12.setter
    def x12(self, value):
        self.__x12 = value

    @property
    def x13(self):
        return self.__x13

    @x13.setter
    def x13(self, value):
        self.__x13 = value

    @property
    def x23(self):
        return self.__x23

    @x23.setter
    def x23(self, value):
        self.__x23 = value

    @property
    def xhl(self):
        return self.__xhl

    @xhl.setter
    def xhl(self, value):
        self.__xhl = value

    @property
    def xht(self):
        return self.__xht

    @xht.setter
    def xht(self, value):
        self.__xht = value

    @property
    def xlt(self):
        return self.__xlt

    @xlt.setter
    def xlt(self, value):
        self.__xlt = value

    @property
    def xneut(self):
        return self.__xneut

    @xneut.setter
    def xneut(self, value):
        self.__xneut = value

    @property
    def xscarray(self):
        return self.__xscarray

    @xscarray.setter
    def xscarray(self, value):
        self.__xscarray = value
