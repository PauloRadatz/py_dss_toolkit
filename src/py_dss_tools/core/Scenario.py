# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 02/09/2021 at 00:42:09
 Project: py_dss_tools [set, 2021]
"""
from .Circuit import Circuit
from ..utils.Logging import Logging
from ..utils.Utils import Utils

from py_dss_interface import DSS

import pandas as pd


class Scenario:
    id = 0
    log_scene = 'Scenario_Log_' + str(id)

    def __init__(self, **kwargs):
        """
        :param kwargs:
        """
        if Scenario.id > 0:
            print("Only one DSS instance is allowed!")
            exit()
        else:
            self.dss = DSS.DSSDLL()
            self.circuit = Circuit(self.dss)
            Scenario.id = Scenario.id + 1

            self.logger = Logging().logger

            if 'file' in kwargs:
                self.dss_file = kwargs.get('file')
            if 'logging' in kwargs:
                self.logger.disabled = not kwargs.get('logging')

    # def end_scenario(self):
    #     Scenario.id = 0
    #     self.logger.info(f"{self.end_scenario.__name__} - Ending simulation of {self.log_scene}")
    #
    # def create_scenario_from_file(self):
    #     self.circuit.create_circuit(self.dss_file)
    #
    # def create_scenario(self, **kwargs):
    #     name = 'My_Circuit'
    #     if 'name' in kwargs:
    #         name = kwargs.get('name')
    #     self.dss.text("new circuit.{0}".format(name))
    #
    # def solve_scenario(self):
    #     self.dss.text("solve")
    #
    # def summary(self):
    #     result = self.dss.text("summary")
    #     result = result.split('\r')
    #     aux = dict()
    #     for n in range(len(result)):
    #         try:
    #             result[n] = result[n].split('\n')[1]
    #         except Exception as e:
    #             self.logger.warning(f" from function {self.summary.__name__}  - {e} - in line "
    #                                 f"{Utils.get_linenumber()}")
    #         try:
    #             aux[str(result[n].split('=')[0])] = [str(result[n].split('=')[1])]
    #         except Exception as e:
    #             try:
    #                 aux[str(result[n].split(':')[0])] = [str(result[n].split(':')[1])]
    #             except Exception as e:
    #                 self.logger.warning(f" from function {self.summary.__name__}  - {e} - in line "
    #                                     f"{Utils.get_linenumber()}")
    #     return pd.DataFrame.from_dict(aux)
    #
    # def select(self, type_, element):
    #     """
    #     :param type_: Element type like Line, Transformer, LineCode...
    #     :param element: Name of element like trafoMM, line650...
    #     :return:
    #     """
    #     self.dss.text("select {0}.{1}".format(type_, element))
    #     self.solve_scenario()
    #
    # def clear_all(self):
    #     """
    #     Clears all the circuits and all the actors, after this instruction there will be only 1 actor (actor 1) and
    #     will be the active actor.
    #     :return:
    #     """
    #     self.dss.text("clearall")
    #
    # def clear(self):
    #     """
    #     Clear all circuits currently in memory.
    #     :return:
    #     """
    #     self.dss.text("clear")
    #
    # def clone_circuit(self):
    #     """
    #     Clones the active circuit. This command creates as many copies of the active cirucit as indicated in the
    #     argument if the number of requested clones does not overpasses the number of local CPUs. The form of this
    #     command is clone X whereX is the number of clones to be created.
    #     :return:
    #     """
    #     self.dss.text("clone")
    #
    # def create_line(self):
    #     pass
    #
    # def create_transformer(self):
    #     pass
    #
    # def create_pv_system(self):
    #     pass
    #
    # def losses(self):
    #     """
    #     :return: Active and Reactive losses at active circuit in kW.
    #     """
    #     aux = self.dss.text("cktlosses").strip().replace(" ", "").split(sep=",")
    #     losses = list()
    #     losses.append(float(aux[0]))
    #     losses.append(float(aux[1]))
    #     return losses
    #
    # def max_iterations(self, max_: int):
    #     self.dss.text("set maxiterations {0}".format(int(max_)))
    #
    # def max_control_iterations(self, max_: int):
    #     self.dss.text("set maxcontrolit {0}".format(int(max_)))
    #
    # def load_mult(self, max_: float):
    #     self.dss.text("set loadmult {0}".format(float(max_)))
    #
    # def help(self):
    #     return self.dss.text("help")
    #
    # def about(self):
    #     return self.dss.text("about")
    #
    def line_exist(self):
        pass
