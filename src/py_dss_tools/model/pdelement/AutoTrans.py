# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:04:23
 Project: py_dss_tools [set, 2021]
"""
from dataclasses import dataclass

from py_dss_tools.model.pdelement import PDElement


@dataclass
class AutoTrans(PDElement):
    title = "AutoTrans"
    plural_title = "AutoTrans"
    columns_ = ['porcentagem_imag', 'porcentagem_loadloss', 'porcentagem_noloadloss', 'porcentagem_r', 'porcentagem_rs',
                'bank', 'basefreq', 'bus', 'buses', 'conn', 'conns', 'core', 'emergamps', 'emerghkva', 'enabled',
                'faultrate', 'flrise', 'hsrise', 'kv', 'kva', 'kvas', 'kvs', 'leadlag', 'like', 'm', 'maxtap', 'mintap',
                'n', 'normamps', 'normhkva', 'numtaps', 'pctperm', 'phases', 'ppm_antifloat', 'rdcohms', 'repair',
                'sub', 'subname', 'tap', 'taps', 'thermal', 'wdg', 'wdgcurrents', 'windings', 'xfmrcode', 'xht', 'xhx',
                'xrconst', 'xscarray', 'xxt']

    _porcentagem_imag: float = 0
    _porcentagem_loadloss: float = 0.4
    _porcentagem_noloadloss: float = 0
    _porcentagem_r: float = 0.2
    _porcentagem_rs: str = ''
    _bank: str = ''
    _bus: str = ''
    _buses: str = ''
    _conn: str = 'Series'
    _conns: str = 'Series'
    _core: str = 'shell'
    _emerghkva: float = 1500
    _flrise: float = 65
    _hsrise: float = 15
    _kv: float = 115
    _kva: float = 1000
    _kvas: str = '1000'
    _kvs: str = '115'
    _leadlag: str = 'Lag'
    _m: float = .8
    _maxtap: float = 1.1
    _mintap: float = 0.9
    _n: float = 0.8
    _normhkva: float = 1100
    _numtaps: int = 32
    _ppm_antifloat: int = 1
    _rdcohms: float = None
    _sub: str = 'n'
    _subname: str = ''
    _tap: float = 1
    _taps: str = '1'
    _thermal: float = 2
    _wdg: float = 1
    _wdgcurrents: str = ''
    _windings: int = 2
    _xfmrcode: str = ''
    _xht: float = 35
    _xhx: float = 10
    _xrconst: str = 'NO'
    _xscarray: str = '10'
    _xxt: float = 30

    def _post_init_(self):
        self._name = 'my_auto_trans_'

    @property
    def emergamps(self):
        return NotImplementedError

    @property
    def enabled(self):
        return NotImplementedError

    @property
    def faultrate(self):
        return NotImplementedError

    @property
    def like(self):
        return NotImplementedError

    @property
    def name(self):
        return NotImplementedError

    @property
    def normamps(self):
        return NotImplementedError

    @property
    def pctperm(self):
        return NotImplementedError

    @property
    def phases(self):
        return NotImplementedError

    @property
    def repair(self):
        return NotImplementedError

    @property
    def imag(self):
        return self._porcentagem_imag

    @imag.setter
    def imag(self, value):
        self._porcentagem_imag = value

    @property
    def loadloss(self):
        return self._porcentagem_loadloss

    @loadloss.setter
    def loadloss(self, value):
        self._porcentagem_loadloss = value

    @property
    def noloadloss(self):
        return self._porcentagem_noloadloss

    @noloadloss.setter
    def noloadloss(self, value):
        self._porcentagem_noloadloss = value

    @property
    def r(self):
        return self._porcentagem_r

    @r.setter
    def r(self, value):
        self._porcentagem_r = value

    @property
    def rs(self):
        return self._porcentagem_rs

    @rs.setter
    def rs(self, value):
        self._porcentagem_rs = value

    @property
    def bank(self):
        return self._bank

    @bank.setter
    def bank(self, value):
        self._bank = value

    @property
    def bus(self):
        return self._bus

    @bus.setter
    def bus(self, value):
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
    def ppm_antifloat(self):
        return self._ppm_antifloat

    @ppm_antifloat.setter
    def ppm_antifloat(self, value):
        self._ppm_antifloat = value

    @property
    def rdcohms(self):
        return self._rdcohms

    @rdcohms.setter
    def rdcohms(self, value):
        self._rdcohms = value

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
    def windings(self, value):
        self._windings = value

    @property
    def xfmrcode(self):
        return self._xfmrcode

    @xfmrcode.setter
    def xfmrcode(self, value):
        self._xfmrcode = value

    @property
    def xht(self):
        return self._xht

    @xht.setter
    def xht(self, value):
        self._xht = value

    @property
    def xhx(self):
        return self._xhx

    @xhx.setter
    def xhx(self, value):
        self._xhx = value

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

    @property
    def xxt(self):
        return self._xxt

    @xxt.setter
    def xxt(self, value):
        self._xxt = value
