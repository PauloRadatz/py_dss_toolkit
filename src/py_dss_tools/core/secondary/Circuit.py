# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 01/09/2021 at 19:51:44
 Project: py_dss_tools [set, 2021]
"""
import pandas as pd

from py_dss_tools.core import *


class Circuit(VSource):
    __id = 0
    __created = False
    name_ = "Circuit"

    def __init__(self, dss, name, basekv, bus1, pu, phases, angle, mvasc3, mvasc1):
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
            self.__df__auto_trans = Circuit.__create_df_autofrans()
            self.__df__capacitors = Circuit.__create_df_capacitors()
            self.__df__gic_transformers = Circuit.__create_df_gictransformers()
            self.__df__lines = Circuit.__create_df_lines()
            self.__df__reactors = Circuit.__create_df_reactors()
            self.__df__transformers = Circuit.__create_df_transformers()
            # endregion
            # region PC Elements
            self.__df__generators = Circuit.__create_df_generators()
            self.__df__generic5 = Circuit.__create_df_generic5()
            self.__df__giclines = Circuit.__create_df_giclines()
            self.__df__indmach012 = Circuit.__create_df_indmach012()
            self.__df__loads = Circuit.__create_df_loads()
            self.__df__pvsystems = Circuit.__create_df_pvsystems()
            self.__df__storages = Circuit.__create_df_storages()
            self.__df__upfcs = Circuit.__create_df_upfcs()
            self.__df__vccs = Circuit.__create_df_vccs()
            self.__df__vsconverters = Circuit.__create_df_vccs()
            # endregion
            # region Controls
            self.__df__cap_controls = Circuit.__create_df_cap_controls()
            self.__df__espv_controls = Circuit.__create_df_espvcontrols()
            self.__df__exp_controls = Circuit.__create_df_exp_controls()
            self.__df__fuses = Circuit.__create_df_exp_controls()
            self.__df__gen_dispatchers = Circuit.__create_df_gen_dispatchers()
            self.__df__inv_controls = Circuit.__create_df_invcontrols()
            self.__df__reg_closers = Circuit.__create_df_regclosers()
            self.__df__reg_controls = Circuit.__create_df_regcontrols()
            self.__df__relays = Circuit.__create_df_relays()
            self.__df__storage_controllers = Circuit.__create_df_storage_controllers()
            self.__df__swt_controls = Circuit.__create_df_swt_controls()
            self.__df__upfc_controls = Circuit.__create_df_upfc_controls()
            # endregion
            # region General
            self.__df__cn_data = Circuit.__create_df_cndata()
            self.__df__growth_shapes = Circuit.__create_df_growth_shape()
            self.__df__line_codes = Circuit.__create_df_line_codes()
            self.__df__line_geometries = Circuit.__create_df_line_geometries()
            self.__df__line_spacings = Circuit.__create_df_line_spacing()
            self.__df__load_shapes = Circuit.__create_df_load_shapes()
            self.__df__price_shapes = Circuit.__create_df_price_shapes()
            self.__df__spectrums = Circuit.__create_df_spectrums()
            self.__df__tcc_curves = Circuit.__create_df_tcc_curves()
            self.__df__ts_data = Circuit.__create_df_tsdata()
            self.__df__tshapes = Circuit.__create_df_tshapes()
            self.__df__wire_data = Circuit.__create_df_wire_data()
            self.__df__xfmr_codes = Circuit.__create_df_xfmr_codes()
            self.__df__xy_curves = Circuit.__create_df_xy_curves()
            # endregion
            # region Meters
            self.__df__energymeters = Circuit.__create_df_energy_meters()
            self.__df__f_monitors = Circuit.__create_df_f_monitors()
            self.__df__monitors = Circuit.__create_df_monitors()
            self.__df__sensors = Circuit.__create_df_sensors()
            # endregion
            # region Other
            self.__df__faults = Circuit.__create_df_faults()
            self.__df__gic_sources = Circuit.__create_df_gic_sources()
            self.__df__i_sources = Circuit.__create_df_i_sources()
            self.__df__v_sources = Circuit.__create_df_v_sources()
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
    def __create_df_line_codes():
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
        output = ""
        for attrib_name, attrib_value in self.__dict__.items():
            if '_Circuit__df' in attrib_name or 'dss' in attrib_name:
                continue
            else:
                attrib_name = attrib_name.replace("_Other__", "")
                attrib_name = attrib_name.replace("_VSource__", "")
                attrib_name = attrib_name.replace("_Circuit__", "")
                output += f"{attrib_name} = {attrib_value}\n"
        return output
