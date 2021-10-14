# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 04/09/2021 at 20:39:04
 Project: py_dss_tools [set, 2021]
"""
import attr
import pandas as pd

from py_dss_tools.model.pdelement import PDElement
from py_dss_tools.utils import Utils


@attr.s(kw_only=True)
class Line(PDElement):
    """
    _b0 = alternate way to specify C0. MicroS per unit length.

    _b1 = alternate way to specify C1. MicroS per unit length.

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

    _cncables = array of CNData names for use in a cable constants calculation. Must be used in conjunction with the
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

    _ratings = an array of ratings to be used when the seasonal ratings flag is True. It can be used to insert multiple
     ratings to change during a QSTS simulation to evaluate different ratings in lines.

    _rg: Carson earth return resistance per unit length used to compute impedance values at base frequency. Default is
     0.01805 = 60 Hz value in ohms per kft (matches default line impedances). This value is required for harmonic
     solutions if you wish to adjust the earth return impedances for frequency. If not, set both Rg and Xg = 0.

    _rho: default_factory=100 meter ohms.  Earth resitivity used to compute earth correction factor. Overrides Line
    geometry definition if specified.

    _rmatrix: Resistance matrix, lower triangle, ohms per unit length. Order of the matrix is the number of phases.
    May be used to specify the impedance of any line configuration. Using any of Rmatrix, Xmatrix, Cmatrix forces
    program to use the matrix values for line impedance definition. For balanced line models, you may use the standard
    symmetrical component data definition instead.

    _seasons: Defines the number of ratings to be defined for the wire, to be used only when defining seasonal ratings
    using the "Ratings" property.

    _spacing: Reference to a LineSpacing for use in a line constants calculation. Must be used in conjunction with the
    Wires property. Specify this before the wires property.

    _switch: {y/n | T/F}  default_factory= no/false.  Designates this line as a switch for graphics and algorithmic
    purposes. SIDE EFFECT: Sets r1 = 1.0; x1 = 1.0; r0 = 1.0; x0 = 1.0; c1 = 1.1 ; c0 = 1.0;  length = 0.001; You
    must reset if you want something different.

    _tscables = array of TSData names for use in a cable constants calculation. Must be used in conjunction with the
    Spacing property. Specify the Spacing first, using "nphases" tscables. You may later specify "nconds-nphases" wires
    for separate neutrals

    _units: Length Units = {none | mi|kft|km|m|Ft|in|cm } Default is None - assumes length units match impedance units.

    _wires = array of WireData names for use in an overhead line constants calculation. Must be used in conjunction with
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
    columns_ = ['_b0', '_b1', '_basefreq', '_bus1', '_bus2', '_c0', '_c1', '_cmatrix', '_cncables', '_earthmodel',
                '_emergamps', '_enabled', '_faultrate', '_geometry', '_length', '_like', '_linecode', '_linetype',
                '_name', '_normamps', '_pctperm', '_phases', '_r0', '_r1', '_ratings', '_repair', '_rg', '_rho',
                '_rmatrix', '_seasons', '_spacing', '_switch', '_tscables', '_units', '_wires', '_x0', '_x1', '_xg',
                '_xmatrix']
    # columns_no_ = ['b0', 'b1', 'basefreq', 'bus1', 'bus2', 'c0', 'c1', 'cmatrix', 'cncables', 'earthmodel',
    # 'emergamps', 'enabled', 'faultrate', 'geometry', 'length', 'like', 'linecode', 'linetype', 'name', 'normamps',
    # 'pctperm', 'phases', 'r0', 'r1', 'ratings', 'repair', 'rg', 'rho', 'rmatrix', 'seasons', 'spacing', 'switch',
    # 'tscables', 'units', 'wires', 'x0', 'x1', 'xg', 'xmatrix']

    _b0 = attr.ib(validator=attr.validators.instance_of((int, float)), default=1.0)
    _b1 = attr.ib(validator=attr.validators.instance_of((int, float)), default=1.0)
    _bus1 = attr.ib(validator=attr.validators.instance_of(str), default='')
    _bus2 = attr.ib(validator=attr.validators.instance_of(str), default='')
    _c0 = attr.ib(validator=attr.validators.instance_of((int, float)), default=1.0)
    _c1 = attr.ib(validator=attr.validators.instance_of((int, float)), default=1.1)
    _cmatrix = attr.ib(validator=attr.validators.instance_of(str), default='[]')
    _cncables = attr.ib(validator=attr.validators.instance_of(str), default='')
    _earthmodel = attr.ib(validator=attr.validators.instance_of(str), default='Deri')
    _geometry = attr.ib(validator=attr.validators.instance_of(str), default='')
    _length = attr.ib(validator=attr.validators.instance_of((int, float)), default=1.0)
    _linecode = attr.ib(validator=attr.validators.instance_of(str), default='')
    _linetype = attr.ib(validator=attr.validators.instance_of(str), default='')
    _phases = attr.ib(validator=attr.validators.instance_of(int), default=3)
    _r0 = attr.ib(validator=attr.validators.instance_of((int, float)), default=0.01)
    _r1 = attr.ib(validator=attr.validators.instance_of((int, float)), default=0.01)
    _ratings = attr.ib(validator=attr.validators.instance_of(str), default='[400,]')
    _rg = attr.ib(validator=attr.validators.instance_of((int, float)), default=0.01805)
    _rho = attr.ib(validator=attr.validators.instance_of((int, float)), default=100)
    _rmatrix = attr.ib(validator=attr.validators.instance_of(str), default='[]')
    _seasons = attr.ib(validator=attr.validators.instance_of(str), default='')
    _spacing = attr.ib(validator=attr.validators.instance_of(str), default='')
    _switch = attr.ib(validator=attr.validators.instance_of(str), default='false')
    _tscables = attr.ib(validator=attr.validators.instance_of(str), default='')
    _units = attr.ib(validator=attr.validators.instance_of(str), default='m')
    _wires = attr.ib(validator=attr.validators.instance_of(str), default='')
    _x0 = attr.ib(validator=attr.validators.instance_of((int, float)), default=1.0)
    _x1 = attr.ib(validator=attr.validators.instance_of((int, float)), default=1.0)
    _xg = attr.ib(validator=attr.validators.instance_of((int, float)), default=0.155081)
    _xmatrix = attr.ib(validator=attr.validators.instance_of(str), default='[]')

    def __attrs_post_init__(self):
        if self._name != '':
            self._name = Utils.remove_blank_spaces(self._name)
        else:
            self._name = 'my_line_' + Utils.generate_random_string()

        if self._bus1 == '':
            self._bus1 = "my_bus1_" + Utils.generate_random_string()
        else:
            self._bus1 = Utils.remove_blank_spaces(self._bus1.lower())

        if self._bus2 == '':
            self._bus2 = "my_bus2_" + Utils.generate_random_string()
        else:
            self._bus2 = Utils.remove_blank_spaces(self._bus2.lower())

    def to_dataframe(self):
        return pd.DataFrame.from_records([self.__dict__])

    def to_dict(self):
        return self.__dict__

    def to_list(self):
        return list(self.__dict__)

    @property
    def basefreq(self) -> [int, float]:
        return self._basefreq

    @basefreq.setter
    def basefreq(self, value: [int, float]):
        Utils.check_instance(value, 'basefreq', ['int', 'float'])
        self._basefreq = value

    @property
    def emergamps(self) -> [int, float]:
        return self._emergamps

    @emergamps.setter
    def emergamps(self, value: [int, float]):
        Utils.check_instance(value, 'emergamps', ['int', 'float'], )
        self._emergamps = value

    @property
    def enabled(self) -> str:
        return self._enabled

    @enabled.setter
    def enabled(self, value: str):
        Utils.check_instance(value, 'enabled', ['str'], )
        self._enabled = value

    @property
    def faultrate(self) -> [int, float]:
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
    def normamps(self) -> [int, float]:
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
    def repair(self, value: [int, float]):
        Utils.check_instance(value, 'repair', ['int', 'float'], )
        self._repair = value

    @property
    def b0(self) -> [int, float]:
        return self._b0

    @b0.setter
    def b0(self, value: [int, float]):
        Utils.check_instance(value, 'b0', ['int', 'float'], )
        self._b0 = value

    @property
    def b1(self) -> [int, float]:
        return self._b1

    @b1.setter
    def b1(self, value: [int, float]):
        Utils.check_instance(value, 'b1', ['int', 'float'], )
        self._b1 = value

    @property
    def bus1(self) -> str:
        return self._bus1

    @bus1.setter
    def bus1(self, value: str):
        Utils.check_instance(value, 'bus1', ['str'], )
        self._bus1 = Utils.remove_blank_spaces(value.lower())

    @property
    def bus2(self) -> str:
        return self._bus2

    @bus2.setter
    def bus2(self, value: str):
        Utils.check_instance(value, 'bus2', ['str'], )
        self._bus2 = Utils.remove_blank_spaces(value.lower())

    @property
    def c0(self) -> [int, float]:
        return self._c0

    @c0.setter
    def c0(self, value: [int, float]):
        Utils.check_instance(value, 'c0', ['int', 'float'], )
        self._c0 = value

    @property
    def c1(self) -> [int, float]:
        return self._c1

    @c1.setter
    def c1(self, value: [int, float]):
        Utils.check_instance(value, 'c1', ['int', 'float'], )
        self._c1 = value

    @property
    def cmatrix(self) -> str:
        return self._cmatrix

    @cmatrix.setter
    def cmatrix(self, value: str):
        Utils.check_instance(value, 'cmatrix', ['str'], )
        self._cmatrix = value

    @property
    def cncables(self) -> str:
        return self._cncables

    @cncables.setter
    def cncables(self, value: str):
        Utils.check_instance(value, 'cncables', ['str'], )
        self._cncables = value

    @property
    def earthmodel(self) -> str:
        return self._earthmodel

    @earthmodel.setter
    def earthmodel(self, value: str):
        Utils.check_instance(value, 'earthmodel', ['str'], )
        self._earthmodel = value

    @property
    def geometry(self) -> str:
        return self._geometry

    @geometry.setter
    def geometry(self, value: str):
        Utils.check_instance(value, 'geometry', ['str'], )
        self._geometry = value

    @property
    def length(self) -> [int, float]:
        return self._length

    @length.setter
    def length(self, value: [int, float]):
        Utils.check_instance(value, 'length', ['int', 'float'], )
        self._length = value

    @property
    def linecode(self) -> str:
        return self._linecode

    @linecode.setter
    def linecode(self, value: str):
        Utils.check_instance(value, 'linecode', ['str'], )
        self._linecode = value

    @property
    def linetype(self) -> str:
        return self._linetype

    @linetype.setter
    def linetype(self, value: str):
        Utils.check_instance(value, 'linetype', ['str'], )
        self._linetype = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        Utils.check_instance(value, 'name', ['str'], )
        self._name = Utils.remove_blank_spaces(value)

    @property
    def r0(self) -> [int, float]:
        return self._r0

    @r0.setter
    def r0(self, value: [int, float]):
        Utils.check_instance(value, 'r0', ['int', 'float'], )
        self._r0 = value

    @property
    def r1(self) -> [int, float]:
        return self._r1

    @r1.setter
    def r1(self, value: [int, float]):
        Utils.check_instance(value, 'r1', ['int', 'float'], )
        self._r1 = value

    @property
    def ratings(self) -> str:
        return self._ratings

    @ratings.setter
    def ratings(self, value: str):
        Utils.check_instance(value, 'ratings', ['str'], )
        self._ratings = value

    @property
    def rg(self) -> [int, float]:
        return self._rg

    @rg.setter
    def rg(self, value: [int, float]):
        Utils.check_instance(value, 'rg', ['int', 'float'], )
        self._rg = value

    @property
    def rho(self) -> [int, float]:
        return self._rho

    @rho.setter
    def rho(self, value: [int, float]):
        Utils.check_instance(value, 'rho', ['int', 'float'], )
        self._rho = value

    @property
    def rmatrix(self) -> str:
        return self._rmatrix

    @rmatrix.setter
    def rmatrix(self, value: str):
        Utils.check_instance(value, 'rmatrix', ['str'], )
        self._rmatrix = value

    @property
    def seasons(self) -> str:
        return self._seasons

    @seasons.setter
    def seasons(self, value: str):
        Utils.check_instance(value, 'seasons', ['str'], )
        self._seasons = value

    @property
    def spacing(self) -> str:
        return self._spacing

    @spacing.setter
    def spacing(self, value: str):
        Utils.check_instance(value, 'spacing', ['str'], )
        self._spacing = value

    @property
    def switch(self) -> str:
        return self._switch

    @switch.setter
    def switch(self, value: str):
        Utils.check_instance(value, 'switch', ['str'], )
        self._switch = value

    @property
    def tscables(self) -> str:
        return self._tscables

    @tscables.setter
    def tscables(self, value: str):
        Utils.check_instance(value, 'tscables', ['str'], )
        self._tscables = value

    @property
    def units(self) -> str:
        return self._units

    @units.setter
    def units(self, value: str):
        Utils.check_instance(value, 'units', ['str'], )
        self._units = value

    @property
    def wires(self) -> str:
        return self._wires

    @wires.setter
    def wires(self, value: str):
        Utils.check_instance(value, 'wires', ['str'], )
        self._wires = value

    @property
    def x0(self) -> [int, float]:
        return self._x0

    @x0.setter
    def x0(self, value: [int, float]):
        Utils.check_instance(value, 'x0', ['int', 'float'], )
        self._x0 = value

    @property
    def x1(self) -> [int, float]:
        return self._x1

    @x1.setter
    def x1(self, value: [int, float]):
        Utils.check_instance(value, 'x1', ['int', 'float'], )
        self._x1 = value

    @property
    def xg(self) -> [int, float]:
        return self._xg

    @xg.setter
    def xg(self, value: [int, float]):
        Utils.check_instance(value, 'xg', ['int', 'float'], )
        self._xg = value

    @property
    def xmatrix(self) -> str:
        return self._xmatrix

    @xmatrix.setter
    def xmatrix(self, value: str):
        Utils.check_instance(value, 'xmatrix', ['str'], )
        self._xmatrix = value
