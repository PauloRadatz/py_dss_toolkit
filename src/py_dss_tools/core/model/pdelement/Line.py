# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 04/09/2021 at 20:39:04
 Project: py_dss_tools [set, 2021]
"""
from dataclasses import dataclass

from py_dss_tools.core.common.Enumerations import EarthModel, LineType, Units
from py_dss_tools.core.model.pdelement.PDElement import PDElement
from py_dss_tools.utils import Utils


@dataclass
class Line(PDElement):
    """
    _b0: Alternate way to specify C0. MicroS per unit length.

    _b1: Alternate way to specify C1. MicroS per unit length.

    _bus1: Name of bus to which first terminal is connected.
        Example:
        bus1=busname   (assumes all terminals connected in normal phase order)
        bus1=busname.3.1.2.0 (specify terminal to node connections explicitly)

    _bus2: Name of bus to which 2nd terminal is connected.

    _c0: Zero-sequence capacitance, nf per unit length. Setting any of R1, R0, X1, X0, C1, C0 forces the program to
    use the symmetrical component line definition.See also B0.

    _c1: Positive-sequence capacitance, nf per unit length.  Setting any of R1, R0, X1, X0, C1, C0 forces the program
    to use the symmetrical component line definition. See also Cmatrix and B1.

    _cmatrix: Nodal Capacitance matrix, lower triangle, nf per unit length.Order of the matrix is the number of
    phases. May be used to specify the shunt capacitance of any line configuration. Using any of Rmatrix, Xmatrix,
    Cmatrix forces program to use the matrix values for line impedance definition.  For balanced line models, you may
    use the standard symmetrical component data definition instead.

    _cncables: Array of CNData names for use in a cable constants calculation. Must be used in conjunction with the
    Spacing property. Specify the Spacing first, using "nphases" cncables. You may later specify "nconds-nphases" wires
    for separate neutrals.

    _earthmodel: One of {Carson | FullCarson | Deri}. Default is the global value established with the Set EarthModel
    command. See the Options Help on EarthModel option. This is used to override the global value for this line. This
    option applies only when the "geometry" property is used.

    _geometry: Geometry code for LineGeometry Object. Supercedes any previous definition of line impedance. Line
    constants are computed for each frequency change or rho change. CAUTION: may alter number of phases. You cannot
    subsequently change the number of phases unless you change how the line impedance is defined.

    _length: Length of line. Default is 1.0. If units do not match the impedance data, specify "units" property.

    _linecode: Name of linecode object describing line impedances. If you use a line code, you do not need to specify
    the impedances here. The line code must have been PREVIOUSLY defined. The values specified last will prevail over
    those specified earlier (left-to-right sequence of properties).  You can subsequently change the number of phases
    if symmetrical component quantities are specified.If no line code or impedance data are specified, the line object
    defaults to 336 MCM ACSR on 4 ft spacing.

    _linetype: Code designating the type of line.
        One of: OH, UG, UG_TS, UG_CN, SWT_LDBRK, SWT_FUSE, SWT_SECT, SWT_REC, SWT_DISC, SWT_BRK, SWT_ELBOW
        OpenDSS currently does not use this internally. For whatever purpose the user defines. Default is OH.

    _r0: Zero-sequence Resistance, ohms per unit length. Setting any of R1, R0, X1, X0, C1, C0 forces the program to
    use the symmetrical component line definition.

    _r1: Positive-sequence Resistance, ohms per unit length. Setting any of R1, R0, X1, X0, C1, C0 forces the program
    to use the symmetrical component line definition. See also Rmatrix.

    _ratings: An array of ratings to be used when the seasonal ratings flag is True. It can be used to insert multiple
     ratings to change during a QSTS simulation to evaluate different ratings in lines.

    _rg: Carson earth return resistance per unit length used to compute impedance values at base frequency. Default is
     0.01805 = 60 Hz value in ohms per kft (matches default line impedances). This value is required for harmonic
     solutions if you wish to adjust the earth return impedances for frequency. If not, set both Rg and Xg = 0.

    _rho: Default=100 meter ohms.  Earth resitivity used to compute earth correction factor. Overrides Line geometry
    definition if specified.

    _rmatrix: Resistance matrix, lower triangle, ohms per unit length. Order of the matrix is the number of phases.
    May be used to specify the impedance of any line configuration. Using any of Rmatrix, Xmatrix, Cmatrix forces
    program to use the matrix values for line impedance definition. For balanced line models, you may use the standard
    symmetrical component data definition instead.

    _seasons: Defines the number of ratings to be defined for the wire, to be used only when defining seasonal ratings
    using the "Ratings" property.

    _spacing: Reference to a LineSpacing for use in a line constants calculation. Must be used in conjunction with the
    Wires property. Specify this before the wires property.

    _switch: {y/n | T/F}  Default= no/false.  Designates this line as a switch for graphics and algorithmic purposes.
    SIDE EFFECT: Sets r1 = 1.0; x1 = 1.0; r0 = 1.0; x0 = 1.0; c1 = 1.1 ; c0 = 1.0;  length = 0.001; You must reset if
    you want something different.

    _tscables: Array of TSData names for use in a cable constants calculation. Must be used in conjunction with the
    Spacing property. Specify the Spacing first, using "nphases" tscables. You may later specify "nconds-nphases" wires
    for separate neutrals

    _units: Length Units = {none | mi|kft|km|m|Ft|in|cm } Default is None - assumes length units match impedance units.

    _wires: Array of WireData names for use in an overhead line constants calculation. Must be used in conjunction with
     the Spacing property. Specify the Spacing first, and "ncond" wires. May also be used to specify bare neutrals with
     cables, using "ncond-nphase" wires.

    _x0: Zero-sequence Reactance, ohms per unit length. Setting any of R1, R0, X1, X0, C1, C0 forces the program to
    use the symmetrical component line definition.

    _x1: Positive-sequence Reactance, ohms per unit length. Setting any of R1, R0, X1, X0, C1, C0 forces the program
    to use the symmetrical component line definition.  See also Xmatrix

    _xg: Carson earth return reactance per unit length used to compute impedance values at base frequency.  For making
    better frequency adjustments. Default is 0.155081 = 60 Hz value in ohms per kft (matches default line impedances).
    This value is required for harmonic solutions if you wish to adjust the earth return impedances for frequency. If
    not, set both Rg and Xg = 0.

    _xmatrix: Reactance matrix, lower triangle, ohms per unit length. Order of the matrix is the number of phases. May
    be used to specify the impedance of any line configuration. Using any of Rmatrix, Xmatrix, Cmatrix forces program to
     use the matrix values for line impedance definition.  For balanced line models, you may use the standard
     symmetrical component data definition instead.
    """

    title_ = "Line"
    plural_title_ = "Lines"
    columns_ = ['b0', 'b1', 'basefreq', 'bus1', 'bus2', 'c0', 'c1', 'cmatrix', 'cncables', 'earthmodel', 'emergamps',
                'enabled', 'faultrate', 'geometry', 'length', 'like', 'linecode', 'linetype', 'name', 'normamps',
                'pctperm', 'phases', 'r0', 'r1', 'ratings', 'repair', 'rg', 'rho', 'rmatrix', 'seasons', 'spacing',
                'switch', 'tscables', 'units', 'wires', 'x0', 'x1', 'xg', 'xmatrix']

    _b0: float = 1.0
    _b1: float = 1.0
    _bus1: str = ''
    _bus2: str = ''
    _c0: float = 1.0
    _c1: float = 1.1
    _cmatrix: str = ''
    # TODO: must be a array of CNData names
    _cncables: str = ''
    _earthmodel: str = EarthModel.Deri.value
    # TODO: must be a LineGeometry object
    _geometry: str = ''
    _length: float = 1.0
    # TODO: must be a LineCode object
    _linecode: str = ''
    _linetype: str = LineType.OH.value
    # _name: str = 'my_line_' + Utils.generate_random_string()
    _r0: float = 0.01
    _r1: float = 0.01
    _ratings: str = '400'
    _rg: float = 0.01805
    _rho: float = 100
    _rmatrix: str = ''
    _seasons: str = ''
    _spacing: str = ''
    # TODO: must be a enum here AND change values in r0 r1 x0 x1 x1 x0 length when true
    _switch: str = 'false'
    # TODO: must be a array of TSData
    _tscables: str = ''
    _units: str = Units.m.value
    # TODO: must be a array of Wiredata
    _wires: str = ''
    _x0: float = 1.0
    _x1: float = 1.0
    _xg: float = 0.155081
    _xmatrix: str = ''

    def _post_init_(self):
        self._name = 'my_line_'

    @property
    def basefreq(self):
        return self._basefreq

    @basefreq.setter
    def basefreq(self, value: float):
        self.check_instance(value, 'basefreq', ['int', 'float'])
        self._basefreq = value

    @property
    def emergamps(self):
        return self._emergamps

    @emergamps.setter
    def emergamps(self, value):
        self.check_instance(value, 'emergamps', ['int', 'float'], )
        self._emergamps = value

    @property
    def enabled(self):
        return 0

    @property
    def faultrate(self):
        return 0

    @property
    def like(self):
        return 0

    @property
    def normamps(self):
        return 0

    @property
    def pctperm(self):
        return 0

    @property
    def phases(self):
        return 0

    @property
    def repair(self):
        return self._repair

    @repair.setter
    def repair(self, value):
        self.check_instance(value, 'repair', ['int', 'float'], )
        self._repair = value

    @property
    def b0(self):
        return self._b0

    @b0.setter
    def b0(self, value):
        self.check_instance(value, 'b0', ['int', 'float'], )
        self._b0 = value

    @property
    def b1(self):
        return self._b1

    @b1.setter
    def b1(self, value):
        self.check_instance(value, 'b1', ['int', 'float'], )
        self._b1 = value

    @property
    def bus1(self):
        return self._bus1

    @bus1.setter
    def bus1(self, value):
        self.check_instance(value, 'bus1', ['str'], )
        self._bus1 = value

    @property
    def bus2(self):
        return self._bus2

    @bus2.setter
    def bus2(self, value):
        self.check_instance(value, 'bus2', ['str'], )
        self._bus2 = value

    @property
    def c0(self):
        return self._c0

    @c0.setter
    def c0(self, value):
        self.check_instance(value, 'c0', ['int', 'float'], )
        self._c0 = value

    @property
    def c1(self):
        return self._c1

    @c1.setter
    def c1(self, value):
        self.check_instance(value, 'c1', ['int', 'float'], )
        self._c1 = value

    @property
    def cmatrix(self):
        return self._cmatrix

    @cmatrix.setter
    def cmatrix(self, value):
        self.check_instance(value, 'cmatrix', ['str'], )
        self._cmatrix = value

    @property
    def cncables(self):
        return self._cncables

    @cncables.setter
    def cncables(self, value):
        self.check_instance(value, 'cncables', ['str'], )
        self._cncables = value

    @property
    def earthmodel(self):
        return self._earthmodel

    @earthmodel.setter
    def earthmodel(self, value):
        self.check_instance(value, 'earthmodel', ['str'], )
        self._earthmodel = value

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, value):
        self.check_instance(value, 'geometry', ['str'], )
        self._geometry = value

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self.check_instance(value, 'length', ['int', 'float'], )
        self._length = value

    @property
    def linecode(self):
        return self._linecode

    @linecode.setter
    def linecode(self, value):
        self.check_instance(value, 'linecode', ['str'], )
        self._linecode = value

    @property
    def linetype(self):
        return self._linetype

    @linetype.setter
    def linetype(self, value):
        self.check_instance(value, 'linetype', ['str'], )
        self._linetype = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self.check_instance(value, 'name', ['str'], )
        self._name = Utils.remove_blank_spaces(value)

    @property
    def r0(self):
        return self._r0

    @r0.setter
    def r0(self, value):
        self.check_instance(value, 'r0', ['int', 'float'], )
        self._r0 = value

    @property
    def r1(self):
        return self._r1

    @r1.setter
    def r1(self, value):
        self.check_instance(value, 'r1', ['int', 'float'], )
        self._r1 = value

    @property
    def ratings(self):
        return self._ratings

    @ratings.setter
    def ratings(self, value):
        self.check_instance(value, 'ratings', ['str'], )
        self._ratings = value

    @property
    def rg(self):
        return self._rg

    @rg.setter
    def rg(self, value):
        self.check_instance(value, 'rg', ['int', 'float'], )
        self._rg = value

    @property
    def rho(self):
        return self._rho

    @rho.setter
    def rho(self, value):
        self.check_instance(value, 'rho', ['int', 'float'], )
        self._rho = value

    @property
    def rmatrix(self):
        return self._rmatrix

    @rmatrix.setter
    def rmatrix(self, value):
        self.check_instance(value, 'rmatrix', ['str'], )
        self._rmatrix = value

    @property
    def seasons(self):
        return self._seasons

    @seasons.setter
    def seasons(self, value):
        self.check_instance(value, 'seasons', ['str'], )
        self._seasons = value

    @property
    def spacing(self):
        return self._spacing

    @spacing.setter
    def spacing(self, value):
        self.check_instance(value, 'spacing', ['str'], )
        self._spacing = value

    @property
    def switch(self):
        return self._switch

    @switch.setter
    def switch(self, value):
        self.check_instance(value, 'switch', ['str'], )
        self._switch = value

    @property
    def tscables(self):
        return self._tscables

    @tscables.setter
    def tscables(self, value):
        self.check_instance(value, 'tscables', ['str'], )
        self._tscables = value

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        self.check_instance(value, 'units', ['str'], )
        self._units = value

    @property
    def wires(self):
        return self._wires

    @wires.setter
    def wires(self, value):
        self.check_instance(value, 'wires', ['str'], )
        self._wires = value

    @property
    def x0(self):
        return self._x0

    @x0.setter
    def x0(self, value):
        self.check_instance(value, 'x0', ['int', 'float'], )
        self._x0 = value

    @property
    def x1(self):
        return self._x1

    @x1.setter
    def x1(self, value):
        self.check_instance(value, 'x1', ['int', 'float'], )
        self._x1 = value

    @property
    def xg(self):
        return self._xg

    @xg.setter
    def xg(self, value):
        self.check_instance(value, 'xg', ['int', 'float'], )
        self._xg = value

    @property
    def xmatrix(self):
        return self._xmatrix

    @xmatrix.setter
    def xmatrix(self, value):
        self.check_instance(value, 'xmatrix', ['str'], )
        self._xmatrix = value
