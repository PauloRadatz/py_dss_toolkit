# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 01/09/2021 at 19:51:44
 Project: py_dss_tools [set, 2021]
"""
import pandas as pd

from py_dss_tools.core.pcelement.Generator import Generator
from py_dss_tools.core.pcelement.Generic5 import Generic5
from py_dss_tools.core.pcelement.GICLine import GICLine
from py_dss_tools.core.pcelement.IndMach012 import IndMach012
from py_dss_tools.core.pcelement.Load import Load
from py_dss_tools.core.pcelement.PVSystem import PVSystem
from py_dss_tools.core.pcelement.Storage import Storage
from py_dss_tools.core.pcelement.UPFC import UPFC
from py_dss_tools.core.pcelement.VCCS import VCCS
from py_dss_tools.core.pcelement.VSConverter import VSConverter

from py_dss_tools.core.pdelement.AutoTrans import AutoTrans
from py_dss_tools.core.pdelement.Capacitor import Capacitor
from py_dss_tools.core.pdelement.GICTransformer import GICTransformer
from py_dss_tools.core.pdelement.Line import Line
from py_dss_tools.core.pdelement.Reactor import Reactor
from py_dss_tools.core.pdelement.Transformer import Transformer

from py_dss_tools.core.control.CapControl import CapControl
from py_dss_tools.core.control.ESPVLControl import ESPVLControl
from py_dss_tools.core.control.ExpControl import ExpControl
from py_dss_tools.core.control.Fuse import Fuse
from py_dss_tools.core.control.GenDispatcher import GenDispatcher
from py_dss_tools.core.control.InvControl import InvControl
from py_dss_tools.core.control.RegCloser import RegCloser
from py_dss_tools.core.control.RegControl import RegControl
from py_dss_tools.core.control.Relay import Relay
from py_dss_tools.core.control.StorageController import StorageController
from py_dss_tools.core.control.SwtControl import SwtControl
from py_dss_tools.core.control.UPFCControl import UPFCControl

from py_dss_tools.core.general.CNData import CNData
from py_dss_tools.core.general.GrowthShape import GrowthShape
from py_dss_tools.core.general.LineCode import LineCode
from py_dss_tools.core.general.LineGeometry import LineGeometry
from py_dss_tools.core.general.LineSpacing import LineSpacing
from py_dss_tools.core.general.LoadShape import LoadShape
from py_dss_tools.core.general.PriceShape import PriceShape
from py_dss_tools.core.general.Spectrum import Spectrum
from py_dss_tools.core.general.TCCCurve import TCCCurve
from py_dss_tools.core.general.TSData import TSData
from py_dss_tools.core.general.TShape import TShape
from py_dss_tools.core.general.WireData import WireData
from py_dss_tools.core.general.XFMRCode import XFMRCode
from py_dss_tools.core.general.XYCurve import XYCurve

from py_dss_tools.core.meters.EnergyMeter import EnergyMeter
from py_dss_tools.core.meters.FMonitor import FMonitor
from py_dss_tools.core.meters.Monitor import Monitor
from py_dss_tools.core.meters.Sensor import Sensor

from py_dss_tools.core.other.Fault import Fault
from py_dss_tools.core.other.GICSource import GICSource
from py_dss_tools.core.other.ISource import ISource
from py_dss_tools.core.other.VSource import VSource


class Circuit(VSource):
    id = 0
    name = "Circuit"

    def __init__(self, dss):
        super().__init__()
        if Circuit.id > 0:
            print("Only one Circuit's instance is allowed!")
            exit()
        else:
            Circuit.id = Circuit.id + 1
            self.dss = dss

            # region PD Elements
            self.auto_trans = Circuit.__create_df_autofrans()
            self.capacitors = Circuit.__create_df_capacitors()
            self.gic_transformers = Circuit.__create_df_gictransformers()
            self.lines = Circuit.__create_df_lines()
            self.reactors = Circuit.__create_df_reactors()
            self.transformers = Circuit.__create_df_transformers()
            # endregion
            # region PC Elements
            self.generators = Circuit.__create_df_generators()
            self.generic5 = Circuit.__create_df_generic5()
            self.giclines = Circuit.__create_df_giclines()
            self.indmach012 = Circuit.__create_df_indmach012()
            self.loads = Circuit.__create_df_loads()
            self.pvsystems = Circuit.__create_df_pvsystems()
            self.storages = Circuit.__create_df_storages()
            self.upfcs = Circuit.__create_df_upfcs()
            self.vccs = Circuit.__create_df_vccs()
            self.vsconverters = Circuit.__create_df_vccs()
            # endregion
            # region Controls
            self.cap_controls = None
            self.espv_controls = None
            self.exp_controls = None
            self.fuses = None
            self.gen_dispatchers = None
            self.inv_controls = None
            self.reg_closers = None
            self.reg_controls = None
            self.relays = None
            self.storage_controllers = None
            self.swt_controls = None
            self.upfc_controls = None
            # endregion
            # region General
            self.cn_data = None
            self.growth_shapes = None
            self.line_codes = None
            self.line_geometries = None
            self.line_spacings = None
            self.load_shapes = None
            self.price_shapes = None
            self.spectrums = None
            self.tcc_curves = None
            self.ts_data = None
            self.tshapes = None
            self.wire_data = None
            self.xfmr_codes = None
            self.xy_curves = None
            # endregion
            # region Meters
            self.energymeters = None
            self.f_monitors = None
            self.monitors = None
            self.sensors = None
            # endregion
            # region Other
            self.faults = None
            self.gic_sources = None
            self.i_sources = None
            self.v_sources = None
            # endregion
            # Utils
            # self.buses = Bus(dss).get_buses()

    # region PD Elements
    @staticmethod
    def __create_df_autofrans():
        return pd.DataFrame(columns=AutoTrans.columns)

    @staticmethod
    def __create_df_capacitors():
        return pd.DataFrame(columns=Capacitor.columns)

    @staticmethod
    def __create_df_gictransformers():
        return pd.DataFrame(columns=GICTransformer.columns)

    @staticmethod
    def __create_df_lines():
        return pd.DataFrame(columns=Line.columns)

    @staticmethod
    def __create_df_reactors():
        return pd.DataFrame(columns=Reactor.columns)

    @staticmethod
    def __create_df_transformers():
        return pd.DataFrame(columns=Transformer.columns)

    # endregion

    # region PC Elements
    @staticmethod
    def __create_df_generators():
        return pd.DataFrame(columns=Generator.columns)

    @staticmethod
    def __create_df_generic5():
        return pd.DataFrame(columns=Generic5.columns)

    @staticmethod
    def __create_df_giclines():
        return pd.DataFrame(columns=GICLine.columns)

    @staticmethod
    def __create_df_indmach012():
        return pd.DataFrame(columns=IndMach012.columns)

    @staticmethod
    def __create_df_loads():
        return pd.DataFrame(columns=Load.columns)

    @staticmethod
    def __create_df_pvsystems():
        return pd.DataFrame(columns=PVSystem.columns)

    @staticmethod
    def __create_df_storages():
        return pd.DataFrame(columns=Storage.columns)

    @staticmethod
    def __create_df_upfcs():
        return pd.DataFrame(columns=UPFC.columns)

    @staticmethod
    def __create_df_vccs():
        return pd.DataFrame(columns=VCCS.columns)

    @staticmethod
    def __create_df_vsconverters():
        return pd.DataFrame(columns=VSConverter.columns)

    # endregion

    # region Controls
    @staticmethod
    def __create_df_cap_controls():
        return pd.DataFrame(columns=CapControl.columns)

    @staticmethod
    def __create_df_espvcontrols():
        return pd.DataFrame(columns=ESPVLControl.columns)

    @staticmethod
    def __create_df_exp_controls():
        return pd.DataFrame(columns=ExpControl.columns)

    @staticmethod
    def __create_df_fuses():
        return pd.DataFrame(columns=Fuse.columns)

    @staticmethod
    def __create_df_gen_dispatchers():
        return pd.DataFrame(columns=GenDispatcher.columns)

    @staticmethod
    def __create_df_invcontrols():
        return pd.DataFrame(columns=InvControl.columns)

    @staticmethod
    def __create_df_regclosers():
        return pd.DataFrame(columns=RegCloser.columns)

    @staticmethod
    def __create_df_regcontrols():
        return pd.DataFrame(columns=RegControl.columns)

    @staticmethod
    def __create_df_relays():
        return pd.DataFrame(columns=Relay.columns)

    @staticmethod
    def __create_df_storage_controllers():
        return pd.DataFrame(columns=StorageController.columns)

    @staticmethod
    def __create_df_swt_controls():
        return pd.DataFrame(columns=SwtControl.columns)

    @staticmethod
    def __create_df_upfc_controls():
        return pd.DataFrame(columns=UPFCControl.columns)

    # endregion

    # region General
    @staticmethod
    def __create_df_cndata():
        return pd.DataFrame(columns=CNData.columns)

    @staticmethod
    def __create_df_growth_shape():
        return pd.DataFrame(columns=GrowthShape.columns)

    @staticmethod
    def __create_df_():
        return pd.DataFrame(columns=LineCode.columns)

    @staticmethod
    def __create_df_line_geometries():
        return pd.DataFrame(columns=LineGeometry.columns)

    @staticmethod
    def __create_df_line_spacing():
        return pd.DataFrame(columns=LineSpacing.columns)

    @staticmethod
    def __create_df_load_shapes():
        return pd.DataFrame(columns=LoadShape.columns)

    @staticmethod
    def __create_df_price_shapes():
        return pd.DataFrame(columns=PriceShape.columns)

    @staticmethod
    def __create_df_spectrums():
        return pd.DataFrame(columns=Spectrum.columns)

    @staticmethod
    def __create_df_tcc_curves():
        return pd.DataFrame(columns=TCCCurve.columns)

    @staticmethod
    def __create_df_tsdata():
        return pd.DataFrame(columns=TSData.columns)

    @staticmethod
    def __create_df_tshapes():
        return pd.DataFrame(columns=TShape.columns)

    @staticmethod
    def __create_df_wire_data():
        return pd.DataFrame(columns=WireData.columns)

    @staticmethod
    def __create_df_xfmr_codes():
        return pd.DataFrame(columns=XFMRCode.columns)

    @staticmethod
    def __create_df_xy_curves():
        return pd.DataFrame(columns=XYCurve.columns)

    # endregion

    # region Meters
    @staticmethod
    def __create_df_energy_meters():
        return pd.DataFrame(columns=EnergyMeter.columns)

    @staticmethod
    def __create_df_f_monitors():
        return pd.DataFrame(columns=FMonitor.columns)

    @staticmethod
    def __create_df_monitors():
        return pd.DataFrame(columns=Monitor.columns)

    @staticmethod
    def __create_df_sensors():
        return pd.DataFrame(columns=Sensor.columns)

    # endregion

    # region Other
    @staticmethod
    def __create_df_faults():
        return pd.DataFrame(columns=Fault.columns)
    @staticmethod
    def __create_df_gic_sources():
        return pd.DataFrame(columns=GICSource.columns)
    @staticmethod
    def __create_df_i_sources():
        return pd.DataFrame(columns=ISource.columns)
    @staticmethod
    def __create_df_v_sources():
        return pd.DataFrame(columns=VSource.columns)
    # endregion

    # def create_circuit(self, dss_file):
    #     self.dss.text("compile [{}]".format(dss_file))
    #
    # def get_all_buses(self):
    #     buses = Bus(self.dss)
    #     return buses.get_buses()

    # print(dss.circuit_name())
    # print(dss.circuit_num_ckt_elements())
    # print(dss.circuit_num_buses())
    # print(dss.circuit_num_nodes())
    # print(dss.circuit_all_bus_volts())
    # print(dss.circuit_all_element_names())
    # print(dss.circuit_all_bus_names())
    # print(dss.cktelement_read_display())
    # print(dss.bus_voltages())
    # print(dss.bus_line_list())

    # def get_all_lines(self):
    #     self.dss.lines_first()
    #     while self.dss.lines_next() != 0:
    #         print(self.dss.lines_read_phases())
    #         print(self.dss.lines_read_units())
    #
    # def reset(self):
    #     """
    #     Resets all Monitors, Energymeters, etc. If no argument specified, resets all options listed.
    #     :return:
    #     """
    #     self.dss.text("reset")
    #
    # def sample(self):
    #     """
    #     Force all monitors and meters to take a sample for the most recent solution. Keep in mind that meters will
    #     perform integration.
    #     :return:
    #     """
    #     self.dss.text("sample")
    #
    # def seq_currents(self):
    #     """
    #     Returns the sequence currents into all terminals of the active circuit element (see Select command) in Result
    #     string.  Returned as comma-separated magnitude only values.Order of returned values: 0, 1, 2  (for each
    #     terminal).
    #     :return:
    #     """
    #     aux = self.dss.text("seqcurrents").strip().replace(" ", "").split(sep=",")
    #     seq_currents = list()
    #     for n in range(len(aux)):
    #         if aux[n] != '':
    #             seq_currents.append(float(aux[n]))
    #     return seq_currents
    #
    # def seq_powers(self):
    #     """
    #     Returns the sequence powers into all terminals of the active circuit element (see Select command) in Result
    #     string.  Returned as comma-separated kw, kvar pairs.Order of returned values: 0, 1, 2  (for each terminal).
    #     :return:
    #     """
    #     aux = self.dss.text("seqpowers").strip().replace(" ", "").split(sep=",")
    #     seq_powers = list()
    #     for n in range(len(aux)):
    #         if aux[n] != '':
    #             seq_powers.append(float(aux[n]))
    #     return seq_powers
    #
    # def seq_voltages(self):
    #     """
    #     Returns the sequence voltages at all terminals of the active circuit element (see Select command) in Result
    #     string.  Returned as comma-separated magnitude only values.Order of returned values: 0, 1, 2  (for each
    #     terminal).
    #     :return:
    #     """
    #     aux = self.dss.text("seqvoltages").strip().replace(" ", "").split(sep=",")
    #     seq_voltages = list()
    #     for n in range(len(aux)):
    #         if aux[n] != '':
    #             seq_voltages.append(float(aux[n]))
    #     return seq_voltages
    #
    # def get_voltages(self):
    #     return self.dss.circuit_allbusvmagpu()
    #
    # def get_voltage_min(self):
    #     v = Circuit.get_voltages(self.dss)
    #     return min(v)
    #
    # def get_voltage_max(self):
    #     v = Circuit.get_voltages(self.dss)
    #     return max(v)
    #
    # def get_active_power(self):
    #     return self.dss.circuit_total_power()[0]
    #
    # def get_reactive_power(self):
    #     return self.dss.circuit_total_power()[1]
    #
    # def create_load(self, **kwargs):
    #     pass
    #
    # def create_transformer(self, **kwargs):
    #     pass
    #
    # def create_line_code(self, **kwargs):
    #     pass
    #
    # def create_line(self, **kwargs):
    #     pass
    #
    # def create_pv_system(self, **kwargs):
    #     pass
    #
    # def create_fuse(self, **kwargs):
    #     pass

    """
    new circuit.5Leg
    ~ bus1=MainBus basekV=230 pu=1.0 isc3=15000 isc1=17000 phases=3 z0=[10, 10] z1=[10, 10] angle=0 mvasc3=200000
    mvasc1=200000
    """
