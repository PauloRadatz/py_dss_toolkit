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


@dataclass(kw_only=True)
class StudyGeneric(StudyBase):
    def __post_init__(self):
        super().__post_init__()
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
