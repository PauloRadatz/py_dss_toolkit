# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:11:29
 Project: py_dss_tools [set, 2021]
"""
from dataclasses import dataclass

from .OtherElement import OtherElement
from ...utils import Utils


@dataclass
class Fault(OtherElement):
    """
    _percentage_stddev: percentage standard deviation in resistance to assume for Monte Carlo fault (MF) solution
    mode for GAUSSIAN distribution. Default is 0 (no variation from mean).

    _bus1: Name of first bus. Examples:
        bus1=busname
        bus1=busname.1.2.3

        Bus2 automatically defaults to busname.0,0,0 unless it was previously defined.

    _bus2: Name of 2nd bus of the 2-terminal Fault object. Defaults to all phases connected to first bus, node 0,
    if not specified. (Shunt Wye Connection to ground reference)

        That is, the Fault defaults to a ground fault unless otherwise specified.

    _emergamps: Maximum or emerg current.

    _faultrate: Failure rate per year.

    _gmatrix: Use this to specify a nodal conductance (G) matrix to represent some arbitrary resistance network.
    Specify in lower triangle form as usual for DSS matrices.

    _minamps: Minimum amps that can sustain a temporary fault. Default is 5.

    _normamps: Normal rated current.

    _ontime: Time (sec) at which the fault is established for time varying simulations. Default is 0.0 (on at the
    beginning of the simulation)

    _pctperm: Percent of failures that become permanent.

    _r: Resistance, each phase, ohms. Default is 0.0001. Assumed to be Mean value if gaussian random mode.Max value
    if uniform mode.  A Fault is actually a series resistance that defaults to a wye connection to ground on the
    second terminal.  You may reconnect the 2nd terminal to achieve whatever connection.  Use the Gmatrix property to
    specify an arbitrary conductance matrix.

    _repair: Hours to repair.

    _temporary: {Yes | No} Default is No.  Designate whether the fault is temporary.  For Time-varying simulations,
    the fault will be removed if the current through the fault drops below the MINAMPS criteria.

    """

    title_ = "Fault"
    plural_title_ = "Faults"
    columns_ = ['percentage_stddev', 'basefreq', 'bus1', 'bus2', 'emergamps', 'enabled', 'faultrate', 'gmatrix',
                'like', 'minamps', 'normamps', 'ontime', 'pctperm', 'phases', 'r', 'repair', 'temporary']

    _percentage_stddev: float = 0
    _bus1: str = ''
    _bus2: str = ''
    _emergamps: float = None
    _faultrate: float = None
    _gmatrix: str = ''
    _minamps: float = 5
    _normamps: float = None
    _ontime: float = 0
    _pctperm: str = ''
    _r: float = 0.0001
    _repair: float = 0
    _temporary: str = 'No'

    @property
    def basefreq(self):
        return self._basefreq

    @basefreq.setter
    def basefreq(self, value):
        Utils.check_instance(value, 'basefreq', ['int', 'float'], )
        self._basefreq = value

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        Utils.check_instance(value, 'enabled', ['str'], )
        self._enabled = value

    @property
    def like(self):
        return self._like

    @like.setter
    def like(self, value):
        Utils.check_instance(value, 'like', ['str'], )
        self._like = value

    @property
    def phases(self):
        return self._phases

    @phases.setter
    def phases(self, value):
        Utils.check_instance(value, 'phases', ['int'], )
        self._phases = value

    @property
    def percentage_stddev(self):
        return self._percentage_stddev

    @percentage_stddev.setter
    def percentage_stddev(self, value):
        Utils.check_instance(value, 'percentage_stddev', ['int', 'float'], )
        self._percentage_stddev = value

    @property
    def bus1(self):
        return self._bus1

    @bus1.setter
    def bus1(self, value):
        Utils.check_instance(value, 'bus1', ['str'], )
        self._bus1 = value

    @property
    def bus2(self):
        return self._bus2

    @bus2.setter
    def bus2(self, value):
        Utils.check_instance(value, 'bus2', ['str'], )
        self._bus2 = value

    @property
    def emergamps(self):
        return self._emergamps

    @emergamps.setter
    def emergamps(self, value):
        Utils.check_instance(value, 'emergamps', ['int', 'float'], )
        self._emergamps = value

    @property
    def faultrate(self):
        return self._faultrate

    @faultrate.setter
    def faultrate(self, value):
        Utils.check_instance(value, 'faultrate', ['int', 'float'], )
        self._faultrate = value

    @property
    def gmatrix(self):
        return self._gmatrix

    @gmatrix.setter
    def gmatrix(self, value):
        Utils.check_instance(value, 'gmatrix', ['str'], )
        self._gmatrix = value

    @property
    def minamps(self):
        return self._minamps

    @minamps.setter
    def minamps(self, value):
        Utils.check_instance(value, 'minamps', ['int', 'float'], )
        self._minamps = value

    @property
    def normamps(self):
        return self._normamps

    @normamps.setter
    def normamps(self, value):
        Utils.check_instance(value, 'normamps', ['int', 'float'], )
        self._normamps = value

    @property
    def ontime(self):
        return self._ontime

    @ontime.setter
    def ontime(self, value):
        Utils.check_instance(value, 'ontime', ['int', 'float'], )
        self._ontime = value

    @property
    def pctperm(self):
        return self._pctperm

    @pctperm.setter
    def pctperm(self, value):
        Utils.check_instance(value, 'pctperm', ['str'], )
        self._pctperm = value

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, value):
        Utils.check_instance(value, 'r', ['int', 'float'], )
        self._r = value

    @property
    def repair(self):
        return self._repair

    @repair.setter
    def repair(self, value):
        Utils.check_instance(value, 'repair', ['int', 'float'], )
        self._repair = value

    @property
    def temporary(self):
        return self._temporary

    @temporary.setter
    def temporary(self, value):
        Utils.check_instance(value, 'temporary', ['str'], )
        self._temporary = value
