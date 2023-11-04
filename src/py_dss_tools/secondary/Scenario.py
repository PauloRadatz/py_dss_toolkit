# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 02/09/2021 at 00:42:09
 Project: py_dss_tools [set, 2021]
"""
import attr
import pandas as pd
from py_dss_interface import DSS


from ..utils import Utils

from py_dss_tools.model.ModelData import ModelData
from py_dss_tools.results.PowerFlowResults import PowerFlowResults
from dataclasses import dataclass, field
from typing import Union, Optional

from py_dss_tools.algorithms.LoadAllocation.load_allocation import LoadAllocation
from py_dss_tools.dss_utils import DSSUtils
from py_dss_tools.visualization.VoltageProfile import VoltageProfile
from py_dss_tools.secondary.StudyBase import StudyBase


# @dataclass(kw_only=True)
class Scenario(StudyBase):
    # _name: str = field(default='scenario_' + Utils.generate_random_string(), init=True, repr=True)
    # _dss_file: str = field(init=True, repr=True)
    # _frequency_base: Union[int, float] = field(default=60, init=True)
    # _dll: str = field(default=None, init=True)
    # _results: PowerFlowResults = field(init=False, repr=False)
    # _modeldata: ModelData = field(init=False, repr=False)

    def __init__(self, name, dss_file, frequency_base=60, dll=None):
        super().__init__(name, dss_file, frequency_base=60, dll=None)
        self._results = PowerFlowResults(_dss=self._dss)

    def to_dict(self) -> dict:
        return self.__dict__

    def to_list(self) -> list:
        return list(self.__dict__)

    @property
    def results(self):
        return self._results

    def allocate_load(self):
        load_allocation = LoadAllocation(self)
        load_allocation.run_load_allocation_kw(5000)
        print(load_allocation.get_status())

    def plot_profile(self):
        VoltageProfile(self).plot_profile()

