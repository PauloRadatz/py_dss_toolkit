# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 02/09/2021 at 00:42:09
 Project: py_dss_tools [set, 2021]
"""

from py_dss_tools.results.Results import Results
from dataclasses import dataclass

from py_dss_tools.studies.StudyBase import StudyBase
from py_dss_tools.view.ViewResults import ViewResults
from py_dss_tools.dss_tools import DSSTools


@dataclass(kw_only=True)
class StudyGeneric(StudyBase):
    def __post_init__(self):
        super().__post_init__()
        self._results = Results(self._dss)
        self._view = ViewResults(self._dss, self._results)
        # self._utils = DSSTools(self._dss)

    def to_dict(self) -> dict:
        return self.__dict__

    def to_list(self) -> list:
        return list(self.__dict__)

    # @property
    # def utils(self):
    #     return self._utils

    @property
    def results(self):
        return self._results

    @property
    def view(self):
        return self._view

    # def allocate_load(self):
    #     load_allocation = LoadAllocation(self)
    #     load_allocation.run_load_allocation_kw(5000)
    #     print(load_allocation.get_status())
    #
    # def plot_profile(self):
    #     VoltageProfile(self).plot_profile()
