# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : StudyTemporal.py
# @Software: PyCharm

from py_dss_tools.studies.StudyBase import StudyBase
from py_dss_tools.results.Temporal.TemporalResults import TemporalResults
from py_dss_tools.static_view.ViewTemporalResults import ViewTemporalResults
from dataclasses import dataclass

from py_dss_tools.studies.StudyTemporalSettings import StudyTemporalSettings

@dataclass(kw_only=True)
class StudyTemporal(StudyBase):

    def __post_init__(self):
        super().__post_init__()
        self._results = TemporalResults(self._dss)
        self._view = ViewTemporalResults(self._dss, self._results)
        self._settings = StudyTemporalSettings(_dss=self.dss)

    @property
    def results(self):
        return self._results

    @property
    def view(self):
        return self._view

    @property
    def settings(self):
        return self._settings

    def run(self):
        self.__check_settings()
        self.dss.text("solve")

    def __check_settings(self):
        self.settings.mode = self.dss.text("get mode")
