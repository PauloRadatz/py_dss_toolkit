# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 01/09/2021 at 19:51:44
 Project: py_dss_tools [set, 2021]
"""
import attr
import pandas as pd

from py_dss_tools.model.other import VSource
from py_dss_tools.utils import Utils


@attr.s
class Circuit(VSource):
    _name = attr.ib(validator=attr.validators.instance_of(str), default='')
    _basekv = attr.ib(validator=attr.validators.instance_of((int, float)), default=115)
    _pu = attr.ib(validator=attr.validators.instance_of((int, float)), default=1.001)
    _phases = attr.ib(validator=attr.validators.instance_of(int), default=3)
    _bus1 = attr.ib(validator=attr.validators.instance_of(str), default='')
    _angle = attr.ib(validator=attr.validators.instance_of((int, float)), default=0)
    # TODO Rever default values
    _mvasc3 = attr.ib(validator=attr.validators.instance_of((int, float)), default=21000)
    _mvasc1 = attr.ib(validator=attr.validators.instance_of((int, float)), default=24000)

    # TODO: checar existência de mais de um Circuit no momento da criação

    def __attrs_post_init__(self):
        if self._name != '':
            self._name = Utils.remove_blank_spaces(self._name)
        else:
            self._name = 'my_circuit_' + Utils.generate_random_string()

    def to_dataframe(self):
        return pd.DataFrame.from_records([self.__dict__])

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
    def basekv(self):
        return self._basekv

    @basekv.setter
    def basekv(self, value):
        self._basekv = value

    @property
    def phases(self):
        return self._phases

    @phases.setter
    def phases(self, value):
        self._phases = value

    # @property
    # def df_lines(self):
    #     return self._df_lines

    # @df_lines.setter
    # def df_lines(self, value):
    #     a_series = pd.Series(value, index=self._df_lines.columns)
    #     self._df_lines = self._df_lines.append(a_series, ignore_index=True)

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

    # def _str_(self):
    #     output = ""
    #     for _, var in vars(self).items():
    #         output += str(var)
    #     return output

    # def _str_(self):
    #     return "".join(
    #         f"{attrib_name} = {attrib_value}\n"
    #         for attrib_name, attrib_value in self._dict_.items()
    #         if '_Circuit_df' not in attrib_name and 'dss' not in attrib_name
    #     )
