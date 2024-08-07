# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : PowerFlow.py
# @Software: PyCharm

from py_dss_tools.studies.StudyBase import StudyBase
from py_dss_tools.results.Static.StaticResults import StaticResults
from py_dss_tools.view.ViewStaticResults import ViewStaticResults
from dataclasses import dataclass

from py_dss_tools.studies.StudyPowerFlowSettings import StudyPowerFlowSettings

@dataclass(kw_only=True)
class StudyPowerFlow(StudyBase):

    def __post_init__(self):
        super().__post_init__()
        self._results = StaticResults(self._dss)
        self._view = ViewStaticResults(self._dss, self._results)
        self._settings = StudyPowerFlowSettings(_dss=self.dss)

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
        if self.settings.mode not in ["snap", "snapshot"]:
            self.settings.number = self.dss.text("get number")

