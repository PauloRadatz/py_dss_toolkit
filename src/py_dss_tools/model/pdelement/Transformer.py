# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 04/09/2021 at 20:37:43
 Project: py_dss_tools [set, 2021]
"""
from py_dss_tools.model.pdelement import PDElement


class Transformer(PDElement):
    name = "Transformer"
    name_plural = "Transformer"
    columns = ['%imag', '%loadloss', '%noloadloss', '%r', '%rs', 'bank', 'basefreq', 'bus', 'buses', 'conn',
               'conns', 'core', 'emergamps', 'emerghkva', 'enabled', 'faultrate', 'flrise', 'hsrise', 'kv', 'kva',
               'kvas', 'kvs', 'leadlag', 'like', 'm', 'maxtap', 'mintap', 'n', 'normamps', 'normhkva', 'numtaps',
               'pctperm', 'phases', 'ppm_antifloat', 'ratings', 'rdcohms', 'repair', 'rneut', 'seasons', 'sub',
               'subname', 'tap', 'taps', 'thermal', 'wdg', 'wdgcurrents', 'windings', 'x12', 'x13', 'x23',
               'xfmrcode', 'xhl', 'xht', 'xlt', 'xneut', 'xrconst', 'xscarray']

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
        self.__ratings = None
        self.__rdcohms = None
        self.__rneut = None
        self.__seasons = None
        self.__sub = None
        self.__subname = None
        self.__tap = None
        self.__taps = None
        self.__thermal = None
        self.__wdg = None
        self.__wdgcurrents = None
        self.__windings = None
        self.__x12 = None
        self.__x13 = None
        self.__x23 = None
        self.__xfmrcode = None
        self.__xhl = None
        self.__xht = None
        self.__xlt = None
        self.__xneut = None
        self.__xrconst = None
        self.__xscarray = None

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
    def xfmrcode(self):
        return self.__xfmrcode

    @xfmrcode.setter
    def xfmrcode(self, value):
        self.__xfmrcode = value

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

    # @property
    # def name_(self):
    #     return self.name
    #
    # @name_.setter
    # def name_(self, value: str):
    #     self.name_ = str(value)
    #
    # @staticmethod
    # def new(self, **kwargs):
    #     value = str
    #     if '_name' in kwargs:
    #         self.name_ = kwargs.get('_name')
    #     # circuit.dss.text(
    #     #     f"New Transformer.{self.name_} phases=3 windings=2 buses=(684, 680) Conns=(Wye, Wye) kVs=(4.16,4.16) "
    #     #     "kVAs=(5000, 5000) %loadloss=2 xhl=4")
    #
    # def __str__(self):
    #     print(f"{str(self.id)} - {self.name}")
