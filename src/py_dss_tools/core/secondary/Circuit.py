# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 01/09/2021 at 19:51:44
 Project: py_dss_tools [set, 2021]
"""
import pandas as pd
from py_dss_tools.core.pdelement.Capacitor import Capacitor
from py_dss_tools.core.pdelement.GICTransformer import GICTransformer
from py_dss_tools.core.pdelement.Line import Line
from py_dss_tools.core.pdelement.Transformer import Transformer


class Circuit:
    id = 0

    def __init__(self, dss):
        if Circuit.id > 0:
            print("Only one Circuit's instance is allowed!")
            exit()
        else:
            Circuit.id = Circuit.id + 1
            self.dss = dss

            # PD Elements
            self.auto_trans = Circuit.__create_df_autofrans()
            self.capacitors = Circuit.__create_df_capacitors()
            self.gic_transformers = Circuit.__create_df_gictransformers()
            self.lines = Circuit.__create_df_lines()
            self.reactors = Circuit.__create_df_reactors()
            self.transformers = Circuit.__create_df_transformers()

            # PC Elements
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

            # Controls
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

            # general
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

            # Meters
            self.energymeters = None
            self.f_monitors = None
            self.monitors = None
            self.sensors = None

            # Other
            self.faults = None
            self.gic_sources = None
            self.i_sources = None
            self.v_sources = None

            # Utils
            # self.buses = Bus(dss).get_buses()

    # PD Elements
    @staticmethod
    def __create_df_autofrans():
        # TODO
        columns = []
        return pd.DataFrame(columns=columns)

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
        columns = ['basefreq', 'bus1', 'bus2', 'conn', 'emergamps', 'enabled', 'faultrate', 'kv', 'kvar', 'lcurve',
                   'like', 'lmh', 'normamps', 'parallel', 'pctperm', 'phases', 'r', 'rcurve', 'repair', 'rmatrix', 'rp',
                   'x', 'xmatrix', 'z', 'z0', 'z1', 'z2']
        return pd.DataFrame(columns=columns)

    @staticmethod
    def __create_df_transformers():
        return pd.DataFrame(columns=Transformer.columns)

    # PC Elements
    @staticmethod
    def __create_df_generators():
        columns = ['%fuel', '%reserve', 'balanced', 'basefreq', 'bus1', 'class', 'conn', 'd', 'daily', 'debugtrace',
                   'dispmode', 'dispvalue', 'duty', 'dutystart', 'enabled', 'forceon', 'fuelkwh', 'h', 'kv', 'kva',
                   'kvar', 'kw', 'like', 'maxkvar', 'minkvar', 'model', 'mva', 'pf', 'phases', 'pvfactor', 'refuel',
                   'rneut', 'shaftdata', 'shaftmodel', 'spectrum', 'status', 'usefuel', 'userdata', 'usermodel',
                   'vmaxpu', 'vminpu', 'vpu', 'xd', 'xdp', 'xdpp', 'xneut', 'xrdp', 'yearly']
        return pd.DataFrame(columns=columns)

    @staticmethod
    def __create_df_generic5():
        columns = ['basefreq', 'bus1', 'cc_switch', 'cluster_num', 'conn', 'ctrl_mode', 'd', 'daily', 'debugtrace',
                   'droop', 'duty', 'enabled', 'h', 'kcd', 'kcq', 'kcq_drp2', 'kqi', 'kv', 'kva', 'kw', 'like',
                   'maxslip', 'p_ref1kw', 'p_ref2kw', 'p_ref3kw', 'p_refkw', 'pbiaskw', 'pf', 'pfctr1', 'pfctr2',
                   'pfctr3', 'pfctr4', 'pfctr5', 'pfctr6', 'phases', 'pmaxkw', 'pminkw', 'pmppkw', 'pqpriority',
                   'q_ref1kvar', 'q_ref2kvar', 'q_ref3kvar', 'q_refkvar', 'qv_flag', 'slipoption', 'spectrum',
                   'v_ref1kvln', 'v_ref2kvln', 'v_ref3kvln', 'v_refkvln', 'volt_trhd', 'yearly']
        return pd.DataFrame(columns=columns)

    @staticmethod
    def __create_df_giclines():
        columns = ['angle', 'basefreq', 'bus1', 'bus2', 'c', 'ee', 'en', 'enabled', 'frequency', 'lat1', 'lat2', 'like',
                   'lon1', 'lon2', 'phases', 'r', 'spectrum', 'volts', 'x']
        return pd.DataFrame(columns=columns)

    @staticmethod
    def __create_df_indmach012():
        columns = ['basefreq', 'bus1', 'conn', 'd', 'daily', 'debugtrace', 'duty', 'enabled', 'h', 'kv', 'kva', 'kw',
                   'like', 'maxslip', 'pf', 'phases', 'purr', 'purs', 'puxm', 'puxr', 'puxs', 'slip', 'slipoption',
                   'spectrum', 'yearly']
        return pd.DataFrame(columns=columns)

    @staticmethod
    def __create_df_loads():
        columns = ['%mean', '%seriesrl', '%stddev', 'allocationfactor', 'basefreq', 'bus1', 'cfactor', 'class', 'conn',
                   'cvrcurve', 'cvrvars', 'cvrwatts', 'daily', 'duty', 'enabled', 'growth', 'kv', 'kva', 'kvar', 'kw',
                   'kwh', 'kwhdays', 'like', 'model', 'numcust', 'pf', 'phases', 'puxharm', 'relweight', 'rneut',
                   'spectrum', 'status', 'vlowpu', 'vmaxpu', 'vminemerg', 'vminnorm', 'vminpu', 'xfkva', 'xneut',
                   'xrharm', 'yearly', 'zipv']
        return pd.DataFrame(columns=columns)

    @staticmethod
    def __create_df_pvsystems():
        columns = ['%cutin', '%cutout', '%pminkvarmax', '%pminnovars', '%pmpp', '%r', '%x', 'balanced', 'basefreq',
                   'bus1', 'class', 'conn', 'daily', 'debugtrace', 'duty', 'dutystart', 'effcurve', 'enabled',
                   'irradiance', 'kv', 'kva', 'kvar', 'kvarmax', 'kvarmaxabs', 'like', 'limitcurrent', 'model', 'pf',
                   'pfpriority', 'phases', 'pmpp', 'p-tcurve', 'spectrum', 'tdaily', 'tduty', 'temperature', 'tyearly',
                   'userdata', 'usermodel', 'varfollowinverter', 'vmaxpu', 'vminpu', 'wattpriority', 'yearly']
        return pd.DataFrame(columns=columns)

    @staticmethod
    def __create_df_storages():
        columns = ['%charge', '%cutin', '%cutout', '%discharge', '%effcharge', '%effdischarge', '%idlingkvar',
                   '%idlingkw', '%kwrated', '%pminkvarmax', '%pminnovars', '%r', '%reserve', '%stored', '%x',
                   'balanced', 'basefreq', 'bus1', 'chargetrigger', 'class', 'conn', 'daily', 'debugtrace',
                   'dischargetrigger', 'dispmode', 'duty', 'dynadata', 'dynadll', 'effcurve', 'enabled', 'kv', 'kva',
                   'kvar', 'kvarmax', 'kvarmaxabs', 'kw', 'kwhrated', 'kwhstored', 'kwrated', 'like', 'limitcurrent',
                   'model', 'pf', 'pfpriority', 'phases', 'spectrum', 'state', 'timechargetrig', 'userdata',
                   'usermodel', 'varfollowinverter', 'vmaxpu', 'vminpu', 'wattpriority', 'yearly']
        return pd.DataFrame(columns=columns)

    @staticmethod
    def __create_df_upfcs():
        columns = ['basefreq', 'bus1', 'bus2', 'climit', 'enabled', 'frequency', 'kvarlimit', 'like', 'losscurve',
                   'mode', 'pf', 'phases', 'refkv', 'refkv2', 'spectrum', 'tol1', 'vhlimit', 'vllimit', 'vpqmax', 'xs']
        return pd.DataFrame(columns=columns)

    @staticmethod
    def __create_df_vccs():
        columns = ['basefreq', 'bp1', 'bp2', 'bus1', 'enabled', 'filter', 'fsample', 'imaxpu', 'irmstau', 'like',
                   'phases', 'ppct', 'prated', 'rmsmode', 'spectrum', 'vrated', 'vrmstau']
        return pd.DataFrame(columns=columns)

    @staticmethod
    def __create_df_vsconverters():
        columns = ['basefreq', 'bus1', 'd0', 'enabled', 'iacmax', 'idcmax', 'kvac', 'kvdc', 'kw', 'like', 'm0', 'mmax',
                   'mmin', 'ndc', 'pacref', 'phases', 'qacref', 'rac', 'spectrum', 'vacref', 'vdcref', 'vscmode', 'xac']
        return pd.DataFrame(columns=columns)

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
