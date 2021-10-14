# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 04/09/2021 at 20:37:43
 Project: py_dss_tools [set, 2021]
"""
import attr
import pandas as pd

from py_dss_tools.model.pdelement import PDElement
from py_dss_tools.utils import Utils


@attr.s(kw_only=True)
class Transformer(PDElement):
    title_ = "Transformer"
    plural_title_ = "Transformers"
    columns_ = ['_percentageimag', '_percentageloadloss', '_percentagenoloadloss', '_percentager',
                '_percentagers', '_bank', '_basefreq', '_bus', '_buses', '_conn', '_conns', '_core', '_emergamps',
                '_emerghkva', '_enabled', '_faultrate', '_flrise', '_hsrise', '_kv', '_kva', '_kvas', '_kvs',
                '_leadlag', '_like', '_m', '_maxtap', '_mintap', '_n', '_name', '_normamps', '_normhkva', '_numtaps',
                '_pctperm', '_phases', '_ppmantifloat', '_ratings', '_rdcohms', '_repair', '_rneut', '_seasons', '_sub',
                '_subname', '_tap', '_taps', '_thermal', '_wdg', '_wdgcurrents', '_windings', '_x12', '_x13', '_x23',
                '_xfmrcode', '_xhl', '_xht', '_xlt', '_xneut', '_xrconst', '_xscarray']

    _percentageimag = attr.ib(validator=attr.validators.instance_of((int, float)), default=0)
    _percentageloadloss = attr.ib(validator=attr.validators.instance_of((int, float)), default=0.4)
    _percentagenoloadloss = attr.ib(validator=attr.validators.instance_of((int, float)), default=0)
    _percentager = attr.ib(validator=attr.validators.instance_of((int, float)), default=0.2)
    _percentagers = attr.ib(validator=attr.validators.instance_of(str), default='[0.2, 0.2]')
    _bank = attr.ib(validator=attr.validators.instance_of(str), default='')
    _bus = attr.ib(validator=attr.validators.instance_of(str), default='')
    _buses = attr.ib(validator=attr.validators.instance_of(str), default='[]')
    _conn = attr.ib(validator=attr.validators.instance_of(str), default='wye')
    _conns = attr.ib(validator=attr.validators.instance_of(str), default='[wye, wye]')
    _core = attr.ib(validator=attr.validators.instance_of(str), default='shell')
    _emerghkva = attr.ib(validator=attr.validators.instance_of((int, float)), default=1500)
    _flrise = attr.ib(validator=attr.validators.instance_of((int, float)), default=65)
    _hsrise = attr.ib(validator=attr.validators.instance_of((int, float)), default=15)
    _kv = attr.ib(validator=attr.validators.instance_of((int, float)), default=12.47)
    _kva = attr.ib(validator=attr.validators.instance_of((int, float)), default=1000)
    _kvas = attr.ib(validator=attr.validators.instance_of(str), default='[1000, 1000]')
    _kvs = attr.ib(validator=attr.validators.instance_of(str), default='[12.47, 12.47]')
    _leadlag = attr.ib(validator=attr.validators.instance_of(str), default='Lag')
    _m = attr.ib(validator=attr.validators.instance_of((int, float)), default=0.8)
    _maxtap = attr.ib(validator=attr.validators.instance_of((int, float)), default=1.1)
    _mintap = attr.ib(validator=attr.validators.instance_of((int, float)), default=0.9)
    _n = attr.ib(validator=attr.validators.instance_of((int, float)), default=0.8)
    _normhkva = attr.ib(validator=attr.validators.instance_of((int, float)), default=1100)
    _numtaps = attr.ib(validator=attr.validators.instance_of(int), default=32)
    _ppmantifloat = attr.ib(validator=attr.validators.instance_of((int, float)), default=1)
    _ratings = attr.ib(validator=attr.validators.instance_of(str), default='[1100,]')
    _rdcohms = attr.ib(validator=attr.validators.instance_of((int, float)), default=0.08811718)
    _rneut = attr.ib(validator=attr.validators.instance_of((int, float)), default=-1)
    _seasons = attr.ib(validator=attr.validators.instance_of((int, float)), default=1)
    _sub = attr.ib(validator=attr.validators.instance_of(str), default='n')
    _subname = attr.ib(validator=attr.validators.instance_of(str), default='')
    _tap = attr.ib(validator=attr.validators.instance_of((int, float)), default=1)
    _taps = attr.ib(validator=attr.validators.instance_of(str), default='[1, 1]')
    _thermal = attr.ib(validator=attr.validators.instance_of((int, float)), default=2)
    _wdg = attr.ib(validator=attr.validators.instance_of(int), default=1)
    _wdgcurrents = attr.ib(validator=attr.validators.instance_of(str), default='')
    _windings = attr.ib(validator=attr.validators.instance_of((int, float)), default=3)
    _x12 = attr.ib(validator=attr.validators.instance_of((int, float)), default=7)
    _x13 = attr.ib(validator=attr.validators.instance_of((int, float)), default=35)
    _x23 = attr.ib(validator=attr.validators.instance_of((int, float)), default=30)
    _xfmrcode = attr.ib(validator=attr.validators.instance_of(str), default='')
    _xhl = attr.ib(validator=attr.validators.instance_of((int, float)), default=7)
    _xht = attr.ib(validator=attr.validators.instance_of((int, float)), default=35)
    _xlt = attr.ib(validator=attr.validators.instance_of((int, float)), default=30)
    _xneut = attr.ib(validator=attr.validators.instance_of((int, float)), default=0)
    _xrconst = attr.ib(validator=attr.validators.instance_of(str), default='NO')
    _xscarray = attr.ib(validator=attr.validators.instance_of(str), default='[7,]')

    def __attrs_post_init__(self):
        if self._name != '':
            self._name = Utils.remove_blank_spaces(self._name)
        else:
            self._name = 'my_transformer_' + Utils.generate_random_string()

        if self._bus == '':
            self._bus = 'my_bus_' + Utils.generate_random_string()
        else:
            self._bus = Utils.remove_blank_spaces(self._bus.lower())

    def to_dataframe(self):
        return pd.DataFrame.from_records([self.__dict__])

    def to_dict(self):
        return self.__dict__

    def to_list(self):
        return list(self.__dict__)

    @property
    def basefreq(self) -> float:
        return self._basefreq

    @basefreq.setter
    def basefreq(self, value: [int, float]):
        Utils.check_instance(value, 'basefreq', ['int', 'float'])
        self._basefreq = value

    @property
    def emergamps(self):
        return self._emergamps

    @emergamps.setter
    def emergamps(self, value: [int, float]):
        Utils.check_instance(value, 'emergamps', ['int', 'float'], )
        self._emergamps = value

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value: str):
        Utils.check_instance(value, 'enabled', ['str'], )
        self._enabled = value

    @property
    def faultrate(self):
        return self._faultrate

    @faultrate.setter
    def faultrate(self, value: [int, float]):
        Utils.check_instance(value, 'faultrate', ['int', 'float'], )
        self._faultrate = value

    @property
    def like(self) -> str:
        return self._like

    @like.setter
    def like(self, value: str):
        Utils.check_instance(value, 'like', ['str'], )
        self._like = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        Utils.check_instance(value, 'name', ['str'], )
        self._name = Utils.remove_blank_spaces(value)

    @property
    def normamps(self):
        return self._normamps

    @normamps.setter
    def normamps(self, value: [int, float]):
        Utils.check_instance(value, 'normamps', ['int', 'float'], )
        self._normamps = value

    @property
    def pctperm(self) -> [int, float]:
        return self._pctperm

    @pctperm.setter
    def pctperm(self, value: [int, float]):
        Utils.check_instance(value, 'pctperm', ['int', 'float'], )
        self._pctperm = value

    @property
    def phases(self) -> int:
        return self._phases

    @phases.setter
    def phases(self, value: int):
        Utils.check_instance(value, 'phases', ['int'], )
        self._phases = value

    @property
    def repair(self) -> [int, float]:
        return self._repair

    @repair.setter
    def repair(self, value):
        Utils.check_instance(value, 'repair', ['int', 'float'], )
        self._repair = value

    @property
    def imag(self) -> [int, float]:
        return self._percentageimag

    @imag.setter
    def imag(self, value: [int, float]):
        self._percentageimag = value

    @property
    def loadloss(self) -> [int, float]:
        return self._percentageloadloss

    @loadloss.setter
    def loadloss(self, value: [int, float]):
        self._percentageloadloss = value

    @property
    def noloadloss(self) -> [int, float]:
        return self._percentagenoloadloss

    @noloadloss.setter
    def noloadloss(self, value: [int, float]):
        self._percentagenoloadloss = value

    @property
    def r(self) -> [int, float]:
        return self._percentager

    @r.setter
    def r(self, value: [int, float]):
        self._percentager = value

    @property
    def rs(self) -> str:
        return self._percentagers

    @rs.setter
    def rs(self, value: str):
        self._percentagers = value

    @property
    def bank(self) -> str:
        return self._bank

    @bank.setter
    def bank(self, value: str):
        self._bank = value

    @property
    def bus(self) -> str:
        return self._bus

    @bus.setter
    def bus(self, value: str):
        self._bus = value

    @property
    def buses(self):
        return self._buses

    @buses.setter
    def buses(self, value):
        self._buses = value

    @property
    def conn(self):
        return self._conn

    @conn.setter
    def conn(self, value):
        self._conn = value

    @property
    def conns(self):
        return self._conns

    @conns.setter
    def conns(self, value):
        self._conns = value

    @property
    def core(self):
        return self._core

    @core.setter
    def core(self, value):
        self._core = value

    @property
    def emerghkva(self):
        return self._emerghkva

    @emerghkva.setter
    def emerghkva(self, value):
        self._emerghkva = value

    @property
    def flrise(self):
        return self._flrise

    @flrise.setter
    def flrise(self, value):
        self._flrise = value

    @property
    def hsrise(self):
        return self._hsrise

    @hsrise.setter
    def hsrise(self, value):
        self._hsrise = value

    @property
    def kv(self):
        return self._kv

    @kv.setter
    def kv(self, value):
        self._kv = value

    @property
    def kva(self):
        return self._kva

    @kva.setter
    def kva(self, value):
        self._kva = value

    @property
    def kvas(self):
        return self._kvas

    @kvas.setter
    def kvas(self, value):
        self._kvas = value

    @property
    def kvs(self):
        return self._kvs

    @kvs.setter
    def kvs(self, value):
        self._kvs = value

    @property
    def leadlag(self):
        return self._leadlag

    @leadlag.setter
    def leadlag(self, value):
        self._leadlag = value

    @property
    def m(self):
        return self._m

    @m.setter
    def m(self, value):
        self._m = value

    @property
    def maxtap(self):
        return self._maxtap

    @maxtap.setter
    def maxtap(self, value):
        self._maxtap = value

    @property
    def mintap(self):
        return self._mintap

    @mintap.setter
    def mintap(self, value):
        self._mintap = value

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value):
        self._n = value

    @property
    def normhkva(self):
        return self._normhkva

    @normhkva.setter
    def normhkva(self, value):
        self._normhkva = value

    @property
    def numtaps(self):
        return self._numtaps

    @numtaps.setter
    def numtaps(self, value):
        self._numtaps = value

    @property
    def ppmantifloat(self):
        return self._ppmantifloat

    @ppmantifloat.setter
    def ppm_ntifloat(self, value):
        self._ppmantifloat = value

    @property
    def ratings(self):
        return self._ratings

    @ratings.setter
    def ratings(self, value):
        self._ratings = value

    @property
    def rdcohms(self):
        return self._rdcohms

    @rdcohms.setter
    def rdcohms(self, value):
        self._rdcohms = value

    @property
    def rneut(self):
        return self._rneut

    @rneut.setter
    def rneut(self, value):
        self._rneut = value

    @property
    def seasons(self):
        return self._seasons

    @seasons.setter
    def seasons(self, value):
        self._seasons = value

    @property
    def sub(self):
        return self._sub

    @sub.setter
    def sub(self, value):
        self._sub = value

    @property
    def subname(self):
        return self._subname

    @subname.setter
    def subname(self, value):
        self._subname = value

    @property
    def tap(self):
        return self._tap

    @tap.setter
    def tap(self, value):
        self._tap = value

    @property
    def taps(self):
        return self._taps

    @taps.setter
    def taps(self, value):
        self._taps = value

    @property
    def thermal(self):
        return self._thermal

    @thermal.setter
    def thermal(self, value):
        self._thermal = value

    @property
    def wdg(self):
        return self._wdg

    @wdg.setter
    def wdg(self, value):
        self._wdg = value

    @property
    def wdgcurrents(self):
        return self._wdgcurrents

    @wdgcurrents.setter
    def wdgcurrents(self, value):
        self._wdgcurrents = value

    @property
    def windings(self):
        return self._windings

    @windings.setter
    def windings(self, value: int):
        self._windings = value

    @property
    def x12(self):
        return self._x12

    @x12.setter
    def x12(self, value):
        self._x12 = value

    @property
    def x13(self):
        return self._x13

    @x13.setter
    def x13(self, value):
        self._x13 = value

    @property
    def x23(self):
        return self._x23

    @x23.setter
    def x23(self, value):
        self._x23 = value

    @property
    def xfmrcode(self):
        return self._xfmrcode

    @xfmrcode.setter
    def xfmrcode(self, value):
        self._xfmrcode = value

    @property
    def xhl(self):
        return self._xhl

    @xhl.setter
    def xhl(self, value):
        self._xhl = value

    @property
    def xht(self):
        return self._xht

    @xht.setter
    def xht(self, value):
        self._xht = value

    @property
    def xlt(self):
        return self._xlt

    @xlt.setter
    def xlt(self, value):
        self._xlt = value

    @property
    def xneut(self):
        return self._xneut

    @xneut.setter
    def xneut(self, value):
        self._xneut = value

    @property
    def xrconst(self):
        return self._xrconst

    @xrconst.setter
    def xrconst(self, value):
        self._xrconst = value

    @property
    def xscarray(self):
        return self._xscarray

    @xscarray.setter
    def xscarray(self, value):
        self._xscarray = value
