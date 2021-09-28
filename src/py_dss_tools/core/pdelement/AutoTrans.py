# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:04:23
 Project: py_dss_tools [set, 2021]
"""
from .PDElement import PDElement


class AutoTrans(PDElement):
    name = "AutoTrans"
    name_plural = "AutoTrans"
    columns = ['%imag', '%loadloss', '%noloadloss', '%r', '%rs', 'bank', 'basefreq', 'bus', 'buses', 'conn', 'conns',
               'core', 'emergamps', 'emerghkva', 'enabled', 'faultrate', 'flrise', 'hsrise', 'kv', 'kva', 'kvas', 'kvs',
               'leadlag', 'like', 'm', 'maxtap', 'mintap', 'n', 'normamps', 'normhkva', 'numtaps', 'pctperm', 'phases',
               'ppm_antifloat', 'rdcohms', 'repair', 'sub', 'subname', 'tap', 'taps', 'thermal', 'wdg', 'wdgcurrents',
               'windings', 'xfmrcode', 'xht', 'xhx', 'xrconst', 'xscarray', 'xxt']

    def __init__(self):
        super().__init__()
        self.__imag = None
        self.__loadloss = None
        self.__noloadloss = None
        self.__r = None
        self.__rs = None
        self.__bank = None
        self.__bus = None
        self.__buses = None
        self.__conn = None
        self.__conns = None
        self.__core = None
        self.__emerghkva = None
        self.__flrise = None
        self.__hsrise = None
        self.__kv = None
        self.__kva = None
        self.__kvas = None
        self.__kvs = None
        self.__leadlag = None
        self.__m = None
        self.__maxtap = None
        self.__mintap = None
        self.__n = None
        self.__normhkva = None
        self.__numtaps = None
        self.__ppm_antifloat = None
        self.__rdcohms = None
        self.__sub = None
        self.__subname = None
        self.__tap = None
        self.__taps = None
        self.__thermal = None
        self.__wdg = None
        self.__wdgcurrents = None
        self.__windings = None
        self.__xfmrcode = None
        self.__xht = None
        self.__xhx = None
        self.__xrconst = None
        self.__xscarray = None
        self.__xxt = None

    @property
    def imag(self):
        return self.__imag

    @imag.setter
    def imag(self, value):
        self.__imag = value

    @property
    def loadloss(self):
        return self.__loadloss

    @loadloss.setter
    def loadloss(self, value):
        self.__loadloss = value

    @property
    def noloadloss(self):
        return self.__noloadloss

    @noloadloss.setter
    def noloadloss(self, value):
        self.__noloadloss = value

    @property
    def r(self):
        return self.__r

    @r.setter
    def r(self, value):
        self.__r = value

    @property
    def rs(self):
        return self.__rs

    @rs.setter
    def rs(self, value):
        self.__rs = value

    @property
    def bank(self):
        return self.__bank

    @bank.setter
    def bank(self, value):
        self.__bank = value

    @property
    def bus(self):
        return self.__bus

    @bus.setter
    def bus(self, value):
        self.__bus = value

    @property
    def buses(self):
        return self.__buses

    @buses.setter
    def buses(self, value):
        self.__buses = value

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
    def core(self):
        return self.__core

    @core.setter
    def core(self, value):
        self.__core = value

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
    def leadlag(self):
        return self.__leadlag

    @leadlag.setter
    def leadlag(self, value):
        self.__leadlag = value

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
    def ppm_antifloat(self):
        return self.__ppm_antifloat

    @ppm_antifloat.setter
    def ppm_antifloat(self, value):
        self.__ppm_antifloat = value

    @property
    def rdcohms(self):
        return self.__rdcohms

    @rdcohms.setter
    def rdcohms(self, value):
        self.__rdcohms = value

    @property
    def sub(self):
        return self.__sub

    @sub.setter
    def sub(self, value):
        self.__sub = value

    @property
    def subname(self):
        return self.__subname

    @subname.setter
    def subname(self, value):
        self.__subname = value

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
    def wdgcurrents(self):
        return self.__wdgcurrents

    @wdgcurrents.setter
    def wdgcurrents(self, value):
        self.__wdgcurrents = value

    @property
    def windings(self):
        return self.__windings

    @windings.setter
    def windings(self, value):
        self.__windings = value

    @property
    def xfmrcode(self):
        return self.__xfmrcode

    @xfmrcode.setter
    def xfmrcode(self, value):
        self.__xfmrcode = value

    @property
    def xht(self):
        return self.__xht

    @xht.setter
    def xht(self, value):
        self.__xht = value

    @property
    def xhx(self):
        return self.__xhx

    @xhx.setter
    def xhx(self, value):
        self.__xhx = value

    @property
    def xrconst(self):
        return self.__xrconst

    @xrconst.setter
    def xrconst(self, value):
        self.__xrconst = value

    @property
    def xscarray(self):
        return self.__xscarray

    @xscarray.setter
    def xscarray(self, value):
        self.__xscarray = value

    @property
    def xxt(self):
        return self.__xxt

    @xxt.setter
    def xxt(self, value):
        self.__xxt = value
