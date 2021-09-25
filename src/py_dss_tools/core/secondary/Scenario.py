# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 02/09/2021 at 00:42:09
 Project: py_dss_tools [set, 2021]
"""
from py_dss_interface import DSS

import py_dss_tools
from py_dss_tools import *

from py_dss_tools.core.secondary import Circuit


class Scenario:
    __id = 0
    __created = False

    def __init__(self, name="My Scenario"):

        py_dss_tools.open_dss()
        py_dss_tools.bear()

        if Scenario.__id > 0:
            print("Only one DSS instance is allowed!")
            exit()
        else:
            self.__dss = DSS.DSSDLL()
            print(57 * '_', end="\n\n")

            self.__name = name
            self.__circuit = None

            Scenario.__id += 1
            Scenario.__created = True

    @property
    def dss(self):
        return self.__dss

    @property
    def created(self):
        return Scenario.__created

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def circuit(self):
        return self.__circuit

    @circuit.setter
    def circuit(self, value: Circuit):
        self.__circuit = value

    @staticmethod
    def __print_header(element_type):
        print(75 * "#" + " " + element_type.name_plural + " " + 75 * "#")

    # # region PD Elements
    # def print_auto_trans(self):
    #     Scenario.print_header(AutoTrans)
    #     print(self.circuit.auto_trans)
    #
    # def print_capacitors(self):
    #     Scenario.print_header(Capacitor)
    #     print(self.circuit.capacitors)
    #
    # def print_gic_transformers(self):
    #     Scenario.print_header(GICTransformer)
    #     print(self.circuit.capacitors)
    #
    # def print_lines(self):
    #     Scenario.print_header(Line)
    #     print(self.circuit.lines)
    #
    # def print_reactors(self):
    #     Scenario.print_header(Reactor)
    #     print(self.circuit.reactors)
    #
    # def print_transformers(self):
    #     Scenario.print_header(Transformer)
    #     print(self.circuit.transformers)
    #
    # def print_pd_elements(self):
    #     self.print_auto_trans()
    #     self.print_capacitors()
    #     self.print_gic_transformers()
    #     self.print_lines()
    #     self.print_reactors()
    #     self.print_transformers()
    #
    # # endregion
    #
    # # region PC Elements
    # def print_generators(self):
    #     Scenario.print_header(Generator)
    #     print(self.circuit.generators)
    #
    # def print_generic5(self):
    #     Scenario.print_header(Generic5)
    #     print(self.circuit.generic5)
    #
    # def print_giclines(self):
    #     Scenario.print_header(GICLine)
    #     print(self.circuit.giclines)
    #
    # def print_indmach012(self):
    #     Scenario.print_header(IndMach012)
    #     print(self.circuit.indmach012)
    #
    # def print_loads(self):
    #     Scenario.print_header(Load)
    #     print(self.circuit.loads)
    #
    # def print_pvsystems(self):
    #     Scenario.print_header(PVSystem)
    #     print(self.circuit.pvsystems)
    #
    # def print_storages(self):
    #     Scenario.print_header(Storage)
    #     print(self.circuit.storages)
    #
    # def print_upfcs(self):
    #     Scenario.print_header(UPFC)
    #     print(self.circuit.upfcs)
    #
    # def print_vccs(self):
    #     Scenario.print_header(VCCS)
    #     print(self.circuit.vccs)
    #
    # def print_vsconverters(self):
    #     Scenario.print_header(VSConverter)
    #     print(self.circuit.vsconverters)
    #
    # def print_pc_elements(self):
    #     self.print_generators()
    #     self.print_generic5()
    #     self.print_giclines()
    #     self.print_indmach012()
    #     self.print_loads()
    #     self.print_pvsystems()
    #     self.print_storages()
    #     self.print_upfcs()
    #     self.print_vccs()
    #     self.print_vsconverters()
    #
    # # endregion
    #
    # # region Controls
    # def print_cap_controls(self):
    #     Scenario.print_header(CapControl)
    #     print(self.circuit.cap_controls)
    #
    # def print_espv_controls(self):
    #     Scenario.print_header(ESPVLControl)
    #     print(self.circuit.espv_controls)
    #
    # def print_exp_controls(self):
    #     Scenario.print_header(ExpControl)
    #     print(self.circuit.exp_controls)
    #
    # def print_fuses(self):
    #     Scenario.print_header(Fuse)
    #     print(self.circuit.fuses)
    #
    # def print_gen_dispatchers(self):
    #     Scenario.print_header(GenDispatcher)
    #     print(self.circuit.gen_dispatchers)
    #
    # def print_inv_controls(self):
    #     Scenario.print_header(InvControl)
    #     print(self.circuit.inv_controls)
    #
    # def print_reg_closers(self):
    #     Scenario.print_header(RegCloser)
    #     print(self.circuit.reg_closers)
    #
    # def print_reg_controls(self):
    #     Scenario.print_header(RegControl)
    #     print(self.circuit.reg_controls)
    #
    # def print_relays(self):
    #     Scenario.print_header(Relay)
    #     print(self.circuit.relays)
    #
    # def print_storage_controllers(self):
    #     Scenario.print_header(StorageController)
    #     print(self.circuit.storage_controllers)
    #
    # def print_swt_controls(self):
    #     Scenario.print_header(SwtControl)
    #     print(self.circuit.swt_controls)
    #
    # def print_upfc_controls(self):
    #     Scenario.print_header(UPFCControl)
    #     print(self.circuit.upfc_controls)
    #
    # def print_controls(self):
    #     self.print_cap_controls()
    #     self.print_espv_controls()
    #     self.print_exp_controls()
    #     self.print_fuses()
    #     self.print_gen_dispatchers()
    #     self.print_inv_controls()
    #     self.print_reg_closers()
    #     self.print_reg_controls()
    #     self.print_relays()
    #     self.print_storage_controllers()
    #     self.print_swt_controls()
    #     self.print_upfc_controls()
    #
    # # endregion
    #
    # # region General
    # def print_cn_data(self):
    #     Scenario.print_header(CNData)
    #     print(self.circuit.cn_data)
    #
    # def print_growth_shapes(self):
    #     Scenario.print_header(GrowthShape)
    #     print(self.circuit.growth_shapes)
    #
    # def print_line_codes(self):
    #     Scenario.print_header(LineCode)
    #     print(self.circuit.line_codes)
    #
    # def print_line_geometries(self):
    #     Scenario.print_header(LineGeometry)
    #     print(self.circuit.line_geometries)
    #
    # def print_line_spacings(self):
    #     Scenario.print_header(LineSpacing)
    #     print(self.circuit.line_spacings)
    #
    # def print_load_shapes(self):
    #     Scenario.print_header(LoadShape)
    #     print(self.circuit.load_shapes)
    #
    # def print_price_shapes(self):
    #     Scenario.print_header(PriceShape)
    #     print(self.circuit.price_shapes)
    #
    # def print_spectrums(self):
    #     Scenario.print_header(Spectrum)
    #     print(self.circuit.spectrums)
    #
    # def print_tcc_curves(self):
    #     Scenario.print_header(TCCCurve)
    #     print(self.circuit.tcc_curves)
    #
    # def print_ts_data(self):
    #     Scenario.print_header(TSData)
    #     print(self.circuit.ts_data)
    #
    # def print_tshapes(self):
    #     Scenario.print_header(TShape)
    #     print(self.circuit.tshapes)
    #
    # def print_wire_data(self):
    #     Scenario.print_header(WireData)
    #     print(self.circuit.wire_data)
    #
    # def print_xfmr_codes(self):
    #     Scenario.print_header(XFMRCode)
    #     print(self.circuit.xfmr_codes)
    #
    # def print_xy_curves(self):
    #     Scenario.print_header(XYCurve)
    #     print(self.circuit.xy_curves)
    #
    # def print_generals(self):
    #     self.print_cn_data()
    #     self.print_growth_shapes()
    #     self.print_line_codes()
    #     self.print_line_geometries()
    #     self.print_line_spacings()
    #     self.print_load_shapes()
    #     self.print_price_shapes()
    #     self.print_spectrums()
    #     self.print_tcc_curves()
    #     self.print_ts_data()
    #     self.print_tshapes()
    #     self.print_wire_data()
    #     self.print_xfmr_codes()
    #     self.print_xy_curves()
    #
    # # endregion
    #
    # # region Meters
    # def print_energymeters(self):
    #     Scenario.print_header(EnergyMeter)
    #     print(self.circuit.energymeters)
    #
    # def print_f_monitors(self):
    #     Scenario.print_header(FMonitor)
    #     print(self.circuit.f_monitors)
    #
    # def print_monitors(self):
    #     Scenario.print_header(Monitor)
    #     print(self.circuit.monitors)
    #
    # def print_sensors(self):
    #     Scenario.print_header(Sensor)
    #     print(self.circuit.sensors)
    #
    # def print_meters(self):
    #     self.print_energymeters()
    #     self.print_f_monitors()
    #     self.print_monitors()
    #     self.print_sensors()
    #
    # # endregion
    #
    # # region Other
    # def print_faults(self):
    #     Scenario.print_header(Fault)
    #     print(self.circuit.faults)
    #
    # def print_gic_sources(self):
    #     Scenario.print_header(GICSource)
    #     print(self.circuit.gic_sources)
    #
    # def print_i_sources(self):
    #     Scenario.print_header(ISource)
    #     print(self.circuit.i_sources)
    #
    # def print_v_sources(self):
    #     Scenario.print_header(VSource)
    #     print(self.circuit.v_sources)
    #
    # def print_others(self):
    #     self.print_faults()
    #     self.print_gic_sources()
    #     self.print_i_sources()
    #     self.print_v_sources()
    #
    # # endregion

    # @property
    # def circuit(self):
    #     return self.__circuit
