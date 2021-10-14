# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 02/09/2021 at 00:42:09
 Project: py_dss_tools [set, 2021]
"""
import attr
import pandas as pd
from py_dss_interface import DSS

from py_dss_tools.controller.LineController import LineController
from py_dss_tools.controller.ReactorController import ReactorController
from py_dss_tools.model.pdelement import Line, Transformer
from py_dss_tools.model.pdelement import Reactor
from .Circuit import Circuit
from ..utils import Utils


@attr.s(kw_only=True)
class Scenario:
    _circuit = attr.ib(validator=attr.validators.instance_of(Circuit), init=False)
    _dss = attr.ib(validator=attr.validators.instance_of(DSS.DSSDLL), repr=False, init=False)
    _frequency_base = attr.ib(validator=attr.validators.instance_of((int, float)), default=60)
    _name = attr.ib(validator=attr.validators.instance_of(str), default='scenario_' + Utils.generate_random_string())
    _lines = attr.ib(validator=attr.validators.instance_of(pd.DataFrame), init=False)
    _transformers = attr.ib(validator=attr.validators.instance_of(pd.DataFrame), init=False)

    def __attrs_post_init__(self):
        self._dss = DSS.DSSDLL()
        self._circuit = Circuit()
        self._name = Utils.remove_blank_spaces(self._name)
        self._lines = pd.DataFrame(columns=Line.columns_)
        self._transformers = pd.DataFrame(columns=Transformer.columns_)

    def to_dict(self) -> dict:
        return self.__dict__

    def to_list(self) -> list:
        return list(self.__dict__)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        Utils.check_instance(value, 'name', ['str'], )
        self._name = Utils.remove_blank_spaces(value)

    @property
    def lines(self):
        return self._lines

    @lines.setter
    def lines(self, value: Line):
        self._lines = self._lines.append(value.to_dict(), ignore_index=True)

    @property
    def transformers(self):
        return self._transformers

    @transformers.setter
    def transformers(self, value: Transformer):
        self._transformers = self._transformers.append(value.to_dict(), ignore_index=True)

    # # region PD Elements
    # self.__df__auto_trans = pd.DataFrame(columns=AutoTrans.columns_)
    # self.__df__capacitors = pd.DataFrame(columns=Capacitor.columns)
    # self.__df__gic_transformers = pd.DataFrame(columns=GICTransformer.columns)
    # self.__df__lines = pd.DataFrame(columns=Line.columns_)
    # self.__df__reactors = pd.DataFrame(columns=Reactor.columns)
    # self.__df__transformers = pd.DataFrame(columns=Transformer.columns)
    # # endregion
    # # region PC Elements
    # self.__df__generators = pd.DataFrame(columns=Generator.columns)
    # self.__df__generic5 = pd.DataFrame(columns=Generic5.columns)
    # self.__df__giclines = pd.DataFrame(columns=GICLine.columns)
    # self.__df__indmach012 = pd.DataFrame(columns=IndMach012.columns)
    # self.__df__loads = pd.DataFrame(columns=Load.columns)
    # self.__df__pvsystems = pd.DataFrame(columns=PVSystem.columns)
    # self.__df__storages = pd.DataFrame(columns=Storage.columns)
    # self.__df__upfcs = pd.DataFrame(columns=UPFC.columns)
    # self.__df__vccs = pd.DataFrame(columns=VCCS.columns)
    # self.__df__vsconverters = pd.DataFrame(columns=VSConverter.columns)
    # # endregion
    # # region Controls
    # self.__df__cap_controls = pd.DataFrame(columns=CapControl.columns)
    # self.__df__espv_controls = pd.DataFrame(columns=ESPVLControl.columns)
    # self.__df__exp_controls = pd.DataFrame(columns=ExpControl.columns)
    # self.__df__fuses = pd.DataFrame(columns=Fuse.columns)
    # self.__df__gen_dispatchers = pd.DataFrame(columns=GenDispatcher.columns)
    # self.__df__inv_controls = pd.DataFrame(columns=InvControl.columns)
    # self.__df__reg_closers = pd.DataFrame(columns=RegCloser.columns)
    # self.__df__reg_controls = pd.DataFrame(columns=RegControl.columns)
    # self.__df__relays = pd.DataFrame(columns=Relay.columns)
    # self.__df__storage_controllers = pd.DataFrame(columns=StorageController.columns)
    # self.__df__swt_controls = pd.DataFrame(columns=SwtControl.columns)
    # self.__df__upfc_controls = pd.DataFrame(columns=UPFCControl.columns)
    # # endregion
    # # region General
    # self.__df__cn_data = pd.DataFrame(columns=CNData.columns)
    # self.__df__growth_shapes = pd.DataFrame(columns=GrowthShape.columns)
    # self.__df__line_codes = pd.DataFrame(columns=LineCode.columns)
    # self.__df__line_geometries = pd.DataFrame(columns=LineGeometry.columns)
    # self.__df__line_spacings = pd.DataFrame(columns=LineSpacing.columns)
    # self.__df__load_shapes = pd.DataFrame(columns=LoadShape.columns)
    # self.__df__price_shapes = pd.DataFrame(columns=PriceShape.columns)
    # self.__df__spectrums = pd.DataFrame(columns=Spectrum.columns)
    # self.__df__tcc_curves = pd.DataFrame(columns=TCCCurve.columns)
    # self.__df__ts_data = pd.DataFrame(columns=TSData.columns)
    # self.__df__tshapes = pd.DataFrame(columns=TShape.columns)
    # self.__df__wire_data = pd.DataFrame(columns=WireData.columns)
    # self.__df__xfmr_codes = pd.DataFrame(columns=XFMRCode.columns)
    # self.__df__xy_curves = pd.DataFrame(columns=XYCurve.columns)
    # # endregion
    # # region Meters
    # self.__df__energymeters = pd.DataFrame(columns=EnergyMeter.columns)
    # self.__df__f_monitors = pd.DataFrame(columns=FMonitor.columns)
    # self.__df__monitors = pd.DataFrame(columns=Monitor.columns)
    # self.__df__sensors = pd.DataFrame(columns=Sensor.columns)
    # # endregion
    # # region Other
    # self.__df__faults = pd.DataFrame(columns=Fault.columns_)
    # self.__df__gic_sources = pd.DataFrame(columns=GICSource.columns)
    # self.__df__i_sources = pd.DataFrame(columns=ISource.columns)
    # self.__df__v_sources = pd.DataFrame(columns=VSource.columns_)
    # # endregion
    # # Utils
    # # self.buses = Bus(dss).get_buses()

    # @classmethod
    # def instance(cls):
    #     if cls._instance is None:
    #         cls._instance = cls()
    #     return cls._instance

    @property
    def dss(self):
        return self._dss

    @property
    def circuit(self):
        return self._circuit

    @circuit.setter
    def circuit(self, circuit: Circuit):
        self._circuit = circuit

    @staticmethod
    def create_line(line: Line):
        return LineController.save(line)

    @staticmethod
    def create_reactor(reactor: Reactor):
        return ReactorController.save(reactor)
