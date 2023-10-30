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

from py_dss_tools.model.ElectricModel import ElectricModel
from dataclasses import dataclass, field
from typing import Union, Optional

@dataclass(kw_only=True)
class Scenario:
    _dss: DSS = field(init=True, repr=False)
    _name: str = field(default='scenario_' + Utils.generate_random_string(), init=True, repr=True)
    _dss_file: str = field(init=True, repr=True)
    _frequency_base: Union[int, float] = field(default=60, init=False)
    _model: Optional[ElectricModel] = field(init=False, repr=False)

    def __post_init__(self):
        self._dss.text(f"compile [{self._dss_file}]")
        self._name = Utils.remove_blank_spaces(self._name)
        self._model = None

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
    def dss(self):
        return self._dss

    @property
    def model(self):
        return self._model

    @staticmethod
    def create_line(line: Line):
        return LineController.save(line)

    @staticmethod
    def create_reactor(reactor: Reactor):
        return ReactorController.save(reactor)

    def create_model_dataframes(self):
        self._model = ElectricModel(_dss=self._dss)
    def update_model_dataframes(self):
        self._model = ElectricModel(_dss=self._dss)

    def dss_command(self, command: str):
        self._dss.text(command)
