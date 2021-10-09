# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 01/09/2021 at 19:51:44
 Project: py_dss_tools [set, 2021]
"""
import pandas as pd

from py_dss_tools.core import *
from py_dss_tools.core.model.pdelement.AutoTrans import AutoTrans
from py_dss_tools.core.model.pdelement.Capacitor import Capacitor
from py_dss_tools.core.model.pdelement.GICTransformer import GICTransformer
from py_dss_tools.core.model.pdelement.Line import Line
from py_dss_tools.core.model.pdelement.Reactor import Reactor
from py_dss_tools.core.model.pdelement.Transformer import Transformer


class Circuit(VSource):
    __id = 0
    __created = False
    name_ = "Circuit"

    # TODO: [URGENTE] refatorar classe Circuit completamente
    def __init__(self, dss, name: str, basekv: [int, float], bus1: str, pu: [int, float], phases: int,
                 angle: [int, float], mvasc3: [int, float], mvasc1: [int, float]):
        super().__init__()
        if Circuit.__id > 0:
            print("Only one Circuit's instance is allowed!")
            exit()
        else:
            Circuit.__id += 1
            Circuit.__created = True
            self.__dss = dss

            self.__name = name
            self.__basekv = basekv
            self.__pu = pu
            self.__phases = phases
            self.__bus1 = bus1
            self.__angle = angle
            self.__mvasc3 = mvasc3
            self.__mvasc1 = mvasc1

            # region PD Elements
            self.__df__auto_trans = pd.DataFrame(columns=AutoTrans.columns)
            self.__df__capacitors = pd.DataFrame(columns=Capacitor.columns)
            self.__df__gic_transformers = pd.DataFrame(columns=GICTransformer.columns)
            self.__df__lines = pd.DataFrame(columns=Line.columns_)
            self.__df__reactors = pd.DataFrame(columns=Reactor.columns)
            self.__df__transformers = pd.DataFrame(columns=Transformer.columns)
            # endregion
            # region PC Elements
            self.__df__generators = pd.DataFrame(columns=Generator.columns)
            self.__df__generic5 = pd.DataFrame(columns=Generic5.columns)
            self.__df__giclines = pd.DataFrame(columns=GICLine.columns)
            self.__df__indmach012 = pd.DataFrame(columns=IndMach012.columns)
            self.__df__loads = pd.DataFrame(columns=Load.columns)
            self.__df__pvsystems = pd.DataFrame(columns=PVSystem.columns)
            self.__df__storages = pd.DataFrame(columns=Storage.columns)
            self.__df__upfcs = pd.DataFrame(columns=UPFC.columns)
            self.__df__vccs = pd.DataFrame(columns=VCCS.columns)
            self.__df__vsconverters = pd.DataFrame(columns=VSConverter.columns)
            # endregion
            # region Controls
            self.__df__cap_controls = pd.DataFrame(columns=CapControl.columns)
            self.__df__espv_controls = pd.DataFrame(columns=ESPVLControl.columns)
            self.__df__exp_controls = pd.DataFrame(columns=ExpControl.columns)
            self.__df__fuses = pd.DataFrame(columns=Fuse.columns)
            self.__df__gen_dispatchers = pd.DataFrame(columns=GenDispatcher.columns)
            self.__df__inv_controls = pd.DataFrame(columns=InvControl.columns)
            self.__df__reg_closers = pd.DataFrame(columns=RegCloser.columns)
            self.__df__reg_controls = pd.DataFrame(columns=RegControl.columns)
            self.__df__relays = pd.DataFrame(columns=Relay.columns)
            self.__df__storage_controllers = pd.DataFrame(columns=StorageController.columns)
            self.__df__swt_controls = pd.DataFrame(columns=SwtControl.columns)
            self.__df__upfc_controls = pd.DataFrame(columns=UPFCControl.columns)
            # endregion
            # region General
            self.__df__cn_data = pd.DataFrame(columns=CNData.columns)
            self.__df__growth_shapes = pd.DataFrame(columns=GrowthShape.columns)
            self.__df__line_codes = pd.DataFrame(columns=LineCode.columns)
            self.__df__line_geometries = pd.DataFrame(columns=LineGeometry.columns)
            self.__df__line_spacings = pd.DataFrame(columns=LineSpacing.columns)
            self.__df__load_shapes = pd.DataFrame(columns=LoadShape.columns)
            self.__df__price_shapes = pd.DataFrame(columns=PriceShape.columns)
            self.__df__spectrums = pd.DataFrame(columns=Spectrum.columns)
            self.__df__tcc_curves = pd.DataFrame(columns=TCCCurve.columns)
            self.__df__ts_data = pd.DataFrame(columns=TSData.columns)
            self.__df__tshapes = pd.DataFrame(columns=TShape.columns)
            self.__df__wire_data = pd.DataFrame(columns=WireData.columns)
            self.__df__xfmr_codes = pd.DataFrame(columns=XFMRCode.columns)
            self.__df__xy_curves = pd.DataFrame(columns=XYCurve.columns)
            # endregion
            # region Meters
            self.__df__energymeters = pd.DataFrame(columns=EnergyMeter.columns)
            self.__df__f_monitors = pd.DataFrame(columns=FMonitor.columns)
            self.__df__monitors = pd.DataFrame(columns=Monitor.columns)
            self.__df__sensors = pd.DataFrame(columns=Sensor.columns)
            # endregion
            # region Other
            self.__df__faults = pd.DataFrame(columns=Fault.columns)
            self.__df__gic_sources = pd.DataFrame(columns=GICSource.columns)
            self.__df__i_sources = pd.DataFrame(columns=ISource.columns)
            self.__df__v_sources = pd.DataFrame(columns=VSource.columns)
            # endregion
            # Utils
            # self.buses = Bus(dss).get_buses()

    @property
    def dss(self):
        return self.__dss

    @property
    def created(self):
        return Circuit.__created

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def basekv(self):
        return self.__basekv

    @basekv.setter
    def basekv(self, value):
        self.__basekv = value

    @property
    def phases(self):
        return self.__phases

    @phases.setter
    def phases(self, value):
        self.__phases = value

    @property
    def df_lines(self):
        return self.__df__lines

    @df_lines.setter
    def df_lines(self, value):
        a_series = pd.Series(value, index=self.__df__lines.columns)
        self.__df__lines = self.__df__lines.append(a_series, ignore_index=True)

    # def create_circuit(self, dss_file):
    #     self.dss.text("compile [{}]".format(dss_file))
    #
    # def get_all_buses(self):
    #     buses = Bus(self.dss)
    #     return buses.get_buses()

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

    # def __str__(self):
    #     output = ""
    #     for _, var in vars(self).items():
    #         output += str(var)
    #     return output

    def __str__(self):
        return "".join(
            f"{attrib_name} = {attrib_value}\n"
            for attrib_name, attrib_value in self.__dict__.items()
            if '_Circuit__df' not in attrib_name and 'dss' not in attrib_name
        )
