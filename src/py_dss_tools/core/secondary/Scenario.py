# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 02/09/2021 at 00:42:09
 Project: py_dss_tools [set, 2021]
"""
from dataclasses import dataclass, field

from py_dss_interface import DSS

from .Circuit import Circuit
from py_dss_tools.core.model.pdelement.Line import Line
from py_dss_tools.core.controller.LineController import LineController
from py_dss_tools.core.model.pdelement.Reactor import Reactor
from py_dss_tools.core.controller.ReactorController import ReactorController


@dataclass
class Scenario:
    # TODO: after OpenDSS library evolved we must add __slots__ here to optimize memory performances
    _instance = None

    __circuit: Circuit = field(init=False)
    __frequency_base: int = 60
    __dss: DSS.DSSDLL = field(init=False, repr=False)

    def __post_init__(self):
        self.__dss = DSS.DSSDLL()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def dss(self):
        return self.__dss

    @property
    def circuit(self):
        return self.__circuit

    @circuit.setter
    def circuit(self, circuit: Circuit):
        self.__circuit = circuit

    @staticmethod
    def create_line(line: Line):
        return LineController.save(line)

    @staticmethod
    def create_reactor(reactor: Reactor):
        return ReactorController.save(reactor)
