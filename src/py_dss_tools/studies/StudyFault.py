# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : StudyFault.py
# @Software: PyCharm

from py_dss_tools.studies.StudyBase import StudyBase
from py_dss_tools.results.FaultResults import FaultResults
from py_dss_tools.view.ViewFaultStudy import ViewFaultResults
from dataclasses import dataclass

# from py_dss_tools.studies.StudyTemporalSettings import StudyTemporalSettings

@dataclass(kw_only=True)
class StudyFault(StudyBase):

    def __post_init__(self):
        super().__post_init__()
        self._results = FaultResults(self._dss)
        self._view = ViewFaultResults(self._dss, self._results)
    #     self._settings = StudyTemporalSettings(_dss=self.dss)
    @property
    def results(self):
        return self._results

    @property
    def view(self):
        return self._view
    #
    # @property
    # def settings(self):
    #     return self._settings
    #
    # def run(self):
    #     self.__check_settings()
    #     self.dss.text("solve")
    #
    # def __check_settings(self):
    #     self.settings.mode = self.dss.text("get mode")
