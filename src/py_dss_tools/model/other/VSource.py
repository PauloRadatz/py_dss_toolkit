# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:11:52
 Project: py_dss_tools [set, 2021]
"""
import attr

from .OtherElement import OtherElement
from ...utils import Utils


@attr.s
class VSource(OtherElement):
    """
    _angle: Phase angle in degrees of first phase: e.g.,Angle=10.3

    _basekv: Base Source kV, usually phase-phase (L-L) unless you are making a positive-sequence model or 1-phase
    modelin which case, it will be phase-neutral (L-N) kV.

    _basemva: Default value is 100. Base used to convert values specifiied with puZ1, puZ0, and puZ2 properties to
    ohms on kV base specified by BasekV property.

    _bus1: Name of bus to which the main terminal (1) is connected.
        bus1=busname
        bus1=busname.1.2.3

        The VSOURCE object is a two-terminal voltage source (thevenin equivalent). Bus2 defaults to Bus1 with all
        phases connected to ground (node 0) unless previously specified. This is a Yg connection. If you want
        something different, define the Bus2 property ezplicitly.

    _bus2: Name of bus to which 2nd terminal is connected.
        bus2=busname
        bus2=busname.1.2.3

        Default is Bus1.0.0.0 (grounded wye connection)

    _daily: LOADSHAPE object to use for the per-unit voltage for DAILY-mode simulations. Set the Mult property of the
    LOADSHAPE to the pu curve. Qmult is not used. If UseActual=Yes then the Mult curve should be actual L-N kV.

        Must be previously defined as a LOADSHAPE object.

        Sets Yearly curve if it is not already defined.   Set to NONE to reset to no loadahape for Yearly mode. The
        default is no variation.

    _duty: LOADSHAPE object to use for the per-unit voltage for DUTYCYCLE-mode simulations. Set the Mult property of
    the LOADSHAPE to the pu curve. Qmult is not used. If UseActual=Yes then the Mult curve should be actual L-N kV.

        Must be previously defined as a LOADSHAPE object.

        Defaults to Daily load shape when Daily is defined.   Set to NONE to reset to no loadahape for Yearly mode.
        The default is no variation.

    _frequency: Source frequency.  Defaults to system default base frequency.

    _isc1: Alternate method of defining the source impedance. Single-phase short circuit current, amps.  Default is
    10500.

    _isc3: Alternate method of defining the source impedance. 3-phase short circuit current, amps.  Default is 10000.

    _model: {Thevenin* | Ideal}  Specifies whether the Vsource is to be considered a Thevenin short circuit model or
    a quasi-ideal voltage source. If Thevenin, the Vsource uses the impedances defined for all calculations. If
    "Ideal", the model uses a small impedance on the diagonal of the impedance matrix for the fundamental base
    frequency power flow only. Then switches to actual Thevenin model for other frequencies.

    _mvasc1: MVA Short Circuit, 1-phase fault. Default = 2100. The "single-phase impedance", Zs, is determined by
    squaring the base kV and dividing by this value. Then Z0 is determined by Z0 = 3Zs - 2Z1.  For 1-phase sources,
    Zs is used directly. Use X0R0 to define X/R ratio for 1-phase source.

    _mvasc3: MVA Short circuit, 3-phase fault. Default = 2000. Z1 is determined by squaring the base kv and dividing
    by this value. For single-phase source, this value is not used.

    _pu: Per unit of the base voltage that the source is actually operating at. "pu=1.05"

    _puz0: 2-element array: e.g., [1  2]. An alternate way to specify Z0. See Z0 property. Per-unit zero-sequence
    impedance on base of Vsource BasekV and BaseMVA.

    _puz1: 2-element array: e.g., [1  2]. An alternate way to specify Z1. See Z1 property. Per-unit positive-sequence
    impedance on base of Vsource BasekV and BaseMVA.

    _puz2: 2-element array: e.g., [1  2]. An alternate way to specify Z2. See Z2 property. Per-unit negative-sequence
    impedance on base of Vsource BasekV and BaseMVA.

    _puzideal: 2-element array: e.g., [1  2]. The pu impedance to use for the quasi-ideal voltage source model.
    Should be a very small impedances. Default is [1e-6, 0.001]. Per-unit impedance on base of Vsource BasekV and
    BaseMVA. If too small, solution may not work. Be sure to check the voltage values and powers.

    _r0: Alternate method of defining the source impedance. Zero-sequence resistance, ohms.  Default is 1.9.

    _r1: Alternate method of defining the source impedance. Positive-sequence resistance, ohms.  Default is 1.65.

    _scantype: {pos*| zero | none} Maintain specified sequence for harmonic solution. Default is positive sequence.
    Otherwise, angle between phases rotates with harmonic.

    _sequence: {pos*| neg | zero} Set the phase angles for the specified symmetrical component sequence for
    non-harmonic solution modes. Default is positive sequence.

    _spectrum: Name of harmonic spectrum for this source.  Default is "defaultvsource", which is defined when the DSS
    starts.

    _x0: Alternate method of defining the source impedance. Zero-sequence reactance, ohms.  Default is 5.7.

    _x0r0: Zero-sequence X/R ratio.Default = 3.

    _x1: Alternate method of defining the source impedance. Positive-sequence reactance, ohms.  Default is 6.6.

    _x1r1: Positive-sequence  X/R ratio. Default = 4.

    _yearly: LOADSHAPE object to use for the per-unit voltage for YEARLY-mode simulations. Set the Mult property of
    the LOADSHAPE to the pu curve. Qmult is not used. If UseActual=Yes then the Mult curve should be actual L-N kV.
        Must be previously defined as a LOADSHAPE object.
        Is set to the Daily load shape when Daily is defined.  The daily load shape is repeated in this case. Set to
        NONE to reset to no loadahape for Yearly mode. The default is no variation.

    _z0: Zero-sequence equivalent source impedance, ohms, as a 2-element array representing a complex number. Example:
        Z0=[3, 4]  ! represents 3 + j4
        Used to define the impedance matrix of the VSOURCE if Z1 is also specified.
        Note: Z0 defaults to Z1 if it is not specifically defined.

    _z1: Positive-sequence equivalent source impedance, ohms, as a 2-element array representing a complex number.
        Example:
        Z1=[1, 2]  ! represents 1 + j2 If defined, Z1, Z2, and Z0 are used to define the impedance matrix of the
        VSOURCE. Z1 MUST BE DEFINED TO USE THIS OPTION FOR DEFINING THE MATRIX. Side Effect: Sets Z2 and Z0 to same
        values unless they were previously defined.

    _z2: Negative-sequence equivalent source impedance, ohms, as a 2-element array representing a complex number.
        Example:
        Z2=[1, 2]  ! represents 1 + j2 Used to define the impedance matrix of the VSOURCE if Z1 is also specified.
        Note: Z2 defaults to Z1 if it is not specifically defined. If Z2 is not equal to Z1, the impedance matrix is
        asymmetrical.

    """

    # title_ = "VSource" plural_title_ = "VSources" columns_ = ['angle', 'basefreq', 'basekv', 'basemva', 'bus1',
    # 'bus2', 'daily', 'duty', 'enabled', 'frequency', 'isc1', 'isc3', 'like', 'model', 'mvasc1', 'mvasc3', 'phases',
    # 'pu', 'puz0', 'puz1', 'puz2', 'puzideal', 'r0', 'r1', 'scantype', 'sequence', 'spectrum', 'x0', 'x0r0', 'x1',
    # 'x1r1', 'yearly', 'z0', 'z1', 'z2']

    _angle = attr.ib(validator=attr.validators.instance_of((int, float)), default=0)
    _basekv = attr.ib(validator=attr.validators.instance_of((int, float)), default=0)
    _basemva = attr.ib(validator=attr.validators.instance_of((int, float)), default=0)
    _bus1 = attr.ib(validator=attr.validators.instance_of(str), default='')
    _bus2 = attr.ib(validator=attr.validators.instance_of(str), default='Bus1.0.0.0')
    _daily = attr.ib(validator=attr.validators.instance_of(str), default='')
    _duty = attr.ib(validator=attr.validators.instance_of(str), default='')
    _frequency = attr.ib(validator=attr.validators.instance_of((int, float)), default=60)
    _isc1 = attr.ib(validator=attr.validators.instance_of((int, float)), default=10500)
    _isc3 = attr.ib(validator=attr.validators.instance_of((int, float)), default=10000)
    _model = attr.ib(validator=attr.validators.instance_of(str), default='Thevenin')
    _mvasc1 = attr.ib(validator=attr.validators.instance_of((int, float)), default=21000)
    _mvasc3 = attr.ib(validator=attr.validators.instance_of((int, float)), default=20000)
    _pu = attr.ib(validator=attr.validators.instance_of((int, float)), default=1.0001)
    _puz0 = attr.ib(validator=attr.validators.instance_of(str), default='[]')
    _puz1 = attr.ib(validator=attr.validators.instance_of(str), default='[]')
    _puz2 = attr.ib(validator=attr.validators.instance_of(str), default='[]')
    _puzideal = attr.ib(validator=attr.validators.instance_of(str), default='[]')
    _r0 = attr.ib(validator=attr.validators.instance_of((int, float)), default=1.9)
    _r1 = attr.ib(validator=attr.validators.instance_of((int, float)), default=1.65)
    _scantype = attr.ib(validator=attr.validators.instance_of(str), default='Pos')
    _sequence = attr.ib(validator=attr.validators.instance_of(str), default='Pos')
    _spectrum = attr.ib(validator=attr.validators.instance_of(str), default='defaultvsource')
    _x0 = attr.ib(validator=attr.validators.instance_of((int, float)), default=5.7)
    _x0r0 = attr.ib(validator=attr.validators.instance_of((int, float)), default=3)
    _x1 = attr.ib(validator=attr.validators.instance_of((int, float)), default=6.6)
    _x1r1 = attr.ib(validator=attr.validators.instance_of((int, float)), default=4)
    _yearly = attr.ib(validator=attr.validators.instance_of(str), default='')
    _z0 = attr.ib(validator=attr.validators.instance_of(str), default='[]')
    _z1 = attr.ib(validator=attr.validators.instance_of(str), default='[]')
    _z2 = attr.ib(validator=attr.validators.instance_of(str), default='[]')

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
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        Utils.check_instance(value, 'angle', ['int', 'float'], )
        self._angle = value

    @property
    def basekv(self):
        return self._basekv

    @basekv.setter
    def basekv(self, value):
        Utils.check_instance(value, 'basekv', ['int', 'float'], )
        self._basekv = value

    @property
    def basemva(self):
        return self._basemva

    @basemva.setter
    def basemva(self, value):
        Utils.check_instance(value, 'basemva', ['int', 'float'], )
        self._basemva = value

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
    def daily(self):
        return self._daily

    @daily.setter
    def daily(self, value):
        Utils.check_instance(value, 'daily', ['str'], )
        self._daily = value

    @property
    def duty(self):
        return self._duty

    @duty.setter
    def duty(self, value):
        Utils.check_instance(value, 'duty', ['str'], )
        self._duty = value

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        Utils.check_instance(value, 'frequency', ['int', 'float'], )
        self._frequency = value

    @property
    def isc1(self):
        return self._isc1

    @isc1.setter
    def isc1(self, value):
        Utils.check_instance(value, 'isc1', ['int', 'float'], )
        self._isc1 = value

    @property
    def isc3(self):
        return self._isc3

    @isc3.setter
    def isc3(self, value):
        Utils.check_instance(value, 'isc3', ['int', 'float'], )
        self._isc3 = value

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        Utils.check_instance(value, 'model', ['str'], )
        self._model = value

    @property
    def mvasc1(self):
        return self._mvasc1

    @mvasc1.setter
    def mvasc1(self, value):
        Utils.check_instance(value, 'mvasc1', ['int', 'float'], )
        self._mvasc1 = value

    @property
    def mvasc3(self):
        return self._mvasc3

    @mvasc3.setter
    def mvasc3(self, value):
        Utils.check_instance(value, 'mvasc3', ['int', 'float'], )
        self._mvasc3 = value

    @property
    def pu(self):
        return self._pu

    @pu.setter
    def pu(self, value):
        Utils.check_instance(value, 'pu', ['int', 'float'], )
        self._pu = value

    @property
    def puz0(self):
        return self._puz0

    @puz0.setter
    def puz0(self, value):
        Utils.check_instance(value, 'puz0', ['str'], )
        self._puz0 = value

    @property
    def puz1(self):
        return self._puz1

    @puz1.setter
    def puz1(self, value):
        Utils.check_instance(value, 'puz1', ['str'], )
        self._puz1 = value

    @property
    def puz2(self):
        return self._puz2

    @puz2.setter
    def puz2(self, value):
        Utils.check_instance(value, 'puz2', ['str'], )
        self._puz2 = value

    @property
    def puzideal(self):
        return self._puzideal

    @puzideal.setter
    def puzideal(self, value):
        Utils.check_instance(value, 'puzideal', ['str'], )
        self._puzideal = value

    @property
    def r0(self):
        return self._r0

    @r0.setter
    def r0(self, value):
        Utils.check_instance(value, 'r0', ['int', 'float'], )
        self._r0 = value

    @property
    def r1(self):
        return self._r1

    @r1.setter
    def r1(self, value):
        Utils.check_instance(value, 'r1', ['int', 'float'], )
        self._r1 = value

    @property
    def scantype(self):
        return self._scantype

    @scantype.setter
    def scantype(self, value):
        Utils.check_instance(value, 'scantype', ['str'], )
        self._scantype = value

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, value):
        Utils.check_instance(value, 'sequence', ['str'], )
        self._sequence = value

    @property
    def spectrum(self):
        return self._spectrum

    @spectrum.setter
    def spectrum(self, value):
        Utils.check_instance(value, 'spectrum', ['str'], )
        self._spectrum = value

    @property
    def x0(self):
        return self._x0

    @x0.setter
    def x0(self, value):
        Utils.check_instance(value, 'x0', ['int', 'float'], )
        self._x0 = value

    @property
    def x0r0(self):
        return self._x0r0

    @x0r0.setter
    def x0r0(self, value):
        Utils.check_instance(value, 'x0r0', ['int', 'float'], )
        self._x0r0 = value

    @property
    def x1(self):
        return self._x1

    @x1.setter
    def x1(self, value):
        Utils.check_instance(value, 'x1', ['int', 'float'], )
        self._x1 = value

    @property
    def x1r1(self):
        return self._x1r1

    @x1r1.setter
    def x1r1(self, value):
        Utils.check_instance(value, 'x1r1', ['int', 'float'], )
        self._x1r1 = value

    @property
    def yearly(self):
        return self._yearly

    @yearly.setter
    def yearly(self, value):
        Utils.check_instance(value, 'yearly', ['str'], )
        self._yearly = value

    @property
    def z0(self):
        return self._z0

    @z0.setter
    def z0(self, value):
        Utils.check_instance(value, 'z0', ['str'], )
        self._z0 = value

    @property
    def z1(self):
        return self._z1

    @z1.setter
    def z1(self, value):
        Utils.check_instance(value, 'z1', ['str'], )
        self._z1 = value

    @property
    def z2(self):
        return self._z2

    @z2.setter
    def z2(self, value):
        Utils.check_instance(value, 'z2', ['str'], )
        self._z2 = value
